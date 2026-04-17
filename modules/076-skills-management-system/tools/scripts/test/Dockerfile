FROM golang:1.21-bookworm

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Git requires user identity for commits
RUN git config --global user.email "smoke-test@test.local" \
 && git config --global user.name  "Smoke Test"

# Copy project source and build (build context = tools/)
WORKDIR /app
COPY scripts/go.mod scripts/main.go ./
COPY scripts/cmd/ cmd/
COPY scripts/internal/ internal/
RUN go build -o /usr/local/bin/skills .

# Place SKILL-CLI.md where the binary expects it (exe_dir/../SKILL-CLI.md)
COPY SKILL-CLI.md /usr/local/SKILL-CLI.md

# Copy test files
COPY scripts/test/ /app/test/

# Prepare workspace directories
RUN mkdir -p /workspace

# Convert CRLF in runner script at build time
RUN sed 's/\r$//' /app/test/run-tests.sh > /usr/local/bin/run-tests.sh \
 && chmod +x /usr/local/bin/run-tests.sh

# Mount test/ as a volume — commands.md is read and rewritten in-place
ENTRYPOINT ["bash", "/usr/local/bin/run-tests.sh"]
ENV SCRIPT_DIR=/app/test
