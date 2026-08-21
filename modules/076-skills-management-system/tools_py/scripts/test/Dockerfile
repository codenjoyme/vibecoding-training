FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "smoke-test@test.local" \
 && git config --global user.name "Smoke Test"

WORKDIR /app
COPY pyproject.toml SKILL-CLI.md ./
COPY scripts/ scripts/
COPY scripts/test/ /app/test/

RUN chmod +x /app/test/*.sh
RUN printf '#!/bin/sh\nexec python /app/scripts/main.py "$@"\n' > /usr/local/bin/skills \
 && chmod +x /usr/local/bin/skills
RUN skills help > /dev/null
RUN mkdir -p /workspace

ENTRYPOINT ["bash", "/app/test/run-tests.sh"]
ENV SCRIPT_DIR=/app/test
