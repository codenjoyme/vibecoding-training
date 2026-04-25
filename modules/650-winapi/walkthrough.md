# WinAPI MCP Toolbox - Hands-on Walkthrough

In this walkthrough you will install a self-contained Python MCP server,
register it in VS Code or Cursor, and have the AI agent take screenshots of
specific windows, click and drag the mouse, and send keystrokes to a target
application — all from a chat prompt.

By the end the agent literally has hands and eyes on your Windows desktop.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Description |
|-----------|-------------|
| `tools/scripts/server.py` | Single-file Python MCP server with 11 WinAPI tools |
| `tools/scripts/install.ps1` | Bootstrap — creates `.venv/`, installs `mcp`, `mss`, `pywin32`, `pyautogui`, `pywinauto`, `pyperclip`, `psutil`, `Pillow` |
| `tools/scripts/run.ps1` | Launcher invoked by the IDE; activates `.venv` and runs the server |
| `tools/config/.vscode/mcp.json` | VS Code config template (root key `servers`) |
| `tools/config/.cursor/mcp.json` | Cursor config template (root key `mcpServers`) |
| `tools/scripts/output/` | Folder where screenshots are saved (gitignored) |

All Python artefacts (`.venv/`, `__pycache__/`) and the `output/` folder live
inside `tools/` and are listed in `tools/.gitignore` — nothing leaks into the
course repository.

---

## Part 1: Inspect the Skill Files

### What We'll Do

Read the existing files so you understand what each piece does before running
anything. The whole skill is intentionally tiny — one Python file, two
PowerShell scripts, two JSON templates.

1. Open [tools/SKILL.md](tools/SKILL.md) — the AI-facing reference.
1. Open [tools/scripts/server.py](tools/scripts/server.py) and skim the
   `TOOLS` dictionary near the bottom: each entry is a `description` plus a
   JSON Schema. This is exactly what the LLM sees when it decides which tool
   to call.
1. Open [tools/scripts/requirements.txt](tools/scripts/requirements.txt) — the
   list of pip packages the bootstrap will install.

### Why This Architecture?

This is the same shape as `mcpyrex` — `lng_winapi/*` lives at
`work/400-task/mcp_server/tools/lng_winapi/` if you want to compare — but
collapsed into a single `server.py`. There is no plugin discovery, no project
scaffolding, no Langchain. It is the **smallest** thing that can be called an
MCP server while still doing real work.

---

## Part 2: Install the Python Environment

### What We'll Do

Bootstrap a virtualenv next to the script and install all dependencies. The
script is idempotent — re-run it whenever you change `requirements.txt`.

From the workspace root, in **PowerShell**:

```powershell
pwsh -ExecutionPolicy Bypass -File ./modules/650-winapi/tools/scripts/install.ps1
```

You should see:

```
[winapi-mcp] script dir : C:\...\modules\650-winapi\tools\scripts
[winapi-mcp] creating virtualenv with: python -m venv .venv
[winapi-mcp] upgrading pip
[winapi-mcp] installing requirements from ...\requirements.txt
...
[winapi-mcp] done.
```

### What Just Happened

The script created `modules/650-winapi/tools/scripts/.venv/`. That folder is
listed in `.gitignore` — git will never see it. The virtualenv is fully
isolated; nothing was installed into your global Python.

> 💬 **Discussion for agent:** Why isolate dependencies into a `.venv` next to
> the server, instead of installing globally or sharing one venv across all
> MCP servers? Push the user to articulate the version-conflict and
> "I-broke-my-system-Python" failure modes.

---

## Part 3: Verify the Server Boots

### What We'll Do

Run the server once by hand to confirm there are no import errors. The server
talks JSON-RPC over stdio, so it will block waiting for input — that is the
healthy state.

```powershell
pwsh -ExecutionPolicy Bypass -File ./modules/650-winapi/tools/scripts/run.ps1
```

If you see no output and the terminal "hangs", **that is success** — the
server is waiting for a JSON-RPC request on stdin. Press `Ctrl+C` to stop it.

If you see a Python traceback (`ModuleNotFoundError`, `ImportError`), re-run
`install.ps1` — usually a missing or partially installed dependency.

### Optional: Send a Manual `tools/list` Request

