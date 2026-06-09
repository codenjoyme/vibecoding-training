# start.ps1 - CodeMie relay startup script
# Run from the module tools directory:
#   cd modules/175-codemie-cli/tools
#   .\start.ps1

Set-StrictMode -Off
$ErrorActionPreference = 'SilentlyContinue'

# --- 1. Kill existing codemie proxy and relay processes ---
Write-Host ""
Write-Host "[1/4] Stopping existing processes..." -ForegroundColor Cyan

Get-Process -Name "node" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*codemie-relay*" } |
    Stop-Process -Force -ErrorAction SilentlyContinue

& codemie proxy stop 2>$null
Start-Sleep -Milliseconds 500
Write-Host "  Done." -ForegroundColor Green

# --- 2. Show available CodeMie models ---
Write-Host ""
Write-Host "[2/4] Available CodeMie models:" -ForegroundColor Cyan
try {
    $models = Invoke-RestMethod -Uri "http://127.0.0.1:4001/v1/models" `
        -Headers @{ Authorization = "Bearer codemie-proxy" } `
        -ErrorAction Stop
    $models.data | ForEach-Object { Write-Host "  - $($_.id)" }
} catch {
    Write-Host "  (proxy not running yet - will start in step 4)" -ForegroundColor Yellow
}

# --- 3. Show chatLanguageModels.json location and current content ---
Write-Host ""
Write-Host "[3/4] chatLanguageModels.json - where to configure Copilot models:" -ForegroundColor Cyan

$configPaths = @(
    "$env:APPDATA\Code - Insiders\User\chatLanguageModels.json",
    "$env:APPDATA\Code\User\chatLanguageModels.json"
)

$foundConfig = $null
foreach ($p in $configPaths) {
    if (Test-Path $p) { $foundConfig = $p; break }
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
    Write-Host "  Create it from chatLanguageModels.js in this folder." -ForegroundColor Yellow
}

Write-Host ""
$refPath = (Resolve-Path ".\chatLanguageModels.js").Path
Write-Host "  Reference config: $refPath" -ForegroundColor DarkGray
Write-Host "  MODEL_MAP is built automatically from chatLanguageModels.json at relay startup." -ForegroundColor DarkGray
Write-Host "  To add a new model - add an entry with realModelId field and restart relay." -ForegroundColor DarkGray

# --- 4. Start codemie proxy + relay ---
Write-Host ""
Write-Host "[4/4] Starting proxies..." -ForegroundColor Cyan

& codemie proxy start
Start-Sleep -Milliseconds 800

$relayDest = "$env:USERPROFILE\.local\bin\codemie-relay.js"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.local\bin" | Out-Null
Copy-Item ".\codemie-relay.js" $relayDest -Force
Write-Host "  Relay copied to: $relayDest" -ForegroundColor Green

Write-Host ""
Write-Host "  Available models (from proxy):" -ForegroundColor Cyan
try {
    $models = Invoke-RestMethod -Uri "http://127.0.0.1:4001/v1/models" `
        -Headers @{ Authorization = "Bearer codemie-proxy" } `
        -ErrorAction Stop
    $models.data | ForEach-Object { Write-Host "    - $($_.id)" }
} catch {
    Write-Host "    (could not reach proxy - check codemie proxy status)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "  Starting relay on port 4002 (Ctrl+C to stop)..." -ForegroundColor Green
node $relayDest
