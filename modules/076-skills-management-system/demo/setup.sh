#!/usr/bin/env bash
# setup.sh — initialize demo/skills-repo as a Git repository
# Run once before using the demo with the skills CLI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR/skills-repo"

echo "→ Initializing demo skills-repo ..."

cd "$REPO_DIR"
git init
git config user.email "demo@skills-cli.local"
git config user.name "Skills Demo"
git config receive.denyCurrentBranch warn
git add .
git commit -m "init: demo skills repository"

echo ""
echo "✅ Demo skills-repo initialized at $REPO_DIR"
echo ""
echo "Next: create a project workspace and run:"
echo "  skills init --repo \"$REPO_DIR\" --groups project-alpha"