Paste the following one-liner and press Enter inside the running server, then
Ctrl+C:

```
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"manual","version":"1"}}}
```

You will see an `initialize` response. The IDE does this handshake
automatically — you just confirmed the server speaks the protocol.

---

## Part 4: Register the Server in VS Code

> **Important:** VS Code uses `"servers"` as the root key. Cursor uses
> `"mcpServers"`. The values are identical.

### 4.1 Add the Configuration

1. Open or create `.vscode/mcp.json` in your **workspace root**
   (e.g. `c:/Java/CopipotTraining/vibecoding-for-managers/.vscode/mcp.json`).
2. Inside the existing `"servers": { ... }` object (or create one), add:

   ```jsonc
   "winapi-mcp": {
     "type": "stdio",
     "command": "powershell",
     "args": [
       "-ExecutionPolicy", "Bypass",
       "-File", "./modules/650-winapi/tools/scripts/run.ps1"
     ]
   }
   ```

   A complete file is at [tools/config/.vscode/mcp.json](tools/config/.vscode/mcp.json) —
   copy it directly if you do not yet have a `.vscode/mcp.json`.

### 4.2 Start the Server from the Editor

VS Code shows an inline action bar above the JSON block:

```
✓ Running | Stop | Restart | 11 tools | More...
```

If it says **Stopped**, click **Start**. If you see **0 tools**, click
**Restart** — usually means `server.py` failed to import (open
View → Output → "Model Context Protocol" for the traceback).

### 4.3 Enable the Tools in Agent Mode

1. Open the GitHub Copilot chat panel.
1. Switch the dropdown to **Agent Mode**.
1. Click the **🔧 wrench icon** at the bottom of the chat input.
1. Find the `winapi-mcp` group and enable any tools that are off.

---

## Part 5: Register the Server in Cursor

1. Create or open `.cursor/mcp.json` in your workspace root.
1. Inside `"mcpServers": { ... }`, add the same `winapi-mcp` entry as above.
   A complete file is at [tools/config/.cursor/mcp.json](tools/config/.cursor/mcp.json).
1. Command Palette → **Reload Window**.
1. Settings → search **MCP** → confirm `winapi-mcp` is listed and its tools
   are toggled on.

---

## Part 6: Drive Your Desktop from Chat

### 6.1 Take a Screenshot of a Specific Window

In Agent Mode chat:

> Use the `screenshot_window` tool with `window_name: "Visual Studio Code"`,
> then describe what is currently on screen.

The agent calls the tool, receives a text caption + the PNG as MCP image
content, and describes what it sees. The PNG is also saved to
`modules/650-winapi/tools/scripts/output/window-Visual_Studio_Code-<timestamp>.png`.

### 6.2 Capture an Arbitrary Region

> Take a screenshot of the area from (0, 0) to (1280, 720) using
> `screenshot_area` and tell me what application owns the top-left corner.

### 6.3 Click and Drag

Pick two safe screen coordinates (somewhere with empty space — your desktop
will do):

> Move the cursor to (500, 500), then drag from (500, 500) to (700, 700)
> over 0.6 seconds with the left button.

### 6.4 Send Hotkeys to an Application

1. Open Notepad.
1. In chat: *"List processes whose name contains `notepad`."* — note the PID.
1. *"Use `send_hotkey` with that PID and text: `Hello from MCP`."*
1. *"Use `send_hotkey` with that PID, sequence:*
   ```json
   [
     {"type": "hotkey", "value": "^a"},
     {"type": "delay",  "value": 100},
     {"type": "key",    "value": "DELETE"},
     {"type": "text",   "value": "Round two."}
   ]
   ```
   *"*

### 6.5 Read and Write the Clipboard

> Read the current clipboard.
>
> Set the clipboard to `winapi-mcp works`. Then read it back to confirm.

---

## Success Criteria

- ✅ `install.ps1` finished without errors and `tools/scripts/.venv/` exists
- ✅ `run.ps1` starts and blocks on stdin (server is alive)
- ✅ VS Code Output → "Model Context Protocol" reports `Discovered 11 tools` for `winapi-mcp`
- ✅ `screenshot_window` returns an MCP image attachment that the agent can describe
- ✅ `screenshot_area` saves a PNG into `tools/scripts/output/`
- ✅ `mouse_move`, `mouse_click`, `mouse_drag` move the cursor on your screen
- ✅ `send_hotkey` delivers text and hotkeys to a focused window
- ✅ `clipboard_get` / `clipboard_set` round-trip a string
- ✅ `list_processes`, `window_tree`, `get_window_content` return usable JSON

