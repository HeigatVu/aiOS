from __future__ import annotations

import re
import time
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from services.migrations import MigrationService
from services.paths import RuntimePaths


_BUNDLE_NAME = re.compile(r"^aios-[0-9]{8}-[0-9]{6}\.tar\.gz$")


class ExportRequest(BaseModel):
    include: list[Literal["state", "private-notes", "workspace", "outputs"]] = Field(
        default_factory=lambda: ["state", "private-notes"]
    )


class RestoreRequest(BaseModel):
    bundle: str


def build_router(*, paths: RuntimePaths) -> APIRouter:
    router = APIRouter(tags=["migrations"])

    @router.post("/api/migrations/export", status_code=status.HTTP_201_CREATED)
    async def export_bundle(request: ExportRequest):
        bundle = f"aios-{time.strftime('%Y%m%d-%H%M%S')}.tar.gz"
        destination = paths.data / "exports" / bundle
        MigrationService(paths.data).export_bundle(destination, include=request.include)
        return {"bundle": bundle}

    @router.get("/api/migrations/export/{bundle}")
    async def download_bundle(bundle: str):
        path = _bundle_path(paths.data / "exports", bundle)
        if not path.is_file():
            raise HTTPException(status_code=404, detail="Migration bundle not found")
        return FileResponse(path, media_type="application/gzip", filename=path.name)

    @router.post("/api/migrations/restore", status_code=status.HTTP_204_NO_CONTENT)
    async def restore_bundle(request: RestoreRequest):
        path = _bundle_path(paths.data / "imports", request.bundle)
        if not path.is_file():
            raise HTTPException(status_code=404, detail="Staged migration bundle not found")
        try:
            MigrationService(paths.data).restore_bundle(path)
        except (OSError, ValueError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router


def _bundle_path(directory: Path, bundle: str) -> Path:
    if not _BUNDLE_NAME.fullmatch(bundle):
        raise HTTPException(status_code=422, detail="Migration bundle name is invalid")
    return directory / bundle
