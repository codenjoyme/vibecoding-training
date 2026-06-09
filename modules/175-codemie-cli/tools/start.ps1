# start.ps1 - CodeMie relay startup script
# Run from the module tools directory:
#   cd modules/175-codemie-cli/tools
#   .\start.ps1

# -- 1. Kill existing processes --
Write-Host ""
Write-Host "[1/4] Stopping existing processes..." -ForegroundColor Cyan

# Kill node process listening on port 4002 (relay)
$relayPid = (Get-NetTCPConnection -LocalPort 4002 -ErrorAction SilentlyContinue).OwningProcess | Select-Object -Unique
if ($relayPid) {
    $relayPid | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
    Write-Host "  Killed relay on port 4002 (PID: $relayPid)" -ForegroundColor Yellow
}

codemie proxy stop 2>$null
Start-Sleep -Milliseconds 500
Write-Host "  Done." -ForegroundColor Green

# -- 2. Start codemie proxy --
Write-Host ""
Write-Host "[2/4] Starting codemie proxy..." -ForegroundColor Cyan
codemie proxy start
Start-Sleep -Milliseconds 800

# -- 3. List available models --
Write-Host ""
Write-Host "[3/4] Available CodeMie models:" -ForegroundColor Cyan
& "$PSScriptRoot\list-codemie-models.ps1"

# -- 4. Copy relay and start it --
Write-Host ""
Write-Host "[4/4] Starting relay..." -ForegroundColor Cyan

$relayDest = "$env:USERPROFILE\.local\bin\codemie-relay.js"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.local\bin" | Out-Null
Copy-Item "$PSScriptRoot\codemie-relay.js" $relayDest -Force
Write-Host "  Relay copied to: $relayDest" -ForegroundColor Green

Write-Host ""
Write-Host "  Starting relay on port 4002 (Ctrl+C to stop)..." -ForegroundColor Green
Write-Host ""
node $relayDest