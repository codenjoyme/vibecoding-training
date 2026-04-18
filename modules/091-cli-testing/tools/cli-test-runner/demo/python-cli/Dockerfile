FROM python:3.12-slim

# Install common utilities
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Git requires user identity
RUN git config --global user.email "test@test.local" \
 && git config --global user.name "Snapshot Test"

# Copy and run custom setup
COPY setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh && /app/setup.sh

# Copy the universal runner script
COPY run-scenarios.sh /app/run-scenarios.sh
RUN chmod +x /app/run-scenarios.sh

# Copy scenario files
COPY scenarios/ /app/scenarios/

# Prepare workspace
RUN mkdir -p /workspace

ENTRYPOINT ["bash", "-c", "sed 's/\\r$//' /app/run-scenarios.sh > /tmp/run.sh && bash /tmp/run.sh \"$@\"", "--"]
