FROM fedora:44

# 1. Update OS and install all system-level tools & extensions
RUN dnf upgrade --refresh -y && \
  dnf install -y \
  nodejs npm \
  git curl wget tar unzip sudo neovim zsh util-linux \
  gcc gcc-c++ make \
  lsd tealdeer fzf \
  autojump-zsh jq lsof \
  gtk3 alsa-lib dbus-libs \
  && dnf clean all

# the ENV PATH line
ENV AGENTMEMORY_III_VERSION=0.11.2

# 3. Setup the isolated user
ARG USER_ID=2000
ARG GROUP_ID=2000
ARG USERNAME=ai_user

RUN groupadd -g ${GROUP_ID} ${USERNAME} && \
  useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/zsh ${USERNAME}

# 4. Copy entrypoint (as root, before switching user)
COPY ./config-file/system-config/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 5. Switch to user to ensure AI agents install securely in user-space
USER ${USERNAME}
WORKDIR /workspace

# Configure NPM global prefix to user-space
ENV NPM_CONFIG_PREFIX=/home/${USERNAME}/.npm-global

# 6. Pre-create all directories that will be bind-mounted
#    This ensures correct ownership even if Docker creates host dirs as root
RUN mkdir -p \
  /home/${USERNAME}/.cache/uv \
  /home/${USERNAME}/miniconda3/pkgs \
  /home/${USERNAME}/.agentmemory \
  /home/${USERNAME}/.hermes \
  /home/${USERNAME}/.mimocode \
  /home/${USERNAME}/.agents \
  /home/${USERNAME}/.iii \
  /home/${USERNAME}/.npm-global \
  /home/${USERNAME}/.reasonix

# Install global NPM packages inside user-space
RUN npm install -g @agentmemory/agentmemory reasonix

# 7. Install Environment Managers (uv & Conda)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN mkdir -p /home/${USERNAME}/miniconda3 && \
  curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh && \
  bash miniconda.sh -b -u -p /home/${USERNAME}/miniconda3 && \
  rm miniconda.sh

# 8. Prepare environment files (Do NOT bake the heavy ML environment here)
COPY --chown=${USERNAME}:${GROUP_ID} environment.yml /home/${USERNAME}/environment.yml
RUN /home/${USERNAME}/miniconda3/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
  /home/${USERNAME}/miniconda3/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# 9. Update PATH so the terminal can find installed agents and Conda
ENV PATH="/home/${USERNAME}/.npm-global/bin:/home/${USERNAME}/.local/bin:/home/${USERNAME}/miniconda3/bin:${PATH}"

# 10. Install Zinit & Powerlevel10k via direct Git clone (Failsafe method)
RUN git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /home/${USERNAME}/powerlevel10k
RUN mkdir -p /home/${USERNAME}/.local/share/zinit && \
  git clone https://github.com/zdharma-continuum/zinit.git /home/${USERNAME}/.local/share/zinit/zinit.git

# 11. Install your requested AI Agents
RUN npm install -g @mimo-ai/cli
RUN curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
RUN curl -fsSL https://chatgpt.com/codex/install.sh | sh
RUN curl -fsSL https://raw.githubusercontent.com/Bande-a-Bonnot/Boucle-framework/main/tools/read-once/install.sh | bash
RUN curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
RUN curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
RUN pip install "headroom-ai[all]"
RUN uv tool install graphifyy

USER root

# Default entrypoint fixes bind-mount permissions, then runs CMD
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/zsh"]
