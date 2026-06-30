#!/usr/bin/env python3
"""Service Health CLI Tool — checks 7 container services concurrently.

Zero external dependencies (stdlib only). All checks run in parallel via
asyncio.gather() with a strict 2-second timeout per probe. Outputs a
compact color table and exits 0 if all healthy, 1 if any fail.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from typing import Callable, Coroutine

__version__ = "0.1.0"

# ── ANSI colors ────────────────────────────────────────────────────────────────

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ── Check function registry ────────────────────────────────────────────────────

# (name: str) -> async callable returning (ok: bool, detail: str)
CHECKS: dict[str, Callable[[], Coroutine[None, None, tuple[bool, str]]]] = {}


# ── Helpers ────────────────────────────────────────────────────────────────────


def is_pid_alive(pid: int) -> bool:
    """Return True if a process with the given PID exists."""
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # process exists, just can't signal it
    except Exception:
        return False


def read_pid_file(filepath: str) -> int:
    """Read an integer PID from a file, expanding ~ if needed."""
    expanded = os.path.expanduser(filepath)
    if not os.path.exists(expanded):
        raise FileNotFoundError(f"PID file not found: {filepath}")
    with open(expanded, encoding="utf-8") as fh:
        return int(fh.read().strip())


async def probe_tcp(port: int, host: str = "127.0.0.1") -> bool:
    """Return True if a TCP connection to host:port succeeds."""
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return True
    except Exception:
        return False


def get_container_ip() -> str:
    """Return the container's primary IP address."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


async def probe_http(url: str) -> tuple[bool, str]:
    """HTTP GET *url* and return (ok, detail). Runs in a thread via urllib."""
    import urllib.request

    def _req() -> tuple[bool, str]:
        try:
            with urllib.request.urlopen(url, timeout=2.0) as resp:  # noqa: S310
                return resp.status == 200, f"HTTP {resp.status}"
        except Exception as exc:
            return False, f"HTTP request failed: {exc}"

    try:
        return await asyncio.to_thread(_req)
    except Exception as exc:
        return False, f"Thread error: {exc}"


async def run_check_with_timeout(
    name: str, check_func: Callable[[], Coroutine[None, None, tuple[bool, str]]]
) -> tuple[bool, str]:
    """Run *check_func* with a 2-second timeout, returning (ok, detail)."""
    try:
        return await asyncio.wait_for(check_func(), timeout=2.0)
    except asyncio.TimeoutError:
        return False, "Timeout after 2.0s"
    except Exception as exc:
        return False, f"Error: {exc}"


# ── Individual service checks ──────────────────────────────────────────────────


