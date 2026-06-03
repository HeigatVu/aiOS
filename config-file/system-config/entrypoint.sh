#!/bin/bash
set +e
# NOTE: set +e (not -e). With set -e, bash on PID 1 can hang at do_wait
# when background jobs exit before exec, never reaching exec or the watchdog.
# Explicit error handling is used where needed.

# ── system init ───────────────────────────────────────────────────────────────

# Fix ownership of bind-mounted directories (Docker may create them as root).
DIRS=(
  "$HOME/.cache/uv"
  "$HOME/miniconda3/envs/ai-baseline"
  "$HOME/miniconda3/pkgs"
  "$HOME/.agentmemory"
  "$HOME/.claude"
  "$HOME/.hermes"
  "$HOME/.gemini"
  "$HOME/.agents"
  "$HOME/.fcc"
  "$HOME/.iii"
  "$HOME/.feynman"
)
for dir in "${DIRS[@]}"; do
  if [ -d "$dir" ] && [ ! -w "$dir" ]; then
    sudo chown -R "$(id -u):$(id -g)" "$dir"
  fi
done

# Build the Conda ai-baseline env on first launch if the bind-mount is empty.
ENV_DIR="$HOME/miniconda3/envs/ai-baseline"
if [ ! -f "$ENV_DIR/conda-meta/history" ]; then
  echo "[entrypoint] Building Conda env 'ai-baseline' (first launch — this is slow)..."
  "$HOME/miniconda3/bin/conda" env create -f "$HOME/environment.yml" -p "$ENV_DIR" ||
    echo "[entrypoint] WARNING: conda env create failed — continuing without it."
fi

