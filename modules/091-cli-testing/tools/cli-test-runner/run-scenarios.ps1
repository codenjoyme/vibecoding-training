<#
.SYNOPSIS
    CLI Snapshot Testing — Universal Scenario Runner (PowerShell)
.DESCRIPTION
    PowerShell port of run-scenarios.sh. Reads Markdown scenario files,
    executes lines matching > `command`, inserts output as fenced code blocks,
    writes results back to the same files.

    Can run:
      1. Inside Docker (default) — builds image, runs scenarios
      2. Locally (-Local) — runs directly on the host via bash
      3. As the inner engine (-Engine) — called from within Docker

    Inspired by Approval Tests (https://approvaltests.com/) by Llewellyn Falco.
.PARAMETER TestDir
    Path to test directory containing setup.sh and scenarios/.
.PARAMETER Pattern
    Glob pattern for scenario files to run (default: *.md).
.PARAMETER ImageName
    Docker image name to use (default: cli-snapshot-test).
.PARAMETER BaseImage
    Docker base image (default: ubuntu:22.04). E.g. node:20-slim, python:3.12-slim.
.PARAMETER NoBuild
    Skip Docker build, use existing image.
.PARAMETER Local
    Run locally without Docker (requires bash — Git Bash or WSL).
.PARAMETER Engine
    Run as inner engine (processes scenario files directly). Used inside Docker.
.PARAMETER ScenariosDir
    Override scenarios directory path (used with -Engine).
#>
param(
    [string]$TestDir = ".",
    [string]$Pattern = "*.md",
    [string]$ImageName = "cli-snapshot-test",
    [string]$BaseImage = "ubuntu:22.04",
    [switch]$NoBuild,
    [switch]$Local,
    [switch]$Engine,
    [string]$ScenariosDir = ""
)

$ErrorActionPreference = "Stop"

# ============================================
# ENGINE MODE — processes scenario files
# ============================================
function Process-Scenario {
    param([string]$FilePath)

    $currentDir = "/workspace"
    $tmpFile = "$FilePath.tmp"
    $lines = [System.IO.File]::ReadAllLines($FilePath)
    $output = [System.Collections.Generic.List[string]]::new()

    $inOutputBlock = $false
    $afterCommand = $false

    foreach ($rawLine in $lines) {
        # Strip Windows CR
        $line = $rawLine -replace "`r", ""

        # Skip old output blocks (``` that follow a command)
        if ($inOutputBlock) {
            if ($line -eq '```') {
                $inOutputBlock = $false
            }
            continue
        }

        # Detect start of old output block
        if ($afterCommand -and $line -eq '```') {
            $inOutputBlock = $true
            continue
        }

        # Check if this line is a command: > `...`
        if ($line -match '^\>\s*`(.+)`$') {
            $cmd = $Matches[1]
            $afterCommand = $true

            # Write the command line
            $output.Add($line)

            # Handle cd
            if ($cmd -match '^cd\s+(.*)') {
                $target = $Matches[1]
                if ($target.StartsWith("/")) {
                    $currentDir = $target
                } else {
                    $resolved = $null
                    try {
                        $resolved = (Resolve-Path (Join-Path $currentDir $target) -ErrorAction Stop).Path
                    } catch {}
                    if ($resolved) { $currentDir = $resolved }
                }
                $output.Add('```')
                $output.Add($currentDir)
                $output.Add('```')
                continue
            }

            # Execute command via bash (< /dev/null prevents stdin consumption)
            $bashCmd = "cd `"$currentDir`" 2>/dev/null && eval `"$($cmd -replace '"', '\"')`" < /dev/null 2>&1"
            try {
                $cmdOutput = bash -c $bashCmd 2>&1 | Out-String
            } catch {
                $cmdOutput = $_.Exception.Message
            }
            # Trim trailing newlines, replace backticks
            $cmdOutput = ($cmdOutput -replace "`r", "").TrimEnd("`n")
            $cmdOutput = $cmdOutput -replace '`', "'"

            $output.Add('```')
            if ($cmdOutput) {
                $output.Add($cmdOutput)
            }
            $output.Add('```')
        } else {
            $afterCommand = $false
            $output.Add($line)
        }
    }

    $result = $output -join "`n"
    [System.IO.File]::WriteAllText($FilePath, $result)
    Write-Host "  ✓ $(Split-Path -Leaf $FilePath)"
}

if ($Engine) {
    # Running as engine inside Docker or locally
    $dir = if ($ScenariosDir) { $ScenariosDir } else { "/app/scenarios" }
    Write-Host "Running scenarios from: $dir"
    Write-Host "Pattern: $Pattern"
    Write-Host "---"

    $files = Get-ChildItem -Path $dir -Filter $Pattern -File -ErrorAction SilentlyContinue
    if (-not $files -or $files.Count -eq 0) {
        Write-Host "No scenario files matching '$Pattern' found in $dir"
        exit 1
    }

    foreach ($f in $files) {
        Process-Scenario -FilePath $f.FullName
    }

    Write-Host "---"
    Write-Host "Done. $($files.Count) scenario(s) processed."
    exit 0
}

# ============================================
# LOCAL MODE — run engine directly on host
# ============================================
if ($Local) {
    $scenDir = Join-Path (Resolve-Path $TestDir) "scenarios"
    if (-not (Test-Path $scenDir)) {
        Write-Error "Error: scenarios directory not found: $scenDir"
        exit 1
    }

    Write-Host "Running locally (no Docker)..."
    Write-Host "Running scenarios from: $scenDir"
    Write-Host "Pattern: $Pattern"
    Write-Host "---"

    $files = Get-ChildItem -Path $scenDir -Filter $Pattern -File -ErrorAction SilentlyContinue
    if (-not $files -or $files.Count -eq 0) {
        Write-Host "No scenario files matching '$Pattern' found in $scenDir"
        exit 1
    }

    foreach ($f in $files) {
        Process-Scenario -FilePath $f.FullName
    }

    Write-Host "---"
    Write-Host "Done. $($files.Count) scenario(s) processed."
    exit 0
}

# ============================================
# DOCKER MODE — build image, mount scenarios, run
# ============================================
$TestDir = (Resolve-Path $TestDir).Path

if (-not (Test-Path $TestDir)) {
    Write-Error "Error: test directory not found: $TestDir"
    exit 1
}

if (-not (Test-Path (Join-Path $TestDir "scenarios"))) {
    Write-Error "Error: scenarios directory not found: $(Join-Path $TestDir 'scenarios')"
    exit 1
}

# Resolve own script path (for copying into build context)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $scriptDir "run-scenarios.sh"

# Create temporary build context
$tmpCtx = Join-Path ([System.IO.Path]::GetTempPath()) "cli-snapshot-$(Get-Random)"
New-Item -ItemType Directory -Path $tmpCtx -Force | Out-Null

try {
    # Copy the bash runner script into build context
    if (Test-Path $scriptPath) {
        Copy-Item $scriptPath -Destination (Join-Path $tmpCtx "run-scenarios.sh") -Force
    } else {
        Write-Error "Error: run-scenarios.sh not found at: $scriptPath"
        exit 1
    }

    # Copy setup.sh (or generate a no-op)
    $setupSrc = Join-Path $TestDir "setup.sh"
    if (Test-Path $setupSrc) {
        Copy-Item $setupSrc -Destination (Join-Path $tmpCtx "setup.sh") -Force
    } else {
        Set-Content -Path (Join-Path $tmpCtx "setup.sh") -Value "#!/bin/bash`necho `"No custom setup.`"`n" -NoNewline
    }

    # Normalize line endings to LF in build context
    foreach ($file in Get-ChildItem $tmpCtx -Filter "*.sh") {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $normalized = $content -replace "`r`n", "`n"
        if ($content -ne $normalized) {
            [System.IO.File]::WriteAllText($file.FullName, $normalized)
        }
    }

    # Use custom Dockerfile from test dir if present, otherwise generate one
    $customDockerfile = Join-Path $TestDir "Dockerfile"
    if (Test-Path $customDockerfile) {
        Copy-Item $customDockerfile -Destination (Join-Path $tmpCtx "Dockerfile") -Force
    } else {
        $dockerfile = @"
ARG BASE_IMAGE=ubuntu:22.04
FROM `${BASE_IMAGE}

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*
RUN git config --global user.email "test@test.local" \
 && git config --global user.name "Snapshot Test"

COPY setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh && /app/setup.sh

COPY run-scenarios.sh /app/run-scenarios.sh
RUN chmod +x /app/run-scenarios.sh

RUN mkdir -p /workspace /app/scenarios

ENTRYPOINT ["bash", "-c", "sed 's/\\r`$//' /app/run-scenarios.sh > /tmp/run.sh && bash /tmp/run.sh \"`$@\"", "--"]
"@
        [System.IO.File]::WriteAllText((Join-Path $tmpCtx "Dockerfile"), $dockerfile)
    }

    # Build
    if (-not $NoBuild) {
        Write-Host "Building Docker image: $ImageName (base: $BaseImage) ..."
        docker build --build-arg "BASE_IMAGE=$BaseImage" -t $ImageName $tmpCtx
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        Write-Host ""
    }

    # Normalize line endings in scenario files before mounting
    $scenariosPath = (Resolve-Path (Join-Path $TestDir "scenarios")).Path
    foreach ($file in Get-ChildItem $scenariosPath -Filter $Pattern) {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $normalized = $content -replace "`r`n", "`n"
        if ($content -ne $normalized) {
            [System.IO.File]::WriteAllText($file.FullName, $normalized)
            Write-Host "  Normalized line endings: $($file.Name)"
        }
    }

    # Run — mount scenarios folder so output is written back to host
    Write-Host "Running scenarios in Docker..."
    $scenariosDocker = $scenariosPath -replace '\\', '/'
    docker run --rm -v "${scenariosDocker}:/app/scenarios" $ImageName --engine --pattern $Pattern
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    # Normalize output line endings
    foreach ($file in Get-ChildItem $scenariosPath -Filter $Pattern) {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $normalized = $content -replace "`r`n", "`n"
        if ($content -ne $normalized) {
            [System.IO.File]::WriteAllText($file.FullName, $normalized)
        }
    }

    Write-Host ""
    Write-Host "Done. Check changes with: git diff $(Join-Path $TestDir 'scenarios')"
} finally {
    # Cleanup temp build context
    Remove-Item -Path $tmpCtx -Recurse -Force -ErrorAction SilentlyContinue
}
