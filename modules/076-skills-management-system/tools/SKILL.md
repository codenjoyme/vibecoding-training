# Skills Management System — SKILL.md

> **This file is both a human guide and an AI skill.** When an AI agent reads this file, it gains full context on how to set up, operate, and manage the skills management system. Use it as an onboarding script: share it with your AI agent and ask it to guide you through any step.

---

## What This System Does

The skills management system solves a specific scaling problem: as a team accumulates AI instructions, a single shared folder breaks down — merge conflicts, everyone seeing all instructions, no ownership model.

This system provides:

| Feature | Implementation |
|---|---|
| Single source of truth | Central Git repository for all skills |
| Per-project selection | `.manifest/<group>.json` defines which skills a project uses |
| No duplication | Sparse checkout — each workspace has only what it needs |
| Team contribution workflow | PR-based: branch → review → merge → everyone updates |
| Automation | `skills` CLI handles all Git operations |

---

## Architecture Overview

```
central-skills-repo/          ← shared Git repo (one per organization)
├── .manifest/
│   ├── _global.json          ← skills for everyone (sorted first)
│   ├── _agents.json          ← IDE/tool-specific bindings (sorted first)
│   ├── <group-name>.json     ← per-project or per-team skills
│   └── security.json         ← example sub-config (shared thematic group)
├── code-review-base/
│   ├── SKILL.md              ← plain Markdown, IDE-agnostic instruction content
│   └── README.md             ← owner, description, usage context
├── security-guidelines/
│   ├── SKILL.md
│   └── README.md
└── ...

project-workspace/            ← a developer's local project
└── .skills/
    ├── config.json           ← saved repo URL + groups + resolved skills
    └── repo/                 ← sparse clone of central-skills-repo
        ├── .manifest/        ← always included
        ├── code-review-base/ ← included (in project's groups)
        └── security-guidelines/ ← included
        # style-guidelines/ NOT here (not in this project's groups)
```

### How the AI agent reads skills

Once `skills init` runs, your AI agent can discover and load skill content from:
```
.skills/repo/<skill-name>/SKILL.md
```

No manual prompt assembly needed. The agent scans the local workspace and loads relevant SKILL.md files as context. The IDE/agent runtime handles composition.

---

## Manifest Files Reference

### `_global.json`

Skills applied to **every** workspace, regardless of groups. Safe for universal team standards.

```json
{
  "skills": ["creating-instructions", "iterative-prompting"]
}
```

### `_agents.json`

IDE/tool-specific skill bindings. Each key is a tool identifier; value is the list of skill directories to load for that tool.

```json
{
  "copilot": ["agent-copilot"],
  "cursor": [],
  "vscode": []
}
```

### `<group-name>.json`

Per-project or per-team skill selection. Can reference sub-configs.

```json
{
  "skills": ["code-review-base", "style-guidelines"],
  "sub-configs": ["security"]
}
```

### Sub-config (e.g., `security.json`)

Reusable thematic group — reference it from multiple group manifests without duplicating the skill list.

```json
{
  "skills": ["security-guidelines", "owasp-top10"],
  "sub-configs": []
}
```

**Resolution order:** `_global.json` skills + group skills + sub-config skills (deduped).

---

## CLI Reference

### Installation

The `skills` CLI is a single compiled Go binary — no runtime dependencies.

**Step 1 — Check if a compiled binary already exists:**

```powershell
# Windows
Get-ChildItem tools\skills-cli\
```
```bash
# macOS/Linux
ls tools/skills-cli/
```

- **`skills.exe` / `skills` present** → binary is ready, go to Option A
- **Only source files** (`main.go`, `go.mod`, `cmd/`, `internal/`) → need to build, go to Option B

---

**Option A — Binary exists (use it directly):**

1. Add `tools/skills-cli/` to PATH:
   - **Windows:** System Properties → Environment Variables → User variables → `Path` → Edit → New → add absolute path to `tools/skills-cli/`
   - **macOS/Linux:** `export PATH=$PATH:<absolute-path>/tools/skills-cli` (add to `~/.bashrc` / `~/.zshrc`)
2. Restart the terminal
3. Verify: `skills help`

> **To rebuild at any time:**
> ```bash
> cd tools/skills-cli
> go build -o skills.exe .   # Windows
> go build -o skills .        # macOS/Linux
> ```
> Requires Go — see Option B.

---

**Option B — No binary, build from source:**

Go is installed into `tools/.golang/` — self-contained, right next to this SKILL.md, no global installation required.

