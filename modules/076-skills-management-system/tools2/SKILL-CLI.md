# Skills CLI - Quick Reference for AI Agents

Skills CLI manages shared AI skills across teams.
Each skill is a self-contained folder with `SKILL.md` (instructions for the AI agent) and `info.json` (metadata).
Skills live in a central Git repository and are distributed to project workspaces via sparse checkout.

## Core Concepts

- **Skill**: a folder (`<skill-name>/SKILL.md` + `info.json`) with instructions an AI agent can follow.
- **Group**: a named collection of skills defined in `.manifest/<group>.json`. Teams assign groups to projects.
- **Manifest**: JSON files in `.manifest/` that define which skills belong to which groups.
- **Workspace config** (`skills.json`): project-level file tracking repo URL, active groups, extra/excluded skills.
- **Sparse checkout**: only the skills your project needs are checked out locally in `instructions/`.

## Commands

```
skills init --repo <url|path> --groups <g1>[,<g2>...]
```
Initialize workspace: clones the skills repo into `instructions/`, reads manifests,
resolves skills for the given groups, and applies sparse checkout.
- `--repo` (required): Git URL or local path to the central skills repository.
- `--groups` (optional): comma-separated group names. Also accepts positional args: `skills init --repo <url> backend security`.
- If `skills.json` already exists and no flags given, re-runs resolution from existing config.

```
skills pull
```
Pulls latest changes from the remote skills repository (`git pull` inside `instructions/`).
Requires initialized workspace (`skills.json` must exist).

```
skills push <skill-name>
```
Proposes local changes to a skill via a feature branch:
1. Creates branch `feature/<skill-name>-update`
2. Stages changes in `instructions/<skill-name>/`
3. Commits with a conventional message
4. Pushes branch to origin
5. Prints the Pull Request URL (GitHub/GitLab)

```
skills list [--verbose] [--json]
```
Lists all skills in the repository. Active skills (in current groups) marked with checkmark.
- `--verbose`: shows description and owner from `info.json`.
- `--json`: outputs as JSON array with `name`, `active`, `description`, `owner` fields.

