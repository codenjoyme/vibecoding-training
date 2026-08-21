FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git config --global user.email "smoke-test@test.local" \
 && git config --global user.name "Smoke Test"

WORKDIR /app
COPY pyproject.toml skills.py SKILL-CLI.md ./
COPY skills_cli/ skills_cli/
COPY test/ /app/test/

RUN chmod +x /app/test/*.sh
RUN python /app/skills.py help > /dev/null
RUN mkdir -p /workspace

ENTRYPOINT ["bash", "/app/test/run-tests.sh"]
ENV SCRIPT_DIR=/app/test
