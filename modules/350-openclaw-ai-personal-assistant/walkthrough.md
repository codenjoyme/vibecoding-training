# OpenClaw — AI Personal Assistant Platform - Hands-on Walkthrough

OpenClaw is an open-source platform that turns any LLM into a personal AI assistant you can talk to from your browser, phone, or any chat app. Unlike IDE-based assistants (Copilot, Cursor), OpenClaw runs as a local Gateway service with its own dashboard and connects to 20+ messaging platforms — WhatsApp, Telegram, Discord, Slack, iMessage, and more. It comes with built-in tools for running shell commands, browsing the web, reading/writing files, and can be extended with skills and plugins.

In this walkthrough, you'll install OpenClaw, connect it to an AI model, chat through the dashboard, try built-in tools, and optionally connect Telegram as a mobile channel.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## Part 1: Verify Node.js

### What We'll Check

OpenClaw requires Node.js 22.14 or later (Node 24 is recommended). Let's verify your installation before proceeding.

### Check Your Version

Open a terminal and run:

```bash
node --version
```

You should see `v22.14.0` or higher. If not, install or update Node.js from [nodejs.org](https://nodejs.org/).

**Windows users:** Both native Windows and WSL2 are supported. WSL2 is recommended for the full experience, but native Windows works fine for this walkthrough.

---

## Part 2: Install OpenClaw

### What We'll Do

Install the OpenClaw CLI globally. This gives you the `openclaw` command that manages the Gateway, runs onboarding, and controls all features.

### Install

**macOS / Linux / WSL2:**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell):**

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**Alternative: Install via npm (any platform):**

```bash
npm install -g openclaw
```

### What Just Happened

The installer downloaded the OpenClaw CLI and placed it in your PATH. You now have access to the `openclaw` command. The CLI is your single entry point for everything — installation, configuration, starting the Gateway, and managing channels.

### Verify Installation

```bash
openclaw --version
```

You should see the version number printed. If the command is not found, close and reopen your terminal to refresh the PATH.

---

## Part 3: Run Onboarding

### What We'll Do

The onboarding wizard walks you through the initial setup in about 2 minutes. It will:
- Ask you to choose a model provider (Anthropic, OpenAI, Google, etc.)
- Prompt you for an API key
- Configure the Gateway
- Optionally install the daemon (background service)

### Start Onboarding

```bash
openclaw onboard --install-daemon
```

### What to Expect

1. **Choose a model provider** — Select your preferred provider. If you have an Anthropic API key, choose Anthropic. OpenAI and Google are also supported. You can change this later.

2. **Enter your API key** — Paste the API key for your chosen provider. The key is stored locally in `~/.openclaw/` and never sent anywhere except to the provider's API.

3. **Gateway configuration** — Accept the defaults unless you have a specific reason to change them. The Gateway will listen on port `18789` by default.

4. **Daemon installation** — The `--install-daemon` flag sets up OpenClaw to run as a background service that starts automatically.

### What Just Happened

OpenClaw created a configuration file at `~/.openclaw/config.yaml` with your model provider settings. The Gateway daemon is now running in the background, ready to handle requests.

---

## Part 4: Verify the Gateway

### What We'll Check

The Gateway is the core of OpenClaw — it sits between you (via any channel) and the AI model. Let's make sure it's running.

### Check Status

```bash
openclaw gateway status
```

You should see the Gateway listening on port `18789`. If the Gateway is not running, start it manually:

```bash
openclaw gateway start
```

### What the Gateway Does

The Gateway is a local HTTP server that:
- Routes messages from any channel (dashboard, Telegram, WhatsApp, etc.) to the AI model
- Manages conversation history and context
- Executes tools on behalf of the AI (shell commands, web browsing, file operations)
- Enforces security controls (tool approval, sandboxing)

Think of it as your personal AI router — one model, many interfaces.

---

## Part 5: Chat Through the Dashboard

### What We'll Do

Open the Control UI — a built-in web dashboard where you can chat with your AI assistant directly in the browser. This is the fastest way to verify everything works.

### Open the Dashboard

```bash
openclaw dashboard
```

This opens a web page in your default browser (usually at `http://localhost:18789`).

### Try Your First Chat

1. Type a message in the chat input: `Hello! What can you do?`
2. You should get an AI response listing its capabilities
3. Try a follow-up: `What tools are available to you?`

The AI should mention tools like `exec`, `browser`, `web_search`, `read`, `write`, and more.

### What Just Happened

