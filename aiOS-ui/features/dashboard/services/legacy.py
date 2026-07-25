from __future__ import annotations

import shutil
import time
from dataclasses import dataclass
from pathlib import Path

from services.paths import RuntimePaths


@dataclass(frozen=True)
class LegacyMigrationItem:
    source: Path
    destination: Path


class LegacyMigrator:
    def __init__(self, paths: RuntimePaths) -> None:
        self.paths = paths

    def plan(self) -> list[LegacyMigrationItem]:
        candidates = [
            (self.paths.app / "persistent", self.paths.state),
            (self.paths.app / "private-notes", self.paths.private_notes),
            (self.paths.app / "config-file" / "aios-permissions.json", self.paths.state / "aios-permissions.json"),
            (self.paths.data / "working-space", self.paths.workspace),
            (self.paths.data / "outputs", self.paths.outputs),
        ]
        return [
            LegacyMigrationItem(source=source, destination=destination)
            for source, destination in candidates
            if source.exists() and (source.is_file() or any(source.iterdir()))
        ]

    def apply(self, items: list[LegacyMigrationItem]) -> Path | None:
        if not items:
            return None
        backup_root = self.paths.data / "backups" / f"legacy-{time.strftime('%Y%m%d-%H%M%S')}"
        for item in items:
            relative_name = item.source.name
            backup = backup_root / relative_name
            if item.source.is_dir():
                shutil.copytree(item.source, backup, dirs_exist_ok=True)
                shutil.copytree(item.source, item.destination, dirs_exist_ok=True)
            else:
                backup.parent.mkdir(parents=True, exist_ok=True)
                item.destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item.source, backup)
                shutil.copy2(item.source, item.destination)
        return backup_root
