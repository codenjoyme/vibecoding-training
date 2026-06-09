# list-codemie-models.ps1 — List all models available via CodeMie proxy
# Run from the module tools directory:
#   cd modules/175-codemie-cli/tools
#   .\list-codemie-models.ps1
#
# Requires: codemie proxy running (codemie proxy start)

$ErrorActionPreference = 'Stop'

$proxyUrl = "http://127.0.0.1:4001/v1/models"
$headers  = @{ Authorization = "Bearer codemie-proxy" }

try {
    $response = Invoke-RestMethod -Uri $proxyUrl -Headers $headers -Method Get
    $models = $response.data | Sort-Object id

    Write-Host ""
    Write-Host "Available CodeMie models ($($models.Count) total):" -ForegroundColor Cyan
    Write-Host ""
    $models | ForEach-Object { Write-Host "  $($_.id)" }
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "ERROR: Could not reach CodeMie proxy at $proxyUrl" -ForegroundColor Red
    Write-Host "Make sure the proxy is running: codemie proxy start" -ForegroundColor Yellow
    Write-Host ""
}
