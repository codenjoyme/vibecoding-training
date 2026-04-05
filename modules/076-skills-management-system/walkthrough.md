# Advanced Skills Management System — Hands-on Walkthrough

In this walkthrough you will build a complete, working skills management system from scratch. By the end you will have:

- A central skills Git repository with the full `.manifest/` structure
- Two independent project workspaces, each with sparse checkout for their specific skills
- The `skills` CLI installed and working on your machine
- Tested push, pull, and list workflows

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

| Component | Description |
|---|---|
| `skills-repo/` | Central Git repository — single source of truth for all skills |
| `.manifest/` | Folder with `_global.json`, `_agents.json`, per-group configs, sub-configs |
| `skills` CLI | Go binary that automates all Git + sparse checkout operations |
| `project-alpha/` | First project workspace — initialized with alpha group skills |
| `project-beta/` | Second project workspace — initialized with beta group skills |
| `demo/` | Pre-built skills-repo with sample skills — use to skip manual content creation |

All files for this walkthrough are created in a folder of your choice. The `demo/` folder inside this module contains a pre-built `skills-repo` so you can skip writing skill content from scratch — see Part 1 for details.

---

## Part 1: Build the Central Skills Repository

### What we'll do

Create the skills repository — a plain Git repo with a flat directory structure. Each directory is one skill. The `.manifest/` folder contains JSON config files that define which skills belong to which team or project.

> **Shortcut — use the pre-built demo:**
> The `demo/skills-repo/` folder in this module contains ready-made skill files. The setup script **copies** them to `work/076-task/skills-repo/` and initializes it as a Git repository — all actual work happens in `work/076-task/`, never inside `demo/`.
>
> Run from the **workspace root** (the `vibecoding-for-managers/` folder):
>
> ```powershell
> # Windows — from workspace root
> .\modules\076-skills-management-system\demo\setup.ps1
> ```
>
> ```bash
> # macOS/Linux — from workspace root
> bash modules/076-skills-management-system/demo/setup.sh
> ```
>
> The script creates `work/076-task/skills-repo/` with all 6 skills committed. Then skip to Part 3. In Part 4 the `skills init` commands already use `--repo ../skills-repo` — that's the folder the script just created.
>
> Follow Parts 1 and 2 if you want to understand how the repository is structured before using the CLI.

### Step 1 — Create the repository structure

Open a terminal and run:

```bash
# Windows
mkdir work\076-task\skills-repo
cd work\076-task\skills-repo
git init
git config receive.denyCurrentBranch warn

# macOS/Linux
mkdir -p work/076-task/skills-repo
cd work/076-task/skills-repo
git init
git config receive.denyCurrentBranch warn
```

> **Why `receive.denyCurrentBranch warn`?** This allows the CLI to push feature branches to this local repo during testing without errors.

### Step 2 — Create the manifest folder and config files

```bash
mkdir .manifest
```

Create `.manifest/_global.json` — skills applied to every workspace:

```json
{
  "skills": ["creating-instructions", "iterative-prompting"]
}
```

Create `.manifest/_agents.json` — IDE-specific skill bindings:

```json
{
  "copilot": ["agent-copilot"],
  "cursor": [],
  "vscode": []
}
```

Create `.manifest/project-alpha.json` — skills for Project Alpha:

```json
{
  "skills": ["code-review-base", "style-guidelines", "security-guidelines"],
  "sub-configs": ["security"]
}
```

Create `.manifest/project-beta.json` — skills for Project Beta:

```json
{
  "skills": ["code-review-base", "test-writing"],
  "sub-configs": []
}
```

Create `.manifest/security.json` — reusable security sub-config:

```json
{
  "skills": ["security-guidelines"],
  "sub-configs": []
}
```

### Step 3 — Create skill directories

Each skill is a directory with a `SKILL.md` and a `README.md`.

```bash
# Create all skill directories
mkdir code-review-base security-guidelines style-guidelines test-writing creating-instructions iterative-prompting
```

You will populate the `SKILL.md` files in Part 2. First commit the structure:

```bash
git add .
git commit -m "init: central skills repository structure"
```

