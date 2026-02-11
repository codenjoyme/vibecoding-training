# Full DIAL Python Environment Docker Image
# This Dockerfile creates a complete Python environment with langchain and DIAL integration
FROM ubuntu:22.04

# Accept script name as build argument (default: query_dial.py)
ARG SCRIPT_NAME=query_dial.py

# Accept packages to install (default: langchain stack)
ARG EXTRA_PACKAGES="python-dotenv langchain langchain-openai langchain-community"

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

# Step 5: Install packages (langchain by default, or custom)
ARG EXTRA_PACKAGES
RUN if [ -n "$EXTRA_PACKAGES" ]; then \
        echo "Installing packages: $EXTRA_PACKAGES" && \
        .venv/bin/pip install $EXTRA_PACKAGES; \
    fi

# Step 6: Verify installation
RUN .venv/bin/pip list

# Set environment to use virtual environment by default
ENV PATH="/app/.venv/bin:$PATH"

# Save SCRIPT_NAME as environment variable for runtime
ARG SCRIPT_NAME
ENV SCRIPT_NAME=${SCRIPT_NAME}

# Working directory for scripts (will be workspace root when building)
WORKDIR /workspace

# Copy all Python scripts from current directory (workspace)
COPY *.py ./

# Copy .env if exists (created by host script, optional)
COPY .env* ./

# Default command: run script
CMD ["bash", "-c", "python ${SCRIPT_NAME}"]
