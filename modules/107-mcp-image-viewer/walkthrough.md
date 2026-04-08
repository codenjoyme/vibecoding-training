# MCP Image Viewer Tool in PowerShell - Hands-on Walkthrough

In this walkthrough you'll build a minimal PowerShell MCP server with a single `load_image` tool. Once registered, the AI can call this tool to load any image from your filesystem and analyze it — the same mechanism used by `chrome-devtools-mcp` when it takes browser screenshots and returns them to the AI.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Description |
|-----------|-------------|
| `tools/mcp-image-viewer.ps1` | PowerShell MCP server — Windows / PowerShell on macOS |
| `tools/mcp-image-viewer.sh` | Bash MCP server — Linux / macOS native terminal |
| `tools/.vscode/mcp.json` | VS Code configuration template |
| `tools/.cursor/mcp.json` | Cursor configuration template |

The tool accepts a file path, reads the image bytes, converts to base64, and wraps them in the MCP `image` content type — exactly the same format used by `chrome-devtools-mcp`'s `take_screenshot`.

---

## Part 1: Understanding MCP Image Content Type

Before coding, let's understand what the MCP protocol expects when returning an image.

A standard MCP `tools/call` response looks like this:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Loaded image: photo.png"
      },
      {
        "type": "image",
        "mimeType": "image/png",
        "data": "<base64-encoded-bytes>"
      }
    ]
  }
}
```

Key points:

1. `content` is an **array** — you can include both text and images in one response
2. Image items have three required fields: `type`, `mimeType`, and `data`
3. `data` is the raw file bytes encoded as **base64** (no `data:` URI prefix)
4. `mimeType` tells the AI model how to interpret the bytes

This is exactly what `chrome-devtools-mcp` does in `screenshot.js`:
```javascript
response.attachImage({
    mimeType: `image/${format}`,
    data: Buffer.from(screenshot).toString('base64'),
});
```

In PowerShell we do the same using `[Convert]::ToBase64String([System.IO.File]::ReadAllBytes($filePath))`.

---

## Part 2: Examine the Ready-Made Tool

This module ships with completed server scripts in `tools/`. Both implement the same `load_image` tool:

1. Open `modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1` (Windows/PowerShell)

1. Notice the `load_image` tool declaration in `tools/list` — it expects a `filePath` string

1. In `tools/call`, find the `load_image` handler:
   - Resolves the path to absolute using `[System.IO.Path]::GetFullPath()`
   - Determines MIME type from file extension (`Get-MimeType` helper)
   - Reads all bytes: `[System.IO.File]::ReadAllBytes($filePath)`
   - Converts to base64: `[Convert]::ToBase64String($bytes)`
   - Returns a `content` array with one text item and one image item

1. The image content item uses `type = "image"`, `mimeType`, and `data` — matching the MCP spec

1. For Linux/macOS, the equivalent is `tools/mcp-image-viewer.sh` which uses `base64 -w 0` for the same result

---

## Part 3: Register the MCP Server

### 3.1 Configuration for VS Code

**Important:** VS Code uses a different configuration format than Cursor!

1. **Locate your configuration file**

   Open or create: `.vscode/mcp.json` in your workspace root

   Path example: `c:/workspace/your-project/.vscode/mcp.json` (Windows) or `~/workspace/your-project/.vscode/mcp.json` (macOS/Linux)

2. **Copy the VS Code configuration template**

   A template file is provided at: `./modules/107-mcp-image-viewer/tools/.vscode/mcp.json`

   Copy it to your workspace's `.vscode/` folder, or add this entry inside the existing `"servers"` object:

   ```json
   "image-viewer-windows": {
     "command": "powershell",
     "args": ["-ExecutionPolicy", "Bypass", "-File", "./modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1"]
   },
   "image-viewer-unix": {
     "command": "bash",
     "args": ["./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh"]
   }
   ```

   **Key field:** `servers` (not `mcpServers`)

3. **Choose the right server for your OS**

   - **Windows users:** Keep only `image-viewer-windows`, remove `image-viewer-unix` section
   - **Linux/macOS users:** Keep only `image-viewer-unix`, remove `image-viewer-windows` section

   **Windows final config:**
   ```json
   {
     "servers": {
       "image-viewer-windows": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1"]
       }
     }
   }
   ```

   **Linux/macOS final config:**
   ```json
   {
     "servers": {
       "image-viewer-unix": {
         "command": "bash",
         "args": ["./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh"]
       }
     }
   }
   ```

4. **Make the bash script executable (Linux/macOS only)**

   Open terminal and run:
   ```bash
   chmod +x ./modules/107-mcp-image-viewer/tools/mcp-image-viewer.sh
   ```

5. **Start the MCP server**

   After saving `mcp.json`, VS Code automatically detects the file and shows an inline action bar directly inside the editor:

   ```
   ✓ Running | Stop | Restart | 1 tool | More...
   ```

   If the server is not running yet, click **"Start"** or **"Restart"** in the inline bar.

   **Verify in Output panel** (View → Output → "Model Context Protocol"):
   ```
   [info] Connection state: Running
   [info] Discovered 1 tool
   ```

### 3.2 Configuration for Cursor

**Important:** Cursor uses a different configuration format and location!

1. **Locate your configuration file**

   Open or create: `.cursor/mcp.json` in your workspace root

2. **Copy the Cursor configuration template**

   A template file is provided at: `./modules/107-mcp-image-viewer/tools/.cursor/mcp.json`

   Copy it to your workspace's `.cursor/` folder, or add this entry inside `"mcpServers"`:

   ```json
   {
     "mcpServers": {
       "image-viewer-windows": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1"]
       }
     }
   }
   ```

   **Key field:** `mcpServers` (not `servers` like VS Code)

3. **Reload Cursor window**

   Open Command Palette → "Reload Window" → press Enter

### 3.3 Enable the Tool (if not auto-enabled)

In most cases, MCP tools are enabled automatically. If the AI doesn't recognize `load_image`:

**VS Code:**
1. Open the GitHub Copilot Chat panel
2. Switch to **Agent Mode** (not Ask or Edit)
3. Click the **🔧 tools icon** (wrench) at the bottom of the chat input
4. Find the `image-viewer-windows` (or `image-viewer-unix`) section
5. Enable the `load_image` toggle

**Cursor:**
1. Open Settings → search for "MCP"
2. Find your server and enable its tools

---

## Part 4: Test the Tool — Load and Describe an Image

1. Find any `.png` or `.jpg` file on your computer. For example, a screenshot you took earlier in module 035.

1. Note its full absolute path:
   - Windows: `C:/Users/YourName/Pictures/screenshot.png`
   - Linux/macOS: `/home/yourname/Pictures/screenshot.png`

1. Open GitHub Copilot Chat in **Agent Mode**

1. Send this prompt (replace the path):
   ```
   Use the load_image tool to load this file:
   C:/path/to/your/screenshot.png

   Describe what you see.
   ```

1. The AI will call `load_image`, receive the base64 image, and describe the content — without you manually attaching anything.

1. Verify: you should see a tool call bubble in the chat showing `load_image` was invoked with your file path.

---

## Part 5: Explore the Difference — Manual Attach vs MCP Tool

| Method | When it works | Limitation |
|--------|---------------|------------|
| Clipboard paste (`Ctrl+V`) | After taking a fresh screenshot | Requires manual action per image |
| File attach (paperclip icon) | For files already on disk | Still manual — you pick the file |
| MCP `load_image` tool | When AI knows the path (from context) | AI must know the path; no GUI picker |

**Key insight:** The MCP approach enables **programmatic access** — AI can load images as part of an automated chain (e.g., take screenshot → save to file → load via MCP → analyze → summarize) without pausing to ask you for input.

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ You understand the MCP `image` content type format (`type`, `mimeType`, `data`)  
✅ You can explain how `chrome-devtools-mcp` returns screenshots (base64 in `content` array)  
✅ You registered `mcp-image-viewer.ps1` (Windows) or `mcp-image-viewer.sh` (Linux/macOS) in your IDE's `mcp.json`  
✅ You successfully asked the AI to load an image by file path using the `load_image` tool  
✅ You understand the difference between manual attachment and MCP-based image loading

## Understanding Check

**Question 1:** What three fields does an MCP image content item require?  
**Expected answer:** `type: "image"`, `mimeType` (e.g. `image/png`), and `data` (base64-encoded bytes).

**Question 2:** Why is `data` base64-encoded rather than raw bytes?  
**Expected answer:** MCP messages are JSON (text). JSON cannot contain raw binary bytes, so binary data is represented as a base64 string.

**Question 3:** What is the format of a `tools/call` response in MCP when returning an image?  
**Expected answer:** JSON-RPC 2.0 response with `result.content` array containing at least one item with `type: "image"`, `mimeType`, and `data`.

**Question 4:** What is the advantage of the MCP `load_image` tool over the manual paperclip attachment?  
**Expected answer:** AI can invoke it programmatically without user interaction — useful in automated workflows where images are generated or saved as part of a pipeline.

**Question 5:** Which npm package served as the reference for understanding how to return images via MCP?  
**Expected answer:** `chrome-devtools-mcp` — specifically its `screenshot.js` tool which calls `response.attachImage({ mimeType, data })`.

## Troubleshooting

**MCP server not appearing in list**
- Check `.vscode/mcp.json` syntax — missing commas are a common cause
- Try `pwsh` instead of `powershell` if PowerShell 7+ is your default shell
- Check the MCP server logs via Command Palette → **MCP: Show Logs**

**`load_image` returns an error about the path**
- Ensure the path uses the correct separator for your OS (`/` works on all platforms in PowerShell)
- Check the file actually exists: `Test-Path "C:/path/to/file.png"` in terminal
- Use absolute paths — relative paths may resolve differently inside the MCP process

**AI does not call the tool**
- Check that Agent Mode is active (not Edit or Ask mode)
- Explicitly say "use the load_image tool" in your prompt
- Reload MCP servers via Command Palette → **MCP: Restart Server**

## Next Steps

- [108 — Token and API Key Management](../108-token-api-key-management/about.md) — next module in sequence
- Extend `mcp-image-viewer.ps1` to accept a directory and load all images in it
- Combine with module 130 techniques to build a screenshot-based QA pipeline