1. **Install Go into `tools/.golang/`:**
   - Windows: download `go1.24.x.windows-amd64.zip` from [https://go.dev/dl/](https://go.dev/dl/), extract so that `tools\.golang\bin\go.exe` exists
   - macOS: `brew install go` or download `.pkg`
   - Linux: `tar -C tools/ -xzf go1.24.x.linux-amd64.tar.gz && mv tools/go tools/.golang`

2. **Add Go to PATH for the session:**
   ```powershell
   # Windows
   $env:PATH = "<absolute-path>\tools\.golang\bin;" + $env:PATH
   ```
   ```bash
   # macOS/Linux (if extracted to tools/.golang/)
   export PATH=$PATH:<absolute-path>/tools/.golang/bin
   ```

3. **Verify Go:**
   ```bash
   go version
   # go version go1.24.x ...
   ```

4. **Build the CLI:**
   ```bash
   cd tools/skills-cli
   go build -o skills.exe .   # Windows
   go build -o skills .        # macOS/Linux
   ```

5. **Add `tools/skills-cli/` to PATH** (see Option A step 1)

6. **Verify:** `skills help`

### Commands

#### `skills init`

Initialize a workspace. Clones the central skills repo, resolves skills for the specified groups, applies sparse checkout.

```bash
skills init --repo <url-or-local-path> --groups <group1>[,<group2>...] [group3 ...]
```

**Flags:**
- `--repo` *(required)* — URL or local filesystem path to the central skills repository
- `--groups` *(required)* — comma-separated list of group names, or space-separated positional args

**Examples:**
```bash
# Remote GitHub repo
skills init --repo https://github.com/org/skills-repo --groups backend

# Local path (for testing)
skills init --repo ../skills-repo --groups backend,security

# Multiple groups, positional style
skills init --repo ../skills-repo backend security
```

**Creates:**
- `.skills/repo/` — sparse clone of the central repo
- `.skills/config.json` — workspace configuration

#### `skills pull`

Update local skills from the remote repository.

```bash
skills pull
```

Runs `git pull` in `.skills/repo/`. Re-applies sparse checkout if configuration has changed.

#### `skills push <skill-name>`

Propose a change to a skill via a branch and Pull Request.

```bash
skills push code-review-base
```

**What it does:**
1. Creates branch `feature/<skill-name>-update` in `.skills/repo/`
2. Stages all changes in `.skills/repo/<skill-name>/`
3. Commits with message `feat(<skill-name>): update skill instructions`
4. Pushes to origin
5. Prints PR creation URL (for GitHub/GitLab remotes)

#### `skills list`

List all skills in the repository with active/inactive status.

```bash
skills list
```

Active skills (checked out in this workspace) are marked ✅. Inactive skills exist in the repo but aren't part of your groups.

#### `skills help`

Show usage information and all available commands.

```bash
skills help
```

#### `skills eval <skill-name>` *(coming soon)*

Run automated evaluation test cases for a skill against an LLM.

```bash
skills eval code-review-base
```

> **Note:** This command is not yet implemented. It will be introduced in a future module alongside `evals.json` test case format.

---

## Skill Directory Structure

Each skill in the central repository must have:

```
<skill-name>/
├── SKILL.md     ← required: instruction content (plain Markdown, AI-readable)
└── README.md    ← required: metadata (owner, description, usage context)
```

Optional:
```
<skill-name>/
└── evals.json   ← coming soon: test cases for automated skill validation
```

### SKILL.md conventions

- Write in plain English, clear and direct
- No IDE-specific syntax (`applyTo:`, `globs:`, frontmatter for Cursor/Copilot)
- Structure with `## Purpose`, `## When to Use`, `## How to Apply` sections
- Cross-references to other skills are allowed: "See also: `code-review-base`"
- Target reading time: 2–5 minutes per skill

### README.md required fields

```markdown
# <skill-name>

**Description:** One sentence explaining what this skill does.

**Owner:** <team-or-person>

**Usage context:** When to apply this skill.
```

---

## AI Agent Setup Guide

When an AI agent reads this SKILL.md, it can perform the following setup steps on behalf of a user (including beginners):

### Step 1 — Check prerequisites
```bash
git --version    # must be 2.25+
skills help      # must show help (binary installed)
```

If `skills` is not installed: compile from `tools/skills-cli/` (requires Go 1.21+).

### Step 2 — Create skills repository (first time, for team admin)
```bash
mkdir my-skills-repo && cd my-skills-repo
git init
git config receive.denyCurrentBranch warn

mkdir .manifest
# Create _global.json, _agents.json, group configs
# Create skill directories
git add . && git commit -m "init: skills repository"
```

### Step 3 — Initialize a project workspace
```bash
cd /path/to/my-project
skills init --repo <skills-repo-url-or-path> --groups <my-group>
```

### Step 4 — Verify
```bash
skills list
ls .skills/repo/
```

### Step 5 — Working with skills daily
```bash
skills pull                    # get latest
# edit .skills/repo/<skill>/SKILL.md
skills push <skill-name>       # propose change via PR
```

---

## Governance Recommendations

> These are advisory guidelines. Enforcement is through your Git host's branch protection, not the CLI.

| Skill type | Approvals required | Reviewer |
|---|---|---|
| Regular skill | 1 | Skill owner (from README.md) |
| Global skill (`_global.json`) | 2 | Any 2 senior team members |
| Sub-config | 1 | Sub-config owner |

**PR best practices:**
- One skill change per PR (smaller = easier review)
- Include a brief description of why the change improves behavior
- Test the skill change locally before pushing

---

## Adding the System to a New IDE

Since SKILL.md files are plain Markdown, they work with any IDE. Add a thin adapter wrapper:

**VSCode (Copilot):** `.github/prompts/skills-context.prompt.md`
```markdown
Load all SKILL.md files from `.skills/repo/` as context for this workspace.
```

**Cursor:** `.cursor/rules/skills-context.mdc`
```
---
description: Load team skills from .skills/repo/
alwaysApply: true
---
Read all SKILL.md files in .skills/repo/**/ and apply them as context.
```

**Claude Code:** `.claude/CLAUDE.md` — reference this SKILL.md file directly.

---

## evals.json Preview *(coming soon)*

In a future release, each skill can have an `evals.json` file:

```json
[
  {
    "input": "Review this function: def process(data): return data",
    "expected_contains": ["missing error handling", "type hints"]
  },
  {
    "input": "SELECT * FROM users WHERE id = '" + user_id + "'",
    "expected_contains": ["SQL injection", "parameterized query"]
  }
]
```

The `skills eval <skill-name>` command will run these cases against an LLM to validate skill quality automatically.
