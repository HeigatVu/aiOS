import asyncio
import datetime as _datetime
import json
import logging
import os
import shutil
import stat as _stat
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response, StreamingResponse

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WORKSPACE_DIR = PROJECT_ROOT
_FILE_BROWSER_HTML_PATH = PROJECT_ROOT / "aiOS-ui" / "dashboard" / "static" / "file-browser" / "index.html"
_FILE_BROWSER_ROOT = str(PROJECT_ROOT)
_FILE_BROWSER_DENY = [
    str(PROJECT_ROOT / ".git"),
    str(PROJECT_ROOT / ".ssh"),
    str(PROJECT_ROOT / "persistent" / ".ssh"),
]
_PERMISSIONS_CONFIG = PROJECT_ROOT / "config-file" / "aios-permissions.json"
_PERMISSION_MODES = {
    "rw": {"file": "666", "dir": "777"},
    "ro": {"file": "644", "dir": "755"},
    "none": {"file": "600", "dir": "700"},
}
is_outside_docker = True
logger = logging.getLogger("bff.files")

def _to_container_path(host_path: Path | str) -> str:
    path_str = str(host_path)
    
    # Check specific docker mappings first
    ws_path = str(WORKSPACE_DIR / "sandbox-data" / "working-space")
    if path_str.startswith(ws_path):
        rel = Path(path_str).relative_to(ws_path)
        return f"/workspace/{rel}" if str(rel) != "." else "/workspace"
        
    my_data_path = str(WORKSPACE_DIR / "sandbox-data" / "my-data")
    if path_str.startswith(my_data_path):
        rel = Path(path_str).relative_to(my_data_path)
        return f"/my-data/{rel}" if str(rel) != "." else "/my-data"
        
    outputs_path = str(WORKSPACE_DIR / "sandbox-data" / "outputs")
    if path_str.startswith(outputs_path):
        rel = Path(path_str).relative_to(outputs_path)
        return f"/outputs/{rel}" if str(rel) != "." else "/outputs"
        
    persistent_path = str(WORKSPACE_DIR / "persistent")
    if path_str.startswith(persistent_path):
        rel = Path(path_str).relative_to(persistent_path)
        return f"/home/ai_user/{rel}" if str(rel) != "." else "/home/ai_user"

    # Fallback for other paths directly under WORKSPACE_DIR
    if path_str.startswith(str(WORKSPACE_DIR)):
        rel = Path(path_str).relative_to(WORKSPACE_DIR)
        return f"/{rel}" if str(rel) != "." else "/"
        
    return path_str

def _load_file_browser_html() -> str:
    try:
        return _FILE_BROWSER_HTML_PATH.read_text()
    except Exception:
        return "<html><body><h1>File browser not found</h1></body></html>"

def _load_ai_permissions() -> dict[str, str]:
    """Load AI permission config → {path_prefix: rw|ro|none}."""
    try:
        cfg = _PERMISSIONS_CONFIG
        if cfg.exists():
            return json.loads(cfg.read_text())
    except Exception:
        pass
    return {}


def _save_ai_permissions(data: dict[str, str]) -> None:
    """Persist AI permission config to disk."""
    cfg = _PERMISSIONS_CONFIG
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps(data, indent=2))


def _get_ai_permission_level(abs_path: str) -> str:
    """Return 'rw', 'ro', or 'none' for a path (longest-prefix match).

    Falls back to 'rw' when no entry matches.
    """
    perms = _load_ai_permissions()
    best_match = "rw"
    best_len = 0
    for prefix, level in perms.items():
        if abs_path == prefix or abs_path.startswith(prefix.rstrip("/") + "/"):
            if len(prefix) > best_len:
                best_match = level
                best_len = len(prefix)
    return best_match


def _check_ai_permission(target: Path, allow: list[str]) -> None:
    """Raise HTTP 403 if the path's AI permission level is not in *allow*."""
    level = _get_ai_permission_level(_to_container_path(target))
    if level not in allow:
        raise HTTPException(
            status_code=403,
            detail=f"AI permission '{level}' — operation not allowed",
        )


