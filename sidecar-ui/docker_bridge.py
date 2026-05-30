import os
import time
from collections import deque
from typing import Generator, Optional
import docker
import docker.errors

_stats_history: deque = deque(maxlen=60)


def get_docker_client() -> Optional[docker.DockerClient]:
    """
    Attempts to connect to the Docker socket.
    Returns None if unreachable or if MOCK_DOCKER env is set.
    """
    if os.environ.get("MOCK_DOCKER", "false").lower() == "true":
        return None
    try:
        return docker.from_env()
    except Exception:
        return None


def get_sandbox_status() -> dict:
    """
    Checks the status of the Docker socket connection and the ai_tui_sandbox container.
    """
    client = get_docker_client()
    if not client:
        return {
            "docker_connected": False,
            "sandbox_status": "running (simulated)",
            "sandbox_running": True,
            "is_mock": True,
        }

    try:
        container = client.containers.get("ai_tui_sandbox")
        return {
            "docker_connected": True,
            "sandbox_status": container.status,
            "sandbox_running": container.status == "running",
            "is_mock": False,
        }
    except docker.errors.NotFound:
        return {
            "docker_connected": True,
            "sandbox_status": "not_found",
            "sandbox_running": False,
            "is_mock": False,
        }
    except Exception:
        return {
            "docker_connected": False,
            "sandbox_status": "unknown",
            "sandbox_running": False,
            "is_mock": False,
        }


