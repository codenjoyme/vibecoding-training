---
external_workspace: true
---

# Installing mcpyrex — MCP Python Toolbox - Hands-on Walkthrough

In this module you will clone the mcpyrex-python repository, run the interactive installer, verify the MCP connection with GitHub Copilot, and execute your first deterministic tool from both terminal and chat.

This module runs in a **separate workspace** (`work/400-task/`) to avoid conflicts between the course instructions and mcpyrex's own AI configuration files.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Install

mcpyrex is an MCP server built with Python and Langchain. The installation flow:

1. **Clone the repository** into `mcp_server/` subfolder inside the workspace
2. **Run the installer** from `mcp_server/build/` — it creates files in the workspace root:
   - **Virtual environment** (`.virtualenv/`) — isolated Python with all dependencies (~200 MB)
   - **IDE configuration** (`.vscode/mcp.json`) — connects GitHub Copilot to the MCP server
   - **Workspace settings** (`.vscode/settings.json`) — enables MCP and Agent Mode
   - **Environment file** (`.env`) — API keys template

The resulting workspace structure:

```
work/400-task/              ← workspace root (open this in VS Code)
  mcp_server/               ← cloned repository (.git/ here)
    build/                  ← installer scripts
    tools/                  ← 28 tool groups
    projects/               ← 8 real-world projects
  .virtualenv/              ← created by installer at workspace root
  .vscode/                  ← created by installer at workspace root
  .env                      ← created by installer at workspace root
```

The full installation takes 5-10 minutes depending on your internet connection.

---

## Part 1: Clone the Repository

### What We'll Do

Clone the mcpyrex-python project into a dedicated practice folder. This gives you:
- The full MCP server source code with 30+ tools
- 8 ready-made projects (Telegram bots, telemetry analysis, RAG pipelines, etc.)
- The build scripts for all platforms (Windows, macOS, Linux)

### If You Already Have It

If you have already cloned mcpyrex into `work/400-task/mcp_server/` from a previous session:

```bash
cd work/400-task/mcp_server
git pull
```

If the pull succeeds — **skip to Part 3**.

### Create the Workspace Folder and Clone

From the course workspace root, run:

**Windows (PowerShell):**

```powershell
mkdir work/400-task -Force
cd work/400-task
git clone https://github.com/codenjoyme/mcpyrex-python.git mcp_server
```

**macOS / Linux:**

```bash
mkdir -p work/400-task
cd work/400-task
git clone https://github.com/codenjoyme/mcpyrex-python.git mcp_server
```

This creates `work/400-task/mcp_server/` with the full mcpyrex project inside. The `work/400-task/` folder is your workspace root — this is where you'll open VS Code.

### What Just Happened

You now have a local copy of the mcpyrex ecosystem inside `mcp_server/`. The key directories are:

| Directory | What's inside |
|-----------|--------------|
| `mcp_server/tools/` | 28 tool groups — each is a separate MCP tool |
| `mcp_server/projects/` | 8 real-world projects (Telegram bots, telemetry, RAG, etc.) |
| `mcp_server/build/` | Installation scripts for all platforms |
| `mcp_server/simple/` | Standalone Python examples (RAG, agents, chains) |
| `mcp_server/pipeline/` | Batch pipeline configurations |
### Why This Architecture?

Notice what mcpyrex is **not**: it's not a plugin, not a VS Code extension, not an API wrapper. It's a standalone Python process that speaks the MCP protocol. This means:

- It works with **any** MCP-compatible IDE (VS Code, Cursor, Claude Desktop...)
- The tool logic lives in plain Python — no framework lock-in
- Each tool folder (`tools/lng_count_words/`) is self-contained: code, config, and tests in one place

This is the "factory" design: new tools follow the same pattern, and the server discovers them automatically by scanning the `tools/` folder.

