# Simple Python Environment Setup for DIAL Integration
# This script downloads portable Python, creates virtual environment, and installs dependencies

param(
    [string]$WorkspacePath = "work\180-task"
)

$ErrorActionPreference = "Stop"

# Function to find project root by .root marker file
function Find-ProjectRoot {
    param([string]$StartPath)
    
    $currentPath = $StartPath
    $maxDepth = 10
    $depth = 0
    
    while ($depth -lt $maxDepth) {
        $rootMarker = Join-Path $currentPath ".root"
        if (Test-Path $rootMarker) {
            return $currentPath
        }
        
        $parentPath = Split-Path $currentPath -Parent
        if (-not $parentPath -or $parentPath -eq $currentPath) {
            break
        }
        
        $currentPath = $parentPath
        $depth++
    }
    
    throw "Could not find project root (.root file not found). Are you in the right directory?"
}

# Configuration
$PYTHON_VERSION = "3.12.8"
$PYTHON_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION-embed-amd64.zip"
$GET_PIP_URL = "https://bootstrap.pypa.io/get-pip.py"

# Find project root and resolve workspace path
$PROJECT_ROOT = Find-ProjectRoot -StartPath $PSScriptRoot
$WORKSPACE_DIR = Join-Path $PROJECT_ROOT $WorkspacePath

if (-not (Test-Path $WORKSPACE_DIR)) {
    New-Item -ItemType Directory -Path $WORKSPACE_DIR -Force | Out-Null
}

$WORKSPACE_DIR = Resolve-Path $WORKSPACE_DIR

# Install tools in temporary location
$TOOLS_DIR = Join-Path $WORKSPACE_DIR ".tools"
$PYTHON_DIR = Join-Path $TOOLS_DIR "python"
$VENV_DIR = Join-Path $WORKSPACE_DIR ".venv"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "DIAL Python Environment Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Workspace: $WORKSPACE_DIR" -ForegroundColor Yellow
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

# Step 6: Copy Python scripts to workspace
Write-Host "Step 6: Copying example scripts to workspace..." -ForegroundColor Yellow

$sourceDir = $PSScriptRoot
Copy-Item (Join-Path $sourceDir "query_dial.py") -Destination $WORKSPACE_DIR -Force
Copy-Item (Join-Path $sourceDir "color.py") -Destination $WORKSPACE_DIR -Force

# Copy .env.example if .env doesn't exist
$envExample = Join-Path $sourceDir ".env.example"
$envTarget = Join-Path $WORKSPACE_DIR ".env"
if ((Test-Path $envExample) -and (-not (Test-Path $envTarget))) {
    Copy-Item $envExample -Destination $envTarget -Force
    Write-Host ""
    Write-Host "IMPORTANT: Configure your API key in .env file!" -ForegroundColor Yellow
}

# Create .gitignore
$gitignore = @"
.venv/
.tools/
.env
__pycache__/
*.pyc
"@
Set-Content -Path (Join-Path $WORKSPACE_DIR ".gitignore") -Value $gitignore

Write-Host "Scripts copied to workspace" -ForegroundColor Green

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Virtual environment location:" -ForegroundColor Cyan
Write-Host "  $VENV_DIR" -ForegroundColor White
Write-Host ""
Write-Host "Workspace location:" -ForegroundColor Cyan
Write-Host "  $WORKSPACE_DIR" -ForegroundColor White
Write-Host ""
Write-Host "To activate virtual environment (run from workspace):" -ForegroundColor Cyan
Write-Host "  cd $WORKSPACE_DIR" -ForegroundColor White
Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run example script:" -ForegroundColor Cyan
Write-Host "  python query_dial.py" -ForegroundColor White
Write-Host ""
