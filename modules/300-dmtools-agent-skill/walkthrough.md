---
external_workspace: true
---

# DMtools — Agent Skill & Automation Catalog - Hands-on Walkthrough

In this module you will clone the DMtools repository, install its agent skill into your AI IDE, and explore the full catalog of 152+ automation tools. You will pick a capability that interests you and use the AI (with the skill loaded) to understand it deeply and generate a working configuration.

This module runs in a **separate workspace** (`work/300-task/`) to avoid conflicts between the course instructions and DMtools' own AI configuration files.

## Prerequisites

- Cursor or VS Code with GitHub Copilot installed
- Git installed
- Git Bash (Windows) or Terminal (macOS/Linux)
- Completed Module 090: AI Skills - Context, Tools & Memory

---

## Part 1: Clone the DMtools Repository

### What We'll Do

Clone the DMtools project into your practice folder. This gives you:
- The full source code of DMtools (Java project)
- The `dmtools-ai-docs/` folder — the living documentation and skill source
- A Git repository you can `git pull` anytime to get the latest updates

### If You Already Have It

If you have already cloned DMtools into `work/300-task/` from a previous session:

```bash
cd work/300-task
git pull
```

If the pull succeeds — **skip to Part 3** (the skill is already installed too).

### Clone

From the course workspace root, run:

```bash
git clone https://github.com/IstiN/dmtools.git work/300-task
```

This creates `work/300-task/` with the full DMtools project inside.

---

## Part 2: Install the DMtools Agent Skill

### What Is an Agent Skill?

A skill is **not** an application — it is a documentation bundle that your AI assistant reads before answering questions. When installed, the skill:

- Adds ~500KB of structured knowledge about DMtools to your project
- Tells your AI assistant what DMtools can do, how to configure it, and what every tool and job does
- Is automatically picked up by Cursor, Claude, or VS Code with GitHub Copilot
- Lives in your project folder — not globally

Think of it like the difference between asking a colleague who has never heard of a tool vs. one who has read the full manual.

**What it does NOT do**: it does not install the dmtools CLI or run any code.

### Install the Skill

Open a terminal inside your IDE. Navigate to the cloned project:

```bash
cd work/300-task
```

**macOS / Linux / Windows (Git Bash):**

```bash
curl -fsSL https://github.com/IstiN/dmtools/releases/download/v1.7.133/skill-install.sh | bash
```

You should see output like:

```
Found skill directories:
  1. .cursor/skills

Non-interactive mode detected, installing to all detected locations
✓ Installed to .cursor/skills/dmtools
```

> **"No skill directories found"?** Create the appropriate folder first:
>
> - Cursor: `mkdir -p .cursor/skills`
> - VS Code: `mkdir -p .github`
>
> Then run the installer again.

### Manual Installation (Windows PowerShell or no curl)

If you cannot use Git Bash:

