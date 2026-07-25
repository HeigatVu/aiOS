FROM node:22-bookworm AS control-web-build

WORKDIR /web
COPY aiOS-ui/apps/control-web/package.json aiOS-ui/apps/control-web/package-lock.json ./
RUN npm ci
COPY aiOS-ui/apps/control-web/ ./
RUN npm run build

FROM node:22-bookworm

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3 python3-dev python3-pip python3-venv git zsh tini curl make g++ \
    && rm -rf /var/lib/apt/lists/*

RUN npm install --global @agentmemory/agentmemory@0.9.28 @colbymchenry/codegraph@1.0.1 \
    && codegraph upgrade 1.5.0 \
    && ln -sf /root/.codegraph/versions/v1.5.0/bin/codegraph /usr/local/bin/codegraph \
    && codegraph install --target codex,hermes --location global --yes

COPY aiOS-ui/features/dashboard/requirements.txt /tmp/control-requirements.txt
RUN python3 -m pip install --break-system-packages --no-cache-dir -r /tmp/control-requirements.txt

WORKDIR /aios/aiOS-ui/features/dashboard
COPY aiOS-ui /aios/aiOS-ui
COPY --from=control-web-build /web/dist /aios/aiOS-ui/features/dashboard/static/control

ENV PYTHONPATH=/aios/aiOS-ui/features/dashboard
ENTRYPOINT ["/usr/bin/tini", "--"]
