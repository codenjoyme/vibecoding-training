<#
.SYNOPSIS
    Run Jira CLI snapshot tests in Docker.
.DESCRIPTION
    Wrapper around the 091-cli-testing snapshot testing framework.
    Builds a Docker image with jira_cli.py installed, then runs scenario files.
    Credentials are loaded from the project root .env via Docker --env-file
    (never baked into the image).

    Prerequisites: Docker Desktop running, project root .env populated.

.PARAMETER EnvFile
    Path to the .env file with Jira credentials.
    Defaults to the project root .env (two directories above this script).

.PARAMETER Pattern
    Glob pattern for scenario files to run (default: *.md).

.PARAMETER NoBuild
    Skip Docker image rebuild (use existing jira-cli-test image).

.PARAMETER ImageName
    Docker image name (default: jira-cli-test).

.EXAMPLE
    # Run all scenarios using root .env
    & modules/470-jira-cli-access/test/run-tests.ps1

.EXAMPLE
    # Skip rebuild, run only smoke tests
    & modules/470-jira-cli-access/test/run-tests.ps1 -NoBuild -Pattern "smoke*"
#>
param(
    [string]$EnvFile = "",
    [string]$Pattern = "*.md",
    [string]$ImageName = "jira-cli-test",
    [switch]$NoBuild
)

$ErrorActionPreference = "Stop"

# ── Resolve paths ──────────────────────────────────────────────────────────────
$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$testDir    = $scriptDir
$scenDir    = Join-Path $testDir "scenarios"
$projectRoot = (Resolve-Path (Join-Path $scriptDir "../../..")).Path

# jira_cli.py lives in tools/scripts/ relative to the module
$cliScript = Join-Path $projectRoot "modules/470-jira-cli-access/tools/scripts/jira_cli.py"

# runner script for -Engine mode (bash, included in docker image)
$runnerDir  = Join-Path $projectRoot "modules/091-cli-testing/tools/cli-test-runner"
$runnerSh   = Join-Path $runnerDir "run-scenarios.sh"
$runnerPs1  = Join-Path $runnerDir "run-scenarios.ps1"

# Resolve .env file
if (-not $EnvFile) {
    $EnvFile = Join-Path $projectRoot ".env"
}
$EnvFile = (Resolve-Path $EnvFile).Path

if (-not (Test-Path $EnvFile)) {
    Write-Error "ERROR: .env file not found at: $EnvFile`nCreate it or pass -EnvFile <path>"
    exit 1
}

Write-Host "Project root : $projectRoot"
Write-Host "Env file     : $EnvFile  (mounted read-only)"
Write-Host "Scenarios    : $scenDir"
Write-Host ""

# ── Build ──────────────────────────────────────────────────────────────────────
if (-not $NoBuild) {
    # Create temp build context
    $tmpCtx = Join-Path ([System.IO.Path]::GetTempPath()) "jira-cli-test-$(Get-Random)"
    New-Item -ItemType Directory -Path $tmpCtx -Force | Out-Null

    try {
        # Copy setup.sh from test dir
        Copy-Item (Join-Path $testDir "setup.sh") (Join-Path $tmpCtx "setup.sh") -Force

        # Copy jira_cli.py so setup.sh can place it in /workspace
        Copy-Item $cliScript (Join-Path $tmpCtx "jira_cli.py") -Force

        # Copy bash runner (used as ENTRYPOINT engine inside container)
        Copy-Item $runnerSh (Join-Path $tmpCtx "run-scenarios.sh") -Force

        # Normalize LF
        foreach ($f in Get-ChildItem $tmpCtx -Filter "*.sh") {
            $c = [System.IO.File]::ReadAllText($f.FullName)
            $n = $c -replace "`r`n", "`n"
            if ($c -ne $n) { [System.IO.File]::WriteAllText($f.FullName, $n) }
        }

        # Generate Dockerfile
        $dockerfile = @"
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends bash && rm -rf /var/lib/apt/lists/*

COPY setup.sh /app/setup.sh
COPY jira_cli.py /app/jira_cli.py
RUN chmod +x /app/setup.sh && /app/setup.sh

COPY run-scenarios.sh /app/run-scenarios.sh
RUN chmod +x /app/run-scenarios.sh

RUN mkdir -p /workspace /app/scenarios
WORKDIR /workspace

ENTRYPOINT ["bash", "-c", "sed 's/\\r`$//' /app/run-scenarios.sh > /tmp/run.sh && bash /tmp/run.sh \"`$@\"", "--"]
"@
        [System.IO.File]::WriteAllText((Join-Path $tmpCtx "Dockerfile"), $dockerfile)

        Write-Host "Building Docker image: $ImageName ..."
        docker build -t $ImageName $tmpCtx
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        Write-Host ""
    } finally {
        Remove-Item -Path $tmpCtx -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# ── Normalize scenario line endings ───────────────────────────────────────────
foreach ($f in Get-ChildItem $scenDir -Filter $Pattern -File -ErrorAction SilentlyContinue) {
    $c = [System.IO.File]::ReadAllText($f.FullName)
    $n = $c -replace "`r`n", "`n"
    if ($c -ne $n) {
        [System.IO.File]::WriteAllText($f.FullName, $n)
        Write-Host "  Normalized line endings: $($f.Name)"
    }
}

# ── Run ────────────────────────────────────────────────────────────────────────
$scenDirDocker = $scenDir -replace '\\', '/'

Write-Host "Running scenarios in Docker (credentials from: $(Split-Path -Leaf $EnvFile)) ..."
docker run --rm `
    -v "${scenDirDocker}:/app/scenarios" `
    --env-file $EnvFile `
    $ImageName --engine --pattern $Pattern

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Normalize output line endings
foreach ($f in Get-ChildItem $scenDir -Filter $Pattern -File -ErrorAction SilentlyContinue) {
    $c = [System.IO.File]::ReadAllText($f.FullName)
    $n = $c -replace "`r`n", "`n"
    if ($c -ne $n) { [System.IO.File]::WriteAllText($f.FullName, $n) }
}

Write-Host ""
Write-Host "Done. Review output with:"
Write-Host "  git diff modules/470-jira-cli-access/test/scenarios/"
Write-Host ""
Write-Host "⚠️  Scenarios may contain real Jira data. Review before committing."
