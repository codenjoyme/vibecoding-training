# PowerShell Docker Runner for DIAL Python Application
# This script builds a production Docker image and runs the DIAL query application

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$IMAGE_NAME = "dial-python-app"
$CONTAINER_NAME = "dial-app-container"

Set-Location $SCRIPT_DIR

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "DIAL Python Docker Application" -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
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
Write-Host ""
docker build -f install-python-docker.dockerfile -t $IMAGE_NAME .

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Running DIAL application in Docker..." -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Run the container with host network bridge
docker run --rm `
    --name $CONTAINER_NAME `
    --add-host "host.docker.internal:host-gateway" `
    -it `
    $IMAGE_NAME

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Application completed!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
