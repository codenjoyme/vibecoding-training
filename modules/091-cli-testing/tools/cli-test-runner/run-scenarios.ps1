<#
.SYNOPSIS
    CLI Snapshot Testing — PowerShell wrapper for Windows users.
.DESCRIPTION
    Builds a Docker image from the test directory and runs CLI snapshot
    scenarios inside a container. Results are written back to the scenario
    Markdown files on the host via a volume mount.
.PARAMETER TestDir
    Path to the test directory containing Dockerfile, setup.sh, and scenarios/.
.PARAMETER Pattern
    Glob pattern for scenario files to run (default: *.md).
.PARAMETER ImageName
    Docker image name to use (default: cli-snapshot-test).
.PARAMETER NoBuild
    Skip Docker build, use existing image.
.PARAMETER Local
    Run locally without Docker (requires WSL or Git Bash).
#>
param(
    [string]$TestDir = ".",
    [string]$Pattern = "*.md",
    [string]$ImageName = "cli-snapshot-test",
    [switch]$NoBuild,
    [switch]$Local
)

$ErrorActionPreference = "Stop"

$TestDir = Resolve-Path $TestDir

if (-not (Test-Path "$TestDir")) {
    Write-Error "Test directory not found: $TestDir"
    exit 1
}

if (-not (Test-Path "$TestDir/scenarios")) {
    Write-Error "Scenarios directory not found: $TestDir/scenarios"
    exit 1
}

if (-not (Test-Path "$TestDir/Dockerfile")) {
    Write-Error "Dockerfile not found: $TestDir/Dockerfile"
    exit 1
}

# Normalize line endings in scenario files (Windows CRLF → Unix LF)
Get-ChildItem "$TestDir/scenarios" -Filter $Pattern | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName)
    $normalized = $content -replace "`r`n", "`n"
    if ($content -ne $normalized) {
        [System.IO.File]::WriteAllText($_.FullName, $normalized)
        Write-Host "  Normalized line endings: $($_.Name)"
    }
}

if ($Local) {
    Write-Host "Running locally via bash..."
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $runnerScript = Join-Path $scriptDir "run-scenarios.sh"
    bash $runnerScript --local --test-dir $TestDir --pattern $Pattern
    exit $LASTEXITCODE
}

# Copy the universal runner script into the build context if not already there
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$runnerSrc = Join-Path $scriptDir "run-scenarios.sh"
$runnerDst = Join-Path $TestDir "run-scenarios.sh"
$copiedRunner = $false

if ((Test-Path $runnerSrc) -and ($runnerSrc -ne $runnerDst)) {
    Copy-Item $runnerSrc -Destination $runnerDst -Force
    $copiedRunner = $true
}

# Build Docker image
if (-not $NoBuild) {
    Write-Host "Building Docker image: $ImageName ..."
    docker build -t $ImageName -f "$TestDir/Dockerfile" "$TestDir"
    if ($LASTEXITCODE -ne 0) {
        if ($copiedRunner) { Remove-Item $runnerDst -ErrorAction SilentlyContinue }
        exit $LASTEXITCODE
    }
    Write-Host ""
}

# Run scenarios in Docker — mount scenarios folder
Write-Host "Running scenarios in Docker..."
$scenariosPath = (Resolve-Path "$TestDir/scenarios").Path -replace '\\', '/'

docker run --rm `
    -v "${scenariosPath}:/app/scenarios" `
    $ImageName `
    --engine --pattern $Pattern

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Normalize output line endings back (Docker produces LF, ensure consistency)
Get-ChildItem "$TestDir/scenarios" -Filter $Pattern | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName)
    $normalized = $content -replace "`r`n", "`n"
    if ($content -ne $normalized) {
        [System.IO.File]::WriteAllText($_.FullName, $normalized)
    }
}

# Clean up copied runner if we put it there
if ($copiedRunner) { Remove-Item $runnerDst -ErrorAction SilentlyContinue }

Write-Host ""
Write-Host "Done. Check changes with: git diff $TestDir/scenarios/"
