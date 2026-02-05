# PowerShell script to test EPAM AI DIAL connection
# Replace YOUR_API_KEY_HERE with your actual API key from EPAM support

$apiKey = "YOUR_API_KEY_HERE"
$endpoint = "https://ai-proxy.lab.epam.com/openai/deployments/gpt-4o-mini-2024-07-18/chat/completions"

Write-Host "Testing EPAM AI DIAL connection..." -ForegroundColor Yellow
Write-Host "Endpoint: $endpoint" -ForegroundColor Cyan
Write-Host ""

$body = @{
    messages = @(
        @{
            role = "user"
            content = "Tell me about artificial intelligence in the style of a pirate."
        }
    )
    max_tokens = 500
    temperature = 0.7
} | ConvertTo-Json -Depth 10

$headers = @{
    "Content-Type" = "application/json"
    "api-key" = $apiKey
}

try {
    Write-Host "Sending request to DIAL..." -ForegroundColor Yellow
    
    $response = Invoke-RestMethod -Uri $endpoint -Method Post -Headers $headers -Body $body
    
    Write-Host "`nSuccess! Response received:" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host $response.choices[0].message.content
    Write-Host "================================" -ForegroundColor Green
    Write-Host "`nModel used: $($response.model)" -ForegroundColor Cyan
    Write-Host "Tokens used: $($response.usage.total_tokens)" -ForegroundColor Cyan
    
} catch {
    Write-Host "`nError occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`nTroubleshooting tips:" -ForegroundColor Yellow
    Write-Host "1. Verify your API key is correct" -ForegroundColor White
    Write-Host "2. Ensure you're connected to EPAM VPN" -ForegroundColor White
    Write-Host "3. Check that the model deployment name is current" -ForegroundColor White
}