> 💬 **Discussion for agent:** Ask the user — in module 100 they hand-crafted an MCP server from scratch with echo/calculate/get_time. Now they're looking at a project with 28+ tools organized into folders. What design decisions would they need to make to scale their own server from 3 tools to 30? What changes, what stays the same? Explore their thinking — don't just confirm, dig into how they'd structure it.
---

## Part 2: Open the Workspace in VS Code

### What We'll Do

Open the workspace as a **separate VS Code window**. This is critical — the installer creates `.vscode/` configuration that would conflict with the course workspace.

1. Open VS Code
2. Go to **File > Open Folder**
3. Navigate to `work/400-task/` inside your course directory:
   - Windows: `c:/Java/CopipotTraining/vibecoding-for-managers/work/400-task/` (adjust to your path)
   - macOS/Linux: `~/workspace/vibecoding-for-managers/work/400-task/`
4. Click **Open**

You should see `mcp_server/` folder in the Explorer panel. Inside it: `build/`, `tools/`, `projects/`, etc.

> **Important**: All subsequent commands in this walkthrough should be run in this new VS Code window, not in the course workspace.

### Why a Separate Workspace?

This is not just a convenience — it's an architectural constraint. mcpyrex has its own `.github/copilot-instructions.md` that defines how Copilot should behave when working with MCP tools. If you opened `mcp_server/` inside the course workspace, you'd have two sets of conflicting Copilot instructions fighting each other.

More broadly: this pattern — where a project has its **own AI personality** — is increasingly common. A customer support bot project instructs the AI to be formal. A creative writing tool instructs it to be expressive. A security-focused repo instructs it to flag risky patterns. Each workspace creates a different AI context.

> 💬 **Discussion for agent:** Ask the user to think about their own team's repositories. If you were setting up a workspace for a project, what AI instructions would you want baked in? What behaviors should the AI default to in YOUR codebase context? Use this to connect the abstract idea of workspace isolation to something concrete from their work.

---

## Part 3: Run the Installer

### What We'll Do

Run the installation script in **silent mode**. It will:
- Detect or download Python 3.11+
- Create a virtual environment with all dependencies
- Configure IDE settings automatically (no interactive prompts)
- Copy configuration files (mcp.json, settings.json, instructions)
- Install all pip dependencies for the MCP tools

### Before You Run: Read the Install Scripts

> **Agent instruction:** Before running the installer, read ALL three installation scripts in `mcp_server/build/` to understand the available modes and parameters:
> - `install-windows.ps1` — Windows (PowerShell)
> - `install-macos.sh` — macOS (Bash)
> - `install-linux.sh` — Linux (Bash)
>
> Each script supports silent mode with various flags. Choose the correct script for the user's OS and determine the IDE choice (cursor or vscode) from the user's training session context (check `.training/progress-notes.md` or ask the user).

### Security Note

Before proceeding, review the security disclaimer (from the workspace root `work/400-task/`):

```bash
cat mcp_server/mcp_server/security-disclaimer.md
```

The key points: mcpyrex communicates with LLMs (GitHub Copilot and optionally a Langchain LLM), uses Python libraries, and generates code. Each tool has a `settings.yaml` where you can disable it if needed.

### Run the Script (Silent Mode)

Open a terminal in VS Code (Terminal > New Terminal). Run the installer in **silent mode** — no interactive prompts needed.

**Windows (PowerShell):**

```powershell
cd mcp_server/build
.\install-windows.ps1 -Silent -InstallVSCode n -IDE vscode -OverwriteConfig -NoLaunch
```

> **Execution Policy error?** If you see "running scripts is disabled on this system", run this first:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Then retry the install script.

**macOS:**

```bash
cd mcp_server/build
chmod +x ./install-macos.sh
./install-macos.sh --silent --install-vscode n --ide vscode --overwrite-config --no-launch
```

**Linux:**

```bash
cd mcp_server/build
chmod +x ./install-linux.sh
./install-linux.sh --silent --install-vscode n --ide vscode --overwrite-config --no-launch
```

