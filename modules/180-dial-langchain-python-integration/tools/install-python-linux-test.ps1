# PowerShell Docker Test Runner for DIAL Python Installation
# This script builds a Docker image and runs the installation test in a clean Linux environment

$ErrorActionPreference = "Stop"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$IMAGE_NAME = "dial-python-test"
$CONTAINER_NAME = "dial-test-container"

Set-Location $SCRIPT_DIR

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Docker Test Runner for DIAL Python Setup" -ForegroundColor White
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

# Check .env.example has real API key (script will copy it to .env in workspace)
if (Test-Path ".env.example") {
    $envContent = Get-Content ".env.example" -Raw
    if ($envContent -match "YOUR_API_KEY_HERE") {
        Write-Host "ERROR: .env.example contains placeholder API key!" -ForegroundColor Red
        Write-Host "Please edit .env.example and replace YOUR_API_KEY_HERE with your actual DIAL API key" -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
    Write-Host "PASS: .env.example has configured API key" -ForegroundColor Green
    Write-Host ""
}

# Clean up any existing container
$existingContainer = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq $CONTAINER_NAME }
if ($existingContainer) {
    Write-Host "Cleaning up existing container..." -ForegroundColor Yellow
    docker rm -f $CONTAINER_NAME 2>$null | Out-Null
}

# Build Docker image (copies .root and all files)
Write-Host "Building Docker image with project structure..." -ForegroundColor Cyan
Write-Host ""
docker build -f install-python-linux-test.dockerfile -t $IMAGE_NAME .

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Running installation test in Docker..." -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Run the container (everything is inside, no volume mounts needed)
docker run --rm `
    --name $CONTAINER_NAME `
    --add-host "host.docker.internal:host-gateway" `
    -it `
    $IMAGE_NAME

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Docker test completed!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