```
skills create <skill-name>
```
Creates a new skill folder in `instructions/` with template `SKILL.md` and `info.json`.
Does not add the skill to any group manifest (that's a manual step in the repo).

```
skills enable group <name>
```
Adds a group to the `groups` array in `skills.json`.
Sparse checkout is re-applied automatically — skill folders appear immediately.

```
skills enable <skill-name>
```
Adds an individual skill to `extra_skills` in `skills.json`.
If the skill was previously excluded, removes it from `excluded_skills` instead.
Sparse checkout is re-applied automatically.

```
skills disable [--force] group <name>
```
Removes a group from the `groups` array in `skills.json`.
If any skills being removed have uncommitted local changes, the command refuses.
Use `--force` to override — changes are stashed automatically (`git stash list` to review).
Sparse checkout is re-applied automatically — skill folders are removed immediately.

```
skills disable [--force] <skill-name>
```
Adds a skill to `excluded_skills` in `skills.json` (removes from `extra_skills` if present).
Excluded skills are filtered out during resolution even if they appear in group manifests.
If the skill has uncommitted local changes, the command refuses.
Use `--force` to override — changes are stashed automatically.
Sparse checkout is re-applied automatically.

```
skills init-repo <folder-name>
```
Scaffolds a new skills repository with example manifests, skills, and folder structure.
Use this to bootstrap a central skills repo from scratch.

```
skills ai-help
```
Shows this reference (reads SKILL-CLI.md or prints inline fallback).

```
skills help
```
Shows general CLI help with command list and examples.

## Typical Workflow

1. `skills init --repo <url> --groups <group>` — set up workspace
2. `skills list --verbose` — see what's available
3. Edit `instructions/<skill>/SKILL.md`
4. `skills push <skill>` — propose changes via PR
5. `skills pull` — get latest updates

## Architecture and Motivation

- IDE-agnostic architecture allows teams to use different IDE/Plugins while sharing same skill base.
- Team alignment on LLM model choice is more critical than IDE choice — IDE switching is less disruptive.
- Skills are self-contained folders with `SKILL.md` describing SDLC workflows without platform-specific adapters like `alwaysApply: true` or `mode: agent`.
- Following Single Responsibility Principle (SRP) — one SDLC workflow piece per skill.
  + Recommended soft limit: ~700 lines per `SKILL.md`. Exceeding this is a signal to split.
  + Complex skills can reference other skills — composability over monoliths.
  + Terminology hint: large multi-step workflows → "agents", small focused actions → "skills". Naming may vary by author.
- `main.agent.md` serves as catalog of all skills with brief descriptions — when asked about (what to do), follow this skill (with file path).
  + Each entry has optional sub-fields after `+`: **Keywords** (trigger words), **Target** (file glob pattern), **Exceptions** (edge cases).
  + When adding new skill to catalog, fill in at least Keywords to help model match user requests to skills.
- Platform-specific entry points (`.github/copilot-instructions.md` for Copilot, `.cursor/rules/*.mdc` for Cursor, `.claude/CLAUDE.md` for Claude Code) reference `main.agent.md` to load with every prompt.
- Optionally, `AGENTS.md` in project root with same content as entry point — universal fallback recognized by Claude, Copilot, Cursor agents.
  + Important when `.github/`, `.cursor/`, or `.claude/` are not committed — without them other non-IDE agents have no entry point to discover `instructions/` folder.
  + Decision is up to the team.
- `instructions/` can live in the project repo or be extracted into a separate sub-repository (git submodule, etc.).
  + `.github/`, `.cursor/` stay local per team member's IDE choice — not committed.
  + For cloud agents — add `AGENTS.md` in project root as described above.
  + Or commit skills together with the project — simpler, fewer moving parts.
  + Each team decides what fits their workflow.
- Why tool-agnostic over native systems (GitHub `.instructions.md`, Cursor `.mdc`):
  + Native formats are incompatible: Copilot's `applyTo` globs, `excludeAgent` fields, Cursor's `alwaysApply`, `globs`, `description` frontmatter, Claude Code's `paths:` frontmatter — none of these are portable.
  + Vendor lock-in: rewriting dozens of skill files when switching IDE or when vendor changes format is wasted effort.
  + This approach: one source of truth in `instructions/`, thin adapter wrappers per IDE — only wrappers change on IDE switch.
  + Pure markdown skills work with any LLM agent (CLI, API, CI pipelines) — not tied to IDE runtime at all.
  + Team members on different IDEs (Copilot, Cursor, Windsurf, etc.) share identical workflow knowledge without translation.
- Architectural advantage — separation of concerns:
  + Skills = **what to do** (platform-agnostic SDLC knowledge).
  + Wrappers = **how to load** (platform-specific glue, 2–3 lines each).
  + Catalog (`main.agent.md`) = **when to use** (routing by task description).
  + Adding a new IDE means only adding a new set of thin wrappers — zero changes to skill content.
- Hybrid approach is always welcome: use full power of your IDE's native features (`applyTo`, `globs`, `excludeAgent`, etc.) in wrappers that reference files in `instructions/`. Just keep in mind — those IDE-specific features only work for users of that particular IDE.
- Place skills where they make sense for your project — then build a tree of `main.agent.md` nodes from root to leaves:
  + Hierarchical layout: `instructions/backend/main.agent.md`, `instructions/frontend/main.agent.md` — each sub-catalog follows same structure, root `main.agent.md` links to them.
  + Alternative: co-located layout — `backend/instructions/*`, `frontend/instructions/*` — but then IDE entry point must reference multiple roots, which adds complexity.
  + Key idea: tree-shaped chain from IDE entry point → root `main.agent.md` → sub-catalogs → leaf skills.
  + This is context management — model navigates the tree on demand instead of loading all skills at once, avoiding context overload and interference between unrelated skills.
- Extract essence from completed chat sessions into new skills to avoid repeating same troubleshooting in future.
  + After achieving desired outcome through multiple iterations with agent, capture workflow as skill.
  + Prevents repeating same back-and-forth when similar task appears later.
  + Skills can be iteratively refined through future usage, triggering on potential model hallucinations.
- Common usage patterns:
  + "Following this skill, create a new skill based on this chat"
  + "Following this skill, create shortcut-links for all my skills for Cursor"
  + "Following this skill, update skill (name) with new knowledge from this chat session"
- Once general idea described in one `SKILL.md`, can follow it with light prompt adjustments for different contexts.

## Creating Skills

- If you are asked to create a new skill — create it as a folder in `./instructions/`.
- Required structure:
  ```
  instructions/[name]/
  ├── SKILL.md          # Required: skill instructions + metadata
  ├── scripts/          # Optional: executable code (shell, Python, JS, etc.)
  ├── references/       # Optional: documentation, API specs, guides
  └── assets/           # Optional: templates, example files, resources
  ```
- `[name]` should consist of several words separated by a `-` symbol, the first of which is a verb, the essence of the operation being performed.
- `SKILL.md` must contain:
  + Frontmatter block with at minimum `name`, `description`, and `version`:
    ```markdown
    ---
    name: skill-name
    description: One-line description of what this skill does
    version: 1.0.0
    ---
    ```
  + Step-by-step instructions in bullet-point style.
  + References to any scripts or assets using relative paths (e.g. `./scripts/run.sh`).
- Use bullet points format, avoid unnecessary headers — keep it simple and actionable.
- Write short, concise statements — minimize words, maximize usefulness.
- Each point should be specific and actionable, not explanatory.
- Only create sub-folders that are actually needed — do not scaffold empty `scripts/`, `references/`, or `assets/` directories.
- Add new skill reference to `./instructions/main.agent.md` with one-line description.
- `main.agent.md` format example:
  ```markdown
  # Skills Catalog

  Each entry below is a skill with a one-line description. Optional sub-fields after `+`:
  - **Keywords** — trigger words/phrases: if user's request matches, load this skill.
  - **Target** — file glob pattern: if current file or context matches, consider this skill relevant.
  - **Exceptions** — edge cases or clarifications that don't fit in the one-liner.

  ---

  - [`./instructions/example/SKILL.md`](./example/SKILL.md) — one-line description.
    + Keywords: word1, word2, phrase
    + Target: `src/**/*.ts`, `config.*`
    + Exceptions: does not apply when ...
  ```
- Use backticks for code examples, file paths, and commands.
- Include practical examples when necessary, but keep them minimal.
- Structure: bullet points with sub-bullets using `+` when needed.
- Avoid long explanations — focus on what to do, not why.
- Use English for skill content, respond in user's language.
- Test practical examples before including them.
- Keep each skill focused on one topic or workflow.
- Apply Single Responsibility Principle to skills to avoid duplication.
- Extract common workflows into separate reusable skill folders.
- Reference shared skills using `./instructions/[name]/SKILL.md` format.
- When a skill grows complex enough to need its own sub-catalog, add `instructions/[name]/main.agent.md` and link it from the root catalog.
- When updating existing skills:
  + Read existing `SKILL.md` first to understand current structure and content.
  + Check which statements from new requirements already exist in the file.
  + Add new statements without rewriting the entire file using targeted edits.
  + Preserve existing useful content and build upon it incrementally.
  + Use sub-bullets with `+` for detailed practices under main points.
  + Include lessons learned from practical implementation experience.
  + Add debug and maintenance guidance for future development work.
  + Focus on actionable insights that improve workflow efficiency.

## Bootstrap Installation (New Project Setup)

- If this skill was shared into an empty agent session in a project that has no skill infrastructure — **this is a signal to install everything from scratch**.
- Detect which IDE is used by checking folder markers:
  + `.github/` folder present → VSCode + GitHub Copilot
  + `.cursor/` folder present → Cursor
  + `.claude/` folder present → Claude Code (CLI / IDE with Claude Code extension)
  + None present → ask user which IDE they use, then create the appropriate folder structure
- For **VSCode + GitHub Copilot**, create the following:
  + `.github/copilot-instructions.md` — with the standard entry-point content (see VSCode section below)
  + `.github/prompts/` — folder for prompt files
  + `.vscode/settings.json` — with required settings (see VSCode section below)
  + `instructions/main.agent.md` — catalog file listing all available skills
  + `instructions/skills-cli/SKILL.md` — this skill itself (copy from source)
- For **Cursor**, create the following:
  + `.cursor/rules/mcpyrex.mdc` — main rules file with entry-point content (see Cursor section below)
  + `.cursor/rules/` — folder for per-skill rule files
  + `instructions/main.agent.md` — catalog file
  + `instructions/skills-cli/SKILL.md` — this skill itself
- For **Claude Code**, create the following:
  + `.claude/CLAUDE.md` — project memory file with entry-point content (see Claude Code section below)
  + `.claude/commands/` — folder for custom slash-command files
  + `.claude/rules/` — folder for modular path-scoped rule files
  + `instructions/main.agent.md` — catalog file
  + `instructions/skills-cli/SKILL.md` — this skill itself
- After creating all files, verify:
  + Entry-point file correctly references `./instructions/main.agent.md`
  + `main.agent.md` exists and lists at least `skills-cli/SKILL.md`
  + IDE settings/rules are configured to load skills on every prompt
- Confirm to user: "Skill infrastructure installed. You can now add more skills following `skills-cli/SKILL.md`."

## IDE Integration: VSCode + GitHub Copilot

- You can identify this case by `.github` folder inside your workspace.
- Add new file to `./.github/prompts/` with name `to-[name].prompt.md` and reference to skill:
  ```markdown
  ---
  mode: agent
  ---
  - When you are asked to _______________, please follow the skill `./instructions/[name]/SKILL.md`.
  ```
- The file `.github/copilot-instructions.md` should contain:
  ```markdown
  - Important! Always follow the instructions in `./instructions/main.agent.md` file.
  - Always load the file completely, not partially.
  - It contains links to other files with skills.
  - You should reload it in **every prompt** to get the latest skills.
  ```
- The settings file `.vscode/settings.json` should contain:
  + Enable skill and MCP files usage:
    ```json
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "chat.mcp.access": "all",
    "chat.agent.maxRequests": 250
    ```
  + [Optionally] Ask user to enable auto-save:
    ```json
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 100
    ```

## IDE Integration: Cursor

- You can identify this case by `.cursor` folder inside your workspace.
- Add new file to `./.cursor/rules/` with name `to-[name].mdc` and reference to skill:
  ```markdown
  ---
  description: Brief description of when to use this skill
  globs:
  alwaysApply: true
  ---

  Follow the skill in `./instructions/[name]/SKILL.md` when you are asked to _______________.
  ```
- The main rules file `.cursor/rules/mcpyrex.mdc` should contain:
  ```markdown
  ---
  description: Main skill orchestrator for the project
  globs:
  alwaysApply: true
  ---

  - Important! Always follow the instructions in `./instructions/main.agent.md` file.
  - Always load the file completely, not partially.
  - It contains links to other files with skills.
  - You should reload it in **every prompt** to get the latest skills.
  ```

## IDE Integration: Claude Code

- You can identify this case by `.claude` folder inside your workspace.
- Add new file to `./.claude/commands/` with name `to-[name].md` and reference to skill:
  ```markdown
  Follow the skill in `./instructions/[name]/SKILL.md`.

  $ARGUMENTS
  ```
- `$ARGUMENTS` is a special placeholder — gets replaced with user input after the slash command. User invokes via `/project:to-[name]`.
- The project memory file `.claude/CLAUDE.md` should contain:
  ```markdown
  - Important! Always follow the instructions in `./instructions/main.agent.md` file.
  - Always load the file completely, not partially.
  - It contains links to other files with skills.
  - You should reload it in **every prompt** to get the latest skills.
  ```

## Config: skills.json (project root)

```json
{
  "repo_url": "../skills-repo",
  "groups": ["project-alpha"],
  "extra_skills": [],
  "excluded_skills": []
}
```

| Field | Description |
|-------|-------------|
| `repo_url` | Path or URL to the central skills repository |
| `groups` | Active groups for this workspace |
| `extra_skills` | Individual skills added outside of groups |
| `excluded_skills` | Skills to exclude even if they appear in groups or global |

Note: active skills are resolved dynamically from manifests. Use `skills list` to see them.

## Skill Resolution Priority

1. `_global.json` skills - included for everyone regardless of groups
2. Group manifest skills - from `<group>.json` + any `sub-configs` referenced recursively
3. `extra_skills` - individual additions from workspace config
4. `excluded_skills` - removals applied last, overrides everything above

## Workspace Layout

```
my-project/
├── skills.json              <- workspace config (auto-generated by init)
├── instructions/            <- cloned skills repo (sparse checkout)
│   ├── .manifest/           <- manifest files defining groups
│   │   ├── _global.json     <- skills for all groups
│   │   ├── backend.json     <- backend group definition
│   │   └── security.json    <- security group definition
│   ├── code-review-base/
│   │   ├── SKILL.md         <- instructions for AI agent
│   │   └── info.json        <- metadata (description, owner)
│   └── ...
└── src/                     <- your project source code
```

## Manifest Files (.manifest/)

| File | Purpose | Format |
|------|---------|--------|
| `_global.json` | Skills for all groups | `{"skills": ["skill-a", "skill-b"]}` |
| `<group>.json` | Group-specific skills | `{"skills": ["skill-c"], "sub-configs": ["sub-group"]}` |
| `<sub>.json` | Sub-config referenced by groups | `{"skills": ["skill-d"], "sub-configs": []}` |

Sub-configs are resolved recursively: a group can reference sub-configs, which can reference other sub-configs.

## Typical Workflow

```bash
# 1. Initialize workspace with skills from a central repo
skills init --repo git@github.com:org/skills.git --groups backend

# 2. See what skills are available
skills list --verbose

# 3. Edit a skill locally
# (edit instructions/code-review-base/SKILL.md)

# 4. Propose changes via PR
skills push code-review-base

# 5. Pull latest updates from the team
skills pull

# 6. Add another group or individual skill
skills enable group security
skills enable my-custom-skill

# 7. Remove a skill you don't need
skills disable unwanted-skill

# 8. Force disable a skill with uncommitted changes
skills disable unwanted-skill --force
```
