from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from services.agents import AgentCatalog, ExtensionStore
from services.jobs import JobStore
from services.paths import RuntimePaths


class AgentJobRequest(BaseModel):
    action: Literal["check", "update"]
    agents: list[str] = Field(min_length=1)


class ExtensionRequest(BaseModel):
    source: Literal["npm", "pypi"]
    name: str = Field(min_length=1)
    version: str = Field(min_length=1)


def build_router(*, paths: RuntimePaths, catalog_path: Path) -> APIRouter:
    catalog = AgentCatalog.from_file(catalog_path)
    catalog_ids = {agent.id for agent in catalog.agents}
    extensions = ExtensionStore(paths.extensions_lock)
    jobs = JobStore(paths.jobs)
    router = APIRouter(tags=["management"])

    @router.get("/api/agents")
    async def list_agents():
        return {"agents": [asdict(agent) for agent in catalog.agents]}

    @router.post("/api/agents/check", status_code=status.HTTP_202_ACCEPTED)
    async def check_agents():
        return _create_job(jobs, kind="agent-check", payload={"agents": sorted(catalog_ids)})

    @router.post("/api/agent-jobs", status_code=status.HTTP_202_ACCEPTED)
    async def create_agent_job(request: AgentJobRequest):
        unknown = sorted(set(request.agents) - catalog_ids)
        if unknown:
            raise HTTPException(status_code=422, detail=f"Unknown managed agents: {', '.join(unknown)}")
        return _create_job(jobs, kind=f"agent-{request.action}", payload={"agents": request.agents})

    @router.get("/api/agent-jobs/{job_id}")
    async def get_agent_job(job_id: str):
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job": asdict(job)}

    @router.get("/api/extensions")
    async def list_extensions():
        return {"extensions": [asdict(extension) for extension in extensions.list()]}

    @router.post("/api/extensions", status_code=status.HTTP_202_ACCEPTED)
    async def create_extension(request: ExtensionRequest):
        try:
            extension = extensions.add(source=request.source, name=request.name, version=request.version)
            job = jobs.create(
                kind="extension-install",
                payload={"source": extension.source, "name": extension.name, "version": extension.version},
            )
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except RuntimeError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        return {"extension": asdict(extension), "job": asdict(job)}

    return router


def _create_job(jobs: JobStore, *, kind: str, payload: dict) -> dict:
    try:
        job = jobs.create(kind=kind, payload=payload)
    except RuntimeError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"job": asdict(job)}
