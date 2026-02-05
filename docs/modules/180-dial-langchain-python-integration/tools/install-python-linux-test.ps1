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

# Clean up any existing container
$existingContainer = docker ps -a --format '{{.Names}}' | Where-Object { $_ -eq $CONTAINER_NAME }
if ($existingContainer) {
    Write-Host "Cleaning up existing container..." -ForegroundColor Yellow
    docker rm -f $CONTAINER_NAME 2>$null | Out-Null
}

# Build Docker image
Write-Host "Building Docker image..." -ForegroundColor Cyan
Write-Host ""
docker build -f install-python-linux-test.dockerfile -t $IMAGE_NAME .

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Running installation test in Docker..." -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Get absolute path to current directory
$TOOLS_PATH = (Get-Location).Path

# Collect all Python files
$pythonFiles = Get-ChildItem -Path $TOOLS_PATH -Filter "*.py" -File

Write-Host "Mounting files:" -ForegroundColor Gray
Write-Host "  .env" -ForegroundColor Gray
Write-Host "  install-python-linux.sh" -ForegroundColor Gray
foreach ($file in $pythonFiles) {
    Write-Host "  $($file.Name)" -ForegroundColor Gray
}
Write-Host ""

# Build docker run command with individual file mounts
$dockerArgs = @(
    "run", "--rm",
    "--name", $CONTAINER_NAME,
    "--add-host", "host.docker.internal:host-gateway",
    "-v", "${TOOLS_PATH}\.env:/workspace/.env:ro",
    "-v", "${TOOLS_PATH}\install-python-linux.sh:/workspace/install-python-linux.sh"
)

# Add each Python file as a mount
foreach ($file in $pythonFiles) {
    $dockerArgs += "-v"
    $dockerArgs += "${TOOLS_PATH}\$($file.Name):/workspace/$($file.Name):ro"
}

# Add interactive flags and image name
$dockerArgs += "-it"
$dockerArgs += $IMAGE_NAME

# Run the container with mounted files
& docker $dockerArgs

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Docker test completed!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""
