# Installing Third-Party Agent Skills (DMtools) - Hands-on Walkthrough

In this module you will install the DMtools agent skill into your AI IDE. A skill is a knowledge package — once installed, your AI assistant knows everything about DMtools and can guide you through configuration, automation, and code generation without you having to copy-paste documentation.

By the end, you will understand the fundamental DMtools architecture and be ready for all 300-series modules.

## Prerequisites

- Cursor or VS Code with GitHub Copilot installed
- A project folder open in your IDE (any folder works — use `./workspace/hello-genai/`)
- Git Bash installed (Windows) or Terminal (macOS/Linux)
- Completed Module 090: AI Skills - Context, Tools & Memory

---

## What We'll Install

### The DMtools Agent Skill

This is **not** an application — it is a documentation bundle that your AI assistant reads before answering questions. When installed, the skill:

- Adds ~500KB of structured knowledge about DMtools to your project
- Tells your AI assistant what DMtools can do, how to configure it, and what every tool and job does
- Is automatically picked up by Cursor, Claude, or any Agent Skills-compatible IDE
- Lives in your project folder (`.cursor/skills/dmtools`, `.claude/skills/dmtools`) — not globally

Think of it like the difference between asking a colleague who has never heard of a tool vs. one who has read the full manual.

**Size**: ~500KB  
**Time to install**: under 30 seconds  
**What it does NOT do**: it does not install the dmtools CLI or run any code

---

## Steps

### 1. Open your project folder

Open your IDE (Cursor or VS Code) with a project folder. Any folder works for this exercise.

- Windows: `c:/workspace/hello-genai/`
- macOS/Linux: `~/workspace/hello-genai/`

### 2. Open a terminal inside your IDE

Use the terminal integrated in your IDE. On Windows, make sure to select **Git Bash** (not PowerShell) from the terminal dropdown.

> **Why Git Bash on Windows?** The skill installer is a bash script. PowerShell cannot run it directly. Git Bash gives you a bash environment without needing WSL.

### 3. Understanding what will happen

Before running the installer, here is what it does step by step:

1. Detects which AI skill folders exist in your project (`.cursor/skills`, `.claude/skills`, `.codex/skills`)
2. Downloads the latest DMtools skill ZIP from GitHub releases
3. Extracts it into all detected skill folders
4. Prints a confirmation for each installed location

No system-level changes are made. Nothing is installed globally.

### 4. Run the installer

**macOS / Linux / Windows Git Bash:**
```bash
curl -fsSL https://github.com/IstiN/dmtools/releases/download/v1.7.133/skill-install.sh | bash
```

You should see output like:
```
Found skill directories:
  1. .cursor/skills
  2. .claude/skills

Non-interactive mode detected, installing to all detected locations
✓ Installed to .cursor/skills/dmtools
✓ Installed to .claude/skills/dmtools
```

> **If you see "No skill directories found"**: This means your project does not yet have `.cursor/` or `.claude/` folders. Create one first:
> ```bash
> mkdir -p .cursor/skills
> ```
> Then run the installer again.

### 5. What just happened

After running the installer, verify the skill was created:

```bash
ls .cursor/skills/dmtools/
```

You should see:
```
SKILL.md    references/
```

- `SKILL.md` — the main skill definition file your AI reads automatically
- `references/` — detailed documentation organized by category (mcp-tools, jobs, agents, etc.)

This is exactly what your AI assistant will use as context when you ask about DMtools.

### 6. Manual installation (Windows PowerShell alternative)

If you cannot use Git Bash, you can install manually:

