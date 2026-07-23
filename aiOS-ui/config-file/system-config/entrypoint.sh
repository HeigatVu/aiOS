#!/bin/bash
set +e
# NOTE: set +e (not -e). With set -e, bash on PID 1 can hang at do_wait
# when background jobs exit before exec, never reaching exec or the watchdog.
# Explicit error handling is used where needed.

# ── system init ───────────────────────────────────────────────────────────────

# Fix ownership of bind-mounted directories (Docker may create them as root).
AI_HOME="/home/ai_user"
DIRS=(
  "$AI_HOME/.cache/uv"
  "$AI_HOME/miniconda3/envs/ai-baseline"
  "$AI_HOME/miniconda3/pkgs"
  "$AI_HOME/.agentmemory"
  "$AI_HOME/.hermes"
  "$AI_HOME/.mimocode"
  "$AI_HOME/.agents"
  "$AI_HOME/.feynman"
  "$AI_HOME/.reasonix"
)
for dir in "${DIRS[@]}"; do
  if [ -d "$dir" ]; then
    chown -R ai_user:ai_user "$dir"
  fi
done

# Build the Conda ai-baseline env on first launch if the bind-mount is empty.
ENV_DIR="/home/ai_user/miniconda3/envs/ai-baseline"
if [ ! -f "$ENV_DIR/conda-meta/history" ]; then
  echo "[entrypoint] Building Conda env 'ai-baseline' (first launch — this is slow)..."
  runuser -u ai_user -- env HOME=/home/ai_user /home/ai_user/miniconda3/bin/conda env create -f /home/ai_user/environment.yml -p "$ENV_DIR" ||
    echo "[entrypoint] WARNING: conda env create failed — continuing without it."
fi

# Resolve python interpreter with fastapi/uvicorn
PYTHON_EXE="python"
for py in "/home/ai_user/.hermes/hermes-agent/venv/bin/python" "/aiOS-ui/features/hermes-webui/.venv/bin/python" "/home/ai_user/miniconda3/envs/ai-baseline/bin/python" "python"; do
  if [ -x "$py" ]; then
    PYTHON_EXE="$py"
    break
  fi
done

