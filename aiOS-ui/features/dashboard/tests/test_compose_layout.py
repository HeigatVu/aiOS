from __future__ import annotations

import unittest
from pathlib import Path


class ComposeLayoutTests(unittest.TestCase):
    def test_compose_defines_the_local_only_service_stack(self):
        compose = (Path(__file__).resolve().parents[3] / "docker-compose.yml").read_text(encoding="utf-8")

        for service in ("control:", "agent-runtime:", "hermes-webui:"):
            self.assertIn(service, compose)
        self.assertIn('"127.0.0.1:${AIOS_PORT:-9119}:9119"', compose)
        self.assertIn("AGENTMEMORY_BASE_URL: http://agent-runtime:3113", compose)
        for mount in (
            "../working-space:/aios/working-space:rw",
            "../outputs:/aios/outputs:rw",
            "../sandbox-data/my-data:/aios/sandbox-data/my-data:ro",
        ):
            self.assertIn(mount, compose)
        self.assertIn("headers={'Host': 'localhost:3113'}", compose)
        self.assertIn("healthcheck:", compose)
        self.assertNotIn("container_name:", compose)
        self.assertNotIn(".:/aiOS-ui", compose)
        self.assertNotIn("\n  agentmemory:\n", compose)
