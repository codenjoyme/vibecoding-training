# Minimal MCP server in PowerShell
# Implements JSON-RPC 2.0 protocol

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Send-Response {
    param($id, $result)
    $response = @{
        jsonrpc = "2.0"
        id = $id
        result = $result
    } | ConvertTo-Json -Depth 10 -Compress
    [Console]::WriteLine($response)
}

function Send-Error {
    param($id, $code, $message)
    $response = @{
        jsonrpc = "2.0"
        id = $id
        error = @{
            code = $code
            message = $message
        }
    } | ConvertTo-Json -Compress
    [Console]::WriteLine($response)
}

# Main request processing loop
while ($true) {
    $line = [Console]::ReadLine()
    if ([string]::IsNullOrEmpty($line)) { continue }
    
    try {
        $request = $line | ConvertFrom-Json
        
        switch ($request.method) {
            "initialize" {
                Send-Response -id $request.id -result @{
                    protocolVersion = "2025-11-25"
                    capabilities = @{
                        tools = @{}
                    }
                    serverInfo = @{
                        name = "PowerShell MCP Demo"
                        version = "1.0.0"
                    }
                }
            }
            "tools/list" {
                Send-Response -id $request.id -result @{
                    tools = @(
                        @{
                            name = "echo"
                            description = "Returns text back"
                            inputSchema = @{
                                type = "object"
                                properties = @{
                                    text = @{
                                        type = "string"
                                        description = "Text to echo"
                                    }
                                }
                                required = @("text")
                            }
                        },
                        @{
                            name = "get_time"
                            description = "Returns current time"
                            inputSchema = @{
                                type = "object"
                                properties = @{}
                            }
                        },
                        @{
                            name = "calculate"
                            description = "Simple calculator"
                            inputSchema = @{
                                type = "object"
                                properties = @{
                                    a = @{ type = "number" }
                                    b = @{ type = "number" }
                                    operation = @{ 
                                        type = "string"
                                        enum = @("add", "subtract", "multiply", "divide")
                                    }
                                }
                                required = @("a", "b", "operation")
                            }
                        }
                    )
                }
            }
            "tools/call" {
                $toolName = $request.params.name
                $args = $request.params.arguments
                
                $result = switch ($toolName) {
                    "echo" {
                        @{
                            content = @(
                                @{
                                    type = "text"
                                    text = "Echo: $($args.text)"
                                }
                            )
                        }
                    }
                    "get_time" {
                        @{
                            content = @(
                                @{
                                    type = "text"
                                    text = "Current time: $((Get-Date).ToString('yyyy-MM-dd HH:mm:ss'))"
                                }
                            )
                        }
                    }
                    "calculate" {
                        $calcResult = switch ($args.operation) {
                            "add" { $args.a + $args.b }
                            "subtract" { $args.a - $args.b }
                            "multiply" { $args.a * $args.b }
                            "divide" { $args.a / $args.b }
                        }
                        @{
                            content = @(
                                @{
                                    type = "text"
                                    text = "Result: $($args.a) $($args.operation) $($args.b) = $calcResult"
                                }
                            )
                        }
                    }
                    default {
                        @{
                            content = @(
                                @{
                                    type = "text"
                                    text = "Unknown tool: $toolName"
                                }
                            )
                            isError = $true
                        }
                    }
                }
                
                Send-Response -id $request.id -result $result
            }
            default {
                Send-Error -id $request.id -code -32601 -message "Method not found: $($request.method)"
            }
        }
    }
    catch {
        Send-Error -id 0 -code -32700 -message "Parse error: $_"
    }
}
