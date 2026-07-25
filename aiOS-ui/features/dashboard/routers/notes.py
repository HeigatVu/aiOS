import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.paths import RuntimePaths

router = APIRouter(prefix="/api/notes", tags=["notes"])

# Path resolver
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
RUNTIME_PATHS = RuntimePaths.from_project_root(
    Path(os.environ.get("AIOS_PROJECT_ROOT", PROJECT_ROOT.parent))
)
if os.environ.get("NOTES_DIR_MOCK") == "1":
    NOTES_DIR = PROJECT_ROOT / "private-notes-test"
else:
    NOTES_DIR = Path(os.environ.get("AIOS_PRIVATE_NOTES", RUNTIME_PATHS.private_notes))

class NoteMeta(BaseModel):
    filename: str
    title: str
    category: str
    status: str
    tags: List[str]
    created_at: str
    updated_at: str

class NoteDetail(BaseModel):
    filename: str
    title: str
    category: str
    status: str
    tags: List[str]
    created_at: str
    updated_at: str
    content: str

class NoteCreateUpdate(BaseModel):
    title: str
    category: str
    status: str
    tags: List[str]
    content: str

def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s or "untitled"

def parse_markdown_file(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    
    stat = path.stat()
    created_iso = datetime.fromtimestamp(stat.st_ctime, timezone.utc).isoformat()
    updated_iso = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()

    if not m:
        return {
            "filename": path.name,
            "title": path.stem,
            "category": "General",
            "status": "Draft",
            "tags": [],
            "created_at": created_iso,
            "updated_at": updated_iso,
            "content": text
        }
        
    frontmatter_text, content = m.groups()
    meta = {}
    for line in frontmatter_text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    meta[k] = json.loads(v.replace("'", '"'))
                except Exception:
                    meta[k] = [x.strip().strip('"') for x in v[1:-1].split(",") if x.strip()]
            else:
                meta[k] = v.strip('"')

    meta.setdefault("title", path.stem)
    meta.setdefault("category", "General")
    meta.setdefault("status", "Draft")
    
    if "tags" in meta:
        if isinstance(meta["tags"], str):
            meta["tags"] = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    else:
        meta["tags"] = []

    meta.setdefault("created_at", created_iso)
    meta.setdefault("updated_at", updated_iso)
    meta["filename"] = path.name
    meta["content"] = content
    return meta

def write_markdown_file(path: Path, meta: Dict[str, Any], content: str):
    frontmatter = [
        "---",
        f'title: "{meta["title"]}"',
        f'category: "{meta["category"]}"',
        f'status: "{meta["status"]}"',
        f'tags: {json.dumps(meta["tags"])}',
        f'created_at: "{meta["created_at"]}"',
        f'updated_at: "{meta["updated_at"]}"',
        "---",
        content
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(frontmatter), encoding="utf-8")

@router.get("", response_model=List[NoteMeta])
async def list_notes():
    if not NOTES_DIR.exists():
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
    notes = []
    for file in NOTES_DIR.glob("*.md"):
        try:
            data = parse_markdown_file(file)
            notes.append(NoteMeta(
                filename=data["filename"],
                title=data["title"],
                category=data["category"],
                status=data["status"],
                tags=data["tags"],
                created_at=data["created_at"],
                updated_at=data["updated_at"]
            ))
        except Exception:
            pass
    return sorted(notes, key=lambda n: n.updated_at, reverse=True)

@router.get("/{filename}", response_model=NoteDetail)
async def get_note(filename: str):
    path = NOTES_DIR / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Note not found")
    data = parse_markdown_file(path)
    return NoteDetail(**data)

@router.post("", response_model=NoteMeta)
async def create_note(note: NoteCreateUpdate):
    slug = slugify(note.title)
    filename = f"{slug}.md"
    path = NOTES_DIR / filename
    
    # Ensure uniqueness
    counter = 1
    while path.exists():
        filename = f"{slug}-{counter}.md"
        path = NOTES_DIR / filename
        counter += 1

    now = datetime.now(timezone.utc).isoformat()
    meta = {
        "title": note.title,
        "category": note.category or "General",
        "status": note.status,
        "tags": note.tags,
        "created_at": now,
        "updated_at": now
    }
    write_markdown_file(path, meta, note.content)
    return NoteMeta(filename=filename, **meta)

@router.put("/{filename}", response_model=NoteMeta)
async def update_note(filename: str, note: NoteCreateUpdate):
    path = NOTES_DIR / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Note not found")

    old_data = parse_markdown_file(path)
    slug = slugify(note.title)
    new_filename = f"{slug}.md"
    new_path = NOTES_DIR / new_filename

    now = datetime.now(timezone.utc).isoformat()
    meta = {
        "title": note.title,
        "category": note.category or "General",
        "status": note.status,
        "tags": note.tags,
        "created_at": old_data["created_at"],
        "updated_at": now
    }

    if filename != new_filename:
        # Ensure new filename is unique if title changed
        counter = 1
        while new_path.exists() and new_path != path:
            new_filename = f"{slug}-{counter}.md"
            new_path = NOTES_DIR / new_filename
            counter += 1
        # Write new file and delete old
        write_markdown_file(new_path, meta, note.content)
        path.unlink()
        filename = new_filename
    else:
        write_markdown_file(path, meta, note.content)

    return NoteMeta(filename=filename, **meta)

@router.delete("/{filename}")
async def delete_note(filename: str):
    path = NOTES_DIR / filename
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="Note not found")
    path.unlink()
    return {"deleted": filename}
