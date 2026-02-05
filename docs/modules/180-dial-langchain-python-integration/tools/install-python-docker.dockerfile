# Full DIAL Python Environment Docker Image
# This Dockerfile creates a complete Python environment with langchain and DIAL integration
FROM ubuntu:22.04

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

# Step 3: Copy application files
COPY .env .
COPY *.py .

# Step 4: Create virtual environment
RUN python3 -m venv .venv

# Step 5: Upgrade pip in virtual environment
RUN .venv/bin/python -m pip install --upgrade pip

# Step 6: Install langchain dependencies
RUN .venv/bin/pip install python-dotenv && \
    .venv/bin/pip install langchain && \
    .venv/bin/pip install langchain-openai && \
    .venv/bin/pip install langchain-community

# Step 7: Verify installation
RUN .venv/bin/pip list

# Set environment to use virtual environment by default
ENV PATH="/app/.venv/bin:$PATH"

# Default command: run query_dial.py
CMD ["python", "query_dial.py"]
