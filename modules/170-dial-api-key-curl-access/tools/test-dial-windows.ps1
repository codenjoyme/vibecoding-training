# PowerShell script to test DIAL connection
# Replace YOUR_API_KEY_HERE with your actual API key from support

$apiKey = "YOUR_API_KEY_HERE"
$endpoint = "https://ai-proxy.lab.epam.com/openai/deployments/anthropic.claude-opus-4-7/chat/completions"

Write-Host "Testing DIAL connection..." -ForegroundColor Yellow
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
    # temperature = 0.7
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
    
    # Получить детальное тело ошибки
    $streamReader = [System.IO.StreamReader]::new($_.Exception.Response.GetResponseStream())
    $errorBody = $streamReader.ReadToEnd()
    $streamReader.Close()
    Write-Host "`nError details:" -ForegroundColor Yellow
    Write-Host $errorBody -ForegroundColor Red
}
