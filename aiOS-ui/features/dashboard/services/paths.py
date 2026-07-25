from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RuntimePaths:
    project_root: Path
    app: Path
    workspace: Path
    outputs: Path
    data: Path
    state: Path
    private_notes: Path
    extensions_lock: Path
    jobs: Path

    @classmethod
    def from_project_root(cls, project_root: Path) -> "RuntimePaths":
        root = project_root.resolve()
        data = root / "sandbox-data"
        state = data / "state"
        return cls(
            project_root=root,
            app=root / "aiOS-ui",
            workspace=root / "working-space",
            outputs=root / "outputs",
            data=data,
            state=state,
            private_notes=data / "private-notes",
            extensions_lock=state / "extensions.lock.json",
            jobs=state / "jobs.json",
        )

    def ensure_data_directories(self) -> None:
        for directory in (self.workspace, self.outputs, self.data, self.state, self.private_notes):
            directory.mkdir(parents=True, exist_ok=True)
