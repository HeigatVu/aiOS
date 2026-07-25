"""
FastAPI BFF (Backend-For-Frontend) wrapper around hermes-webui server.py.

Starts server.py as a subprocess, reverse-proxies all requests on 127.0.0.1:8788
through a health-gated httpx client, and exposes chat endpoints for Codex/agy.

Architecture: subprocess (NOT threading) — avoids GIL contention between the
sync BaseHTTPRequestHandler and Uvicorn's async event loop.

WARNING: This module uses module-level globals (_proc, _healthy, _client).
Do NOT configure uvicorn with workers > 1 — each worker would spawn its own
hermes-webui subprocess.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import signal
import subprocess
import sys
import time
import pty
import fcntl
import struct
import termios
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from routers import files, management, migrations, notes, terminal, update
from services.paths import RuntimePaths
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

import httpx
import websockets

# ── Configuration ────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RUNTIME_PATHS = RuntimePaths.from_project_root(
    Path(os.environ.get("AIOS_PROJECT_ROOT", PROJECT_ROOT.parent))
)

HERMES_SUB_HOST = os.environ.get("HERMES_SUB_HOST", "127.0.0.1")
HERMES_SUB_PORT = int(os.environ.get("HERMES_SUB_PORT", "8501"))
AGENTMEMORY_BASE_URL = os.environ.get("AGENTMEMORY_BASE_URL", "http://127.0.0.1:3113").rstrip("/")
AGENTMEMORY_SECRET_FILE = Path(
    os.environ.get("AGENTMEMORY_SECRET_FILE", str(RUNTIME_PATHS.state / "credentials" / "agentmemory-viewer-secret"))
)

def _get_writable_hermes_home() -> str:
    h = os.environ.get("HERMES_HOME")
    if h:
        return h
    default_home = Path.home() / ".hermes"
    try:
        default_home.mkdir(parents=True, exist_ok=True)
        test_file = default_home / ".write_test"
        test_file.touch()
        test_file.unlink()
        return str(default_home)
    except Exception:
        fallback = RUNTIME_PATHS.state / "hermes"
        fallback.mkdir(parents=True, exist_ok=True)
        return str(fallback)

HERMES_HOME = _get_writable_hermes_home()
SIDECAR_HOST = os.environ.get("SIDECAR_HOST", "127.0.0.1")
SIDECAR_PORT = int(os.environ.get("SIDECAR_PORT", "8788"))
MAX_PROMPT_LENGTH = int(os.environ.get("SIDECAR_MAX_PROMPT_LENGTH", "16384"))  # 16KB

SERVER_SCRIPT = Path(__file__).resolve().parent.parent / "hermes-webui" / "server.py"
SUBSERVER_LOG = Path(f"/tmp/hermes-subserver-{os.getuid()}.log")

logger = logging.getLogger("bff")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s %(message)s")

# ── Safe environment for chat subprocesses ───────────────────────────────────
# Never pass the full os.environ to chat CLI subprocesses — it may contain
# API keys, tokens, and other secrets that could leak into CLI output.
_CHAT_SAFE_ENV_KEYS = {
    "PATH", "HOME", "USER", "LOGNAME", "SHELL",
    "LANG", "LC_ALL", "LC_CTYPE",
    "TERM", "COLORTERM", "NO_COLOR", "FORCE_COLOR",
    "PYTHONUNBUFFERED",
    "HERMES_HOME",
    "VIRTUAL_ENV", "CONDA_PREFIX", "CONDA_DEFAULT_ENV",
    "TMPDIR", "TEMP", "TMP",
}

_CHAT_SAFE_ENV = {
    k: v for k, v in os.environ.items()
    if k in _CHAT_SAFE_ENV_KEYS or k.startswith(("UV_", "PIP_", "PYTHON"))
}
_CHAT_SAFE_ENV.setdefault("PYTHONUNBUFFERED", "1")
_CHAT_SAFE_ENV.setdefault("TERM", "xterm-256color")
_CHAT_SAFE_ENV.setdefault("COLORTERM", "truecolor")

# ── Workdir validation ───────────────────────────────────────────────────────
_ALLOWED_WORKDIR_ROOTS = [
    Path(HERMES_HOME).resolve(),
    Path.home().resolve(),
    Path("/workspace").resolve(),
    Path("/aiOS-ui").resolve(),
    Path("/tmp").resolve(),
    Path("/outputs").resolve(),
    Path("/my-data").resolve(),
]

# ── Path translation for host-level execution ─────────────────────────────────
def _check_outside_docker() -> bool:
    if Path("/.dockerenv").exists() or Path("/run/.containerenv").exists():
        return False
    try:
        import getpass
        if getpass.getuser() == "ai_user":
            return False
    except Exception:
        pass
    if Path("/workspace").exists() and Path("/home/ai_user").exists():
        return False
    return True

is_outside_docker = _check_outside_docker()

CONTAINER_TO_HOST_MAPPING = {
    "/workspace": RUNTIME_PATHS.workspace,
    "/outputs": RUNTIME_PATHS.outputs,
    "/my-data": RUNTIME_PATHS.data / "my-data",
    "/config-file": PROJECT_ROOT / "config-file",
    "/aiOS-ui": PROJECT_ROOT,
    "/home/ai_user/.agentmemory": RUNTIME_PATHS.state / "agentmemory",
    "/home/ai_user/.hermes": RUNTIME_PATHS.state / "hermes",
    "/home/ai_user/.mimocode": RUNTIME_PATHS.state / "mimocode",
    "/home/ai_user/.agents": RUNTIME_PATHS.state / "agents",
    "/home/ai_user/.iii": RUNTIME_PATHS.state / "iii",
    "/home/ai_user": RUNTIME_PATHS.data / "home_ai_user",
}

if is_outside_docker:
    (RUNTIME_PATHS.data / "home_ai_user").mkdir(parents=True, exist_ok=True)

def _to_host_path(path_str: str) -> Path:
    if not is_outside_docker:
        return Path(path_str)
    normalized = os.path.normpath(path_str)
    for c_prefix, h_path in sorted(CONTAINER_TO_HOST_MAPPING.items(), key=lambda x: len(x[0]), reverse=True):
        if normalized == c_prefix:
            return h_path
        if normalized.startswith(c_prefix.rstrip("/") + "/"):
            rel = os.path.relpath(normalized, c_prefix)
            return h_path / rel
    return Path(normalized)

def _to_container_path(host_path: Path | str) -> str:
    if not is_outside_docker:
        return str(host_path)
    h_abs = Path(host_path).resolve()
    for c_prefix, h_path in sorted(CONTAINER_TO_HOST_MAPPING.items(), key=lambda x: len(str(x[1])), reverse=True):
        h_abs_prefix = h_path.resolve()
        if h_abs == h_abs_prefix:
            return c_prefix
        try:
            rel = h_abs.relative_to(h_abs_prefix)
            return (Path(c_prefix) / rel).as_posix()
        except ValueError:
            continue
    return h_abs.as_posix()


def _validate_workdir(workdir: str) -> Path:
    """Validate workdir is within an allowed root. Returns resolved Path."""
    p = Path(workdir).expanduser().resolve()
    if not p.is_dir():
        raise HTTPException(status_code=400, detail=f"workdir does not exist: {workdir}")
    for root in _ALLOWED_WORKDIR_ROOTS:
        try:
            p.relative_to(root)
            return p
        except ValueError:
            continue
    raise HTTPException(status_code=403, detail=f"workdir not in allowed paths: {workdir}")


# ── SSE escaping ─────────────────────────────────────────────────────────────
# SSE field names: 'data', 'event', 'id', 'retry'. Lines starting with ':' are comments.
# We must prevent CLI output from injecting control fields.
_SSE_CONTROL_RE = re.compile(r"^(data|event|id|retry):\s*|^:", re.MULTILINE)


def _escape_sse_line(line: str) -> str:
    """Prefix-protect lines that look like SSE control fields."""
    if _SSE_CONTROL_RE.match(line):
        return f":{line}"  # SSE comment — hidden from client EventSource
    return line


# ── Subprocess management ────────────────────────────────────────────────────
_proc: subprocess.Popen | None = None
_healthy: bool = False
_client: httpx.AsyncClient | None = None
# Track chat subprocesses for cleanup on shutdown
_active_chat_procs: set[asyncio.subprocess.Process] = set()


def _subprocess_start() -> subprocess.Popen:
    """Launch server.py in an isolated process group (os.setsid).
    Redirects stdout+stderr to a log file to avoid pipe-buffer deadlock."""
    logger.info(f"Starting hermes-webui subprocess on {HERMES_SUB_HOST}:{HERMES_SUB_PORT}")
    env = {
        **os.environ,
        "HERMES_HOME": HERMES_HOME,
        "HERMES_WEBUI_HOST": HERMES_SUB_HOST,
        "HERMES_WEBUI_PORT": str(HERMES_SUB_PORT),
        "HERMES_WEBUI_TRUST_FORWARDED_HOST": "1",
        "HERMES_WEBUI_DEFAULT_WORKSPACE": str(RUNTIME_PATHS.workspace) if is_outside_docker else "/workspace",
        "HERMES_WEBUI_STATE_DIR": str(Path(HERMES_HOME) / "webui"),
    }
    log_fh = open(SUBSERVER_LOG, "ab", buffering=0)
    return subprocess.Popen(
        [sys.executable, str(SERVER_SCRIPT)],
        cwd=str(SERVER_SCRIPT.parent),
        env=env,
        stdout=log_fh,
        stderr=subprocess.STDOUT,
        preexec_fn=os.setsid,
    )


def _subprocess_stop(proc: subprocess.Popen | None, timeout: float = 10.0) -> None:
    """SIGTERM the entire process group, then SIGKILL if needed."""
    if proc is None or proc.poll() is not None:
        return
    pid = proc.pid
    if pid is None:
        return
    logger.info(f"Stopping subprocess group PGID={pid}")
    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
    except (ProcessLookupError, OSError):
        pass
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        logger.warning(f"Subprocess did not exit after {timeout}s, sending SIGKILL")
        try:
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        except (ProcessLookupError, OSError):
            pass
        try:
            proc.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            logger.error(f"Subprocess unkillable after SIGKILL (pid={pid})")


def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """TCP connect check for health probing."""
    import socket

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


async def _wait_for_subserver(timeout: float = 60.0) -> bool:
    """Poll TCP + HTTP health until the subserver responds or timeout expires."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if _is_port_open(HERMES_SUB_HOST, HERMES_SUB_PORT, timeout=0.5):
            try:
                async with httpx.AsyncClient() as check_client:
                    resp = await check_client.get(
                        f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}/health",
                        timeout=2.0,
                    )
                    if resp.status_code == 200:
                        logger.info(f"Subserver healthy on {HERMES_SUB_HOST}:{HERMES_SUB_PORT}")
                        return True
            except Exception:
                logger.debug("Health check failed, retrying...", exc_info=True)
        await asyncio.sleep(0.5)
    logger.error(f"Subserver did not become healthy within {timeout}s")
    return False


