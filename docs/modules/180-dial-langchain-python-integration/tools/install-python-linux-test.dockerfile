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

# Create working directory
WORKDIR /workspace

# Note: Files are mounted from host at runtime via docker run -v
# This allows editing files on host without rebuilding the image

# Default command: run the installation script
CMD ["bash", "-c", "dos2unix install-python-linux.sh 2>/dev/null; chmod +x install-python-linux.sh; echo '=== Starting installation test ===' && ./install-python-linux.sh && echo '=== Installation completed ===' && echo '' && echo '=== Testing query_dial.py ===' && ./.venv/bin/python query_dial.py"]
