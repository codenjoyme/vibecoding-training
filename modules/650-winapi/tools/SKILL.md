# WinAPI MCP Toolbox — SKILL.md

> **This file is both a human guide and an AI skill.** Hand it to your AI agent
> together with the contents of `scripts/`, and it has everything it needs to
> install, register, and start the server in either VS Code (GitHub Copilot)
> or Cursor.

---

## What This Tool Does

`winapi-mcp` is a self-contained Python MCP server that gives the agent direct
control over a Windows desktop:

| Tool | Purpose |
|---|---|
| `screenshot_window` | Capture a window by title (or class) substring; returns PNG as MCP image |
| `screenshot_area` | Capture a rectangle `(x1,y1)-(x2,y2)` of the screen; returns PNG as MCP image |
| `mouse_move` | Move the cursor to absolute `(x, y)` |
| `mouse_click` | Click at a point or current position; `left/right/middle`, single or double |
| `mouse_drag` | Drag from `(x1,y1)` to `(x2,y2)` with held button — drag-and-drop |
| `send_hotkey` | Send hotkeys, named keys, text, or sequences (`^t`, `F12`, plain text, `[{type, value}, ...]`); optionally focus a process by `pid` first |
| `clipboard_get` / `clipboard_set` | Read / write the system clipboard |
| `list_processes` | Enumerate processes (with optional name filter and "only with windows" mode) |
| `window_tree` | Dump window hierarchy `(hwnd, title, class)` for a `pid` |
| `get_window_content` | Deep UI-Automation dump (control type, name, position, children) for a `pid` |

Screenshots are returned as `{ "type": "image", "mimeType": "image/png", "data": "<base64>" }`
content — the same shape used by `chrome-devtools-mcp` and module 107's image viewer.
Every screenshot is also written to `scripts/output/` for later inspection.

---

## Files in This Skill

| Path (relative to module folder) | Purpose |
|---|---|
| `tools/scripts/server.py` | Single-file MCP server; one tool per Python function |
| `tools/scripts/requirements.txt` | Python dependencies (`mcp`, `mss`, `pywin32`, `psutil`, `pyautogui`, `pyperclip`, `pywinauto`, `Pillow`) |
| `tools/scripts/install.ps1` | One-shot bootstrap — creates `.venv`, installs deps, idempotent |
| `tools/scripts/run.ps1` | Entry point used by `mcp.json`; activates venv, launches `server.py` |
| `tools/scripts/output/` | Screenshots saved by the screenshot tools (gitignored) |
| `tools/scripts/test_client.py` | Optional smoke-test client — initializes, lists tools, takes a tiny screenshot, round-trips the clipboard |
| `tools/.vscode/mcp.json` | VS Code config template (key: `servers`) |
| `tools/.cursor/mcp.json` | Cursor config template (key: `mcpServers`) |
| `tools/.gitignore` | Keeps `.venv/`, `__pycache__/`, `output/` out of git |

---

## Platform Support

**Windows only.** This server depends on `pywin32`, `pywinauto`, and the WinAPI
window/keyboard primitives. It will not load on macOS or Linux.

---

## Step 1 — Install (once)

From the workspace root, in **PowerShell**:

```powershell
pwsh -ExecutionPolicy Bypass -File ./modules/650-winapi/tools/scripts/install.ps1
```

What this does:

1. Detects `python` / `py -3` on `PATH` (requires Python **3.10+**).
2. Creates `modules/650-winapi/tools/scripts/.venv/` (gitignored).
3. Upgrades `pip` and installs everything in `requirements.txt`.

Re-running the script is safe — it reuses the existing venv and only updates
packages.

---

## Step 2 — Register the Server in Your IDE

> **Critical naming difference:** VS Code's `.vscode/mcp.json` uses the key
> `"servers"`. Cursor's `.cursor/mcp.json` uses `"mcpServers"`. Same payload,
> different parent key.

### VS Code (GitHub Copilot Agent Mode)

Add this entry inside `.vscode/mcp.json` at the **workspace root**:

```jsonc
{
  "servers": {
    "winapi-mcp": {
      "type": "stdio",
      "command": "powershell",
      "args": [
        "-ExecutionPolicy", "Bypass",
        "-File", "./modules/650-winapi/tools/scripts/run.ps1"
      ]
    }
  }
}
```

A ready-to-copy file is at [tools/.vscode/mcp.json](.vscode/mcp.json).

