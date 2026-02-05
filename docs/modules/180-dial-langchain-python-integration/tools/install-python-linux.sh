#!/bin/bash
# Simple Python Environment Setup for DIAL Integration
# This script installs system Python, creates virtual environment, and installs dependencies

set -e

# Install everything in the tools directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS_DIR="${INSTALL_DIR}/.tools"
VENV_DIR="${INSTALL_DIR}/.venv"
GET_PIP_URL="https://bootstrap.pypa.io/get-pip.py"

echo ""
echo "============================================="
echo "DIAL Python Environment Setup"
echo "============================================="
echo ""

# Create tools directory
if [ ! -d "$TOOLS_DIR" ]; then
    mkdir -p "$TOOLS_DIR"
fi

# Step 1: Install system Python if needed
echo "Step 1: Setting up Python..."

if command -v python3 &> /dev/null; then
    PYTHON_EXE=$(which python3)
    echo "Python already installed: $PYTHON_EXE"
    python3 --version
else
    echo "Python not found. Installing..."
    
    # Check if running as root (in Docker) or need sudo
    if [ "$EUID" -eq 0 ]; then
        SUDO_CMD=""
    else
        SUDO_CMD="sudo"
    fi
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        echo "Installing Python via apt-get..."
        $SUDO_CMD apt-get update
        $SUDO_CMD apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        # RedHat/CentOS/Fedora
        echo "Installing Python via yum..."
        $SUDO_CMD yum install -y python3 python3-pip
    elif command -v brew &> /dev/null; then
        # macOS
        echo "Installing Python via Homebrew..."
        brew install python@3.12
    else
        echo "Error: No supported package manager found!"
        echo "Please install Python 3.10+ manually:"
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
        echo "  macOS: brew install python@3.12"
        exit 1
    fi
    
    PYTHON_EXE=$(which python3)
    echo "Python installed to: $PYTHON_EXE"
fi

# Step 2: Ensure pip is available
echo ""
echo "Step 2: Ensuring pip is available..."

if python3 -m pip --version &> /dev/null; then
    echo "Pip already available"
else
    echo "Installing pip..."
    
    # Download get-pip.py
    GET_PIP_PATH="${TOOLS_DIR}/get-pip.py"
    if [ ! -f "$GET_PIP_PATH" ]; then
        echo "Downloading get-pip.py..."
        curl -o "$GET_PIP_PATH" "$GET_PIP_URL"
    fi
    
    python3 "$GET_PIP_PATH"
    echo "Pip installed!"
fi

# Step 3: Install virtualenv
echo ""
echo "Step 3: Installing virtualenv..."

python3 -m pip install virtualenv

# Step 4: Create virtual environment
echo ""
echo "Step 4: Creating virtual environment..."

if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at: $VENV_DIR"
fi

# Step 5: Install dependencies in virtual environment
echo ""
echo "Step 5: Installing dependencies..."

VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_PIP="${VENV_DIR}/bin/pip"

echo "Upgrading pip in virtual environment..."
"$VENV_PYTHON" -m pip install --upgrade pip

echo "Installing langchain packages..."
"$VENV_PIP" install python-dotenv
"$VENV_PIP" install langchain
"$VENV_PIP" install langchain-openai
"$VENV_PIP" install langchain-community

echo ""
echo "============================================="
echo "Installation completed successfully!"
echo "============================================="
echo ""
echo "Virtual environment location:"
echo "  $VENV_DIR"
echo ""
echo "To activate virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run scripts with virtual environment:"
echo "  $VENV_PYTHON query_dial.py"
echo ""