You should see output like:
```
[main (root-commit) abc1234] init: central skills repository structure
 5 files changed, ...
```

---

## Part 2: Populate Skill Content

### What we'll do

Add `SKILL.md` and `README.md` files to each skill directory. Two of the skills (`creating-instructions` and `iterative-prompting`) are real, actionable skills sourced from this project's instructions folder — they become global skills available to all teams.

> **Note:** If you used the demo shortcut in Part 1, the files below are already in place. Read through this part to understand the content structure, then continue to Part 3.

### Step 4 — Create the global skills

#### `creating-instructions/SKILL.md`

```markdown
# Creating Instructions — SKILL.md

## Purpose
This skill defines how to create, organize, and maintain AI instruction files.

## Core Principles
- IDE-agnostic: instructions are plain Markdown in a dedicated folder
- Single Responsibility: one SDLC workflow piece per instruction file
- Tools-agnostic: works with VSCode Copilot, Cursor, Claude Code, and any LLM agent
- Composable: instructions can reference each other; no monoliths

## How to Create an Instruction
1. Identify the SDLC workflow to capture
2. Create `<name>.agent.md` in `instructions/`
3. Register it in `main.agent.md` catalog with a short description and keywords
4. Add thin IDE adapter wrappers (`.github/prompts/`, `.cursor/rules/`) pointing to the file

## IDE Adapter Wrappers
- VSCode Copilot: `.github/prompts/<name>.prompt.md` referencing `../../instructions/<name>.agent.md`
- Cursor: `.cursor/rules/<name>.mdc` with `globs: ""` and content referencing the instruction file
- Claude Code: `.claude/commands/<name>.md` calling the instruction file

## When to Split a File
Split when a single file exceeds ~700 lines or covers more than one logical workflow.
```

Create `creating-instructions/README.md`:

```markdown
# creating-instructions

**Description:** Guidelines for creating, organizing, and maintaining AI instruction files using the tools-agnostic architecture.

**Owner:** training-team

**Usage context:** Apply when onboarding a new project to the instructions system, or when creating a new instruction file.
```

#### `iterative-prompting/SKILL.md`

```markdown
# Iterative Prompting — SKILL.md

## Purpose
This skill defines the iterative prompt workflow — maintaining a `main.prompt.md` file
as a living specification that grows with your project rather than losing context in chat.

## Core Workflow
- Keep a `main.prompt.md` file in your request folder (version-controlled)
- Add each new request as a new `## UPD[N]` block at the bottom
- After the AI acts, it appends a `### RESULT` block with a brief changelog
- Use `git diff` to give the AI precise context about what changed since last run

## Key Benefits
- No context drift — the file is the full history
- `git diff` replaces "here's what changed since last time"
- Works with any AI agent (Copilot, Cursor, Claude Code, CLI)
- Self-documenting: file is both spec and breadcrumb trail

## When to Use
Use iterative prompting for any multi-step task where you need to:
- Maintain context across multiple AI interactions
- Track what was done and what's still pending
- Reproduce the exact sequence of changes later
```

Create `iterative-prompting/README.md`:

```markdown
# iterative-prompting

**Description:** Workflow pattern for AI-assisted development using a living prompt file with sequential UPD blocks.

**Owner:** training-team

**Usage context:** Apply for any multi-step development task requiring persistent context.
```

### Step 5 — Create project-specific skills

Create `code-review-base/SKILL.md`:

```markdown
# Code Review Base — SKILL.md

## Purpose
Baseline code review guidelines applicable to all projects.

## Review Checklist
- [ ] Function and variable names are clear and descriptive
- [ ] No hardcoded secrets or credentials
- [ ] Error handling is explicit (no silent swallows)
- [ ] Code follows the team's style guidelines
- [ ] New functionality has corresponding tests or test plan

## Anti-patterns to Flag
- Magic numbers without named constants
- Deeply nested conditionals (prefer early return)
- Functions exceeding 50 lines (suggest splitting)
- Missing input validation at system boundaries
```

Create `code-review-base/README.md`:

```markdown
# code-review-base

