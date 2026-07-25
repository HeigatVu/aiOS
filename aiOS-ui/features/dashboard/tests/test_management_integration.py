from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx
import main


class ManagementIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_dashboard_serves_the_react_control_application(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url="http://test") as client:
            response = await client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn('<div id="root"></div>', response.text)

    async def test_dashboard_application_registers_management_routes(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url="http://test") as client:
            response = await client.get("/api/agents")

        self.assertEqual(response.status_code, 200)
        self.assertIn("codex", {agent["id"] for agent in response.json()["agents"]})

    async def test_dashboard_application_registers_migration_routes(self):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url="http://test") as client:
            response = await client.get("/api/migrations/export/not-a-bundle")

        self.assertEqual(response.status_code, 422)
