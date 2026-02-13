import mcp.types as types
import json
import sys
import os
from pathlib import Path

# Add the stuff directory to the path to import our library
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stuff'))
from simple_chat_exporter import SimpleChatExporter

async def tool_info() -> dict:
    """Returns information about the lng_copilot_chat_export_list_workspaces tool."""
    return {
        "description": """Lists all VS Code workspaces that contain GitHub Copilot chat sessions.

**Parameters:**
- `vscode_path` (string, required): Path to VS Code user settings directory (e.g., 'C:/Users/YourName/AppData/Roaming/Code' or '~/.vscode')

**Example Usage:**
- List workspaces: `{"vscode_path": "C:/Users/YourName/AppData/Roaming/Code"}`
- Unix path: `{"vscode_path": "~/.vscode"}`

**Returns:**
- JSON array with workspace information including:
  - workspace_id: Unique identifier for the workspace
  - workspace_name: Human-readable workspace name
  - sessions_count: Number of chat sessions in the workspace
  - path: Full path to workspace directory

**Note:** Make sure VS Code is closed when using this tool to avoid file access conflicts.""",
        "schema": {
            "type": "object",
            "properties": {
                "vscode_path": {
                    "type": "string",
                    "description": "Path to VS Code user settings directory"
                }
            },
            "required": ["vscode_path"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Lists all VS Code workspaces with GitHub Copilot chat sessions."""
    try:
        vscode_path = parameters.get("vscode_path", "")
        
        if not vscode_path:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "vscode_path parameter is required"
            }))]
        
        # Expand user path if needed
        vscode_path = os.path.expanduser(vscode_path)
        
        if not os.path.exists(vscode_path):
            return [types.TextContent(type="text", text=json.dumps({
                "error": f"VS Code path does not exist: {vscode_path}"
            }))]
        
        # Create exporter and find workspaces
        exporter = SimpleChatExporter(vscode_path)
        workspaces = exporter.find_workspaces()
        
        if not workspaces:
            return [types.TextContent(type="text", text=json.dumps({
                "workspaces": [],
                "message": "No workspaces with chat sessions found"
            }))]
        
        # Format workspace information
        workspace_list = []
        for ws in workspaces:
            workspace_list.append({
                "workspace_id": ws['workspace_id'],
                "workspace_name": ws['workspace_name'],
                "sessions_count": ws['sessions_count'],
                "path": ws['path']
            })
        
        result = {
            "workspaces": workspace_list,
            "total_workspaces": len(workspace_list),
            "vscode_path": vscode_path
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Failed to list workspaces: {str(e)}"
        }))]
