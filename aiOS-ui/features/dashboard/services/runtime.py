from __future__ import annotations

import logging
import os
import secrets
import signal
import subprocess
import time
from collections.abc import Mapping
from pathlib import Path

from services.paths import RuntimePaths
from services.worker import run_once

logger = logging.getLogger(__name__)


def ensure_agentmemory_secret(paths: RuntimePaths) -> str:
    secret_file = paths.state / "credentials" / "agentmemory-viewer-secret"
    if secret_file.is_file():
        secret = secret_file.read_text(encoding="utf-8").strip()
        if secret:
            return secret
    secret_file.parent.mkdir(parents=True, exist_ok=True)
    secret = secrets.token_urlsafe(32)
    secret_file.write_text(f"{secret}\n", encoding="utf-8")
    secret_file.chmod(0o600)
    return secret


def build_runtime_environment(paths: RuntimePaths, environ: Mapping[str, str] | None = None) -> dict[str, str]:
    environment = dict(os.environ if environ is None else environ)
    secret = ensure_agentmemory_secret(paths)
    environment["AGENTMEMORY_HOME"] = str(paths.state / "agentmemory")
    environment["AGENTMEMORY_VIEWER_HOST"] = "0.0.0.0"
    environment["AGENTMEMORY_SECRET"] = secret
    environment["VIEWER_ALLOWED_HOSTS"] = "localhost:3113"
    environment["CODEGRAPH_PROJECT"] = str(paths.workspace)
    return environment


def agentmemory_environment(paths: RuntimePaths, environ: Mapping[str, str]) -> dict[str, str]:
    environment = dict(environ)
    environment["HOME"] = str(paths.state / "agentmemory")
    return environment


def codegraph_index_command(workspace: Path) -> list[str]:
    action = "sync" if (workspace / ".codegraph" / "codegraph.db").is_file() else "init"
    return ["codegraph", action, str(workspace)]


def _start_agentmemory(
    *, paths: RuntimePaths, workspace: Path, environment: Mapping[str, str]
) -> subprocess.Popen[bytes]:
    child_environment = agentmemory_environment(paths, environment)
    Path(child_environment["HOME"]).mkdir(parents=True, exist_ok=True)
    return subprocess.Popen(
        ["agentmemory", "start"],
        cwd=workspace,
        env=child_environment,
        start_new_session=True,
    )


def _stop_agentmemory(process: subprocess.Popen[bytes], timeout: float = 10.0) -> None:
    if process.poll() is not None:
        return
    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5.0)


def main() -> None:
    project_root = Path(os.environ.get("AIOS_PROJECT_ROOT", "/aios"))
    paths = RuntimePaths.from_project_root(project_root)
    paths.ensure_data_directories()
    catalog_path = Path(os.environ.get("AIOS_AGENT_CATALOG", paths.app / "config" / "agent-catalog.json"))
    poll_seconds = float(os.environ.get("AIOS_JOB_POLL_SECONDS", "1"))
    environment = build_runtime_environment(paths)

    index = subprocess.run(
        codegraph_index_command(paths.workspace),
        cwd=paths.workspace,
        env=environment,
        check=False,
    )
    if index.returncode:
        logger.warning("CodeGraph index command exited with status %s", index.returncode)

    agentmemory = _start_agentmemory(paths=paths, workspace=paths.workspace, environment=environment)
    running = True

    def stop(_signum: int, _frame: object) -> None:
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)
    try:
        while running:
            if agentmemory.poll() is not None:
                raise RuntimeError(f"AgentMemory exited with status {agentmemory.returncode}")
            run_once(paths=paths, catalog_path=catalog_path)
            time.sleep(poll_seconds)
    finally:
        _stop_agentmemory(agentmemory)


if __name__ == "__main__":
    main()
