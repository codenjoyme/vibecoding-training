#!/bin/bash
# Bash Docker Runner for DIAL Python Application
# This script builds a production Docker image and runs the DIAL query application

# Accept script name and workspace path parameters
SCRIPT_NAME="${1:-query_dial.py}"
WORKSPACE_PATH="${2:-work/180-task}"
EXTRA_PACKAGES="${3:-python-dotenv langchain langchain-openai langchain-community}"

set -e

# Function to find project root by .root marker file
find_project_root() {
    local current_path="$1"
    local max_depth=10
    local depth=0
    
    while [ $depth -lt $max_depth ]; do
        if [ -f "${current_path}/.root" ]; then
            echo "${current_path}"
            return 0
        fi
        
        local parent_path="$(dirname "${current_path}")"
        if [ "${parent_path}" = "${current_path}" ] || [ "${parent_path}" = "/" ]; then
            break
        fi
        
        current_path="${parent_path}"
        depth=$((depth + 1))
    done
    
    echo "Error: Could not find project root (.root file not found). Are you in the right directory?" >&2
    exit 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="dial-python-app"
CONTAINER_NAME="dial-app-container"

# Convert path for Docker on Windows (Git Bash)
# /c/Users/... → C:/Users/...
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    SCRIPT_DIR_DOCKER="$(cygpath -w "$SCRIPT_DIR" | sed 's|\\|/|g')"
else
    SCRIPT_DIR_DOCKER="$SCRIPT_DIR"
fi

# Find project root and resolve workspace path
PROJECT_ROOT="$(find_project_root "${SCRIPT_DIR}")"
WORKSPACE_DIR="${PROJECT_ROOT}/${WORKSPACE_PATH}"

mkdir -p "${WORKSPACE_DIR}"
WORKSPACE_DIR="$(cd "${WORKSPACE_DIR}" && pwd)"

cd "$SCRIPT_DIR"

echo ""
echo "============================================="
echo "DIAL Python Docker Application"
echo "============================================="
echo ""
echo "Script to run: $SCRIPT_NAME"
echo "Workspace: $WORKSPACE_DIR"
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

# Copy files to workspace
echo "Preparing workspace..."

# Copy all .py files if they don't exist in workspace
for pyfile in "${SCRIPT_DIR}"/*.py; do
    if [ -f "$pyfile" ]; then
        filename=$(basename "$pyfile")
        if [ ! -f "${WORKSPACE_DIR}/${filename}" ]; then
            cp "$pyfile" "${WORKSPACE_DIR}/"
            echo "  Copied: $filename"
        fi
    fi
done

# Copy .env.example if .env doesn't exist
ENV_EXAMPLE="${SCRIPT_DIR}/.env.example"
ENV_TARGET="${WORKSPACE_DIR}/.env"
if [ -f "$ENV_EXAMPLE" ] && [ ! -f "$ENV_TARGET" ]; then
    cp "$ENV_EXAMPLE" "$ENV_TARGET"
    echo "  Created .env from template"
fi

# Copy Dockerfile to workspace
cp "${SCRIPT_DIR}/install-python-docker.dockerfile" "${WORKSPACE_DIR}/Dockerfile"
echo "  Copied: Dockerfile"

echo ""

# Clean up any existing container
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Cleaning up existing container..."
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
fi

# Build Docker image
echo "Building Docker image with full Python environment..."
if [ -n "$EXTRA_PACKAGES" ]; then
    echo "Extra packages: $EXTRA_PACKAGES"
fi
echo ""

cd "${WORKSPACE_DIR}"

BUILD_ARGS=(
    "-f" "Dockerfile"
    "--build-arg" "SCRIPT_NAME=$SCRIPT_NAME"
)

if [ -n "$EXTRA_PACKAGES" ]; then
    BUILD_ARGS+=("--build-arg" "EXTRA_PACKAGES=$EXTRA_PACKAGES")
fi

BUILD_ARGS+=("-t" "$IMAGE_NAME" ".")

docker build "${BUILD_ARGS[@]}"

cd "${SCRIPT_DIR}"

echo ""
echo "============================================="
echo "Running DIAL application in Docker..."
echo "============================================="
echo ""

# Run the container with workspace directory mounted
docker run --rm \
    --name "$CONTAINER_NAME" \
    --add-host "host.docker.internal:host-gateway" \
    -v "${WORKSPACE_DIR}:/workspace" \
    -it \
    "$IMAGE_NAME" \
    bash -c "python $SCRIPT_NAME"

echo ""
echo "============================================="
echo "Application completed!"
echo "============================================="
echo ""
