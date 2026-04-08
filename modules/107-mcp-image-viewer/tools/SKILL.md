# MCP Image Viewer — SKILL.md

> **This file is both a human guide and an AI skill.** When an AI agent reads this file, it gains full context on how to install, configure, and use the MCP Image Viewer tool across all operating systems and IDEs. Share it with your AI agent and ask it to guide you through setup.

---

## What This Tool Does

`mcp-image-viewer` is a minimal MCP server that exposes a single `load_image` tool. The AI calls it with a local file path and receives the image content directly — no manual attachment needed. Works identically to how `chrome-devtools-mcp` returns browser screenshots.

**Supported formats:** PNG, JPEG, GIF, WebP, BMP, SVG

**MCP content type used:**
```json
{ "type": "image", "mimeType": "image/png", "data": "<base64>" }
```

---

## Files in This Directory

| File | Purpose |
|------|---------|
| `mcp-image-viewer.ps1` | MCP server — Windows / PowerShell (all platforms) |
| `mcp-image-viewer.sh` | MCP server — Linux / macOS native Bash |
| `.vscode/mcp.json` | VS Code configuration template |
| `.cursor/mcp.json` | Cursor configuration template |

---

## Installation by OS and IDE

### Windows — VS Code

Add to `.vscode/mcp.json` in your workspace root (inside `"servers"`):

```json
"image-viewer-windows": {
  "command": "powershell",
  "args": ["-ExecutionPolicy", "Bypass", "-File", "./modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1"]
}
```

Save the file. VS Code auto-detects it and shows an inline **Start** button. Click it — status should become **Running | 1 tool**.

### Linux / macOS — VS Code

1. Make the script executable (one-time):
   ```bash
   chmod +x ./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh
   ```

2. Add to `.vscode/mcp.json` (inside `"servers"`):
   ```json
   "image-viewer-unix": {
     "command": "bash",
     "args": ["./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh"]
   }
   ```

3. Save — server starts automatically.

### Windows — Cursor

Add to `.cursor/mcp.json` in your workspace root (inside `"mcpServers"`):

```json
"image-viewer-windows": {
  "command": "powershell",
  "args": ["-ExecutionPolicy", "Bypass", "-File", "./modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1"]
}
```

Reload window: Command Palette → **Reload Window**.

### Linux / macOS — Cursor

1. Make the script executable:
   ```bash
   chmod +x ./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh
   ```

2. Add to `.cursor/mcp.json` (inside `"mcpServers"`):
   ```json
   "image-viewer-unix": {
     "command": "bash",
     "args": ["./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh"]
   }
   ```

3. Reload window.

---

## Key Difference: VS Code vs Cursor Config Format

| Setting | VS Code (`.vscode/mcp.json`) | Cursor (`.cursor/mcp.json`) |
|---------|-----------------------------|-----------------------------|
| Root key | `"servers"` | `"mcpServers"` |
| Auto-reload | Yes — saves trigger reload | No — requires Reload Window |
| Template | `tools/.vscode/mcp.json` | `tools/.cursor/mcp.json` |

---

## Enabling the Tool in Agent Mode

If `load_image` is not auto-enabled after the server starts:

**VS Code:**
1. Open Copilot Chat → switch to **Agent Mode**
2. Click the 🔧 wrench icon at the bottom of the chat input
3. Find `image-viewer-windows` (or `image-viewer-unix`) → enable `load_image`

**Cursor:**
1. Settings → search **MCP** → find the server → enable tools

---

## Usage

In Agent Mode, prompt:

```
Use the load_image tool to load:
C:/path/to/image.png

Describe what you see.
```

The AI calls the tool, receives the base64 image, and analyzes it — no manual attachment.

**Path format:**
- Windows: `C:/Users/name/Pictures/image.png` (forward slashes work)
- Linux/macOS: `/home/name/pictures/image.png`

---

## Verification

After installing, check:
- VS Code Output panel → **Model Context Protocol** → `Discovered 1 tool`
- Or ask the AI in Agent Mode: `list available MCP tools` — `load_image` should appear

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Server not starting | Check JSON syntax in `mcp.json` — missing commas are common |
| `load_image` — file not found | Use absolute path; verify with `Test-Path "C:/path"` (PS) or `ls /path` (bash) |
| AI doesn't call the tool | Ensure Agent Mode is active; explicitly say "use the load_image tool" |
| PowerShell execution policy error | Add `-ExecutionPolicy Bypass` to args (already included in template) |
| `base64: invalid option -w` on macOS | macOS `base64` doesn't support `-w 0`; the script auto-handles this with `|| base64 "$file"` fallback |
