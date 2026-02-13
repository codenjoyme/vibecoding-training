import mcp.types as types
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Add the stuff directory to the path to import our library
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stuff'))
from simple_chat_exporter import SimpleChatExporter

async def tool_info() -> dict:
    """Returns information about the lng_copilot_chat_export_export_sessions tool."""
    return {
        "description": """Exports GitHub Copilot chat sessions to HTML format.

**Parameters:**
- `vscode_path` (string, required): Path to VS Code user settings directory
- `workspace_id` (string, required): Workspace ID containing the sessions
- `sessions` (string, required): Session selection - specific session ID, comma-separated IDs, or "*" for all sessions
- `output_dir` (string, optional): Output directory for HTML files (default: "work/copilot_export")

**Session Selection Examples:**
- Single session: `"abc123def456"`
- Multiple sessions: `"abc123,def456,ghi789"`
- All sessions: `"*"`

**Example Usage:**
- Export single session: `{"vscode_path": "C:/Users/YourName/AppData/Roaming/Code", "workspace_id": "abc123def456", "sessions": "session123"}`
- Export multiple: `{"vscode_path": "C:/Users/YourName/AppData/Roaming/Code", "workspace_id": "abc123def456", "sessions": "session1,session2"}`
- Export all: `{"vscode_path": "C:/Users/YourName/AppData/Roaming/Code", "workspace_id": "abc123def456", "sessions": "*"}`

**Returns:**
- JSON object with export results including:
  - exported_files: Array of successfully exported file paths
  - failed_sessions: Array of sessions that failed to export
  - total_exported: Number of successfully exported sessions
  - output_directory: Directory where files were saved

**Note:** The HTML files include interactive features, tool call details, and VS Code-like styling.""",
        "schema": {
            "type": "object",
            "properties": {
                "vscode_path": {
                    "type": "string",
                    "description": "Path to VS Code user settings directory"
                },
                "workspace_id": {
                    "type": "string",
                    "description": "Workspace ID containing the sessions"
                },
                "sessions": {
                    "type": "string",
                    "description": "Session selection: specific ID, comma-separated IDs, or '*' for all"
                },
                "output_dir": {
                    "type": "string",
                    "description": "Output directory for HTML files (default: 'work/copilot_export')"
                }
            },
            "required": ["vscode_path", "workspace_id", "sessions"]
        }
    }

async def run_tool(name: str, parameters: dict) -> list[types.Content]:
    """Exports GitHub Copilot chat sessions to HTML format."""
    try:
        vscode_path = parameters.get("vscode_path", "")
        workspace_id = parameters.get("workspace_id", "")
        sessions_param = parameters.get("sessions", "")
        output_dir = parameters.get("output_dir", "work/copilot_export")
        
        if not vscode_path:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "vscode_path parameter is required"
            }))]
        
        if not workspace_id:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "workspace_id parameter is required"
            }))]
        
        if not sessions_param:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "sessions parameter is required"
            }))]
        
        # Expand user path if needed
        vscode_path = os.path.expanduser(vscode_path)
        
        if not os.path.exists(vscode_path):
            return [types.TextContent(type="text", text=json.dumps({
                "error": f"VS Code path does not exist: {vscode_path}"
            }))]
        
        # Create exporter
        exporter = SimpleChatExporter(vscode_path, output_dir)
        
        # Determine which sessions to export
        target_sessions = []
        if sessions_param == "*":
            # Export all sessions in workspace
            all_sessions = exporter.list_sessions_in_workspace(workspace_id)
            target_sessions = [s['id'] for s in all_sessions]
        else:
            # Parse comma-separated session IDs
            target_sessions = [s.strip() for s in sessions_param.split(",") if s.strip()]
        
        if not target_sessions:
            return [types.TextContent(type="text", text=json.dumps({
                "error": "No sessions found to export",
                "sessions_param": sessions_param
            }))]
        
        # Export sessions
        exported_files = []
        failed_sessions = []
        
        for session_id in target_sessions:
            try:
                output_filename = f"chat_{workspace_id}_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                exported_file = exporter.export_session(workspace_id, session_id, output_filename)
                
                if exported_file:
                    exported_files.append({
                        "session_id": session_id,
                        "file_path": exported_file,
                        "file_size": os.path.getsize(exported_file)
                    })
                else:
                    failed_sessions.append({
                        "session_id": session_id,
                        "error": "Session not found or failed to read"
                    })
            except Exception as e:
                failed_sessions.append({
                    "session_id": session_id,
                    "error": str(e)
                })
        
        result = {
            "exported_files": exported_files,
            "failed_sessions": failed_sessions,
            "total_exported": len(exported_files),
            "total_failed": len(failed_sessions),
            "output_directory": str(Path(output_dir).resolve()),
            "workspace_id": workspace_id,
            "target_sessions": target_sessions
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
    except Exception as e:
        return [types.TextContent(type="text", text=json.dumps({
            "error": f"Failed to export sessions: {str(e)}"
        }))]