After saving, VS Code shows an inline **Start | Stop | Restart | N tools**
action bar above the JSON block. Click **Start**. Open the Output panel
(View → Output → "Model Context Protocol") — you should see
`Discovered 11 tools`.

### Cursor

Add this entry inside `.cursor/mcp.json` at the workspace root:

```jsonc
{
  "mcpServers": {
    "winapi-mcp": {
      "command": "powershell",
      "args": [
        "-ExecutionPolicy", "Bypass",
        "-File", "./modules/650-winapi/tools/scripts/run.ps1"
      ]
    }
  }
}
```

A ready-to-copy file is at [tools/.cursor/mcp.json](.cursor/mcp.json).

Then: Command Palette → **Reload Window**. Settings → **MCP** — verify
`winapi-mcp` is listed and its tools are toggled on.

---

## Step 3 — Verify the Tools Are Loaded

In the IDE chat, switch to **Agent Mode** and ask:

> List the tools provided by the `winapi-mcp` MCP server.

You should see all 11 tools above. If you only see some, click the wrench icon
in the chat input and enable the missing ones for `winapi-mcp`.

---

## Usage Examples

### Take a screenshot of a specific window

> Use the `screenshot_window` tool with `window_name: "Visual Studio Code"`,
> then describe what is visible in the editor area.

The agent will receive both a text caption (with the saved file path) and the
PNG as MCP image content — no manual attachment.

### Capture a custom screen region

> Take a screenshot of the area from (100, 100) to (900, 600) using the
> `screenshot_area` tool and tell me what application is in the top-left
> corner.

### Click a button by its known coordinates

> Move the mouse to (450, 380) and left-click once.

### Drag-and-drop

> Drag from (300, 400) to (700, 400) over 0.8 seconds with the left mouse
> button.

### Send a hotkey to a specific app

1. `list_processes` → find the PID of `notepad.exe`.
2. `send_hotkey` with `pid: <pid>`, `hotkey: "^a"` (Select All).
3. `send_hotkey` with `pid: <pid>`, `text: "Hello from MCP"`.

### Run a multi-step input sequence

> Use `send_hotkey` with this sequence:
> ```json
> [
>   {"type": "hotkey", "value": "^+p"},
>   {"type": "delay",  "value": 200},
>   {"type": "text",   "value": "Reload Window"},
>   {"type": "key",    "value": "ENTER"}
> ]
> ```

---

## Hotkey Modifier Cheat Sheet

| Symbol | Modifier |
|---|---|
| `^` | Ctrl |
| `+` | Shift |
| `%` | Alt |
| `~` | Win |

Examples: `^t` = Ctrl+T, `^+i` = Ctrl+Shift+I, `%{F4}` = Alt+F4,
`~e` = Win+E.

---

## Security Considerations

This server **drives your physical machine**: it can move the mouse, type into
any focused window, and read whatever is on screen. Treat it like installing a
remote-control tool. Only enable it for chats where you actively want UI
automation, and disable / unregister when you are done.

The agent has no notion of "this window is sensitive" — if your password
manager is the focused window when `send_hotkey` fires with `text: "..."`,
that text goes there.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `install.ps1` says "Python ... not found" | Install Python 3.10+ from python.org and re-open PowerShell |
| `pywin32` install fails | Re-run as a normal user (not admin); ensure 64-bit Python |
| Server starts but `0 tools` discovered | Check Output → "Model Context Protocol" log; usually a Python import error inside `server.py` |
| `screenshot_window` returns "No window matching" | The match is case-insensitive substring; try `list_processes only_with_windows: true` then `window_tree pid: <pid>` to find the exact title |
| `send_hotkey` does nothing | The target window may not have focus; pass `pid` so the server focuses it first |
| `mouse_drag` releases too early | Increase `duration` (some apps require slow motion to register a drag) |
| Output panel shows JSON parse errors | The `run.ps1` script forces `PYTHONIOENCODING=utf-8`; if you launch `server.py` manually, set that env var too |

---

## How to Extend

Add a new tool by:

1. Writing an `async def _tool_xxx(arguments: dict) -> list[types.Content]:` in
   `server.py`.
2. Adding an entry to the `TOOLS` dict at the bottom: `description` (LLM-facing,
   make it action-oriented) + JSON Schema for `inputSchema`.
3. Restarting the MCP server from the IDE (Command Palette → `MCP: Restart Server`).

The discovery layer (`list_tools` / `call_tool`) is wired generically against
`TOOLS`, so you do not need to touch it.
