# WinAPI MCP — Hands-On Reproduction Guide (Snow on google.com)

> A **human-readable manual** for reproducing the live experiment where an AI
> agent opens Chrome, opens DevTools Console, and starts a snowfall animation
> on `google.com` — all by itself, through MCP. If [SKILL.md](SKILL.md) is the
> agent-facing reference, this file is for you. Walk through it step by step;
> the screenshots act as visual checkpoints.

---

## What You Will Get at the End

![Final frame: snow falling on google.com, with the agent reasoning in the side panel](img/00-final-result.png)

White snowflakes of varying size and speed are falling over `google.com`. The
logo, search box, and buttons keep working (the canvas uses
`pointer-events:none`). The right-hand panel shows the agent's chat — it
located the Chrome process by itself, sent hotkeys, copied JS into the
clipboard, defeated paste-protection, and saved the final screenshot.

To reproduce this, you need to:

1. Install and register the `winapi-mcp` server (one-time setup).
2. Enable its tools in your chat session.
3. Give the agent the task in plain language — it will click everything itself.

---

## Step 1 — Install the Server

From the workspace root, in **PowerShell**:

```powershell
pwsh -ExecutionPolicy Bypass -File ./modules/650-winapi/tools/scripts/install.ps1
```

The script is idempotent: it creates `.venv/` next to `server.py`, upgrades
`pip`, and installs everything in `requirements.txt`. If your Python build is
missing the `venv` module, it transparently falls back to `virtualenv`.

> Requires **Python 3.10+** and **Windows**. The server will not load on
> macOS or Linux (it depends on `pywin32` / `pywinauto`).

---

## Step 2 — Register the Server in VS Code

Open `.vscode/mcp.json` at your workspace root and add the `winapi-mcp` block.
If the file does not exist, create it; note that VS Code uses the key
`"servers"` (Cursor would use `"mcpServers"`). Ready-to-copy templates live in
[`config/.vscode/mcp.json`](config/.vscode/mcp.json) (and
[`config/.cursor/mcp.json`](config/.cursor/mcp.json) for Cursor).

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

Save the file. VS Code shows an inline action bar above the JSON block:
**Start | Stop | Restart | N tools**. Click **Start**.

In **Output → Model Context Protocol** you should see `Discovered 11 tools` —
that means the server started and the MCP handshake succeeded.

![mcp.json with winapi-mcp and the "Discovered 11 tools" log](img/06-mcp-server-registered.png)

The screenshot highlights: the `winapi-mcp` entry under `servers`, the inline
`Running | 11 tools` indicator, and the `Discovered 11 tools` line in the log.

---

## Step 3 — Enable the Tools in the Chat

Open Copilot Chat → switch to **Agent Mode** → click the wrench icon
(Configure Tools). Find the `winapi-mcp` branch in the tree and make sure all
11 checkboxes are ticked:

![Configure Tools — all 11 winapi-mcp tools enabled](img/07-tools-enabled.png)

Tool list (see [SKILL.md](SKILL.md) for full details):

- `screenshot_window`, `screenshot_area` — screenshots
- `mouse_move`, `mouse_click`, `mouse_drag` — mouse
- `send_hotkey` — keyboard (hotkeys / named keys / text / sequences)
- `clipboard_get`, `clipboard_set` — clipboard
- `list_processes`, `window_tree`, `get_window_content` — window inspection

> **If you just registered the server but the tool list is empty** — VS Code
> discovers MCP servers at chat-session startup. Open a fresh chat (`+` next
> to the model) or explicitly approve the new server via `Configure Tools`.

---

## Step 4 — Run the Demo

Open a new Agent Mode chat and ask the agent something like:

> Open Chrome on `google.com`, open the DevTools Console, and paste a
> JavaScript snippet that draws falling snow over the page. Take a screenshot
> after every step and explain what you see.

The agent will go through roughly the following route (each step → one MCP
call):

### 4.1. Find and focus Chrome

```
list_processes filter=chrome only_with_windows=true
→ pid=78812
send_hotkey pid=78812 key=ESC      # side effect of _focus_pid → set_focus()+restore()
screenshot_window window_name="Google Chrome"
```

![01 — Chrome with google.com in the foreground](img/01-chrome-google-loaded.png)

### 4.2. Open DevTools, switch to Console

