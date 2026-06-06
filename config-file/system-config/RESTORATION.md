# System Restoration Guide

---

## Architecture

```
Dockerfile:
  COPY ./config-file/system-config/entrypoint.sh /usr/local/bin/entrypoint.sh
  ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
  CMD ["/bin/zsh"]
```

`/config-file/system-config/entrypoint.sh` IS the Docker entrypoint — baked into
the image on every `docker compose build`. Changes to it take effect after rebuild.

---

## What the entrypoint does on every container start

| Step | Action |
|------|--------|
| 1 | Fix ownership of bind-mounted dirs (if not writable) |
| 2 | Build Conda `ai-baseline` env if empty (first launch only) |
| 3 | Restore iii v0.11.2 from `~/.agentmemory/bin/iii` → `~/.local/bin/iii` |
| 4 | Copy `iii-config.yaml` to agentmemory dist dir |
| 5 | Install viewer-proxy.mjs (HTTP reverse proxy for agentmemory) |
| 6 | Start agentmemory (if not running) |
| 7 | Start viewer-proxy (if not running) |
| 8 | Restore Claude Code credentials from backup (if `~/.claude/.credentials.json` missing) |
| 9 | Refresh Claude Code OAuth token (`claude auth status`) |
| 10 | Start hermes dashboard + proxy (kills stale processes via /proc scan) |
| 11 | Start fcc-server (kills stale processes via /proc scan) |
| 12 | Start hermes gateway |
| 13 | Start watchdog (auto-restarts dashboard, proxy, viewer-proxy, fcc-server, gateway on crash) |
| 14 | `exec /bin/zsh` (hands off to interactive shell) |

## Diagnostic & Recovery Tooling

| Tool | File | Purpose |
|------|------|---------|
| Health check | `service_health.py` | Concurrent service probes (asyncio, 2s timeout). Exits 0/1. |
| Test suite | `test_service_health.py` | 16 mock-based tests. Zero deps, runs in <1s. |
| Recovery | `recover.sh` | One-shot fix-everything. Kill stale, restart, verify. |
| Shell login | `~/.zshrc` | Auto-runs `service_health.py` on every new terminal. |

`service_health.py` covers: iii engine, agentmemory, viewer-proxy, hermes
dashboard, dashboard-proxy, fcc-server, hermes gateway. It is the single
source of truth for what "healthy" means — recover.sh and .zshrc both
delegate to it rather than duplicating checks.

### Fixes applied 2026-05-31

| Bug | Fix |
|-----|-----|
| `agentmemory start` could abort entrypoint via `set -e` | Added `\\|\\| true` |
| Hermes proxy EADDRINUSE on restart: killed by stale PID, port not released | Scan `/proc/*/cmdline` for `dashboard-proxy` processes, kill all before starting |
| fcc-server same stale-process issue | Same `/proc` scan + kill before starting |
| Watchdog `$TG_STATE` never expanded (escaped as `\\$TG_STATE`) | Fixed to `$TG_STATE` — gateway reconnect now actually works |
| Watchdog only covered dashboard + gateway | Now also covers proxy and fcc-server |
| `claude auth status --output json` failed (unknown option) | Removed `--output json` |

### Fixes applied 2026-05-31 (session 2)

| Bug | Fix |
|-----|-----|
| /proc scan used SIGTERM: process could ignore, port not released → EADDRINUSE | Changed to `kill -9` (SIGKILL) + port-release polling via `/proc/net/tcp` (up to 5s for proxy, 3s for fcc) |
| Watchdog subshell inherited `set -e`: any transient command failure silently killed the 60s restart loop | Added `set +e` at top of watchdog subshell |
| `.zshrc` also starts `dashboard-proxy.mjs` — races with entrypoint for port 9119 | `.zshrc` updated with PID-file guard (see below) |
| agentmemory viewer-proxy not covered by watchdog — would die and stay dead after gateway crash | Added viewer-proxy restart to watchdog (PID file: `~/.agentmemory/viewer-proxy.pid`) |

### Fixes applied 2026-06-01

| Bug | Fix |
|-----|-----|
| Health checks duplicated across entrypoint, watchdog, and recover.sh — no canonical "healthy" definition | Created `service_health.py`: 7 concurrent async probes, 2s timeout, exit 0/1. Single source of truth. |
| No test coverage for health checks — timeout bugs, PID edge cases, JSON parse errors all silent | Created `test_service_health.py`: 16 mock-based tests, zero deps, runs <1s. |
| `~/.zshrc` had dead alias `service-health` (never defined) + proxy guard missed PID-file race | Replaced with `python3 .../service_health.py` auto-on-login + hardened proxy guard (PID file check before pgrep) |
| No one-shot recovery for post-sleep/wake service death (multiple services dead at once) | Created `recover.sh`: checks all 8 services, restarts dead ones, prints status table. |

### .zshrc (auto-status on login)