---

## Understanding Check

1. **Why does VS Code use `servers` while Cursor uses `mcpServers`?**
   > Each IDE was built independently against draft versions of the MCP spec.
   > The payload shape is the same — only the parent key differs. Always
   > consult both templates ([tools/config/.vscode/mcp.json](tools/config/.vscode/mcp.json),
   > [tools/config/.cursor/mcp.json](tools/config/.cursor/mcp.json)) when porting a server
   > between IDEs.

2. **Why is the screenshot returned as base64 instead of just a file path?**
   > MCP `image` content lets the LLM read the bytes directly without an
   > extra round-trip through a file-loading tool. This is the same mechanism
   > used by `chrome-devtools-mcp` (and module 107's `load_image` tool).

3. **What happens if you call `send_hotkey` without a `pid`?**
   > The server uses Win32 `SendInput`-style global key events, which go to
   > whichever window currently has focus. Pass `pid` to have the server
   > focus the target process first — much more reliable.

4. **Why is `pyautogui.FAILSAFE` disabled in the server?**
   > FAILSAFE aborts pyautogui when the cursor reaches a screen corner. That
   > is helpful for humans testing scripts, but inside an MCP tool it would
   > randomly throw mid-run. We disable it because the agent is presumed to
   > be in control.

5. **How does the agent discover that a tool exists?**
   > On startup, the IDE sends `tools/list`; the server responds with the
   > entries in `TOOLS` — name, description, and JSON Schema. The
   > `description` is the prompt that tells the LLM when to call the tool.

6. **Where do screenshots end up on disk?**
   > `modules/650-winapi/tools/scripts/output/`. The folder is gitignored
   > except for `.gitkeep`, so it survives `git clean` but contents are not
   > committed.

7. **What is the security model?**
   > There isn't one. The server is a remote control for your desktop. Only
   > enable it in chats where you want UI automation; unregister it from
   > `mcp.json` when you are finished.

---

## Troubleshooting

### `pwsh: command not found`

Use `powershell` (Windows PowerShell 5.1) instead — both scripts are
PowerShell 5-compatible. If you also do not have `powershell`, install
PowerShell 7+ from
[github.com/PowerShell/PowerShell](https://github.com/PowerShell/PowerShell).

### `install.ps1` fails on `pywin32`

`pywin32` is Windows-only. Make sure you are on a 64-bit Python 3.10+ build
(`python -c "import struct; print(struct.calcsize('P')*8)"` → `64`). If pip
still fails, install pywin32 alone first:
`./.venv/Scripts/python.exe -m pip install pywin32`.

### Server shows up but `0 tools`

Open VS Code → View → Output → "Model Context Protocol". If you see a Python
traceback, the most common cause is a missing dependency. Re-run
`install.ps1`. If a specific import is broken, you can `pip install` it
manually inside `tools/scripts/.venv/`.

### `screenshot_window` returns `No window matching`

Window matching is a case-insensitive substring of the title or class. Use
`list_processes` with `only_with_windows: true` then `window_tree` on the PID
to discover the exact title.

### `send_hotkey` text appears in the wrong window

The server only forces focus when you pass `pid`. Pass it. Without `pid` the
keystrokes go to whichever window had focus when the tool fired, including
the chat window itself.

### The `.venv` keeps appearing in source control

It should not — `tools/.gitignore` has `.venv/`. If you committed it earlier,
run `git rm -r --cached modules/650-winapi/tools/scripts/.venv` and recommit.

---

## Next Steps

- Combine `screenshot_window` with `mouse_click` to write end-to-end UI tests
  that the agent can run on demand.
- Extend `server.py` with a `find_image_on_screen` tool (template-match a PNG
  on the screen and return the coordinates) so the agent can click visual
  targets without hard-coded coordinates.
- Re-use this skill scaffolding (single `server.py` + `install.ps1` +
  `run.ps1` + two `mcp.json` templates) as the template for any narrow,
  domain-specific MCP server you need.