Your message went through this flow:
1. **Dashboard** → sent message via WebSocket to the Gateway
2. **Gateway** → forwarded the message to your configured model provider (e.g., Anthropic API)
3. **Model** → generated a response, potentially requesting tool calls
4. **Gateway** → executed any tool calls and returned the final response
5. **Dashboard** → displayed the response in your browser

---

## Part 6: Explore Built-in Tools

### What We'll Do

OpenClaw comes with powerful built-in tools that the AI can use autonomously. Let's try the most important ones through the dashboard chat.

### 6.1 Run a Shell Command (exec)

Ask the AI to run a command:

```
Can you check what version of Node.js is installed? Run `node --version` and tell me.
```

The AI will use the `exec` tool to run the command and report the output. Notice that OpenClaw may ask for your **approval** before executing — this is a security feature.

### 6.2 Search the Web (web_search)

Ask the AI to search for something:

```
Search the web for "OpenClaw AI latest features" and summarize what you find.
```

The AI uses the `web_search` tool to query the web and `web_fetch` to read page content.

### 6.3 Read and Write Files (read/write)

Ask the AI to create a file:

```
Create a file called hello.txt with the text "Hello from OpenClaw!" and then read it back to me.
```

The AI uses `write` to create the file and `read` to verify its contents.

### 6.4 Browse a Website (browser)

Ask the AI to check a webpage:

```
Open https://example.com in the browser and describe what you see.
```

The AI controls a headless Chromium browser via the `browser` tool — it can navigate, click, take screenshots, and extract content.

### Tool Approval Flow

By default, OpenClaw asks for approval before running potentially dangerous tools (like `exec`). You'll see prompts like:

```
[Approval required] exec: node --version
Allow? (y/n)
```

This is configurable via `tools.exec.security` in the config. For this walkthrough, approve the requests to see the tools in action.

---

## Part 7: Connect Telegram (Optional)

### What We'll Do

Connect your AI assistant to Telegram so you can chat with it from your phone. Telegram is the easiest channel to set up — it only requires a bot token.

### 7.1 Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send the command `/newbot`
3. Follow the prompts:
   - Enter a **name** for your bot (e.g., "My OpenClaw Assistant")
   - Enter a **username** for your bot (must end with `bot`, e.g., `my_openclaw_bot`)
4. BotFather will give you a **bot token** — a long string like `123456789:ABCdefGhIjKlMnOpQrStUvWxYz`. Copy it.

### 7.2 Configure the Channel

Add the Telegram channel configuration. Open or edit your OpenClaw config:

```bash
openclaw config edit
```

Add the Telegram section:

```yaml
channels:
  telegram:
    token: "YOUR_BOT_TOKEN_HERE"
```

Replace `YOUR_BOT_TOKEN_HERE` with the actual token from BotFather.

### 7.3 Restart the Gateway

```bash
openclaw gateway restart
```

### 7.4 Test It

1. Open Telegram on your phone or desktop
2. Search for your bot by its username
3. Send a message: `Hi! Are you working?`
4. You should get an AI response within a few seconds

### What Just Happened

Telegram messages now flow through your local Gateway to the AI model and back. The conversation happens on your infrastructure — messages are processed locally, and only API calls go to the model provider. The AI has access to the same tools (exec, browser, web_search) regardless of which channel you use.

---

## Part 8: Understand Skills and Plugins

### Skills

Skills are markdown files (`SKILL.md`) that get injected into the AI's system prompt. They teach the AI **when and how** to use tools effectively. Skills can:

- Live in your workspace (project-specific knowledge)
- Ship inside plugins (packaged by the community)
- Be shared across teams

This is conceptually similar to custom instruction files in VS Code or Cursor — but applied to the OpenClaw assistant.

### Plugins

Plugins extend OpenClaw with additional capabilities:

- **Channels** — LINE, Matrix, Mattermost, Microsoft Teams, Twitch, Voice Call, etc.
- **Model providers** — Additional LLM backends
- **Tools** — Lobster (workflow runtime), OpenProse (markdown orchestration), Diffs (diff viewer), etc.
- **Speech & Image** — Text-to-speech, speech-to-text, image generation

Plugins are installed via npm and configured in your config file.

### Tool Configuration

You can control which tools the AI can use via allow/deny lists in the config:

```yaml
tools:
  allow:
    - "group:fs"
    - "browser"
    - "web_search"
  deny:
    - "exec"
```

This is useful for restricting the AI's capabilities in shared or production environments.

---

## Part 9: Clean Up

### Stop the Gateway

If you want to stop OpenClaw after experimenting:

