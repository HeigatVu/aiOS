# Ideas & Notes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a host-secured, git-trackable Markdown Ideas & Notes Manager in the aiOS Control Center.

**Architecture:** A FastAPI notes router running on the host reading/writing to a host-only `private-notes/` directory, integrated as a new tab with category sidebar, search, and dynamic markdown rendering in the main dashboard page.

**Tech Stack:** Python 3 (FastAPI, Pydantic), Vanilla CSS, HTML5, Vanilla JavaScript.

---

### Task 1: Create Backend Router

**Files:**
- Create: `aiOS-ui/dashboard/routers/notes.py`
- Test: `aiOS-ui/dashboard/tests/test_notes.py`

- [ ] **Step 1: Write backend tests to verify endpoints**
  Create `aiOS-ui/dashboard/tests/test_notes.py` with tests for CRUD operations:
  ```python
  import pytest
  from pathlib import Path
  import shutil
  from fastapi.testclient import TestClient

  # Mock path setting
  import os
  os.environ["NOTES_DIR_MOCK"] = "1"

  from main import app

  client = TestClient(app)

  @pytest.fixture(autouse=True)
  def setup_teardown():
      # Setup clean test private-notes
      test_dir = Path("private-notes-test")
      if test_dir.exists():
          shutil.rmtree(test_dir)
      test_dir.mkdir(parents=True, exist_ok=True)
      yield
      if test_dir.exists():
          shutil.rmtree(test_dir)

  def test_notes_crud():
      # 1. Create a note
      payload = {
          "title": "Test YouTube Idea",
          "category": "YouTube",
          "status": "Draft",
          "tags": ["test", "video"],
          "content": "This is test content"
      }
      resp = client.post("/api/notes", json=payload)
      assert resp.status_code == 200
      data = resp.json()
      assert data["title"] == "Test YouTube Idea"
      assert data["filename"] == "test-youtube-idea.md"

      # 2. Get list of notes
      resp = client.get("/api/notes")
      assert resp.status_code == 200
      notes = resp.json()
      assert len(notes) == 1
      assert notes[0]["category"] == "YouTube"

      # 3. Get specific note
      resp = client.get("/api/notes/test-youtube-idea.md")
      assert resp.status_code == 200
      note = resp.json()
      assert note["content"] == "This is test content"

      # 4. Update note
      payload["status"] = "Active"
      payload["content"] = "Updated content"
      resp = client.put("/api/notes/test-youtube-idea.md", json=payload)
      assert resp.status_code == 200
      updated = resp.json()
      assert updated["status"] == "Active"

      # 5. Delete note
      resp = client.delete("/api/notes/test-youtube-idea.md")
      assert resp.status_code == 200
      resp = client.get("/api/notes")
      assert len(resp.json()) == 0
  ```

- [ ] **Step 2: Implement routers/notes.py**
  Create `aiOS-ui/dashboard/routers/notes.py`:
  ```python
  import os
  import re
  import json
  from pathlib import Path
  from datetime import datetime, timezone
  from typing import List, Dict, Any
  from fastapi import APIRouter, HTTPException
  from pydantic import BaseModel

  router = APIRouter(prefix="/api/notes", tags=["notes"])

  # Path resolver
  PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
  if os.environ.get("NOTES_DIR_MOCK") == "1":
      NOTES_DIR = PROJECT_ROOT / "private-notes-test"
  else:
      NOTES_DIR = PROJECT_ROOT / "private-notes"

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
  ```

- [ ] **Step 3: Register router in main.py**
  In `aiOS-ui/dashboard/main.py`, import and include the notes router:
  * Modify `aiOS-ui/dashboard/main.py`:
    ```python
    # Under: from routers import files, update, terminal
    from routers import files, update, terminal, notes

    # Under: app.include_router(terminal.router)
    app.include_router(notes.router)
    ```

- [ ] **Step 4: Commit**
  ```bash
  git add aiOS-ui/dashboard/routers/notes.py aiOS-ui/dashboard/main.py
  git commit -m "feat(backend): add private ideas and notes api endpoints"
  ```

---

### Task 2: Frontend HTML, CSS, and JS Integration

**Files:**
- Modify: `aiOS-ui/dashboard/static/dashboard/index.html`

