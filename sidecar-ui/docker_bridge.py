import os
import time
from typing import Generator, Optional
import docker
import docker.errors


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
