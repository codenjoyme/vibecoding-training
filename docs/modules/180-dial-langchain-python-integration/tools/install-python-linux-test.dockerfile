# Dockerfile for testing DIAL Python installation script on clean Linux
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Create project structure to emulate real Linux system
RUN mkdir -p /project/docs/modules/180-dial-langchain-python-integration/tools && \
    mkdir -p /project/work && \
    touch /project/.root

# Set working directory to tools (where user would run the script)
WORKDIR /project/docs/modules/180-dial-langchain-python-integration/tools

# Copy installation script and Python files from build context
COPY install-python-linux.sh .
COPY *.py .
COPY .env* .

# Fix line endings and permissions
RUN dos2unix install-python-linux.sh 2>/dev/null || true && \
    chmod +x install-python-linux.sh && \
    if [ -f .env.example ] && [ ! -f .env ]; then cp .env.example .env; fi

# Default command: run the installation script and test
CMD ["bash", "-c", "echo '=== Starting installation test ===' && ./install-python-linux.sh && echo '' && echo '=== Installation completed ===' && echo '' && echo '=== Checking workspace ===' && ls -la /project/work/python-ai-workspace/ && echo '' && echo '=== Testing query_dial.py ===' && cd /project/work/python-ai-workspace && source .venv/bin/activate && python query_dial.py"]
