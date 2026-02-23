# REST server in PowerShell - same 3 tools as MCP echo server
# Endpoints: POST /echo, GET /time, POST /calculate, POST /upload
# Requires no external dependencies - uses built-in .NET HttpListener

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$port = 8080
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()

Write-Host "REST server running at http://localhost:$port"
Write-Host "Available endpoints:"
Write-Host "  POST /echo        - body: {`"text`": `"hello`"}"
Write-Host "  GET  /time        - returns current timestamp"
Write-Host "  POST /calculate   - body: {`"a`": 10, `"b`": 5, `"operation`": `"add`"}"
Write-Host "  POST /upload      - multipart file upload (binary demo)"
Write-Host "Press Ctrl+C to stop"
Write-Host ""

function Write-JsonResponse {
    param($context, $data, [int]$statusCode = 200)
    $json = $data | ConvertTo-Json -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $context.Response.StatusCode = $statusCode
    $context.Response.ContentType = "application/json; charset=utf-8"
    $context.Response.ContentLength64 = $bytes.Length
    $context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    $context.Response.OutputStream.Close()
}

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $request = $context.Request
        $path = $request.Url.AbsolutePath
        $method = $request.HttpMethod

        Write-Host "[$method] $path"

        switch ("$method $path") {

            "POST /echo" {
                $body = [System.IO.StreamReader]::new($request.InputStream).ReadToEnd()
                $data = $body | ConvertFrom-Json
                Write-JsonResponse -context $context -data @{
                    result = "Echo: $($data.text)"
                }
            }

            "GET /time" {
                Write-JsonResponse -context $context -data @{
                    result = "Current time: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))"
                }
            }

            "POST /calculate" {
                $body = [System.IO.StreamReader]::new($request.InputStream).ReadToEnd()
                $data = $body | ConvertFrom-Json
                $calcResult = switch ($data.operation) {
                    "add"      { $data.a + $data.b }
                    "subtract" { $data.a - $data.b }
                    "multiply" { $data.a * $data.b }
                    "divide"   { $data.a / $data.b }
                    default    { $null }
                }
                if ($null -eq $calcResult) {
                    Write-JsonResponse -context $context -data @{ error = "Unknown operation: $($data.operation)" } -statusCode 400
                } else {
                    Write-JsonResponse -context $context -data @{
                        result = "Result: $($data.a) $($data.operation) $($data.b) = $calcResult"
                    }
                }
            }

            "POST /upload" {
                # Read raw body bytes to simulate binary file upload
                $stream = $request.InputStream
                $buffer = [byte[]]::new(1MB)
                $totalBytes = 0
                $bytesRead = 0
                do {
                    $bytesRead = $stream.Read($buffer, $totalBytes, $buffer.Length - $totalBytes)
                    $totalBytes += $bytesRead
                } while ($bytesRead -gt 0 -and $totalBytes -lt $buffer.Length)

                $contentType = $request.ContentType
                Write-JsonResponse -context $context -data @{
                    result       = "File received successfully"
                    bytes        = $totalBytes
                    content_type = $contentType
                    note         = "Binary data arrived intact - no encoding needed"
                }
            }

            default {
                Write-JsonResponse -context $context -data @{ error = "Not found: $path" } -statusCode 404
            }
        }
    }
    catch [System.Net.HttpListenerException] {
        # Listener was stopped - exit cleanly
        break
    }
    catch {
        Write-Host "Error: $_"
    }
}

$listener.Stop()
Write-Host "Server stopped."