# ── watchdog (starts FIRST so it survives even if later sections hang) ──────────
# Covers: dashboard, proxy, viewer-proxy, fcc-server, gateway
# Runs in background. Uses set +e internally to never die from transient errors.
# disown prevents PID 1 from waiting for this infinite-loop process.
(
  set +e
  while true; do
    sleep 60
    # Dashboard
    if [ -f /tmp/hermes-dashboard.pid ] && ! kill -0 "$(cat /tmp/hermes-dashboard.pid 2>/dev/null)" 2>/dev/null; then
      mkdir -p "$HOME/.hermes/logs"
      hermes dashboard --no-open >>"$HOME/.hermes/logs/dashboard.log" 2>&1 &
      echo $! >/tmp/hermes-dashboard.pid
      echo "[watchdog] $(date -Iseconds): dashboard restarted" >>/tmp/hermes-watchdog.log
    fi
    # Dashboard-proxy
    if [ -f /tmp/hermes-proxy.pid ] && ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null; then
      nohup node /config-file/hermes/dashboard-proxy.mjs >>/tmp/hermes-proxy.log 2>&1 &
      echo $! >/tmp/hermes-proxy.pid
      echo "[watchdog] $(date -Iseconds): dashboard-proxy restarted" >>/tmp/hermes-watchdog.log
    fi
    # agentmemory viewer-proxy (LAN access to agentmemory viewer)
    if [ -f "$HOME/.agentmemory/viewer-proxy.pid" ] && ! kill -0 "$(cat "$HOME/.agentmemory/viewer-proxy.pid" 2>/dev/null)" 2>/dev/null; then
      cp /config-file/agentmemory/viewer-proxy.mjs "$HOME/.agentmemory/viewer-proxy.mjs" 2>/dev/null || true
      nohup node "$HOME/.agentmemory/viewer-proxy.mjs" >>"$HOME/.agentmemory/viewer-proxy.log" 2>&1 &
      echo $! >"$HOME/.agentmemory/viewer-proxy.pid"
      echo "[watchdog] $(date -Iseconds): viewer-proxy restarted" >>/tmp/hermes-watchdog.log
    fi
    # fcc-server
    if [ -f /tmp/fcc-server.pid ] && ! kill -0 "$(cat /tmp/fcc-server.pid 2>/dev/null)" 2>/dev/null; then
      nohup fcc-server >>"$HOME/.fcc/logs/fcc-server.log" 2>&1 &
      echo $! >/tmp/fcc-server.pid
      echo "[watchdog] $(date -Iseconds): fcc-server restarted" >>/tmp/hermes-watchdog.log
    fi
    # Gateway (Telegram reconnect)
    if [ -f "$HOME/.hermes/gateway_state.json" ]; then
      TG_STATE=$(python3 -c "
import json
try:
    d = json.load(open('$HOME/.hermes/gateway_state.json'))
    gw = d.get('gateway_state', '')
    tg = d.get('platforms', {}).get('telegram', {}).get('state', 'unknown')
    print(gw, tg)
except Exception as e:
    print('error')
" 2>/dev/null)
      if ! echo "$TG_STATE" | grep -q "running connected"; then
        hermes gateway restart >>"$HOME/.hermes/logs/gateway.log" 2>&1 || true
        echo "[watchdog] $(date -Iseconds): gateway restarted (state: $TG_STATE)" >>/tmp/hermes-watchdog.log
      fi
    fi
    # aiOS-ui (FastAPI on port 8501)
    if [ -f /tmp/aiOS-ui.pid ] && ! kill -0 "$(cat /tmp/aiOS-ui.pid 2>/dev/null)" 2>/dev/null; then
      (cd /aiOS-ui && exec python main.py) >>/tmp/aiOS-ui.log 2>&1 &
      echo $! > /tmp/aiOS-ui.pid
      echo "[watchdog] $(date -Iseconds): aiOS-ui restarted" >>/tmp/hermes-watchdog.log
    fi
  done
) >>/tmp/hermes-watchdog.log 2>&1 &
disown %1 2>/dev/null || true
echo "[entrypoint] watchdog started"

# ── agentmemory ───────────────────────────────────────────────────────────────

# Restore pinned iii v0.11.2 from persistent storage.
# ~/.local/bin is ephemeral (not a bind-mount) so it reverts to the image
# version (v0.16.1) on every rebuild. agentmemory v0.9.24 hard-pins v0.11.2.
if [ -f "$HOME/.agentmemory/bin/iii" ]; then
  cp "$HOME/.agentmemory/bin/iii" "$HOME/.local/bin/iii"
  chmod +x "$HOME/.local/bin/iii"
  echo "[entrypoint] iii v0.11.2 restored to ~/.local/bin"
fi

if [ -f /config-file/agentmemory/iii-config.yaml ]; then
  sudo cp /config-file/agentmemory/iii-config.yaml \
    /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
  echo "[entrypoint] iii-config.yaml copied"
fi
mkdir -p "$HOME/.agentmemory/data"

# Install the patched viewer-proxy (rewrites Host header for LAN access).
if [ -f /config-file/agentmemory/viewer-proxy.mjs ]; then
  cp /config-file/agentmemory/viewer-proxy.mjs "$HOME/.agentmemory/viewer-proxy.mjs"
  echo "[entrypoint] viewer-proxy.mjs (patched) installed"
fi

# Start agentmemory if not already running.
if [ ! -f "$HOME/.agentmemory/iii.pid" ] || ! kill -0 "$(cat "$HOME/.agentmemory/iii.pid" 2>/dev/null)" 2>/dev/null; then
  agentmemory start >>"$HOME/.agentmemory/agentmemory.log" 2>&1 || true
  echo "[entrypoint] agentmemory started"
  sleep 4
fi

# Start viewer proxy if not already running.
PROXY="$HOME/.agentmemory/viewer-proxy.mjs"
PROXY_PID_FILE="$HOME/.agentmemory/viewer-proxy.pid"
if [ -f "$PROXY" ]; then
  if [ ! -f "$PROXY_PID_FILE" ] || ! kill -0 "$(cat "$PROXY_PID_FILE" 2>/dev/null)" 2>/dev/null; then
    nohup node "$PROXY" >>"$HOME/.agentmemory/viewer-proxy.log" 2>&1 &
    echo $! >"$PROXY_PID_FILE"
    echo "[entrypoint] viewer-proxy started (PID $!)"
  fi
fi

# ── hermes dashboard ──────────────────────────────────────────────────────────

HERMES_DASH_PID=/tmp/hermes-dashboard.pid
if [ ! -f "$HERMES_DASH_PID" ] || ! kill -0 "$(cat "$HERMES_DASH_PID" 2>/dev/null)" 2>/dev/null; then
  mkdir -p "$HOME/.hermes/logs"
  hermes dashboard --no-open >>"$HOME/.hermes/logs/dashboard.log" 2>&1 &
  echo $! >"$HERMES_DASH_PID"
  echo "[entrypoint] hermes dashboard started (PID $!)"
  sleep 4
fi

HERMES_PROXY=/config-file/hermes/dashboard-proxy.mjs
HERMES_PROXY_PID=/tmp/hermes-proxy.pid
if [ -f "$HERMES_PROXY" ]; then
  # Kill any process holding the LAN IP port 9119.
  # Use SIGKILL (not TERM) so the port is released immediately.
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}; pid=${pid#/proc/}
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
  nohup node "$HERMES_PROXY" >>/tmp/hermes-proxy.log 2>&1 &
  echo $! >"$HERMES_PROXY_PID"
  echo "[entrypoint] hermes dashboard-proxy started (PID $!)"
fi

# ── fcc-server ────────────────────────────────────────────────────────────────

if [ -f /config-file/fcc/.env ]; then
  cp /config-file/fcc/.env "$HOME/.fcc/.env"
  echo "[entrypoint] fcc-server .env copied"
fi
mkdir -p "$HOME/.fcc/logs"

FCC_PID_FILE=/tmp/fcc-server.pid
if [ ! -f "$FCC_PID_FILE" ] || ! kill -0 "$(cat "$FCC_PID_FILE" 2>/dev/null)" 2>/dev/null; then
  # Kill any stale fcc-server process holding port 8082.
  # Use SIGKILL for immediate port release.
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}; pid=${pid#/proc/}
    grep -q "fcc-server" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  rm -f "$FCC_PID_FILE"
  # Wait until port 8082 is released (up to 3 seconds).
  for i in 1 2 3; do
    if ! awk 'NR>1{split($2,a,":");p=strtonum("0x"a[2]);if(p==8082)print}' /proc/net/tcp 2>/dev/null | grep -q .; then
      break
    fi
    sleep 1
  done
  nohup fcc-server >>"$HOME/.fcc/logs/fcc-server.log" 2>&1 &
  echo $! >"$FCC_PID_FILE"
  echo "[entrypoint] fcc-server started (PID $!)"
  sleep 2
fi

# ── hermes gateway ────────────────────────────────────────────────────────────

GATEWAY_STATE_FILE="$HOME/.hermes/gateway_state.json"
GATEWAY_PID=""
if [ -f "$GATEWAY_STATE_FILE" ]; then
  GATEWAY_PID=$(python3 -c "import json; print(json.load(open('$GATEWAY_STATE_FILE')).get('pid',''))" 2>/dev/null)
fi
if [ -z "$GATEWAY_PID" ] || ! kill -0 "$GATEWAY_PID" 2>/dev/null; then
  nohup hermes gateway run >>"$HOME/.hermes/logs/gateway.log" 2>&1 &
  echo "[entrypoint] hermes gateway started"
  sleep 3
fi

# ── aiOS-ui (FastAPI on port 8501) ────────────────────────────────────────
AIOS_UI_PID=/tmp/aiOS-ui.pid
if [ ! -f "$AIOS_UI_PID" ] || ! kill -0 "$(cat "$AIOS_UI_PID" 2>/dev/null)" 2>/dev/null; then
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}; pid=${pid#/proc/}
    grep -q "main.py" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  rm -f "$AIOS_UI_PID"
  (cd /aiOS-ui && exec python main.py) >>/tmp/aiOS-ui.log 2>&1 &
  echo $! > "$AIOS_UI_PID"
  echo "[entrypoint] aiOS-ui started (PID $!)"
  sleep 3
fi

# ── hand off to CMD (/bin/zsh) ────────────────────────────────────────────────
# disown all background jobs so PID 1 does not wait for them (prevents do_wait hang)
disown -a 2>/dev/null || true
exec "$@"
