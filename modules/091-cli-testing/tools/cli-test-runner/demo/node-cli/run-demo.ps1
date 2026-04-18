<#
.SYNOPSIS
    Run demo: Node.js CLI snapshot test
.DESCRIPTION
    Copies the universal runner into the demo folder, builds Docker, runs scenarios.
#>
param(
    [string]$Pattern = "*.md"
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent (Split-Path -Parent $scriptRoot)
$runnerSrc = Join-Path $skillRoot "run-scenarios.sh"
$demoDir = $scriptRoot

# Copy the universal runner into the demo dir for Docker build context
Copy-Item $runnerSrc -Destination (Join-Path $demoDir "run-scenarios.sh") -Force

# Use the main PowerShell wrapper
$ps1Runner = Join-Path $skillRoot "run-scenarios.ps1"
& $ps1Runner -TestDir $demoDir -Pattern $Pattern -ImageName "demo-node-cli-test"

# Clean up copied runner
Remove-Item (Join-Path $demoDir "run-scenarios.sh") -ErrorAction SilentlyContinue