def _resolve_safe_path(rel: str) -> Path:
    """Resolve and jail a relative path to FILE_BROWSER_ROOT."""
    root = Path(_FILE_BROWSER_ROOT).resolve()
    rel = rel.replace("\\", "/")
    
    # Handle Docker paths mapped to host
    if rel == "/workspace" or rel.startswith("/workspace/"):
        sub = rel[len("/workspace"):]
        target = (root / "sandbox-data" / "working-space" / sub.lstrip("/")).resolve()
    elif rel == "/my-data" or rel.startswith("/my-data/"):
        sub = rel[len("/my-data"):]
        target = (root / "sandbox-data" / "my-data" / sub.lstrip("/")).resolve()
    elif rel == "/outputs" or rel.startswith("/outputs/"):
        sub = rel[len("/outputs"):]
        target = (root / "sandbox-data" / "outputs" / sub.lstrip("/")).resolve()
    elif rel == "/home/ai_user" or rel.startswith("/home/ai_user/"):
        sub = rel[len("/home/ai_user"):]
        target = (root / "persistent" / sub.lstrip("/")).resolve()
    else:
        rel_path = rel.lstrip("/")
        # If the client sends an absolute path under the root, strip the root prefix
        root_str = str(root)
        if rel_path.startswith(root_str.lstrip("/")):
            rel_path = rel_path[len(root_str.lstrip("/")):].lstrip("/")
        target = (root / rel_path).resolve()
            
    try:
        target.relative_to(root)
    except ValueError:
        raise HTTPException(status_code=403, detail="Path outside file browser root")
    
    target_str = str(target)
    if target_str in _FILE_BROWSER_DENY or any(
        target_str.startswith(d + "/") for d in _FILE_BROWSER_DENY
    ):
        raise HTTPException(status_code=403, detail="Path is blocked")
    return target


@router.get("/api/files/list")
async def files_list(path: str = ""):
    """List directory contents."""
    target = _resolve_safe_path(path)
    logger.warning(f"DEBUG files_list: path={path!r} target={target!r} exists={target.exists()} is_outside_docker={is_outside_docker}")
    if not target.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    if not target.is_dir():
        raise HTTPException(status_code=400, detail="Not a directory")

    entries = []
    try:
        for entry in sorted(target.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower())):
            try:
                st = entry.stat()
            except PermissionError:
                entries.append({
                    "name": entry.name,
                    "type": "dir" if entry.is_dir() else "file",
                    "size": None,
                    "modified": None,
                    "mode": None,
                    "mode_octal": None,
                    "unreadable": True,
                })
                continue
            abs_path = _to_container_path(target / entry.name)
            entries.append({
                "name": entry.name,
                "type": "dir" if entry.is_dir() else "file",
                "size": st.st_size,
                "modified": _datetime.datetime.fromtimestamp(
                    st.st_mtime, tz=_datetime.timezone.utc
                ).isoformat(),
                "mode": _stat.filemode(st.st_mode),
                "mode_octal": oct(st.st_mode)[-3:],
                "uid": st.st_uid,
                "gid": st.st_gid,
                "ai_level": _get_ai_permission_level(abs_path),
            })
    except PermissionError:
        raise HTTPException(status_code=403, detail="Cannot read directory")

    # ── Filter out entries the AI is not allowed to see ──
    entries = [e for e in entries if e.get("ai_level") != "none"]

    return {"path": _to_container_path(target), "entries": entries}


@router.get("/api/files/read")
async def files_read(path: str = ""):
    """Read file content."""
    target = _resolve_safe_path(path)
    _check_ai_permission(target, allow=["rw", "ro"])
    if not target.is_file():
        raise HTTPException(status_code=400, detail="Not a file")
    try:
        content = target.read_text()
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Binary file — cannot display as text")
    return {"path": _to_container_path(target), "content": content, "size": target.stat().st_size}


@router.post("/api/files/write")
async def files_write(request: Request):
    """Write file content."""
    body = await request.json()
    rel = body.get("path", "")
    content = body.get("content", "")
    target = _resolve_safe_path(rel)
    _check_ai_permission(target, allow=["rw"])
    try:
        target.write_text(content)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"path": _to_container_path(target), "written": len(content)}


