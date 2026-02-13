# lng_copilot/chat_export - GitHub Copilot Chat Export Tools

Tools for exporting and managing GitHub Copilot chat sessions from VS Code workspace storage.

## Overview

These tools allow you to:
1. **Discover workspaces** with chat sessions
2. **List chat sessions** in specific workspaces  
3. **Export chat sessions** to beautiful HTML format with VS Code-like styling

The exported HTML files include:
- Interactive tool call details
- Markdown rendering
- File attachments and inline references
- Dark theme matching VS Code
- Expandable sections for detailed information

## Tools

### lng_copilot_chat_export_list_workspaces
Lists all VS Code workspaces that contain GitHub Copilot chat sessions.

**Use this first** to discover available workspaces and their IDs.

### lng_copilot_chat_export_list_sessions  
Lists all chat sessions in a specific workspace with metadata like file size, modification time, and message count.

**Use this second** to see available sessions in a workspace.

### lng_copilot_chat_export_export_sessions
Exports selected chat sessions to HTML format with full fidelity including tool calls, attachments, and interactive features.

**Use this last** to export the actual chat sessions.

## Workflow

1. **Find workspaces**: Use `list_workspaces` to get workspace IDs
2. **List sessions**: Use `list_sessions` to see available sessions  
3. **Export sessions**: Use `export_sessions` to create HTML files

## Usage Examples

### Step 1: Find Workspaces

```bash
# Windows
python -m mcp_server.run run lng_copilot_chat_export_list_workspaces '{\"vscode_path\":\"C:/Users/YourName/AppData/Roaming/Code\"}'

# macOS  
python -m mcp_server.run run lng_copilot_chat_export_list_workspaces '{\"vscode_path\":\"~/Library/Application Support/Code\"}'

# Linux
python -m mcp_server.run run lng_copilot_chat_export_list_workspaces '{\"vscode_path\":\"~/.config/Code\"}'
```

### Step 2: List Sessions in Workspace

```bash
python -m mcp_server.run run lng_copilot_chat_export_list_sessions '{\"vscode_path\":\"C:/Users/YourName/AppData/Roaming/Code\",\"workspace_id\":\"abc123def456\"}'
```

### Step 3: Export Sessions

```bash
# Export single session
python -m mcp_server.run run lng_copilot_chat_export_export_sessions '{\"vscode_path\":\"C:/Users/YourName/AppData/Roaming/Code\",\"workspace_id\":\"abc123def456\",\"sessions\":\"session123\"}'

# Export multiple sessions
python -m mcp_server.run run lng_copilot_chat_export_export_sessions '{\"vscode_path\":\"C:/Users/YourName/AppData/Roaming/Code\",\"workspace_id\":\"abc123def456\",\"sessions\":\"session1,session2,session3\"}'

# Export ALL sessions in workspace
python -m mcp_server.run run lng_copilot_chat_export_export_sessions '{\"vscode_path\":\"C:/Users/YourName/AppData/Roaming/Code\",\"workspace_id\":\"abc123def456\",\"sessions\":\"*\"}'

# Export to custom directory
python -m mcp_server.run run lng_copilot_chat_export_export_sessions '{\"vscode_path\":\"C:/Users/YourName/AppData/Roaming/Code\",\"workspace_id\":\"abc123def456\",\"sessions\":\"*\",\"output_dir\":\"my_exports\"}'
```

## VS Code Paths by OS

### Windows
- **VS Code**: `C:/Users/YourName/AppData/Roaming/Code`
- **VS Code Insiders**: `C:/Users/YourName/AppData/Roaming/Code - Insiders`

### macOS
- **VS Code**: `~/Library/Application Support/Code`
- **VS Code Insiders**: `~/Library/Application Support/Code - Insiders`

### Linux  
- **VS Code**: `~/.config/Code`
- **VS Code Insiders**: `~/.config/Code - Insiders`

## Output Format

The exported HTML files include:

- **VS Code Dark Theme**: Matches the familiar dark interface
- **Interactive Tool Calls**: Click to expand/collapse tool execution details
- **Markdown Rendering**: Proper formatting for code blocks, headers, lists
- **File References**: Clickable file links with folder icons
- **Tool Call Details**: Input/output parameters, execution status
- **Message Threading**: Clear separation between user and assistant messages
- **Timestamps**: File modification and export timestamps

## Important Notes

1. **Close VS Code**: Make sure VS Code is closed when running these tools to avoid file access conflicts
2. **Workspace Storage**: These tools read from VS Code's internal workspace storage, not your project files
3. **Chat History**: Only chat sessions that were saved by VS Code will be available
4. **Large Files**: Very large chat sessions may take longer to process
5. **Output Directory**: Default output directory is `work/copilot_export` (created automatically)

## Troubleshooting

### "No workspaces found"
- Make sure VS Code path is correct for your OS
- Verify you have used GitHub Copilot Chat in VS Code
- Check that the path exists and contains a `User/workspaceStorage` directory

### "Session not found"  
- Session may have been deleted by VS Code
- Use `list_sessions` to get current valid session IDs
- Make sure workspace ID is correct

### "Permission denied"
- Close VS Code completely
- Check file system permissions on the VS Code directory
- Try running from an elevated terminal (if needed)

## Stuff Directory

The `stuff` directory contains:
- **simple_chat_exporter.py**: Original standalone script (moved from project root)
- **copilot_chat_lib.py**: Shared library with core export functionality

Use the standalone script if you prefer command-line usage outside of MCP.
