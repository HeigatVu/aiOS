from __future__ import annotations

import hashlib
import io
import json
import tarfile
import time
from pathlib import Path


_EXCLUDED_PREFIXES = ("state/credentials/", "state/secrets/")


class MigrationService:
    def __init__(self, data_root: Path) -> None:
        self.data_root = data_root

    def export_bundle(self, destination: Path, *, include: list[str]) -> None:
        files = []
        for relative_root in include:
            root = self._safe_relative(relative_root)
            source = self.data_root / root
            if not source.exists():
                continue
            for path in sorted(item for item in source.rglob("*") if item.is_file()):
                relative = path.relative_to(self.data_root).as_posix()
                if relative.startswith(_EXCLUDED_PREFIXES):
                    continue
                content = path.read_bytes()
                files.append({"path": relative, "sha256": hashlib.sha256(content).hexdigest(), "size": len(content)})

        manifest = {"schema_version": 1, "created_at": time.time(), "files": files}
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(destination, "w:gz") as archive:
            manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
            manifest_info = tarfile.TarInfo("manifest.json")
            manifest_info.size = len(manifest_bytes)
            archive.addfile(manifest_info, io.BytesIO(manifest_bytes))
            for item in files:
                content = (self.data_root / item["path"]).read_bytes()
                info = tarfile.TarInfo(item["path"])
                info.size = len(content)
                archive.addfile(info, io.BytesIO(content))

    def restore_bundle(self, bundle: Path) -> None:
        with tarfile.open(bundle, "r:gz") as archive:
            manifest_file = archive.extractfile("manifest.json")
            if manifest_file is None:
                raise ValueError("Migration bundle has no manifest")
            manifest = json.load(manifest_file)
            if manifest.get("schema_version") != 1 or not isinstance(manifest.get("files"), list):
                raise ValueError("Migration bundle schema is not supported")
            verified = []
            for item in manifest["files"]:
                relative = self._safe_relative(item.get("path", ""))
                member = archive.getmember(relative.as_posix())
                source = archive.extractfile(member)
                if source is None:
                    raise ValueError(f"Migration bundle is missing {relative}")
                content = source.read()
                if len(content) != item.get("size") or hashlib.sha256(content).hexdigest() != item.get("sha256"):
                    raise ValueError(f"Migration bundle checksum failed for {relative}")
                verified.append((relative, content))

        for relative, content in verified:
            destination = self.data_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(destination.suffix + ".tmp")
            temporary.write_bytes(content)
            temporary.replace(destination)

    @staticmethod
    def _safe_relative(value: str) -> Path:
        path = Path(value)
        if not value or path.is_absolute() or ".." in path.parts:
            raise ValueError("Migration bundle contains an unsafe path")
        return path
