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

# Convert CRLF in runner script at build time
RUN sed 's/\r$//' /app/test/run-tests.sh > /usr/local/bin/run-tests.sh \
 && chmod +x /usr/local/bin/run-tests.sh

# Mount test/ as a volume — commands.md is read and rewritten in-place
ENTRYPOINT ["bash", "/usr/local/bin/run-tests.sh"]
ENV SCRIPT_DIR=/app/test