def execute_in_sandbox(cmd: str) -> Generator[str, None, None]:
    """
    Executes a command inside the ai_tui_sandbox container.
    Streams back the stdout/stderr output chunks.
    If the Docker socket is unreachable, streams a rich, simulated installation log.
    """
    client = get_docker_client()

    if not client:
        # --- RICH MOCK SIMULATION FOR MAXIMUM PORTABILITY ---
        yield "[SIMULATED SOCKET] Connecting to sandbox container 'ai_tui_sandbox'...\n"
        yield f"[SIMULATED SOCKET] Running: {cmd}\n\n"
        time.sleep(0.8)

        cmd_stripped = cmd.strip()

        if "uv pip install" in cmd_stripped or "pip install" in cmd_stripped:
            pkg = cmd_stripped.split()[-1]
            yield f"Resolved source packages for {pkg}...\n"
            time.sleep(0.4)
            yield f"Downloading {pkg}-2.4.1-py3-none-any.whl (124 kB)\n"
            yield "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 124.2/124.2 kB 3.1 MB/s eta 0:00:00\n"
            time.sleep(0.5)
            yield "Using cached packages for dependencies...\n"
            yield "Resolving dependencies...\n"
            time.sleep(0.4)
            yield "Installing collected packages...\n"
            time.sleep(0.6)
            yield f"Successfully installed {pkg}-2.4.1\n"

        elif "conda install" in cmd_stripped:
            pkg = cmd_stripped.split()[-1]
            yield "Collecting package metadata (current_repodata.json): done\n"
            yield "Solving environment: done\n\n"
            time.sleep(0.5)
            yield "## Package Plan ##\n\n"
            yield "  environment location: /opt/conda/envs/ai-baseline\n\n"
            yield "  added / updated specs:\n"
            yield f"    - {pkg}\n\n"
            yield "The following packages will be downloaded:\n\n"
            yield f"    package                    |            build\n"
            yield "    ---------------------------|-----------------\n"
            yield f"    {pkg}-1.2.3                 |   py312h1234567_0         1.2 MB  conda-forge\n"
            yield "    ------------------------------------------------------------\n"
            yield "                                           Total:         1.2 MB\n\n"
            yield "Proceed ([y]/n)? y\n\n"
            time.sleep(0.6)
            yield "Downloading and Extracting Packages:\n"
            yield f"Downloading {pkg}-1.2.3 ... 100%\n"
            yield "Preparing transaction: done\n"
            yield "Verifying transaction: done\n"
            yield "Executing transaction: done\n"

        elif "dnf install" in cmd_stripped:
            pkg = cmd_stripped.split()[-1]
            yield "Updating Subscription Management repositories.\n"
            yield "Fedora 44 openh264 (From Cisco) - Head            1.8 kB/s | 2.5 kB     00:01\n"
            yield "Fedora 44 - x86_64 - Updates                    3.2 MB/s |  22 MB     00:06\n"
            time.sleep(0.5)
            yield "Dependencies resolved.\n"
            yield "================================================================================\n"
            yield " Package            Architecture     Version            Repository         Size\n"
            yield "================================================================================\n"
            yield " Installing:\n"
            yield f"  {pkg}             x86_64           2.1.4-1.fc44       updates           142 k\n"
            yield "================================================================================\n"
            time.sleep(0.5)
            yield "Downloading Packages:\n"
            yield f"[{pkg}-2.1.4-1.fc44.x86_64.rpm] Downloading ... 100%\n"
            yield "Running transaction check\n"
            yield "Transaction member checking successful.\n"
            yield "Running transaction test\n"
            yield "Transaction test successful.\n"
            yield "Running transaction\n"
            yield f"  Installing       : {pkg}-2.1.4-1.fc44.x86_64                               1/1\n"
            yield f"  Verifying        : {pkg}-2.1.4-1.fc44.x86_64                               1/1\n"
            yield f"\nInstalled:\n  {pkg}-2.1.4-1.fc44.x86_64\n\nComplete!\n"

        elif "npm install" in cmd_stripped:
            pkg = cmd_stripped.split()[-1]
            yield "npm WARN deprecated harmless-library@1.0.2: no longer supported\n"
            time.sleep(0.3)
            yield f"npm HTTP GET https://registry.npmjs.org/{pkg}\n"
            yield f"npm HTTP 200 https://registry.npmjs.org/{pkg}\n"
            time.sleep(0.5)
            yield "added 18 packages, and audited 19 packages in 1.87s\n"
            yield "found 0 vulnerabilities\n\n"
            yield f"Successfully installed {pkg} globally!\n"

        elif "echo" in cmd_stripped:
            val = cmd_stripped.replace("echo", "").strip().replace('"', "").replace("'", "")
            yield f"{val}\n"
        else:
            yield f"Executing raw command: {cmd_stripped}\n"
            time.sleep(0.6)
            yield "Execution completed successfully.\n"

        yield "\n[SIMULATED SOCKET] Process finished with exit code 0\n"
        return

    # --- REAL DOCKER EXECUTION BRIDGE ---
    try:
        container = client.containers.get("ai_tui_sandbox")

        yield f"[DOCKER SOCKET] Connected to sandbox '{container.name}' ({container.short_id})\n"
        yield f"[DOCKER SOCKET] Running: {cmd}\n\n"

        exec_res = container.exec_run(cmd, stream=True)

        # docker-py exec_run stream=True returns either an ExecResult namedtuple
        # with (exit_code, generator) or a generator depending on the SDK version.
        if isinstance(exec_res, tuple):
            _, generator = exec_res
        else:
            generator = exec_res

        for chunk in generator:
            yield chunk.decode("utf-8", errors="replace")

    except docker.errors.NotFound:
        yield "ERROR: Container 'ai_tui_sandbox' was not found on this host!\n"
        yield "Please run 'docker compose up -d' to start the sandbox container.\n"
    except Exception as e:
        yield f"ERROR executing command: {str(e)}\n"


def live_remount_volume(container_path: str, mode: str) -> tuple[bool, str]:
    """
    Attempt to remount a path inside ai_tui_sandbox with the given mode (rw/ro).
    Uses a privileged exec so the container itself does not need SYS_ADMIN.
    Returns (success, output_message).
    """
    client = get_docker_client()
    if not client:
        return False, "Docker not connected (mock mode)"
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(
            ["mount", "-o", f"remount,{mode}", container_path],
            privileged=True,
            user="root",
        )
        output = result.output.decode("utf-8", errors="replace").strip() if result.output else ""
        return result.exit_code == 0, output
    except docker.errors.NotFound:
        return False, "Container 'ai_tui_sandbox' not found"
    except Exception as e:
        return False, str(e)


