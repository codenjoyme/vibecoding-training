# run.ps1 — entry point used by .vscode/mcp.json and .cursor/mcp.json.
# Activates the local virtualenv and launches the WinAPI MCP server on stdio.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"
$Server = Join-Path $ScriptDir "server.py"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtualenv not found at $VenvPython. Run install.ps1 first."
    exit 1
}
if (-not (Test-Path $Server)) {
    Write-Error "server.py not found at $Server"
    exit 1
}

# Force UTF-8 so JSON-RPC frames over stdio are not corrupted by the system codepage.
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"

& $VenvPython $Server
exit $LASTEXITCODE
