import asyncio
import json
import os
import pty
import fcntl
import struct
import termios
import subprocess
from pathlib import Path
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

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

DASHBOARD_DIR = Path(__file__).resolve().parent.parent

@router.get("/terminals", response_class=HTMLResponse)
async def get_terminals():
    candidates = [
        Path("/aiOS-ui/features/dashboard/static/terminal/index.html"),
        DASHBOARD_DIR / "static" / "terminal" / "index.html",
        PROJECT_ROOT / "features" / "dashboard" / "static" / "terminal" / "index.html",
        PROJECT_ROOT / "aiOS-ui" / "features" / "dashboard" / "static" / "terminal" / "index.html",
        Path("/home/HeigatWorkspace/My-file/my-project/my-assistance/aiOS-ui/features/dashboard/static/terminal/index.html"),
    ]
    for path in candidates:
        if path.exists():
            return path.read_text()
    return "Terminal HTML not found"

@router.websocket("/ws/terminal")
async def terminal_ws(websocket: WebSocket, cols: int = 80, rows: int = 24, user: str = "ai_user"):
    await websocket.accept()
    
    pid, fd = pty.fork()
    if pid == 0:
        os.environ["TERM"] = "xterm-256color"
        
        if not is_outside_docker:
            # We are already inside docker: run shell directly
            for shell in ["zsh", "bash", "sh"]:
                try:
                    os.execvp(shell, [shell])
                except FileNotFoundError:
                    continue
        else:
            # Change directory to project root so docker compose find docker-compose.yml
            try:
                os.chdir(PROJECT_ROOT)
            except Exception:
                pass

            # On the host: determine the container engine and execution command
            cmd_prefix = None
            
            # 1. Try Docker Compose
            try:
                res = subprocess.run(["docker", "compose", "ps", "--status", "running", "--format", "json"], capture_output=True, text=True, timeout=2)
                if res.returncode == 0 and "agent-runtime" in res.stdout:
                    cmd_prefix = ["docker", "compose", "exec", "-it", "-w", "/workspace", "agent-runtime", "/bin/zsh"]
            except Exception:
                pass

            # 2. Try Podman Compose
            if not cmd_prefix:
                try:
                    res = subprocess.run(["podman", "compose", "ps", "--format", "json"], capture_output=True, text=True, timeout=2)
                    if res.returncode == 0 and "agent-runtime" in res.stdout:
                        cmd_prefix = ["podman", "compose", "exec", "-it", "-w", "/workspace", "agent-runtime", "/bin/zsh"]
                except Exception:
                    pass

            # 3. Try raw Docker inspect
            if not cmd_prefix:
                try:
                    res = subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", "ai_tui_sandbox"], capture_output=True, text=True, timeout=2)
                    if res.returncode == 0 and "true" in res.stdout.lower():
                        cmd_prefix = ["docker", "exec", "-it", "-u", user, "-w", "/workspace", "ai_tui_sandbox", "/bin/zsh"]
                except Exception:
                    pass

            # 4. Try raw Podman inspect
            if not cmd_prefix:
                try:
                    res = subprocess.run(["podman", "inspect", "-f", "{{.State.Running}}", "ai_tui_sandbox"], capture_output=True, text=True, timeout=2)
                    if res.returncode == 0 and "true" in res.stdout.lower():
                        cmd_prefix = ["podman", "exec", "-it", "-u", user, "-w", "/workspace", "ai_tui_sandbox", "/bin/zsh"]
                except Exception:
                    pass

            # Try executing the determined container command
            if cmd_prefix:
                try:
                    os.execvp(cmd_prefix[0], cmd_prefix)
                except FileNotFoundError:
                    pass
            
            # Fallback to local shell on host if container exec failed or wasn't found
            for shell in ["zsh", "bash", "sh"]:
                try:
                    os.execvp(shell, [shell])
                except FileNotFoundError:
                    continue
        
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