- [ ] **Step 1: Add sidebar navigation link**
  Insert the navigation link inside `<aside class="sidebar">` below the File Explorer menu item:
  ```html
  <li>
    <a class="nav-item nav-ideas" data-tab="ideas" data-tooltip="Ideas & Notes">
      <span class="nav-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0012 18.75c-.305 0-.6.04-.88.114l-.548-.547z"/></svg>
      </span>
      <span class="nav-label">Ideas & Notes</span>
    </a>
  </li>
  ```

- [ ] **Step 2: Add theme CSS variables and styling for Viewport**
  Insert styles under the `<style>` block:
  ```css
  .nav-ideas { --theme-color: #ffd700; }

  /* Ideas split layout */
  .ideas-split-layout {
    display: flex;
    height: calc(100vh - 124px);
    margin: -30px;
    background: #07090e;
  }

  .ideas-list-pane {
    width: 340px;
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    background: rgba(11, 15, 23, 0.4);
    backdrop-filter: blur(10px);
  }

  .ideas-pane-header {
    padding: 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .search-wrap {
    display: flex;
    gap: 8px;
  }

  .search-input {
    flex-grow: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 12px;
    color: #fff;
    font-size: 14px;
    outline: none;
    transition: var(--transition);
  }

  .search-input:focus {
    border-color: #ffd700;
    box-shadow: 0 0 8px rgba(255, 215, 0, 0.2);
  }

  .btn-new-note {
    background: rgba(255, 215, 0, 0.1);
    color: #ffd700;
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: 8px;
    padding: 8px 14px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: var(--transition);
  }

  .btn-new-note:hover {
    background: rgba(255, 215, 0, 0.2);
    border-color: #ffd700;
  }

  .category-filter-list {
    display: flex;
    gap: 6px;
    overflow-x: auto;
    padding: 0 4px pb-2px;
    scrollbar-width: none;
  }

  .category-pill {
    padding: 4px 10px;
    border-radius: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    font-size: 11px;
    color: var(--text-muted);
    cursor: pointer;
    white-space: nowrap;
    transition: var(--transition);
  }

  .category-pill.active, .category-pill:hover {
    color: #fff;
    background: rgba(255, 215, 0, 0.1);
    border-color: #ffd700;
  }

  .notes-scroll-list {
    flex-grow: 1;
    overflow-y: auto;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .note-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    cursor: pointer;
    transition: var(--transition);
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .note-card:hover, .note-card.active {
    background: rgba(255, 215, 0, 0.03);
    border-color: rgba(255, 215, 0, 0.4);
  }

  .note-card-title {
    font-size: 14px;
    font-weight: 600;
    color: #fff;
  }

  .note-card-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-muted);
  }

  .note-badge-status {
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .status-draft { background: rgba(139, 148, 158, 0.15); color: var(--text-muted); }
  .status-active { background: rgba(46, 160, 67, 0.15); color: #58a6ff; }
  .status-archived { background: rgba(248, 81, 73, 0.15); color: #f85149; }

  .ideas-work-pane {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    padding: 30px;
    overflow-y: auto;
    position: relative;
  }

  .empty-note-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: var(--text-muted);
    gap: 12px;
  }

  .empty-note-state svg {
    width: 64px;
    height: 64px;
    stroke: var(--text-dark);
  }

  .note-view-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .note-view-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
  }

  .note-header-left {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .note-title-text {
    font-size: 26px;
    font-weight: 800;
    color: #fff;
  }

  .note-meta-row {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: var(--text-muted);
  }

  .note-actions {
    display: flex;
    gap: 8px;
  }

  .btn-action {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 12px;
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: var(--transition);
  }

  .btn-action:hover {
    color: #fff;
    background: rgba(255,255,255,0.08);
  }

  .btn-action.copy-btn {
    border-color: rgba(255, 215, 0, 0.4);
    color: #ffd700;
    background: rgba(255, 215, 0, 0.05);
  }
  .btn-action.copy-btn:hover {
    background: rgba(255, 215, 0, 0.1);
    box-shadow: 0 0 8px rgba(255, 215, 0, 0.2);
  }

  .note-tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .tag-badge {
    padding: 3px 8px;
    border-radius: 6px;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    font-size: 11px;
    color: var(--text-muted);
  }

  .note-body-content {
    background: rgba(20, 26, 38, 0.3);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    min-height: 300px;
    white-space: pre-wrap;
    font-family: 'Outfit', sans-serif;
    line-height: 1.6;
    color: #e6edf3;
  }

  /* Edit Form CSS */
  .edit-form-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .form-row {
    display: flex;
    gap: 16px;
  }

  .form-field {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-grow: 1;
  }

  .form-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
  }

  .form-input, .form-select, .form-textarea {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    color: #fff;
    font-size: 14px;
    outline: none;
    transition: var(--transition);
  }

  .form-input:focus, .form-select:focus, .form-textarea:focus {
    border-color: #ffd700;
    box-shadow: 0 0 8px rgba(255, 215, 0, 0.2);
  }

  .form-textarea {
    min-height: 400px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.5;
    resize: vertical;
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 10px;
  }
  
  /* Status pill dropdown selection hover styles */
  .status-interactive {
    cursor: pointer;
    position: relative;
  }
  .status-interactive:hover {
    filter: brightness(1.2);
    box-shadow: 0 0 6px rgba(255,255,255,0.1);
  }
  .status-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: #0f141c;
    border: 1px solid var(--border);
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    z-index: 50;
    display: none;
    flex-direction: column;
    padding: 4px;
    min-width: 100px;
  }
  .status-menu-item {
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    cursor: pointer;
    border-radius: 4px;
  }
  .status-menu-item:hover {
    background: rgba(255,255,255,0.05);
    color: #fff;
  }
  ```

