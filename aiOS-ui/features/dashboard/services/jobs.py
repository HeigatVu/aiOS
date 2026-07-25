from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path


_ACTIVE_STATUSES = {"queued", "running"}
_FINAL_STATUSES = {"succeeded", "failed", "cancelled"}


@dataclass(frozen=True)
class Job:
    id: str
    kind: str
    payload: dict
    status: str
    created_at: float
    updated_at: float
    logs: list[str] = field(default_factory=list)


class JobStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(self) -> list[Job]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        jobs = [Job(**item) for item in raw.get("jobs", [])]
        return sorted(jobs, key=lambda job: job.created_at, reverse=True)

    def get(self, job_id: str) -> Job | None:
        return next((job for job in self.list() if job.id == job_id), None)

    def create(self, *, kind: str, payload: dict) -> Job:
        if not isinstance(kind, str) or not kind:
            raise ValueError("Job kind is required")
        if not isinstance(payload, dict):
            raise ValueError("Job payload must be an object")
        if any(job.status in _ACTIVE_STATUSES for job in self.list()):
            raise RuntimeError("Another mutating job is already active")
        now = time.time()
        job = Job(id=uuid.uuid4().hex, kind=kind, payload=payload, status="queued", created_at=now, updated_at=now)
        self._write([job, *self.list()])
        return job

    def finish(self, job_id: str, *, status: str) -> Job:
        if status not in _FINAL_STATUSES:
            raise ValueError("Job status must be final")
        jobs = self.list()
        updated = None
        result = []
        for job in jobs:
            if job.id == job_id:
                updated = Job(**{**asdict(job), "status": status, "updated_at": time.time()})
                result.append(updated)
            else:
                result.append(job)
        if updated is None:
            raise KeyError(job_id)
        self._write(result)
        return updated

    def start_next(self) -> Job | None:
        queued = sorted((job for job in self.list() if job.status == "queued"), key=lambda job: job.created_at)
        if not queued:
            return None
        return self._replace(queued[0].id, status="running")

    def append_log(self, job_id: str, message: str) -> Job:
        if not isinstance(message, str) or not message:
            raise ValueError("Job log message is required")
        job = self.get(job_id)
        if job is None:
            raise KeyError(job_id)
        return self._replace(job_id, logs=[*job.logs, message])

    def _replace(self, job_id: str, **changes) -> Job:
        jobs = self.list()
        updated = None
        result = []
        for job in jobs:
            if job.id == job_id:
                updated = Job(**{**asdict(job), **changes, "updated_at": time.time()})
                result.append(updated)
            else:
                result.append(job)
        if updated is None:
            raise KeyError(job_id)
        self._write(result)
        return updated

    def _write(self, jobs: list[Job]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps({"schema_version": 1, "jobs": [asdict(job) for job in jobs]}, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.path)