**Description:** Baseline code review checklist for all projects.

**Owner:** engineering-leads

**Usage context:** Apply during all code review sessions.
```

Create `style-guidelines/SKILL.md`:

```markdown
# Style Guidelines — SKILL.md

## Purpose
Consistent code style across all team repositories.

## Naming Conventions
- Variables: camelCase (JS/TS), snake_case (Python/Go)
- Constants: UPPER_SNAKE_CASE
- Types/Classes: PascalCase
- Files: kebab-case for modules, PascalCase for components

## Formatting
- Max line length: 120 characters
- Indentation: 2 spaces (JS/TS), 4 spaces (Python), tabs (Go)
- Trailing newline required in all files
- No trailing whitespace

## Import Order
1. Standard library imports
2. Third-party imports
3. Internal project imports
(blank line between each group)
```

Create `style-guidelines/README.md`:

```markdown
# style-guidelines

**Description:** Team-wide code style and formatting conventions.

**Owner:** engineering-leads

**Usage context:** Apply to all code generation and review tasks.
```

Create `security-guidelines/SKILL.md`:

```markdown
# Security Guidelines — SKILL.md

## Purpose
Security-first development practices to prevent common vulnerabilities (OWASP Top 10).

## Always Check
- No hardcoded credentials, API keys, or secrets in source code
- User input validated and sanitized at all system boundaries
- SQL queries use parameterized statements (no string concatenation)
- Authentication tokens have appropriate expiry
- Sensitive data not logged

## Dependency Management
- Scan dependencies for CVEs before adding new packages
- Pin dependency versions in lock files
- Keep dependencies updated (monthly review)

## Code Review Security Gate
Block merge if any of the above are violated.
```

Create `security-guidelines/README.md`:

```markdown
# security-guidelines

**Description:** Security-first development practices aligned with OWASP Top 10.

**Owner:** security-team

**Usage context:** Apply to all code with user input, authentication, or external dependencies.
```

Create `test-writing/SKILL.md`:

```markdown
# Test Writing — SKILL.md

## Purpose
Guidelines for writing effective automated tests.

## Test Structure (AAA Pattern)
```
// Arrange — set up inputs and dependencies
// Act — call the function under test
// Assert — verify the output or side effects
```

## What to Test
- Happy path: expected inputs produce expected outputs
- Edge cases: empty input, max values, null/undefined
- Error cases: invalid input, network failure, timeout
- Integration points: external API calls, database queries

## Naming Convention
Tests should read as sentences:
- `it_returns_empty_list_when_no_users_exist`
- `throws_error_when_token_is_expired`

## Coverage Target
80% line coverage minimum; 100% for security-critical paths.
```

Create `test-writing/README.md`:

```markdown
# test-writing

**Description:** Guidelines for writing automated tests using the AAA pattern.

**Owner:** qa-team

**Usage context:** Apply during feature development and code review for test quality.
```

### Step 6 — Commit all skill content

```bash
git add .
git commit -m "feat: add initial skill content for all skills"
```

---

## Part 3: Install the `skills` CLI

### What we'll do

The `skills` CLI is a Go binary located in this module's `tools/skills-cli/` folder. You'll compile it from source and add it to your PATH.

### Before we install

The `skills` CLI is a compiled Go binary. It:
- Has no runtime dependencies (single executable)
- Works on Windows, macOS, and Linux
- Automates all Git + sparse checkout operations

### Step 7 — Install Go

Download and install Go from [https://go.dev/dl/](https://go.dev/dl/).

For this training, Go is installed to `C:\Java\go-<version>` on Windows.

After installation, verify:

```bash
go version
# go version go1.24.x windows/amd64
```

### Step 8 — Compile the CLI

```bash
# Navigate to the CLI source
cd modules/076-skills-management-system/tools/skills-cli

# Windows
go build -o skills.exe .

