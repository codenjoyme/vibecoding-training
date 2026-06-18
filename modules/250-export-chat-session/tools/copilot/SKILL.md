---
name: copilot-chat-export
description: >-
  Export, list, and search GitHub Copilot chat sessions from VS Code (both
  stable and Insiders) to HTML, JSON, JSONL, or text. Use when the user wants
  to save, share, back up, summarize, or search past Copilot chat conversations.
---

# Copilot Chat Export

Standalone Python tools that read VS Code's internal chat storage and convert
sessions to portable formats. No external dependencies — Python 3 only.
Supports both the legacy `.json` and the modern `.jsonl` (delta/CRDT) session
formats.

## When to use

- "Export / save / share my Copilot chat session"
- "Back up all my AI conversations"
- "Search my chat history for <topic>"
- "Make an HTML / JSON copy of this session"

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/chat_export.py` | List workspaces & sessions, export one or many sessions, search across all history |
| `scripts/export_all.py` | Batch-export every session from every workspace, preserving folder structure |

## Usage

Run from the repository root.

### Discover

```bash
# List all workspaces that have chat history
python ./modules/250-export-chat-session/tools/copilot/scripts/chat_export.py workspaces

# List sessions inside one workspace
python ./modules/250-export-chat-session/tools/copilot/scripts/chat_export.py sessions <workspace_id>
```

### Export

```bash
# One session to HTML (default format)
python ./modules/250-export-chat-session/tools/copilot/scripts/chat_export.py export <workspace_id> <session_id> --output-dir ./work/copilot_export --format html

# Other formats: json | jsonl | text
python ./modules/250-export-chat-session/tools/copilot/scripts/chat_export.py export <workspace_id> <session_id> --format json

# All sessions in one workspace
python ./modules/250-export-chat-session/tools/copilot/scripts/chat_export.py export <workspace_id> * --output-dir ./work/copilot_export
```

### Search

```bash
python ./modules/250-export-chat-session/tools/copilot/scripts/chat_export.py search "github mcp"
```

### Batch export everything

```bash
python ./modules/250-export-chat-session/tools/copilot/scripts/export_all.py
python ./modules/250-export-chat-session/tools/copilot/scripts/export_all.py --output-dir ./work/my_backup
python ./modules/250-export-chat-session/tools/copilot/scripts/export_all.py --format json
```

## Options

| Option | Meaning |
|--------|---------|
| `--vscode-path PATH` | Override the VS Code settings path (auto-detects Code and Code Insiders by default) |
| `--output-dir DIR` | Output directory (default `./work/copilot_export`) |
| `--format FORMAT` | `html` (default), `json`, `jsonl`, or `text` |

## Output formats

- **html** — standalone, styled, shareable; open in any browser.
- **json** — structured; for scripting / analysis / redaction.
- **jsonl** — raw VS Code internal copy; for backup / archival.
- **text** — plain text; for quick reading or piping.

## Security note

Exported sessions may contain secrets, tokens, file contents, or customer data.
Treat them like server logs: review before sharing externally, and redact
sensitive patterns when exporting for a public audience.
