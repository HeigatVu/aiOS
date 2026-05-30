import asyncio
import queue
import threading
from typing import Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
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


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/status")
def get_status() -> dict:
    return docker_bridge.get_sandbox_status()


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


@app.post("/api/volumes/{idx}/mode")
def set_volume_mode(idx: int, body: VolumeModeBody) -> dict:
    try:
        volumes.update_volume_mode(idx, body.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IndexError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"ok": True}


@app.get("/api/volumes/{idx}/files")
def get_volume_files(idx: int) -> list[dict]:
    vol_list = volumes.list_volumes()
    if idx < 0 or idx >= len(vol_list):
        raise HTTPException(status_code=404, detail=f"Volume index {idx} not found")
    container_path = vol_list[idx]["container_path"]
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


@app.get("/")
def index() -> FileResponse:
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
