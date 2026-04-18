#!/usr/bin/env bash
# setup.sh — Install a simple Node.js CLI tool for testing
set -e

# Install the 'cowsay' npm package globally as our demo CLI
npm install -g cowsay

# Verify installation
echo "Setup complete. cowsay installed at: $(command -v cowsay)"