1. Download the latest skill ZIP from [github.com/IstiN/dmtools/releases](https://github.com/IstiN/dmtools/releases) — look for `dmtools-skill-v*.zip`
2. Extract it to your project folder into `.cursor/skills/dmtools/` (or `.claude/skills/dmtools/`)
3. Verify the folder contains `SKILL.md`

### 7. First conversation using the skill

Restart your AI assistant chat (to pick up the new skill context), then ask:

> "What is DMtools and what can I do with it?"

Your AI should now give a structured answer about:
- 152+ MCP tools across 16 integrations
- 23 ready-made jobs
- The `dmtools.env + config.json + dmtools run` pattern

If the answer looks generic or the AI doesn't know DMtools — the skill may not be loaded yet. Try opening a new chat window.

### 8. Understanding the core architecture

Ask your AI assistant this follow-up question:

> "Show me the simplest possible dmtools config.json and explain what each field does"

The AI should explain the fundamental pattern that all DMtools modules share:

```json
{
  "name": "JobName",
  "params": {
    "...where to get data...",
    "...what to do...",
    "...where to put result..."
  }
}
```

- **`name`** — which Job to run (maps directly to a Java class — never change the spelling)
- **input source** — depends on the Job type:
  - `inputJql` — Jira Query Language filter, used when source is Jira tickets
  - `dataSources` — array of GitHub/GitLab/CSV/Figma sources, used by `ReportGenerator`
  - `jsPath` — path to a JavaScript file, used by `JSRunner`
- **output target** — where the result goes:
  - `outputType: "comment"` — post as a comment on the ticket
  - `outputType: "field"` — update a field on the ticket
  - `outputPath: "reports/output"` — save as HTML/JSON files
  - `outputType: "none"` — dry run, no changes

Two concrete examples of the same pattern with different input sources:

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

The Job name changes, the input source changes, the output target changes — but the envelope `{ "name": ..., "params": {...} }` is always the same. That is the only thing you need to memorize.

### 9. Ask about what's available

Ask your AI:

> "List the main job categories in DMtools and give me one example use case for each"

This gives you a mental map of everything you can automate before going into specific modules.

---

## What Happened — Summary

You installed a knowledge package into your AI assistant. Your IDE now has a `.cursor/skills/dmtools/` folder containing structured documentation that the AI reads as context. No dmtools CLI was installed yet — that comes in subsequent modules when you actually want to run automation.

---

## Success Criteria

- ✅ `.cursor/skills/dmtools/SKILL.md` exists in your project folder
- ✅ Your AI assistant can answer "what is dmtools?" with specifics (not a generic answer)
- ✅ You can explain the three parts of a dmtools config: `name`, `inputJql`, `outputType`
- ✅ You understand the difference between a skill (knowledge) and a CLI tool (executable)

---

## Understanding Check

1. **What is an agent skill?** What does it actually add to your AI assistant?
   > A structured documentation bundle that the AI reads as context. It adds domain knowledge — the AI can now answer questions and generate configurations for that tool.

2. **Where does the DMtools skill get installed?** Is it global or project-local?
   > Project-local only. It goes into `.cursor/skills/dmtools/` inside your project folder. It does not affect other projects.

3. **After installing the skill, what can your AI do that it couldn't before?**
   > It can explain DMtools configuration, generate correct JSON configs, describe all 152+ tools, and guide setup — without you needing to look at documentation.

4. **What is the difference between `skill-install.sh` and `install.sh` in DMtools?**
   > `skill-install.sh` installs the knowledge bundle for AI. `install.sh` installs the actual dmtools CLI tool that runs automation. They are independent.

5. **What are the three parts of every dmtools config.json envelope?**
   > `name` (which Job to run), input source (where to get data — could be `inputJql`, `dataSources`, `jsPath`, etc.), and output target (where to put the result — `outputType: comment/field/none` or `outputPath` to a file).

6. **What are the three layers of DMtools automation from low-level to high-level?**
   > MCP Tools (atomic API calls) → Jobs (pre-built workflows using MCP tools) → JS Agents (custom logic you write on top of MCP tools).

7. **On Windows, why do you need Git Bash instead of PowerShell to run the installer?**
   > The installer is a bash shell script. PowerShell cannot interpret bash syntax. Git Bash provides a bash runtime on Windows.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No skill directories found" | Create `.cursor/skills/` first: `mkdir -p .cursor/skills`, then re-run |
| AI still doesn't know DMtools after install | Open a completely new chat window — old windows don't reload context |
| `curl: command not found` on Windows | Use Git Bash, not PowerShell. Or use the manual ZIP installation method |
| Skill installed but AI gives wrong answers | Check that `SKILL.md` exists inside `.cursor/skills/dmtools/` |
| Installed to wrong location | Delete the folder and re-run from your actual project root |

---

## Next Steps

You now have the DMtools skill loaded and understand the core architecture. The next modules in the 300 series each focus on one category of DMtools jobs:

- **Module 305** (coming soon): AI Teammate on Tickets — configure `Teammate` to process Jira/ADO tickets with AI
- **Module 310** (coming soon): Automated Test Case Generation — use `TestCasesGenerator` to create Xray test cases from stories
- **Module 315** (coming soon): Productivity Reports — generate HTML team reports from Jira + GitHub PRs
