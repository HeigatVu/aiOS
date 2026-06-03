# Post-Rebuild Verification Prompt

After `docker compose build && docker compose up -d`, paste the block below
into Claude Code. Claude will verify every service, fix anything broken, and
report a final status table.

---

## Quick Recovery (preferred — one command)

Run: `bash /config-file/system-config/recover.sh`

This single command checks and restarts: iii, agentmemory, viewer-proxy,
hermes dashboard, dashboard-proxy, fcc-server, gateway, and the watchdog.
Outputs a status table at the end.

---

## Health Check (diagnostic only — no fixes)

Run: `python3 /config-file/system-config/service_health.py`

Concurrently probes all 7 services (asyncio, 2s timeout each) and prints a
color table. Exits 0 if all healthy, 1 if any fail. Zero external deps.
Tests live at `test_service_health.py` (16 tests, mock-based, no real services).

This runs automatically on every new shell via `~/.zshrc` — you see the
table on login without doing anything.

---

## Manual Recovery Steps (if recover.sh unavailable)

```
Read /config-file/step-to-reconfig.md and execute every step in order.
Fix anything that is not in the expected state before moving to the next step.

## Step 0 — Entrypoint ran correctly

Check the entrypoint logs:
  tail -5 ~/.agentmemory/agentmemory.log
  cat /tmp/claude-auth-refresh.log

If agentmemory.log shows "iii-engine on PATH is v0.16.1" errors:
  the iii binary needs restoring (Step 1 will fix this).
If claude-auth-refresh.log is missing or empty:
  the entrypoint may not have run — verify with:
    grep "config-file/system-config" /usr/local/bin/entrypoint.sh

## Step 1 — iii engine

Run: iii --version
Expected: 0.11.2

If wrong version:
  cp ~/.agentmemory/bin/iii ~/.local/bin/iii && chmod +x ~/.local/bin/iii

If ~/.agentmemory/bin/iii is missing (re-download once):
  mkdir -p ~/.agentmemory/bin
  curl -fsSL -o /tmp/iii.tar.gz \
    https://github.com/iii-hq/iii/releases/download/iii/v0.11.2/iii-x86_64-unknown-linux-gnu.tar.gz
  tar -xzf /tmp/iii.tar.gz -C ~/.agentmemory/bin
  chmod +x ~/.agentmemory/bin/iii
  cp ~/.agentmemory/bin/iii ~/.local/bin/iii

## Step 2 — agentmemory

Run: agentmemory status
Expected: Health: ✓ healthy, Provider: ✓ llm, four flags ticked

If "Not running":
  sudo cp /config-file/agentmemory/iii-config.yaml \
    /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
  agentmemory start >> ~/.agentmemory/agentmemory.log 2>&1
  sleep 5
  agentmemory status

## Step 3 — agentmemory viewer-proxy

Run: tail -1 ~/.agentmemory/viewer-proxy.log
Expected: contains "host-rewrite enabled"

If stale or missing:
  kill $(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null) 2>/dev/null
  cp /config-file/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
  nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
  echo $! > ~/.agentmemory/viewer-proxy.pid
  sleep 1 && tail -1 ~/.agentmemory/viewer-proxy.log

## Step 4 — Hermes dashboard

Run: kill -0 $(cat /tmp/hermes-dashboard.pid 2>/dev/null) 2>/dev/null && echo OK || echo FAIL

If FAIL:
  mkdir -p ~/.hermes/logs
  hermes dashboard --no-open >> ~/.hermes/logs/dashboard.log 2>&1 &
  echo $! > /tmp/hermes-dashboard.pid
  sleep 4

## Step 5 — Hermes dashboard-proxy

Run: kill -0 $(cat /tmp/hermes-proxy.pid 2>/dev/null) 2>/dev/null && echo OK || echo FAIL

If FAIL:
  nohup node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
  echo $! > /tmp/hermes-proxy.pid

## Step 6 — fcc-server

Run: kill -0 $(cat /tmp/fcc-server.pid 2>/dev/null) 2>/dev/null && echo OK || echo FAIL

If FAIL:
  mkdir -p ~/.fcc/logs
  nohup fcc-server >> ~/.fcc/logs/fcc-server.log 2>&1 &
  echo $! > /tmp/fcc-server.pid

## Step 7 — Watchdog

Run: tail -3 /tmp/hermes-watchdog.log 2>/dev/null || echo "WATCHDOG LOG MISSING"

Expected: Recent timestamps within the last 2 minutes. If the log is
missing or has no entries from the last 2 minutes, the watchdog is dead.

If DEAD (restart it):
  (set +e
  while true; do
    sleep 60
    if ! kill -0 "$(cat /tmp/hermes-dashboard.pid 2>/dev/null)" 2>/dev/null; then
      mkdir -p "$HOME/.hermes/logs"
      hermes dashboard --no-open >>"$HOME/.hermes/logs/dashboard.log" 2>&1 &
      echo $! >/tmp/hermes-dashboard.pid
    fi
    if ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null; then
      nohup node /config-file/hermes/dashboard-proxy.mjs >>/tmp/hermes-proxy.log 2>&1 &
      echo $! >/tmp/hermes-proxy.pid
    fi
    if ! kill -0 "$(cat /tmp/fcc-server.pid 2>/dev/null)" 2>/dev/null; then
      nohup fcc-server >>"$HOME/.fcc/logs/fcc-server.log" 2>&1 &
      echo $! >/tmp/fcc-server.pid
    fi
    if [ -f "$HOME/.hermes/gateway_state.json" ]; then
      TG_STATE=$(python3 -c "import json; d=json.load(open('$HOME/.hermes/gateway_state.json')); print(d.get('gateway_state',''), d.get('platforms',{}).get('telegram',{}).get('state','unknown'))" 2>/dev/null)
      if ! echo "$TG_STATE" | grep -q "running connected"; then
        hermes gateway restart >>"$HOME/.hermes/logs/gateway.log" 2>&1 || true
      fi
    fi
  done) >>/tmp/hermes-watchdog.log 2>&1 &

## Step 8 — Final status

Run all checks and output a markdown table:

  iii --version
  agentmemory status 2>&1 | grep -E 'Health|Provider|Not running'
  claude auth status 2>/dev/null
  kill -0 $(cat /tmp/hermes-dashboard.pid 2>/dev/null) 2>/dev/null && echo "hermes OK" || echo "hermes FAIL"
  kill -0 $(cat /tmp/fcc-server.pid 2>/dev/null) 2>/dev/null && echo "fcc OK" || echo "fcc FAIL"
  tail -1 ~/.agentmemory/viewer-proxy.log

Format: | Service | Status | Notes |
Do not stop until every service shows OK or healthy.
```

