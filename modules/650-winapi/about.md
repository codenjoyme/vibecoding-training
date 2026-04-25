# WinAPI MCP Toolbox — Give the Agent Hands and Eyes on Windows

**Duration:** 15-20 minutes

**Skill:** Install a self-contained Python MCP server that exposes Windows automation tools (screenshots of arbitrary windows or screen regions, mouse clicks/drags, keyboard hotkeys/text input, clipboard, process and window inspection) so the AI agent can drive your desktop the same way you do — with a mouse, keyboard, and eyes.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why a `winapi`-only MCP server (not the full `mcpyrex` install) — minimal dependencies, single folder, gitignored Python
- Tools the server exposes: `screenshot_window`, `screenshot_area`, `mouse_click`, `mouse_move`, `mouse_drag`, `send_hotkey`, `clipboard_get`, `clipboard_set`, `list_processes`, `window_tree`, `get_window_content`
- Returning screenshots as MCP `image` content (the same pattern used in module 107)
- IDE configuration: `.vscode/mcp.json` (key: `servers`) vs `.cursor/mcp.json` (key: `mcpServers`)
- Bootstrap script that creates a virtualenv, installs dependencies, and verifies the install
- Running the server from VS Code (Agent Mode) and Cursor

## Learning Outcome

You will have a working MCP server living entirely in `modules/650-winapi/tools/scripts/` (with all Python artefacts gitignored), registered in your IDE, that lets the AI agent take screenshots of any application window or screen region, click and drag the mouse, type text, send hotkeys, and read/write the clipboard — enabling end-to-end UI automation driven from chat.

## Prerequisites

### Required Modules

- [100 — Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)
- [107 — MCP Image Viewer Tool in PowerShell](../107-mcp-image-viewer/about.md)
- [400 — Installing mcpyrex MCP Python Toolbox](../400-installing-mcpyrex-mcp-python-toolbox/about.md) *(optional, recommended — the `lng_winapi` tools live there as the reference implementation)*

### Required Skills & Tools

- Windows 10 or 11 (this module targets WinAPI; macOS/Linux are out of scope)
- Python 3.10+ available on PATH (`python --version`)
- VS Code with GitHub Copilot **Agent Mode** or Cursor
- A workspace with `.vscode/mcp.json` or `.cursor/mcp.json` already in use (or willingness to create one)

## When to Use

- You want the agent to operate a desktop application via UI (click buttons, paste text, take screenshots) rather than via API
- You need to feed live screenshots of a specific window into chat as MCP image attachments
- You want to script multi-step UI flows (focus app → hotkey → type → screenshot → verify) from a single chat prompt
- You want a minimal, hackable reference for building your own narrow-purpose Python MCP servers

## Resources

- Reference implementation: `lng_winapi` tools inside the [mcpyrex repository](https://github.com/codenjoyme/mcpyrex-python) (cloned into `work/400-task/mcp_server/tools/lng_winapi/`)
- MCP image content type: see [107 — MCP Image Viewer](../107-mcp-image-viewer/about.md)
- Python MCP SDK: [`pip install mcp`](https://pypi.org/project/mcp/)