# macOS/Linux
go build -o skills .
```

### Step 9 — Add to PATH

**Windows option 1 — copy to System32:**
```bash
copy skills.exe C:\Windows\System32\skills.exe
```

**Windows option 2 — add folder to PATH:**
Add `C:\Java\CopipotTraining\vibecoding-for-managers\modules\076-skills-management-system\tools\skills-cli` to your PATH in System Properties → Environment Variables.

**macOS/Linux:**
```bash
sudo cp skills /usr/local/bin/skills
chmod +x /usr/local/bin/skills
```

### Step 10 — Verify installation

```bash
skills help
```

You should see the full command reference. If you see `command not found`, check that the binary is in your PATH.

---

## Part 4: Initialize Project Workspaces

### What we'll do

Use `skills init` to set up two independent project workspaces, each pulling only the skills relevant to their project from the central repository.

### Step 11 — Initialize Project Alpha

```bash
# Return to work/076-task/
mkdir project-alpha
cd project-alpha

skills init --repo ../skills-repo --groups project-alpha
```

Expected output:
```
→ Cloning skills repo from ../skills-repo ...
  ✓ Cloned
→ Resolving skills for groups: project-alpha ...
  ✓ Resolved 5 skill(s): code-review-base, creating-instructions, iterative-prompting, security-guidelines, style-guidelines
→ Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace initialized!
   Repository: ../skills-repo
   Groups:     project-alpha
   Skills:     code-review-base, creating-instructions, iterative-prompting, security-guidelines, style-guidelines
   Location:   .skills/repo/
```

### Step 12 — Verify sparse checkout

```bash
ls .skills/repo/
```

You should see: `.manifest`, `code-review-base`, `creating-instructions`, `iterative-prompting`, `security-guidelines`, `style-guidelines`

You should NOT see: `test-writing` (it belongs to project-beta, not project-alpha)

### Step 13 — Initialize Project Beta

```bash
# Back to work/076-task/
cd ..
mkdir project-beta
cd project-beta

skills init --repo ../skills-repo --groups project-beta
```

Verify that project-beta has `test-writing` but NOT `style-guidelines`:
```bash
ls .skills/repo/
# test-writing present ✅, style-guidelines absent ✅
```

### Step 14 — List skills

```bash
skills list
```

Active skills show with ✅, available-but-not-active show with ○.

---

## Part 5: Contribute a Skill Change

### What we'll do

Edit a skill locally, then push the change for team review using the PR workflow.

### Step 15 — Make a change

In `project-alpha/`, edit the skill:

```bash
# Open in your editor:
.skills/repo/code-review-base/SKILL.md
```

Add a new item to the review checklist — something like:
```markdown
- [ ] No circular dependencies introduced
```

### Step 16 — Push for review

```bash
skills push code-review-base
```

Expected output:
```
→ Creating branch feature/code-review-base-update ...
  ✓ Branch created
→ Staging changes in code-review-base/ ...
  ✓ Changes committed
→ Pushing branch feature/code-review-base-update ...
  ✓ Branch pushed

✅ Skill "code-review-base" pushed for review
   Branch: feature/code-review-base-update
   (local repository — request a review from the skill owner)
```

### Step 17 — Verify the branch in skills-repo

```bash
cd ../skills-repo
git log --oneline --all
# Should show the new feature branch alongside main
```

For a real remote repository (GitHub/GitLab), `skills push` would print a PR creation URL automatically.

### Step 18 — Pull the merged update

Simulate a merge — in skills-repo, accept the change:

```bash
cd ../skills-repo
git merge feature/code-review-base-update
git branch -d feature/code-review-base-update
```

Now in project-alpha workspace, pull the update:

```bash
cd ../project-alpha
skills pull
```

The updated `code-review-base/SKILL.md` is now synchronized.

---

## Part 6: Governance Model (Advisory)

### Skill ownership

Each skill declares an owner in its `README.md`:

```markdown
**Owner:** security-team
```

**Recommended approval rules:**
- Regular skills: 1 approval from skill owner required before merge
- Global skills (`_global.json`): 2 approvals required (affects everyone)
- Sub-configs: 1 approval from sub-config owner

This is enforced through your Git host's branch protection rules, not by the CLI.

### Making skills discoverable

Add a brief description and usage context to every `README.md`. When your skills library grows to 50+ entries, descriptions help developers find the right one instead of creating duplicates.

---

## Part 7: Apply to Your Real Project

### What we'll do

Bring the skills management system into your actual development workflow. You will:

1. Create a personal skills repository with two foundational skills
2. Run `skills init` in your real project directory

This is the moment the system becomes genuinely useful — your AI agent will automatically load the right skills every time it opens your project.

### Step 19 — Identify your real project

Pick a directory on your machine that is a real (or planned) project. Note the absolute path:

- Windows example: `C:\projects\my-app`
- macOS/Linux example: `~/projects/my-app`

If you don't have an existing project yet, create an empty folder as a placeholder:

```bash
# Windows
mkdir C:\projects\my-app