def restart_sandbox() -> dict:
    client = get_docker_client()
    if not client:
        return {"ok": False, "error": "Docker not connected (mock mode)"}
    try:
        container = client.containers.get("ai_tui_sandbox")
        container.restart()
        return {"ok": True}
    except docker.errors.NotFound:
        return {"ok": False, "error": "Container 'ai_tui_sandbox' not found"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _get_gpu_stats(container: docker.models.containers.Container) -> Optional[dict]:
    try:
        result = container.exec_run(
            ["nvidia-smi", "--query-gpu=name,utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
        )
        if result.exit_code != 0:
            return None
        output = result.output.decode("utf-8", errors="replace").strip()
        if not output:
            return None
        parts = [p.strip() for p in output.splitlines()[0].split(",")]
        if len(parts) < 4:
            return None
        return {
            "name": parts[0],
            "utilization": float(parts[1]),
            "mem_used_mb": float(parts[2]),
            "mem_total_mb": float(parts[3]),
        }
    except Exception:
        return None


def get_sandbox_stats() -> dict:
    client = get_docker_client()
    if not client:
        return {
            "cpu_percent": 0.0,
            "mem_usage_mb": 0.0,
            "mem_limit_mb": 0.0,
            "mem_percent": 0.0,
            "gpu": None,
            "is_mock": True,
        }
    try:
        container = client.containers.get("ai_tui_sandbox")
        raw = container.stats(stream=False)

        cpu_delta = (
            raw["cpu_stats"]["cpu_usage"]["total_usage"]
            - raw["precpu_stats"]["cpu_usage"]["total_usage"]
        )
        system_delta = (
            raw["cpu_stats"].get("system_cpu_usage", 0)
            - raw["precpu_stats"].get("system_cpu_usage", 0)
        )
        num_cpus = raw["cpu_stats"].get("online_cpus") or len(
            raw["cpu_stats"]["cpu_usage"].get("percpu_usage", [1])
        )
        cpu_percent = (cpu_delta / system_delta * num_cpus * 100.0) if system_delta > 0 else 0.0

        mem_usage = raw["memory_stats"].get("usage", 0)
        mem_limit = raw["memory_stats"].get("limit", 1)
        mem_usage_mb = mem_usage / 1024 / 1024
        mem_limit_mb = mem_limit / 1024 / 1024
        mem_percent = (mem_usage / mem_limit * 100.0) if mem_limit > 0 else 0.0

        return {
            "cpu_percent": round(cpu_percent, 1),
            "mem_usage_mb": round(mem_usage_mb, 1),
            "mem_limit_mb": round(mem_limit_mb, 1),
            "mem_percent": round(mem_percent, 1),
            "gpu": _get_gpu_stats(container),
            "is_mock": False,
        }
    except docker.errors.NotFound:
        return {"cpu_percent": 0.0, "mem_usage_mb": 0.0, "mem_limit_mb": 0.0, "mem_percent": 0.0, "gpu": None, "is_mock": False}
    except Exception:
        return {"cpu_percent": 0.0, "mem_usage_mb": 0.0, "mem_limit_mb": 0.0, "mem_percent": 0.0, "gpu": None, "is_mock": False}


def stream_logs(tail: int = 100) -> Generator[str, None, None]:
    client = get_docker_client()
    if not client:
        yield "[MOCK] No Docker connection — simulated log stream\n"
        for i in range(5):
            yield f"[MOCK] Log line {i + 1}\n"
            time.sleep(0.3)
        return
    try:
        container = client.containers.get("ai_tui_sandbox")
        for chunk in container.logs(stream=True, follow=True, tail=tail):
            yield chunk.decode("utf-8", errors="replace")
    except docker.errors.NotFound:
        yield "ERROR: Container 'ai_tui_sandbox' not found\n"
    except Exception as e:
        yield f"ERROR: {str(e)}\n"


def list_files_in_container(path: str) -> list[dict]:
    """
    Lists files in the given path inside the ai_tui_sandbox container.
    Returns a list of dicts with keys: permissions, owner, group, size, type, name, is_dir.
    Falls back to a mock list if in mock mode or if the container is unavailable.
    """
    client = get_docker_client()

    if not client:
        return [
            {
                "permissions": "755",
                "owner": "root",
                "group": "root",
                "size": "4096",
                "type": "directory",
                "name": path,
                "is_dir": True,
            },
            {
                "permissions": "644",
                "owner": "user",
                "group": "user",
                "size": "1024",
                "type": "regular file",
                "name": f"{path}/example.txt",
                "is_dir": False,
            },
            {
                "permissions": "755",
                "owner": "user",
                "group": "user",
                "size": "4096",
                "type": "directory",
                "name": f"{path}/subdir",
                "is_dir": True,
            },
        ]

    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(
            ["sh", "-c", f"find {path} -maxdepth 1 -exec stat -c '%a|%U|%G|%s|%F|%n' {{}} + 2>/dev/null"]
        )
        output = result.output.decode("utf-8", errors="replace") if result.output else ""
        files: list[dict] = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split("|", 5)
            if len(parts) < 6:
                continue
            permissions, owner, group, size, ftype, name = parts
            files.append(
                {
                    "permissions": permissions,
                    "owner": owner,
                    "group": group,
                    "size": size,
                    "type": ftype,
                    "name": name,
                    "is_dir": ftype == "directory",
                }
            )
        return files
    except docker.errors.NotFound:
        return []
    except Exception:
        return []


def read_file_in_container(path: str) -> str:
    """Reads a file from the container, returning its string content."""
    client = get_docker_client()
    if not client:
        # mock mode
        if os.path.exists(path):
            with open(path, "r", errors="replace") as f:
                return f.read()
        return f"[MOCK] Content of file {path}"
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["cat", path], user="root")
        if result.exit_code != 0:
            raise Exception(result.output.decode("utf-8", errors="replace"))
        return result.output.decode("utf-8", errors="replace")
    except Exception as e:
        raise Exception(f"Failed to read file: {str(e)}")


def write_file_in_container(path: str, content: str) -> None:
    """Writes content to a file in the container securely using base64."""
    import base64
    client = get_docker_client()
    if not client:
        # mock mode
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return
    try:
        container = client.containers.get("ai_tui_sandbox")
        encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        cmd = ["sh", "-c", f"echo '{encoded}' | base64 -d > '{path}'"]
        result = container.exec_run(cmd, user="root")
        if result.exit_code != 0:
            raise Exception(result.output.decode("utf-8", errors="replace"))
    except Exception as e:
        raise Exception(f"Failed to write file: {str(e)}")


def read_binary_file_in_container(path: str) -> bytes:
    """Reads a file from the container as raw bytes."""
    client = get_docker_client()
    if not client:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        return b"mock binary data"
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["cat", path], user="root")
        if result.exit_code != 0:
            raise Exception(result.output.decode("utf-8", errors="replace"))
        return result.output
    except Exception as e:
        raise Exception(f"Failed to read binary file: {str(e)}")


