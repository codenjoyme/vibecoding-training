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

# -- 4. Copy relay and start it as daemon --
Write-Host ""
Write-Host "[4/4] Starting relay daemon..." -ForegroundColor Cyan

$relayDest = "$env:USERPROFILE\.local\bin\codemie-relay.js"
$relayLog  = "$env:USERPROFILE\.local\bin\codemie-relay.log"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.local\bin" | Out-Null
Copy-Item "$PSScriptRoot\codemie-relay.js" $relayDest -Force
Write-Host "  Relay copied to: $relayDest" -ForegroundColor Green

# Start relay as background job, redirect output to log file
$proc = Start-Process -FilePath "node" -ArgumentList $relayDest `
    -WindowStyle Hidden `
    -RedirectStandardOutput $relayLog `
    -RedirectStandardError "$env:USERPROFILE\.local\bin\codemie-relay.err.log" `
    -PassThru

Start-Sleep -Milliseconds 500

# Verify it started
$check = Get-NetTCPConnection -LocalPort 4002 -ErrorAction SilentlyContinue
if ($check) {
    Write-Host "  Relay daemon started (PID: $($proc.Id), port 4002)" -ForegroundColor Green
    Write-Host "  Log: $relayLog" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  To stop:  Stop-Process -Id $($proc.Id)" -ForegroundColor DarkGray
    Write-Host "  To check: Get-Content $relayLog" -ForegroundColor DarkGray
} else {
    Write-Host "  WARNING: relay may not have started. Check log:" -ForegroundColor Red
    Write-Host "  $relayLog" -ForegroundColor Yellow
    if (Test-Path $relayLog) { Get-Content $relayLog | ForEach-Object { Write-Host "    $_" } }
}

Write-Host ""
Write-Host "Done. Both proxies running as daemons." -ForegroundColor Green
Write-Host "  codemie proxy: http://127.0.0.1:4001" -ForegroundColor DarkGray
Write-Host "  codemie relay: http://127.0.0.1:4002" -ForegroundColor DarkGray