- [ ] **Step 3: Add Viewport markup**
  Add the container inside `<main class="viewport-content">` below the update tab:
  ```html
  <!-- Tab 8: Ideas & Notes -->
  <div class="view-container" id="view-ideas">
    <div class="ideas-split-layout">
      <!-- Left sidebar pane -->
      <aside class="ideas-list-pane">
        <div class="ideas-pane-header">
          <div class="search-wrap">
            <input type="text" class="search-input" id="search-notes" placeholder="Search ideas & prompts..." oninput="filterNotes()">
            <button class="btn-new-note" onclick="initNewNote()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M12 5v14M5 12h14"/></svg>
              New
            </button>
          </div>
          <!-- Category filters -->
          <div class="category-filter-list" id="category-filter-list">
            <!-- Rendered dynamically -->
          </div>
        </div>
        
        <!-- Notes scroll area -->
        <div class="notes-scroll-list" id="notes-scroll-list">
          <!-- Rendered dynamically -->
        </div>
      </aside>

      <!-- Right detail/edit pane -->
      <section class="ideas-work-pane" id="ideas-work-pane">
        <div class="empty-note-state" id="empty-note-state">
          <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0012 18.75c-.305 0-.6.04-.88.114l-.548-.547z"/></svg>
          <h3>Private Ideas & Prompts</h3>
          <p>Store your draft prompts and secure thoughts outside the sandbox.</p>
        </div>

        <!-- Detail Viewer -->
        <div class="note-view-container" id="note-view-container" style="display: none;">
          <div class="note-view-header">
            <div class="note-header-left">
              <h2 class="note-title-text" id="view-note-title">Note Title</h2>
              <div class="note-meta-row">
                <span class="note-category-label">Category: <strong id="view-note-category" style="color: #ffd700;">General</strong></span>
                <span>•</span>
                <span class="status-interactive" style="position: relative;" onclick="toggleStatusMenu(event)">
                  <span class="note-badge-status" id="view-note-status">Draft</span>
                  <div class="status-menu" id="status-change-menu">
                    <div class="status-menu-item" onclick="changeNoteStatusDirectly('Draft')">Draft</div>
                    <div class="status-menu-item" onclick="changeNoteStatusDirectly('Active')">Active</div>
                    <div class="status-menu-item" onclick="changeNoteStatusDirectly('Archived')">Archived</div>
                  </div>
                </span>
                <span>•</span>
                <span id="view-note-updated">Updated just now</span>
              </div>
            </div>
            <div class="note-actions">
              <button class="btn-action copy-btn" onclick="copyNoteContent()">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
                Copy Prompt
              </button>
              <button class="btn-action" onclick="editCurrentNote()">Edit</button>
              <button class="btn-action" style="color: #f85149;" onclick="deleteCurrentNote()">Delete</button>
            </div>
          </div>
          
          <div class="note-tag-row" id="view-note-tags">
            <!-- Rendered dynamically -->
          </div>

          <div class="note-body-content" id="view-note-body">
            <!-- Content -->
          </div>
        </div>

        <!-- Edit Form -->
        <div class="edit-form-container" id="note-edit-container" style="display: none;">
          <div class="form-row">
            <div class="form-field" style="flex: 2;">
              <label class="form-label">Title</label>
              <input type="text" class="form-input" id="edit-note-title" placeholder="E.g. Code Review Prompt">
            </div>
            <div class="form-field">
              <label class="form-label">Category</label>
              <input type="text" class="form-input" id="edit-note-category" placeholder="E.g. aiOS, YouTube" list="category-options-list">
              <datalist id="category-options-list">
                <!-- Autocomplete list of categories -->
              </datalist>
            </div>
            <div class="form-field">
              <label class="form-label">Status</label>
              <select class="form-select" id="edit-note-status">
                <option value="Draft">Draft</option>
                <option value="Active">Active</option>
                <option value="Archived">Archived</option>
              </select>
            </div>
          </div>
          <div class="form-field">
            <label class="form-label">Tags (comma-separated)</label>
            <input type="text" class="form-input" id="edit-note-tags" placeholder="E.g. templates, python, short">
          </div>
          <div class="form-field">
            <label class="form-label">Content (Markdown supported)</label>
            <textarea class="form-textarea" id="edit-note-body" placeholder="Write your idea or prompt here..."></textarea>
          </div>
          <div class="form-actions">
            <button class="btn-action" onclick="cancelEditing()">Cancel</button>
            <button class="btn-action" style="background: var(--accent); color: #fff; border-color: transparent;" onclick="saveNote()">Save Note</button>
          </div>
        </div>
      </section>
    </div>
  </div>
  ```