@router.post("/api/files/chmod")
async def files_chmod(request: Request):
    """Change file permissions. Mode is an octal string like '644' or '755'."""
    body = await request.json()
    rel = body.get("path", "")
    mode_str = body.get("mode", "")
    if not mode_str or not all(c in "01234567" for c in mode_str) or len(mode_str) != 3:
        raise HTTPException(status_code=400, detail="Invalid mode — must be 3-digit octal (e.g. 644)")

    target = _resolve_safe_path(rel)
    _check_ai_permission(target, allow=["rw"])
    try:
        new_mode = int(mode_str, 8)
        os.chmod(target, new_mode)
        st = target.stat()
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except OSError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "path": _to_container_path(target),
        "mode": _stat.filemode(st.st_mode),
        "mode_octal": oct(st.st_mode)[-3:],
    }


@router.post("/api/files/copy")
async def files_copy(request: Request):
    """Copy a file or directory. {src, dst}"""
    import shutil as _shutil
    body = await request.json()
    src = _resolve_safe_path(body.get("src", ""))
    dst = _resolve_safe_path(body.get("dst", ""))
    if not src.exists():
        raise HTTPException(status_code=404, detail="Source not found")
    _check_ai_permission(src, allow=["rw"])
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_dir():
        dst = dst / src.name
    # Avoid clobbering: suffix if dst already exists
    stem, suffix = dst.stem, dst.suffix
    counter = 1
    while dst.exists():
        dst = dst.parent / f"{stem} (copy {counter}){suffix}"
        counter += 1
    try:
        if src.is_dir():
            _shutil.copytree(str(src), str(dst))
        else:
            _shutil.copy2(str(src), str(dst))
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except OSError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"src": _to_container_path(src), "dst": _to_container_path(dst)}


@router.post("/api/files/move")
async def files_move(request: Request):
    """Move/rename a file or directory. {src, dst} — both relative to FILE_BROWSER_ROOT."""
    import shutil as _shutil
    body = await request.json()
    src = _resolve_safe_path(body.get("src", ""))
    dst = _resolve_safe_path(body.get("dst", ""))
    if not src.exists():
        raise HTTPException(status_code=404, detail="Source not found")
    _check_ai_permission(src, allow=["rw"])
    dst.parent.mkdir(parents=True, exist_ok=True)
    # If dst is a directory, move src inside it
    if dst.is_dir():
        dst = dst / src.name
    try:
        _shutil.move(str(src), str(dst))
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except OSError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"src": _to_container_path(src), "dst": _to_container_path(dst)}


@router.post("/api/files/delete")
async def files_delete(request: Request):
    """Permanently delete a file or directory."""
    import shutil as _shutil
    body = await request.json()
    target = _resolve_safe_path(body.get("path", ""))
    if not target.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    _check_ai_permission(target, allow=["rw"])
    try:
        if target.is_dir():
            _shutil.rmtree(str(target))
        else:
            target.unlink()
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")
    except OSError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"deleted": _to_container_path(target)}