def write_binary_file_in_container(path: str, data: bytes) -> None:
    """Writes raw bytes to a file in the container using base64."""
    import base64
    client = get_docker_client()
    if not client:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        return
    try:
        container = client.containers.get("ai_tui_sandbox")
        encoded = base64.b64encode(data).decode("utf-8")
        cmd = ["sh", "-c", f"echo '{encoded}' | base64 -d > '{path}'"]
        result = container.exec_run(cmd, user="root")
        if result.exit_code != 0:
            raise Exception(result.output.decode("utf-8", errors="replace"))
    except Exception as e:
        raise Exception(f"Failed to write binary file: {str(e)}")



def list_processes() -> list[dict]:
    """Lists running processes inside the sandbox container."""
    client = get_docker_client()
    if not client:
        return [
            {"pid": "1", "user": "root", "cpu": "0.0", "mem": "0.1", "vsz": "1024", "rss": "512", "tty": "?", "stat": "Ss", "start": "14:30", "time": "0:00", "command": "/bin/bash"},
            {"pid": "42", "user": "ai_user", "cpu": "1.2", "mem": "4.5", "vsz": "204850", "rss": "85900", "tty": "pts/0", "stat": "Sl", "start": "14:32", "time": "0:05", "command": "python my_agent.py"},
        ]
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["ps", "aux"])
        if result.exit_code != 0:
            return []
        output = result.output.decode("utf-8", errors="replace")
        lines = output.splitlines()
        if not lines:
            return []
        
        headers = lines[0].split()
        processes = []
        for line in lines[1:]:
            parts = line.split(None, len(headers) - 1)
            if len(parts) < len(headers):
                continue
            processes.append({
                "user": parts[0],
                "pid": parts[1],
                "cpu": parts[2],
                "mem": parts[3],
                "vsz": parts[4],
                "rss": parts[5],
                "tty": parts[6],
                "stat": parts[7],
                "start": parts[8],
                "time": parts[9],
                "command": parts[10]
            })
        return processes
    except Exception:
        return []