---

## Optional — Step 9: Proxies returning 400 from LAN IP

Run: `CONTAINER_IP=$(hostname -I | awk '{print $1}') && curl -s -o /dev/null -w '%{http_code}' http://$CONTAINER_IP:3113/`
Expected: 200

If 400, the proxy is using the old raw-TCP implementation. Fix:
  cp /config-file/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
  kill $(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null) 2>/dev/null
  nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
  echo $! > ~/.agentmemory/viewer-proxy.pid

Same for hermes (port 9119):
  kill $(cat /tmp/hermes-proxy.pid 2>/dev/null) 2>/dev/null
  nohup node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
  echo $! > /tmp/hermes-proxy.pid

Note: /config-file/ version now uses http.createServer (proper HTTP forwarding)
instead of net.createServer (raw TCP with regex Host rewriting). The source files
have been updated — entrypoint copies them on rebuild.

## Optional — Step 10: Docker auto-start + LAN access

On your host laptop, copy `/config-file/docker-compose.reference.yml` to the same
directory as your Dockerfile, rename to `docker-compose.yml`, adjust the image
name, then run:

  docker compose down && docker compose up -d

Key settings:
  restart: always        # auto-start on laptop boot
  ports without 127.0.0.1:  # accessible from any LAN device

Also ensure Docker itself auto-starts:
  sudo systemctl enable docker

## Access URLs

| Service | URL (inside container) | URL (from LAN via host) |
|---------|----------------------|------------------------|
| agentmemory viewer | <http://localhost:3113> | http://<laptop-IP>:3113 |
| hermes dashboard | <http://localhost:9119> | http://<laptop-IP>:9119 |
| fcc-server | <http://localhost:8082/admin> | http://<laptop-IP>:8082/admin |

---

## Normal rebuild flow (everything auto-starts)

```bash
# On host:
docker compose build && docker compose up -d
# Then inside container — just verify:
agentmemory status && claude auth status
```

The entrypoint handles iii, agentmemory, Claude auth, hermes, fcc-server, and
gateway automatically. A watchdog (60s loop) auto-restarts dashboard, proxy,
fcc-server, and gateway if they crash. The steps above are only needed when
something fails.

### Bug fixes (2026-06-01, session 3)

- **`set -e` removed** from entrypoint top — it caused PID 1 to hang at `do_wait`
  when background jobs exited before `exec`, preventing the watchdog from starting
  and preventing `exec "$@"` from handing off to zsh
- **Watchdog moved to top** of entrypoint (right after ownership fix) — starts
  before any services so it survives even if later sections hang
- **`disown -a` added** before `exec "$@"` to prevent bash from waiting for
  background jobs before handing off to zsh
- **`recover.sh` created** at `/config-file/system-config/recover.sh` — one-command
  recovery that checks and restarts all services + watchdog, outputs status table

### Bug fixes (2026-05-31, session 1)

- `set -e` in entrypoint no longer aborts on `agentmemory start` failure
- Hermes proxy + fcc-server: stale processes killed via `/proc` scan before start (fixes EADDRINUSE)
- Watchdog `$TG_STATE` variable expansion fixed (was escaped literal)
- Watchdog now covers dashboard-proxy and fcc-server (not just dashboard + gateway)
- `claude auth status --output json` → `claude auth status` (unknown flag removed)

### Bug fixes (2026-05-31, session 2)

- `/proc` scan now uses SIGKILL (-9) instead of SIGTERM — processes can't ignore it, port releases immediately
- Port-release polling via `/proc/net/tcp` before starting proxy (up to 5s) and fcc-server (up to 3s)
- Watchdog subshell now runs with `set +e` — transient failures no longer kill the 60s restart loop
- `.zshrc` duplicate proxy startup documented as a known race condition (see RESTORATION.md for fix)
- agentmemory viewer-proxy added to watchdog coverage (was missing — would die and stay dead)
