# Entrypoint Restoration Guide

The Docker image already uses `/usr/local/bin/entrypoint.sh` as its entrypoint.
After a rebuild, that file is reset to the image default — restore it from the
copy saved here.

---

## What the entrypoint does (on every container start)

1. Fixes ownership of bind-mounted dirs (`.agentmemory`, `.hermes`, etc.)
2. Builds the Conda `ai-baseline` env on first launch
3. Copies `agentmemory/.env` → `~/.agentmemory/.env`
4. Copies `agentmemory/iii-config.yaml` → npm dist (absolute data paths)
5. Installs the patched `viewer-proxy.mjs` (Host-header rewrite for port 3113)
6. Starts agentmemory with correct config
7. Starts the agentmemory viewer proxy
8. Starts the hermes dashboard
9. Starts the hermes dashboard proxy (Host-header rewrite for port 9119)
10. `exec "$@"` — hands off to the container's shell (zsh)

---

## Restoration steps after a rebuild

### Step 1 — Restore the entrypoint

```bash
sudo cp /config-file/entrypoint/entrypoint.sh /usr/local/bin/entrypoint.sh
```

That's it. The next container restart will run the updated script automatically.

If you want to run it immediately in the current session without restarting:

```bash
bash /usr/local/bin/entrypoint.sh zsh
```

---

## Verify it worked

```bash
# Check the agentmemory and hermes logs from boot
grep '\[entrypoint\]' /dev/stdin < /proc/1/fd/1 2>/dev/null || true

# Or run the proxy smoke test
node -e "
const net=require('net'),LAN='172.17.0.3';
['3113','9119'].forEach(p=>{
  const c=net.connect(+p,LAN,()=>c.write('GET / HTTP/1.0\r\nHost: '+LAN+':'+p+'\r\n\r\n'));
  c.once('data',d=>{ console.log('port '+p+': '+d.toString().slice(0,15)); c.destroy(); });
  c.on('error',e=>console.error('port '+p+' FAIL:',e.message));
});
setTimeout(()=>process.exit(0),3000);"
```

Expected:
```
port 3113: HTTP/1.1 200 OK
port 9119: HTTP/1.1 200 OK
```

---

## Files

| File | Purpose |
|------|---------|
| `entrypoint.sh` | Copy of `/usr/local/bin/entrypoint.sh` — restore after every rebuild |
| `../agentmemory/.env` | agentmemory feature flags + Gemini key |
| `../agentmemory/iii-config.yaml` | Service config with absolute data paths |
| `../agentmemory/viewer-proxy.mjs` | Host-rewrite proxy for port 3113 |
| `../hermes/dashboard-proxy.mjs` | Host-rewrite proxy for port 9119 |