_client_lock = asyncio.Lock()


async def _ensure_client() -> httpx.AsyncClient | None:
    global _healthy, _client
    if _healthy and _client is not None:
        return _client
    async with _client_lock:
        if _healthy and _client is not None:
            return _client
        if _is_port_open(HERMES_SUB_HOST, HERMES_SUB_PORT, timeout=0.5):
            try:
                async with httpx.AsyncClient() as check_client:
                    resp = await check_client.get(
                        f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}/health",
                        timeout=2.0,
                    )
                    if resp.status_code == 200:
                        _client = httpx.AsyncClient(
                            base_url=f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}",
                            timeout=httpx.Timeout(300.0, connect=5.0),
                            limits=httpx.Limits(max_keepalive_connections=50, max_connections=200),
                        )
                        _healthy = True
                        logger.info(f"Subserver connected and healthy on {HERMES_SUB_HOST}:{HERMES_SUB_PORT}")
                        return _client
            except Exception:
                pass
        return None


# ── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _proc, _healthy, _client
    if os.environ.get("HERMES_AUTO_UPDATE", "1") == "1":
        logger.info("Auto-updating Hermes Agent & WebUI on dashboard startup...")
        try:
            update_script = PROJECT_ROOT / "config-file" / "update-all.sh"
            if update_script.exists():
                proc = await asyncio.create_subprocess_exec(
                    "bash", str(update_script),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                    cwd=str(PROJECT_ROOT)
                )
                stdout, _ = await proc.communicate()
                logger.info(f"Auto-update completed with code {proc.returncode}:\n{stdout.decode('utf-8', errors='replace')[-500:]}")
        except Exception as e:
            logger.warning(f"Auto-update on startup encountered error: {e}")

    if os.environ.get("HERMES_SKIP_SUBPROCESS") == "1":
        logger.info(f"Skipping subprocess startup. Connecting to existing subserver at {HERMES_SUB_HOST}:{HERMES_SUB_PORT}")
        _proc = None
        _healthy = await _wait_for_subserver(timeout=10.0)
    else:
        _proc = _subprocess_start()
        _healthy = await _wait_for_subserver(timeout=60.0)
    if _healthy:
        _client = httpx.AsyncClient(
            base_url=f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}",
            timeout=httpx.Timeout(300.0, connect=5.0),
            limits=httpx.Limits(max_keepalive_connections=50, max_connections=200),
        )
    else:
        logger.warning("BFF started but subserver is NOT healthy — proxy routes will return 503")
    yield
    # Shutdown: clean up chat subprocesses, then the hermes subserver
    for chat_proc in list(_active_chat_procs):
        if chat_proc.returncode is None:
            try:
                os.killpg(os.getpgid(chat_proc.pid), signal.SIGTERM)
            except (ProcessLookupError, OSError):
                pass
    _active_chat_procs.clear()
    if _client:
        await _client.aclose()
    if _proc:
        _subprocess_stop(_proc)
    _healthy = False


