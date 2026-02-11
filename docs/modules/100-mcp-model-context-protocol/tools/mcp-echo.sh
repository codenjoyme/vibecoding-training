#!/bin/bash
# Minimal MCP server in Bash
# Implements JSON-RPC 2.0 protocol

set -e

# Function to send JSON response
send_response() {
    local id=$1
    local result=$2
    echo "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":$result}"
}

# Function to send error
send_error() {
    local id=$1
    local code=$2
    local message=$3
    echo "{\"jsonrpc\":\"2.0\",\"id\":$id,\"error\":{\"code\":$code,\"message\":\"$message\"}}"
}

# Function to extract JSON field (simple parser, no external deps)
get_json_field() {
    local json=$1
    local field=$2
    echo "$json" | grep -o "\"$field\":[^,}]*" | cut -d':' -f2- | tr -d '"' | tr -d ' '
}

# Function to get nested field
get_nested_field() {
    local json=$1
    local path=$2
    # Simple extraction for params.name, params.arguments.text, etc.
    echo "$json" | grep -o "\"$path\":[^,}]*" | cut -d':' -f2- | tr -d '"' | tr -d ' '
}

# Main request processing loop
while IFS= read -r line; do
    [ -z "$line" ] && continue
    
    # Extract method and id
    method=$(get_json_field "$line" "method")
    id=$(get_json_field "$line" "id")
    
    case "$method" in
        "initialize")
            result='{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"Bash MCP Demo","version":"1.0.0"}}'
            send_response "$id" "$result"
            ;;
        
        "notifications/initialized")
            # This is a notification, no response needed
            ;;
            
        "tools/list")
            result='{"tools":[{"name":"echo","description":"Returns text back","inputSchema":{"type":"object","properties":{"text":{"type":"string","description":"Text to echo"}},"required":["text"]}},{"name":"get_time","description":"Returns current time","inputSchema":{"type":"object","properties":{}}},{"name":"calculate","description":"Simple calculator","inputSchema":{"type":"object","properties":{"a":{"type":"number"},"b":{"type":"number"},"operation":{"type":"string","enum":["add","subtract","multiply","divide"]}},"required":["a","b","operation"]}}]}'
            send_response "$id" "$result"
            ;;
            
        "tools/call")
            # Extract tool name
            tool_name=$(echo "$line" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
            
            case "$tool_name" in
                "echo")
                    # Extract text argument
                    text=$(echo "$line" | grep -o '"text":"[^"]*"' | cut -d'"' -f4)
                    result="{\"content\":[{\"type\":\"text\",\"text\":\"Echo: $text\"}]}"
                    send_response "$id" "$result"
                    ;;
                    
                "get_time")
                    current_time=$(date '+%Y-%m-%d %H:%M:%S')
                    result="{\"content\":[{\"type\":\"text\",\"text\":\"Current time: $current_time\"}]}"
                    send_response "$id" "$result"
                    ;;
                    
                "calculate")
                    # Extract arguments (simplified parsing)
                    a=$(echo "$line" | grep -o '"a":[0-9.]*' | cut -d':' -f2)
                    b=$(echo "$line" | grep -o '"b":[0-9.]*' | cut -d':' -f2)
                    op=$(echo "$line" | grep -o '"operation":"[^"]*"' | cut -d'"' -f4)
                    
                    # Calculate result
                    case "$op" in
                        "add") calc_result=$(echo "$a + $b" | bc 2>/dev/null || echo "$((a + b))") ;;
                        "subtract") calc_result=$(echo "$a - $b" | bc 2>/dev/null || echo "$((a - b))") ;;
                        "multiply") calc_result=$(echo "$a * $b" | bc 2>/dev/null || echo "$((a * b))") ;;
                        "divide") calc_result=$(echo "scale=2; $a / $b" | bc 2>/dev/null || echo "$((a / b))") ;;
                        *) calc_result="unknown operation" ;;
                    esac
                    
                    result="{\"content\":[{\"type\":\"text\",\"text\":\"Result: $a $op $b = $calc_result\"}]}"
                    send_response "$id" "$result"
                    ;;
                    
                *)
                    result="{\"content\":[{\"type\":\"text\",\"text\":\"Unknown tool: $tool_name\"}],\"isError\":true}"
                    send_response "$id" "$result"
                    ;;
            esac
            ;;
            
        "notifications/initialized")
            # This is a notification, no response needed
            ;;
            
        *)
            # Only send error if it's a request (has id), not a notification
            if [ -n "$id" ] && [ "$id" != "null" ]; then
                send_error "$id" -32601 "Method not found: $method"
            fi
            ;;
    esac
done