# macOS/Linux
mkdir -p ~/projects/my-app
```

### Step 20 — Create a skills repository next to your project

Create a `my-skills-repo/` directory at the same level as your project:

```bash
# Windows — from C:\projects\
mkdir my-skills-repo
cd my-skills-repo
git init
git config receive.denyCurrentBranch warn
mkdir .manifest

# macOS/Linux — from ~/projects/
mkdir my-skills-repo
cd my-skills-repo
git init
git config receive.denyCurrentBranch warn
mkdir .manifest
```

### Step 21 — Add two foundational skills

**Skill 1: `creating-instructions`** — teaches the AI how your team writes instruction files.

Copy the pre-built skill from the demo:

```powershell
# Windows — from inside my-skills-repo
xcopy /E /I "<path-to-module>\demo\skills-repo\creating-instructions" "creating-instructions\"
```

```bash
# macOS/Linux — from inside my-skills-repo
cp -r <path-to-module>/demo/skills-repo/creating-instructions ./creating-instructions/
```

Or write your own `creating-instructions/SKILL.md` capturing how your team creates instruction files.

**Skill 2: `skills-cli-usage`** — teaches the AI how to help team members use this system.

Create `skills-cli-usage/SKILL.md`:

```markdown
# Skills CLI Usage — SKILL.md

## Purpose
This skill describes how to use the `skills` CLI to manage team AI instructions.

## Quick Reference
- `skills init --repo <path-or-url> --groups <group>` — initialize a workspace
- `skills pull` — get latest skills from the central repository
- `skills push <skill-name>` — propose a change to a skill
- `skills list` — see which skills are active in this workspace

## Repository Location
The central skills repository is at: [insert your repo path or URL here]

## Groups
[insert your group names here, e.g., "backend", "frontend", "devops"]

## Adding New Skills
1. Create a new directory in the skills repo: `mkdir <skill-name>`
2. Add `SKILL.md` and `README.md`
3. Reference it in the appropriate `.manifest/<group>.json`
4. Submit a PR for review
```

Create `skills-cli-usage/README.md`:

```markdown
# skills-cli-usage

**Description:** Guide for team members on using the skills CLI to manage AI instructions.

**Owner:** team-lead

**Usage context:** Apply when team members need to set up or update their workspace.
```

### Step 22 — Configure manifest files

Create `.manifest/_global.json` — these skills load in every workspace:

```json
{"skills": ["creating-instructions", "skills-cli-usage"]}
```

Create `.manifest/my-project.json` — project-specific skills (expand as your library grows):

```json
{"skills": [], "sub-configs": []}
```

### Step 23 — Commit and initialize your project

```bash
# Inside my-skills-repo
git add .
git commit -m "init: team skills repository"

# Navigate to your real project
cd ../my-app

