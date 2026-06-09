"""
FastAPI BFF (Backend-For-Frontend) wrapper around hermes-webui server.py.

Starts server.py as a subprocess on 127.0.0.1:8787, reverse-proxies all requests
through a health-gated httpx client, and exposes chat endpoints for Claude/agy.

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
from routers import files, update, terminal
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse

import httpx

# ── Configuration ────────────────────────────────────────────────────────────
HERMES_SUB_HOST = os.environ.get("HERMES_SUB_HOST", "127.0.0.1")
HERMES_SUB_PORT = int(os.environ.get("HERMES_SUB_PORT", "8501"))
HERMES_HOME = os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))
SIDECAR_HOST = os.environ.get("SIDECAR_HOST", "127.0.0.1")
SIDECAR_PORT = int(os.environ.get("SIDECAR_PORT", "8787"))
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
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
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
    "/workspace": PROJECT_ROOT / "sandbox-data" / "working-space",
    "/outputs": PROJECT_ROOT / "sandbox-data" / "outputs",
    "/my-data": PROJECT_ROOT / "sandbox-data" / "my-data",
    "/config-file": PROJECT_ROOT / "config-file",
    "/aiOS-ui": PROJECT_ROOT / "aiOS-ui",
    "/home/ai_user/.agentmemory": PROJECT_ROOT / "persistent" / "agentmemory",
    "/home/ai_user/.claude": PROJECT_ROOT / "persistent" / "claude",
    "/home/ai_user/.hermes": PROJECT_ROOT / "persistent" / "hermes",
    "/home/ai_user/.gemini": PROJECT_ROOT / "persistent" / "gemini",
    "/home/ai_user/.agents": PROJECT_ROOT / "persistent" / "agents",
    "/home/ai_user/.iii": PROJECT_ROOT / "persistent" / "iii",
    "/home/ai_user": PROJECT_ROOT / "sandbox-data" / "home_ai_user",
}

if is_outside_docker:
    (PROJECT_ROOT / "sandbox-data" / "home_ai_user").mkdir(parents=True, exist_ok=True)

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
@app.get("/")
async def dashboard():
    dashboard_html_path = PROJECT_ROOT / 'aiOS-ui' / 'dashboard' / 'static' / 'dashboard' / 'index.html'
    if dashboard_html_path.exists():
        return HTMLResponse(dashboard_html_path.read_text())
    return HTMLResponse('Dashboard HTML not found')

@app.get("/favicon.ico")
async def favicon():
    favicon_path = PROJECT_ROOT / 'aiOS-ui' / 'hermes-webui' / 'static' / 'favicon.svg'
    if favicon_path.exists():
        return Response(content=favicon_path.read_bytes(), media_type="image/svg+xml")
    return Response(status_code=404)


async def proxy_target(request: Request, path: str, target_base: str):
    client = await _ensure_client()
    if not client:
        raise HTTPException(status_code=503, detail="Proxy client not ready")
    url = f"{target_base}/{path}" if path else f"{target_base}/"
    if request.url.query:
        url = f"{url}?{request.url.query.decode() if isinstance(request.url.query, bytes) else request.url.query}"
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "transfer-encoding")}
    headers["X-Forwarded-Host"] = request.headers.get("host", "")
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
    
    if request.method == "HEAD":
        return Response(status_code=resp.status_code, headers=resp_headers)
    
    from starlette.background import BackgroundTask
    return StreamingResponse(
        resp.aiter_bytes(), status_code=resp.status_code, headers=resp_headers,
        media_type=resp.headers.get("content-type", ""), background=BackgroundTask(resp.aclose)
    )

@app.api_route("/{path:path}", methods=PROXIED_METHODS)
async def proxy_to_hermes(request: Request, path: str):
    """Forward all unmatched requests to the hermes-webui subserver."""
    target_base = f"http://{HERMES_SUB_HOST}:{HERMES_SUB_PORT}"
    return await proxy_target(request, path, target_base)

if __name__ == "__main__":
    import uvicorn
    # The hermes subprocess must not be spawned by multiple workers!
    uvicorn.run(app, host="0.0.0.0", port=SIDECAR_PORT)
