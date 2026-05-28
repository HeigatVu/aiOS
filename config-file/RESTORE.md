# Agentmemory Docker Restore

After rebuilding the Docker container, run these steps in order.

---

## Step 1 — Copy config files into place

```bash
# general port proxy (replaces viewer-proxy.mjs)
cp /config-file/proxy.mjs ~/proxy.mjs

# iii-config.yaml — patched to bind REST/stream to 127.0.0.1 (not 0.0.0.0)
# and to include the correct CORS origins for the viewer
cp /config-file/iii-config.yaml \
  /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
```

---

## Step 2 — Start agentmemory

```bash
cd ~/.agentmemory
agentmemory start
```

Wait a few seconds for the daemon to come up, then verify:

```bash
agentmemory status
```

---

## Step 3 — Start the port proxy

Services bind to 127.0.0.1 inside the container. The proxy re-exposes them on
the container's LAN IP so the host ma- agentmemory uses Gemini (gemini-3.1-flash-lite) as the LLM providerchine can reach them.

```bash
node ~/proxy.mjs &
```

Output looks like:

```
[proxy] agentmemory-viewer       172.17.0.2:3113 -> 127.0.0.1:3113
```

Open the viewer from the host at: `http://<container-ip>:3113`

To add a new service later, edit `proxy.mjs` and add a line to the PORTS array:

```js
{ port: 8080, label: "my-app" },
```

---

## What each file does

| File | Purpose |
|------|---------|
| `proxy.mjs` | General TCP proxy — exposes any listed port on LAN IP; edit PORTS array to add services |
| `iii-config.yaml` | iii worker config — REST on port 3111, streams on 3112, viewer on 3113 |

---
