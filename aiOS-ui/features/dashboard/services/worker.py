from __future__ import annotations

import os
import time
from pathlib import Path

from services.agents import AgentCatalog, ExtensionStore
from services.execution import AgentJobExecutor, CommandRunner
from services.jobs import Job, JobStore
from services.paths import RuntimePaths


def run_once(*, paths: RuntimePaths, catalog_path: Path, command_runner: CommandRunner | None = None) -> Job | None:
    catalog = AgentCatalog.from_file(catalog_path)
    store = JobStore(paths.jobs)
    _queue_restored_extension(paths=paths, store=store)
    executor = AgentJobExecutor(catalog=catalog, store=store, command_runner=command_runner)
    return executor.run_next()


def _queue_restored_extension(*, paths: RuntimePaths, store: JobStore) -> None:
    jobs = store.list()
    if any(job.status in {"queued", "running"} for job in jobs):
        return
    for extension in ExtensionStore(paths.extensions_lock).list():
        payload = {"source": extension.source, "name": extension.name, "version": extension.version}
        if any(job.kind == "extension-install" and job.payload == payload for job in jobs):
            continue
        store.create(kind="extension-install", payload=payload)
        return


def main() -> None:
    project_root = Path(os.environ.get("AIOS_PROJECT_ROOT", "/aios"))
    paths = RuntimePaths.from_project_root(project_root)
    catalog_path = Path(os.environ.get("AIOS_AGENT_CATALOG", paths.app / "config" / "agent-catalog.json"))
    poll_seconds = float(os.environ.get("AIOS_JOB_POLL_SECONDS", "1"))
    while True:
        run_once(paths=paths, catalog_path=catalog_path)
        time.sleep(poll_seconds)


if __name__ == "__main__":
    main()
