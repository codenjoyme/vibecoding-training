# install.ps1 — bootstrap a self-contained Python virtualenv for the WinAPI MCP server.
#
# Usage:
#   pwsh -ExecutionPolicy Bypass -File .\install.ps1
#
# The .venv folder is created next to this script and is gitignored.
# Re-running this script is safe (idempotent): it reuses the existing venv and
# upgrades dependencies in place.

$ErrorActionPreference = "Stop"

$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir     = Join-Path $ScriptDir ".venv"
$VenvPython  = Join-Path $VenvDir "Scripts\python.exe"
$Requirements = Join-Path $ScriptDir "requirements.txt"

function Find-Python {
    # Try `python` first, then `py -3`. Returns the command tokens as an array,
    # or $null if neither launcher is usable.
    foreach ($cmd in @(@("python"), @("py", "-3"))) {
        $exe = $cmd[0]
        if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
        try {
            if ($cmd.Length -gt 1) {
                $rest = $cmd[1..($cmd.Length - 1)] + @("--version")
                $null = & $exe @rest 2>&1
            } else {
                $null = & $exe --version 2>&1
            }
            if ($LASTEXITCODE -eq 0) { return ,$cmd }
        } catch { }
    }
    return $null
}

Write-Host "[winapi-mcp] script dir : $ScriptDir"

if (-not (Test-Path $VenvDir)) {
    $py = Find-Python
    if ($null -eq $py) {
        throw "Python 3.10+ is required but was not found on PATH. Install it from https://www.python.org/downloads/ and re-run."
    }
    Write-Host "[winapi-mcp] creating virtualenv with: $($py -join ' ') -m venv .venv"
    if ($py.Length -gt 1) {
        $rest = $py[1..($py.Length - 1)] + @("-m", "venv", $VenvDir)
        & $py[0] @rest
    } else {
        & $py[0] -m venv $VenvDir
    }
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
        Write-Host "[winapi-mcp] 'venv' module unavailable; falling back to 'virtualenv'"
        if ($py.Length -gt 1) {
            $rest = $py[1..($py.Length - 1)] + @("-m", "virtualenv", $VenvDir)
            & $py[0] @rest
        } else {
            & $py[0] -m virtualenv $VenvDir
        }
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[winapi-mcp] 'virtualenv' not installed; installing it globally now"
            if ($py.Length -gt 1) {
                $rest = $py[1..($py.Length - 1)] + @("-m", "pip", "install", "--user", "virtualenv")
                & $py[0] @rest
            } else {
                & $py[0] -m pip install --user virtualenv
            }
            if ($LASTEXITCODE -ne 0) { throw "could not install virtualenv" }
            if ($py.Length -gt 1) {
                $rest = $py[1..($py.Length - 1)] + @("-m", "virtualenv", $VenvDir)
                & $py[0] @rest
            } else {
                & $py[0] -m virtualenv $VenvDir
            }
            if ($LASTEXITCODE -ne 0) { throw "venv creation failed via virtualenv" }
        }
    }
} else {
    Write-Host "[winapi-mcp] reusing existing virtualenv at $VenvDir"
}

if (-not (Test-Path $VenvPython)) {
    throw "Expected $VenvPython after venv creation, not found."
}

Write-Host "[winapi-mcp] upgrading pip"
& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed" }

Write-Host "[winapi-mcp] installing requirements from $Requirements"
& $VenvPython -m pip install -r $Requirements
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

Write-Host ""
Write-Host "[winapi-mcp] done. To verify the server starts, run:"
Write-Host "             pwsh -ExecutionPolicy Bypass -File `"$ScriptDir\run.ps1`""
Write-Host ""
Write-Host "[winapi-mcp] Then register it in your IDE - see SKILL.md in the parent folder."
