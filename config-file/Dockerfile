# Dockerfile — AI Dev Container
# Multi-service environment: agentmemory, hermes, fcc-server, camofox browser.
# agy/Gemini, Claude Code, and ECC all available.

FROM debian:bookworm-slim

# ── System packages ────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git wget unzip xz-utils \
    python3 python3-pip python3-venv \
    nodejs npm \
    zsh sudo procps \
    # Firefox/Camoufox deps (for browser automation)
    libgtk-3-0 libdbus-glib-1-2 libxt6 libasound2 \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    libegl1-mesa libgl1-mesa-dri libgbm1 xvfb \
    fonts-liberation fontconfig \
    && rm -rf /var/lib/apt/lists/*

# ── User setup ─────────────────────────────────────────────────────────────────
RUN useradd -m -s /bin/zsh ai_user && \
    echo "ai_user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER ai_user
WORKDIR /home/ai_user
ENV HOME=/home/ai_user
ENV PATH="${HOME}/.local/bin:${HOME}/miniconda3/bin:${PATH}"

# ── Conda + ai-baseline env ────────────────────────────────────────────────────
# Pre-installed into image; bind mount preserves envs/ and pkgs/ across rebuilds
COPY --chown=ai_user:ai_user environment.yml /tmp/environment.yml
RUN curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
        -o /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p ${HOME}/miniconda3 && \
    rm /tmp/miniconda.sh && \
    ${HOME}/miniconda3/bin/conda env create -f /tmp/environment.yml -p ${HOME}/miniconda3/envs/ai-baseline || true

# ── npm global packages ────────────────────────────────────────────────────────
RUN npm install -g \
    @agentmemory/agentmemory \
    @agentmemory/mcp \
    @anthropic-ai/claude-code \
    && rm -rf /tmp/*

# ── iii engine (v0.11.2, pinned for agentmemory compatibility) ──────────────────
RUN mkdir -p ${HOME}/.agentmemory/bin && \
    curl -fsSL -o /tmp/iii.tar.gz \
        https://github.com/iii-hq/iii/releases/download/iii/v0.11.2/iii-x86_64-unknown-linux-gnu.tar.gz && \
    tar -xzf /tmp/iii.tar.gz -C ${HOME}/.agentmemory/bin && \
    chmod +x ${HOME}/.agentmemory/bin/iii && \
    cp ${HOME}/.agentmemory/bin/iii ${HOME}/.local/bin/iii && \
    rm /tmp/iii.tar.gz

# ── agy/Gemini (pre-baked for immediate use) ────────────────────────────────────
# Installed to ~/.local/bin which IS bind-mounted, so it survives rebuilds
RUN curl -fsSL -o ${HOME}/.local/bin/agy \
        https://github.com/antigravity/antigravity-cli/releases/latest/download/agy-linux-x86_64 && \
    chmod +x ${HOME}/.local/bin/agy

# ── rtk (Rust Token Killer — token-compact CLI proxy) ───────────────────────────
RUN curl -fsSL https://github.com/reachingforthejack/rtk/releases/latest/download/rtk-linux-x86_64 \
        -o ${HOME}/.local/bin/rtk && \
    chmod +x ${HOME}/.local/bin/rtk

# ── codegraph ──────────────────────────────────────────────────────────────────
RUN npm install -g @codegraph/cli

# ── Copy config and entrypoint ──────────────────────────────────────────────────
COPY --chown=ai_user:ai_user config-file/system-config/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY --chown=ai_user:ai_user config-file/agentmemory/iii-config.yaml /config-file/agentmemory/iii-config.yaml
COPY --chown=ai_user:ai_user config-file/agentmemory/viewer-proxy.mjs /config-file/agentmemory/viewer-proxy.mjs
COPY --chown=ai_user:ai_user config-file/hermes/dashboard-proxy.mjs /config-file/hermes/dashboard-proxy.mjs
COPY --chown=ai_user:ai_user config-file/fcc/.env /config-file/fcc/.env

# ── Camofox browser ─────────────────────────────────────────────────────────────
# Pre-baked into image; uses pinned version for reproducible builds
ARG CAMOUFOX_VERSION=135.0.1
ARG CAMOUFOX_RELEASE=beta.24
RUN mkdir -p /home/ai_user/.cache/camoufox && \
    curl -fsSL -o /tmp/camoufox.zip \
        "https://github.com/daijro/camoufox/releases/download/v${CAMOUFOX_VERSION}+${CAMOUFOX_RELEASE}/camoufox-${CAMOUFOX_VERSION}-x86_64.zip" && \
    unzip -q /tmp/camoufox.zip -d /home/ai_user/.cache/camoufox || true && \
    chmod -R 755 /home/ai_user/.cache/camoufox && \
    rm /tmp/camoufox.zip

# ── Entrypoint ──────────────────────────────────────────────────────────────────
ENTRYPOINT ["/bin/bash", "/usr/local/bin/entrypoint.sh"]
CMD ["/bin/zsh"]
