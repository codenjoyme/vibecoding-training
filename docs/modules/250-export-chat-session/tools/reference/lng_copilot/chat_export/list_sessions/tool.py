import mcp.types as types
import json
import sys
import os
from pathlib import Path

# Add the stuff directory to the path to import our library
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stuff'))
from simple_chat_exporter import SimpleChatExporter

async def tool_info() -> dict:
    """Returns information about the lng_copilot_chat_export_list_sessions tool."""
    return {
        "description": """Lists all GitHub Copilot chat sessions in a specific VS Code workspace.

**Parameters:**
- `vscode_path` (string, required): Path to VS Code user settings directory
- `workspace_id` (string, required): Workspace ID to list sessions from (get from list_workspaces tool)

**Example Usage:**
- List sessions: `{"vscode_path": "C:/Users/YourName/AppData/Roaming/Code", "workspace_id": "abc123def456"}`

**Returns:**
- JSON object with session information including:
  - sessions: Array of session objects with id, file_path, file_size, modified_time, messages_count
  - total_sessions: Total number of sessions found
  - workspace_id: The workspace ID that was searched

**Note:** Use the lng_copilot_chat_export_list_workspaces tool first to get available workspace IDs.""",
        "schema": {
            "type": "object",
            "properties": {
                "vscode_path": {
                    "type": "string",
                    "description": "Path to VS Code user settings directory"
                },
                "workspace_id": {
                    "type": "string",
                    "description": "Workspace ID to list sessions from"
                }
            },
            "required": ["vscode_path", "workspace_id"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Lists all GitHub Copilot chat sessions in a specific workspace."""
    try:
        vscode_path = parameters.get("vscode_path", "")
        workspace_id = parameters.get("workspace_id", "")
        
        if not vscode_path:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "vscode_path parameter is required"
            }))]
        
        if not workspace_id:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "workspace_id parameter is required"
            }))]
        
        # Expand user path if needed
        vscode_path = os.path.expanduser(vscode_path)
        
        if not os.path.exists(vscode_path):
            return [types.TextContent(type="text", text=json.dumps({
                "error": f"VS Code path does not exist: {vscode_path}"
            }))]
        
        # Create exporter and list sessions
        exporter = SimpleChatExporter(vscode_path)
        sessions = exporter.list_sessions_in_workspace(workspace_id)
        
        if not sessions:
            return [types.TextContent(type="text", text=json.dumps({
                "sessions": [],
                "total_sessions": 0,
                "workspace_id": workspace_id,
                "message": f"No chat sessions found in workspace {workspace_id}"
            }))]
        
        # Sort sessions by modified time (newest first)
        sessions.sort(key=lambda x: x['modified_time'], reverse=True)
        
        result = {
            "sessions": sessions,
            "total_sessions": len(sessions),
            "workspace_id": workspace_id,
            "vscode_path": vscode_path
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Failed to list sessions: {str(e)}"
        }))]
