from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx
from fastapi import FastAPI

from routers.migrations import build_router
from services.paths import RuntimePaths


class MigrationsApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = RuntimePaths.from_project_root(Path(self.temp_dir.name))
        self.paths.state.mkdir(parents=True)
        (self.paths.state / "settings.json").write_text('{"theme":"dark"}', encoding="utf-8")
        app = FastAPI()
        app.include_router(build_router(paths=self.paths))
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()
        self.temp_dir.cleanup()

    async def test_export_and_restore_use_only_managed_bundle_locations(self):
        exported = await self.client.post("/api/migrations/export", json={"include": ["state"]})

        self.assertEqual(exported.status_code, 201)
        bundle = exported.json()["bundle"]
        self.assertTrue((self.paths.data / "exports" / bundle).is_file())

        (self.paths.state / "settings.json").unlink()
        imported = self.paths.data / "imports"
        imported.mkdir()
        (imported / bundle).write_bytes((self.paths.data / "exports" / bundle).read_bytes())
        restored = await self.client.post("/api/migrations/restore", json={"bundle": bundle})

        self.assertEqual(restored.status_code, 204)
        self.assertEqual((self.paths.state / "settings.json").read_text(encoding="utf-8"), '{"theme":"dark"}')

