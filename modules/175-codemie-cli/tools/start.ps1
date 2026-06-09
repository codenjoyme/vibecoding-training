# start.ps1 — CodeMie relay startup script
# Run from the module tools directory:
#   cd modules/175-codemie-cli/tools
#   .\start.ps1

Set-StrictMode -Off
$ErrorActionPreference = 'SilentlyContinue'

# ── 1. Kill existing codemie proxy and relay processes ──────────────────────
Write-Host "`n[1/4] Stopping existing processes..." -ForegroundColor Cyan

# Kill any running codemie-relay node process
Get-Process -Name "node" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*codemie-relay*" } |
    Stop-Process -Force -ErrorAction SilentlyContinue

# Kill codemie proxy daemon (uses its own stop command)
codemie proxy stop 2>$null
Start-Sleep -Milliseconds 500

Write-Host "  Done." -ForegroundColor Green

# ── 2. Show available CodeMie models ────────────────────────────────────────
Write-Host "`n[2/4] Available CodeMie models:" -ForegroundColor Cyan
try {
    $models = Invoke-RestMethod -Uri "http://127.0.0.1:4001/v1/models" `
        -Headers @{ Authorization = "Bearer codemie-proxy" } `
        -ErrorAction Stop
    $models.data | ForEach-Object { Write-Host "  - $($_.id)" }
} catch {
    Write-Host "  (proxy not running yet — will start in step 4)" -ForegroundColor Yellow
}

# ── 3. Show chatLanguageModels.json location and current content ─────────────
Write-Host "`n[3/4] chatLanguageModels.json — where to configure Copilot models:" -ForegroundColor Cyan

$configPaths = @(
    "$env:APPDATA\Code - Insiders\User\chatLanguageModels.json",
    "$env:APPDATA\Code\User\chatLanguageModels.json"
)

$foundConfig = $null
foreach ($p in $configPaths) {
    if (Test-Path $p) {
        $foundConfig = $p
        break
    }
}

if ($foundConfig) {
    Write-Host "  Found: $foundConfig" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Current content:" -ForegroundColor DarkGray
    Get-Content $foundConfig | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
} else {
    Write-Host "  Not found at default locations:" -ForegroundColor Yellow
    $configPaths | ForEach-Object { Write-Host "    $_" }
    Write-Host ""
    Write-Host "  Create it with the content from chatLanguageModels.js in this folder." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Reference config (this folder): $(Resolve-Path '.\chatLanguageModels.js')" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  MODEL_MAP is built automatically from chatLanguageModels.json at relay startup." -ForegroundColor DarkGray
Write-Host "  To add a new model — add an entry to chatLanguageModels.json with 'realModelId':" -ForegroundColor DarkGray
Write-Host '    { "id": "gpt-4o-mini", "realModelId": "claude-haiku-4-6", "name": "...", ... }' -ForegroundColor DarkGray
Write-Host "  No changes to codemie-relay.js needed." -ForegroundColor DarkGray

# ── 4. Start codemie proxy + relay ──────────────────────────────────────────
Write-Host "`n[4/4] Starting proxies..." -ForegroundColor Cyan

# Start codemie proxy (background)
codemie proxy start
Start-Sleep -Milliseconds 800

# Copy relay to user bin and start it (foreground — keep terminal open)
$relayDest = "$env:USERPROFILE\.local\bin\codemie-relay.js"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.local\bin" | Out-Null
Copy-Item ".\codemie-relay.js" $relayDest -Force
Write-Host "  Relay copied to: $relayDest" -ForegroundColor Green

# Show available models now that proxy is running
Write-Host "`n  Available models (from proxy):" -ForegroundColor Cyan
try {
    $models = Invoke-RestMethod -Uri "http://127.0.0.1:4001/v1/models" `
        -Headers @{ Authorization = "Bearer codemie-proxy" } `
        -ErrorAction Stop
    $models.data | ForEach-Object { Write-Host "    - $($_.id)" }
} catch {
    Write-Host "    (could not reach proxy — check codemie proxy status)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Starting relay on port 4002 (Ctrl+C to stop)..." -ForegroundColor Green
node $relayDest