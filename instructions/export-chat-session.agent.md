- Export GitHub Copilot chat sessions from VS Code / VS Code Insiders using standalone Python scripts.
- Scripts location: `./docs/modules/250-export-chat-session/tools/copilot/` package.
  + `chat_export.py` — main export tool (single session export, list, search).
  + `export_all.py` — batch export ALL sessions from ALL workspaces at once.
- Previously was a single file `copilot_chat_export.py` — now reorganized into `copilot/` package.
- No external dependencies required — uses only Python standard library.
- Supports both legacy `.json` and modern `.jsonl` (delta/CRDT) session formats.
- Auto-detects VS Code and VS Code Insiders installations on Windows, macOS, and Linux.

## Available Commands (chat_export.py)

- `workspaces` — list all VS Code workspaces that have chat sessions.
- `sessions <workspace_id>` — list all sessions in a specific workspace with title, message count, size, date.
- `export <workspace_id> <session_id>` — export one or more sessions to file.
- `search <text>` — full-text search across all sessions in all workspaces.

## Typical Workflow: Export CURRENT Session (Fastest)

When user asks to save/export the current chat session:

- Step 1: Generate a unique marker — random string of 10 uppercase Latin letters (e.g., `QWZXJKLMRT`).
  + Post this marker as a plain text message in the chat so it gets written to the session file.
  + Example: just write `Session marker: QWZXJKLMRT` in your response.
- Step 2: Search for the marker using `search "QWZXJKLMRT"`.
  + This instantly returns the workspace ID and session ID — no need to browse workspaces or sessions lists.
- Step 3: Export the session by running `export <workspace_id> <session_id>`.
  + Default format is HTML with dark theme, collapsible tool calls, and syntax highlighting.
  + Use `--format json` for raw JSON data or `--format text` for plain text.
  + Use `--output-dir <path>` to specify where to save exports.

**Why this works:** VS Code writes chat content to disk in near-real-time. The unique marker guarantees a single search hit pointing exactly to this session.

## Typical Workflow: Export ANY Session (Manual)

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

## Batch Export All Sessions (export_all.py)

- Exports ALL sessions from ALL workspaces in one command.
- Preserves directory structure: `<output_dir>/<VSCode Variant>/<workspace_name>/chat_<id>_<ts>.html`.
- Automatically skips sessions that have already been exported (idempotent re-runs).
- Default output directory: `./work/copilot_export_all/`.
- Supports `--format`, `--output-dir`, `--vscode-path` options.

### Batch Export Examples

```powershell
$batch = "./docs/modules/250-export-chat-session/tools/copilot/export_all.py"

# Export everything to default location (./work/copilot_export_all/)
python $batch

# Export to a custom directory
python $batch --output-dir ./my_exports

# Export all sessions as JSON instead of HTML
python $batch --format json

# Export only from specific VS Code variant
python $batch --vscode-path "C:/Users/user/AppData/Roaming/Code - Insiders"
```

### Batch Export Output Structure

```
work/copilot_export_all/
├── Code/
│   ├── my-project/
│   │   ├── chat_abc123def456_20260213_120000.html
│   │   └── chat_fed654cba321_20260213_120001.html
│   └── another-project/
│       └── ...
├── Code_-_Insiders/
│   ├── main-workspace/
│   │   └── ...
│   └── ...
```

## Single Session Command Examples

```powershell
# Set script path for convenience
$script = "./docs/modules/250-export-chat-session/tools/copilot/chat_export.py"

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
- `jsonl` — raw original JSONL file copy (lossless, no parsing).
  + Exact copy of the source session file.
  + Useful for archival or migration.
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
- `--format {html,json,jsonl,text}` — export format (default: `html`).
- All options can be placed after the subcommand name.

## Troubleshooting

- If `workspaces` shows 0 results — check that VS Code stores data in standard APPDATA location.
- If sessions show 0 messages — this was a known bug with JSONL parsing (fixed: key paths are lists, not strings).
- Unicode errors on Windows (cp1252) — script auto-sets UTF-8 output encoding.
- If export is empty or too small — session may still be active and not fully flushed to disk; try again after closing the chat tab.
