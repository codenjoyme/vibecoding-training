# Simple Python Environment Setup for DIAL Integration
# This script downloads portable Python, creates virtual environment, and installs dependencies

$ErrorActionPreference = "Stop"

# Configuration
$PYTHON_VERSION = "3.12.8"
$PYTHON_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-embed-amd64.zip"
$GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

# Install everything in the tools directory
$INSTALL_DIR = $PSScriptRoot
$TOOLS_DIR = Join-Path $INSTALL_DIR ".tools"
$PYTHON_DIR = Join-Path $TOOLS_DIR "python"
$VENV_DIR = Join-Path $INSTALL_DIR ".venv"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "DIAL Python Environment Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Create tools directory
if (-not (Test-Path $TOOLS_DIR)) {
    New-Item -ItemType Directory -Path $TOOLS_DIR | Out-Null
}

# Step 1: Download and extract portable Python
Write-Host "Step 1: Setting up portable Python..." -ForegroundColor Yellow

if (Test-Path (Join-Path $PYTHON_DIR "python.exe")) {
    Write-Host "Python already exists, skipping download..." -ForegroundColor Green
} else {
    Write-Host "Downloading Python $PYTHON_VERSION..." -ForegroundColor Yellow
    
    $pythonZip = Join-Path $TOOLS_DIR "python.zip"
    
    # Download Python
    Invoke-WebRequest -Uri $PYTHON_URL -OutFile $pythonZip
    
    # Extract Python
    Write-Host "Extracting Python..." -ForegroundColor Yellow
    Expand-Archive -Path $pythonZip -DestinationPath $PYTHON_DIR -Force
    
    # Clean up zip
    Remove-Item $pythonZip
    
    Write-Host "Python installed to: $PYTHON_DIR" -ForegroundColor Green
}

$PYTHON_EXE = Join-Path $PYTHON_DIR "python.exe"

# Step 2: Enable pip for embedded Python
Write-Host ""
Write-Host "Step 2: Enabling pip..." -ForegroundColor Yellow

# Modify python312._pth to enable site-packages
$pthFile = Join-Path $PYTHON_DIR "python312._pth"
if (Test-Path $pthFile) {
    $content = Get-Content $pthFile
    $content = $content -replace "^#import site", "import site"
    $content | Set-Content $pthFile
}

# Download and install pip
$getPipPath = Join-Path $TOOLS_DIR "get-pip.py"
if (-not (Test-Path $getPipPath)) {
    Write-Host "Downloading get-pip.py..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $GET_PIP_URL -OutFile $getPipPath
}

Write-Host "Installing pip..." -ForegroundColor Yellow
& $PYTHON_EXE $getPipPath --no-warn-script-location

Write-Host "Pip installed!" -ForegroundColor Green

# Step 3: Install virtualenv
Write-Host ""
Write-Host "Step 3: Installing virtualenv..." -ForegroundColor Yellow

& $PYTHON_EXE -m pip install virtualenv --no-warn-script-location

# Step 4: Create virtual environment
Write-Host ""
Write-Host "Step 4: Creating virtual environment..." -ForegroundColor Yellow

if (Test-Path $VENV_DIR) {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Green
} else {
    & $PYTHON_EXE -m virtualenv $VENV_DIR
    Write-Host "Virtual environment created at: $VENV_DIR" -ForegroundColor Green
}

# Step 5: Install dependencies in virtual environment
Write-Host ""
Write-Host "Step 5: Installing dependencies..." -ForegroundColor Yellow

$VENV_PYTHON = Join-Path $VENV_DIR "Scripts\python.exe"
$VENV_PIP = Join-Path $VENV_DIR "Scripts\pip.exe"

Write-Host "Upgrading pip in virtual environment..." -ForegroundColor Yellow
& $VENV_PYTHON -m pip install --upgrade pip

Write-Host "Installing langchain packages..." -ForegroundColor Yellow
& $VENV_PIP install python-dotenv
& $VENV_PIP install langchain
& $VENV_PIP install langchain-openai
& $VENV_PIP install langchain-community

Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Virtual environment location:" -ForegroundColor Cyan
Write-Host "  $VENV_DIR" -ForegroundColor White
Write-Host ""
Write-Host "To activate virtual environment:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run scripts with virtual environment:" -ForegroundColor Cyan
Write-Host "  $VENV_PYTHON query_dial.py" -ForegroundColor White
Write-Host ""
