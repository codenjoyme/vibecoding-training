---
external_workspace: true
---

# Installing mcpyrex — MCP Python Toolbox - Hands-on Walkthrough

In this module you will clone the mcpyrex-python repository, run the interactive installer, verify the MCP connection with GitHub Copilot, and execute your first deterministic tool from both terminal and chat.

This module runs in a **separate workspace** (`work/400-mcpyrex/`) to avoid conflicts between the course instructions and mcpyrex's own AI configuration files.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Install

mcpyrex is an MCP server built with Python and Langchain. The installation creates:

- **Python 3.11+ environment** — either uses your existing Python or downloads an embedded version (~30 MB)
- **Virtual environment** (`.virtualenv/`) — isolated Python with all dependencies (~200 MB)
- **MCP server** (`mcp_server/`) — the server code with 30+ tools
- **IDE configuration** (`.vscode/mcp.json`) — connects GitHub Copilot to the MCP server
- **Workspace settings** (`.vscode/settings.json`) — enables MCP and Agent Mode

The full installation takes 5-10 minutes depending on your internet connection.

---

## Part 1: Clone the Repository

### What We'll Do

Clone the mcpyrex-python project into a dedicated practice folder. This gives you:
- The full MCP server source code with 30+ tools
- 8 ready-made projects (Telegram bots, telemetry analysis, RAG pipelines, etc.)
- The build scripts for all platforms (Windows, macOS, Linux)

### If You Already Have It

If you have already cloned mcpyrex into `work/400-mcpyrex/` from a previous session:

```bash
cd work/400-mcpyrex
git pull
```

If the pull succeeds — **skip to Part 3**.

### Clone

From the course workspace root, run:

**Windows (PowerShell):**

```powershell
git clone https://github.com/codenjoyme/mcpyrex-python.git work/400-mcpyrex
```

**macOS / Linux:**

```bash
git clone https://github.com/codenjoyme/mcpyrex-python.git work/400-mcpyrex
```

This creates `work/400-mcpyrex/` with the full mcpyrex project inside.

### What Just Happened

You now have a local copy of the mcpyrex ecosystem. The key directories are:

| Directory | What's inside |
|-----------|--------------|
| `tools/` | 28 tool groups — each is a separate MCP tool |
| `projects/` | 8 real-world projects (Telegram bots, telemetry, RAG, etc.) |
| `build/` | Installation scripts for all platforms |
| `simple/` | Standalone Python examples (RAG, agents, chains) |
| `pipeline/` | Batch pipeline configurations |

---

## Part 2: Open the Workspace in VS Code

### What We'll Do

Open the cloned project as a **separate VS Code window**. This is critical — mcpyrex has its own `.vscode/` configuration that would conflict with the course workspace.

1. Open VS Code
2. Go to **File > Open Folder**
3. Navigate to `work/400-mcpyrex/` inside your course directory:
   - Windows: `c:/Java/CopipotTraining/vibecoding-for-managers/work/400-mcpyrex/` (adjust to your path)
   - macOS/Linux: `~/workspace/vibecoding-for-managers/work/400-mcpyrex/`
4. Click **Open**

You should see the mcpyrex project structure in the Explorer panel: `build/`, `tools/`, `projects/`, `server.py`, etc.

> **Important**: All subsequent commands in this walkthrough should be run in this new VS Code window, not in the course workspace.

---

## Part 3: Run the Installer

### What We'll Do

Run the interactive installation script. It will:
- Detect or download Python 3.11+
- Create a virtual environment with all dependencies
- Ask you to choose between Cursor and VS Code
- Copy configuration files (mcp.json, settings.json, instructions)
- Install all pip dependencies for the MCP tools

### Security Note

Before proceeding, review the security disclaimer:

```bash
cat mcp_server/security-disclaimer.md
```

The key points: mcpyrex communicates with LLMs (GitHub Copilot and optionally a Langchain LLM), uses Python libraries, and generates code. Each tool has a `settings.yaml` where you can disable it if needed.

### Run the Script

Open a terminal in VS Code (Terminal > New Terminal).

**Windows (PowerShell):**

```powershell
cd mcp_server/build
.\install-windows.ps1
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
./install-macos.sh
```

**Linux:**

```bash
cd mcp_server/build
chmod +x ./install-linux.sh
./install-linux.sh
```

### Interactive Prompts

The installer will ask you several questions:

1. **"Do you want to install VSCode portable?"** — Answer `n` (you already have VS Code installed)
2. **"Choose your IDE configuration: (c)ursor or (v)scode?"** — Answer `v` for VS Code with GitHub Copilot
3. **File replacement prompts** — The installer will show you each config file it wants to create and ask for confirmation. Answer `y` to accept each one

### What Just Happened

The installer created:

| File/Directory | Purpose |
|---------------|---------|
| `.virtualenv/` | Python virtual environment with all dependencies |
| `.vscode/mcp.json` | MCP server configuration — tells Copilot how to start the Python server |
| `.vscode/settings.json` | Workspace settings — enables MCP and Agent Mode |
| `.github/copilot-instructions.md` | Copilot instructions for the mcpyrex workspace |
| `.env` | Environment variables template (API keys go here) |

---

## Part 4: Verify the MCP Connection

### What We'll Do

Confirm that GitHub Copilot can see and communicate with the mcpyrex MCP server.

1. **Restart VS Code** — Close and reopen the `work/400-mcpyrex/` workspace to pick up the new configuration

2. **Check MCP status** — In VS Code, open the Command Palette (View > Command Palette) and search for `MCP: List Servers`. You should see `mcpyrex-python` in the list

3. **Check the MCP indicator** — In the Copilot chat panel, you should see the MCP tools icon indicating available tools. Click it to see the list of registered tools

### What to Look For

You should see tools like:
- `lng_count_words` — word counting with statistics
- `lng_math_calculator` — math expression evaluation
- `lng_get_tools_info` — tool catalog
- `lng_file_read`, `lng_file_write` — file operations
- And many more (30+ tools total)

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

---

## Part 7: Explore the Tool Catalog

### What We'll Do

Use the built-in `lng_get_tools_info` tool to explore everything mcpyrex offers.

1. In Copilot chat, ask:

> Show me all available mcpyrex tools and their descriptions

Copilot should call `lng_get_tools_info` and return a structured list of all tools, grouped by category.

2. Browse the tools directory in the file explorer. Each tool lives in `tools/[tool_name]/`:
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

### The Project Ecosystem

Beyond individual tools, mcpyrex includes 8 ready-made projects in `projects/`:

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

---

## Success Criteria

- ✅ mcpyrex repository cloned into `work/400-mcpyrex/`
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