# ── watchdog (starts FIRST so it survives even if later sections hang) ──────────
# Covers: dashboard, proxy, viewer-proxy, gateway, headroom
# Runs in background. Uses set +e internally to never die from transient errors.
# disown prevents PID 1 from waiting for this infinite-loop process.
(
  set +e
  while true; do
    sleep 60
    # Dashboard
    if [ -f /tmp/hermes-dashboard.pid ] && ! kill -0 "$(cat /tmp/hermes-dashboard.pid 2>/dev/null)" 2>/dev/null; then
      runuser -u ai_user -- env HOME=/home/ai_user HERMES_WEBUI_TRUST_FORWARDED_HOST=1 zsh -c 'mkdir -p ~/.hermes/logs && hermes dashboard --no-open >> /config-file/dashboard.log 2>&1' &
      echo $! >/tmp/hermes-dashboard.pid
      chown ai_user:ai_user /tmp/hermes-dashboard.pid
      echo "[watchdog] $(date -Iseconds): dashboard restarted" >>/config-file/hermes-watchdog.log
    fi
    # Dashboard-proxy
    if [ -f /tmp/hermes-proxy.pid ] && ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null; then
      runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup node /config-file/hermes/dashboard-proxy.mjs >> /config-file/hermes-proxy.log 2>&1' &
      echo $! >/tmp/hermes-proxy.pid
      chown ai_user:ai_user /tmp/hermes-proxy.pid
      echo "[watchdog] $(date -Iseconds): dashboard-proxy restarted" >>/config-file/hermes-watchdog.log
    fi
    # agentmemory viewer-proxy (LAN access to agentmemory viewer)
    if [ -f /home/ai_user/.agentmemory/viewer-proxy.pid ] && ! kill -0 "$(cat /home/ai_user/.agentmemory/viewer-proxy.pid 2>/dev/null)" 2>/dev/null; then
      for f in /proc/[0-9]*/cmdline; do
        pid=${f%/cmdline}
        pid=${pid#/proc/}
        grep -q "viewer-proxy" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
      done
      runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'cp /config-file/aiOS-ui/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs 2>/dev/null || true'
      runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1' &
      echo $! >/home/ai_user/.agentmemory/viewer-proxy.pid
      chown ai_user:ai_user /home/ai_user/.agentmemory/viewer-proxy.pid
      echo "[watchdog] $(date -Iseconds): viewer-proxy restarted" >>/config-file/hermes-watchdog.log
    fi
    # Gateway (Telegram reconnect)
    if [ -f /home/ai_user/.hermes/gateway_state.json ]; then
      TG_STATE=$(runuser -u ai_user -- env HOME=/home/ai_user python3 -c "
import json
try:
    d = json.load(open('/home/ai_user/.hermes/gateway_state.json'))
    gw = d.get('gateway_state', '')
    tg = d.get('platforms', {}).get('telegram', {}).get('state', 'unknown')
    print(gw, tg)
except Exception as e:
    print('error')
" 2>/dev/null)
      if ! echo "$TG_STATE" | grep -q "running connected"; then
        runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'hermes gateway restart >> /config-file/gateway.log 2>&1' || true
        echo "[watchdog] $(date -Iseconds): gateway restarted (state: $TG_STATE)" >>/config-file/hermes-watchdog.log
      fi
    fi
    # hermes-webui (server.py on port 8501)
    if [ -f /tmp/hermes-subserver.pid ] && ! kill -0 "$(cat /tmp/hermes-subserver.pid 2>/dev/null)" 2>/dev/null; then
      runuser -u ai_user -- env HOME=/home/ai_user HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8501 HERMES_WEBUI_TRUST_FORWARDED_HOST=1 "$PYTHON_EXE" /aiOS-ui/features/hermes-webui/server.py >>/config-file/aiOS-ui.log 2>&1 &
      echo $! >/tmp/hermes-subserver.pid
      chown ai_user:ai_user /tmp/hermes-subserver.pid
      echo "[watchdog] $(date -Iseconds): hermes-webui restarted" >>/config-file/hermes-watchdog.log
    fi
    # headroom proxy (port 8787)
    if [ -f /tmp/headroom.pid ] && ! kill -0 "$(cat /tmp/headroom.pid 2>/dev/null)" 2>/dev/null; then
      runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup /home/ai_user/miniconda3/bin/headroom proxy >> /config-file/headroom.log 2>&1' &
      echo $! >/tmp/headroom.pid
      chown ai_user:ai_user /tmp/headroom.pid
      echo "[watchdog] $(date -Iseconds): headroom proxy restarted" >>/config-file/hermes-watchdog.log
    fi
  done
) >>/config-file/hermes-watchdog.log 2>&1 &
disown %1 2>/dev/null || true
echo "[entrypoint] watchdog started"

# ── agentmemory ───────────────────────────────────────────────────────────────

# Restore pinned iii v0.11.2 from persistent storage.
# ~/.local/bin is ephemeral (not a bind-mount) so it reverts to the image
# version (v0.16.1) on every rebuild. agentmemory v0.9.24 hard-pins v0.11.2.
if [ -f "/home/ai_user/.agentmemory/bin/iii" ]; then
  runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'cp ~/.agentmemory/bin/iii ~/.local/bin/iii && chmod +x ~/.local/bin/iii'
  echo "[entrypoint] iii v0.11.2 restored to ~/.local/bin"
fi

if [ -f /config-file/aiOS-ui/agentmemory/iii-config.yaml ]; then
  cp /config-file/aiOS-ui/agentmemory/iii-config.yaml \
    /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
  echo "[entrypoint] iii-config.yaml copied"
fi
runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'mkdir -p ~/.agentmemory/data'

# Install the patched viewer-proxy (rewrites Host header for LAN access).
if [ -f /config-file/aiOS-ui/agentmemory/viewer-proxy.mjs ]; then
  runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'cp /config-file/aiOS-ui/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs'
  echo "[entrypoint] viewer-proxy.mjs (patched) installed"
fi

# Start agentmemory if not already running.
if [ ! -f "/home/ai_user/.agentmemory/iii.pid" ] || ! kill -0 "$(cat "/home/ai_user/.agentmemory/iii.pid" 2>/dev/null)" 2>/dev/null; then
  # Comment out AGENTMEMORY_VIEWER_HOST=0.0.0.0 in .env if present (causes port 3113 EADDRINUSE conflict with viewer-proxy)
  if [ -f "/home/ai_user/.agentmemory/.env" ]; then
    sed -i 's/^AGENTMEMORY_VIEWER_HOST=0.0.0.0/# AGENTMEMORY_VIEWER_HOST=0.0.0.0/g' /home/ai_user/.agentmemory/.env
    sed -i 's/^VIEWER_ALLOWED_HOSTS=/# VIEWER_ALLOWED_HOSTS=/g' /home/ai_user/.agentmemory/.env
  fi
  runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'agentmemory start >> ~/.agentmemory/agentmemory.log 2>&1 &' || true
  echo "[entrypoint] agentmemory started"
  sleep 4
fi

# Start viewer proxy if not already running.
PROXY="/home/ai_user/.agentmemory/viewer-proxy.mjs"
PROXY_PID_FILE="/home/ai_user/.agentmemory/viewer-proxy.pid"
if [ -f "$PROXY" ]; then
  # Kill any stale viewer-proxy process holding port 3113.
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}
    pid=${pid#/proc/}
    grep -q "viewer-proxy" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  rm -f "$PROXY_PID_FILE"
  # Wait until port 3113 is released (up to 3 seconds).
  for i in 1 2 3; do
    if ! awk 'NR>1{split($2,a,":");p=strtonum("0x"a[2]);if(p==3113)print}' /proc/net/tcp 2>/dev/null | grep -q .; then
      break
    fi
    sleep 1
  done
  if [ ! -f "$PROXY_PID_FILE" ] || ! kill -0 "$(cat "$PROXY_PID_FILE" 2>/dev/null)" 2>/dev/null; then
    runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1' &
    echo $! >"$PROXY_PID_FILE"
    chown ai_user:ai_user "$PROXY_PID_FILE"
    echo "[entrypoint] viewer-proxy started (PID $!)"
  fi
fi

# ── hermes dashboard ──────────────────────────────────────────────────────────

HERMES_DASH_PID=/tmp/hermes-dashboard.pid
if [ ! -f "$HERMES_DASH_PID" ] || ! kill -0 "$(cat "$HERMES_DASH_PID" 2>/dev/null)" 2>/dev/null; then
  runuser -u ai_user -- env HOME=/home/ai_user HERMES_WEBUI_TRUST_FORWARDED_HOST=1 zsh -c 'mkdir -p ~/.hermes/logs && hermes dashboard --no-open >> /config-file/dashboard.log 2>&1' &
  echo $! >"$HERMES_DASH_PID"
  chown ai_user:ai_user "$HERMES_DASH_PID"
  echo "[entrypoint] hermes dashboard started (PID $!)"
  sleep 4
fi

HERMES_PROXY=/config-file/hermes/dashboard-proxy.mjs
HERMES_PROXY_PID=/tmp/hermes-proxy.pid
if [ -f "$HERMES_PROXY" ]; then
  # Kill any process holding the LAN IP port 9119.
  # Use SIGKILL (not TERM) so the port is released immediately.
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}
    pid=${pid#/proc/}
    grep -q "dashboard-proxy" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  rm -f "$HERMES_PROXY_PID"
  # Wait until the port is actually released (up to 5 seconds).
  for i in 1 2 3 4 5; do
    if ! awk 'NR>1{split($2,a,":");p=strtonum("0x"a[2]);if(p==9119)print}' /proc/net/tcp 2>/dev/null | grep -v "0100007F" >/dev/null; then
      break
    fi
    sleep 1
  done
  runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup node /config-file/hermes/dashboard-proxy.mjs >> /config-file/hermes-proxy.log 2>&1' &
  echo $! >"$HERMES_PROXY_PID"
  chown ai_user:ai_user "$HERMES_PROXY_PID"
  echo "[entrypoint] hermes dashboard-proxy started (PID $!)"
fi

# ── hermes gateway ────────────────────────────────────────────────────────────

GATEWAY_STATE_FILE="/home/ai_user/.hermes/gateway_state.json"
GATEWAY_PID=""
if [ -f "$GATEWAY_STATE_FILE" ]; then
  GATEWAY_PID=$(runuser -u ai_user -- env HOME=/home/ai_user python3 -c "import json; print(json.load(open('$GATEWAY_STATE_FILE')).get('pid',''))" 2>/dev/null)
fi
if [ -z "$GATEWAY_PID" ] || ! kill -0 "$GATEWAY_PID" 2>/dev/null; then
  runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup hermes gateway run >> /config-file/gateway.log 2>&1' &
  echo "[entrypoint] hermes gateway started"
  sleep 3
fi

# ── hermes-webui (server.py on port 8501) ───────────────────────────────────
HERMES_SUB_PID=/tmp/hermes-subserver.pid
if [ ! -f "$HERMES_SUB_PID" ] || ! kill -0 "$(cat "$HERMES_SUB_PID" 2>/dev/null)" 2>/dev/null; then
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}
    pid=${pid#/proc/}
    grep -q "server.py" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  rm -f "$HERMES_SUB_PID"
  runuser -u ai_user -- env HOME=/home/ai_user HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8501 HERMES_WEBUI_TRUST_FORWARDED_HOST=1 "$PYTHON_EXE" /aiOS-ui/features/hermes-webui/server.py >>/config-file/aiOS-ui.log 2>&1 &
  echo $! >"$HERMES_SUB_PID"
  chown ai_user:ai_user "$HERMES_SUB_PID"
  echo "[entrypoint] hermes-webui started (PID $!) with $PYTHON_EXE"
  sleep 3
fi

# ── headroom proxy ────────────────────────────────────────────────────────────
runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup /home/ai_user/miniconda3/bin/headroom proxy >> /config-file/headroom.log 2>&1 & echo $! >/tmp/headroom.pid'
chown ai_user:ai_user /tmp/headroom.pid
echo "[entrypoint] headroom proxy started"

# ── hand off to CMD (/bin/zsh) ────────────────────────────────────────────────
# disown all background jobs so PID 1 does not wait for them (prevents do_wait hang)
disown -a 2>/dev/null || true
exec runuser -u ai_user -- "$@"