- [ ] **Step 4: Implement JavaScript application controller**
  Add state and operations to the `<script>` tag:
  ```javascript
  // ── Ideas & Notes controller ──
  var allNotes = [];
  var selectedNote = null;
  var selectedCategory = 'All';
  var isEditing = false;
  var isNew = false;

  async function loadNotes() {
    try {
      var r = await fetch('/api/notes');
      allNotes = await r.json();
      renderCategories();
      renderNotesList();
    } catch(e) {
      console.error("Failed to load notes", e);
    }
  }

  function getUniqueCategories() {
    var cats = {'All': 0};
    allNotes.forEach(function(n) {
      var c = n.category || 'General';
      cats[c] = (cats[c] || 0) + 1;
      cats['All']++;
    });
    return cats;
  }

  function renderCategories() {
    var list = document.getElementById('category-filter-list');
    var datalist = document.getElementById('category-options-list');
    if (!list) return;

    var cats = getUniqueCategories();
    
    // Render horizontal pills
    var html = '';
    for (var name in cats) {
      var count = cats[name];
      var activeClass = name === selectedCategory ? 'active' : '';
      html += '<span class="category-pill ' + activeClass + '" onclick="selectCategory(\'' + name + '\')">' + name + ' (' + count + ')</span>';
    }
    list.innerHTML = html;

    // Render datalist autocomplete options
    if (datalist) {
      var optionsHtml = '';
      for (var name in cats) {
        if (name !== 'All') {
          optionsHtml += '<option value="' + name + '">';
        }
      }
      datalist.innerHTML = optionsHtml;
    }
  }

  function selectCategory(cat) {
    selectedCategory = cat;
    renderCategories();
    renderNotesList();
  }

  function renderNotesList() {
    var container = document.getElementById('notes-scroll-list');
    if (!container) return;

    var query = (document.getElementById('search-notes').value || '').toLowerCase();
    
    var filtered = allNotes.filter(function(n) {
      // Filter by category
      if (selectedCategory !== 'All') {
        var cat = n.category || 'General';
        if (cat !== selectedCategory) return false;
      }
      // Filter by search query
      if (query) {
        var inTitle = n.title.toLowerCase().indexOf(query) !== -1;
        var inTags = n.tags.some(function(t) { return t.toLowerCase().indexOf(query) !== -1; });
        var inCat = (n.category || '').toLowerCase().indexOf(query) !== -1;
        return inTitle || inTags || inCat;
      }
      return true;
    });

    if (filtered.length === 0) {
      container.innerHTML = '<div style="text-align:center; padding: 40px 10px; color: var(--text-dark); font-size:13px;">No entries found.</div>';
      return;
    }

    var html = '';
    filtered.forEach(function(n) {
      var activeClass = (selectedNote && selectedNote.filename === n.filename) ? 'active' : '';
      var statusClass = 'status-' + n.status.toLowerCase();
      var dateStr = new Date(n.updated_at).toLocaleString();
      var tagsHtml = n.tags.map(function(t) { return '<span class="tag-badge" style="padding: 1px 4px; font-size: 9px; margin-right: 4px;">' + t + '</span>'; }).join('');
      
      html += '<div class="note-card ' + activeClass + '" onclick="selectNote(\'' + n.filename + '\')">';
      html += '  <div class="note-card-title">' + n.title + '</div>';
      html += '  <div style="font-size: 11px; color: #ffd700;">' + (n.category || 'General') + '</div>';
      html += '  <div class="note-card-meta">';
      html += '    <span class="note-badge-status ' + statusClass + '">' + n.status + '</span>';
      html += '    <span>' + dateStr.split(',')[0] + '</span>';
      html += '  </div>';
      html += '  <div style="margin-top: 4px;">' + tagsHtml + '</div>';
      html += '</div>';
    });
    container.innerHTML = html;
  }

  async function selectNote(filename) {
    try {
      isEditing = false;
      isNew = false;
      var r = await fetch('/api/notes/' + filename);
      selectedNote = await r.json();
      
      // Update UI panels
      document.getElementById('empty-note-state').style.display = 'none';
      document.getElementById('note-edit-container').style.display = 'none';
      document.getElementById('note-view-container').style.display = 'flex';

      document.getElementById('view-note-title').textContent = selectedNote.title;
      document.getElementById('view-note-category').textContent = selectedNote.category || 'General';
      document.getElementById('view-note-updated').textContent = 'Updated ' + new Date(selectedNote.updated_at).toLocaleString();
      
      var statusBadge = document.getElementById('view-note-status');
      statusBadge.textContent = selectedNote.status;
      statusBadge.className = 'note-badge-status status-' + selectedNote.status.toLowerCase();

      var tagsContainer = document.getElementById('view-note-tags');
      tagsContainer.innerHTML = selectedNote.tags.map(function(t) {
        return '<span class="tag-badge">' + t + '</span>';
      }).join('');

      // Render markdown body (or text if no markdown library, we preserve pre-wrap spacing)
      document.getElementById('view-note-body').textContent = selectedNote.content;

      renderNotesList();
    } catch(e) {
      console.error("Failed to select note", e);
    }
  }

  function filterNotes() {
    renderNotesList();
  }

  function initNewNote() {
    isEditing = true;
    isNew = true;
    selectedNote = null;

    document.getElementById('empty-note-state').style.display = 'none';
    document.getElementById('note-view-container').style.display = 'none';
    document.getElementById('note-edit-container').style.display = 'flex';

    document.getElementById('edit-note-title').value = '';
    document.getElementById('edit-note-category').value = '';
    document.getElementById('edit-note-status').value = 'Draft';
    document.getElementById('edit-note-tags').value = '';
    document.getElementById('edit-note-body').value = '';

    renderNotesList();
  }

  function editCurrentNote() {
    if (!selectedNote) return;
    isEditing = true;
    isNew = false;

    document.getElementById('note-view-container').style.display = 'none';
    document.getElementById('note-edit-container').style.display = 'flex';

    document.getElementById('edit-note-title').value = selectedNote.title;
    document.getElementById('edit-note-category').value = selectedNote.category || 'General';
    document.getElementById('edit-note-status').value = selectedNote.status;
    document.getElementById('edit-note-tags').value = selectedNote.tags.join(', ');
    document.getElementById('edit-note-body').value = selectedNote.content;
  }

  function cancelEditing() {
    isEditing = false;
    if (isNew || !selectedNote) {
      document.getElementById('note-edit-container').style.display = 'none';
      document.getElementById('empty-note-state').style.display = 'flex';
    } else {
      selectNote(selectedNote.filename);
    }
  }

  async function saveNote() {
    var title = document.getElementById('edit-note-title').value.trim();
    if (!title) {
      alert("Note Title is required.");
      return;
    }
    var category = document.getElementById('edit-note-category').value.trim();
    var status = document.getElementById('edit-note-status').value;
    var tagsRaw = document.getElementById('edit-note-tags').value;
    var tags = tagsRaw.split(',').map(function(t) { return t.trim(); }).filter(function(t) { return t; });
    var content = document.getElementById('edit-note-body').value;

    var payload = {
      title: title,
      category: category || 'General',
      status: status,
      tags: tags,
      content: content
    };

    try {
      var url = '/api/notes';
      var method = 'POST';
      if (!isNew && selectedNote) {
        url = '/api/notes/' + selectedNote.filename;
        method = 'PUT';
      }

      var resp = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!resp.ok) throw new Error("Save request failed");
      var savedMeta = await resp.json();
      
      await loadNotes();
      selectNote(savedMeta.filename);
    } catch(e) {
      alert("Error saving note: " + e.message);
    }
  }

  async function deleteCurrentNote() {
    if (!selectedNote) return;
    if (!confirm("Are you sure you want to permanently delete this note?")) return;

    try {
      var resp = await fetch('/api/notes/' + selectedNote.filename, { method: 'DELETE' });
      if (!resp.ok) throw new Error("Delete failed");

      selectedNote = null;
      document.getElementById('note-view-container').style.display = 'none';
      document.getElementById('empty-note-state').style.display = 'flex';
      
      await loadNotes();
    } catch(e) {
      alert("Error deleting note: " + e.message);
    }
  }

  function copyNoteContent() {
    if (!selectedNote) return;
    navigator.clipboard.writeText(selectedNote.content).then(function() {
      // Flash copy button to indicate success
      var btn = document.querySelector('.copy-btn');
      var origText = btn.innerHTML;
      btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg> Copied!';
      btn.style.color = '#3fb950';
      btn.style.borderColor = 'rgba(63, 185, 80, 0.4)';
      btn.style.background = 'rgba(63, 185, 80, 0.05)';
      setTimeout(function() {
        btn.innerHTML = origText;
        btn.style.color = '';
        btn.style.borderColor = '';
        btn.style.background = '';
      }, 1500);
    }).catch(function(e) {
      alert("Failed to copy note content: " + e);
    });
  }

  function toggleStatusMenu(event) {
    event.stopPropagation();
    var menu = document.getElementById('status-change-menu');
    if (menu.style.display === 'flex') {
      menu.style.display = 'none';
    } else {
      menu.style.display = 'flex';
    }
  }

  // Close status menu when clicking outside
  document.addEventListener('click', function() {
    var menu = document.getElementById('status-change-menu');
    if (menu) menu.style.display = 'none';
  });

  async function changeNoteStatusDirectly(newStatus) {
    if (!selectedNote) return;
    
    var payload = {
      title: selectedNote.title,
      category: selectedNote.category || 'General',
      status: newStatus,
      tags: selectedNote.tags,
      content: selectedNote.content
    };

    try {
      var resp = await fetch('/api/notes/' + selectedNote.filename, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!resp.ok) throw new Error("Status update failed");
      var savedMeta = await resp.json();
      
      await loadNotes();
      selectNote(savedMeta.filename);
    } catch(e) {
      alert("Failed to update status: " + e.message);
    }
  }

  // Trigger loading when switching tab
  var origSwitchTab = switchTab;
  switchTab = function(tabId) {
    origSwitchTab(tabId);
    if (tabId === 'ideas') {
      loadNotes();
    }
  };
  ```

- [ ] **Step 5: Register view title map**
  In the switchTab function map inside `index.html`:
  * Add the title mapping `ideas: 'Ideas & Notes'` to the `titleMap` dictionary:
    ```javascript
    var titleMap = {
      overview: 'Control Center',
      hermes: 'Hermes Chat',
      metrics: 'Hermes Dashboard',
      memory: 'Agent Memory',
      files: 'File Explorer',
      terminal: 'Shell Terminal',
      update: 'System Update',
      ideas: 'Ideas & Notes'
    };
    ```

- [ ] **Step 6: Commit**
  ```bash
  git add aiOS-ui/dashboard/static/dashboard/index.html
  git commit -m "feat(frontend): integrate ideas and notes panel UI and JS controller"
  ```
