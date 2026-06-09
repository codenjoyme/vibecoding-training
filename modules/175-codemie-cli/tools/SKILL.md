# CodeMie CLI FAQ

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Step 1 — Install Node.js](#step-1--install-nodejs)
  - [Step 2 — Install CodeMie CLI](#step-2--install-codemie-cli)
  - [Step 3 — Install Python (recommended)](#step-3--install-python-recommended)
  - [Step 4 — Authenticate](#step-4--authenticate)
  - [Step 5 — Install an Agent](#step-5--install-an-agent)
- [Verify Setup](#verify-setup)
- [IDE Integration](#ide-integration)
  - [Cursor](#cursor)
    - [1. Install the Extension](#1-install-the-extension)
    - [2. Set Up the Proxy](#2-set-up-the-proxy)
    - [3. Configure Cursor Settings](#3-configure-cursor-settings)
    - [4. Restart Cursor and Test](#4-restart-cursor-and-test)
  - [VS Code](#vs-code)
  - [Other IDEs via ACP Protocol](#other-ides-via-acp-protocol)
- [FAQ / Common Issues](#faq--common-issues)
  - [macOS](#macos)
    - [npm or codemie command not found](#macos-npm-not-found)
    - [Agent command not found (claude, codemie-claude, etc.)](#macos-agent-not-found)
    - [Browser doesn’t open during codemie setup](#macos-browser-sso)
    - [Query closed before response received in the IDE](#macos-query-closed)
    - [SSO session expired error in the IDE](#macos-sso-expired)
    - [Python and uv warnings in codemie doctor](#macos-python-warnings)
    - [npm error EACCES: permission denied](#macos-npm-eacces)
  - [Windows](#windows)
    - [npm or codemie command not found](#win-npm-not-found)
    - [PowerShell blocks npm scripts](#win-powershell-policy)
    - [Agent command not found (claude, codemie-claude, etc.)](#win-agent-not-found)
    - [Browser doesn’t open during codemie setup](#win-browser-sso)
    - [Query closed before response received in the IDE](#win-query-closed)
    - [spawn EINVAL in Cursor](#win-spawn-einval)
    - [SSO session expired error in the IDE](#win-sso-expired)
    - [Python and uv warnings in codemie doctor](#win-python-warnings)
    - [codemie install claude --supported - Failed (Checksum verification failed)](#win-checksum-failed)
    - [E404 - Not Found for the codemie package](#win-e404)
    - [CodeMie Proxy Gateway Does Not Appear in Claude App](#codemie-proxy-gateway)
    - [Commands not found after npm install -g @codemieai/code](#win-commands-not-found)
- [GitHub Copilot Integration (OpenAI Compatible)](#ghcp-openai-compatible)
  - [Fixing Tool Calls — Unknown tokenizer fix](#ghcp-relay-fix)
- [Sources](#sources)

---

## CodeMie CLI — Installation Guide

What this gives you: A unified AI coding assistant CLI with support for Claude Code, Gemini, OpenCode, and more. Supports multiple authentication providers — enterprise SSO, JWT, OpenAI-compatible APIs, and others.

---

## Prerequisites

- Node.js — installed in Step 1

> [!CAUTION]
> All commands must be run in a terminal **outside of any IDE** (Terminal on macOS, PowerShell or CMD on Windows). Running them inside an IDE’s built-in terminal may cause PATH and authentication issues.

---

## Installation

### Step 1 — Install Node.js <a id="step-1--install-nodejs"></a>

**macOS**

1. Go to [https://nodejs.org](https://nodejs.org)
2. Click the LTS download button
3. Run the `.pkg` installer
4. Open a new Terminal and verify:

```
node --version
npm --version
```

Both should print a version number (e.g. `v24.x.x` and `11.x.x`).

**Windows**

1. Go to [https://nodejs.org/en/download](https://nodejs.org/en/download)
2. The page may default to Docker instructions — scroll down and click **Windows Installer (.msi)**
3. Run the installer. Make sure to check **“Add to PATH”** ✅
4. Open a new PowerShell window and verify:

```
node --version
npm --version
```

Both should print a version number (e.g. `v24.x.x` and `11.x.x`).

---

### Step 2 — Install CodeMie CLI <a id="step-2--install-codemie-cli"></a>

```bash
npm install -g @codemieai/code
```

If npm is not recognized: [macOS](#macos-npm-not-found) · [Windows](#win-npm-not-found)

Verify:

```bash
codemie --version
```

Should print `0.0.54` or higher.

If codemie is not recognized: [macOS](#macos-npm-not-found) · [Windows](#win-npm-not-found) · [Windows: PowerShell policy](#win-powershell-policy)

---

### Step 3 — Install Python (recommended) <a id="step-3--install-python-recommended"></a>

Some CodeMie agents use Python-based tools at runtime. The core setup works without Python, but install it when in doubt.

1. Go to [https://python.org/downloads](https://python.org/downloads)
2. Download Python 3.13.x (latest stable)
3. Run the installer — on Windows, check **“Add Python to PATH”** ✅

---

### Step 4 — Authenticate <a id="step-4--authenticate"></a>

```bash
codemie setup
```

If the browser doesn’t open: [macOS](#macos-browser-sso) · [Windows](#win-browser-sso)

The wizard will prompt for your provider and credentials. Example using CodeMie SSO:

| Prompt | Selection |
|---|---|
| Where to store configuration? | Global (`~/.codemie/`) |
| Action | Add new profile |
| LLM provider | Choose your provider (e.g. CodeMie SSO, LiteLLM, Azure OpenAI) |
| Organization URL | Your CodeMie instance URL, if applicable |
| Model | `claude-sonnet-4-6` (or another available model) |
| Profile name | e.g. `work-coding` |

Run a health check:

```bash
codemie doctor
```

Confirm at minimum:

```
✓ SSO credentials stored
✓ Model available
```

Warnings about Python or uv are safe to ignore — see FAQ: [macOS](#macos-python-warnings) · [Windows](#win-python-warnings)

---

### Step 5 — Install an Agent <a id="step-5--install-an-agent"></a>

CodeMie supports multiple AI coding agents. Install one or more:

```bash
codemie install claude --supported   # Claude Code (Anthropic)
codemie install gemini               # Gemini CLI (Google)
codemie install opencode             # OpenCode (open-source)
codemie install claude-acp           # Claude Code for IDE integration via ACP protocol
```

Use `--supported` for Claude Code to install the version tested with your CodeMie CLI version. CodeMie notifies you when running a different version.

If an agent command is not found after installation: [macOS](#macos-agent-not-found) · [Windows](#win-agent-not-found)

**Claude Code version options**

```bash
codemie install claude --supported   # Latest version tested with your CodeMie CLI (recommended)
codemie install claude 2.1.22        # Specific version
codemie install claude               # Absolute latest (may not be tested)
```

---

## Verify Setup <a id="verify-setup"></a>

```bash
codemie doctor
```

Expected output:

```
✓ Node.js version compatible
✓ API authentication successful
✓ SSO credentials stored
✓ Model available
✓ CodeMie Code installed
```

---

## IDE Integration <a id="ide-integration"></a>

- [Cursor](#cursor)
- [VS Code](#vs-code)
- [Zed, JetBrains, Emacs (ACP)](#other-ides-via-acp-protocol)

---

### Cursor <a id="cursor"></a>

The Claude Code extension for Cursor needs a proxy that routes requests through CodeMie instead of directly to Anthropic.

#### 1. Install the Extension <a id="1-install-the-extension"></a>

1. Open Cursor
2. Go to Extensions (`Cmd+Shift+X` / `Ctrl+Shift+X`)
3. Search for **Claude Code for VS Code** (publisher: Anthropic) and install it

#### 2. Set Up the Proxy <a id="2-set-up-the-proxy"></a>

**macOS**

Run in Terminal (outside of Cursor):

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/claude-codemie-proxy << 'EOF'
#!/bin/bash
CODEMIE_CLAUDE="/opt/homebrew/bin/codemie-claude"
LOG_FILE="$HOME/.local/share/claude-codemie-proxy.log"

mkdir -p "$(dirname "$LOG_FILE")"
echo "[$( date -u +%Y-%m-%dT%H:%M:%SZ)] ARGS: $*" >> "$LOG_FILE"

# Strip leading executable paths injected by claudeProcessWrapper
while [[ $# -gt 0 && -f "$1" && -x "$1" ]]; do shift; done

exec "$CODEMIE_CLAUDE" "$@"
EOF
chmod +x ~/.local/bin/claude-codemie-proxy
```

If CodeMie was installed via npm instead of Homebrew, run `which codemie-claude` to find the correct path and update `CODEMIE_CLAUDE` in the script.

**Windows**

**a. Create the proxy JavaScript file**

```powershell
notepad "$env:USERPROFILE\.local\bin\proxy.js"
```

Paste the following. Replace both `<you>` placeholders with your Windows username, save and close:

```js
'use strict';
var spawn = require('child_process').spawn;
var fs = require('fs');
var path = require('path');

var CODEMIE_SCRIPT = 'C:\\Users\\<you>\\AppData\\Roaming\\npm\\node_modules\\@codemieai\\code\\bin\\codemie-claude.js';
var LOCAL_BIN = 'C:\\Users\\<you>\\.local\\bin';

function findNodeExe() {
  var dirs = (process.env.PATH || '').split(path.delimiter);
  for (var i = 0; i < dirs.length; i++) {
    var candidate = path.join(dirs[i], 'node.exe');
    try { fs.accessSync(candidate, fs.constants.F_OK); return candidate; } catch (e) {}
  }
  return 'C:\\Program Files\\nodejs\\node.exe';
}

var nodeExe = findNodeExe();
if ((process.env.PATH || '').indexOf(LOCAL_BIN) === -1) {
  process.env.PATH = (process.env.PATH || '') + path.delimiter + LOCAL_BIN;
}

var rawArgs = process.argv.slice(2);
var skip = 0;
while (skip < rawArgs.length && fs.existsSync(rawArgs[skip])) { skip++; }
var claudeArgs = rawArgs.slice(skip);

var child = spawn(nodeExe, [CODEMIE_SCRIPT].concat(claudeArgs), { stdio: 'inherit', env: process.env });
child.on('exit', function (code) { process.exit(code !== null ? code : 0); });
child.on('error', function () { process.exit(1); });
```

Run `npm root -g` to find the correct npm global modules path if yours differs from the default.

**b. Build the proxy executable**

```powershell
cd "$env:USERPROFILE\.local\bin"

@{
    main = "$env:USERPROFILE\.local\bin\proxy.js"
    output = "$env:USERPROFILE\.local\bin\sea-prep.blob"
    disableExperimentalSEAWarning = $true
} | ConvertTo-Json | Set-Content sea-config.json

node --experimental-sea-config sea-config.json
node -e "require('fs').copyFileSync(process.execPath, 'claude-codemie-proxy.exe')"
npx postject claude-codemie-proxy.exe NODE_SEA_BLOB sea-prep.blob --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2 --overwrite
```

Expected: output ends with `Injection done!`. The warning `The signature seems corrupted!` line before it is normal on Windows.

#### 3. Configure Cursor Settings <a id="3-configure-cursor-settings"></a>

**macOS** — `~/Library/Application Support/Cursor/User/settings.json`

```json
{
  "claudeCode.claudeProcessWrapper": "/Users/<you>/.local/bin/claude-codemie-proxy",
  "claudeCode.disableLoginPrompt": true
}
```

**Windows** — open with `notepad "$env:APPDATA\Cursor\User\settings.json"`

Add a comma after the last existing entry, then insert before the closing `}`:

```json
{
  "existing.setting": "...",
  "claudeCode.claudeProcessWrapper": "C:\\Users\\<you>\\.local\\bin\\claude-codemie-proxy.exe",
  "claudeCode.disableLoginPrompt": true
}
```

> ⚠️ **Bedrock conflict:** If `settings.json` has `claudeCode.environmentVariables` with `CLAUDE_CODE_USE_BEDROCK` or `AWS_PROFILE`, remove them or set the array to `[]`. See [FAQ](#win-sso-expired) for why.

#### 4. Restart Cursor and Test <a id="4-restart-cursor-and-test"></a>

Close Cursor completely (`Cmd+Q` / `Alt+F4`) and reopen it — “Developer: Reload Window” is not enough. Then open **Claude Code: Open** from the More actions menu (⋯) and send a message. Claude should reply within a few seconds.

---

### VS Code <a id="vs-code"></a>

1. Go to Extensions (`Cmd+Shift+X` / `Ctrl+Shift+X`)
2. Search for **Claude Code for VS Code** (publisher: Anthropic) and install it
3. Open the command palette and run **Claude Code: Open**

**Windows only:** VS Code also requires `claudeCode.claudeProcessWrapper` pointing to the `.exe` proxy (same setup as [Cursor › Set Up the Proxy](#2-set-up-the-proxy)). Without it you will get `spawn EINVAL`. Add to `%APPDATA%\Code\User\settings.json` (or `%APPDATA%\Code - Insiders\User\settings.json` for VS Code Insiders):

```json
"claudeCode.claudeProcessWrapper": "C:\\Users\\<you>\\.local\\bin\\claude-codemie-proxy.exe",
"claudeCode.disableLoginPrompt": true
```

Restart VS Code completely (not Reload Window) after saving.

---

### Other IDEs via ACP Protocol <a id="other-ides-via-acp-protocol"></a>

```bash
codemie install claude-acp
```

**Zed** — `~/.config/zed/settings.json`

```json
{
  "agent_servers": {
    "claude": {
      "command": "codemie-claude-acp",
      "args": ["--profile", "work-coding"]
    }
  }
}
```

**JetBrains** — `~/.jetbrains/acp.json`

```json
{
  "default_mcp_settings": {},
  "agent_servers": {
    "Claude Code via CodeMie": {
      "command": "codemie-claude-acp",
      "args": ["--profile", "work-coding"]
    }
  }
}
```

**Emacs** — with `acp.el`

```elisp
(setq acp-claude-command "codemie-claude-acp")
(setq acp-claude-args '("--profile" "work-coding"))
```

---

## FAQ / Common Issues <a id="faq--common-issues"></a>

### macOS <a id="macos"></a>

#### npm or codemie command not found <a id="macos-npm-not-found"></a>

**Why it happens:** Installers modify PATH in your shell profile, but the current terminal session has a frozen copy of the environment from when it started and won’t see the change.

**Fix:** Open a new Terminal window after installing Node.js or CodeMie CLI and retry the command.

---

#### Agent command not found (claude, codemie-claude, etc.) <a id="macos-agent-not-found"></a>

**Why it happens:** Agents are installed to `~/.local/bin/`, which is not in PATH by default on macOS.

**Fix:**

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

If you use bash instead of zsh, replace `~/.zshrc` with `~/.bash_profile`. Verify with `which claude` — should print `/Users/<you>/.local/bin/claude`.

---

#### Browser doesn’t open during codemie setup <a id="macos-browser-sso"></a>

**Why it happens:** The SSO flow needs to launch your default browser. IDEs intercept process spawning in their built-in terminals, which can silently block the browser launch or capture the callback URL.

**Fix:** Run `codemie setup` in a regular Terminal window, not inside any IDE.

---

#### Query closed before response received in the IDE <a id="macos-query-closed"></a>

**Why it happens:** The Claude Code extension spawns the Claude binary as a subprocess that inherits the IDE’s environment — not your shell’s. If `~/.local/bin` wasn’t in PATH when the IDE launched, the binary cannot be found.

**Fix:** Fully close the IDE (`Cmd+Q`) and reopen it. “Developer: Reload Window” is not enough — it reuses the same process with a frozen environment. A fresh launch re-reads your shell profile and picks up the updated PATH.

---

#### SSO session expired error in the IDE <a id="macos-sso-expired"></a>

**Why it happens:** If `settings.json` has `claudeCode.environmentVariables` containing `CLAUDE_CODE_USE_BEDROCK` or `AWS_PROFILE`, the extension authenticates via AWS SSO instead of CodeMie. When that AWS session expires, all requests fail — even though your CodeMie credentials are valid.

**Fix:** Open `~/Library/Application Support/Cursor/User/settings.json` (or VS Code equivalent) and remove those keys, or set the array to `[]`:

```json
"claudeCode.environmentVariables": []
```

---

#### Python and uv warnings in codemie doctor <a id="macos-python-warnings"></a>

**Why it happens:** Some CodeMie agents use Python-based tools at runtime. `uv` is a Python package manager those agents depend on. `codemie doctor` reports them missing as a warning, not an error.

These warnings do not affect Claude Code. Install Python from [python.org](https://python.org/downloads) only if you plan to use agents that require it.

---

#### npm error Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules/@codemieai' <a id="macos-npm-eacces"></a>

**Why it happens:** Node.js installed via the `.pkg` installer puts global `node_modules` in `/usr/local/lib`, which is owned by root.

**Fix:** Reconfigure npm to use a user-writable directory:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
npm install -g @codemieai/code
```

Alternatively, install Node.js via nvm — it installs into the user’s home directory and avoids permission issues entirely.

---

### Windows <a id="windows"></a>

#### npm or codemie command not found <a id="win-npm-not-found"></a>

**Why it happens:** The current PowerShell session has a frozen copy of PATH from before Node.js was installed. Additionally, the Node.js installer only adds to PATH if the option was checked during setup.

**Fix:** Open a new PowerShell window and retry. If the command is still not found, reinstall Node.js and make sure **“Add to PATH”** ✅ is checked in the installer.

---

#### PowerShell blocks npm scripts <a id="win-powershell-policy"></a>

**Why it happens:** Windows restricts script execution by default. npm global packages install `.ps1` shims that PowerShell refuses to run under the default `Restricted` or `RemoteSigned` policy.

**Fix:** Run once in PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Alternatively, use Command Prompt (`cmd`) — it does not have this restriction.

---

#### Agent command not found (claude, codemie-claude, etc.) <a id="win-agent-not-found"></a>

**Why it happens:** Agents are installed to `C:\Users\<you>\.local\bin\`, which Windows does not add to PATH automatically.

**Fix:** Run in PowerShell:

```powershell
$localBin = "$env:USERPROFILE\.local\bin"
$current = [Environment]::GetEnvironmentVariable("Path", "User")
if ($current -notlike "*$localBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$current;$localBin", "User")
    Write-Host "Added to PATH"
} else {
    Write-Host "Already in PATH"
}
```

Open a new PowerShell window after running this — the current session won’t see the change.

---

#### Browser doesn’t open during codemie setup <a id="win-browser-sso"></a>

**Why it happens:** The SSO flow needs to launch your default browser. IDEs intercept process spawning in their built-in terminals, which can silently block the browser launch or capture the callback URL.

**Fix:** Run `codemie setup` in a regular PowerShell or CMD window, not inside any IDE.

---

#### Query closed before response received in the IDE <a id="win-query-closed"></a>

**Why it happens:** The Claude Code extension spawns the Claude binary as a subprocess that inherits the IDE’s environment — not your shell’s. If `.local\bin` wasn’t in PATH when the IDE launched, the binary cannot be found.

**Fix:** Fully close the IDE (`File → Exit`) and reopen it. “Developer: Reload Window” is not enough — it reuses the same process with a frozen environment. A fresh launch re-reads your user PATH and picks up the updated value.

---

#### spawn EINVAL in Cursor <a id="win-spawn-einval"></a>

**Why it happens:** npm sometimes creates a `.cmd` wrapper instead of a real executable. The Claude Code extension expects a proper `.exe` and throws `EINVAL` when given a script file.

**Fix:** Rebuild the proxy executable using the steps in [Cursor › Set Up the Proxy](#2-set-up-the-proxy). The SEA build produces a real `.exe` the extension can spawn directly.

---

#### SSO session expired error in the IDE <a id="win-sso-expired"></a>

**Why it happens:** If `settings.json` has `claudeCode.environmentVariables` containing `CLAUDE_CODE_USE_BEDROCK` or `AWS_PROFILE`, the extension authenticates via AWS SSO instead of CodeMie. When that AWS session expires, all requests fail — even though your CodeMie credentials are valid.

**Fix:** Open `%APPDATA%\Cursor\User\settings.json` (or VS Code equivalent) and remove those keys, or set the array to `[]`:

```json
"claudeCode.environmentVariables": []
```

---

#### Python and uv warnings in codemie doctor <a id="win-python-warnings"></a>

**Why it happens:** Some CodeMie agents use Python-based tools at runtime. `uv` is a Python package manager those agents depend on. `codemie doctor` reports them missing as a warning, not an error.

These warnings do not affect Claude Code. Install Python from [python.org](https://python.org/downloads) only if you plan to use agents that require it.

---

#### codemie install claude --supported - Failed with message: "Failed to install agent claude: Installer exited with code 1. Output: Checksum verification failed" <a id="win-checksum-failed"></a>

**Why it happens:** The Claude binary download was interrupted or corrupted, or a corporate proxy is rewriting the response body.

**Fix:**

1. Delete cached files:
   ```powershell
   Remove-Item -Recurse "$env:USERPROFILE\.local\share\codemie" -Force
   ```
2. Retry:
   ```powershell
   codemie install claude --supported
   ```
3. If it fails again, run the command in CMD (not PowerShell) — proxies sometimes handle `.exe` downloads differently per user-agent.
4. If behind a corporate proxy, check with your IT team that the proxy allows binary downloads from: [github.com/anthropics](https://github.com/anthropics).

---

#### E404 - Not Found for the codemie package when running 'npm install -g codemie' <a id="win-e404"></a>

**Why it happens:** Your npm is configured to use a corporate registry that does not proxy the `@codemieai` scope, or the wrong package name was used (`codemie` instead of `@codemieai/code`).

**Fix:**

1. Check current registry:
   ```bash
   npm config get registry
   ```
2. Install from the public registry explicitly:
   ```bash
   npm install -g @codemieai/code --registry https://registry.npmjs.org
   ```
3. Or temporarily reset to public registry:
   ```bash
   npm config set registry https://registry.npmjs.org
   ```

---

#### CodeMie Proxy Gateway Does Not Appear in Claude App <a id="codemie-proxy-gateway"></a>

If you do not see **CodeMie Proxy Gateway (Continue with Gateway)** while signing into the Claude application, please follow these steps:

**1. Authenticate in CodeMie via terminal**

Run the following command:

```bash
codemie profile refresh
```

Your browser will open automatically and complete the authentication process.

Example of a successful output:

```
⧋ Launching SSO authentication...Opening browser for authentication...
✔ SSO authentication successful
🔗 Connected to: https://codemie.lab.epam.com
🔑 Credentials stored securely
```

**2. Start the proxy gateway**

Run:

```bash
codemie proxy start desktop
```

Example of a successful output:

```
✓ Proxy already running at http://127.0.0.1:4001  (profile: default)
```

**3. Launch the Claude application**

Only after completing steps 1 and 2, start the Claude application.

You should now see the following option during login:

> **CodeMie Proxy Gateway (Continue with Gateway)**

This is the correct option to use when working through the CodeMie Proxy.

---

#### Commands not found after running npm install -g @codemieai/code (codemie: command not found) <a id="win-commands-not-found"></a>

**Why it happens:** npm installed the package to a custom prefix directory (e.g. `~/.npm-global`) that is not in your `$PATH`. This typically occurs on macOS with Homebrew Node.js when the default global modules directory does not exist yet and npm falls back to a user-local prefix.

**Fix:**

1. Check where npm installed the binaries:
   ```bash
   npm config get prefix
   ```
2. Check if that directory is in your PATH:
   ```bash
   echo $PATH | tr ':' '\n' | grep npm
   ```
3. If missing — add it to your shell config:
   ```bash
   echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```
4. Verify:
   ```bash
   which codemie
   codemie --version
   ```

> **Note:** Replace `~/.npm-global` with the actual prefix from step 1 if different. For bash users replace `~/.zshrc` with `~/.bash_profile`.

---

#### codemie install claude times out with "Command timed out after 300000ms"

**Why it happens:** `npm install -g @anthropic-ai/claude-code` is taking longer than 5 minutes. Typically caused by a slow or corporate npm registry that proxies the `@anthropic-ai` scope slowly or blocks it entirely.

**Fix:**

1. Install Claude Code manually bypassing corporate registry:
   ```bash
   npm install -g @anthropic-ai/claude-code --registry https://registry.npmjs.org
   ```
2. Then retry:
   ```bash
   codemie install claude
   ```
   `codemie` will detect it’s already installed and skip the download.

---

## GitHub Copilot Integration (OpenAI Compatible) <a id="ghcp-openai-compatible"></a>

CodeMie's local proxy daemon exposes a fully **OpenAI-compatible REST API** at `http://127.0.0.1:4001/v1`. This means GitHub Copilot (VS Code) can use it as an "OpenAI Compatible" custom model provider — routing Copilot model requests through your corporate CodeMie authentication.

A relay proxy (`codemie-relay.js`) sits between Copilot and CodeMie on port 4002. It handles:
- **Multi-model routing** — reads `realModelId` from `chatLanguageModels.json` and translates model names automatically
- **Auth passthrough** — accepts any API key from Copilot, forwards with the correct gateway key
- **Parameter fixing** — removes `top_p` when `temperature` is also present (Bedrock Claude rejects both)
- **Response patching** — echoes back the fake model id so Copilot resolves the tokenizer correctly

### Step 1 — Start the proxy daemon

```bash
codemie proxy start
```

Verify: `codemie proxy status` should show `running` at `http://127.0.0.1:4001`.

### Step 2 — Find the gateway key

The local key is stored in `~/.codemie/proxy-daemon.json` under `gatewayKey`. Default value: `codemie-proxy`.

```bash
# macOS/Linux
cat ~/.codemie/proxy-daemon.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['gatewayKey'])"

# Windows PowerShell
python -c "import json,os; d=json.load(open(os.path.join(os.environ['USERPROFILE'],'.codemie','proxy-daemon.json'))); print(d['gatewayKey'])"
```

### Step 3 — Add custom models in GitHub Copilot

The `chatLanguageModels.json` file is located at:
- **Windows:** `%APPDATA%\Code - Insiders\User\chatLanguageModels.json` (or `Code\User\` for stable)
- **macOS:** `~/Library/Application Support/Code - Insiders/User/chatLanguageModels.json`
- **Linux:** `~/.config/Code - Insiders/User/chatLanguageModels.json`

Add a vendor block with your models. Each model needs:
- `id` — a Copilot-known tokenizer name (`gpt-4`, `gpt-4o`, `gpt-4o-mini`, `o1`, etc.)
- `realModelId` — the actual CodeMie model name (find exact names with `list-codemie-models.ps1`)
- `url` — pointing to the relay on port 4002

```json
{
  "name": "CodeMie Proxy",
  "vendor": "customoai",
  "apiKey": "${input:chat.lm.secret.codemie}",
  "models": [
    {
      "id": "gpt-4",
      "realModelId": "claude-sonnet-4-6",
      "name": "Claude Sonnet 4.6 (CodeMie)",
      "url": "http://127.0.0.1:4002/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 200000,
      "maxOutputTokens": 16000
    },
    {
      "id": "gpt-4o",
      "realModelId": "claude-opus-4-6-20260205",
      "name": "Claude Opus 4.6 (CodeMie)",
      "url": "http://127.0.0.1:4002/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 200000,
      "maxOutputTokens": 16000
    }
  ]
}
```

A ready-to-use reference config: `tools/chatLanguageModels.js`

1. Open VS Code command palette → **GitHub Copilot: Manage Models** (or open the Language Models panel)
2. The config file above is the programmatic equivalent of adding models via the UI
3. Save and **Reload Window**
4. Select the model in Copilot Chat — VS Code will ask for an API key once: enter any non-empty string (e.g. `sk-codemie`)

### Available models (example)

The full list is returned by `GET http://127.0.0.1:4001/v1/models` with `Authorization: Bearer codemie-proxy`. Common entries:

```
claude-sonnet-4-6        claude-opus-4-6-...      claude-haiku-4-5-...
gpt-4.1                  gpt-4.1-mini             gpt-5-2025-08-07
o3-mini                  o3-2025-04-16            deepseek-r1
gemini-3.5-flash         gemini-3.1-pro           qwen.qwen3-coder-480b-...
```

### Notes

- The proxy daemon **must be running** when Copilot makes requests. Add `codemie proxy start` to your shell startup or run it manually before using Copilot.
- The proxy key (`codemie-proxy`) is a **local-only** pass-through key — it is not your SSO credential. Authentication with the corporate endpoint happens inside the daemon using your stored SSO session.
- If the SSO session expires (`codemie doctor` shows SSO expired), re-run `codemie setup` or `codemie profile login` and then restart the proxy.
- The daemon auto-selects port 4001. If that port is busy, start with `codemie proxy start --port <other-port>` and update the URL in Copilot settings.

### Fixing Tool Calls — Unknown tokenizer fix <a id="ghcp-relay-fix"></a>

GitHub Copilot's `customoai` (BYOK) endpoint has a known bug: tool calls fail with `Unknown tokenizer: undefined` because the `JN` class that wraps custom models stores `tokenizer` as a prototype getter, not an own property. When Copilot spreads the endpoint `{...endpoint, modelMaxPromptTokens: X}`, prototype getters are not copied → `tokenizer` becomes `undefined` → every tool call fails.

This affects all `customoai` integrations (DIAL, CodeMie, any other BYOK entry).

**Fix A — Patch extension.js (one-time, re-run after Copilot extension updates)**

Run `patch_jn.py` from the module tools folder. It adds `Object.defineProperty` to the `JN` constructor so `tokenizer` becomes an own enumerable property that survives the spread.

```powershell
# Run from the directory that contains the VSCode installation
# (e.g. C:\Java if VS Code Insiders is in C:\Java\VSCode-win32-x64-...)
python modules/175-codemie-cli/tools/patch_jn.py
```

Expected output: `Found target: ... Patched successfully!`

Then **Reload Window** in VS Code Insiders (Ctrl+Shift+P → Developer: Reload Window).

**Fix B — Relay proxy for model name translation (multi-model)**

Copilot sends the `id` from `chatLanguageModels.json` as the model name. The CodeMie proxy only recognises real model names like `claude-sonnet-4-6`, not `gpt-4`. The relay:
- Translates model names in both directions (request: fake→real, response: real→fake)
- Removes the `top_p` / `temperature` conflict that Bedrock Claude rejects
- Supports **multiple models** via `MODEL_MAP` built from `chatLanguageModels.json`

### Multi-model support via `realModelId`

Add a `realModelId` field to each model entry in `chatLanguageModels.json`. The relay reads this field at startup and builds a mapping table automatically:

```json
{
  "name": "CodeMie Proxy",
  "vendor": "customoai",
  "apiKey": "${input:chat.lm.secret.codemie}",
  "models": [
    {
      "id": "gpt-4",
      "realModelId": "claude-sonnet-4-6",
      "name": "Claude Sonnet 4.6 (CodeMie)",
      "url": "http://127.0.0.1:4002/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 200000,
      "maxOutputTokens": 16000
    },
    {
      "id": "gpt-4o",
      "realModelId": "claude-opus-4-6-20260205",
      "name": "Claude Opus 4.6 (CodeMie)",
      "url": "http://127.0.0.1:4002/v1/chat/completions",
      "toolCalling": true,
      "vision": true,
      "maxInputTokens": 200000,
      "maxOutputTokens": 16000
    }
  ]
}
```

- `id` must be a Copilot-known tokenizer name (`gpt-4`, `gpt-4o`, `gpt-4o-mini`, `o1`, `o3-mini`, etc.) → resolves `o200k_base`
- `realModelId` is the actual CodeMie model name (use `list-codemie-models.ps1` to find exact names)
- VS Code ignores unknown fields — `realModelId` is safe to add

**To add a new model:** add an entry to `chatLanguageModels.json` with `realModelId`, restart relay. No code changes needed.

A ready-to-use reference config: `tools/chatLanguageModels.js`

### Listing available CodeMie models

```powershell
# Requires: codemie proxy start
.\list-codemie-models.ps1
```

Returns all model IDs available through your CodeMie proxy (sorted alphabetically). Use these exact names for `realModelId`.

### Startup script (`start.ps1`)

The `start.ps1` script automates the full startup sequence:

```powershell
cd modules/175-codemie-cli/tools
.\start.ps1
```

What it does (4 steps):
1. **Kill** — stops relay (by port 4002) and codemie proxy
2. **Start codemie proxy** — `codemie proxy start` (port 4001)
3. **List models** — shows all available CodeMie models
4. **Start relay daemon** — copies `codemie-relay.js` to `~/.local/bin/`, starts as background process (`Start-Process -WindowStyle Hidden`), logs to `~/.local/bin/codemie-relay.log`

After `start.ps1` finishes, both proxies run as daemons — terminal is free. Relay lives until reboot or `Stop-Process -Id <PID>`.

### Manual startup (without start.ps1)

```powershell
codemie proxy start                                              # port 4001
Copy-Item modules/175-codemie-cli/tools/codemie-relay.js "$env:USERPROFILE\.local\bin\codemie-relay.js"
node "$env:USERPROFILE\.local\bin\codemie-relay.js"            # port 4002 (foreground)
# Then Reload Window in VS Code
```

First time using the model in Copilot Chat, VS Code prompts "Enter API key for CodeMie Proxy" — enter any non-empty string (e.g. `sk-codemie`).

---

## Usage Analytics <a id="usage-analytics"></a>

Track token and session usage after running agents:

```bash
codemie analytics --last 7d          # summary for last 7 days
codemie analytics --last 7d -v       # per-session breakdown
codemie analytics --last 30d --export csv   # export to file
```

Filters: `--agent claude`, `--project myrepo`, `--from 2026-01-01 --to 2026-01-31`.

Data appears only after the first agent session completes. More detailed analytics (with token cost breakdown) are available in the CodeMie web platform under the same URL used during `codemie setup`.

---

## Sources <a id="sources"></a>

- [CodeMie CLI — GitHub](https://github.com/codemie-ai/codemie-code)