def kill_process(pid: str) -> dict:
    """Kills a process inside the sandbox container."""
    client = get_docker_client()
    if not client:
        return {"ok": True, "msg": f"[MOCK] Process {pid} killed"}
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["kill", "-9", pid])
        if result.exit_code == 0:
            return {"ok": True}
        else:
            return {"ok": False, "error": result.output.decode("utf-8", errors="replace")}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def get_env_vars(path: Optional[str] = None) -> dict:
    """Get active container environments and local .env keys."""
    client = get_docker_client()
    container_env = {}
    if client:
        try:
            container = client.containers.get("ai_tui_sandbox")
            env_list = container.attrs.get("Config", {}).get("Env", [])
            for item in env_list:
                if "=" in item:
                    k, v = item.split("=", 1)
                    container_env[k] = v
        except Exception:
            pass
    else:
        container_env = {"MOCK_ENV": "true", "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}

    import volumes
    dots_env = {}
    env_file_path = path if path else os.path.join(volumes.WORKSPACE_DIR, ".env")
    
    try:
        if path:
            content = read_file_in_container(path)
        else:
            if os.path.exists(env_file_path):
                with open(env_file_path, "r") as f:
                    content = f.read()
            else:
                content = ""
                
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            dots_env[k.strip()] = v.strip().strip('"').strip("'")
    except Exception:
        pass

    return {
        "container_env": container_env,
        "dotenv": dots_env,
    }


def save_dotenv_var(key: str, value: str, path: Optional[str] = None) -> dict:
    """Save an environment variable to a specific .env file in container or workspace."""
    import volumes
    env_file_path = path if path else os.path.join(volumes.WORKSPACE_DIR, ".env")
    
    lines = []
    found = False
    try:
        if path:
            content = read_file_in_container(path)
        else:
            if os.path.exists(env_file_path):
                with open(env_file_path, "r") as f:
                    content = f.read()
            else:
                content = ""
        lines = content.splitlines(keepends=True)
    except Exception:
        lines = []
        
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or "=" not in stripped:
            new_lines.append(line)
            continue
        k, v = stripped.split("=", 1)
        if k.strip() == key:
            suffix = "\r\n" if line.endswith("\r\n") else "\n"
            new_lines.append(f"{key}={value}{suffix}")
            found = True
        else:
            new_lines.append(line)
            
    if not found:
        new_lines.append(f"{key}={value}\n")
        
    try:
        new_content = "".join(new_lines)
        if path:
            write_file_in_container(path, new_content)
        else:
            with open(env_file_path, "w") as f:
                f.write(new_content)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": f"Failed to write .env: {str(e)}"}


def delete_dotenv_var(key: str, path: Optional[str] = None) -> dict:
    """Delete an environment variable from a specific .env file in container or workspace."""
    import volumes
    env_file_path = path if path else os.path.join(volumes.WORKSPACE_DIR, ".env")
    
    lines = []
    try:
        if path:
            content = read_file_in_container(path)
        else:
            if os.path.exists(env_file_path):
                with open(env_file_path, "r") as f:
                    content = f.read()
            else:
                content = ""
        lines = content.splitlines(keepends=True)
    except Exception:
        lines = []
        
    new_lines = []
    found = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#") or "=" not in stripped:
            new_lines.append(line)
            continue
        k, v = stripped.split("=", 1)
        if k.strip() == key:
            found = True
            continue  # skip writing the line to delete it
        else:
            new_lines.append(line)
            
    try:
        new_content = "".join(new_lines)
        if path:
            write_file_in_container(path, new_content)
        else:
            with open(env_file_path, "w") as f:
                f.write(new_content)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": f"Failed to delete .env key: {str(e)}"}



def get_listening_ports() -> list[dict]:
    """Gets active listening ports in the container."""
    client = get_docker_client()
    if not client:
        return [
            {"proto": "tcp", "local_addr": "127.0.0.1:3113", "pid": "12", "program": "uvicorn"},
            {"proto": "tcp", "local_addr": "0.0.0.0:8082", "pid": "45", "program": "nginx"},
        ]
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["ss", "-tlnp"])
        if result.exit_code == 0:
            return _parse_ss_output(result.output.decode("utf-8", errors="replace"))
            
        result = container.exec_run(["netstat", "-tlnp"])
        if result.exit_code == 0:
            return _parse_netstat_output(result.output.decode("utf-8", errors="replace"))
            
        result = container.exec_run(["ss", "-tln"])
        if result.exit_code == 0:
            return _parse_ss_output_no_pid(result.output.decode("utf-8", errors="replace"))
            
        return []
    except Exception:
        return []


