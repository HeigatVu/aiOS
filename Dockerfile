FROM fedora:44

# 1. Update OS and install all system-level tools & extensions
RUN dnf upgrade --refresh -y && \
  dnf install -y \
  nodejs npm \
  git curl wget tar unzip sudo neovim zsh util-linux \
  gcc gcc-c++ make \
  lsd tealdeer fzf \
  autojump-zsh \
  && dnf clean all
  
# 2. Install global NPM packages
RUN npm install -g @agentmemory/agentmemory

# 3. Setup the isolated user
ARG USER_ID=1001
ARG GROUP_ID=1001
ARG USERNAME=ai_user

RUN groupadd -g ${GROUP_ID} ${USERNAME} && \
  useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/zsh ${USERNAME} && \
  echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}

# 4. Copy entrypoint (as root, before switching user)
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# 5. Switch to user to ensure AI agents install securely in user-space
USER ${USERNAME}
WORKDIR /workspace

# 6. Pre-create all directories that will be bind-mounted
#    This ensures correct ownership even if Docker creates host dirs as root
RUN mkdir -p \
  /home/${USERNAME}/.cache/uv \
  /home/${USERNAME}/miniconda3/pkgs \
  /home/${USERNAME}/.agentmemory \
  /home/${USERNAME}/.claude \
  /home/${USERNAME}/.hermes \
  /home/${USERNAME}/.gemini \
  /home/${USERNAME}/.agents \
  /home/${USERNAME}/.fcc \
  /home/${USERNAME}/.iii \
  /home/${USERNAME}/.feynman

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
ENV PATH="/home/${USERNAME}/.local/bin:/home/${USERNAME}/miniconda3/bin:${PATH}"

# 10. Install Zinit & Powerlevel10k via direct Git clone (Failsafe method)
RUN git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /home/${USERNAME}/powerlevel10k
RUN mkdir -p /home/${USERNAME}/.local/share/zinit && \
  git clone https://github.com/zdharma-continuum/zinit.git /home/${USERNAME}/.local/share/zinit/zinit.git

# 11. Install your requested AI Agents
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash
RUN curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
RUN curl -fsSL https://claude.ai/install.sh | bash
RUN curl -fsSL "https://github.com/Alishahryar1/free-claude-code/blob/main/scripts/install.sh?raw=1" | sh
RUN curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
RUN curl -fsSL https://feynman.is/install | bash

# --- AI SIDECAR AUTO-INSTALLS ---
# (Sidecar UI injects new RUN layers directly under this marker. Do not remove.)

# Default entrypoint fixes bind-mount permissions, then runs CMD
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/zsh"]
