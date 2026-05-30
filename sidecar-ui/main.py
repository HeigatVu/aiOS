import asyncio
import queue
import subprocess
import threading
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, Response, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import docker_bridge
import volumes
import config_editors

app = FastAPI(title="aiOS Control Panel")


# ---------------------------------------------------------------------------
# Pydantic request models
# ---------------------------------------------------------------------------

class VolumeModeBody(BaseModel):
    mode: str


class ChmodBody(BaseModel):
    path: str
    mode: str


class DockerfileBody(BaseModel):
    package: str
    ecosystem: str
    use_sudo: bool = False


class ReadmeBody(BaseModel):
    note: str


class EnvironmentBody(BaseModel):
    package: str


class VolumeBody(BaseModel):
    host_path: str
    container_path: str


class FileReadBody(BaseModel):
    path: str


class FileWriteBody(BaseModel):
    path: str
    content: str


class KillProcessBody(BaseModel):
    pid: str


class EnvSaveBody(BaseModel):
    key: str
    value: str


class SQLiteQueryBody(BaseModel):
    db_path: str
    query: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/status")
def get_status() -> dict:
    return docker_bridge.get_sandbox_status()


@app.post("/api/sandbox/restart")
def sandbox_restart() -> dict:
    return docker_bridge.restart_sandbox()


@app.get("/api/sandbox/stats")
def sandbox_stats() -> dict:
    return docker_bridge.get_sandbox_stats()


@app.websocket("/ws/logs")
async def ws_logs(websocket: WebSocket) -> None:
    await websocket.accept()
    q: queue.Queue[Optional[str]] = queue.Queue()

    def run_in_thread() -> None:
        try:
            for chunk in docker_bridge.stream_logs(tail=100):
                q.put(chunk)
        finally:
            q.put(None)

    thread = threading.Thread(target=run_in_thread, daemon=True)
    thread.start()

    try:
        while True:
            try:
                chunk = q.get_nowait()
            except queue.Empty:
                await asyncio.sleep(0.01)
                continue
            if chunk is None:
                break
            await websocket.send_text(chunk)
    except WebSocketDisconnect:
        pass
    finally:
        thread.join(timeout=5)