def _parse_ss_output(output: str) -> list[dict]:
    ports = []
    lines = output.splitlines()
    if len(lines) < 2:
        return []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[3]
        proc = parts[5] if len(parts) > 5 else "-"
        
        pid = "-"
        prog = "-"
        if "pid=" in proc:
            try:
                subparts = proc.split('pid=')
                pid = subparts[1].split(',')[0]
                prog = proc.split('"')[1]
            except Exception:
                pass
                
        ports.append({
            "proto": "tcp",
            "local_addr": local,
            "pid": pid,
            "program": prog
        })
    return ports


def _parse_netstat_output(output: str) -> list[dict]:
    ports = []
    lines = output.splitlines()
    for line in lines:
        if not line.startswith("tcp"):
            continue
        parts = line.split()
        if len(parts) < 6:
            continue
        proto = parts[0]
        local = parts[3]
        proc = parts[6] if len(parts) > 6 else "-"
        pid, prog = "-", "-"
        if "/" in proc:
            pid, prog = proc.split("/", 1)
        ports.append({
            "proto": proto,
            "local_addr": local,
            "pid": pid,
            "program": prog
        })
    return ports


def _parse_ss_output_no_pid(output: str) -> list[dict]:
    ports = []
    lines = output.splitlines()
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 4:
            continue
        ports.append({
            "proto": "tcp",
            "local_addr": parts[3],
            "pid": "-",
            "program": "-"
        })
    return ports


def record_stats() -> None:
    sample = get_sandbox_stats()
    sample['ts'] = time.time()
    _stats_history.append(sample)


def get_stats_history() -> list[dict]:
    return list(_stats_history)


def query_sqlite_in_container(db_path: str, query: str) -> dict:
    """Executes a query on an SQLite database inside the container."""
    import json
    client = get_docker_client()
    if not client:
        return {
            "ok": True,
            "columns": ["id", "name", "value"],
            "rows": [
                {"id": 1, "name": "mock_setting", "value": "enabled"},
                {"id": 2, "name": "theme", "value": "dark"},
            ],
            "count": 2
        }
        
    py_code = """
import sqlite3, json, sys
try:
    conn = sqlite3.connect(sys.argv[1])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sys.argv[2])
    if cursor.description:
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        res = {"columns": cols, "rows": [dict(r) for r in rows], "count": len(rows), "ok": True}
    else:
        conn.commit()
        res = {"count": cursor.rowcount, "ok": True}
    print(json.dumps(res))
except Exception as e:
    print(json.dumps({"ok": False, "error": str(e)}))
"""
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["python", "-c", py_code, db_path, query])
        if result.exit_code != 0:
            return {"ok": False, "error": result.output.decode("utf-8", errors="replace")}
            
        output = result.output.decode("utf-8", errors="replace").strip()
        return json.loads(output)
    except Exception as e:
        return {"ok": False, "error": str(e)}