app = FastAPI(title="aiOS", lifespan=lifespan)
app.include_router(files.router)
app.include_router(update.router)
app.include_router(terminal.router)
app.include_router(notes.router)
app.include_router(
    management.build_router(
        paths=RUNTIME_PATHS,
        catalog_path=RUNTIME_PATHS.app / "config" / "agent-catalog.json",
    )
)
app.include_router(migrations.build_router(paths=RUNTIME_PATHS))

# CORS — allow browser access from LAN
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health endpoint ──────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    await _ensure_client()
    subserver_info = {
        "healthy": _healthy,
        "host": HERMES_SUB_HOST,
        "port": HERMES_SUB_PORT,
        "pid": _proc.pid if _proc else None,
    }
    return {"status": "ok", "subserver": subserver_info}


# ── Reverse proxy constants ───────────────────────────────────────────────────
PROXIED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


# ── aiOS Launcher (root) ─────────────────────────────────────────────────────
DASHBOARD_DIR = Path(__file__).resolve().parent
CONTROL_STATIC_DIR = next(
    (
        path
        for path in (
            DASHBOARD_DIR / "static" / "control",
            RUNTIME_PATHS.app / "apps" / "control-web" / "dist",
        )
        if path.exists()
    ),
    DASHBOARD_DIR / "static" / "control",
)
if (CONTROL_STATIC_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=CONTROL_STATIC_DIR / "assets"), name="control-assets")

