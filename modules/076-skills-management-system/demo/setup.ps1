# setup.ps1 — copy demo skills-repo to work/076-task/ and git-initialize it
# Run from workspace root: .\modules\076-skills-management-system\demo\setup.ps1

$ErrorActionPreference = "Stop"

# Resolve paths
$DemoDir = $PSScriptRoot
$SourceDir = Join-Path $DemoDir "skills-repo"

# Workspace root is 3 levels up from demo/
$WorkspaceRoot = Split-Path (Split-Path (Split-Path $DemoDir -Parent) -Parent) -Parent
$TargetDir = Join-Path $WorkspaceRoot "work\076-task\skills-repo"

Write-Host "→ Setting up skills-repo at: $TargetDir"

if (Test-Path $TargetDir) {
    Write-Host ""
    Write-Host "✋ Target already exists: $TargetDir"
    Write-Host "   Delete it first if you want to reset:"
    Write-Host "   Remove-Item -Recurse -Force '$TargetDir'"
    exit 1
}

# Ensure parent work/076-task/ exists
$ParentDir = Split-Path $TargetDir -Parent
if (-not (Test-Path $ParentDir)) {
    New-Item -ItemType Directory -Path $ParentDir | Out-Null
}

# Copy demo content to target
Copy-Item -Recurse $SourceDir $TargetDir

# Initialize Git repo in target
Push-Location $TargetDir
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
Write-Host "✅ Done! skills-repo initialized at:"
Write-Host "   $TargetDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  cd work\076-task"
Write-Host "  mkdir project-alpha ; cd project-alpha"
Write-Host "  skills init --repo ..\skills-repo --groups project-alpha"