@router.get("/api/files/watch")
async def files_watch(path: str = ""):
    """SSE stream that tails a file. Emits new lines as they appear."""
    from asyncio import sleep as _async_sleep

    target = _resolve_safe_path(path)
    if not target.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    async def _tail():
        yield "data: {\"status\": \"watching\", \"path\": \"" + _to_container_path(target) + "\"}\n\n"
        try:
            with open(target, "r") as f:
                f.seek(0, 2)  # end of file
                while True:
                    line = f.readline()
                    if line:
                        yield f"data: {json.dumps({'line': line.rstrip()})}\n\n"
                    else:
                        await _async_sleep(0.5)
        except PermissionError:
            yield "data: {\"error\": \"Permission denied\"}\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(
        _tail(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── AI Permissions Management API ────────────────────────────────────────────
@router.get("/api/files/permissions")
async def files_permissions_get(path: str = ""):
    """Get AI permissions config. Pass ?path= to query a single path."""
    if path:
        target = _resolve_safe_path(path)
        container_path = _to_container_path(target)
        level = _get_ai_permission_level(container_path)
        return {"path": container_path, "level": level, "mode": _PERMISSION_MODES.get(level)}
    return _load_ai_permissions()


@router.post("/api/files/permissions/set")
async def files_permissions_set(request: Request):
    """Set AI permission level for a path + apply matching chmod.

    Body: {path, level, type}  — level ∈ {rw, ro, none}, type ∈ {file, dir}
    """
    body = await request.json()
    rel = body.get("path", "")
    level = body.get("level", "rw")
    entry_type = body.get("type", "file")

    if level not in ("rw", "ro", "none"):
        raise HTTPException(status_code=400, detail="Invalid level: must be rw, ro, or none")
    if entry_type not in ("file", "dir"):
        raise HTTPException(status_code=400, detail="Invalid type: must be 'file' or 'dir'")

    target = _resolve_safe_path(rel)
    container_path = _to_container_path(target)

    # ── Persist permission level ──
    perms = _load_ai_permissions()
    perms[container_path] = level
    _save_ai_permissions(perms)

    # ── Apply filesystem mode and ownership directly ──
    is_root = (os.geteuid() == 0)
    mode_octal = _PERMISSION_MODES[level][entry_type]

    chmod_error = None
    chmod_applied = False

    if not target.exists():
        chmod_error = "target does not exist"
    else:
        try:
            if is_root:
                import shutil
                target_uid = int(os.environ.get("USER_ID", str(os.getuid())))
                target_gid = int(os.environ.get("GROUP_ID", str(os.getgid())))
                try:
                    shutil.chown(target, user=target_uid, group=target_gid)
                except Exception as e:
                    logger.warning(f"Failed to chown {target}: {e}")

            # Change filesystem permission mode
            os.chmod(target, int(mode_octal, 8))
            applied_mode = oct(target.stat().st_mode)[-3:]
            if applied_mode == mode_octal:
                chmod_applied = True
            else:
                chmod_error = f"chmod succeeded but mode is {applied_mode}, expected {mode_octal}"
        except PermissionError as pe:
            # Fallback: if permission is denied and we are outside Docker, try running chmod inside the container
            if is_outside_docker:
                try:
                    # Try docker first
                    cmd = ["docker", "exec", "-u", "root", "ai_tui_sandbox", "chmod", mode_octal, container_path]
                    res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    if res.returncode == 0:
                        chmod_applied = True
                    else:
                        # Try podman as fallback
                        cmd_pm = ["podman", "exec", "-u", "root", "ai_tui_sandbox", "chmod", mode_octal, container_path]
                        res_pm = subprocess.run(cmd_pm, capture_output=True, text=True, timeout=5)
                        if res_pm.returncode == 0:
                            chmod_applied = True
                        else:
                            chmod_error = f"Permission denied on host, container chmod failed: {res.stderr or res_pm.stderr}"
                except Exception as ex:
                    chmod_error = f"Permission denied on host, container chmod failed: {str(ex)}"
            else:
                chmod_error = str(pe)
        except OSError as e:
            chmod_error = str(e)

    return {
        "path": container_path, "level": level, "mode": mode_octal,
        "chmod_applied": chmod_applied,
        "chmod_error": chmod_error,
    }


@router.post("/api/files/permissions/remove")
async def files_permissions_remove(request: Request):
    """Remove AI permission entry for a path and its children."""
    body = await request.json()
    rel = body.get("path", "")
    target = _resolve_safe_path(rel)
    container_path = _to_container_path(target)

    perms = _load_ai_permissions()
    to_remove = [k for k in perms if k == container_path or k.startswith(container_path.rstrip("/") + "/")]
    for k in to_remove:
        del perms[k]
    _save_ai_permissions(perms)

    return {"path": container_path, "removed": to_remove}


# ── File Browser SPA ─────────────────────────────────────────────────────────
_FILE_BROWSER_HTML_PATH = PROJECT_ROOT / "aiOS-ui" / "dashboard" / "static" / "file-browser" / "index.html"


def _load_file_browser_html() -> str:
    """Load the file browser SPA HTML, with a fallback for missing file."""
    try:
        return _FILE_BROWSER_HTML_PATH.read_text()
    except Exception:
        return "<html><body><h1>File browser not found</h1></body></html>"


@router.get("/files")
async def file_browser_spa():
    """Serve the file browser single-page app."""
    return HTMLResponse(
        content=_load_file_browser_html(),
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
    )

