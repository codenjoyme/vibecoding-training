# Skills Management System — SKILL.md (Python Edition)

> **This file is both a human guide and an AI skill.** When an AI agent reads this file, it gains full context on how to set up, operate, and manage the skills management system using the Python CLI. Use it as an onboarding script: share it with your AI agent and ask it to guide you through any step.

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
├── skills.json               ← local workspace configuration
└── instructions/             ← sparse clone of central-skills-repo (has .git)
    ├── .git/
    ├── .manifest/
    │   ├── _global.json      ← tracked: universal skills
    │   ├── project-alpha.json← tracked: group config
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

The Python edition runs from `scripts/main.py` and has no third-party runtime dependencies.

#### Prerequisites

- **Python 3.10+** — use the system installation or a portable distribution
- **git 2.25+** — required for sparse checkout
- A configured Git identity for `skills push` commits

Verify:
```bash
python --version
git --version
```

#### Run from the source checkout

From `tools_py/`:
```powershell
python scripts\main.py help
```
```bash
python3 ./scripts/main.py help
```

On a regular Python installation, the package entry point is also available:
```bash
python -m scripts.main help
```

#### Install as a local command

From `tools_py/`:
```bash
python -m pip install .
skills help
```

For development:
```bash
python -m pip install --editable .
```

The direct launcher is recommended for isolated portable Python distributions because it adds the source directory to `sys.path` and configures UTF-8 output.

---

### Commands

#### `skills init`

Initialize a workspace. Clones the central skills repo, resolves skills for the specified groups, applies sparse checkout.

```bash
skills init --repo <url-or-local-path> --groups <group1>[,<group2>...] [group3 ...]
```

**Flags:**
- `--repo` *(required)* — URL or local filesystem path to the central skills repository
- `--groups` *(optional)* — comma-separated list of group names, or space-separated positional args

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

If `--groups` is omitted, only `_global.json` skills are initialized. If `skills.json` already exists and no `--repo` is supplied, the saved configuration is used to reinitialize the workspace.

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

Active skills (checked out in this workspace) are marked ✅. Inactive skills exist in the repo but aren't part of your groups. Use `--verbose` to show `info.json` metadata or `--json` for a structured array.

```bash
skills list --verbose
skills list --json
```

#### `skills create <skill-name>`

Create `instructions/<skill-name>/SKILL.md` and `info.json` templates, register the skill in `extra_skills`, and extend sparse checkout.

```bash
skills create my-custom-skill
```

#### `skills enable`

Enable a group or an individual skill and immediately reapply sparse checkout:

```bash
skills enable group security
skills enable my-custom-skill
```

Groups are stored in `groups`; individual additions are stored in `extra_skills`. Enabling a previously excluded individual skill removes it from `excluded_skills`.

#### `skills disable`

Disable a group or exclude an individual skill:

```bash
skills disable group security
skills disable security-guidelines
skills disable security-guidelines --force
```

The command refuses to remove uncommitted skill changes unless `--force` is used. Forced disable stashes tracked and untracked changes with `git stash push -u` before sparse checkout is reapplied.

#### `skills init-repo <folder-name>`

Create a central skills repository skeleton with `.manifest/` example files and the `skills-cli/` starter skill. The command prints the follow-up `git init` commands; it does not initialize Git itself.

```bash
skills init-repo my-skills-repo
```

#### `skills ai-help`

Print the compact `SKILL-CLI.md` reference for AI agents:

```bash
skills ai-help
```

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
python --version # must be 3.10+
git --version    # must be 2.25+
python scripts/main.py help
```

If `skills` is not installed: run `python -m pip install .` from `tools_py/`, or use `python scripts/main.py ...` directly.

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
skills init --repo <skills-repo-url-or-path> [--groups <my-group>]
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

## Snapshot Test Framework

The Python test surface is snapshot-only and matches the Go and Node.js test structure:

```text
scripts/test/
├── README.md
├── commands.md
├── run-tests.sh
└── Dockerfile
```

Build and run it from `tools_py/`:

```bash
docker build -t skills-python-smoke -f scripts/test/Dockerfile .
docker run --rm -v ./scripts/test:/app/test skills-python-smoke
git diff scripts/test/commands.md
```

`commands.md` is both the command source and the golden snapshot. The runner replaces only output fences, so headings and command lines remain stable. The Python edition intentionally has no separate unit-test directory.

---

## Differences across Editions

| Aspect | Go edition (`tools/`) | Node.js edition (`tools2/`) | Python edition (`tools_py/`) |
|---|---|---|---|
| Runtime | None (compiled binary) | Node.js 18+ required | Python 3.10+ required |
| Installation | Copy binary to PATH | `npm install -g git+<url>` | `python -m pip install .` or direct launcher |
| Build required | Only if no pre-built binary | Never (dist/ is committed) | No build step |
| CLI interface | Identical | Identical | Identical |
| Config format | Identical | Identical | Identical |
| Manifest format | Identical | Identical | Identical |
| Git operations | `os/exec` → system `git` | `child_process.execSync` → system `git` | `subprocess.run` → system `git` |
| Platform | Windows/macOS/Linux | Windows/macOS/Linux | Windows/macOS/Linux |

All editions are fully interoperable — the `instructions/` folder and `.manifest/` configs are 100% compatible. Teams can mix the CLIs.

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
