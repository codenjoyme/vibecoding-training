# CodeMie CLI Setup & IDE Integration — Hands-on Walkthrough

In this walkthrough you will install and configure CodeMie CLI, authenticate with your provider, install an AI coding agent, and connect it to your IDE. By the end:

- `codemie doctor` shows all required checks as ✓
- Claude Code (or another agent) is reachable from VS Code or Cursor
- You know how to use `tools/SKILL.md` as a context document for your AI agent during troubleshooting

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Set Up

| Component | Description |
|---|---|
| Node.js LTS | Runtime required by CodeMie CLI |
| `@codemieai/code` | CodeMie CLI — the enterprise AI proxy layer |
| AI agent | Claude Code, Gemini CLI, or OpenCode (your choice) |
| IDE plugin | Claude Code for VS Code or Cursor with proxy configuration |
| `tools/SKILL.md` | Reference FAQ — load this into your agent when you hit issues |

> **How to use `tools/SKILL.md`:** At any step where something doesn't work, open a chat with your AI agent, attach `tools/SKILL.md`, and ask: *"I followed step X but got error Y — what does the SKILL.md say to do?"* The document is written as an agent-readable reference so it gives precise, step-specific answers.

---

## Part 1: Install Node.js

### What we'll do

CodeMie CLI is an npm package. Node.js must be installed first.

### Step 1 — Download and install Node.js

**macOS**

