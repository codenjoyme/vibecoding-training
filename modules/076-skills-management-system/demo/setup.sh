#!/usr/bin/env bash
# setup.sh — copy demo skills-repo to work/076-task/ and git-initialize it
# Run from workspace root: bash modules/076-skills-management-system/demo/setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills-repo"

# Workspace root is 3 levels up from demo/
WORKSPACE_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
TARGET_DIR="$WORKSPACE_ROOT/work/076-task/skills-repo"

echo "→ Setting up skills-repo at: $TARGET_DIR"

if [ -d "$TARGET_DIR" ]; then
    echo ""
    echo "✋ Target already exists: $TARGET_DIR"
    echo "   Delete it first if you want to reset:"
    echo "   rm -rf '$TARGET_DIR'"
    exit 1
fi

# Ensure parent work/076-task/ exists
mkdir -p "$(dirname "$TARGET_DIR")"

# Copy demo content to target
cp -r "$SOURCE_DIR" "$TARGET_DIR"

# Initialize Git repo in target
cd "$TARGET_DIR"
git init
git config user.email "demo@skills-cli.local"
git config user.name "Skills Demo"
git config receive.denyCurrentBranch warn
git add .
git commit -m "init: demo skills repository"

echo ""
echo "✅ Done! skills-repo initialized at:"
echo "   $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  cd work/076-task"
echo "  mkdir project-alpha && cd project-alpha"
echo "  skills init --repo ../skills-repo --groups project-alpha"
