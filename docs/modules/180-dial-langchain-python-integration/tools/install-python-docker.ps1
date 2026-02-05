# PowerShell Docker Runner for DIAL Python Application
# This script builds a production Docker image and runs the DIAL query application

param(
    [string]$Script = "query_dial.py",
    [string]$WorkspacePath = "work\python-ai-workspace",
    [string]$ExtraPackages = ""
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

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$IMAGE_NAME = "dial-python-app"
$CONTAINER_NAME = "dial-app-container"

# Find project root and resolve workspace path
$PROJECT_ROOT = Find-ProjectRoot -StartPath $SCRIPT_DIR
$WORKSPACE_DIR = Join-Path $PROJECT_ROOT $WorkspacePath

if (-not (Test-Path $WORKSPACE_DIR)) {
    New-Item -ItemType Directory -Path $WORKSPACE_DIR -Force | Out-Null
}

$WORKSPACE_DIR = Resolve-Path $WORKSPACE_DIR

Set-Location $SCRIPT_DIR

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "DIAL Python Docker Application" -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Script to run: $Script" -ForegroundColor Yellow
Write-Host "Workspace: $WORKSPACE_DIR" -ForegroundColor Yellow
Write-Host ""

# Check if Docker is available
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Docker Desktop first:" -ForegroundColor Yellow
    Write-Host "  https://www.docker.com/products/docker-desktop" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

$dockerVersion = docker --version
Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
Write-Host ""

# Clean up any existing container
$existingContainer = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq $CONTAINER_NAME }
if ($existingContainer) {
    Write-Host "Cleaning up existing container..." -ForegroundColor Yellow
    docker rm -f $CONTAINER_NAME 2>$null | Out-Null
}

# Build Docker image
Write-Host "Building Docker image with full Python environment..." -ForegroundColor Cyan
if ($ExtraPackages) {
    Write-Host "Extra packages: $ExtraPackages" -ForegroundColor Yellow
}
Write-Host ""

$buildArgs = @("-f", "install-python-docker.dockerfile", "--build-arg", "SCRIPT_NAME=$Script")
if ($ExtraPackages) {
    $buildArgs += "--build-arg"
    $buildArgs += "EXTRA_PACKAGES=$ExtraPackages"
}
$buildArgs += @("-t", $IMAGE_NAME, ".")

& docker build @buildArgs

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Running DIAL application in Docker..." -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Run the container with tools directory mounted (contains scripts and .env)
docker run --rm `
    --name $CONTAINER_NAME `
    --add-host "host.docker.internal:host-gateway" `
    -v "${SCRIPT_DIR}:/workspace" `
    -it `
    $IMAGE_NAME `
    bash -c "if [ -f .env.example ] && [ ! -f .env ]; then cp .env.example .env; fi && python $Script"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Application completed!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
