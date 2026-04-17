FROM node:20-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Git requires user identity for commits
RUN git config --global user.email "smoke-test@test.local" \
 && git config --global user.name  "Smoke Test"

# Copy project source
WORKDIR /app
COPY package.json tsconfig.json SKILL-CLI.md ./
COPY src/ src/
RUN npm install && npm run build

# Copy test files
COPY test/ /app/test/

# Prepare workspace directories
RUN mkdir -p /workspace

# Mount test/ as a volume — commands.md is read and rewritten in-place
ENTRYPOINT ["bash", "-c", "sed 's/\\r$//' /app/test/run-tests.sh > /tmp/run.sh && SCRIPT_DIR=/app/test bash /tmp/run.sh"]