```
send_hotkey hotkey="^+i"           # Ctrl+Shift+I — DevTools (Elements tab by default)
screenshot_window window_name="Google Chrome"
```

![02 — DevTools open, Elements tab active](img/02-devtools-elements.png)

```
send_hotkey hotkey="^+j"           # Ctrl+Shift+J — switch to Console
screenshot_window window_name="Google Chrome"
```

![03 — Console tab active, input prompt ready](img/03-console-tab-ready.png)

> ⚠️ If DevTools was already open on Console, `^+j` will close it. Send it
> again in that case.

### 4.3. Put JS in the clipboard and paste it

JS payload (569 chars, IIFE — creates a canvas and animates 200 snowflakes):

```js
(()=>{const c=document.createElement('canvas');Object.assign(c.style,{position:'fixed',inset:'0',pointerEvents:'none',zIndex:'2147483647'});c.width=innerWidth;c.height=innerHeight;document.body.appendChild(c);const x=c.getContext('2d');const f=Array.from({length:200},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:1+Math.random()*3,s:0.5+Math.random()*1.5}));(function t(){x.clearRect(0,0,c.width,c.height);x.fillStyle='white';for(const k of f){x.beginPath();x.arc(k.x,k.y,k.r,0,7);x.fill();k.y+=k.s;if(k.y>c.height)k.y=0;}requestAnimationFrame(t);})();})();
```

```
clipboard_set text="<JS above>"
send_hotkey pid=78812 sequence=[
  {type: hotkey, value: "^v"},
  {type: delay,  value: 400},
  {type: key,    value: "ENTER"}
]
```

### 4.4. Defeat paste-protection (one time per origin)

By default Chrome blocks the first paste into the DevTools Console (self-XSS
protection). The first attempt shows a yellow warning bar:

![04 — "Don't paste code into the DevTools Console" warning](img/04-paste-protection-warning.png)

Unlock it by typing the magic phrase, then re-paste:

```
send_hotkey pid=78812 sequence=[
  {type: text,  value: "allow pasting"},
  {type: delay, value: 200},
  {type: key,   value: "ENTER"},
  {type: delay, value: 300},
  {type: hotkey, value: "^v"},
  {type: delay,  value: 400},
  {type: key,    value: "ENTER"}
]
```

### 4.5. Final screenshot — snow is falling

```
send_hotkey pid=78812 key=ESC      # focus Chrome on top of everything else
screenshot_window window_name="Google - Google Chrome"
```

![05 — snow falling on google.com](img/05-snow-running.png)

You should see the pasted code in the console, `undefined` underneath
(an IIFE returns nothing — that is expected), and snowflakes drifting down
across the Google UI.

---

## Lessons Learned

- **`screenshot_window` captures the window's screen bbox, not its bitmap.**
  If the target window is occluded, the screenshot shows whatever is on top.
  Focus the window before each important screenshot via
  `send_hotkey pid=...` (any safe key like ESC works) — `_focus_pid` has the
  side effect of `set_focus()` + `restore()`.
- **Hotkey-via-`pid` is more reliable than a global hotkey.** With `pid` the
  server focuses the window first and only then sends keys — no more
  "the keystroke went to the wrong window".
- **`Ctrl+Shift+J` toggles Console.** If DevTools is already open on Console,
  the second press closes it. Sometimes you need to send it twice, sometimes
  not at all — verify with a screenshot.
- **Chrome paste-protection is per-origin.** Once you typed `allow pasting`
  on `google.com`, all later `^v` operations in that session work silently.
- **`sequence` with `delay` solves race conditions.** Without `delay`, ENTER
  can arrive before a long `^v` paste has actually landed in the input.

---

## Security

This server **physically drives your machine**: it moves the mouse, types
into whatever window is focused, and reads the screen. Only enable it for
chats where you actively want UI automation, and disable / unregister it from
`mcp.json` when you are done. The agent has no concept of "this is a
sensitive window" — if your password manager is focused when `send_hotkey`
fires with `text: "..."`, that text goes there.

---

## Where to Go Next

- [SKILL.md](SKILL.md) — full reference for every tool and its parameters
  (agent-facing and deep-read for humans).
- [Module walkthrough.md](../walkthrough.md) — step-by-step coverage of
  everything, from install to writing your own MCP commands.
- [scripts/server.py](scripts/server.py) — see how to plug in your own MCP
  tool next to the existing 11.
