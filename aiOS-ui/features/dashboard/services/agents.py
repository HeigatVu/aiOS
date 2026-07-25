from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


_NPM_NAME = re.compile(r"^(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*$", re.IGNORECASE)
_PYPI_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*$", re.IGNORECASE)


@dataclass(frozen=True)
class AgentDefinition:
    id: str
    display_name: str
    source: str
    package: str
    version_command: list[str]
    update_command: list[str]


@dataclass(frozen=True)
class Extension:
    source: str
    name: str
    version: str


class AgentCatalog:
    def __init__(self, agents: list[AgentDefinition]) -> None:
        ids = [agent.id for agent in agents]
        if len(ids) != len(set(ids)):
            raise ValueError("Agent catalog contains duplicate ids")
        self.agents = agents

    @classmethod
    def from_file(cls, path: Path) -> "AgentCatalog":
        raw = json.loads(path.read_text(encoding="utf-8"))
        items = raw.get("agents")
        if not isinstance(items, list):
            raise ValueError("Agent catalog must contain an agents list")
        agents = []
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Agent catalog entries must be objects")
            required = {"id", "display_name", "source", "package", "version_command", "update_command"}
            if not required.issubset(item):
                raise ValueError("Agent catalog entry is incomplete")
            if not all(isinstance(item[key], str) and item[key] for key in required - {"version_command", "update_command"}):
                raise ValueError("Agent catalog string fields must be non-empty")
            if not all(isinstance(item[key], list) and all(isinstance(value, str) for value in item[key]) for key in ("version_command", "update_command")):
                raise ValueError("Agent catalog commands must be string arrays")
            agents.append(AgentDefinition(**item))
        return cls(agents)


class ExtensionStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(self) -> list[Extension]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        items = raw.get("extensions", [])
        if not isinstance(items, list):
            raise ValueError("Extension lockfile is invalid")
        extensions = [Extension(**item) for item in items]
        for extension in extensions:
            self._validate(extension.source, extension.name, extension.version)
        return sorted(extensions, key=lambda extension: (extension.source, extension.name))

    def add(self, *, source: str, name: str, version: str) -> Extension:
        self._validate(source, name, version)
        extension = Extension(source=source, name=name, version=version)
        current = [item for item in self.list() if (item.source, item.name) != (source, name)]
        current.append(extension)
        self._write(current)
        return extension

    def _write(self, extensions: list[Extension]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "extensions": [asdict(extension) for extension in sorted(extensions, key=lambda item: (item.source, item.name))],
        }
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        temp_path.replace(self.path)

    @staticmethod
    def _validate(source: str, name: str, version: str) -> None:
        if source not in {"npm", "pypi"}:
            raise ValueError("Only npm and pypi extensions are supported")
        if not isinstance(version, str) or not version.strip() or version.strip().lower() in {"latest", "*"}:
            raise ValueError("Extensions must use an exact version")
        valid_name = _NPM_NAME.fullmatch(name) if source == "npm" else _PYPI_NAME.fullmatch(name)
        if not valid_name:
            raise ValueError("Extension package name is invalid")