async def check_iii_engine() -> tuple[bool, str]:
    """Verify iii --version reports v0.11.2."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "iii",
            "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        if proc.returncode != 0:
            return False, f"Command exited with {proc.returncode}"
        version = stdout.decode().strip()
        if "0.11.2" in version:
            return True, "Version: 0.11.2"
        return False, f"Incorrect version: {version}"
    except FileNotFoundError:
        return False, "iii binary not found"
    except Exception as exc:
        return False, f"Failed to run: {exc}"


async def check_agentmemory() -> tuple[bool, str]:
    """TCP-probe port 3111 and verify agentmemory status."""
    if not await probe_tcp(3111):
        return False, "TCP probe failed on port 3111"
    try:
        proc = await asyncio.create_subprocess_exec(
            "agentmemory",
            "status",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        if proc.returncode != 0:
            return False, f"agentmemory status exited with {proc.returncode}"
        return True, "Port 3111 open, status active"
    except Exception as exc:
        return False, f"Failed to run agentmemory status: {exc}"


async def check_viewer_proxy() -> tuple[bool, str]:
    """Check viewer-proxy PID and TCP port 3113."""
    try:
        pid = read_pid_file("~/.agentmemory/viewer-proxy.pid")
    except Exception as exc:
        return False, f"PID file error: {exc}"
    if not is_pid_alive(pid):
        return False, f"PID {pid} is not running"
    if not await probe_tcp(3113):
        return False, f"PID {pid} active, but TCP probe failed on port 3113"
    return True, f"PID {pid} active, Port 3113 open"


async def check_hermes_dashboard() -> tuple[bool, str]:
    """Check hermes dashboard PID and TCP port 9119 on localhost."""
    try:
        pid = read_pid_file("/tmp/hermes-dashboard.pid")
    except Exception as exc:
        return False, f"PID file error: {exc}"
    if not is_pid_alive(pid):
        return False, f"PID {pid} is not running"
    if not await probe_tcp(9119, host="127.0.0.1"):
        return False, f"PID {pid} active, but TCP probe failed on localhost port 9119"
    return True, f"PID {pid} active, Port 9119 open on localhost"


async def check_dashboard_proxy() -> tuple[bool, str]:
    """Check dashboard-proxy PID and TCP port 9119 on container IP."""
    try:
        pid = read_pid_file("/tmp/hermes-proxy.pid")
    except Exception as exc:
        return False, f"PID file error: {exc}"
    if not is_pid_alive(pid):
        return False, f"PID {pid} is not running"
    ip = get_container_ip()
    if not await probe_tcp(9119, host=ip):
        return False, f"PID {pid} active, but TCP probe failed on host {ip} port 9119"
    return True, f"PID {pid} active, Port 9119 open on host {ip}"



async def check_hermes_gateway() -> tuple[bool, str]:
    """Parse gateway_state.json and verify PID + Telegram state."""
    filepath = os.path.expanduser("~/.hermes/gateway_state.json")
    if not os.path.exists(filepath):
        return False, "gateway_state.json not found"
    try:
        with open(filepath, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as exc:
        return False, f"Failed to parse JSON: {exc}"
    pid = data.get("pid")
    if not pid:
        return False, "PID not found in state JSON"
    if not is_pid_alive(pid):
        return False, f"PID {pid} is not running"
    try:
        tg_state = data["platforms"]["telegram"]["state"]
    except KeyError:
        return False, "Telegram state key path not found in JSON"
    if tg_state != "connected":
        return False, f"Telegram state: {tg_state} (expected connected)"
    try:
        proc = await asyncio.create_subprocess_exec(
            "hermes",
            "gateway",
            "status",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, _ = await proc.communicate()
        if proc.returncode != 0:
            return False, f"hermes gateway status exited with {proc.returncode}"
    except Exception as exc:
        return False, f"Failed to run hermes gateway status: {exc}"
    return True, f"PID {pid} active, Telegram connected, status OK"


# ── Register checks ────────────────────────────────────────────────────────────

CHECKS["iii engine"] = check_iii_engine
CHECKS["agentmemory"] = check_agentmemory
CHECKS["viewer-proxy"] = check_viewer_proxy
CHECKS["hermes dashboard"] = check_hermes_dashboard
CHECKS["dashboard-proxy"] = check_dashboard_proxy
CHECKS["hermes gateway"] = check_hermes_gateway


# ── Main runner ────────────────────────────────────────────────────────────────


async def main() -> None:
    """Run all health checks concurrently and print a color table."""
    header = f"{BOLD}{'Service':<20} {'Status':<8} {'Detail'}{RESET}"
    print(header)
    print("─" * 60)

    names = list(CHECKS.keys())
    tasks = [run_check_with_timeout(name, CHECKS[name]) for name in names]
    results = await asyncio.gather(*tasks)

    all_healthy = True
    for name, (ok_flag, detail) in zip(names, results):
        if not ok_flag:
            all_healthy = False
            status_str = f"{RED}FAIL{RESET}"
        else:
            status_str = f"{GREEN}OK{RESET}"
        # ANSI codes don't count for column width — pad after the visible text
        print(f"{name:<20} {status_str:<17} {detail}")

    sys.exit(0 if all_healthy else 1)


if __name__ == "__main__":
    asyncio.run(main())
