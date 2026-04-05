# setup.ps1 — initialize demo/skills-repo as a Git repository
# Run once before using the demo with the skills CLI
# Usage: .\setup.ps1

$ErrorActionPreference = "Stop"

$ScriptDir = $PSScriptRoot
$RepoDir = Join-Path $ScriptDir "skills-repo"

Write-Host "→ Initializing demo skills-repo ..."

Push-Location $RepoDir
try {
    git init
    git config user.email "demo@skills-cli.local"
    git config user.name "Skills Demo"
    git config receive.denyCurrentBranch warn
    git add .
    git commit -m "init: demo skills repository"
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "✅ Demo skills-repo initialized at $RepoDir"
Write-Host ""
Write-Host "Next: create a project workspace and run:"
Write-Host "  skills init --repo `"$RepoDir`" --groups project-alpha"
