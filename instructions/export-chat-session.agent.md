- Export GitHub Copilot chat sessions from VS Code / VS Code Insiders using standalone Python script.
- Script location: `./docs/modules/250-export-chat-session/tools/copilot_chat_export.py`.
- No external dependencies required — uses only Python standard library.
- Supports both legacy `.json` and modern `.jsonl` (delta/CRDT) session formats.
- Auto-detects VS Code and VS Code Insiders installations on Windows, macOS, and Linux.

## Available Commands

- `workspaces` — list all VS Code workspaces that have chat sessions.
- `sessions <workspace_id>` — list all sessions in a specific workspace with title, message count, size, date.
- `export <workspace_id> <session_id>` — export one or more sessions to file.
- `search <text>` — full-text search across all sessions in all workspaces.

## Typical Workflow

- Step 1: find the workspace by running `workspaces` command.
  + Copy the workspace ID from the output (32-char hex string).
- Step 2: list sessions in that workspace by running `sessions <workspace_id>`.
  + Identify the session you need by title, date, or message count.
  + Copy the session ID (UUID format).
- Step 3: export the session by running `export <workspace_id> <session_id>`.
  + Default format is HTML with dark theme, collapsible tool calls, and syntax highlighting.
  + Use `--format json` for raw JSON data or `--format text` for plain text.
  + Use `--output-dir <path>` to specify where to save exports.
- Alternative: search for a session by text content using `search "keyword"`.
  + Returns matching session IDs, workspace names, and VS Code variant.

## Command Examples

```powershell
# Set script path for convenience
$script = "./docs/modules/250-export-chat-session/tools/copilot_chat_export.py"

# List all workspaces
python $script workspaces

# List sessions in a workspace
python $script sessions abc123def456

# Export a single session to HTML
python $script export abc123def456 session-uuid-here

# Export to JSON format with custom output directory
python $script export abc123def456 session-uuid-here --format json --output-dir ./work/exports

# Export all sessions from a workspace
python $script export abc123def456 *

# Export multiple sessions (comma-separated)
python $script export abc123def456 uuid1,uuid2,uuid3

# Search for text across all sessions
python $script search "some important text"

# Override VS Code path if auto-detect fails
python $script workspaces --vscode-path "C:/Users/user/AppData/Roaming/Code - Insiders"
```

## Export Formats

- `html` (default) — standalone HTML file with dark GitHub-like theme.
  + Collapsible tool call blocks (click to expand/collapse).
  + File attachments and inline references rendered.
  + MCP tool calls formatted with server:tool naming.
  + User messages with context attachments.
  + Session metadata header (title, date, message count, model).
- `json` — raw reconstructed session data as JSON.
  + Full session object after JSONL delta reconstruction.
  + Useful for programmatic processing or archival.
- `text` — plain text conversation log.
  + User and assistant messages with timestamps.
  + Tool calls listed by name only (no input/output details).

## JSONL Delta Format (Technical Details)

- Modern VS Code stores sessions as `.jsonl` files (not `.json`).
- Line 0: `kind=0` — initial full session state (usually empty `requests: []`).
- Subsequent lines: deltas applied incrementally.
  + `kind=1` — set value at key path (e.g., `['customTitle']` or `['requests', 0, 'modelState']`).
  + `kind=2` — append items to array at key path (e.g., `['requests', 0, 'response']`).
- Key `k` is a JSON array like `['requests', 0, 'response']` (not a string).
- The script reconstructs full session by replaying all deltas sequentially.

## Common Options

- `--vscode-path PATH` — manually specify VS Code settings directory.
  + Useful when auto-detection fails or you want a specific VS Code variant.
- `--output-dir DIR` — output directory for exported files (default: `./copilot_export`).
- `--format {html,json,text}` — export format (default: `html`).
- All options can be placed after the subcommand name.

## Troubleshooting

- If `workspaces` shows 0 results — check that VS Code stores data in standard APPDATA location.
- If sessions show 0 messages — this was a known bug with JSONL parsing (fixed: key paths are lists, not strings).
- Unicode errors on Windows (cp1252) — script auto-sets UTF-8 output encoding.
- If export is empty or too small — session may still be active and not fully flushed to disk; try again after closing the chat tab.
