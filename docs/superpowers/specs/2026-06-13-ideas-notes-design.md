# Design Spec: Private Ideas, Prompts, & Notes Manager (2026-06-13)

A host-secured, git-trackable markdown note-taking and prompt-management system integrated into the aiOS Control Center.

## Goals

1. **Security Isolation:** Save ideas, notes, and draft prompts in a host directory (`private-notes/`) that is **not** volume-mounted in `docker-compose.yml`, ensuring the sandbox AI cannot access or scan them.
2. **Git Integration:** Store entries as individual `.md` files with human-readable frontmatter, making them easy to commit, review, and track in git.
3. **Rich Organization:** Categorize notes (e.g., `YouTube`, `aiOS`, `Coding`), add tags, and track statuses (`Draft`, `Active`, `Archived`).
4. **Convenient UI:** Split-pane interface in the dashboard for searching, filtering, reading/writing markdown, and copying prompts to the clipboard.

## Data Model & Storage

Notes are saved as individual Markdown (`.md`) files on the host machine inside `private-notes/` at the project root.

### File Structure Example

```markdown
---
title: "Video outline about aiOS architectures"
category: "YouTube"
status: "Draft"
tags: ["aios", "video", "outline"]
created_at: "2026-06-13T10:01:00+07:00"
updated_at: "2026-06-13T10:01:00+07:00"
---
# Main Structure
1. Introduction to the Sidecar Pattern in aiOS.
2. Explaining why we isolate the GPU container.
3. Live demo of BFF proxying.
```

* **Filenames:** Generated automatically from the title slug (e.g., `video-outline-about-aios-architectures.md`). If a note is renamed, the file is moved/renamed.
* **Allowed Status values:** `Draft`, `Active`, `Archived`.
* **Allowed Category values:** Arbitrary string typed by user or selected from existing ones.

## API Endpoints (BFF Backend)

A new FastAPI router in `aiOS-ui/dashboard/routers/notes.py` will expose endpoints under `/api/notes`:

1. **`GET /api/notes`**:
   * Scans `private-notes/` for `.md` files.
   * Parses frontmatter.
   * Returns list of notes: `[ { filename, title, category, status, tags, created_at, updated_at }, ... ]`.
2. **`GET /api/notes/{filename}`**:
   * Reads target file.
   * Returns complete JSON: `{ filename, title, category, status, tags, created_at, updated_at, content }`.
3. **`POST /api/notes`**:
   * Receives `{ title, category, status, tags, content }`.
   * Generates a unique filename using a slugified title.
   * Writes the frontmatter and content.
   * Returns the created note's metadata.
4. **`PUT /api/notes/{filename}`**:
   * Receives `{ title, category, status, tags, content }`.
   * Updates file. If the title changes, deletes the old filename and writes to the new slug filename.
   * Returns updated metadata.
5. **`DELETE /api/notes/{filename}`**:
   * Deletes the file.
   * Returns confirmation: `{ "deleted": filename }`.

## UI Design & Interaction (Frontend)

Implemented in `aiOS-ui/dashboard/static/dashboard/index.html`.

### Navigation
* Add a menu item `Ideas & Notes` with a lightbulb icon in the main sidebar.
* Activates `#view-ideas` view.

### Layout: Split Pane (`#view-ideas`)
1. **Left Pane (Note List & Category Filter):**
   * **Category Section:** A dynamic list of categories (e.g., `All`, `aiOS`, `YouTube`) with counts. Clicking filters the notes list.
   * **Header:** Search bar and a primary button `+ New Note`.
   * **Note Stack:** Scrollable list of cards. Each card displays title, category tag, status badge (Draft/Active/Archived), and last-updated time.
2. **Right Pane (Workspace / Editor):**
   * **Welcome State:** Instructions to select or create a note.
   * **View Mode:**
     * Header containing title, category, status pill, and action buttons (`Copy Prompt`, `Edit`, `Delete`).
     * Status pill is a dropdown or clickable element to cycle status instantly.
     * Content box displaying parsed markdown with elegant styling (Outfit and JetBrains Mono fonts).
   * **Edit Mode:**
     * Form inputs: Title text field, Category autocomplete/dropdown select, Status dropdown, Tags input, and a Markdown text area.
     * Actions: `Save` and `Cancel` buttons.

## Verification Plan

### Automated/Unit Verification
* Verify python syntax of routers.
* Verify uvicorn server startup and API responses via simple python tests.

### Manual Verification
* Deploy the application locally on port `8787`.
* Create multiple notes in different categories (e.g., `aiOS`, `YouTube`).
* Verify files are written to host `private-notes/` directory.
* Verify the Docker sandbox cannot view files in `private-notes/`.
* Test search and category filtering.
* Test copy-to-clipboard functionality.
* Test quick status switching by clicking the status badge.
