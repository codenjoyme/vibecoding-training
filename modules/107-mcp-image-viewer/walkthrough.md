# MCP Image Viewer Tool in PowerShell - Hands-on Walkthrough

In this walkthrough you'll build a minimal PowerShell MCP server with a single `load_image` tool. Once registered, the AI can call this tool to load any image from your filesystem and analyze it — the same mechanism used by `chrome-devtools-mcp` when it takes browser screenshots and returns them to the AI.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Description |
|-----------|-------------|
| `tools/mcp-image-viewer.ps1` | PowerShell MCP server with one tool: `load_image` |
| `.vscode/mcp.json` entry | Registration so VS Code / Copilot can invoke it |

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

## Part 2: Review the Reference MCP Server

The `mcp-echo.ps1` in module 100 is our starting template. It handles:

- JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call` messages
- Returning `content` arrays with `type: "text"` items
- Running as a stdio process (VS Code communicates via stdin/stdout)

Open the reference file to refresh your memory:

```
modules/100-mcp-model-context-protocol/tools/mcp-echo.ps1
```

Our `mcp-image-viewer.ps1` follows the same structure but adds one new tool and returns `type: "image"` content.

---

## Part 3: Examine the Ready-Made Tool

This module ships with a completed `mcp-image-viewer.ps1` in `tools/`. Let's read through it:

1. Open `modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1`

1. Notice the `load_image` tool declaration in `tools/list` — it expects a `filePath` string

1. In `tools/call`, find the `load_image` handler:
   - Resolves the path to absolute
   - Determines MIME type from file extension
   - Reads all bytes and converts to base64
   - Returns a `content` array with one text item and one image item

1. Verify: the image content item uses `type = "image"`, `mimeType`, and `data` — matching the MCP spec.

---

## Part 4: Register the MCP Server in mcp.json

1. Open `.vscode/mcp.json` in your workspace

1. Add the following entry inside the `"servers"` object:

   ```json
   "image-viewer": {
     "type": "stdio",
     "command": "powershell",
     "args": [
       "-ExecutionPolicy", "Bypass",
       "-File", "${workspaceFolder}/modules/107-mcp-image-viewer/tools/mcp-image-viewer.ps1"
     ]
   }
   ```

   > **Windows note:** Use `powershell` for Windows PowerShell 5.1 or `pwsh` for PowerShell 7+. Either works.

1. Save the file

1. Reload / restart the MCP server list: open Command Palette → **MCP: List Servers** → verify `image-viewer` appears

---

## Part 5: Test the Tool — Load and Describe an Image

1. Find any `.png` or `.jpg` file on your computer. For example, a screenshot you took earlier in module 035.

1. Note its full absolute path, e.g.:  
   `C:/Users/YourName/Pictures/screenshot.png` (Windows)  
   `/home/yourname/Pictures/screenshot.png` (Linux/macOS)

1. Open GitHub Copilot Chat in Agent Mode

1. Send this prompt (replace the path):
   ```
   Use the load_image tool to load this file:
   C:/path/to/your/screenshot.png
   
   Describe what you see.
   ```

1. The AI will call `load_image`, receive the base64 image, and describe the content — without you manually attaching anything.

1. Verify: you should see a tool call bubble in the chat showing `load_image` was invoked with your file path.

---

## Part 6: Explore the Difference — Manual Attach vs MCP Tool

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
✅ You registered `mcp-image-viewer.ps1` in `.vscode/mcp.json`  
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
