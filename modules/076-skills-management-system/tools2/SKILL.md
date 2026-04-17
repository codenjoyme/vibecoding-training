# Skills Management System — SKILL.md (Node.js/TypeScript Edition)

> **This file is both a human guide and an AI skill.** When an AI agent reads this file, it gains full context on how to set up, operate, and manage the skills management system using the Node.js/TypeScript CLI. Use it as an onboarding script: share it with your AI agent and ask it to guide you through any step.

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
│   └── info.json             ← owner, description metadata
├── security-guidelines/
│   ├── SKILL.md
│   └── info.json
└── ...

project-workspace/            ← a developer's local project
└── instructions/             ← sparse clone of central-skills-repo (has .git)
    ├── .git/
    ├── .gitignore            ← ignores .manifest/config.json
    ├── .manifest/
    │   ├── _global.json      ← tracked: universal skills
    │   ├── project-alpha.json← tracked: group config
    │   └── config.json       ← LOCAL only (gitignored)
    ├── code-review-base/     ← included (in project's groups)
    └── security-guidelines/  ← included
    # style-guidelines/ NOT here (not in this project's groups)
```

### How the AI agent reads skills

Once `skills init` runs, your AI agent can discover and load skill content from:
```
instructions/<skill-name>/SKILL.md
```

No manual prompt assembly needed. The agent scans the local workspace and loads relevant SKILL.md files as context.

---

## Manifest Files Reference

### `_global.json`

Skills applied to **every** workspace, regardless of groups.

```json
{
  "skills": ["creating-instructions", "iterative-prompting"]
}
```

### `_agents.json`

IDE/tool-specific skill bindings.

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

Reusable thematic group — reference it from multiple group manifests.

```json
{
  "skills": ["security-guidelines", "owasp-top10"],
  "sub-configs": []
}
```

**Resolution order:** `_global.json` skills + group skills + sub-config skills (deduped, sorted).

---

## CLI Reference

### Installation

The `skills` CLI is a Node.js package installed globally via npm. No Go, no compilation needed.

#### Prerequisites

- **Node.js 18+** — download from [https://nodejs.org/](https://nodejs.org/)
- **npm** — bundled with Node.js
- **git 2.25+** — required for sparse checkout

Verify:
```bash
node --version   # v18.x.x or higher
npm --version    # 9.x.x or higher
git --version    # 2.25 or higher
```

#### Install from a private Git repository

```bash
npm install -g --install-links git+https://github.com/codenjoyme/apm-lite.git
```

Or via SSH:
```bash
npm install -g --install-links git+ssh://git@github.com/codenjoyme/apm-lite.git
```

Or from a local folder (for development/testing):
```bash
npm install -g --install-links ./tools2
```

After installation, `skills` is available globally:
```bash
skills help
```

#### Uninstall

```bash
npm uninstall -g skills-cli
```

#### How it works

The repository includes pre-built `dist/` files, so no compilation step is needed during install. `npm install -g` links `dist/index.js` as the `skills` binary globally. No manual PATH changes required.

> **After making changes to source code (`src/`)**, always rebuild before testing or committing:
> ```bash
> npm run build
> ```
> This compiles TypeScript into `dist/`. The `dist/` folder is committed to the repo so that `npm install -g` works without a build step for end users.

> **Note (Windows):** The `--install-links` flag is always required. Without it, npm creates a junction (symlink) to the source directory instead of copying files. If you later delete or move the source, you get `MODULE_NOT_FOUND` errors.

---

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
- `instructions/` — sparse clone of the central repo (contains `.git`)
- `skills.json` — workspace configuration in project root

#### `skills pull`

Update local skills from the remote repository.

```bash
skills pull
```

Runs `git pull` in `instructions/`. Always checks out the default branch first to avoid tracking issues.

#### `skills push <skill-name>`

Propose a change to a skill via a branch and Pull Request.

```bash
skills push code-review-base
```

**What it does:**
1. Creates branch `feature/<skill-name>-update` in `instructions/`
2. Stages all changes in `instructions/<skill-name>/`
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

---

## Skill Directory Structure

Each skill in the central repository must have:

```
<skill-name>/
├── SKILL.md     ← required: instruction content (plain Markdown, AI-readable)
└── info.json    ← required: metadata (owner, description)
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

### info.json required fields

```json
{
  "description": "One sentence explaining what this skill does.",
  "owner": "team-or-person@example.com"
}
```

---

## AI Agent Setup Guide

When an AI agent reads this SKILL.md, it can perform the following setup steps on behalf of a user (including beginners):

### Step 1 — Check prerequisites
```bash
node --version   # must be 18+
git --version    # must be 2.25+
skills help      # must show help (npm package installed)
```

If `skills` is not installed: run `npm install -g git+<repo-url>` (see Installation above).

### Step 2 — Create skills repository (first time, for team admin)
```bash
mkdir my-skills-repo && cd my-skills-repo
git init
git config receive.denyCurrentBranch warn

mkdir .manifest
# Create _global.json, _agents.json, group configs
# Create skill directories with SKILL.md + README.md
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
ls instructions/
```

### Step 5 — Working with skills daily
```bash
skills pull                    # get latest
# edit instructions/<skill>/SKILL.md
skills push <skill-name>       # propose change via PR
```

---

## Differences from the Go Edition

| Aspect | Go edition (`tools/`) | Node.js edition (`tools2/`) |
|---|---|---|
| Runtime | None (compiled binary) | Node.js 18+ required |
| Installation | Copy binary to PATH | `npm install -g git+<url>` |
| Build required | Only if no pre-built binary | Never (dist/ is committed) |
| CLI interface | Identical | Identical |
| Config format | Identical | Identical |
| Manifest format | Identical | Identical |
| Git operations | `os/exec` → system `git` | `child_process.execSync` → system `git` |
| Platform | Windows/macOS/Linux | Windows/macOS/Linux |

Both editions are fully interoperable — the `instructions/` folder and `.manifest/` configs are 100% compatible. Teams can mix both CLIs.

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
Load all SKILL.md files from `instructions/` as context for this workspace.
```

**Cursor:** `.cursor/rules/skills-context.mdc`
```
---
description: Load team skills from instructions/
alwaysApply: true
---
Read all SKILL.md files in instructions/**/ and apply them as context.
```

**Claude Code:** `.claude/CLAUDE.md` — reference this SKILL.md file directly.

---

## evals.json Preview *(coming soon)*

In a future release, each skill can have an `evals.json` file with automated test cases for validating skill behaviour.
