#!/usr/bin/env bash
# setup.sh — Install Jira CLI dependencies inside Docker
set -e

pip install --no-cache-dir requests python-dotenv

# Copy the CLI script to /workspace so scenarios can run it with `python jira_cli.py`
mkdir -p /workspace
cp /app/jira_cli.py /workspace/jira_cli.py

echo "Setup complete."
python --version
python -c "import requests, dotenv; print('requests + python-dotenv OK')"
