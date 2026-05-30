# sidecar-ui — Reference Notes

## Stack

- **Backend:** FastAPI + uvicorn, port `8502`
- **Frontend:** Vue 3 (unpkg CDN, no build step) + Vue Router 4, served from `static/`
- **Container image:** `python:3.11-slim` + uv

## File Map

```
sidecar-ui/
├── Dockerfile.sidecar      FastAPI + uvicorn image
├── main.py                 All API routes, WebSocket endpoints, lifespan
├── docker_bridge.py        Docker SDK wrapper — exec, streaming, file I/O, stats, PTY helpers
├── git_manager.py          git -C <path> operations inside the sandbox container
├── volumes.py              docker-compose.yml volume parser + mode updater
├── config_editors.py       Dockerfile / README / environment.yml writers
├── app.py                  OLD Streamlit file — unused, safe to delete
└── static/
    ├── index.html          Vue 3 shell + CDN imports (CodeMirror 5, Chart.js 4, xterm.js 4)
    ├── app.js              Full SPA — all components, router, API helpers, WebSocket logic
    └── style.css           Dark dev-tool theme (VS Code palette), light theme toggle
```

---

## API Routes

| Method | Path | Does |
|--------|------|------|
| GET | `/api/status` | Sandbox container status |
| POST | `/api/sandbox/restart` | Restart sandbox container |
| GET | `/api/sandbox/stats` | Live CPU / RAM / GPU metrics |
| GET | `/api/sandbox/stats/history` | Last 60 stat samples (5-min ring buffer) |
| GET | `/api/sandbox/processes` | `ps aux` process list |
| POST | `/api/sandbox/processes/kill` | `kill -9 <pid>` |
| GET | `/api/sandbox/env` | Container env + dotenv keys |
| POST | `/api/sandbox/env/save` | Upsert key in dotenv file |
| POST | `/api/sandbox/env/delete` | Delete key from dotenv file |
| GET | `/api/sandbox/ports` | Listening ports (`ss -tlnp`) |
| GET | `/api/volumes` | List volume mounts from docker-compose.yml |
| POST | `/api/volumes/chmod` | chmod a path inside the container |
| DELETE | `/api/volumes/{idx}` | Remove volume entry from docker-compose.yml |
| POST | `/api/volumes/{idx}/mode` | Toggle rw/ro in docker-compose.yml |
| GET | `/api/volumes/{idx}/files` | List files at a container path |
| POST | `/api/volumes/upload` | Upload binary file into a volume path |
| GET | `/api/volumes/download` | Download binary file from a volume path |
| POST | `/api/editor/read` | Read text file from container |
| POST | `/api/editor/write` | Write text file to container |
| POST | `/api/db/query` | Run SQLite query inside container |
| GET | `/api/git/status` | Branch + staged/unstaged/untracked |
| POST | `/api/git/diff` | Patch diff (working tree or staged) |
| POST | `/api/git/stage` | `git add -A` |
| POST | `/api/git/commit` | Commit with message |
| POST | `/api/git/push` | Push to remote |
| POST | `/api/config/dockerfile` | Append RUN layer to Dockerfile |
| POST | `/api/config/readme` | Append note to README.md |
| POST | `/api/config/environment` | Append package to environment.yml |
| POST | `/api/config/volume` | Add volume to docker-compose.yml |
| WS | `/ws/exec` | Stream one-shot command output |
| WS | `/ws/logs` | `docker logs -f` stream |
| WS | `/ws/rebuild` | `docker compose build` stream |
| WS | `/ws/pty` | Full bidirectional PTY shell (resize-aware) |
| GET | `/` | Serve index.html |
| static | `/static/*` | Serve JS/CSS |

---

## Frontend Views

| Route | View | Key features |
|-------|------|-------------|
| `#/dashboard` | Dashboard | Container status cards, CPU/RAM/GPU live bars, Chart.js history charts (5 min), live logs, rebuild stream, restart button |
| `#/terminal` | Terminal | Package installer (uv/conda/dnf/npm), raw command executor, command history (↑↓), custom snippet bank (localStorage) |
| `#/pty` | PTY Shell | Full xterm.js interactive shell session, terminal resize, connects to `/ws/pty` |
| `#/volumes` | Volumes | Volume table, breadcrumb file browser, upload/download, chmod form, mode toggle (rw/ro), Detach (two-step) |
| `#/processes` | Processes & Ports | ps aux with CPU/MEM color bars, kill action, listening ports tab |
| `#/git` | Git Manager | Branch status, staged/unstaged file lists, diff viewer, stage-all + commit + push |
| `#/editor` | File Editor | CodeMirror 5, auto language detection, save to container |
| `#/db-viewer` | SQLite Inspector | Table schema browser, interactive SQL executor |
| `#/config` | Config | Dockerfile / README / Conda yml / Volume mapper tabs + .env Manager (multi-file, CRUD) |

---

## Known Caveats

- `app.py` (Streamlit) is still present — safe to delete
- The `/api/volumes/chmod` route is ordered **before** `/{idx}/mode` and `/{idx}/files` intentionally — FastAPI would otherwise try to cast the literal `"chmod"` as `int` and return 422
- Volume mode toggle writes docker-compose.yml immediately but **requires a container restart** to take effect (UI shows a hint; live `mount -o remount` is attempted first via `SYS_ADMIN`)
- `list_files_in_container` uses `find -maxdepth 1 + stat` — not recursive by design
- WebSocket streaming bridges synchronous docker-py generators via `threading.Thread` + `queue.Queue`
- PTY (`/ws/pty`) requires the `docker` CLI on the same host as the sidecar process

---

## Pending

- **Port Tunneling** — pure-Python asyncio TCP proxy (no socat needed): `asyncio.start_server` on a host port → container IP:port, managed start/stop via API. Deferred; ready to implement on request.
