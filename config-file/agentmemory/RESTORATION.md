# agentmemory Restoration Guide

Read this file at the start of any session after a Docker container rebuild.
Follow the steps in order; each step has a verification check.

---

## Background — why this is needed

On every container start, agentmemory launches a bare boot daemon (low PID, ~90)
with **no environment variables**. This daemon:
- Binds ports 3111 (REST), 3112 (streams), 3113 (viewer) on 127.0.0.1
- Reads nothing from `~/.agentmemory/.env` — all feature flags are absent
- Spawns `~/.agentmemory/viewer-proxy.mjs` to expose the viewer on the LAN IP

The viewer enforces a Host-header allowlist using `process.env.VIEWER_ALLOWED_HOSTS`,
which is evaluated at module load time — **not** from the `.env` file. So even after
writing the correct env, the boot daemon's viewer rejects browser requests with
`403 forbidden host`.

The fix lives in `viewer-proxy.mjs`: an HTTP-aware reverse proxy using
`http.createServer` → `http.request`. It forwards all requests to the backend
viewer on `127.0.0.1:3113`, rewriting the `Host` header to `localhost:3113`
so the viewer's allowlist check passes. The original implementation used raw
TCP (`net.createServer`) with regex-based Host rewriting on the first chunk,
which was fragile and returned `400 Bad Request` from the container LAN IP.
The current HTTP-based approach returns `200` from both localhost and the
container IP.

---

## Architecture — what auto-starts on container rebuild

The entrypoint chain handles everything automatically:

```
Docker daemon
  └─ /usr/local/bin/entrypoint.sh        (baked into image)
       └─ /config-file/system-config/entrypoint.sh   (starts agentmemory + all services)
```

On each rebuild the entrypoint:
1. Copies `~/.agentmemory/bin/iii` (v0.11.2, persistent) → `~/.local/bin/iii` (ephemeral)
2. Copies `iii-config.yaml` to the agentmemory dist directory
3. Installs the patched `viewer-proxy.mjs`
4. Starts agentmemory
5. Starts viewer-proxy

**You should not need to do anything manually after a rebuild.**

---

## Files managed here

| File | Purpose |
|------|---------|
| `iii-config.yaml` | Service config — binds REST/stream to 127.0.0.1, sets CORS origins |
| `viewer-proxy.mjs` | HTTP reverse proxy (`http.createServer`): exposes viewer on LAN IP with proper Host-header forwarding |

**Not in this directory (intentionally):**
- `.env` — lives only in `~/.agentmemory/.env` (persistent mount, never pushed to git)
- `bin/iii` — lives only in `~/.agentmemory/bin/iii` (persistent mount, never pushed to git)

---

## Why iii v0.11.2 is pinned

`~/.local/bin/` is ephemeral — it resets to the Docker image on every rebuild.
The image ships iii v0.16.1. agentmemory v0.9.24 hard-pins v0.11.2; v0.16.1
causes `state::list-not-found` runtime failures.

The correct binary is stored at `~/.agentmemory/bin/iii` (persistent mount).
The entrypoint copies it to `~/.local/bin/iii` on every start.

To re-download v0.11.2 if the persistent binary is lost:
```bash
mkdir -p ~/.agentmemory/bin
curl -fsSL -o /tmp/iii.tar.gz \
  https://github.com/iii-hq/iii/releases/download/iii/v0.11.2/iii-x86_64-unknown-linux-gnu.tar.gz
tar -xzf /tmp/iii.tar.gz -C ~/.agentmemory/bin
chmod +x ~/.agentmemory/bin/iii
~/.agentmemory/bin/iii --version  # should print 0.11.2
```

---

## Verification after rebuild

```bash
# agentmemory healthy?
agentmemory status
# Expected: Health: ✓ healthy, Provider: ✓ llm

# iii version correct?
iii --version
# Expected: 0.11.2

# viewer-proxy running?
tail -1 ~/.agentmemory/viewer-proxy.log
# Expected: host-rewrite enabled

# viewer accessible from loopback?
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3113/
# Expected: 200

# viewer accessible from container LAN IP?
curl -s -o /dev/null -w '%{http_code}\n' http://$(hostname -I | awk '{print $1}'):3113/
# Expected: 200
```

## Access URLs

| From | URL |
|------|-----|
| Inside container | http://localhost:3113 |
| Host browser (via docker-compose port mapping) | http://localhost:3113 |
| LAN device (via docker-compose, no 127.0.0.1: prefix) | http://<laptop-IP>:3113 |

See `/config-file/docker-compose.reference.yml` for the host-side configuration
(`restart: always` + published ports without `127.0.0.1:` prefix).

---

## Manual start if a service failed

```bash
# Restore iii and start agentmemory
cp ~/.agentmemory/bin/iii ~/.local/bin/iii && chmod +x ~/.local/bin/iii
sudo cp /config-file/agentmemory/iii-config.yaml \
  /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
agentmemory start >> ~/.agentmemory/agentmemory.log 2>&1
sleep 4

# Start viewer-proxy
cp /config-file/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
echo $! > ~/.agentmemory/viewer-proxy.pid
```

---

## Troubleshooting

### Viewer falls back to port 3114 (stale boot daemon)

A bare `agentmemory` boot daemon (PID ~90, from the Docker image) starts
without environment variables and grabs localhost:3113. When the entrypoint
starts the real agentmemory, it cannot bind port 3113 and silently falls
back to 3114. The viewer-proxy still forwards to 3113 — requests fail.

Fix — kill the stale daemon and restart:

```bash
# Find PID holding 3113
awk 'NR>1 { split($2,a,":"); p=strtonum("0x"a[2]); if(p==3113) print $10 }' /proc/net/tcp
# Look up the PID from the inode:
lsof -i :3113 | grep localhost | awk '{print $2}'
# Kill it
kill <PID>
# Kill current agentmemory (on 3114) and restart
kill $(cat ~/.agentmemory/iii.pid 2>/dev/null) 2>/dev/null
sleep 2
sudo cp /config-file/agentmemory/iii-config.yaml \
  /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
agentmemory start >> ~/.agentmemory/agentmemory.log 2>&1
sleep 5
agentmemory status  | grep Viewer  # should show :3113, not :3114
```

### Viewer returns 400 Bad Request from LAN IP

The proxy is using the old raw-TCP implementation. Fix:

```bash
cp /config-file/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
kill $(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null) 2>/dev/null
nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
echo $! > ~/.agentmemory/viewer-proxy.pid
sleep 1
curl -s -o /dev/null -w '%{http_code}\n' http://$(hostname -I | awk '{print $1}'):3113/
# Expected: 200
```

### Flags not showing in `agentmemory status`

`.env` was missing or the daemon started before it was populated. Verify:

```bash
grep 'AGENTMEMORY_AUTO_COMPRESS\|CONSOLIDATION_ENABLED' ~/.agentmemory/.env
```

If missing, the `.env` needs to be recreated manually (it's not in git by design).

### LAN IP changed after rebuild

The LAN IP is auto-detected by viewer-proxy.mjs at startup — no action needed.

---

## Known bug in agentmemory v0.9.22+

`VIEWER_ALLOWED_HOSTS` in `.env` is silently ignored. The viewer reads
`process.env.VIEWER_ALLOWED_HOSTS` at module-load time; `loadEnvFile()` only
populates `getMergedEnv()`, not `process.env`. The viewer-proxy Host-rewrite
is the correct workaround until this is fixed upstream.