@app.get("/")
async def dashboard():
    candidates = [
        CONTROL_STATIC_DIR / "index.html",
        Path("/aiOS-ui/features/dashboard/static/dashboard/index.html"),
        DASHBOARD_DIR / 'static' / 'dashboard' / 'index.html',
        PROJECT_ROOT / 'features' / 'dashboard' / 'static' / 'dashboard' / 'index.html',
        PROJECT_ROOT / 'aiOS-ui' / 'features' / 'dashboard' / 'static' / 'dashboard' / 'index.html',
        Path("/home/HeigatWorkspace/My-file/my-project/my-assistance/aiOS-ui/features/dashboard/static/dashboard/index.html"),
    ]
    for path in candidates:
        if path.exists():
            return HTMLResponse(path.read_text())
    return HTMLResponse('Dashboard HTML not found')


@app.get("/legacy")
async def legacy_dashboard():
    candidates = [
        Path("/aiOS-ui/features/dashboard/static/dashboard/index.html"),
        DASHBOARD_DIR / "static" / "dashboard" / "index.html",
        PROJECT_ROOT / "features" / "dashboard" / "static" / "dashboard" / "index.html",
        PROJECT_ROOT / "aiOS-ui" / "features" / "dashboard" / "static" / "dashboard" / "index.html",
    ]
    for path in candidates:
        if path.exists():
            return HTMLResponse(path.read_text())
    return HTMLResponse("Legacy dashboard HTML not found", status_code=404)

