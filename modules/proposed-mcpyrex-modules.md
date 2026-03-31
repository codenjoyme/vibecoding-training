# Proposed mcpyrex Modules — Elevator Pitches & Training Plans

> This document proposes training modules based on the [mcpyrex-python](https://github.com/codenjoyme/mcpyrex-python) ecosystem.  
> mcpyrex extends GitHub Copilot with Python, Langchain, and MCP — giving the agent deterministic tools, pipelines, and real-world integrations.  
> Each module includes: elevator pitch, training plan outline, what the student gets, proposed placement, and motivation.  
> **All modules run in an external workspace** (`work/400-mcpyrex/`) to avoid conflicts with the course instructions.

---

## Numbering Map (mcpyrex series)

```
400  Installing mcpyrex — MCP Python Toolbox           ← installation & orientation
405  mcpyrex: Word Count & Math — First Custom Tools    ← tools: lng_count_words, lng_math_calculator
410  mcpyrex: LLM Chains & Prompt Templates             ← tools: lng_llm (chain, prompt_template)
415  mcpyrex: RAG with Vector Search                    ← tools: lng_llm/rag + project docs-rag
420  mcpyrex: Structured Output & Chain of Thought      ← tools: lng_llm (structured_output, chain_of_thought)
425  mcpyrex: LLM Agent Demo                            ← tools: lng_llm/agent_demo
430  mcpyrex: Batch Pipelines                           ← tools: lng_batch_run
435  mcpyrex: File Operations                           ← tools: lng_file
440  mcpyrex: Terminal Execution                        ← tools: lng_terminal, lng_terminal_chat
445  mcpyrex: HTTP Client & REST APIs                   ← tools: lng_http_client
450  mcpyrex: Webhook Server — Calculator API           ← tools: lng_webhook_server (2 demos)
455  mcpyrex: Browser Automation                        ← tools: lng_browser_automation
460  mcpyrex: JSON/CSV & Excel Batch Processing         ← tools: lng_json_to_csv, lng_xls_batch
465  mcpyrex: Cookie Grabber & Secure API Calls         ← tools: lng_cookie_grabber (1 demo)
470  mcpyrex: Jira Integration & PDF Processing         ← tools: lng_jira (1 demo)
475  mcpyrex: JavaScript Execution Engine               ← tools: lng_javascript
480  mcpyrex: PowerPoint Notes Extraction               ← tools: lng_pptx
485  mcpyrex: Screenshot & Speech Tools                 ← tools: lng_save_screenshot, lng_speech
490  mcpyrex: Email Client                              ← tools: lng_email_client
495  mcpyrex: Telegram Bot — Super Empath               ← tools: lng_telegram + project super-empath
500  mcpyrex: Windows Automation (WinAPI)               ← tools: lng_winapi (3 demos)
505  mcpyrex: WebSocket & Agent Pairing                 ← tools: lng_websocket_server, lng_agents_pairing
510  mcpyrex: Multi-Agent Orchestration                 ← tools: lng_multi_agent
515  mcpyrex: Docker Terminal                           ← tools: lng_terminal_docker
520  mcpyrex: Copilot Telemetry Analysis                ← project telemetry
525  mcpyrex: CSS Selector Finder                       ← project css-selector-finder
530  mcpyrex: Instruction Processor                     ← project instruction-processor
535  mcpyrex: Copilot CLI — Terminal AI                  ← project copilot-cli
540  mcpyrex: Web MCP — Browser Interface               ← project web-mcp
545  mcpyrex: Telescope Avatar Grabber                  ← project telescope-avatar-grabber
550  mcpyrex: Tools Info & Discovery                    ← tools: lng_get_tools_info, lng_copilot
```

---

## ✅ Module 400: Installing mcpyrex — MCP Python Toolbox

**Proposed ID:** `400`  
**Proposed Name:** Installing mcpyrex — MCP Python Toolbox

### Elevator Pitch

Your AI assistant is smart, but it can't run Python scripts, call REST APIs, or process Excel files deterministically. mcpyrex fixes that — it's an open-source MCP server that gives GitHub Copilot 30+ custom tools powered by Python and Langchain. This module installs mcpyrex into a dedicated workspace, verifies MCP connectivity, and lets you run your first tool.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **What is mcpyrex?** — Overview of the project: why deterministic tools matter, what the ecosystem includes (tools, projects, pipelines). |
| 2 | **Clone the repository** — Clone mcpyrex-python into `work/400-mcpyrex/`. Open workspace in VS Code. |
| 3 | **Run the installer** — Execute `install-windows.ps1` (or macOS/Linux equivalent). Python 3.11+, virtual environment, pip dependencies. |
| 4 | **Verify MCP connection** — Check `.vscode/mcp.json`, restart MCP, confirm the server starts and tools are listed. |
| 5 | **Run a tool from terminal** — Use `python -m mcp_server.run list` and `python -m mcp_server.run run lng_count_words`. |
| 6 | **Run a tool from Copilot** — Ask GitHub Copilot to count words in a sentence. Verify it calls `lng_count_words`. |
| 7 | **Explore the catalog** — Use `lng_get_tools_info` to see all available tools and their descriptions. |

### What the Student Gets

- A fully working mcpyrex installation with 30+ MCP tools
- Understanding of the mcpyrex architecture (tools, projects, pipelines)
- Verified MCP connection between GitHub Copilot and the Python server
- Ability to run tools from both terminal and chat

### Placement Motivation

> **After 350 (OpenClaw) as the first module in the 400-series.** This is the installation/setup module — all subsequent mcpyrex modules depend on it. Comparable to module 300 (DMtools installation). Depends on: 010 (VS Code + Copilot), 100 (MCP concepts).

---

## ✅ Module 405: Word Count & Math — First Custom Tools

**Proposed ID:** `405`  
**Proposed Name:** mcpyrex: Word Count & Math — First Custom Tools

### Elevator Pitch

The simplest way to understand MCP tools is to use one. `lng_count_words` counts words with statistics (unique words, character count, avg word length). `lng_math_calculator` evaluates math expressions safely. These two tools teach the foundational pattern: every tool has a name, input schema, and deterministic output — no hallucinations.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Anatomy of a tool** — Read `tools/lng_count_words/tool.py`. Understand the pattern: function + settings.yaml + schema. |
| 2 | **Word count hands-on** — Count words from chat, from file, compare with LLM's answer. |
| 3 | **Math calculator** — Evaluate complex expressions. Compare with LLM's math (which hallucinates). |
| 4 | **Why deterministic > LLM** — Side-by-side: ask LLM to count words vs. tool. See the difference. |
| 5 | **Create your own simple tool** — Modify or create a basic tool following the same pattern. |

### What the Student Gets

- Understanding of the MCP tool anatomy (Python function + settings.yaml)
- First-hand proof that deterministic tools outperform LLMs for precise tasks
- Ability to read and understand any mcpyrex tool source

### Placement Motivation

> **After 400 (installation).** First hands-on module. Simplest tools to build understanding.

---

## ✅ Module 410: LLM Chains & Prompt Templates

**Proposed ID:** `410`  
**Proposed Name:** mcpyrex: LLM Chains & Prompt Templates

### Elevator Pitch

Langchain's chain and prompt template are the building blocks of every intelligent pipeline. This module teaches you to use `lng_llm_run_chain` for executing Langchain chains and `lng_llm_prompt_template` for managing reusable prompt templates with file storage. You'll build chains that combine LLM calls with structured inputs.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **What is a Langchain chain?** — Concept: input → prompt → model → output. |
| 2 | **Run a chain via MCP** — Use `lng_llm_run_chain` from Copilot chat. See the chain execute. |
| 3 | **Prompt templates** — Save, list, and use prompt templates with `lng_llm_prompt_template`. |
| 4 | **Template variables** — Create templates with `{variable}` placeholders. Fill them dynamically. |
| 5 | **Chain + template combo** — Build a reusable processing pipeline: template → chain → result. |

### What the Student Gets

- Understanding of Langchain chains through MCP
- A set of reusable prompt templates saved to disk
- Ability to combine templates with chains for repeatable workflows

### Placement Motivation

> **After 405.** Natural progression from simple tools to LLM-powered tools.

---

## ✅ Module 415: RAG with Vector Search

**Proposed ID:** `415`  
**Proposed Name:** mcpyrex: RAG with Vector Search

### Elevator Pitch

You have documents. You want AI to answer questions about them accurately. RAG (Retrieval-Augmented Generation) makes this possible by indexing your docs into a vector database and searching them before asking the LLM. This module uses `lng_rag_add_data` and `lng_rag_search` to build a working RAG system, then scales it with the `docs-rag` project for automated document processing.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **RAG concept** — Why LLMs need context retrieval. The embed → store → search → answer flow. |
| 2 | **Add data** — Use `lng_rag_add_data` to index sample documents. |
| 3 | **Search** — Use `lng_rag_search` to query the vector store. See relevant chunks. |
| 4 | **LLM-powered Q&A** — Ask questions, get answers grounded in your documents. |
| 5 | **docs-rag project** — Run the `docs-rag` batch pipeline to process an entire folder. |
| 6 | **RAG demo walkthrough** — Follow `llm-rag.demo.agent.md` end-to-end. |

### What the Student Gets

- A working RAG system powered by FAISS
- Experience with both manual RAG and automated batch processing
- Understanding of when RAG beats plain prompting

### Placement Motivation

> **After 410.** Builds on LLM chain understanding. RAG is the most requested enterprise use case. Ties to project `docs-rag`.

---

## ✅ Module 420: Structured Output & Chain of Thought

**Proposed ID:** `420`  
**Proposed Name:** mcpyrex: Structured Output & Chain of Thought

### Elevator Pitch

Two power techniques: get LLMs to output structured JSON/YAML/Markdown reliably with `lng_llm_structured_output`, and enable transparent step-by-step reasoning with `lng_llm_chain_of_thought`. Together they make LLM responses predictable and explainable.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Structured output** — Use `lng_llm_structured_output` to get JSON, YAML, and Markdown from LLM. |
| 2 | **Schema definition** — Define the output schema and see how LLM conforms to it. |
| 3 | **Chain of thought** — Use `lng_llm_chain_of_thought` for step-by-step reasoning. |
| 4 | **Memory in CoT** — See how conversation history helps CoT maintain context. |
| 5 | **Combined workflow** — Use CoT for reasoning, then structured output for the final answer. |

### What the Student Gets

- Ability to get reliable structured data from LLMs
- Understanding of chain-of-thought reasoning with memory
- A pattern for combining reasoning with structured results

### Placement Motivation

> **After 415.** Continues the LLM tools progression. Structured output is essential for pipelines.

---

## ✅ Module 425: LLM Agent Demo

**Proposed ID:** `425`  
**Proposed Name:** mcpyrex: LLM Agent Demo

### Elevator Pitch

A Langchain agent can autonomously decide which tools to use, plan steps, and iterate until it solves a problem. `lng_llm_agent_demo` demonstrates this in action — an agent with character counting, MD5 hashing, and regex matching tools that solves text processing tasks on its own.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **What is an agent?** — Agent = LLM + tools + reasoning loop. |
| 2 | **Run the agent demo** — Use `lng_llm_agent_demo` and observe tool selection. |
| 3 | **Trace the reasoning** — See how the agent decides which tool to call. |
| 4 | **Test edge cases** — Give the agent ambiguous tasks. See how it handles them. |
| 5 | **Agent vs. chain** — When to use agents vs. fixed chains. |

### What the Student Gets

- Understanding of agent-based reasoning
- First-hand observation of autonomous tool selection
- Clarity on agents vs. chains decision matrix

### Placement Motivation

> **After 420.** The culmination of the LLM tools arc: from chains → RAG → structured output → autonomous agents.

---

## ✅ Module 430: Batch Pipelines

**Proposed ID:** `430`  
**Proposed Name:** mcpyrex: Batch Pipelines

### Elevator Pitch

Real automation requires sequences of steps: fetch data → transform → save → notify. `lng_batch_run` is the pipeline engine of mcpyrex — it supports sequential steps, JavaScript expressions, conditionals, loops, parallel execution, and timing control. This is where individual tools become workflows.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Pipeline anatomy** — Read a `pipeline.json` file. Understand steps, variables, expressions. |
| 2 | **Run a simple pipeline** — Execute a 3-step pipeline: count words → calculate → save result. |
| 3 | **Conditionals and loops** — Add if/else logic and iteration to pipelines. |
| 4 | **Parallel execution** — Run multiple steps simultaneously. |
| 5 | **Build your own** — Create a pipeline that combines 3+ tools for a practical task. |

### What the Student Gets

- Ability to create multi-step automation pipelines
- Understanding of pipeline language (expressions, conditionals, loops)
- A reusable pipeline they built themselves

### Placement Motivation

> **After 425.** Pipelines orchestrate all the tools learned so far. Required for later project modules (docs-rag, telemetry, instruction-processor).

---

## ✅ Module 435: File Operations

**Proposed ID:** `435`  
**Proposed Name:** mcpyrex: File Operations

### Elevator Pitch

Read files, write files, list directories with glob patterns — `lng_file` gives your AI assistant deterministic file system access with encoding support, offset/limit, and JSON/text output. Simple but essential for any automation.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Read files** — Use `lng_file` to read files with different encodings and offsets. |
| 2 | **Write files** — Write content to new and existing files. |
| 3 | **List directories** — Use glob patterns to explorer workspace files. |
| 4 | **Pipeline integration** — Combine file ops with batch pipeline for file processing workflows. |

### What the Student Gets

- Ability to perform deterministic file operations through MCP
- Understanding of when file tools beat LLM-based file access

### Placement Motivation

> **After 430.** File operations support many later modules (Excel, JSON, pipelines).

---

## ✅ Module 440: Terminal Execution

**Proposed ID:** `440`  
**Proposed Name:** mcpyrex: Terminal Execution

### Elevator Pitch

Run shell commands, analyze output, and get AI-powered explanations — all through MCP. `lng_terminal` executes commands in any shell (PowerShell, bash, cmd, zsh) with async sessions and timeout control. `lng_terminal_chat` adds LLM analysis of terminal output.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Run commands** — Execute terminal commands via `lng_terminal`. See output in chat. |
| 2 | **Shell selection** — Switch between PowerShell, bash, cmd. |
| 3 | **Async sessions** — Start long-running commands, check status later. |
| 4 | **Terminal chat** — Use `lng_terminal_chat` to analyze command output with LLM. |
| 5 | **Error debugging** — Run a failing command, ask AI to explain the error. |

### What the Student Gets

- Ability to execute and manage terminal sessions through MCP
- AI-powered terminal output analysis

### Placement Motivation

> **After 435.** Terminal is the next layer of system access after files.

---

## ✅ Module 445: HTTP Client & REST APIs

**Proposed ID:** `445`  
**Proposed Name:** mcpyrex: HTTP Client & REST APIs

### Elevator Pitch

`lng_http_client` is a universal HTTP client with request/batch/paginate modes, session management, cURL export, HAR import, and full auth support (Bearer, Basic, OAuth, API keys). It turns your AI assistant into an API testing and integration powerhouse.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Simple request** — Make GET/POST requests to a public API. |
| 2 | **Authentication** — Use Bearer tokens, API keys. |
| 3 | **Batch requests** — Send multiple requests in sequence. |
| 4 | **Pagination** — Auto-paginate through API results. |
| 5 | **cURL export** — Export requests as cURL commands for sharing. |

### What the Student Gets

- A powerful API client accessible from AI chat
- Understanding of HTTP authentication patterns through MCP

### Placement Motivation

> **After 440.** HTTP is required for webhook, cookie, and Jira modules.

---

## ✅ Module 450: Webhook Server — Calculator API

**Proposed ID:** `450`  
**Proposed Name:** mcpyrex: Webhook Server — Calculator API

### Elevator Pitch

Build a working HTTP server in minutes — from Copilot chat. `lng_webhook_server` creates webhooks with pipeline execution, variable substitution, HTML templates, and SSL support. Two demos show the full range: a beautiful calculator HTML page and a REST API returning JSON.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Demo 1: Simple Calculator API** — Follow `simple-calculator-api.demo.agent.md`. Build a JSON API on port 8089. |
| 2 | **Demo 2: Calculator HTML Page** — Follow `calculator-html-page.demo.agent.md`. Build a beautiful web page. |
| 3 | **Pipeline integration** — See how webhooks trigger batch pipelines. |
| 4 | **Custom webhook** — Create your own webhook for a practical task. |

### What the Student Gets

- Two working webhook servers (API + HTML)
- Understanding of webhook-to-pipeline integration
- Ability to create custom endpoints from AI chat

### Placement Motivation

> **After 445 (HTTP Client).** Natural progression: first consume APIs, then create them. Has 2 demo walkthroughs.

---

## ✅ Module 455: Browser Automation

**Proposed ID:** `455`  
**Proposed Name:** mcpyrex: Browser Automation

### Elevator Pitch

Selenium-powered browser automation through MCP. `lng_browser_automation` supports Chrome and Firefox with session management, script execution, and element interaction. Automate web testing, data scraping, or UI verification — all driven by your AI assistant.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Start a browser session** — Launch Chrome/Firefox through MCP. |
| 2 | **Navigate and interact** — Open pages, click elements, fill forms. |
| 3 | **Execute scripts** — Run JavaScript in the browser context. |
| 4 | **Session management** — Manage multiple browser sessions. |
| 5 | **Practical automation** — Automate a real-world web task. |

### What the Student Gets

- Browser automation capability through AI chat
- Understanding of Selenium integration with MCP

### Placement Motivation

> **After 450.** Extends web interaction from HTTP requests to full browser control.

---

## ✅ Module 460: JSON/CSV & Excel Batch Processing

**Proposed ID:** `460`  
**Proposed Name:** mcpyrex: JSON/CSV & Excel Batch Processing

### Elevator Pitch

Data comes in JSON, CSV, and Excel. `lng_json_to_csv` converts between formats with pandas, handling nested structures. `lng_xls_batch` performs Excel/CSV batch operations with expression support and formula preservation. Together they make your AI a data processing engine.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **JSON to CSV** — Convert nested JSON to clean CSV with configurable delimiters. |
| 2 | **CSV to Markdown** — Generate markdown tables from data. |
| 3 | **Excel operations** — Use `lng_xls_batch` for batch Excel processing. |
| 4 | **Formula preservation** — Copy/paste data while keeping Excel formulas intact. |
| 5 | **Pipeline combo** — Fetch data → transform → save as Excel report. |

### What the Student Gets

- Data format conversion through AI chat
- Excel batch processing with formula support
- A data processing pipeline template

### Placement Motivation

> **After 455.** Data processing is a common automation need. Builds on file and pipeline knowledge.

---

## ✅ Module 465: Cookie Grabber & Secure API Calls

**Proposed ID:** `465`  
**Proposed Name:** mcpyrex: Cookie Grabber & Secure API Calls

### Elevator Pitch

Access protected APIs that require browser cookies. `lng_cookie_grabber` extracts cookies from Chrome using AES-256-GCM encrypted storage, then feeds them to `lng_http_client` for authenticated API access. The demo shows the full workflow: grab cookies → make secure REST call.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Security overview** — How cookies work, why encryption matters, the threat model. |
| 2 | **Follow the demo** — `make-secure-rest-api-call-with-cookies-grabbing.demo.agent.md`. |
| 3 | **Cookie extraction** — Grab cookies from an active Chrome session. |
| 4 | **Secure API call** — Use extracted cookies with `lng_http_client`. |
| 5 | **Security best practices** — When this is appropriate and when it isn't. |

### What the Student Gets

- Understanding of encrypted cookie management
- Ability to access cookie-protected APIs through MCP
- Security awareness for cookie-based automation

### Placement Motivation

> **After 460.** Requires HTTP client knowledge. Has a demo walkthrough.

---

## ✅ Module 470: Jira Integration & PDF Processing

**Proposed ID:** `470`  
**Proposed Name:** mcpyrex: Jira Integration & PDF Processing

### Elevator Pitch

Connect Copilot to Jira. `lng_jira` reads tickets, downloads PDF attachments, extracts images from PDFs, and uploads them back. The demo walks through the complete workflow: ticket → PDF → images → upload. A practical integration for project management automation.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Jira connection** — Configure Jira credentials and endpoint. |
| 2 | **Follow the demo** — `jira-pdf-processing.demo.agent.md`. |
| 3 | **Read ticket data** — Retrieve Jira ticket descriptions and metadata. |
| 4 | **PDF processing** — Download and extract content from PDF attachments. |
| 5 | **Upload results** — Push extracted images back to the ticket. |

### What the Student Gets

- Jira integration through MCP
- PDF processing pipeline
- A reusable Jira automation workflow

### Placement Motivation

> **After 465.** Requires HTTP/API knowledge. Has a demo walkthrough. Major enterprise use case.

---

## ✅ Module 475: JavaScript Execution Engine

**Proposed ID:** `475`  
**Proposed Name:** mcpyrex: JavaScript Execution Engine

### Elevator Pitch

`lng_javascript` stores and executes JavaScript functions inside the Python environment using PyMiniRacer. ES6+ support, console logging, and function persistence — useful for custom transformations, data processing, and extending pipeline logic without leaving the MCP ecosystem.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Store functions** — Save JavaScript functions for reuse. |
| 2 | **Execute JS** — Run JavaScript code and capture output. |
| 3 | **Console logging** — Use console.log for debugging. |
| 4 | **Pipeline integration** — Use JS functions within batch pipelines for transformations. |

### What the Student Gets

- JavaScript execution capability within mcpyrex
- Understanding of cross-language tool integration

### Placement Motivation

> **After 470.** A utility module that enriches pipeline capabilities.

---

## ✅ Module 480: PowerPoint Notes Extraction

**Proposed ID:** `480`  
**Proposed Name:** mcpyrex: PowerPoint Notes Extraction

### Elevator Pitch

Extract speaker notes from PowerPoint presentations in JSON, plain text, or file format. `lng_pptx` reads `.pptx` files and pulls out the notes — perfect for converting presentations into documentation, training scripts, or meeting minutes.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Extract notes** — Use `lng_pptx` to read speaker notes from a .pptx file. |
| 2 | **Output formats** — Get results in JSON, plain text, or saved to file. |
| 3 | **Batch processing** — Process multiple presentations via pipeline. |
| 4 | **Documentation conversion** — Turn presentation notes into markdown documentation. |

### What the Student Gets

- Ability to extract PowerPoint content through AI chat
- A presentation-to-documentation workflow

### Placement Motivation

> **After 475.** Standalone utility module for office document processing.

---

## ✅ Module 485: Screenshot & Speech Tools

**Proposed ID:** `485`  
**Proposed Name:** mcpyrex: Screenshot & Speech Tools

### Elevator Pitch

Capture screenshots of all your screens and convert text to high-quality speech. `lng_save_screenshot` takes screenshots using MSS. `lng_speech` generates multilingual audio via ElevenLabs API. Two utility tools that bridge the gap between text and multimedia.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Screenshots** — Capture all screens, save to folder, reference in chat. |
| 2 | **Available voices** — List ElevenLabs voices with `get_voices`. |
| 3 | **Text-to-speech** — Convert text to audio with `from_text`. |
| 4 | **Practical uses** — Automated reporting, accessibility, content creation. |

### What the Student Gets

- Screenshot capture through MCP
- Text-to-speech generation with ElevenLabs
- Multimedia automation capabilities

### Placement Motivation

> **After 480.** Multimedia utility modules. Requires ElevenLabs API key for speech.

---

## ✅ Module 490: Email Client

**Proposed ID:** `490`  
**Proposed Name:** mcpyrex: Email Client

### Elevator Pitch

Send emails from your AI assistant. `lng_email_client` supports SMTP, SendGrid, Mailgun, and SES with HTML templates, attachments, and batch operations. Automate notifications, reports, and alerts — all driven by natural language commands.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Configure provider** — Set up SMTP or SendGrid credentials. |
| 2 | **Send an email** — Compose and send from chat. |
| 3 | **HTML templates** — Use templates for formatted emails. |
| 4 | **Attachments** — Attach files from the workspace. |
| 5 | **Batch emails** — Send to multiple recipients via pipeline. |

### What the Student Gets

- Email sending capability through AI assistant
- Template-based email automation
- Batch notification workflows

### Placement Motivation

> **After 485.** Communication tool. Natural follow-up to data processing modules.

---

## ✅ Module 495: Telegram Bot — Super Empath

**Proposed ID:** `495`  
**Proposed Name:** mcpyrex: Telegram Bot — Super Empath

### Elevator Pitch

Build a Telegram bot that serves as an "emotional translator" — reformulating harsh messages into empathetic alternatives. This module combines `lng_telegram` (polling server, chat extraction), `lng_llm`, and `lng_batch_run` into the `super-empath` project — a fully functional bot with multi-user sessions, deep linking, and message classification.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Telegram bot setup** — Create a bot via BotFather, configure tokens. |
| 2 | **Polling server** — Start the Telegram polling server through MCP. |
| 3 | **Super Empath walkthrough** — Deploy the emotional translator bot. |
| 4 | **Multi-user sessions** — Test with multiple participants. |
| 5 | **Chat extraction** — Use the chat extractor to pull message history. |

### What the Student Gets

- A working Telegram bot with LLM integration
- Understanding of bot-to-pipeline architecture
- The Super Empath project running end-to-end

### Placement Motivation

> **After 490 (Email).** Continues the communication tools arc. The most complex project — combines tools, LLM, and pipelines. Ties to project `super-empath`.

---

## ✅ Module 500: Windows Automation (WinAPI)

**Proposed ID:** `500`  
**Proposed Name:** mcpyrex: Windows Automation (WinAPI)

### Elevator Pitch

Automate Windows desktop applications through hotkeys and the Windows API. `lng_winapi` has three complete demos: auto-translate clipboard text, automate Chrome browsing, and interact with Microsoft Teams. This is desktop automation driven by your AI assistant — beyond the browser and terminal.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Demo 1: Auto-translate clipboard** — `auto-translate-text-from-clipboard.demo.agent.md`. Hotkey grabs clipboard → LLM translates → pastes back. |
| 2 | **Demo 2: Chrome automation** — `working-with-chrome.demo.agent.md`. Open Chrome, navigate, execute console commands. |
| 3 | **Demo 3: Teams messaging** — `working-with-teams.demo.agent.md`. Find contacts, send messages via automation. |
| 4 | **Custom hotkey chain** — Create your own automation using the WinAPI tools. |

### What the Student Gets

- Windows desktop automation through MCP tools
- Three working automation scripts (clipboard, Chrome, Teams)
- Understanding of hotkey-driven AI workflows

### Placement Motivation

> **After 495.** Windows-only module with 3 demos. The richest demo collection. Advanced automation.

---

## ✅ Module 505: WebSocket & Agent Pairing

**Proposed ID:** `505`  
**Proposed Name:** mcpyrex: WebSocket & Agent Pairing

### Elevator Pitch

Real-time communication between agents. `lng_websocket_server` creates WebSocket servers/clients with WSS encryption, heartbeats, and auto-reconnection. `lng_agents_pairing` enables secure file transfer between Copilot agent instances using AES-256-GCM encrypted WebSocket channels. Two agents, one mission.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **WebSocket basics** — Start a WebSocket server through MCP. Connect a client. |
| 2 | **Message exchange** — Send and receive messages in real time. |
| 3 | **Agent pairing** — Connect two agent instances for secure communication. |
| 4 | **File transfer** — Transfer files between agents with end-to-end encryption. |
| 5 | **Practical use case** — Coordinate agents working on different aspects of a task. |

### What the Student Gets

- Real-time WebSocket communication through MCP
- Agent-to-agent secure communication
- Understanding of multi-instance agent coordination

### Placement Motivation

> **After 500.** Advanced networking and agent coordination. Builds toward multi-agent orchestration.

---

## ✅ Module 510: Multi-Agent Orchestration

**Proposed ID:** `510`  
**Proposed Name:** mcpyrex: Multi-Agent Orchestration

### Elevator Pitch

One agent is good. Multiple specialized agents working together is better. `lng_multi_agent` provides a MultiAgentManager that orchestrates sub-agents with tool integration, memory management, and async processing. This is the capstone module for the mcpyrex series — coordinating everything learned into a multi-agent system.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Multi-agent architecture** — Manager + sub-agents. Module delegation. Memory. |
| 2 | **Configure agents** — Set up specialized agents for different tasks. |
| 3 | **Delegate work** — Send tasks to sub-agents, collect results. |
| 4 | **Memory management** — ConversationSummaryBufferMemory for context retention. |
| 5 | **End-to-end workflow** — A complex task split across multiple agents. |

### What the Student Gets

- Multi-agent orchestration through MCP
- Understanding of agent delegation and memory patterns
- A working multi-agent workflow

### Placement Motivation

> **After 505.** Capstone for agent capabilities. Requires understanding of all tool types.

---

## ✅ Module 515: Docker Terminal

**Proposed ID:** `515`  
**Proposed Name:** mcpyrex: Docker Terminal

### Elevator Pitch

Run commands in isolated Docker containers through MCP. `lng_terminal_docker` manages container lifecycle, volume mounting, port mapping, and image management — all from your AI chat. Perfect for safe experimentation and reproducible environments.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Docker basics through MCP** — Pull an image, start a container, run a command. |
| 2 | **Volume mounting** — Share workspace files with the container. |
| 3 | **Port mapping** — Expose container services to localhost. |
| 4 | **Image management** — Build, list, remove images. |
| 5 | **Isolated testing** — Run risky commands safely in a container. |

### What the Student Gets

- Docker management through AI chat
- Isolated command execution capability
- Understanding of container-based tool isolation

### Placement Motivation

> **After 510.** Requires Docker installed. Advanced infrastructure module.

---

## ✅ Module 520: Copilot Telemetry Analysis

**Proposed ID:** `520`  
**Proposed Name:** mcpyrex: Copilot Telemetry Analysis

### Elevator Pitch

How productive is your team with Copilot? The `telemetry` project converts GitHub Copilot telemetry JSON files into analyzable CSV and Excel reports. Use it to measure adoption, track usage patterns, and make data-driven decisions about AI tooling investment.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Export telemetry** — Get Copilot telemetry JSON files. |
| 2 | **Run the pipeline** — Follow `convert-copilot-telemetry-jsons-to-xls.demo.agent.md`. |
| 3 | **Analyze results** — Open the generated Excel/CSV reports. |
| 4 | **Key metrics** — Understand acceptance rate, suggestion count, language breakdown. |
| 5 | **Team reporting** — Generate a team-level usage summary. |

### What the Student Gets

- Copilot telemetry processing pipeline
- Excel/CSV reports for usage analysis
- Metrics framework for AI adoption tracking

### Placement Motivation

> **After 515.** Ties to project `telemetry`. Requires batch pipeline and Excel processing knowledge. Very relevant for managers.

---

## ✅ Module 525: CSS Selector Finder

**Proposed ID:** `525`  
**Proposed Name:** mcpyrex: CSS Selector Finder

### Elevator Pitch

Finding the right CSS selector for browser automation is tedious. The `css-selector-finder` project injects an interactive overlay into any web page — hover to highlight, click to select, get smart selectors (ID, class, data-testid, ARIA, nth-child). Works in Chrome and Firefox. Essential for QA automation.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Inject the script** — Load the selector finder into a web page. |
| 2 | **Interactive selection** — Hover, click, copy selectors. |
| 3 | **Selector types** — Understand ID, class, data-testid, ARIA, and hierarchy-based selectors. |
| 4 | **Integration** — Use found selectors with browser automation or testing tools. |

### What the Student Gets

- Interactive CSS selector discovery tool
- Understanding of selector strategies for automation
- Integration with browser automation modules

### Placement Motivation

> **After 520.** Ties to project `css-selector-finder`. Complements browser automation (455).

---

## ✅ Module 530: Instruction Processor

**Proposed ID:** `530`  
**Proposed Name:** mcpyrex: Instruction Processor

### Elevator Pitch

You have 20 instruction files. How do you improve them all consistently? The `instruction-processor` project runs each file through an LLM enhancement pipeline, saving improved versions as `.updated.agent.md`. Batch processing meets instruction quality — automated and repeatable.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The problem** — Manual instruction improvement doesn't scale. |
| 2 | **Run the pipeline** — Follow `process-instructions.demo.agent.md`. |
| 3 | **Review results** — Compare original vs. enhanced instruction files. |
| 4 | **Customize the template** — Modify the enhancement prompt for your needs. |
| 5 | **Apply to your project** — Process your own instruction files. |

### What the Student Gets

- Automated instruction improvement pipeline
- Understanding of LLM-based content processing
- A reusable workflow for maintaining instruction quality

### Placement Motivation

> **After 525.** Ties to project `instruction-processor`. Requires batch pipeline knowledge. Meta-module: improving the tools you use.

---

## ✅ Module 535: Copilot CLI — Terminal AI

**Proposed ID:** `535`  
**Proposed Name:** mcpyrex: Copilot CLI — Terminal AI

### Elevator Pitch

Ask AI questions from the terminal — without opening an IDE. The `copilot-cli` project provides `ask` scripts (PowerShell, Bash, Batch) that connect to your LLM with automatic system context detection (OS, shell, architecture). Simple question mode + command analysis mode.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Install the CLI** — Set up `ask` alias for your OS. |
| 2 | **Simple questions** — Ask the terminal AI programming questions. |
| 3 | **Command analysis** — Pipe command output to AI for analysis. |
| 4 | **System context** — See how automatic OS/shell detection improves responses. |
| 5 | **Global installation** — Set up system-wide alias. |

### What the Student Gets

- Terminal-based AI access without IDE
- Command output analysis capability
- A globally available `ask` command

### Placement Motivation

> **After 530.** Ties to project `copilot-cli`. Light utility module for terminal-centric users.

---

## ✅ Module 540: Web MCP — Browser Interface

**Proposed ID:** `540`  
**Proposed Name:** mcpyrex: Web MCP — Browser Interface

### Elevator Pitch

Access all your MCP tools from a web browser — no IDE required. The `web-mcp` project provides a static web interface (port 8080) + execution API (port 8081) with daemon mode, auto-restart, and cross-platform support. Share your tools with teammates who don't use VS Code.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Start the web server** — Run `web-mcp/run.ps1 start`. |
| 2 | **Browse tools** — Open `http://localhost:8080` and explore. |
| 3 | **Execute tools** — Run tools from the browser interface. |
| 4 | **API access** — Use the execution API at port 8081 programmatically. |
| 5 | **Daemon mode** — Configure auto-restart and background operation. |

### What the Student Gets

- Web-accessible MCP tool interface
- Understanding of MCP server deployment beyond IDE
- API access for programmatic tool execution

### Placement Motivation

> **After 535.** Ties to project `web-mcp`. Alternative access method for the entire toolset.

---

## ✅ Module 545: Telescope Avatar Grabber

**Proposed ID:** `545`  
**Proposed Name:** mcpyrex: Telescope Avatar Grabber

### Elevator Pitch

The `telescope-avatar-grabber` project demonstrates a practical pipeline: grab user avatars from the EPAM Telescope API using encrypted cookie management (AES-256-GCM + PBKDF2). A real-world example of cookie grabber + HTTP client + batch pipeline working together.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Pipeline overview** — Understand the avatar grabbing workflow. |
| 2 | **Cookie setup** — Configure encrypted cookie storage for Telescope. |
| 3 | **Run the pipeline** — Execute the avatar grabbing batch pipeline. |
| 4 | **Results** — Review downloaded avatars and user info JSON. |
| 5 | **Adaptation** — How to modify for other internal APIs. |

### What the Student Gets

- A working API integration pipeline with encrypted cookies
- Understanding of enterprise API automation patterns
- Reusable template for cookie-based internal API access

### Placement Motivation

> **After 540.** Ties to project `telescope-avatar-grabber`. Requires cookie grabber and HTTP client knowledge. EPAM-specific but demonstrates the pattern.

---

## ✅ Module 550: Tools Info & Discovery

**Proposed ID:** `550`  
**Proposed Name:** mcpyrex: Tools Info & Discovery

### Elevator Pitch

Meta-module: use `lng_get_tools_info` to discover available tools (JSON/Markdown output) and `lng_copilot` to explore GitHub Copilot integration. This is the "map" module — learn to navigate the full mcpyrex ecosystem and find the right tool for any task.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **List all tools** — Use `lng_get_tools_info` to get the full catalog. |
| 2 | **Tool schema inspection** — Examine input/output schemas of any tool. |
| 3 | **Copilot integration** — Explore `lng_copilot` capabilities (chat export). |
| 4 | **Tool selection framework** — Given a task, find the right tool. |
| 5 | **Creating new tools** — Understand the pattern for contributing new tools. |

### What the Student Gets

- Complete awareness of the mcpyrex ecosystem
- Tool selection skills for any automation task
- Understanding of how to extend mcpyrex with new tools

### Placement Motivation

> **Final module in the series.** The capstone that ties everything together. Best appreciated after experiencing many individual tools.

---

## Summary

| ID | Module Name | Source | Has Demo? |
|----|-------------|--------|-----------|
| 400 | Installing mcpyrex | setup | — |
| 405 | Word Count & Math | `lng_count_words`, `lng_math_calculator` | No |
| 410 | LLM Chains & Prompt Templates | `lng_llm` (chain, prompt_template) | No |
| 415 | RAG with Vector Search | `lng_llm/rag`, project `docs-rag` | ✅ `llm-rag.demo.agent.md` |
| 420 | Structured Output & Chain of Thought | `lng_llm` (structured_output, chain_of_thought) | No |
| 425 | LLM Agent Demo | `lng_llm/agent_demo` | No |
| 430 | Batch Pipelines | `lng_batch_run` | No |
| 435 | File Operations | `lng_file` | No |
| 440 | Terminal Execution | `lng_terminal`, `lng_terminal_chat` | No |
| 445 | HTTP Client & REST APIs | `lng_http_client` | No |
| 450 | Webhook Server — Calculator API | `lng_webhook_server` | ✅ 2 demos |
| 455 | Browser Automation | `lng_browser_automation` | No |
| 460 | JSON/CSV & Excel Processing | `lng_json_to_csv`, `lng_xls_batch` | No |
| 465 | Cookie Grabber & Secure API | `lng_cookie_grabber` | ✅ 1 demo |
| 470 | Jira Integration & PDF | `lng_jira` | ✅ 1 demo |
| 475 | JavaScript Execution Engine | `lng_javascript` | No |
| 480 | PowerPoint Notes Extraction | `lng_pptx` | No |
| 485 | Screenshot & Speech | `lng_save_screenshot`, `lng_speech` | No |
| 490 | Email Client | `lng_email_client` | No |
| 495 | Telegram Bot — Super Empath | `lng_telegram`, project `super-empath` | No |
| 500 | Windows Automation (WinAPI) | `lng_winapi` | ✅ 3 demos |
| 505 | WebSocket & Agent Pairing | `lng_websocket_server`, `lng_agents_pairing` | No |
| 510 | Multi-Agent Orchestration | `lng_multi_agent` | No |
| 515 | Docker Terminal | `lng_terminal_docker` | No |
| 520 | Copilot Telemetry Analysis | project `telemetry` | ✅ 1 demo |
| 525 | CSS Selector Finder | project `css-selector-finder` | No |
| 530 | Instruction Processor | project `instruction-processor` | ✅ 1 demo |
| 535 | Copilot CLI — Terminal AI | project `copilot-cli` | No |
| 540 | Web MCP — Browser Interface | project `web-mcp` | No |
| 545 | Telescope Avatar Grabber | project `telescope-avatar-grabber` | No |
| 550 | Tools Info & Discovery | `lng_get_tools_info`, `lng_copilot` | No |

**Total: 31 modules** (1 installation + 22 tool modules + 8 project modules)