> **Note:** The `--ide` flag should match the user's IDE: use `vscode` for VS Code with GitHub Copilot, or `cursor` for Cursor. The `-NoLaunch` / `--no-launch` flag prevents the script from opening a new VS Code window since we already have one open.

### What Just Happened

The installer created:

| File/Directory | Purpose |
|---------------|---------|
| `.virtualenv/` | Python virtual environment with all dependencies |
| `.vscode/mcp.json` | MCP server configuration — tells Copilot how to start the Python server |
| `.vscode/settings.json` | Workspace settings — enables MCP and Agent Mode |
| `.github/copilot-instructions.md` | Copilot instructions for the mcpyrex workspace |
| `.env` | Environment variables template (API keys go here) |

### The Key File: mcp.json

Open `.vscode/mcp.json` and look at what's inside. You'll see something like:

```json
{
  "servers": {
    "mcpyrex-python": {
      "type": "stdio",
      "command": ".virtualenv/Scripts/python.exe",
      "args": ["server.py"]
    }
  }
}
```

This is the **discovery contract**: VS Code reads this file and knows how to start the MCP server. The `stdio` type means communication happens over standard input/output — the simplest possible IPC. VS Code launches Python, Python starts the server, and they talk through stdin/stdout.

This is also why the virtualenv matters: `command` points to `.virtualenv/Scripts/python.exe` — not your system Python. If you have Python 3.9 globally but mcpyrex needs 3.11+, the virtualenv solves this silently.

> 💬 **Discussion for agent:** After showing the user what's in `.vscode/mcp.json`, ask them: the config uses a relative path to python.exe — what would break if you moved the `400-task/` folder to a different location on disk? How would you fix it? This is a real portability question — connect it to their experience of "it works on my machine" problems in team environments.

### Security: What Did You Just Install?

Before moving on, open `mcp_server/security-disclaimer.md`. Read it — it's short. The mcpyrex design acknowledges that you're installing a system that:
- Executes arbitrary Python code
- Communicates with an LLM (Copilot)
- Can read and write files on your system
- Can make HTTP requests

The mitigation is `settings.yaml` per tool — you control what's active. This is a governance model: default on, opt-out per tool.

> 💬 **Discussion for agent:** Ask the user — if they were deploying this in a corporate environment where security matters, which tools would they disable by default and why? For example: `lng_terminal` runs shell commands, `lng_file_write` writes files, `lng_http_client` makes external network requests. How would the risk profile change depending on whether this runs on a developer's laptop vs. a shared team environment?

---

## Part 4: Verify the MCP Connection

### What We'll Do

Confirm that GitHub Copilot can see and communicate with the mcpyrex MCP server.

1. **Restart VS Code** — Close and reopen the `work/400-task/` workspace (not `mcp_server/`!) to pick up the new configuration

2. **Check MCP status** — In VS Code, open the Command Palette (View > Command Palette) and search for `MCP: List Servers`. You should see `mcpyrex-python` in the list

3. **Check the MCP indicator** — In the Copilot chat panel, you should see the MCP tools icon indicating available tools. Click it to see the list of registered tools

### What to Look For

You should see tools like:
- `lng_count_words` — word counting with statistics
- `lng_math_calculator` — math expression evaluation
- `lng_get_tools_info` — tool catalog
- `lng_file_read`, `lng_file_write` — file operations
- And many more (30+ tools total)

### How Does Copilot "Know" About Tools?

This is worth understanding at a deeper level. When VS Code starts the MCP server, it sends a `tools/list` request over stdio. The server responds with all tool schemas — name, description, parameter names and types. Copilot stores these schemas in its context.

When you ask "count the words in this text", Copilot doesn't search for a function — it matches your intent against the tool descriptions it received. The description `"Count words, unique words, characters in text"` is what triggers `lng_count_words`. Change the description, and routing changes too.

This is why tool descriptions are critical — they're the routing layer between natural language and code.

