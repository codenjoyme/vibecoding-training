# PowerShell Docker Runner for DIAL Python Application
# This script builds a production Docker image and runs the DIAL query application

param(
    [string]$Script = "query_dial.py",
    [string]$WorkspacePath = "work\180-task",
    [string]$ExtraPackages = "python-dotenv langchain langchain-openai langchain-community"
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

# Copy files to workspace
Write-Host "Preparing workspace..." -ForegroundColor Yellow

# Copy all .py files if they don't exist in workspace
Get-ChildItem -Path $SCRIPT_DIR -Filter "*.py" | ForEach-Object {
    $targetFile = Join-Path $WORKSPACE_DIR $_.Name
    if (-not (Test-Path $targetFile)) {
        Copy-Item $_.FullName -Destination $targetFile -Force
        Write-Host "  Copied: $($_.Name)" -ForegroundColor Gray
    }
}

# Copy .env.example if .env doesn't exist
$envExample = Join-Path $SCRIPT_DIR ".env.example"
$envTarget = Join-Path $WORKSPACE_DIR ".env"
if ((Test-Path $envExample) -and (-not (Test-Path $envTarget))) {
    Copy-Item $envExample -Destination $envTarget -Force
    Write-Host "  Created .env from template" -ForegroundColor Gray
}

# Copy Dockerfile to workspace
$dockerfileSource = Join-Path $SCRIPT_DIR "install-python-docker.dockerfile"
$dockerfileTarget = Join-Path $WORKSPACE_DIR "Dockerfile"
Copy-Item $dockerfileSource -Destination $dockerfileTarget -Force
Write-Host "  Copied: Dockerfile" -ForegroundColor Gray

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

Set-Location $WORKSPACE_DIR

$buildArgs = @("-f", "Dockerfile", "--build-arg", "SCRIPT_NAME=$Script")
if ($ExtraPackages) {
    $buildArgs += "--build-arg"
    $buildArgs += "EXTRA_PACKAGES=$ExtraPackages"
}
$buildArgs += @("-t", $IMAGE_NAME, ".")

& docker build @buildArgs

Set-Location $SCRIPT_DIR

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Running DIAL application in Docker..." -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Run the container with workspace directory mounted
docker run --rm `
    --name $CONTAINER_NAME `
    --add-host "host.docker.internal:host-gateway" `
    -v "${WORKSPACE_DIR}:/workspace" `
    -it `
    $IMAGE_NAME `
    bash -c "python $Script"

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Application completed!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
