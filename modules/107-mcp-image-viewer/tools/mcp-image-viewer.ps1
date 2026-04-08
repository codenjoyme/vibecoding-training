# MCP Image Viewer — PowerShell MCP Server
# Returns local image files as base64 image content in MCP protocol format.
# Implements JSON-RPC 2.0 over stdio — same pattern as mcp-echo.ps1.
#
# MCP image content type reference (from chrome-devtools-mcp/screenshot.js):
#   response.attachImage({ mimeType: "image/png", data: <base64> })
# Maps to JSON content item: { type: "image", mimeType: "image/png", data: "<base64>" }

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$OutputEncoding           = [System.Text.Encoding]::UTF8

function Send-Response {
    param($id, $result)
    $response = @{ jsonrpc = "2.0"; id = $id; result = $result } |
        ConvertTo-Json -Depth 10 -Compress
    [Console]::WriteLine($response)
}

function Send-Error {
    param($id, $code, $message)
    $response = @{
        jsonrpc = "2.0"; id = $id
        error   = @{ code = $code; message = $message }
    } | ConvertTo-Json -Compress
    [Console]::WriteLine($response)
}

function Get-MimeType {
    param([string]$filePath)
    switch ([System.IO.Path]::GetExtension($filePath).ToLower()) {
        ".png"  { "image/png" }
        ".jpg"  { "image/jpeg" }
        ".jpeg" { "image/jpeg" }
        ".gif"  { "image/gif" }
        ".webp" { "image/webp" }
        ".bmp"  { "image/bmp" }
        ".svg"  { "image/svg+xml" }
        default { "application/octet-stream" }
    }
}

while ($true) {
    $line = [Console]::ReadLine()
    if ([string]::IsNullOrEmpty($line)) { continue }

    try {
        $req = $line | ConvertFrom-Json

        switch ($req.method) {

            "initialize" {
                Send-Response -id $req.id -result @{
                    protocolVersion = "2025-11-25"
                    capabilities    = @{ tools = @{} }
                    serverInfo      = @{ name = "MCP Image Viewer"; version = "1.0.0" }
                }
            }

            "tools/list" {
                Send-Response -id $req.id -result @{
                    tools = @(
                        @{
                            name        = "load_image"
                            description = "Load a local image file and return it as base64 image content so the AI can see and analyze it."
                            inputSchema = @{
                                type       = "object"
                                properties = @{
                                    filePath = @{
                                        type        = "string"
                                        description = "Absolute path to the image file (png, jpg, gif, webp, bmp, svg)."
                                    }
                                }
                                required   = @("filePath")
                            }
                        }
                    )
                }
            }

            "tools/call" {
                $toolName = $req.params.name
                $args     = $req.params.arguments

                if ($toolName -eq "load_image") {
                    $filePath = [System.IO.Path]::GetFullPath($args.filePath)

                    if (-not (Test-Path -LiteralPath $filePath)) {
                        Send-Response -id $req.id -result @{
                            content = @(@{ type = "text"; text = "Error: file not found: $filePath" })
                            isError = $true
                        }
                        continue
                    }

                    $bytes    = [System.IO.File]::ReadAllBytes($filePath)
                    $base64   = [Convert]::ToBase64String($bytes)
                    $mimeType = Get-MimeType -filePath $filePath
                    $fileName = [System.IO.Path]::GetFileName($filePath)

                    Send-Response -id $req.id -result @{
                        content = @(
                            @{ type = "text";  text     = "Loaded image: $fileName" }
                            @{ type = "image"; mimeType = $mimeType; data = $base64 }
                        )
                    }
                }
                else {
                    Send-Response -id $req.id -result @{
                        content = @(@{ type = "text"; text = "Unknown tool: $toolName" })
                        isError = $true
                    }
                }
            }

            "notifications/initialized" {
                # No response required for notifications
            }

            default {
                if ($req.id) {
                    Send-Error -id $req.id -code -32601 -message "Method not found: $($req.method)"
                }
            }
        }
    }
    catch {
        if ($req -and $req.id) {
            Send-Error -id $req.id -code -32603 -message "Internal error: $_"
        }
    }
}