@app.get("/workspace")
async def workspace_portal():
    candidates = [
        Path("/aiOS-ui/features/dashboard/static/workspace/index.html"),
        DASHBOARD_DIR / 'static' / 'workspace' / 'index.html',
        PROJECT_ROOT / 'features' / 'dashboard' / 'static' / 'workspace' / 'index.html',
        PROJECT_ROOT / 'aiOS-ui' / 'features' / 'dashboard' / 'static' / 'workspace' / 'index.html',
        Path("/home/HeigatWorkspace/My-file/my-project/my-assistance/aiOS-ui/features/dashboard/static/workspace/index.html"),
    ]
    for path in candidates:
        if path.exists():
            return HTMLResponse(path.read_text())
    return HTMLResponse('Workspace HTML not found')

@app.get("/favicon.ico")
async def favicon():
    favicon_path = PROJECT_ROOT / 'features' / 'hermes-webui' / 'static' / 'favicon.svg'
    if favicon_path.exists():
        return Response(content=favicon_path.read_bytes(), media_type="image/svg+xml")
    return Response(status_code=404)


_proxy_clients: dict[str, httpx.AsyncClient] = {}


def agentmemory_proxy_headers(secret_file: Path) -> dict[str, str]:
    secret = secret_file.read_text(encoding="utf-8").strip()
    if not secret:
        raise ValueError("AgentMemory viewer secret is empty")
    return {"authorization": f"Bearer {secret}"}


def _get_proxy_client(target_base: str) -> httpx.AsyncClient:
    if target_base not in _proxy_clients:
        _proxy_clients[target_base] = httpx.AsyncClient(
            base_url=target_base,
            timeout=httpx.Timeout(300.0, connect=5.0),
            limits=httpx.Limits(max_keepalive_connections=50, max_connections=200),
        )
    return _proxy_clients[target_base]

async def proxy_target(
    request: Request,
    path: str,
    target_base: str,
    client: httpx.AsyncClient | None = None,
    extra_headers: dict[str, str] | None = None,
):
    if not client:
        client = _get_proxy_client(target_base)
    url = f"{target_base}/{path}" if path else f"{target_base}/"
    if request.url.query:
        url = f"{url}?{request.url.query.decode() if isinstance(request.url.query, bytes) else request.url.query}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "transfer-encoding")}
    # Set the Host header to localhost to pass any host-allowlist checks
    from urllib.parse import urlparse
    parsed_target = urlparse(target_base)
    if parsed_target.port:
        headers["host"] = f"localhost:{parsed_target.port}"
    else:
        headers["host"] = "localhost"
    headers["X-Forwarded-Host"] = request.headers.get("host", "")
    if extra_headers:
        headers.update(extra_headers)
    body = await request.body()
    try:
        req = client.build_request(
            method="GET" if request.method == "HEAD" else request.method,
            url=url, headers=headers, content=body
        )
        resp = await client.send(req, stream=True, follow_redirects=False)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Target unreachable: {e}")
        
    resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in ("transfer-encoding", "content-encoding")}
    resp_headers.pop("content-length", None)
    
    # Strip X-Frame-Options and Content-Security-Policy to allow embedding in iframes
    resp_headers.pop("x-frame-options", None)
    resp_headers.pop("content-security-policy", None)
    
    if request.method == "HEAD":
        return Response(status_code=resp.status_code, headers=resp_headers)
    
    from starlette.background import BackgroundTask
    return StreamingResponse(
        resp.aiter_bytes(), status_code=resp.status_code, headers=resp_headers,
        media_type=resp.headers.get("content-type", ""), background=BackgroundTask(resp.aclose)
    )

async def proxy_websocket(websocket: WebSocket, target_url: str):
    await websocket.accept()
    try:
        async with websockets.connect(target_url) as target_ws:
            async def forward_to_target():
                try:
                    while True:
                        msg = await websocket.receive()
                        if msg.get("type") == "websocket.disconnect":
                            break
                        if "text" in msg:
                            await target_ws.send(msg["text"])
                        elif "bytes" in msg:
                            await target_ws.send(msg["bytes"])
                except Exception:
                    pass

            async def forward_to_client():
                try:
                    async for message in target_ws:
                        if isinstance(message, bytes):
                            await websocket.send_bytes(message)
                        else:
                            await websocket.send_text(message)
                except Exception:
                    pass

            await asyncio.gather(forward_to_target(), forward_to_client())
    except Exception as e:
        logger.error(f"WebSocket proxy error to {target_url}: {e}")
    finally:
        try:
            await websocket.close()
        except Exception:
            pass

