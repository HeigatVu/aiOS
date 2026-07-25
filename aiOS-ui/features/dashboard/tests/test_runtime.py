from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.paths import RuntimePaths
from main import agentmemory_proxy_headers
from services.runtime import agentmemory_environment, build_runtime_environment, codegraph_index_command, ensure_agentmemory_secret


class RuntimeSupervisorTests(unittest.TestCase):
    def test_runtime_provisions_a_private_agentmemory_viewer_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = RuntimePaths.from_project_root(Path(tmp))

            secret = ensure_agentmemory_secret(paths)
            secret_file = paths.state / "credentials" / "agentmemory-viewer-secret"

            self.assertEqual(secret_file.read_text(encoding="utf-8").strip(), secret)
            self.assertEqual(ensure_agentmemory_secret(paths), secret)
            environment = build_runtime_environment(paths, {"PATH": "/usr/bin"})
            self.assertEqual(environment["AGENTMEMORY_VIEWER_HOST"], "0.0.0.0")
            self.assertEqual(environment["AGENTMEMORY_SECRET"], secret)
            self.assertEqual(environment["VIEWER_ALLOWED_HOSTS"], "localhost:3113")

    def test_runtime_uses_persistent_state_and_a_shared_workspace_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = RuntimePaths.from_project_root(Path(tmp))
            paths.workspace.mkdir(parents=True)

            environment = build_runtime_environment(paths, {"PATH": "/usr/bin", "HOME": "/root"})

            self.assertEqual(environment["AGENTMEMORY_HOME"], str(paths.state / "agentmemory"))
            self.assertEqual(environment["HOME"], "/root")
            self.assertEqual(environment["CODEGRAPH_PROJECT"], str(paths.workspace))
            self.assertEqual(
                codegraph_index_command(paths.workspace),
                ["codegraph", "init", str(paths.workspace)],
            )

            index = paths.workspace / ".codegraph"
            index.mkdir()
            (index / "codegraph.db").touch()

            self.assertEqual(
                codegraph_index_command(paths.workspace),
                ["codegraph", "sync", str(paths.workspace)],
            )

    def test_agentmemory_uses_its_persistent_state_directory_as_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = RuntimePaths.from_project_root(Path(tmp))

            environment = agentmemory_environment(paths, {"HOME": "/root"})

            self.assertEqual(environment["HOME"], str(paths.state / "agentmemory"))

    def test_control_proxy_header_uses_the_runtime_secret(self):
        with tempfile.TemporaryDirectory() as tmp:
            secret_file = Path(tmp) / "agentmemory-viewer-secret"
            secret_file.write_text("test-secret\n", encoding="utf-8")

            self.assertEqual(
                agentmemory_proxy_headers(secret_file),
                {"authorization": "Bearer test-secret"},
            )
