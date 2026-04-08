#!/bin/bash
# MCP Image Viewer — Bash MCP Server (Linux/macOS)
# Returns local image files as base64 image content in MCP protocol format.
# Implements JSON-RPC 2.0 over stdio — same pattern as mcp-echo.sh.
#
# MCP image content type reference (from chrome-devtools-mcp/screenshot.js):
#   { type: "image", mimeType: "image/png", data: "<base64>" }

set -e

send_response() {
    local id=$1
    local result=$2
    echo "{\"jsonrpc\":\"2.0\",\"id\":$id,\"result\":$result}"
}

send_error() {
    local id=$1
    local code=$2
    local message=$3
    echo "{\"jsonrpc\":\"2.0\",\"id\":$id,\"error\":{\"code\":$code,\"message\":\"$message\"}}"
}

get_mime_type() {
    local file="$1"
    case "${file##*.}" in
        png)  echo "image/png" ;;
        jpg|jpeg) echo "image/jpeg" ;;
        gif)  echo "image/gif" ;;
        webp) echo "image/webp" ;;
        bmp)  echo "image/bmp" ;;
        svg)  echo "image/svg+xml" ;;
        *)    echo "application/octet-stream" ;;
    esac
}

TOOLS_LIST='{"tools":[{"name":"load_image","description":"Load a local image file and return it as base64 image content so the AI can see and analyze it.","inputSchema":{"type":"object","properties":{"filePath":{"type":"string","description":"Absolute path to the image file (png, jpg, gif, webp, bmp, svg)."}},"required":["filePath"]}}]}'

while IFS= read -r line; do
    [ -z "$line" ] && continue

    method=$(echo "$line" | grep -o '"method":"[^"]*"' | cut -d'"' -f4)
    id=$(echo "$line"     | grep -o '"id":[^,}]*'     | cut -d':' -f2 | tr -d ' ')

    case "$method" in
        "initialize")
            result='{"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"MCP Image Viewer","version":"1.0.0"}}'
            send_response "$id" "$result"
            ;;

        "tools/list")
            send_response "$id" "$TOOLS_LIST"
            ;;

        "tools/call")
            tool_name=$(echo "$line" | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)

            case "$tool_name" in
                "load_image")
                    file_path=$(echo "$line" | grep -o '"filePath":"[^"]*"' | cut -d'"' -f4)

                    if [ ! -f "$file_path" ]; then
                        result="{\"content\":[{\"type\":\"text\",\"text\":\"Error: file not found: $file_path\"}],\"isError\":true}"
                        send_response "$id" "$result"
                        continue
                    fi

                    mime_type=$(get_mime_type "$file_path")
                    file_name=$(basename "$file_path")
                    base64_data=$(base64 -w 0 "$file_path" 2>/dev/null || base64 "$file_path")

                    result="{\"content\":[{\"type\":\"text\",\"text\":\"Loaded image: $file_name\"},{\"type\":\"image\",\"mimeType\":\"$mime_type\",\"data\":\"$base64_data\"}]}"
                    send_response "$id" "$result"
                    ;;

                *)
                    result="{\"content\":[{\"type\":\"text\",\"text\":\"Unknown tool: $tool_name\"}],\"isError\":true}"
                    send_response "$id" "$result"
                    ;;
            esac
            ;;

        "notifications/initialized")
            # Notification — no response needed
            ;;

        *)
            if [ -n "$id" ] && [ "$id" != "null" ]; then
                send_error "$id" -32601 "Method not found: $method"
            fi
            ;;
    esac
done