```bash
openclaw gateway stop
```

### Where Data Lives

All OpenClaw data is stored locally in `~/.openclaw/`:
- `config.yaml` — your configuration
- `state/` — conversation history and session data
- `exec-approvals.json` — approved commands

To completely remove OpenClaw, delete this directory and uninstall:

```bash
npm uninstall -g openclaw
rm -rf ~/.openclaw
```

On Windows (PowerShell):

```powershell
npm uninstall -g openclaw
Remove-Item -Recurse -Force "$env:USERPROFILE\.openclaw"
```

---

## Success Criteria

After completing this walkthrough, verify:

- ✅ OpenClaw CLI is installed and `openclaw --version` works
- ✅ Onboarding completed with your API key configured
- ✅ Gateway is running on port 18789
- ✅ Dashboard opens and you can chat with the AI
- ✅ You successfully used at least 2 built-in tools (exec, web_search, read/write, or browser)
- ✅ (Optional) Telegram bot is connected and responds to messages
- ✅ You understand the difference between tools, skills, and plugins

---

## Understanding Check

Test your knowledge of OpenClaw concepts:

1. **What is the Gateway and what role does it play in the OpenClaw architecture?**
   - The Gateway is a local HTTP server that routes messages between channels (dashboard, Telegram, etc.) and the AI model. It manages context, executes tools, and enforces security controls.

2. **How does OpenClaw differ from IDE-based AI assistants like GitHub Copilot or Cursor?**
   - OpenClaw runs as a standalone service accessible from any device/app (phone, browser, chat apps), not just inside an IDE. It's designed as a general-purpose AI assistant, not specifically for coding.

3. **What are the three layers of OpenClaw's capability system?**
   - Tools (typed functions the AI calls), Skills (markdown instructions injected into the system prompt), and Plugins (packages that bundle channels, tools, skills, and other capabilities).

4. **Why does OpenClaw ask for approval before running certain tools?**
   - Security. Tools like `exec` can run arbitrary shell commands on your machine. The approval flow prevents the AI from executing potentially dangerous operations without your consent.

5. **What happens when you send a message via Telegram to your OpenClaw bot?**
   - Telegram forwards the message to the bot → the Gateway receives it via the Telegram Bot API → routes it to the configured model provider → receives the AI response → sends it back through Telegram. All processing happens on your local Gateway.

6. **Where is the OpenClaw configuration stored and what does it contain?**
   - In `~/.openclaw/config.yaml`. It contains model provider settings (API keys, model selection), channel configurations (Telegram token, WhatsApp settings), tool permissions (allow/deny lists), and Gateway settings.

7. **Name at least 4 built-in tools that OpenClaw provides out of the box.**
   - exec (run commands), browser (control Chromium), web_search/web_fetch (search/read web), read/write/edit (file I/O), message (send messages), canvas (drive node Canvas), image/image_generate (analyze/generate images).

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `openclaw: command not found` | Close and reopen your terminal to refresh PATH. If using npm install, make sure global npm bin is in PATH. |
| Gateway won't start | Check if port 18789 is already in use: `netstat -an | grep 18789` (Linux/macOS) or `netstat -an | findstr 18789` (Windows). Kill the blocking process or change the port in config. |
| "Invalid API key" error | Verify your API key in `~/.openclaw/config.yaml`. Re-run `openclaw onboard` to reconfigure. |
| Dashboard opens but no AI response | Check Gateway status with `openclaw gateway status`. Verify your model provider API key is valid and has credits. |
| Telegram bot doesn't respond | Verify the bot token in config. Make sure you restarted the Gateway after adding the Telegram config. Check that you're messaging the correct bot username. |
| Tool execution blocked | OpenClaw asks for approval by default. Type `y` when prompted. Or configure `tools.exec.security: full` for unrestricted access (not recommended for production). |
| Node.js version too old | Update to Node 22.14+ or Node 24. Use `nvm install 24` if you have nvm installed. |

---

## Next Steps

After getting comfortable with OpenClaw basics, explore these directions:

- **Connect WhatsApp** — Pair via QR code for the most popular messaging platform (`openclaw` WhatsApp setup requires local session storage)
- **Create custom Skills** — Write `SKILL.md` files to teach the AI about your workflows
- **Install plugins** — Browse community plugins for additional channels and tools
- **Configure security** — Set up tool profiles, allow/deny lists, and sandboxing for production use
- **Explore sub-agents** — Use `agents_list` and `sessions_*` tools to create specialized sub-agents for different tasks
