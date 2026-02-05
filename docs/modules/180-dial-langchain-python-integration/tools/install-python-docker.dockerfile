# Full DIAL Python Environment Docker Image
# This Dockerfile creates a complete Python environment with langchain and DIAL integration
FROM ubuntu:22.04

# Accept script name as build argument (default: query_dial.py)
ARG SCRIPT_NAME=query_dial.py

# Accept extra packages to install (e.g., "faiss-cpu numpy")
ARG EXTRA_PACKAGES=""

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Step 1: Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Step 2: Create working directory
WORKDIR /app

# Step 3: Create virtual environment
RUN python3 -m venv .venv

# Step 4: Upgrade pip in virtual environment
RUN .venv/bin/python -m pip install --upgrade pip

# Step 5: Install langchain dependencies (heavy operations, cached)
RUN .venv/bin/pip install python-dotenv && \
    .venv/bin/pip install langchain && \
    .venv/bin/pip install langchain-openai && \
    .venv/bin/pip install langchain-community

# Step 6: Install extra packages if specified (e.g., faiss-cpu for RAG)
ARG EXTRA_PACKAGES
RUN if [ -n "$EXTRA_PACKAGES" ]; then \
        echo "Installing extra packages: $EXTRA_PACKAGES" && \
        .venv/bin/pip install $EXTRA_PACKAGES; \
    fi

# Step 7: Verify installation
RUN .venv/bin/pip list

# Set environment to use virtual environment by default
ENV PATH="/app/.venv/bin:$PATH"

# Working directory for mounted scripts
WORKDIR /workspace

# Default command: create .env if needed, then run script
CMD ["bash", "-c", "if [ -f .env.example ] && [ ! -f .env ]; then cp .env.example .env; fi && python query_dial.py"]