@app.websocket("/ws/rebuild")
async def ws_rebuild(websocket: WebSocket) -> None:
    await websocket.accept()
    q: queue.Queue[Optional[str]] = queue.Queue()

    def run_in_thread() -> None:
        try:
            proc = subprocess.Popen(
                ["docker", "compose", "build"],
                cwd=volumes.WORKSPACE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            assert proc.stdout is not None
            for line in proc.stdout:
                q.put(line)
            proc.wait()
            q.put(f"\n[exit code {proc.returncode}]\n")
        except FileNotFoundError:
            q.put("ERROR: 'docker compose' not found in PATH\n")
        except Exception as e:
            q.put(f"ERROR: {str(e)}\n")
        finally:
            q.put(None)

    thread = threading.Thread(target=run_in_thread, daemon=True)
    thread.start()

    try:
        while True:
            try:
                chunk = q.get_nowait()
            except queue.Empty:
                await asyncio.sleep(0.01)
                continue
            if chunk is None:
                break
            await websocket.send_text(chunk)
    except WebSocketDisconnect:
        pass
    finally:
        thread.join(timeout=300)


@app.websocket("/ws/exec")
async def ws_exec(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        cmd = await websocket.receive_text()
    except WebSocketDisconnect:
        return

    q: queue.Queue[Optional[str]] = queue.Queue()

    def run_in_thread() -> None:
        try:
            for chunk in docker_bridge.execute_in_sandbox(cmd):
                q.put(chunk)
        finally:
            q.put(None)  # sentinel

    thread = threading.Thread(target=run_in_thread, daemon=True)
    thread.start()

    try:
        while True:
            try:
                chunk = q.get_nowait()
            except queue.Empty:
                await asyncio.sleep(0.01)
                continue

            if chunk is None:
                break
            await websocket.send_text(chunk)
    except WebSocketDisconnect:
        pass
    finally:
        thread.join(timeout=5)


@app.get("/api/volumes")
def get_volumes() -> list[dict]:
    return volumes.list_volumes()


# Static sub-paths must come before /{idx} routes so FastAPI does not try to
# cast "chmod" to int and 422 before reaching this handler.
@app.post("/api/volumes/chmod")
def chmod_path(body: ChmodBody) -> dict:
    cmd = f"chmod {body.mode} '{body.path}'"
    output = "".join(docker_bridge.execute_in_sandbox(cmd))
    return {"output": output}


@app.delete("/api/volumes/{idx}")
def delete_volume(idx: int) -> dict:
    try:
        volumes.delete_volume(idx)
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


@app.post("/api/volumes/{idx}/mode")
def set_volume_mode(idx: int, body: VolumeModeBody) -> dict:
    try:
        vol_list = volumes.list_volumes()
        if idx < 0 or idx >= len(vol_list):
            raise IndexError(f"Volume index {idx} out of range")
        container_path = vol_list[idx]["container_path"]
        volumes.update_volume_mode(idx, body.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))

    live_ok, live_msg = docker_bridge.live_remount_volume(container_path, body.mode)
    return {"ok": True, "live_applied": live_ok, "live_msg": live_msg}


@app.get("/api/volumes/{idx}/files")
def get_volume_files(idx: int, path: str | None = Query(default=None)) -> list[dict]:
    vol_list = volumes.list_volumes()
    if idx < 0 or idx >= len(vol_list):
        raise HTTPException(status_code=404, detail=f"Volume index {idx} not found")
    container_path = path if path else vol_list[idx]["container_path"]
    return docker_bridge.list_files_in_container(container_path)


@app.post("/api/config/dockerfile")
def config_dockerfile(body: DockerfileBody) -> dict:
    try:
        config_editors.append_to_dockerfile(body.package, body.ecosystem, body.use_sudo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


@app.post("/api/config/readme")
def config_readme(body: ReadmeBody) -> dict:
    try:
        config_editors.append_to_readme(body.note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


@app.post("/api/config/environment")
def config_environment(body: EnvironmentBody) -> dict:
    try:
        config_editors.append_to_environment(body.package)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


@app.post("/api/config/volume")
def config_volume(body: VolumeBody) -> dict:
    try:
        config_editors.add_volume_to_compose(body.host_path, body.container_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"ok": True}


@app.post("/api/editor/read")
def read_file(body: FileReadBody) -> dict:
    try:
        content = docker_bridge.read_file_in_container(body.path)
        return {"ok": True, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/editor/write")
def write_file(body: FileWriteBody) -> dict:
    try:
        docker_bridge.write_file_in_container(body.path, body.content)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sandbox/processes")
def get_processes() -> list[dict]:
    return docker_bridge.list_processes()


@app.post("/api/sandbox/processes/kill")
def kill_process_route(body: KillProcessBody) -> dict:
    return docker_bridge.kill_process(body.pid)


@app.get("/api/sandbox/env")
def get_env_route() -> dict:
    return docker_bridge.get_env_vars()


@app.post("/api/sandbox/env/save")
def save_env_route(body: EnvSaveBody) -> dict:
    return docker_bridge.save_dotenv_var(body.key, body.value)


@app.get("/api/sandbox/ports")
def get_ports() -> list[dict]:
    return docker_bridge.get_listening_ports()


@app.post("/api/db/query")
def db_query(body: SQLiteQueryBody) -> dict:
    return docker_bridge.query_sqlite_in_container(body.db_path, body.query)


@app.post("/api/volumes/upload")
async def upload_file_to_volume(path: str = Form(...), file: UploadFile = File(...)) -> dict:
    try:
        data = await file.read()
        docker_bridge.write_binary_file_in_container(path, data)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/volumes/download")
def download_file_from_volume(path: str = Query(...)) -> Response:
    try:
        data = docker_bridge.read_binary_file_in_container(path)
        filename = path.split("/")[-1] or "download"
        return Response(
            content=data,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def index() -> FileResponse:
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