1. Go to [https://nodejs.org](https://nodejs.org)
2. Click **LTS** download
3. Run the `.pkg` installer
4. Open a **new** Terminal window and verify:

```bash
node --version
npm --version
```

Both should print a version number (e.g. `v24.x.x` and `11.x.x`).

**Windows**

1. Go to [https://nodejs.org/en/download](https://nodejs.org/en/download)
2. If the page defaults to Docker instructions — scroll down and click **Windows Installer (.msi)**
3. Run the installer. Check **"Add to PATH"** ✅
4. Open a **new PowerShell** window (not inside any IDE) and verify:

```powershell
node --version
npm --version
```

> **Trouble?** If the commands are not found after a fresh terminal window, look up [npm or codemie command not found](tools/SKILL.md) in the SKILL.md.

---

## Part 2: Install CodeMie CLI

### What we'll do

Install the `@codemieai/code` npm package globally. This makes the `codemie` command available system-wide.

### Step 1 — Install

Run this in a terminal **outside of your IDE**:

```bash
npm install -g @codemieai/code
```

### Step 2 — Verify

```bash
codemie --version
```

Expected: `0.0.54` or higher.

> **Why does IDE terminal matter?**  
> IDE terminals (VS Code, Cursor) may have modified PATH environments that cause auth and PATH issues later. Always use the native terminal for setup steps.

---

## Part 3: Authenticate with `codemie setup`

### What we'll do

Run the interactive setup wizard. It connects CodeMie CLI to your auth provider and stores credentials in a named profile. The profile is used by all agent commands later.

### Step 1 — Run the wizard

```bash
codemie setup
```

If the browser doesn't open automatically: see [Browser doesn't open during codemie setup](tools/SKILL.md) in the SKILL.md.

### Step 2 — Follow the prompts

The wizard will ask you to choose a storage location, add a profile, and select a provider. Example for CodeMie SSO:

| Prompt | Selection |
|---|---|
| Where to store configuration? | Global (`~/.codemie/`) |
| Action | Add new profile |
| LLM provider | CodeMie SSO (or your company's provider) |
| Organization URL | Your CodeMie instance URL |
| Model | `claude-sonnet-4-6` |
| Profile name | e.g. `work-coding` |

### Step 3 — Run a health check

```bash
codemie doctor
```

Confirm at minimum:

```
✓ SSO credentials stored
✓ Model available
```

> Warnings about Python or `uv` are safe to ignore at this stage — see [Python and uv warnings](tools/SKILL.md) in the SKILL.md for why.

---

## Part 4: Install an AI Agent

### What we'll do

Install one or more AI coding agents. CodeMie wraps them to route traffic through your authenticated profile.

### Step 1 — Choose and install

```bash
# Claude Code (recommended — tested with your CodeMie version)
codemie install claude --supported

# Gemini CLI (Google)
codemie install gemini

# OpenCode (open-source)
codemie install opencode

# Claude Code via ACP protocol (for Zed, JetBrains, Emacs)
codemie install claude-acp
```

Install at least one. `claude --supported` is the recommended starting point.

### Step 2 — Verify the agent command is available

```bash
claude --version
```

> If the agent command is not found: see [Agent command not found](tools/SKILL.md) in the SKILL.md.

---

## Part 5: Connect to Your IDE

### What we'll do

Make the installed agent accessible from inside your editor.

### VS Code (simplest path)

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Search **Claude Code for VS Code** (publisher: Anthropic) and install
4. Open the command palette (`Ctrl+Shift+P`) and run **Claude Code: Open**

Claude Code will launch using the globally installed `claude` binary, which CodeMie already configured. No additional proxy setup needed for VS Code.

### Cursor (requires proxy)

Cursor's Claude Code extension needs a proxy wrapper that redirects requests through CodeMie instead of directly to Anthropic. The SKILL.md has the full step-by-step proxy setup.

**Option A — follow the SKILL.md with your agent**

1. Open a chat with your AI agent in any editor
2. Attach `modules/175-codemie-cli/tools/SKILL.md`
3. Ask: *"Help me set up the Cursor proxy for CodeMie on my platform (macOS/Windows)"*
4. Follow the generated steps — the agent will read the correct platform section and adapt paths to your username

**Option B — follow manually**

See the [Cursor section](tools/SKILL.md) in the SKILL.md. It covers:

- Creating the proxy script (`~/.local/bin/claude-codemie-proxy` on macOS, `.exe` on Windows)
- Adding `claudeCode.claudeProcessWrapper` to `settings.json`
- Restarting Cursor completely (not just Reload Window)

### Other IDEs (ACP protocol — Zed, JetBrains, Emacs)

See [Other IDEs via ACP Protocol](tools/SKILL.md) in the SKILL.md for ready-to-paste config snippets.

---

## Part 6: Verify the Full Setup

### Step 1 — Run the full health check

```bash
codemie doctor
```

Expected final output:

```
✓ Node.js version compatible
✓ API authentication successful
✓ SSO credentials stored
✓ Model available
✓ CodeMie Code installed
```

All five checks should be green. Python/uv warnings are acceptable.

### Step 2 — Send a test message from the IDE

Open **Claude Code: Open** in VS Code (or the Cursor equivalent) and type:

```
Hello! What model are you running on?
```

A response confirms the full chain: IDE → extension → agent → CodeMie proxy → LLM is working.

---

## Success Criteria

- ✅ `node --version` and `npm --version` both print version numbers
- ✅ `codemie --version` prints `0.0.54` or higher
- ✅ `codemie doctor` shows all five required checks as ✓
- ✅ At least one agent (`claude`, `gemini`, or `opencode`) is installed and responds to `--version`
- ✅ The agent is reachable from inside VS Code or Cursor

---

## Understanding Check

1. **Why must `codemie setup` be run outside of the IDE terminal?**  
   *(IDE terminals can inherit modified PATH and env vars that interfere with authentication and PATH resolution)*

2. **What does `codemie doctor` check, and what does a Python/uv warning mean?**  
   *(Checks Node.js compat, auth, SSO, model availability, agent install. Python warnings are informational — they appear when Python or uv is not installed, but the core CLI still works.)*

3. **Why does Cursor need a proxy script but VS Code does not?**  
   *(Cursor's extension uses `claudeProcessWrapper` to intercept the claude binary path. VS Code's Claude Code extension calls the binary directly from PATH — which CodeMie already controls.)*

4. **What is the `--supported` flag on `codemie install claude`?**  
   *(Installs the specific Claude Code version tested with your CodeMie CLI version, avoiding compatibility issues with the absolute latest release.)*

5. **How do you use `tools/SKILL.md` for troubleshooting in an agentic workflow?**  
   *(Attach it to your AI agent chat session and describe the error — the agent reads the relevant FAQ section and provides adapted fix commands.)*

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `codemie: command not found` after install | Open a **new** terminal window (PATH is loaded at shell start) |
| Browser doesn't open during `codemie setup` | See [Browser doesn't open](tools/SKILL.md) in SKILL.md |
| `EACCES: permission denied` on npm install | See [npm error EACCES](tools/SKILL.md) in SKILL.md (macOS) |
| PowerShell blocks npm scripts | See [PowerShell blocks npm scripts](tools/SKILL.md) in SKILL.md (Windows) |
| Cursor shows "Injection done!" but model not responding | Check `settings.json` path and restart Cursor completely (not Reload Window) |
| `codemie doctor` shows SSO expired | See [SSO session expired](tools/SKILL.md) in SKILL.md |
| `spawn EINVAL` in Cursor | Windows-specific — see [spawn EINVAL in Cursor](tools/SKILL.md) in SKILL.md |

For issues not listed here, attach `tools/SKILL.md` to your AI agent and describe what you see.

---

## Next Steps

After this module you have a working CodeMie CLI and IDE integration. Next:

- **Module 180 — DIAL LangChain Python Integration** — use the LLM access you just set up in Python scripts
- **Module 076 — Skills Management System** — learn how SKILL.md files like `tools/SKILL.md` are authored, stored, and distributed across teams