`~/.zshrc` starts the dashboard-proxy as a fallback (entrypoint handles it first;
the PID-file guard prevents duplicates) and runs `service_health.py` on every
new shell so you see service status immediately on login.

Current pattern:
```zsh
# Auto-start Hermes dashboard proxy (fallback with PID-file guard)
if ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null && \
   ! pgrep -f "dashboard-proxy.mjs" > /dev/null 2>&1; then
  node /config-file/hermes/dashboard-proxy.mjs >> ~/.hermes/logs/dashboard-proxy.log 2>&1 &
  disown
fi

# Show service status on every new shell
echo ""
python3 /config-file/system-config/service_health.py
```

---

## After a Docker rebuild

```bash
docker compose build && docker compose up -d
```

That's it — the entrypoint handles everything automatically.

Check it worked:
```bash
iii --version                          # expect: 0.11.2
agentmemory status                     # expect: Health: ✓ healthy
claude auth status                     # expect: "loggedIn": true
cat /tmp/claude-auth-refresh.log       # OAuth refresh result
tail -5 ~/.agentmemory/agentmemory.log # agentmemory start log
```

---

## Files managed by the entrypoint

| Source | Destination | Notes |
|--------|-------------|-------|
| `~/.agentmemory/bin/iii` | `~/.local/bin/iii` | v0.11.2, persistent → ephemeral |
| `aiOS-ui/agentmemory/iii-config.yaml` | agentmemory dist dir | Service bind config |
| `aiOS-ui/agentmemory/viewer-proxy.mjs` | `~/.agentmemory/viewer-proxy.mjs` | HTTP reverse proxy (Host-header fix) |
| `/config-file/hermes/dashboard-proxy.mjs` | `—` (started from source) | HTTP reverse proxy (Host-header fix) |
| `fcc/.env` *(optional)* | `~/.fcc/.env` | API keys (copied from backup) |

**Config backups stored in `/config-file/`:**
- `aiOS-ui/agentmemory/.env` — backed up to `/config-file/aiOS-ui/agentmemory/.env`
- `fcc/.env` — backed up to `/config-file/fcc/.env`
- `claude/settings.json` — backed up to `/config-file/claude/settings.json`
- `gemini/settings.json` — backed up to `/config-file/gemini/settings.json`

**Not in `/config-file/` (excluded via `.gitignore`):**
- `agentmemory/bin/iii` — in `~/.agentmemory/bin/iii` (persistent mount, 32 MB binary)
- `claude/.credentials.json` — in `~/.claude/.credentials.json` (persistent mount)

---

## Manual start if a service failed

**agentmemory:**
```bash
sudo cp /config-file/aiOS-ui/agentmemory/iii-config.yaml \
  /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
agentmemory start >> ~/.agentmemory/agentmemory.log 2>&1
sleep 4
cp /config-file/aiOS-ui/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
echo $! > ~/.agentmemory/viewer-proxy.pid
```

**hermes dashboard:**
```bash
mkdir -p ~/.hermes/logs
hermes dashboard --no-open >> ~/.hermes/logs/dashboard.log 2>&1 &
echo $! > /tmp/hermes-dashboard.pid
sleep 4
nohup node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
echo $! > /tmp/hermes-proxy.pid
```

**fcc-server:**
```bash
mkdir -p ~/.fcc/logs
nohup fcc-server >> ~/.fcc/logs/fcc-server.log 2>&1 &
echo $! > /tmp/fcc-server.pid
```

---

## Access URLs

| Service | Inside container | Host browser (localhost) | LAN device (via host IP) |
|---------|-----------------|------------------------|-------------------------|
| agentmemory viewer | http://localhost:3113 | http://localhost:3113 | http://<laptop-IP>:3113 |
| hermes dashboard | http://localhost:9119 | http://localhost:9119 | http://<laptop-IP>:9119 |
| fcc-server admin | http://localhost:8082/admin | http://localhost:8082/admin | http://<laptop-IP>:8082/admin |

For LAN access, publish ports in the host's `docker-compose.yml` **without**
the `127.0.0.1:` prefix (e.g. `"3113:3113"` instead of `"127.0.0.1:3113:3113"`).
See `/config-file/docker-compose.reference.yml` for a complete example with
`restart: always` for auto-start on laptop boot.

---

## Troubleshooting

### agentmemory not starting
```bash
tail -20 ~/.agentmemory/agentmemory.log
agentmemory stop 2>/dev/null; sleep 2; agentmemory start
```

### Hermes dashboard 421 errors
```bash
nohup node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
```

### fcc-server port 8082 in use
```bash
for f in /proc/[0-9]*/cmdline; do
  pid=${f%/cmdline}; pid=${pid#/proc/}
  grep -q "fcc-server" "$f" 2>/dev/null && kill "$pid"
done
nohup fcc-server >> ~/.fcc/logs/fcc-server.log 2>&1 &
echo $! > /tmp/fcc-server.pid
```
