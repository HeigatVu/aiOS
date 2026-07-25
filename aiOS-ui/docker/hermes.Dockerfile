FROM python:3.12-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY aiOS-ui/features/hermes-webui/requirements.txt /tmp/hermes-requirements.txt
RUN pip install --no-cache-dir -r /tmp/hermes-requirements.txt
COPY aiOS-ui/features/hermes-webui /app

CMD ["python", "server.py"]
