#!/usr/bin/env python3
"""Host-side aiOS data initialization, migration, and bundle management."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT / "features" / "dashboard"))

from services.legacy import LegacyMigrator
from services.migrations import MigrationService
from services.paths import RuntimePaths


def get_paths(root: str | None) -> RuntimePaths:
    return RuntimePaths.from_project_root(Path(root).resolve() if root else APP_ROOT.parent)


def initialize(paths: RuntimePaths) -> None:
    paths.ensure_data_directories()
    for directory in (paths.data / "imports", paths.data / "exports", paths.data / "backups"):
        directory.mkdir(parents=True, exist_ok=True)
    if not paths.extensions_lock.exists():
        paths.extensions_lock.write_text(json.dumps({"schema_version": 1, "extensions": []}, indent=2) + "\n", encoding="utf-8")
    print(f"Initialized aiOS data directories in {paths.data}")


def migrate(paths: RuntimePaths, apply: bool) -> int:
    items = LegacyMigrator(paths).plan()
    if not items:
        print("No legacy aiOS data detected.")
        return 0
    for item in items:
        print(f"{item.source} -> {item.destination}")
    if not apply:
        print("Preview only. Re-run with --apply after reviewing these copies.")
        return 0
    backup = LegacyMigrator(paths).apply(items)
    print(f"Copied legacy data. Backup: {backup}")
    return 0


def export_bundle(paths: RuntimePaths, include: list[str]) -> None:
    destination = paths.data / "exports" / f"aios-{time.strftime('%Y%m%d-%H%M%S')}.tar.gz"
    MigrationService(paths.data).export_bundle(destination, include=include)
    print(destination)


def restore_bundle(paths: RuntimePaths, bundle: str) -> None:
    source = Path(bundle).expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"Bundle not found: {source}")
    staged = paths.data / "imports" / source.name
    staged.parent.mkdir(parents=True, exist_ok=True)
    if source != staged:
        shutil.copy2(source, staged)
    MigrationService(paths.data).restore_bundle(staged)
    print(f"Restored {staged}")


def doctor(paths: RuntimePaths) -> int:
    failures = []
    for command in ("docker",):
        if shutil.which(command) is None:
            failures.append(f"{command} is not installed or not in PATH")
    if not failures:
        result = subprocess.run(["docker", "compose", "version"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            failures.append("Docker Compose v2 is not available")
    for directory in (paths.workspace, paths.outputs, paths.data):
        if not directory.exists():
            failures.append(f"Missing data directory: {directory}")
    if failures:
        print("aiOS doctor found problems:", *failures, sep="\n- ")
        return 1
    print("aiOS doctor: Docker Compose and data directories are ready.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="Repository root containing aiOS-ui")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    migration = commands.add_parser("migrate")
    migration.add_argument("--apply", action="store_true")
    export = commands.add_parser("export")
    export.add_argument("--include", nargs="+", default=["state", "private-notes"])
    restore = commands.add_parser("restore")
    restore.add_argument("bundle")
    commands.add_parser("doctor")
    args = parser.parse_args()
    paths = get_paths(args.root)
    if args.command == "init":
        initialize(paths)
        return 0
    if args.command == "migrate":
        return migrate(paths, args.apply)
    if args.command == "export":
        export_bundle(paths, args.include)
        return 0
    if args.command == "restore":
        restore_bundle(paths, args.bundle)
        return 0
    return doctor(paths)


if __name__ == "__main__":
    raise SystemExit(main())
