$apiKey = "YOUR_API_KEY_HERE"
$baseUrl = "https://ai-proxy.lab.epam.com"

$headers = @{
    "api-key" = $apiKey
}

# Вариант 1: /openai/models
try {
    Write-Host "Trying /openai/models..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/openai/models" -Method Get -Headers $headers
    $response.data | ForEach-Object { Write-Host $_.id -ForegroundColor Green }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Вариант 2: /openai/deployments
try {
    Write-Host "`nTrying /openai/deployments..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "$baseUrl/openai/deployments" -Method Get -Headers $headers
    $response.data | ForEach-Object { Write-Host $_.id -ForegroundColor Green }
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}