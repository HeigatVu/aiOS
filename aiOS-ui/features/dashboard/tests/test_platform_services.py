from __future__ import annotations

import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.agents import AgentCatalog, ExtensionStore
from services.execution import AgentJobExecutor, CommandResult
from services.jobs import JobStore
from services.legacy import LegacyMigrator
from services.migrations import MigrationService
from services.paths import RuntimePaths
from services.worker import run_once


class RuntimePathsTests(unittest.TestCase):
    def test_project_layout_uses_root_level_workspace_outputs_and_sandbox_data(self):
        root = Path("/tmp/aios-project")

        paths = RuntimePaths.from_project_root(root)

        self.assertEqual(paths.app, root / "aiOS-ui")
        self.assertEqual(paths.workspace, root / "working-space")
        self.assertEqual(paths.outputs, root / "outputs")
        self.assertEqual(paths.data, root / "sandbox-data")
        self.assertEqual(paths.state, root / "sandbox-data" / "state")
        self.assertEqual(paths.private_notes, root / "sandbox-data" / "private-notes")


class AgentCatalogTests(unittest.TestCase):
    def test_catalog_loads_the_supported_core_agents(self):
        catalog = AgentCatalog.from_file(
            Path(__file__).resolve().parents[3] / "config" / "agent-catalog.json"
        )

        self.assertEqual(
            {agent.id for agent in catalog.agents},
            {"agentmemory", "codegraph", "codex", "hermes", "mimo", "reasonix"},
        )

    def test_extension_store_accepts_pinned_npm_and_pypi_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = ExtensionStore(Path(tmp) / "extensions.lock.json")

            npm = store.add(source="npm", name="@acme/runner", version="1.2.3")
            pypi = store.add(source="pypi", name="tool-runner", version="4.5.6")

            self.assertEqual(npm.source, "npm")
            self.assertEqual(pypi.source, "pypi")
            self.assertEqual(
                [(tool.source, tool.name, tool.version) for tool in store.list()],
                [("npm", "@acme/runner", "1.2.3"), ("pypi", "tool-runner", "4.5.6")],
            )

    def test_extension_store_rejects_unpinned_or_unsupported_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = ExtensionStore(Path(tmp) / "extensions.lock.json")

            with self.assertRaises(ValueError):
                store.add(source="npm", name="runner", version="latest")
            with self.assertRaises(ValueError):
                store.add(source="shell", name="curl example.com | sh", version="1.0.0")


class JobStoreTests(unittest.TestCase):
    def test_only_one_active_mutating_job_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = JobStore(Path(tmp) / "jobs.json")
            first = store.create(kind="agent-update", payload={"agents": ["codex"]})

            with self.assertRaises(RuntimeError):
                store.create(kind="extension-install", payload={"name": "tool"})

            store.finish(first.id, status="succeeded")
            second = store.create(kind="extension-install", payload={"name": "tool"})

            self.assertEqual(second.status, "queued")

    def test_executor_runs_catalog_commands_and_records_the_result(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = AgentCatalog.from_file(
                Path(__file__).resolve().parents[3] / "config" / "agent-catalog.json"
            )
            store = JobStore(root / "jobs.json")
            job = store.create(kind="agent-check", payload={"agents": ["codex"]})
            commands = []

            def run(command: list[str]) -> CommandResult:
                commands.append(command)
                return CommandResult(returncode=0, output="codex 1.2.3")

            completed = AgentJobExecutor(catalog=catalog, store=store, command_runner=run).run_next()

            self.assertEqual(commands, [["codex", "--version"]])
            self.assertEqual(completed.id, job.id)
            self.assertEqual(completed.status, "succeeded")
            self.assertIn("codex 1.2.3", completed.logs)

    def test_executor_installs_pinned_extensions_without_shell_interpolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = AgentCatalog.from_file(
                Path(__file__).resolve().parents[3] / "config" / "agent-catalog.json"
            )
            store = JobStore(root / "jobs.json")
            store.create(
                kind="extension-install",
                payload={"source": "pypi", "name": "tool-runner", "version": "4.5.6"},
            )
            commands = []

            def run(command: list[str]) -> CommandResult:
                commands.append(command)
                return CommandResult(returncode=0, output="installed")

            AgentJobExecutor(catalog=catalog, store=store, command_runner=run).run_next()

            self.assertEqual(commands, [["uv", "tool", "install", "tool-runner==4.5.6"]])

    def test_worker_claims_and_processes_the_next_job_from_runtime_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = RuntimePaths.from_project_root(root)
            store = JobStore(paths.jobs)
            store.create(kind="agent-check", payload={"agents": ["codex"]})
            commands = []

            result = run_once(
                paths=paths,
                catalog_path=Path(__file__).resolve().parents[3] / "config" / "agent-catalog.json",
                command_runner=lambda command: commands.append(command) or CommandResult(0, "ok"),
            )

            self.assertEqual(result.status, "succeeded")
            self.assertEqual(commands, [["codex", "--version"]])

    def test_worker_replays_a_pinned_extension_from_restored_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = RuntimePaths.from_project_root(Path(tmp))
            ExtensionStore(paths.extensions_lock).add(source="npm", name="tool-runner", version="1.0.0")
            commands = []

            result = run_once(
                paths=paths,
                catalog_path=Path(__file__).resolve().parents[3] / "config" / "agent-catalog.json",
                command_runner=lambda command: commands.append(command) or CommandResult(0, "installed"),
            )

            self.assertEqual(result.status, "succeeded")
            self.assertEqual(commands, [["npm", "install", "--global", "tool-runner@1.0.0"]])


class MigrationServiceTests(unittest.TestCase):
    def test_export_and_restore_verify_files_and_exclude_credentials(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            (source / "state" / "credentials").mkdir(parents=True)
            (source / "state" / "settings.json").write_text('{"theme":"dark"}', encoding="utf-8")
            (source / "state" / "credentials" / "token.txt").write_text("secret", encoding="utf-8")
            (source / "private-notes").mkdir()
            (source / "private-notes" / "idea.md").write_text("private", encoding="utf-8")

            bundle = root / "backup.tar.gz"
            service = MigrationService(source)
            service.export_bundle(bundle, include=["state", "private-notes"])

            with tarfile.open(bundle, "r:gz") as archive:
                manifest = json.load(archive.extractfile("manifest.json"))
            self.assertEqual(manifest["schema_version"], 1)
            self.assertNotIn("state/credentials/token.txt", {item["path"] for item in manifest["files"]})

            destination = root / "restored"
            MigrationService(destination).restore_bundle(bundle)

            self.assertEqual((destination / "state" / "settings.json").read_text(encoding="utf-8"), '{"theme":"dark"}')
            self.assertFalse((destination / "state" / "credentials" / "token.txt").exists())


class LegacyMigrationTests(unittest.TestCase):
    def test_legacy_migration_previews_and_copies_state_without_deleting_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = RuntimePaths.from_project_root(Path(tmp))
            legacy_state = paths.app / "persistent" / "hermes"
            legacy_state.mkdir(parents=True)
            (legacy_state / "config.json").write_text("{}", encoding="utf-8")

            migrator = LegacyMigrator(paths)
            plan = migrator.plan()
            migrator.apply(plan)

            self.assertEqual(len(plan), 1)
            self.assertTrue((paths.state / "hermes" / "config.json").is_file())
            self.assertTrue((legacy_state / "config.json").is_file())
