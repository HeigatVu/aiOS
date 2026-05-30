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
| POST | `/api/volumes/upload` | Upload binary file to volume mount |
| GET | `/api/volumes/download` | Download binary file from volume mount |
| POST | `/api/config/dockerfile` | Append RUN layer to Dockerfile |
| POST | `/api/config/readme` | Append timestamped note to README |
| POST | `/api/config/environment` | Append to environment.yml |
| POST | `/api/config/volume` | Add new volume to docker-compose.yml |
| POST | `/api/editor/read` | Read text file contents inside container |
| POST | `/api/editor/write` | Save updated text file contents inside container |
| GET | `/api/sandbox/processes` | List active processes using `ps aux` |
| POST | `/api/sandbox/processes/kill` | Kill target process by PID (`kill -9`) |
| GET | `/api/sandbox/env` | Get container active environment + dotenv keys |
| POST | `/api/sandbox/env/save` | Add or update key in dynamic dotenv files |
| POST | `/api/sandbox/env/delete` | Remove key from dynamic dotenv files |
| GET | `/api/sandbox/ports` | Get Listening ports inside container |
| POST | `/api/db/query` | Run SQLite SQL queries and inspect tables |
| GET | `/` | Serve index.html |
| static | `/static/*` | Serve JS/CSS |

### Frontend Views & Features

- **Dashboard** — Docker socket + sandbox container status, live `docker logs -f` stream panel, active container stats metrics.
- **Terminal** — package installer tool (uv/conda/dnf/npm) with snippets terminal assistant panel (persisted custom command bank).
- **Volumes** — volume tables, recursive breadcrumb browser with uploads & downloads, inline chmod forms, and quick launcher buttons:
  - **edit** (purple/vibrant text editor using CodeMirror 5 with syntax highlighting)
  - **inspect** (SQLite database inspector with table schemas and custom interactive query executor)
  - **env** (Dynamic `.env` Manager)
- **Config** — configuration editor sub-tabs: Dockerfile, README, environment.yml, volume mapper, and the persistent **.env Manager**:
  - Automatically registers custom `.env` file paths visited from volumes.
  - Active dropdown selector context switcher.
  - CRUD operations: Edit, add new, and permanently **delete** environment variables.

---

## Known state & caveats

- `app.py` (Streamlit) is still in the directory — safe to delete once the new stack is confirmed working
- The chmod route is ordered BEFORE `/{idx}/mode` and `/{idx}/files` in `main.py` on purpose — FastAPI would otherwise try to cast "chmod" as `int` and return 422
- Volume mode toggle writes to docker-compose.yml immediately but **requires a container restart** to take effect (the UI shows a hint)
- `list_files_in_container` uses `find + stat -c '%a|%U|%G|%s|%F|%n'` — maxdepth 1 only (not recursive)
- WebSocket streaming bridges the synchronous docker-py generator into async FastAPI via `threading.Thread` + `queue.Queue`

---

## Completed Batch (High-Fidelity Features)

- [x] **Restart sandbox button** on Dashboard
- [x] **Live container logs** in Dashboard with WebSocket streaming
- [x] **GPU / CPU / RAM usage metrics** dynamically loaded from stats API
- [x] **Delete volume entry** in Volumes tab (two-step Detach action)
- [x] **Terminal history & Snippets bank** persisted in localStorage
- [x] **Rebuild image button** streaming docker-compose build stdout
- [x] **Vue Router integration** supporting fully deep-linkable URLs
- [x] **CodeMirror 5 Text Editor** with customized light & dark theme wrappers
- [x] **SQLite Database Inspector** and interactive custom query executor
- [x] **Volume Upload & Download utilities** for seamless binary binary transfer
- [x] **Light Theme Mode Toggle** with persistent localStorage setting
- [x] **Sub-project .env Manager** with dynamic dropdown, auto-register, and key deletion CRUD

---

## Future Enhancements & Ideas Checkpoint (Next Batch)

- [ ] **Real-time Pty Terminal (xterm.js):** Upgrade command executor to support full interactive shell sessions using pseudo-terminals (PTYs).
- [ ] **Interactive Metrics History:** Render active memory, CPU, and GPU usage over time as beautiful Chart.js lines rather than plain static text cards.
- [ ] **Visual Git Manager:** View current git branch status, local uncommitted diff comparison, and add rapid commit-and-push actions.
- [ ] **Process Resource Monitoring:** Show individual process memory and CPU consumption dynamically in the Processes list to quickly identify heavy tasks.
- [ ] **Automatic Port Tunneling:** Expose internal container ports on public or host networks dynamically using custom reverse proxies or tunnels.
