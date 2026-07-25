from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI
import httpx

from routers.management import build_router
from services.paths import RuntimePaths


class ManagementApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = RuntimePaths.from_project_root(Path(self.temp_dir.name))
        catalog_path = Path(__file__).resolve().parents[3] / "config" / "agent-catalog.json"
        app = FastAPI()
        app.include_router(build_router(paths=self.paths, catalog_path=catalog_path))
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()
        self.temp_dir.cleanup()

    async def test_agents_endpoint_exposes_the_supported_catalog(self):
        response = await self.client.get("/api/agents")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {agent["id"] for agent in response.json()["agents"]},
            {"agentmemory", "codegraph", "codex", "hermes", "mimo", "reasonix"},
        )

    async def test_extension_endpoint_records_only_a_pinned_supported_package(self):
        response = await self.client.post(
            "/api/extensions",
            json={"source": "npm", "name": "@acme/runner", "version": "1.2.3"},
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json()["extension"], {"source": "npm", "name": "@acme/runner", "version": "1.2.3"})
        extensions = await self.client.get("/api/extensions")
        self.assertEqual(extensions.json()["extensions"], [response.json()["extension"]])

    async def test_agent_job_rejects_unknown_agents(self):
        response = await self.client.post(
            "/api/agent-jobs",
            json={"action": "update", "agents": ["unknown-agent"]},
        )

        self.assertEqual(response.status_code, 422)