> 💬 **Discussion for agent:** Ask the user — knowing that Copilot routes based on tool descriptions, what makes a good vs. bad tool description? If you were writing `lng_count_words` from scratch, what description would you write? What words would you include to make it easier for the LLM to choose it correctly? This connects to a real skill: writing tools that get used.

### If MCP Is Not Connected

1. Check that `.vscode/mcp.json` exists and contains the server configuration
2. Verify the virtual environment exists: `.virtualenv/Scripts/python.exe` (Windows) or `.virtualenv/bin/python` (macOS/Linux)
3. Try restarting the MCP server: Command Palette > `MCP: Restart Server` > select `mcpyrex-python`
4. Check the Output panel (View > Output > select "MCP") for error messages

---

## Part 5: Run a Tool from Terminal

### What We'll Do

Test the MCP tools directly from the terminal — without going through Copilot. This is useful for debugging and quick testing.

1. Activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\.virtualenv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .virtualenv/bin/activate
```

2. List all available tools:

```bash
python -m mcp_server.run list
```

You should see a list of 30+ tools with their names.

3. Check a tool's schema:

```bash
python -m mcp_server.run schema lng_count_words
```

This shows the input parameters the tool expects.

4. Run a tool:

```bash
python -m mcp_server.run run lng_count_words "{\"input_text\":\"Hello world from mcpyrex\"}"
```

You should see output like:
```
Word count: 4
Unique words: 4
Character count: 24
Average word length: 5.0
```

5. Try the math calculator:

```bash
python -m mcp_server.run run lng_math_calculator "{\"expression\":\"2 + 3 * 4\"}"
```

Expected result: `14`

### What Just Happened

You executed MCP tools directly — bypassing the LLM entirely. This confirms:
- The Python environment is correctly set up
- The tools load and execute properly
- The input/output schema works as documented

### Why Run Tools Without the LLM?

This terminal pattern has three real use cases:

1. **Debugging**: If a tool misbehaves in chat, run it from terminal to isolate whether the problem is the tool itself or the LLM's routing/parameter construction
2. **Automation**: Shell scripts can call tools directly without spinning up an IDE. Zero tokens, zero cost.
3. **Development**: When you create a new tool, you test it from terminal first before exposing it through MCP

This is the same principle as in module 103 (CLI): the terminal path is cheaper, faster, and deterministic. The LLM adds value when you need natural language routing — not when you already know exactly what to call.

> 💬 **Discussion for agent:** Ask the user to think about their actual workflow. What kind of operations do they currently do manually or with scripts that involve text processing, math, or file manipulation? For each one: would a deterministic tool be better than asking an LLM, or would LLM judgment add value? Push them to identify a concrete personal use case for terminal-mode tool execution.

---

## Part 6: Run a Tool from Copilot Chat

### What We'll Do

Now test the same tools through GitHub Copilot. This is the real use case — the AI decides when and how to call tools.

1. Open a new Copilot chat (make sure **Agent Mode** is enabled — look for the agent icon in the chat panel)

2. Ask Copilot:

> Count the words in this text: "The quick brown fox jumps over the lazy dog"

Copilot should call `lng_count_words` and return precise statistics (9 words, 8 unique words, etc.).

3. Try a math problem:

> Calculate: (15 + 7) * 3 - 12 / 4

Copilot should call `lng_math_calculator` and return the exact result (`63.0`).

4. Compare with a non-tool response — open a **new chat without MCP** and ask the same word count question. Notice how the LLM might give an approximate or incorrect count, while the tool gives an exact answer.

### Why This Matters

LLMs are notoriously bad at precise text operations:
- Word counting: LLMs often miscount by 1-2 words
- Math: LLMs make arithmetic errors on complex expressions
- Character counting: LLMs struggle with exact character positions

Deterministic tools eliminate these errors entirely. The LLM's job becomes routing — deciding which tool to call — not computing.

### The Architecture Insight

Look at what just happened from a system architecture perspective:

```
Your natural language → Copilot (understands intent) → lng_count_words (executes exactly) → Copilot (formats result)
```

This is a hybrid: LLM for understanding and presentation, Python for computation. Each part does what it's good at. This pattern — LLM as orchestrator, deterministic code as executor — is the core of reliable AI-augmented systems.

The alternative (pure LLM computing) is like asking a philosopher to add up your restaurant bill. They might get it right, they might not, and you can't be sure which.

> 💬 **Discussion for agent:** This is a good moment for a real story — ask the user if they've had a situation where an LLM gave them a confidently wrong answer on something that should be exact (a calculation, a count, a date). What happened? How did they catch it? Connect their experience to the value of this hybrid pattern. Then: in their work, what types of tasks would benefit most from this approach?

---

## Part 7: Explore the Tool Catalog

### What We'll Do

Use the built-in `lng_get_tools_info` tool to explore everything mcpyrex offers.

1. In Copilot chat, ask:

> Show me all available mcpyrex tools and their descriptions

Copilot should call `lng_get_tools_info` and return a structured list of all tools, grouped by category.

2. Browse the tools directory in the file explorer. Each tool lives in `mcp_server/tools/[tool_name]/`:
   - `tool.py` — the Python implementation
   - `settings.yaml` — configuration (enabled/disabled, dependencies)
   - `case/` — demo scenarios (if available)

3. Check which tools have demo walkthroughs:

| Tool | Demo file |
|------|-----------|
| `lng_cookie_grabber` | `case/make-secure-rest-api-call-with-cookies-grabbing.demo.agent.md` |
| `lng_jira` | `case/jira-pdf-processing.demo.agent.md` |
| `lng_webhook_server` | `case/calculator-html-page.demo.agent.md`, `case/simple-calculator-api.demo.agent.md` |
| `lng_winapi` | `case/auto-translate-text-from-clipboard.demo.agent.md`, `case/working-with-chrome.demo.agent.md`, `case/working-with-teams.demo.agent.md` |
| `lng_llm/rag` | `case/llm-rag.demo.agent.md` |

These demos are the basis for upcoming training modules (405-550).

> 💬 **Discussion for agent:** Look at the tool list with the user and ask them to pick 2-3 tools that seem most relevant to their actual work. For each one: what problem would it solve? What would they use it for specifically? This is not a hypothetical exercise — push them to think concretely. A manager might say "I spend a lot of time summarizing reports" → `lng_file_read` + `lng_llm_chat`. A developer might say "I need to count tokens before sending to API" → `lng_count_words` as a proxy. Make the catalog personally relevant, not just a list.

### The Project Ecosystem

Beyond individual tools, mcpyrex includes 8 ready-made projects in `mcp_server/projects/`:

| Project | What it does |
|---------|-------------|
| `copilot-cli` | Ask AI from terminal without IDE |
| `css-selector-finder` | Interactive CSS selector extraction |
| `docs-rag` | Automated document processing into RAG |
| `instruction-processor` | Batch improvement of instruction files |
| `super-empath` | Telegram bot for empathetic messaging |
| `telemetry` | GitHub Copilot usage analysis |
| `telescope-avatar-grabber` | API automation with encrypted cookies |
| `web-mcp` | Browser-based MCP tool interface |

These projects show the **end state**: what you can build when individual MCP tools are composed together. `telemetry` tracks your own Copilot usage to optimize costs (connects to module 083). `docs-rag` turns a folder of documents into a searchable knowledge base — a common enterprise use case.

> 💬 **Discussion for agent:** Pick one project from the table above that seems most relevant to the user's context (based on what you know about their work from earlier in the session). Walk through what that project actually does at a conceptual level. Then ask: if you were going to build something like this for your team, what documents or data would you feed into it? What questions would you want to answer? This turns a catalog item into a concrete vision.

---

## Success Criteria

- ✅ mcpyrex repository cloned into `work/400-task/mcp_server/`
- ✅ Installation script completed without errors
- ✅ `.vscode/mcp.json` configured with `mcpyrex-python` server
- ✅ MCP server visible in VS Code (MCP: List Servers)
- ✅ `python -m mcp_server.run list` shows 30+ tools
- ✅ `lng_count_words` works from terminal
- ✅ `lng_count_words` works from Copilot chat
- ✅ `lng_math_calculator` returns correct results
- ✅ `lng_get_tools_info` returns the full tool catalog

---

## Understanding Check

1. **What problem does mcpyrex solve?**
   > LLMs hallucinate on precise operations (counting, math, file processing). mcpyrex provides deterministic Python tools that execute exact logic, while the LLM handles routing and natural language understanding.

2. **What is the role of `.vscode/mcp.json`?**
   > It tells VS Code how to start the MCP server — the Python executable path and the server script. Without it, Copilot cannot discover or call mcpyrex tools.

3. **How does Copilot decide to call a tool vs. answering directly?**
   > Copilot sees the tool schemas (name, description, parameters) and decides based on the user's request. If a request matches a tool's capability (e.g., "count words" matches `lng_count_words`), it calls the tool. Otherwise it answers from its own knowledge.

4. **What is the difference between running a tool from terminal vs. from chat?**
   > Terminal (`python -m mcp_server.run`) bypasses the LLM entirely — you specify the tool and parameters directly. From chat, the LLM interprets your request, selects the appropriate tool, constructs the parameters, and formats the result in natural language.

5. **Where are the security risks in this setup?**
   > Four potential data leak points: (1) the primary LLM (Copilot), (2) the Langchain LLM used by `lng_llm_*` tools, (3) Python libraries imported by tools, (4) code generated by the agent. Each tool can be disabled in its `settings.yaml`.

6. **How do you disable a tool you don't need?**
   > Open the tool's `settings.yaml` file (e.g., `tools/lng_email_client/settings.yaml`) and set `enabled: false`. Restart the MCP server.

7. **What is the `projects/` directory for?**
   > It contains 8 complete real-world projects that combine multiple tools into working applications (Telegram bots, telemetry dashboards, RAG pipelines, etc.).

---

## Troubleshooting

### "install-windows.ps1 cannot be loaded because running scripts is disabled"

Run before the installer:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Python version too old

The installer needs Python 3.11+. If your system Python is older, the installer will download an embedded Python automatically (Windows only). On macOS/Linux, install Python 3.11+ via `brew install python@3.13` or your package manager.

### "Module mcp_server not found" when running tools

Make sure you activated the virtual environment first:
- Windows: `.\.virtualenv\Scripts\Activate.ps1`
- macOS/Linux: `source .virtualenv/bin/activate`

### MCP server not showing in VS Code

1. Check `.vscode/mcp.json` exists and has the correct path to Python
2. The path should point to `.virtualenv/Scripts/python.exe` (Windows) or `.virtualenv/bin/python` (macOS/Linux)
3. Restart VS Code completely (close all windows, reopen)
4. Check Output panel > MCP for error messages

### Tools work in terminal but not from Copilot

1. Verify that `chat.mcp.enabled` is `true` in `.vscode/settings.json`
2. Make sure you're using **Agent Mode** in the chat panel (not just regular chat)
3. Restart the MCP server: Command Palette > `MCP: Restart Server`

### pip install fails with SSL errors

Your network might block PyPI. Try:
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## Next Steps

With mcpyrex installed and verified, you're ready to explore individual tools in depth. The next module — **405: Word Count & Math — First Custom Tools** — dives into the anatomy of an MCP tool and teaches you to read, understand, and modify tool source code.

The full mcpyrex training series (400-550) covers all 30+ tools and 8 projects. See `modules/proposed-mcpyrex-modules.md` for the complete roadmap.