@app.websocket("/api/{path:path}")
async def ws_proxy_catchall(websocket: WebSocket, path: str):
    query = websocket.query_params
    target_base = "ws://127.0.0.1:9119"
    target = f"{target_base}/api/{path}?{query}" if query else f"{target_base}/api/{path}"
    await proxy_websocket(websocket, target)

@app.api_route("/agentmemory/{path:path}", methods=PROXIED_METHODS)
async def proxy_to_agentmemory(request: Request, path: str):
    """Proxy AgentMemory requests to port 3113."""
    target_base = AGENTMEMORY_BASE_URL
    try:
        headers = agentmemory_proxy_headers(AGENTMEMORY_SECRET_FILE)
    except (OSError, ValueError):
        raise HTTPException(status_code=503, detail="AgentMemory proxy is not initialized")
    return await proxy_target(request, path, target_base, extra_headers=headers)

@app.api_route("/hermes-chat/{path:path}", methods=PROXIED_METHODS)
async def proxy_to_hermes_chat(request: Request, path: str):
    """Proxy Hermes Chat requests to port 8501."""
    target_base = f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}"
    client = await _ensure_client()
    return await proxy_target(request, path, target_base, client=client)

@app.api_route("/hermes-dashboard/{path:path}", methods=PROXIED_METHODS)
async def proxy_to_hermes_dashboard(request: Request, path: str):
    """Proxy Hermes Dashboard requests to port 9119."""
    target_base = "http://127.0.0.1:9119"
    return await proxy_target(request, path, target_base)

@app.api_route("/{path:path}", methods=PROXIED_METHODS)
async def proxy_to_hermes(request: Request, path: str):
    """Forward all unmatched requests to the appropriate subserver based on the Referer header
    and path, with fallbacks to other subservers if a 404 is returned.
    """
    referer = request.headers.get("referer", "").lower()
    
    # Parse referer path to identify SPA routes
    referer_path = ""
    if referer:
        try:
            from urllib.parse import urlparse
            referer_path = urlparse(referer).path
        except Exception:
            pass

    # Dashboard routes in the Hermes Dashboard React/Vue router
    dashboard_routes = {
        "/skills", "/settings", "/sessions", "/chat", "/logs", "/runs", "/agents",
        "/system", "/status", "/cron"
    }
    
    is_from_dashboard = "hermes-dashboard" in referer
    if referer_path:
        for route in dashboard_routes:
            if referer_path == route or referer_path.rstrip("/").startswith(route + "/"):
                is_from_dashboard = True
                break

    # Also check if the requested API path itself is dashboard-specific
    is_dashboard_api = False
    normalized_path = "/" + path.lstrip("/")
    dashboard_api_prefixes = {
        "/api/auth", "/api/ws", "/api/events", "/api/pty", "/api/tools/toolsets",
        "/api/status", "/api/config", "/api/cron", "/api/analytics"
    }
    for prefix in dashboard_api_prefixes:
        if normalized_path == prefix or normalized_path.startswith(prefix + "/"):
            is_dashboard_api = True
            break
            
    # Determine the preferred target base based on referer
    if is_from_dashboard or is_dashboard_api:
        bases_order = [
            ("dashboard", "http://127.0.0.1:9119"),
            ("webui", f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}"),
            ("agentmemory", AGENTMEMORY_BASE_URL)
        ]
    elif "agentmemory" in referer:
        bases_order = [
            ("agentmemory", AGENTMEMORY_BASE_URL),
            ("webui", f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}"),
            ("dashboard", "http://127.0.0.1:9119")
        ]
    else:
        bases_order = [
            ("webui", f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}"),
            ("agentmemory", AGENTMEMORY_BASE_URL),
            ("dashboard", "http://127.0.0.1:9119")
        ]

    for name, target_base in bases_order:
        try:
            if name == "webui":
                client = await _ensure_client()
                response = await proxy_target(request, path, target_base, client=client)
            else:
                response = await proxy_target(request, path, target_base)
                
            if response.status_code != 404:
                return response
        except Exception:
            pass

    # Fallback response: if nothing matches, return 404
    raise HTTPException(status_code=404, detail="Not found on any subserver")

if __name__ == "__main__":
    import uvicorn
    # The hermes subprocess must not be spawned by multiple workers!
    uvicorn.run(app, host="0.0.0.0", port=SIDECAR_PORT, timeout_graceful_shutdown=5)
