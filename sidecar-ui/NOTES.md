# sidecar-ui — Build Notes

## What was here before

Streamlit app (`app.py`) — single-file dashboard with:

- Package installer terminal (uv / conda / dnf / npm)
- Dockerfile auto-install section editor
- README.md note appender
- environment.yml editor
- Volume mapper (add new mounts to docker-compose.yml)

## What we converted it to

FastAPI backend + Vue 3 frontend (CDN, no build step).

### Stack

- **Backend:** FastAPI + uvicorn, running on port 8502
- **Frontend:** Vue 3 via unpkg CDN (no npm/vite), served from `static/`
- **Container image:** `python:3.11-slim` + uv for installs

### File map

```
sidecar-ui/
├── Dockerfile.sidecar      FastAPI + uvicorn (replaced Streamlit)
├── main.py                 FastAPI app — all API routes + WebSocket
├── docker_bridge.py        Docker SDK wrapper (exec streaming, file listing)
├── volumes.py              docker-compose.yml volume parser + mode updater
├── config_editors.py       Dockerfile / README / environment.yml writers (unchanged)
├── app.py                  OLD Streamlit file — kept but not used, safe to delete
└── static/
    ├── index.html          Vue 3 shell
    ├── app.js              Full SPA: all components + API + WebSocket logic
    └── style.css           Dark dev-tool theme (VS Code-ish)
```

### API routes

| Method | Path | Does |
|--------|------|------|
| GET | `/api/status` | Sandbox container status |
| WS | `/ws/exec` | Stream command output from sandbox |
| GET | `/api/volumes` | List all sandbox volume mounts |
| POST | `/api/volumes/chmod` | chmod a file inside the container |
| POST | `/api/volumes/{idx}/mode` | Toggle rw/ro in docker-compose.yml |
| GET | `/api/volumes/{idx}/files` | List files inside the container path |
| POST | `/api/config/dockerfile` | Append RUN layer to Dockerfile |
| POST | `/api/config/readme` | Append timestamped note to README |
| POST | `/api/config/environment` | Append to environment.yml |
| POST | `/api/config/volume` | Add new volume to docker-compose.yml |
| GET | `/` | Serve index.html |
| static | `/static/*` | Serve JS/CSS |

### Frontend tabs

- **Dashboard** — Docker socket + sandbox status cards
- **Terminal** — ecosystem picker (uv/conda/dnf/npm), package name or raw command, WebSocket streaming output, optional "bake into Dockerfile" + "save note to README" checkboxes
- **Volumes** — volume table with mode badges, Browse button (file listing with octal + symbolic perms), chmod inline form, Toggle mode button (writes docker-compose.yml)
- **Config** — sub-tabs for Dockerfile / README / environment.yml / volume mapping

---

## Known state & caveats

- `app.py` (Streamlit) is still in the directory — safe to delete once the new stack is confirmed working
- The chmod route is ordered BEFORE `/{idx}/mode` and `/{idx}/files` in `main.py` on purpose — FastAPI would otherwise try to cast "chmod" as `int` and return 422
- Volume mode toggle writes to docker-compose.yml immediately but **requires a container restart** to take effect (the UI shows a hint)
- `list_files_in_container` uses `find + stat -c '%a|%U|%G|%s|%F|%n'` — maxdepth 1 only (not recursive)
- WebSocket streaming bridges the synchronous docker-py generator into async FastAPI via `threading.Thread` + `queue.Queue`

---

## Ideas / things to continue

- [x] **Restart sandbox button** on Dashboard → POST `/api/sandbox/restart` → `docker restart ai_tui_sandbox`
- [x] **Live container logs** in Dashboard → WebSocket `/ws/logs` tails `docker logs -f`, toggle on/off
- [x] **GPU / CPU / RAM usage cards** — CPU + RAM from Docker stats API; GPU via `nvidia-smi` exec (hidden if unavailable)
- [x] **Delete volume entry** in Volumes tab — click Delete → Confirm? two-step, calls DELETE `/api/volumes/{idx}`
- [x] **Terminal history** — last 20 commands persisted in localStorage, ↑↓ arrow keys to navigate
- [x] **Rebuild image button** — streams `docker compose build` output via WebSocket `/ws/rebuild`
- [x] **Vue Router** — tabs are now deep-linkable via URL hash (`/#/dashboard`, `/#/terminal`, etc.)

### Future Enhancements (Next Batch)

**Developer Experience (DX) & Productivity**
- [ ] **Web-Based File Editor** — Integrate Monaco Editor or CodeMirror into a new "Editor" tab for quick script/config edits.
- [ ] **Snippet Library / Saved Commands** — Save frequently used complex commands with descriptions for one-click execution.
- [ ] **Environment Variables Manager** — UI for managing `.env` files or container environment variables (add, edit, hide/show secrets).

**Container State & Debugging**
- [ ] **Process Explorer (Task Manager)** — Run `ps aux` or `top` inside the sandbox and display in a data table, with a "Kill Process" button.
- [ ] **Network & Port Manager** — Show listening ports (`netstat` / `ss`) and provide a way to dynamically expose new ports.
- [ ] **Log Filtering & Search** — Enhance live logs with a search bar (regex) and log level filtering (Error, Warn, Info).

**File & Data Management**
- [ ] **File Upload/Download** — In the Volumes tab, add ability to upload/download files directly from host to container via the browser.
- [ ] **SQLite / DB Viewer** — Built-in SQLite table viewer to inspect database files without downloading them.

**UI / UX Polish**
- [ ] **Toast Notifications** — Non-blocking toasts in the corner for long-running commands (image rebuilds, heavy installs).
- [ ] **Theme Toggle** — Add a Light/Dark mode toggle, persisted in localStorage.
- [ ] **System Resource Alarms** — Visual indicators (orange/red) when the container maxes out its allocated CPU/RAM/GPU resources.
