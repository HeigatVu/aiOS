import asyncio
import json
import os
import pty
import fcntl
import struct
import termios
from pathlib import Path
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

@router.get("/terminals", response_class=HTMLResponse)
async def get_terminals():
    terminal_html_path = PROJECT_ROOT / "aiOS-ui" / "dashboard" / "static" / "terminal" / "index.html"
    if terminal_html_path.exists():
        return terminal_html_path.read_text()
    return "Terminal HTML not found"

@router.websocket("/ws/terminal")
async def terminal_ws(websocket: WebSocket, cols: int = 80, rows: int = 24):
    await websocket.accept()
    
    pid, fd = pty.fork()
    if pid == 0:
        os.environ["TERM"] = "xterm-256color"
        os.execvp("docker", ["docker", "exec", "-it", "-u", "ai_user", "-w", "/workspace", "ai_tui_sandbox", "/bin/zsh"])
        
    wsz = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, wsz)
    
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()
    
    def pty_ready():
        try:
            data = os.read(fd, 4096)
            if data:
                queue.put_nowait(data)
            else:
                loop.remove_reader(fd)
                queue.put_nowait(None)
        except OSError:
            loop.remove_reader(fd)
            queue.put_nowait(None)
            
    loop.add_reader(fd, pty_ready)
    
    async def send_to_ws():
        while True:
            data = await queue.get()
            if data is None:
                break
            try:
                await websocket.send_bytes(data)
            except Exception:
                break
                
    async def receive_from_ws():
        try:
            while True:
                message = await websocket.receive()
                if "text" in message:
                    try:
                        msg = json.loads(message["text"])
                        if msg.get("type") == "resize":
                            r = int(msg.get("rows", 24))
                            c = int(msg.get("cols", 80))
                            wsz_new = struct.pack("HHHH", r, c, 0, 0)
                            fcntl.ioctl(fd, termios.TIOCSWINSZ, wsz_new)
                        elif msg.get("type") == "data":
                            os.write(fd, msg["data"].encode("utf-8"))
                    except ValueError:
                        os.write(fd, message["text"].encode("utf-8"))
                elif "bytes" in message:
                    os.write(fd, message["bytes"])
        except WebSocketDisconnect:
            pass
            
    try:
        await asyncio.gather(send_to_ws(), receive_from_ws())
    finally:
        try:
            loop.remove_reader(fd)
        except Exception:
            pass
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            pass