1. Download the latest skill ZIP from [github.com/IstiN/dmtools/releases](https://github.com/IstiN/dmtools/releases) — look for `dmtools-skill-v*.zip`
2. Extract it into one of these folders inside `work/300-task/`:
   - Cursor: `.cursor/skills/dmtools/`
   - VS Code: `.github/skills/dmtools/` or copy `SKILL.md` content into your Copilot instructions

### Verify Installation

```bash
ls .cursor/skills/dmtools/
```

You should see:

```
SKILL.md    references/
```

- `SKILL.md` — the main skill definition file your AI reads automatically
- `references/` — detailed documentation organized by category

### Test the Skill

Open a new AI chat in your IDE and ask:

> "What is DMtools and what can I do with it?"

Your AI should give a structured answer mentioning MCP tools, Jobs, and integrations — not a generic response. If it does not know DMtools, try opening a completely new chat window to force context reload.

---

## Part 3: Core Architecture Pattern

Every DMtools automation follows the same envelope:

```json
{
  "name": "JobName",
  "params": {
    "...input source...",
    "...what to do...",
    "...output target..."
  }
}
```

### The Three Parts

- **`name`** — which Job to run. This maps directly to a Java class name — never change the spelling. Example: `"TestCasesGenerator"` → `new TestCasesGenerator()` in Java.

- **Input source** — where to get data. Depends on the Job:

  | Input type | Used by | Example |
  |-----------|---------|---------|
  | `inputJql` | Jobs that read Jira tickets | `"inputJql": "project = MYPROJ AND type = Story"` |
  | `dataSources` | ReportGenerator (GitHub, CSV, Figma...) | `"dataSources": [{"name": "pullRequests", ...}]` |
  | `jsPath` | JSRunner | `"jsPath": "agents/js/myScript.js"` |

- **Output target** — where to put the result:

  | Output type | What it does |
  |------------|-------------|
  | `"outputType": "comment"` | Post as a comment on the ticket |
  | `"outputType": "field"` | Update a field on the ticket |
  | `"outputPath": "reports/output"` | Save as HTML/JSON files |
  | `"outputType": "none"` | Dry run — no changes made |

### Two Concrete Examples

**Example A — Jira as input:**
```json
{
  "name": "Teammate",
  "params": {
    "inputJql": "project = MYPROJ AND type = Story",
    "outputType": "comment"
  }
}
```

**Example B — GitHub as input:**
```json
{
  "name": "ReportGenerator",
  "params": {
    "dataSources": [{"name": "pullRequests", "params": {"sourceType": "github", "workspace": "my-org", "repository": "my-repo"}}],
    "output": {"outputPath": "reports/output"}
  }
}
```

The Job name changes, the input source changes, the output target changes — but the envelope `{ "name": ..., "params": {...} }` is always the same.

---

## Part 4: Catalog — MCP Tools (152+ tools across 16 integrations)

MCP Tools are the **atomic building blocks** — each one is a single API call. DMtools wraps 16 different platforms into a unified interface.

> 💡 **Always check the latest catalog.** The live reference is in `work/300-task/dmtools-ai-docs/references/mcp-tools/`. Run `git pull` to get the most current list.

| Integration | Tools | What You Can Do |
|------------|-------|----------------|
| **Jira** | 52 | Get/create/update tickets, search by JQL, manage comments, attachments, labels, fix versions, sprint operations, Xray test management |
| **MS Teams** | 30 | Send/read messages, manage chats and channels, download files, get meeting transcripts |
| **Confluence** | 17 | Create/update/read pages, search content, manage attachments |
| **Azure DevOps** | 14 | Get/create/update work items, run queries, manage comments and attachments |
| **Figma** | 12 | Extract design data, download icons, read layers, styles, components |
| **Gemini** | 2 | AI chat, multimodal processing (Google's free tier — 15 req/min) |
| **OpenAI** | 2 | AI chat, vision models with file support |
| **Anthropic** | 2 | Claude chat |
| **Bedrock** | 2 | AWS Claude |
| **DIAL** | 2 | Enterprise AI gateway |
| **Ollama** | 2 | Local AI models |
| **Knowledge Base** | 5 | Document search, indexing, RAG (retrieval-augmented generation) |
| **File** | 4 | Read/write files on disk |
| **Mermaid** | 3 | Generate diagrams (flowcharts, sequence, class, etc.) |
| **SharePoint** | 2 | Document management |
| **TestRail** | — | Test case management |
| **CLI** | 1 | Execute shell commands |

### How MCP Tools Are Used

In JavaScript agents, every tool is a direct function call:

```javascript
const ticket = jira_get_ticket("PROJ-123");
const analysis = gemini_ai_chat("Analyze this: " + ticket.fields.description);
jira_post_comment("PROJ-123", analysis);
```

You do not use MCP tools directly from the command line — they are used by **Jobs** and **JS Agents** under the hood.

---

## Part 5: Catalog — Jobs (23 Ready-Made Workflows)

Jobs are **pre-built workflows** that orchestrate MCP tools and AI to accomplish complex tasks. Each Job is a Java class with specific parameters.

> 💡 **Live reference:** `work/300-task/dmtools-ai-docs/references/jobs/README.md`

### Business Analysis

| Job | What It Does |
|-----|-------------|
| `RequirementsCollector` | Gather and analyze requirements from tickets |
| `UserStoryGenerator` | Generate user stories from requirements |
| `PreSaleSupport` | Pre-sales analysis and proposals |
| `BAProductivityReport` | BA team productivity metrics (features created, stories written, Figma activity) |

### Quality Assurance

| Job | What It Does |
|-----|-------------|
| `TestCasesGenerator` | Auto-generate test cases from Jira stories (Xray or Cucumber format) |
| `QAProductivityReport` | QA team metrics (test cases created, bugs found, stories tested) |

### Development

| Job | What It Does |
|-----|-------------|
| `CodeGenerator` | Generate code from user stories |
| `UnitTestsGenerator` | Generate unit tests for existing code |
| `DevProductivityReport` | Dev team metrics (stories completed, PRs, code changes, time spent) |
| `CommitsTriage` | Analyze and categorize git commits |

### Architecture & Documentation

| Job | What It Does |
|-----|-------------|
| `SolutionArchitectureCreator` | Create solution architecture documents |
| `DiagramsCreator` | Generate Mermaid diagrams from project context |
| `InstructionsGenerator` | Extract patterns from existing tickets → generate reusable guidelines |
| `DocumentationGenerator` | Generate technical documentation |

### Reports

| Job | What It Does |
|-----|-------------|
| `ReportGenerator` | Flexible report: pull data from Jira + GitHub PRs + commits + CSV + Figma → generate HTML with charts, scores, custom formulas |

### AI Assistants

| Job | What It Does |
|-----|-------------|
| `Teammate` | Flexible AI assistant with custom instructions — can process tickets, run CLI agents (Cursor, Claude, Copilot), create PRs |
| `Expert` | Domain expert — answers questions using Jira, Confluence, and codebase as context |

### Project Management

| Job | What It Does |
|-----|-------------|
| `JEstimator` | Estimate story points and effort |
| `ScrumMasterDaily` | Generate daily scrum reports |
| `BusinessAnalyticDORGeneration` | Create Definition of Ready documents |

### Utilities

| Job | What It Does |
|-----|-------------|
| `JSRunner` | Run a JavaScript agent directly (no JSON config needed) |
| `KBProcessingJob` | Process and index a knowledge base |
| `SourceCodeTrackerSyncJob` | Sync source code changes with issue tracker |

---

## Part 6: Three Layers of Automation

DMtools has three levels, from low-level to high-level:

```
┌─────────────────────────────────────────┐
│  JS Agents (custom logic you write)     │  ← Your code
│  function action(params) { ... }        │
├─────────────────────────────────────────┤
│  Jobs (23 pre-built workflows)          │  ← Ready to use
│  Teammate, TestCasesGenerator, Expert.. │
├─────────────────────────────────────────┤
│  MCP Tools (152+ atomic API calls)      │  ← Building blocks
│  jira_get_ticket, gemini_ai_chat, ...   │
└─────────────────────────────────────────┘
```

- **MCP Tools** — you never call these directly from CLI; Jobs and Agents use them
- **Jobs** — you configure with a JSON file and run with `dmtools run config.json`
- **JS Agents** — you write JavaScript that calls MCP Tools as functions; run with `JSRunner` or as pre/post actions inside other Jobs

Most users will work at the **Jobs** level — pick a Job, write a config, run it.

---

## Part 7: Practice — Choose & Explore

This is your mini-task. Look at the catalog in Parts 4 and 5 and **pick one capability** that is relevant to your work or interests you.

### Some Ideas

| If you work with... | Try exploring... |
|---------------------|-----------------|
| Jira | `Teammate` — ask AI to draft a config that summarizes stories |
| GitHub PRs | `ReportGenerator` — ask AI to generate a report config for your repo |
| QA / Testing | `TestCasesGenerator` — ask AI to explain the Xray integration |
| Team management | `DevProductivityReport` or `QAProductivityReport` |
| Confluence | `Expert` — ask AI how to set up a Q&A expert over Confluence pages |
| Something else | Pick any Job and ask AI: "Explain [JobName] and show me a minimal config" |

### What To Do

1. **Ask your AI assistant** (the one with the DMtools skill loaded):

   > "Explain the [JobName] job in DMtools. What does it do, what parameters does it need, and show me a minimal config.json example."

2. **Read the AI's response** — it should give you a detailed, accurate answer because it has the full skill documentation.

3. **Ask a follow-up** — dig deeper into something that interests you:
   - "What AI providers can I use with this?"
   - "Can I output to a file instead of a Jira comment?"
   - "Show me a more complex config with [specific feature]"

4. **Save your config** — if the AI generated a useful config, save it:

   ```bash
   mkdir -p work/300-task/agents
   ```

   Save the generated JSON as `work/300-task/agents/my-first-config.json`.

This practice demonstrates the core value of agent skills: **you installed knowledge, and now the AI can generate working configurations for you.**

---

## Part 8: Setting Up Standalone Training (Optional)

If you want to continue exploring DMtools in its own IDE window (recommended for deeper work), set up the training files for standalone launch:

### Copy Training Files

```bash
mkdir -p work/300-task/.training
cp modules/300-dmtools-agent-skill/walkthrough.md work/300-task/.training/
cp modules/300-dmtools-agent-skill/about.md work/300-task/.training/
cp instructions/training-mode.agent.md work/300-task/.training/
```

### Launch in Separate IDE Window

1. Open a new IDE window (File → New Window)
2. Open the `work/300-task/` folder in that window
3. Start a new AI chat and paste:

```
Use the instructions in the .training/ folder to start the training module.
```

The AI in the new window will have access to both the DMtools skill AND the training methodology.

---

## What Happened — Summary

You cloned the DMtools repository, installed a knowledge package (agent skill) into your AI assistant, explored the full catalog of 152+ tools and 23 jobs, and completed a self-chosen exploration task. Your AI can now generate DMtools configurations, explain any tool or job in detail, and guide you through setup — all because you gave it structured knowledge to read.

---

## Success Criteria

- ✅ DMtools repository cloned in `work/300-task/`
- ✅ DMtools skill installed (`.cursor/skills/dmtools/SKILL.md` exists or equivalent for your IDE)
- ✅ AI assistant answers DMtools questions with specifics (not generic responses)
- ✅ You can explain the three parts of a config: `name`, input source, output target
- ✅ You can name at least 5 different Jobs and explain what category they belong to
- ✅ You completed the exploration task — picked a capability and got AI to generate a config

---

## Understanding Check

1. **What is an agent skill?** What does it actually add to your AI assistant?
   > A structured documentation bundle that the AI reads as context. It adds domain knowledge — the AI can now answer questions and generate configurations for that tool.

2. **Where does the DMtools skill get installed?** Is it global or project-local?
   > Project-local only. It goes into `.cursor/skills/dmtools/` (Cursor) or equivalent folder inside your project. It does not affect other projects.

3. **What is the difference between `skill-install.sh` and `install.sh` in DMtools?**
   > `skill-install.sh` installs the knowledge bundle for AI. `install.sh` installs the actual dmtools CLI tool that runs automation. They are independent.

4. **What are the three parts of every dmtools config.json envelope?**
   > `name` (which Job to run), input source (where to get data — could be `inputJql`, `dataSources`, `jsPath`, etc.), and output target (where to put the result — `outputType: comment/field/none` or `outputPath` to a file).

5. **What are the three layers of DMtools automation from low-level to high-level?**
   > MCP Tools (atomic API calls) → Jobs (pre-built workflows using MCP tools) → JS Agents (custom logic you write on top of MCP tools).

6. **Why must the `name` field in config.json exactly match the Java class name?**
   > Because DMtools maps the name string directly to a Java class at runtime: `"TestCasesGenerator"` → `new TestCasesGenerator()`. A typo means "Unknown job" error.

7. **How do you get the latest DMtools documentation and capabilities?**
   > Run `git pull` inside the cloned DMtools repository. The `dmtools-ai-docs/references/` folder contains the living catalog that is auto-generated from the actual build.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No skill directories found" | Create the folder first: `mkdir -p .cursor/skills` (Cursor) then re-run installer |
| AI still doesn't know DMtools after install | Open a completely new chat window — old windows don't reload context |
| `curl: command not found` on Windows | Use Git Bash, not PowerShell. Or use the manual ZIP installation method |
| Skill installed but AI gives wrong answers | Check that `SKILL.md` exists inside the skills folder |
| `git clone` fails | Check your internet connection and that `git` is installed: `git --version` |
| Installed to wrong location | Delete the folder and re-run from your project root (`work/300-task/`) |

---

## Next Steps

You now have the DMtools skill loaded and a mental map of all capabilities. From here:

- **Explore more capabilities** — go back to the catalog (Parts 4-5), pick another Job, and ask the AI to explain it
- **Install the DMtools CLI** — when you're ready to actually run automation (not just explore), install the CLI tool: `curl -fsSL https://raw.githubusercontent.com/IstiN/dmtools/main/install.sh | bash`
- **Create real configurations** — use the AI to generate configs for your actual Jira/ADO projects
- **Read the live docs** — browse `work/300-task/dmtools-ai-docs/references/` for detailed parameter documentation
