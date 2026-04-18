#!/usr/bin/env bash
# setup.sh — Install Python CLI tools for testing
set -e

# Install httpie — a user-friendly HTTP CLI client
pip install --no-cache-dir httpie

# Verify installation
echo "Setup complete. http installed at: $(command -v http)"