# Initialize skills workspace
skills init --repo ../my-skills-repo --groups my-project
```

Your project now has a `.skills/` folder with the two foundational skills ready for your AI agent.

### What happened

When your AI agent opens this project, it reads `.skills/repo/creating-instructions/SKILL.md` and `.skills/repo/skills-cli-usage/SKILL.md` automatically — giving it:

- Your team's conventions for writing AI instructions
- A self-service guide for setting up the skills system

This is the foundation for your team's shared AI knowledge base. Grow it skill by skill as your team's workflows mature.

### Step 24 — Verify

```bash
skills list
```

You should see both global skills as ✅ active.

---

## Success Criteria

- ✅ `skills-repo/` created as a local Git repository with `.manifest/` folder (or demo initialized via setup script)
- ✅ All 6 skills populated with `SKILL.md` and `README.md` content
- ✅ `skills` CLI compiled and accessible from PATH
- ✅ `project-alpha` initialized — sparse checkout includes alpha skills + globals only
- ✅ `project-beta` initialized — sparse checkout includes beta skills + globals only
- ✅ `skills list` shows correct active/inactive skill counts for each workspace
- ✅ `skills push` created a branch in `skills-repo` 
- ✅ `skills pull` synced the merged change back to the workspace
- ✅ (Part 7) Personal skills repository created and linked to your real project directory

## Understanding Check

**1. Why does the system use a `.manifest/` folder instead of a single `manifest.json` file?**

> Multiple teams editing separate JSON files eliminates merge conflicts. If all teams edit one `manifest.json` simultaneously, every PR causes a conflict.

**2. What are global skills and when are they loaded?**

> Skills defined in `_global.json` — loaded automatically for every workspace regardless of which groups are specified. Used for universal team standards (e.g., code review baseline, iterative prompting workflow).

**3. What happens locally when `skills init` applies sparse checkout?**

> Only the directories for resolved skills (global + group + sub-configs) are checked out locally. All other skill directories are invisible in the file system — they exist in the Git history but don't take up local disk space.

**4. A developer edits a skill locally using `skills push`. What is the correct approval flow before the change reaches all teammates?**

> `skills push` creates a feature branch and pushes it. The skill owner reviews the PR. After ≥1 approval and merge to main, all teammates running `skills pull` get the updated skill.

**5. What is the purpose of `_agents.json` and how does it differ from `_global.json`?**

> `_agents.json` defines IDE/tool-specific skill bindings (which skills a Copilot agent vs. a Cursor agent loads). `_global.json` defines content shown to all developers using any tool. An IDE adapter reads `_agents.json` to inject the right tool-specific skill alongside the global ones.

**6. How does a sub-config differ from a group manifest?**

> Both are `.manifest/<name>.json` files. A group manifest is the entry point referenced in `skills init --groups`. A sub-config is a shared building block that multiple group manifests can reference — it avoids duplicating the same skill list across several group files.

**7. The `skills` CLI is described as tools-agnostic. What does that mean in practice?**

> The SKILL.md files are plain Markdown with no IDE-specific syntax. They work identically whether loaded by VSCode Copilot, Cursor, Claude Code, or a raw API call. IDE-specific behavior (e.g., `applyTo:` patterns) lives in thin adapter wrappers at the IDE level — not in the skill content itself.

## Troubleshooting

**`skills: command not found`**
The binary is not in PATH. Copy it to `C:\Windows\System32\` (Windows) or `/usr/local/bin/` (macOS/Linux), or add its directory to PATH.

**`not a skills workspace — run skills init first`**
You're running a command from a directory that has no `.skills/config.json`. Navigate to your project root (where you ran `skills init`) or run `skills init` first.

**`clone failed: repository not found`**
Check that `--repo` points to a valid Git repository. For local paths, the path must exist and be a Git repo (contains `.git/` folder).

**`sparse checkout failed: ...`**
Requires Git 2.25+. Check with `git --version`. On older systems, update Git first.

**`push failed: refusing to update checked out branch`**
The branch you're pushing to is checked out in the remote. This can happen if you push a branch with the same name as the currently checked-out branch in `skills-repo`. Use `git config receive.denyCurrentBranch warn` in the target repo to allow it.

**Sparse checkout shows extra directories**
Run `git sparse-checkout reapply` inside `.skills/repo/` to force reapply the sparse filter.

## Next Steps

- **Module 077** (coming soon): Evaluate skill quality with automated evals (`evals.json` test cases run against LLM)
- Add new skills to your team repository and propose them via PR
- Configure branch protection rules in your Git host to enforce the governance model
- Use `SKILL.md` from `tools/SKILL.md` to guide your AI agent through any setup questions
