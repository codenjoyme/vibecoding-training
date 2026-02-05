#!/bin/bash
# Bash Docker Runner for DIAL Python Application
# This script builds a production Docker image and runs the DIAL query application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="dial-python-app"
CONTAINER_NAME="dial-app-container"

cd "$SCRIPT_DIR"

echo ""
echo "============================================="
echo "DIAL Python Docker Application"
echo "============================================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed!"
    echo ""
    echo "Please install Docker first:"
    echo "  Ubuntu/Debian: sudo apt install docker.io"
    echo "  macOS: brew install --cask docker"
    echo "  Or visit: https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi

DOCKER_VERSION=$(docker --version)
echo "Docker found: $DOCKER_VERSION"
echo ""

# Clean up any existing container
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Cleaning up existing container..."
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
fi

# Build Docker image
echo "Building Docker image with full Python environment..."
echo ""
docker build -f install-python-docker.dockerfile -t "$IMAGE_NAME" .

echo ""
echo "============================================="
echo "Running DIAL application in Docker..."
echo "============================================="
echo ""

# Run the container with host network bridge
docker run --rm \
    --name "$CONTAINER_NAME" \
    --add-host "host.docker.internal:host-gateway" \
    -it \
    "$IMAGE_NAME"

echo ""
echo "============================================="
echo "Application completed!"
echo "============================================="
echo ""
