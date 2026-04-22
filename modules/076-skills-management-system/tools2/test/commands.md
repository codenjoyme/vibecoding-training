# Skills CLI — Smoke Test

## Phase 1: Cleanup & Install

> `npm uninstall -g skills-cli`
```

up to date in 568ms
```
> `rm -rf /workspace/skills-repo`
```
```
> `rm -rf /workspace/project-repo`
```
```
> `npm install -g --install-links /app`
```

added 1 package in 383ms
```
> `command -v skills`
```
/usr/local/bin/skills
```

## Phase 2: Help commands

> `skills help`
```
Skills CLI - manage shared AI instruction skills across your team

Usage:
  skills <command> [flags]

Commands:
  init      Initialize workspace from a central skills repository
              --repo <url|path>   URL or local path to the skills repo (required)
              --groups <g1,g2>    Groups to activate (optional; omit for global-only)

  pull      Update local skills from the remote repository

  push      Propose changes to a skill via a branch and Pull Request
              <skill-name>        Name of the skill to push (required)
              --groups <g1> <g2>  Add skill to group manifests (optional)

  list      List available skills in the repository
              --verbose           Show description and owner from info.json
              --json              Output as JSON array

  create    Create a new skill with SKILL.md and info.json templates
              <skill-name>        Name of the new skill (required)

  enable    Enable a group or individual skill
              group <name>        Add a group to the workspace
              <skill-name>        Add an individual skill (extra_skills)

  disable   Disable a group or individual skill (--force to override)
              [--force] group <name>   Remove a group from the workspace
              [--force] <skill-name>   Exclude an individual skill (excluded_skills)

  ai-help   Show concise CLI reference for AI agents
  init-repo Initialize a new skills repository with base structure
              <folder-name>       Target folder name (required)

  help      Show this help message

Use "skills <command> --help" for more information about a command.

Examples:
  skills init --repo https://github.com/org/skills
  skills init --repo ../skills-repo --groups backend,security
  skills pull
  skills push code-review-base
  skills push my-skill --groups backend security
  skills list --verbose
  skills create my-skill
  skills enable group security
  skills enable my-custom-skill
  skills disable group security
  skills disable obsolete-skill
  skills disable obsolete-skill --force
```
> `skills ai-help`
```
# Skills CLI - Quick Reference for AI Agents

Skills CLI manages shared AI skills across teams.
Each skill is a self-contained folder with 'SKILL.md' (instructions for the AI agent) and 'info.json' (metadata).
Skills live in a central Git repository and are distributed to project workspaces via sparse checkout.

## Core Concepts

- **Skill**: a folder ('<skill-name>/SKILL.md' + 'info.json') with instructions an AI agent can follow.
- **Group**: a named collection of skills defined in '.manifest/<group>.json'. Teams assign groups to projects.
- **Manifest**: JSON files in '.manifest/' that define which skills belong to which groups.
- **Workspace config** ('skills.json'): project-level file tracking repo URL, active groups, extra/excluded skills.
- **Sparse checkout**: only the skills your project needs are checked out locally in 'instructions/'.

## Commands

'''
skills init --repo <url|path> [--groups <g1>[,<g2>...]]
'''
Initialize workspace: clones the skills repo into 'instructions/', reads manifests,
resolves skills for the given groups, and applies sparse checkout.
- '--repo' (required): Git URL or local path to the central skills repository.
- '--groups' (optional): comma-separated group names. Also accepts positional args: 'skills init --repo <url> backend security'.
- If no groups specified, only '_global.json' skills are initialized. Use 'skills enable group <name>' later.
- If 'skills.json' already exists and no flags given, re-runs resolution from existing config.

'''
skills pull
'''
Pulls latest changes from the remote skills repository ('git pull' inside 'instructions/').
Requires initialized workspace ('skills.json' must exist).

'''
skills push <skill-name> [--groups <group1> <group2> ...]
'''
Proposes local changes to a skill via a feature branch:
1. Creates branch 'feature/<skill-name>-update'
2. Stages changes in 'instructions/<skill-name>/'
3. Commits with a conventional message
4. (optional) Adds skill to specified group manifests and commits manifest changes
5. Pushes branch to origin
6. Prints the Pull Request URL (GitHub/GitLab)
- '--groups' (optional): add skill to specified group manifests. Creates the group file if it doesn't exist. Changes are included in the same PR branch.

'''
skills list [--verbose] [--json]
'''
Lists all skills in the repository. Active skills (in current groups) marked with checkmark.
- '--verbose': shows description and owner from 'info.json'.
- '--json': outputs as JSON array with 'name', 'active', 'description', 'owner' fields.

'''
skills create <skill-name>
'''
Creates a new skill folder in 'instructions/' with template 'SKILL.md' and 'info.json'.
Does not add the skill to any group manifest (that's a manual step in the repo).

'''
skills enable group <name>
'''
Adds a group to the 'groups' array in 'skills.json'.
Sparse checkout is re-applied automatically — skill folders appear immediately.

'''
skills enable <skill-name>
'''
Adds an individual skill to 'extra_skills' in 'skills.json'.
If the skill was previously excluded, removes it from 'excluded_skills' instead.
Sparse checkout is re-applied automatically.

'''
skills disable [--force] group <name>
'''
Removes a group from the 'groups' array in 'skills.json'.
If any skills being removed have uncommitted local changes, the command refuses.
Use '--force' to override — changes are stashed automatically ('git stash list' to review).
Sparse checkout is re-applied automatically — skill folders are removed immediately.

'''
skills disable [--force] <skill-name>
'''
Adds a skill to 'excluded_skills' in 'skills.json' (removes from 'extra_skills' if present).
Excluded skills are filtered out during resolution even if they appear in group manifests.
If the skill has uncommitted local changes, the command refuses.
Use '--force' to override — changes are stashed automatically.
Sparse checkout is re-applied automatically.

'''
skills init-repo <folder-name>
'''
Scaffolds a new skills repository with example manifests, skills, and folder structure.
Use this to bootstrap a central skills repo from scratch.

'''
skills ai-help
'''
Shows this reference (reads SKILL-CLI.md or prints inline fallback).

'''
skills help
'''
Shows general CLI help with command list and examples.

## Typical Workflow

1. 'skills init --repo <url>' - set up workspace (global skills only, or add '--groups <group>' for group-specific skills)
2. 'skills list --verbose' - see what's available
3. Edit 'instructions/<skill>/SKILL.md'
4. 'skills push <skill>' - propose changes via PR (optionally '--groups <g1> <g2>' to assign to groups)
5. 'skills pull' - get latest updates

## Architecture and Motivation

- IDE-agnostic architecture allows teams to use different IDE/Plugins while sharing same skill base.
- Team alignment on LLM model choice is more critical than IDE choice — IDE switching is less disruptive.
- Skills are self-contained folders with 'SKILL.md' describing SDLC workflows without platform-specific adapters like 'alwaysApply: true' or 'mode: agent'.
- Following Single Responsibility Principle (SRP) — one SDLC workflow piece per skill.
  + Recommended soft limit: ~700 lines per 'SKILL.md'. Exceeding this is a signal to split.
  + Complex skills can reference other skills — composability over monoliths.
  + Terminology hint: large multi-step workflows → "agents", small focused actions → "skills". Naming may vary by author.
- 'main.agent.md' serves as catalog of all skills with brief descriptions — when asked about (what to do), follow this skill (with file path).
  + Each entry has optional sub-fields after '+': **Keywords** (trigger words), **Target** (file glob pattern), **Exceptions** (edge cases).
  + When adding new skill to catalog, fill in at least Keywords to help model match user requests to skills.
- Platform-specific entry points ('.github/copilot-instructions.md' for Copilot, '.cursor/rules/*.mdc' for Cursor, '.claude/CLAUDE.md' for Claude Code) reference 'main.agent.md' to load with every prompt.
- Optionally, 'AGENTS.md' in project root with same content as entry point — universal fallback recognized by Claude, Copilot, Cursor agents.
  + Important when '.github/', '.cursor/', or '.claude/' are not committed — without them other non-IDE agents have no entry point to discover 'instructions/' folder.
  + Decision is up to the team.
- 'instructions/' can live in the project repo or be extracted into a separate sub-repository (git submodule, etc.).
  + '.github/', '.cursor/' stay local per team member's IDE choice — not committed.
  + For cloud agents — add 'AGENTS.md' in project root as described above.
  + Or commit skills together with the project — simpler, fewer moving parts.
  + Each team decides what fits their workflow.
- Why tool-agnostic over native systems (GitHub '.instructions.md', Cursor '.mdc'):
  + Native formats are incompatible: Copilot's 'applyTo' globs, 'excludeAgent' fields, Cursor's 'alwaysApply', 'globs', 'description' frontmatter, Claude Code's 'paths:' frontmatter — none of these are portable.
  + Vendor lock-in: rewriting dozens of skill files when switching IDE or when vendor changes format is wasted effort.
  + This approach: one source of truth in 'instructions/', thin adapter wrappers per IDE — only wrappers change on IDE switch.
  + Pure markdown skills work with any LLM agent (CLI, API, CI pipelines) — not tied to IDE runtime at all.
  + Team members on different IDEs (Copilot, Cursor, Windsurf, etc.) share identical workflow knowledge without translation.
- Architectural advantage — separation of concerns:
  + Skills = **what to do** (platform-agnostic SDLC knowledge).
  + Wrappers = **how to load** (platform-specific glue, 2–3 lines each).
  + Catalog ('main.agent.md') = **when to use** (routing by task description).
  + Adding a new IDE means only adding a new set of thin wrappers — zero changes to skill content.
- Hybrid approach is always welcome: use full power of your IDE's native features ('applyTo', 'globs', 'excludeAgent', etc.) in wrappers that reference files in 'instructions/'. Just keep in mind — those IDE-specific features only work for users of that particular IDE.
- Place skills where they make sense for your project — then build a tree of 'main.agent.md' nodes from root to leaves:
  + Hierarchical layout: 'instructions/backend/main.agent.md', 'instructions/frontend/main.agent.md' — each sub-catalog follows same structure, root 'main.agent.md' links to them.
  + Alternative: co-located layout — 'backend/instructions/*', 'frontend/instructions/*' — but then IDE entry point must reference multiple roots, which adds complexity.
  + Key idea: tree-shaped chain from IDE entry point → root 'main.agent.md' → sub-catalogs → leaf skills.
  + This is context management — model navigates the tree on demand instead of loading all skills at once, avoiding context overload and interference between unrelated skills.
- Extract essence from completed chat sessions into new skills to avoid repeating same troubleshooting in future.
  + After achieving desired outcome through multiple iterations with agent, capture workflow as skill.
  + Prevents repeating same back-and-forth when similar task appears later.
  + Skills can be iteratively refined through future usage, triggering on potential model hallucinations.
- Common usage patterns:
  + "Following this skill, create a new skill based on this chat"
  + "Following this skill, create shortcut-links for all my skills for Cursor"
  + "Following this skill, update skill (name) with new knowledge from this chat session"
- Once general idea described in one 'SKILL.md', can follow it with light prompt adjustments for different contexts.

## Creating Skills

- If you are asked to create a new skill — create it as a folder in './instructions/'.
- Required structure:
  '''
  instructions/[name]/
  ├── SKILL.md          # Required: skill instructions + metadata
  ├── scripts/          # Optional: executable code (shell, Python, JS, etc.)
  ├── references/       # Optional: documentation, API specs, guides
  └── assets/           # Optional: templates, example files, resources
  '''
- '[name]' should consist of several words separated by a '-' symbol, the first of which is a verb, the essence of the operation being performed.
- 'SKILL.md' must contain:
  + Frontmatter block with at minimum 'name', 'description', and 'version':
    '''markdown
    ---
    name: skill-name
    description: One-line description of what this skill does
    version: 1.0.0
    ---
    '''
  + Step-by-step instructions in bullet-point style.
  + References to any scripts or assets using relative paths (e.g. './scripts/run.sh').
- Use bullet points format, avoid unnecessary headers — keep it simple and actionable.
- Write short, concise statements — minimize words, maximize usefulness.
- Each point should be specific and actionable, not explanatory.
- Only create sub-folders that are actually needed — do not scaffold empty 'scripts/', 'references/', or 'assets/' directories.
- Add new skill reference to './instructions/main.agent.md' with one-line description.
- 'main.agent.md' format example:
  '''markdown
  # Skills Catalog

  Each entry below is a skill with a one-line description. Optional sub-fields after '+':
  - **Keywords** — trigger words/phrases: if user's request matches, load this skill.
  - **Target** — file glob pattern: if current file or context matches, consider this skill relevant.
  - **Exceptions** — edge cases or clarifications that don't fit in the one-liner.

  ---

  - ['./instructions/example/SKILL.md'](./example/SKILL.md) — one-line description.
    + Keywords: word1, word2, phrase
    + Target: 'src/**/*.ts', 'config.*'
    + Exceptions: does not apply when ...
  '''
- Use backticks for code examples, file paths, and commands.
- Include practical examples when necessary, but keep them minimal.
- Structure: bullet points with sub-bullets using '+' when needed.
- Avoid long explanations — focus on what to do, not why.
- Use English for skill content, respond in user's language.
- Test practical examples before including them.
- Keep each skill focused on one topic or workflow.
- Apply Single Responsibility Principle to skills to avoid duplication.
- Extract common workflows into separate reusable skill folders.
- Reference shared skills using './instructions/[name]/SKILL.md' format.
- When a skill grows complex enough to need its own sub-catalog, add 'instructions/[name]/main.agent.md' and link it from the root catalog.
- When updating existing skills:
  + Read existing 'SKILL.md' first to understand current structure and content.
  + Check which statements from new requirements already exist in the file.
  + Add new statements without rewriting the entire file using targeted edits.
  + Preserve existing useful content and build upon it incrementally.
  + Use sub-bullets with '+' for detailed practices under main points.
  + Include lessons learned from practical implementation experience.
  + Add debug and maintenance guidance for future development work.
  + Focus on actionable insights that improve workflow efficiency.

## Bootstrap Installation (New Project Setup)

- If this skill was shared into an empty agent session in a project that has no skill infrastructure — **this is a signal to install everything from scratch**.
- Detect which IDE is used by checking folder markers:
  + '.github/' folder present → VSCode + GitHub Copilot
  + '.cursor/' folder present → Cursor
  + '.claude/' folder present → Claude Code (CLI / IDE with Claude Code extension)
  + None present → ask user which IDE they use, then create the appropriate folder structure
- For **VSCode + GitHub Copilot**, create the following:
  + '.github/copilot-instructions.md' — with the standard entry-point content (see VSCode section below)
  + '.github/prompts/' — folder for prompt files
  + '.vscode/settings.json' — with required settings (see VSCode section below)
  + 'instructions/main.agent.md' — catalog file listing all available skills
  + 'instructions/skills-cli/SKILL.md' — this skill itself (copy from source)
- For **Cursor**, create the following:
  + '.cursor/rules/mcpyrex.mdc' — main rules file with entry-point content (see Cursor section below)
  + '.cursor/rules/' — folder for per-skill rule files
  + 'instructions/main.agent.md' — catalog file
  + 'instructions/skills-cli/SKILL.md' — this skill itself
- For **Claude Code**, create the following:
  + '.claude/CLAUDE.md' — project memory file with entry-point content (see Claude Code section below)
  + '.claude/commands/' — folder for custom slash-command files
  + '.claude/rules/' — folder for modular path-scoped rule files
  + 'instructions/main.agent.md' — catalog file
  + 'instructions/skills-cli/SKILL.md' — this skill itself
- After creating all files, verify:
  + Entry-point file correctly references './instructions/main.agent.md'
  + 'main.agent.md' exists and lists at least 'skills-cli/SKILL.md'
  + IDE settings/rules are configured to load skills on every prompt
- Confirm to user: "Skill infrastructure installed. You can now add more skills following 'skills-cli/SKILL.md'."

## IDE Integration: VSCode + GitHub Copilot

- You can identify this case by '.github' folder inside your workspace.
- Add new file to './.github/prompts/' with name 'to-[name].prompt.md' and reference to skill:
  '''markdown
  ---
  mode: agent
  ---
  - When you are asked to _______________, please follow the skill './instructions/[name]/SKILL.md'.
  '''
- The file '.github/copilot-instructions.md' should contain:
  '''markdown
  - Important! Always follow the instructions in './instructions/main.agent.md' file.
  - Always load the file completely, not partially.
  - It contains links to other files with skills.
  - You should reload it in **every prompt** to get the latest skills.
  '''
- The settings file '.vscode/settings.json' should contain:
  + Enable skill and MCP files usage:
    '''json
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "chat.mcp.access": "all",
    "chat.agent.maxRequests": 250
    '''
  + [Optionally] Ask user to enable auto-save:
    '''json
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 100
    '''

## IDE Integration: Cursor

- You can identify this case by '.cursor' folder inside your workspace.
- Add new file to './.cursor/rules/' with name 'to-[name].mdc' and reference to skill:
  '''markdown
  ---
  description: Brief description of when to use this skill
  globs:
  alwaysApply: true
  ---

  Follow the skill in './instructions/[name]/SKILL.md' when you are asked to _______________.
  '''
- The main rules file '.cursor/rules/mcpyrex.mdc' should contain:
  '''markdown
  ---
  description: Main skill orchestrator for the project
  globs:
  alwaysApply: true
  ---

  - Important! Always follow the instructions in './instructions/main.agent.md' file.
  - Always load the file completely, not partially.
  - It contains links to other files with skills.
  - You should reload it in **every prompt** to get the latest skills.
  '''

## IDE Integration: Claude Code

- You can identify this case by '.claude' folder inside your workspace.
- Add new file to './.claude/commands/' with name 'to-[name].md' and reference to skill:
  '''markdown
  Follow the skill in './instructions/[name]/SKILL.md'.

  $ARGUMENTS
  '''
- '$ARGUMENTS' is a special placeholder — gets replaced with user input after the slash command. User invokes via '/project:to-[name]'.
- The project memory file '.claude/CLAUDE.md' should contain:
  '''markdown
  - Important! Always follow the instructions in './instructions/main.agent.md' file.
  - Always load the file completely, not partially.
  - It contains links to other files with skills.
  - You should reload it in **every prompt** to get the latest skills.
  '''

## Config: skills.json (project root)

'''json
{
  "repo_url": "../skills-repo",
  "groups": ["project-alpha"],
  "extra_skills": [],
  "excluded_skills": []
}
'''

| Field | Description |
|-------|-------------|
| 'repo_url' | Path or URL to the central skills repository |
| 'groups' | Active groups for this workspace |
| 'extra_skills' | Individual skills added outside of groups |
| 'excluded_skills' | Skills to exclude even if they appear in groups or global |

Note: active skills are resolved dynamically from manifests. Use 'skills list' to see them.

## Skill Resolution Priority

1. '_global.json' skills - included for everyone regardless of groups
2. Group manifest skills - from '<group>.json' + any 'sub-configs' referenced recursively
3. 'extra_skills' - individual additions from workspace config
4. 'excluded_skills' - removals applied last, overrides everything above

## Workspace Layout

'''
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
'''

## Manifest Files (.manifest/)

| File | Purpose | Format |
|------|---------|--------|
| '_global.json' | Skills for all groups | '{"skills": ["skill-a", "skill-b"]}' |
| '<group>.json' | Group-specific skills | '{"skills": ["skill-c"], "sub-configs": ["sub-group"]}' |
| '<sub>.json' | Sub-config referenced by groups | '{"skills": ["skill-d"], "sub-configs": []}' |

Sub-configs are resolved recursively: a group can reference sub-configs, which can reference other sub-configs.

## Typical Workflow

'''bash
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
'''
```
> `skills init-repo --help`
```
Initialize a new skills repository with base structure.

Creates a folder with:
  .manifest/_global.json      — global skills config
  .manifest/group-1.json      — example group config
  .manifest/sub-group.json    — example sub-config
  skills-cli/                 — skill: CLI usage, creating skills, IDE integration

Usage:
  skills init-repo <folder-name>

Examples:
  skills init-repo my-skills-repo
  skills init-repo ../shared-skills
```
> `skills list --help`
```
List all available skills in the repository.

Usage:
  skills list [--verbose] [--json]

Flags:
  --verbose  Show description and owner from info.json
  --json     Output skills as JSON array

Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.
```
> `skills push --help`
```
Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name> [--groups <group1> <group2> ...]

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. (optional) Add skill to specified group manifests and commit manifest changes
  5. Push the branch to origin
  6. Print the Pull Request URL (for GitHub/GitLab remotes)

Flags:
  --groups  Add skill to specified group manifests (creates group file if not found)

Examples:
  skills push my-skill
  skills push my-skill --groups backend security
  skills push my-skill --groups backend,frontend

Note: when --groups is used, manifest changes are included in the same PR branch.
If a group manifest does not exist, it will be created with the skill as its first entry.
```
> `skills pull --help`
```
Update local skills from the remote repository.

Usage:
  skills pull
```
> `skills enable --help`
```
Enable a group or individual skill in this workspace.

Usage:
  skills enable group <group-name>   Add a group to the workspace
  skills enable <skill-name>         Add an individual skill

Sparse checkout is re-applied automatically after enabling.

Examples:
  skills enable group security
  skills enable my-custom-skill
```
> `skills disable --help`
```
Disable a group or individual skill in this workspace.

Usage:
  skills disable group <group-name>   Remove a group from the workspace
  skills disable <skill-name>         Exclude an individual skill

Flags:
  --force   Force disable even if there are uncommitted local changes

If the skill has uncommitted local changes, the command will refuse
to disable it. Use --force to override - changes will be stashed
automatically (use 'git stash list' inside instructions/ to review).

Sparse checkout is re-applied automatically after disabling.

Examples:
  skills disable group security
  skills disable security-guidelines
  skills disable security-guidelines --force
```

## Phase 3: Create skills repository

> `mkdir -p /workspace/skills-repo`
```
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `skills init-repo ../project-repo`
```
→ Creating skills repository at ../project-repo ...
  ✓ Files created

✅ Skills repository initialized at ../project-repo

Next steps:
  cd ../project-repo
  git init && git add . && git commit -m "init: skills repository"
  # Then push to your Git hosting
```

Check what was generated:

> `ls ../project-repo`
```
skills-cli
```
> `ls ../project-repo/.manifest`
```
_global.json
group-1.json
sub-group.json
```
> `cat ../project-repo/.manifest/_global.json`
```
{
  "skills": [
    "skills-cli"
  ]
}
```
> `cat ../project-repo/.manifest/group-1.json`
```
{
  "skills": [],
  "sub-configs": ["sub-group"]
}
```
> `cat ../project-repo/.manifest/sub-group.json`
```
{
  "skills": [],
  "sub-configs": []
}
```
> `cat ../project-repo/skills-cli/info.json`
```
{
  "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
  "owner": "your-name@example.com"
}
```

Init git in the skills repo:

> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git init`
```
hint: Using 'master' as the name for the initial branch. This default branch name
hint: is subject to change. To configure the initial branch name to use in all
hint: of your new repositories, which will suppress this warning, call:
hint: 
hint: 	git config --global init.defaultBranch <name>
hint: 
hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
hint: 'development'. The just-created branch can be renamed via this command:
hint: 
hint: 	git branch -m <name>
Initialized empty Git repository in /workspace/project-repo/.git/
```
> `git add .`
```
```
> `git commit -m "Initial commit"`
```
[master (root-commit) faf0c18] Initial commit
 6 files changed, 430 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 .manifest/_global.json
 create mode 100644 .manifest/group-1.json
 create mode 100644 .manifest/sub-group.json
 create mode 100644 skills-cli/SKILL.md
 create mode 100644 skills-cli/info.json
```
> `git log --oneline`
```
faf0c18 Initial commit
```
> `git branch --list`
```
* master
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```

Error case — init-repo to already existing folder:

> `skills init-repo ../project-repo`
```
Error: folder "../project-repo" already exists
```

## Phase 4: Init workspace

> `skills init --repo ../project-repo --groups group-1`
```
→ Cloning skills repo from ../project-repo ...
Cloning into 'instructions'...
done.
  ✓ Cloned
→ Resolving skills for groups: group-1 ...
  ✓ Resolved 1 skill(s): skills-cli
→ Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace initialized!
   Repository: ../project-repo
   Groups:     group-1
   Skills:     skills-cli
   Location:   instructions/

Your AI agent can now read skills from instructions/<skill-name>/SKILL.md
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [],
  "excluded_skills": []
}
```
> `ls instructions/`
```
skills-cli
```
> `ls instructions/.manifest/`
```
_global.json
group-1.json
sub-group.json
```
> `ls instructions/skills-cli/`
```
SKILL.md
info.json
```

Error case — init without --repo and no config:

> `rm -rf /workspace/no-config-dir`
```
```
> `mkdir -p /workspace/no-config-dir`
```
```
> `cd /workspace/no-config-dir`
```
/workspace/no-config-dir
```
> `skills init`
```
Error: --repo is required (no existing skills.json found)
Initialize skills workspace from a central repository.

Clones the skills repository, resolves skills for the specified groups,
and applies sparse checkout so only the needed skills are present.

If --groups is omitted, only _global.json skills are initialized.
Use 'skills enable group <name>' later to add group-specific skills.

Usage:
  skills init --repo <url-or-path> [--groups <group1>[,<group2>...]] [group...]

Flags:
  --repo    URL or local path to the central skills repository (required)
  --groups  Groups to initialize (comma-separated or repeated flag; positional args also accepted; optional)

Examples:
  skills init --repo https://github.com/org/skills
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills init --repo ../skills-repo backend security
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```

## Phase 5: List skills

> `skills list`
```
Skills repository: ../project-repo
Groups:           group-1

  ✅ skills-cli

Active: 1  |  Total: 1
```
> `skills list --verbose`
```
Skills repository: ../project-repo
Groups:           group-1

  ✅ skills-cli
     Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).
     Owner: your-name@example.com

Active: 1  |  Total: 1
```
> `skills list --json`
```
[
  {
    "name": "skills-cli",
    "active": true,
    "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
    "owner": "your-name@example.com"
  }
]
```

## Phase 6: Create skills, push to repo

Create alpha-skill, check files, push and merge into project-repo:

> `skills create alpha-skill`
```
✅ Skill "alpha-skill" created at instructions/alpha-skill
   → instructions/alpha-skill/SKILL.md
   → instructions/alpha-skill/info.json

Edit SKILL.md with your instructions, then use 'skills push' to propose it.
```
> `ls instructions/alpha-skill/`
```
SKILL.md
info.json
```
> `cat instructions/alpha-skill/SKILL.md`
```
# Skill: alpha-skill

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
```
> `cat instructions/alpha-skill/info.json`
```
{
  "description": "This skill provides _____. It can be used for _____. The main features include _____.",
  "owner": "Your_Name@domain.com"
}
```
> `skills push alpha-skill`
```
→ Creating branch feature/alpha-skill-update ...
Switched to a new branch 'feature/alpha-skill-update'
  ✓ Branch created
→ Staging and committing changes in alpha-skill/ ...
  ✓ Changes committed
→ Pushing branch feature/alpha-skill-update ...
To /workspace/skills-repo/../project-repo
 * [new branch]      feature/alpha-skill-update -> feature/alpha-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "alpha-skill" pushed for review
   Branch: feature/alpha-skill-update
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "alpha-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```
> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git merge feature/alpha-skill-update --no-edit`
```
Updating faf0c18..a611368
Fast-forward
 alpha-skill/SKILL.md  | 9 +++++++++
 alpha-skill/info.json | 4 ++++
 2 files changed, 13 insertions(+)
 create mode 100644 alpha-skill/SKILL.md
 create mode 100644 alpha-skill/info.json
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
   faf0c18..a611368  master     -> origin/master
✅ Skills updated successfully
```

Create beta-skill, push and merge:

> `skills create beta-skill`
```
✅ Skill "beta-skill" created at instructions/beta-skill
   → instructions/beta-skill/SKILL.md
   → instructions/beta-skill/info.json

Edit SKILL.md with your instructions, then use 'skills push' to propose it.
```
> `ls instructions/beta-skill/`
```
SKILL.md
info.json
```
> `skills push beta-skill`
```
→ Creating branch feature/beta-skill-update ...
Switched to a new branch 'feature/beta-skill-update'
  ✓ Branch created
→ Staging and committing changes in beta-skill/ ...
  ✓ Changes committed
→ Pushing branch feature/beta-skill-update ...
To /workspace/skills-repo/../project-repo
 * [new branch]      feature/beta-skill-update -> feature/beta-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "beta-skill" pushed for review
   Branch: feature/beta-skill-update
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "beta-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```
> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git merge feature/beta-skill-update --no-edit`
```
Updating a611368..4ee631e
Fast-forward
 beta-skill/SKILL.md  | 9 +++++++++
 beta-skill/info.json | 4 ++++
 2 files changed, 13 insertions(+)
 create mode 100644 beta-skill/SKILL.md
 create mode 100644 beta-skill/info.json
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
   a611368..4ee631e  master     -> origin/master
✅ Skills updated successfully
```

Create gamma-skill, push and merge:

> `skills create gamma-skill`
```
✅ Skill "gamma-skill" created at instructions/gamma-skill
   → instructions/gamma-skill/SKILL.md
   → instructions/gamma-skill/info.json

Edit SKILL.md with your instructions, then use 'skills push' to propose it.
```
> `skills push gamma-skill`
```
→ Creating branch feature/gamma-skill-update ...
Switched to a new branch 'feature/gamma-skill-update'
  ✓ Branch created
→ Staging and committing changes in gamma-skill/ ...
  ✓ Changes committed
→ Pushing branch feature/gamma-skill-update ...
To /workspace/skills-repo/../project-repo
 * [new branch]      feature/gamma-skill-update -> feature/gamma-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "gamma-skill" pushed for review
   Branch: feature/gamma-skill-update
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "gamma-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```
> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git merge feature/gamma-skill-update --no-edit`
```
Updating 4ee631e..5b41aee
Fast-forward
 gamma-skill/SKILL.md  | 9 +++++++++
 gamma-skill/info.json | 4 ++++
 2 files changed, 13 insertions(+)
 create mode 100644 gamma-skill/SKILL.md
 create mode 100644 gamma-skill/info.json
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
   4ee631e..5b41aee  master     -> origin/master
✅ Skills updated successfully
```

All three skills now exist in project-repo:

> `skills list`
```
Skills repository: ../project-repo
Groups:           group-1

  ✅ alpha-skill
  ✅ beta-skill
  ✅ gamma-skill
  ✅ skills-cli

Active: 4  |  Total: 4
```
> `skills list --json`
```
[
  {
    "name": "alpha-skill",
    "active": true,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "beta-skill",
    "active": true,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "gamma-skill",
    "active": true,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "skills-cli",
    "active": true,
    "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
    "owner": "your-name@example.com"
  }
]
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "alpha-skill",
    "beta-skill",
    "gamma-skill"
  ],
  "excluded_skills": []
}
```

Error case — create duplicate skill:

> `skills create alpha-skill`
```
Error: skill "alpha-skill" already exists at instructions/alpha-skill
```

Error case — create without name:

> `skills create`
```
Error: skill name is required
Usage: skills create <skill-name>
```

## Phase 7: Enable/disable individual skills

Skills were auto-added to extra_skills by create. Verify state:

> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "alpha-skill",
    "beta-skill",
    "gamma-skill"
  ],
  "excluded_skills": []
}
```

Disable alpha-skill:

> `skills disable alpha-skill`
```
✅ Skill "alpha-skill" disabled
→ Applying sparse checkout (3 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "beta-skill",
    "gamma-skill"
  ],
  "excluded_skills": [
    "alpha-skill"
  ]
}
```
> `skills list`
```
Skills repository: ../project-repo
Groups:           group-1

  ○  alpha-skill
  ✅ beta-skill
  ✅ gamma-skill
  ✅ skills-cli

Active: 3  |  Total: 4
```

Re-enable alpha-skill (remove from excluded):

> `skills enable alpha-skill`
```
✅ Skill "alpha-skill" re-enabled (removed from exclusion list)
→ Applying sparse checkout (3 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "beta-skill",
    "gamma-skill"
  ],
  "excluded_skills": []
}
```
> `skills list`
```
Skills repository: ../project-repo
Groups:           group-1

  ○  alpha-skill
  ✅ beta-skill
  ✅ gamma-skill
  ✅ skills-cli

Active: 3  |  Total: 4
```

Disable beta-skill:

> `skills disable beta-skill`
```
✅ Skill "beta-skill" disabled
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "gamma-skill"
  ],
  "excluded_skills": [
    "beta-skill"
  ]
}
```

Re-enable beta-skill:

> `skills enable beta-skill`
```
✅ Skill "beta-skill" re-enabled (removed from exclusion list)
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "gamma-skill"
  ],
  "excluded_skills": []
}
```

Error case — enable already enabled skill:

> `skills enable alpha-skill`
```
✅ Skill "alpha-skill" enabled
→ Applying sparse checkout (3 skill(s)) ...
  ✓ Sparse checkout applied
```

Error case — disable then double-disable:

> `skills disable alpha-skill`
```
✅ Skill "alpha-skill" disabled
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `skills disable alpha-skill`
```
Skill "alpha-skill" is already disabled
```

Re-enable for later phases:

> `skills enable alpha-skill`
```
✅ Skill "alpha-skill" re-enabled (removed from exclusion list)
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "gamma-skill"
  ],
  "excluded_skills": []
}
```

## Phase 8: Enable/disable groups

Current state:

> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "gamma-skill"
  ],
  "excluded_skills": []
}
```

Disable group-1 (was set during init):

> `skills disable group group-1`
```
✅ Group "group-1" disabled
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [],
  "extra_skills": [
    "gamma-skill"
  ],
  "excluded_skills": []
}
```
> `skills list`
```
Skills repository: ../project-repo
Groups:           

  ○  alpha-skill
  ○  beta-skill
  ✅ gamma-skill
  ✅ skills-cli

Active: 2  |  Total: 4
```

Re-enable group-1:

> `skills enable group group-1`
```
✅ Group "group-1" enabled
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "gamma-skill"
  ],
  "excluded_skills": []
}
```
> `skills list`
```
Skills repository: ../project-repo
Groups:           group-1

  ○  alpha-skill
  ○  beta-skill
  ✅ gamma-skill
  ✅ skills-cli

Active: 2  |  Total: 4
```

Error case — enable already enabled group:

> `skills enable group group-1`
```
Group "group-1" is already enabled
```

Disable and try double-disable:

> `skills disable group group-1`
```
✅ Group "group-1" disabled
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```
> `skills disable group group-1`
```
Group "group-1" is not currently enabled
```

Error case — missing group name:

> `skills enable group`
```
Error: group name is required
Usage: skills enable group <group-name>
```
> `skills disable group`
```
Error: group name is required
Usage: skills disable group <group-name>
```

Re-enable for later phases:

> `skills enable group group-1`
```
✅ Group "group-1" enabled
→ Applying sparse checkout (2 skill(s)) ...
  ✓ Sparse checkout applied
```

## Phase 9: Pull

> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
✅ Skills updated successfully
```

## Phase 10: Push + verify in project-repo

Make a change in alpha-skill before push:

> `skills enable alpha-skill`
```
✅ Skill "alpha-skill" enabled
→ Applying sparse checkout (3 skill(s)) ...
  ✓ Sparse checkout applied
```
> `echo "## Updated content for smoke test" >> instructions/alpha-skill/SKILL.md`
```
```
> `cat instructions/alpha-skill/SKILL.md`
```
# Skill: alpha-skill

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
## Updated content for smoke test
```
> `skills push alpha-skill`
```
→ Creating branch feature/alpha-skill-update ...
fatal: a branch named 'feature/alpha-skill-update' already exists
Switched to a new branch 'feature/alpha-skill-update'
  ✓ Branch created
→ Staging and committing changes in alpha-skill/ ...
  ✓ Changes committed
→ Pushing branch feature/alpha-skill-update ...
To /workspace/skills-repo/../project-repo
   a611368..b75b762  feature/alpha-skill-update -> feature/alpha-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "alpha-skill" pushed for review
   Branch: feature/alpha-skill-update
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "alpha-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```

Check what happened in the project repo:

> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git branch --list`
```
  feature/alpha-skill-update
  feature/beta-skill-update
  feature/gamma-skill-update
* master
```
> `git log --oneline --all`
```
b75b762 feat(alpha-skill): update skill instructions
5b41aee feat(gamma-skill): update skill instructions
4ee631e feat(beta-skill): update skill instructions
a611368 feat(alpha-skill): update skill instructions
faf0c18 Initial commit
```
> `git log --oneline feature/alpha-skill-update`
```
b75b762 feat(alpha-skill): update skill instructions
5b41aee feat(gamma-skill): update skill instructions
4ee631e feat(beta-skill): update skill instructions
a611368 feat(alpha-skill): update skill instructions
faf0c18 Initial commit
```

Merge the feature branch:

> `git merge feature/alpha-skill-update --no-edit`
```
Updating 5b41aee..b75b762
Fast-forward
 alpha-skill/SKILL.md | 1 +
 1 file changed, 1 insertion(+)
```
> `git log --oneline`
```
b75b762 feat(alpha-skill): update skill instructions
5b41aee feat(gamma-skill): update skill instructions
4ee631e feat(beta-skill): update skill instructions
a611368 feat(alpha-skill): update skill instructions
faf0c18 Initial commit
```
> `cat alpha-skill/SKILL.md`
```
# Skill: alpha-skill

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
## Updated content for smoke test
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```

Pull the merged changes:

> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
   5b41aee..b75b762  master     -> origin/master
✅ Skills updated successfully
```
> `skills list --verbose`
```
Skills repository: ../project-repo
Groups:           group-1

  ✅ alpha-skill
     This skill provides _____. It can be used for _____. The main features include _____.
     Owner: Your_Name@domain.com
  ○  beta-skill
     This skill provides _____. It can be used for _____. The main features include _____.
     Owner: Your_Name@domain.com
  ✅ gamma-skill
     This skill provides _____. It can be used for _____. The main features include _____.
     Owner: Your_Name@domain.com
  ✅ skills-cli
     Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).
     Owner: your-name@example.com

Active: 3  |  Total: 4
```

## Phase 11: Second push (different skill)

> `skills enable beta-skill`
```
✅ Skill "beta-skill" enabled
→ Applying sparse checkout (4 skill(s)) ...
  ✓ Sparse checkout applied
```
> `echo "## Beta skill content" >> instructions/beta-skill/SKILL.md`
```
```
> `skills push beta-skill`
```
→ Creating branch feature/beta-skill-update ...
fatal: a branch named 'feature/beta-skill-update' already exists
Switched to a new branch 'feature/beta-skill-update'
  ✓ Branch created
→ Staging and committing changes in beta-skill/ ...
  ✓ Changes committed
→ Pushing branch feature/beta-skill-update ...
To /workspace/skills-repo/../project-repo
   4ee631e..352ccf5  feature/beta-skill-update -> feature/beta-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "beta-skill" pushed for review
   Branch: feature/beta-skill-update
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "beta-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```

> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git branch --list`
```
  feature/alpha-skill-update
  feature/beta-skill-update
  feature/gamma-skill-update
* master
```
> `git merge feature/beta-skill-update --no-edit`
```
Updating b75b762..352ccf5
Fast-forward
 beta-skill/SKILL.md | 1 +
 1 file changed, 1 insertion(+)
```
> `git log --oneline`
```
352ccf5 feat(beta-skill): update skill instructions
b75b762 feat(alpha-skill): update skill instructions
5b41aee feat(gamma-skill): update skill instructions
4ee631e feat(beta-skill): update skill instructions
a611368 feat(alpha-skill): update skill instructions
faf0c18 Initial commit
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```

> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
   b75b762..352ccf5  master     -> origin/master
✅ Skills updated successfully
```

## Phase 12: Disable with uncommitted changes

> `echo "## Dirty change" >> instructions/gamma-skill/SKILL.md`
```
```

Should fail — uncommitted changes:

> `skills disable gamma-skill`
```
Error: cannot disable skill "gamma-skill" - uncommitted local changes detected
Commit or discard your changes first, or use --force to override.
```

Force disable — stashes changes:

> `skills disable gamma-skill --force`
```
  ⚠ Stashed uncommitted changes for "gamma-skill" (use 'git stash list' to review)
✅ Skill "gamma-skill" disabled
→ Applying sparse checkout (3 skill(s)) ...
  ✓ Sparse checkout applied
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "alpha-skill",
    "beta-skill"
  ],
  "excluded_skills": [
    "gamma-skill"
  ]
}
```

## Phase 13: Re-init from existing config

> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "alpha-skill",
    "beta-skill"
  ],
  "excluded_skills": [
    "gamma-skill"
  ]
}
```
> `skills init`
```
→ Re-initializing from existing skills.json ...
→ Removing old instructions/ ...
→ Cloning skills repo from ../project-repo ...
Cloning into 'instructions'...
done.
  ✓ Cloned
→ Resolving skills for groups: group-1 ...
  ✓ Resolved 3 skill(s): alpha-skill, beta-skill, skills-cli
→ Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace re-initialized!
   Skills:     alpha-skill, beta-skill, skills-cli
```
> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "alpha-skill",
    "beta-skill"
  ],
  "excluded_skills": [
    "gamma-skill"
  ]
}
```
> `skills list`
```
Skills repository: ../project-repo
Groups:           group-1

  ✅ alpha-skill
  ✅ beta-skill
  ○  gamma-skill
  ✅ skills-cli

Active: 3  |  Total: 4
```
> `skills list --verbose`
```
Skills repository: ../project-repo
Groups:           group-1

  ✅ alpha-skill
     This skill provides _____. It can be used for _____. The main features include _____.
     Owner: Your_Name@domain.com
  ✅ beta-skill
     This skill provides _____. It can be used for _____. The main features include _____.
     Owner: Your_Name@domain.com
  ○  gamma-skill
     This skill provides _____. It can be used for _____. The main features include _____.
     Owner: Your_Name@domain.com
  ✅ skills-cli
     Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).
     Owner: your-name@example.com

Active: 3  |  Total: 4
```

## Phase 13b: Init without groups (global-only)

> `rm -rf /workspace/no-groups-test`
```
```
> `mkdir -p /workspace/no-groups-test`
```
```
> `cd /workspace/no-groups-test`
```
/workspace/no-groups-test
```
> `skills init --repo /workspace/project-repo`
```
ℹ No --groups specified. Initializing with _global.json skills only.
  Use 'skills enable group <name>' later to add group-specific skills.
→ Cloning skills repo from /workspace/project-repo ...
Cloning into 'instructions'...
done.
  ✓ Cloned
→ Resolving skills for groups: (none — global only) ...
  ✓ Resolved 1 skill(s): skills-cli
→ Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace initialized!
   Repository: /workspace/project-repo
   Groups:     (none — global only)
   Skills:     skills-cli
   Location:   instructions/

Your AI agent can now read skills from instructions/<skill-name>/SKILL.md
```
> `cat skills.json`
```
{
  "repo_url": "/workspace/project-repo",
  "groups": [],
  "extra_skills": [],
  "excluded_skills": []
}
```
> `skills list`
```
Skills repository: /workspace/project-repo
Groups:           

  ○  alpha-skill
  ○  beta-skill
  ○  gamma-skill
  ✅ skills-cli

Active: 1  |  Total: 4
```
> `ls instructions/`
```
skills-cli
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `rm -rf /workspace/no-groups-test`
```
```

## Phase 13c: Push with --groups

> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `skills create delta-skill`
```
✅ Skill "delta-skill" created at instructions/delta-skill
   → instructions/delta-skill/SKILL.md
   → instructions/delta-skill/info.json

Edit SKILL.md with your instructions, then use 'skills push' to propose it.
```
> `echo "# Delta Skill" > instructions/delta-skill/SKILL.md`
```
```
> `skills push delta-skill --groups group-1`
```
→ Creating branch feature/delta-skill-update ...
Switched to a new branch 'feature/delta-skill-update'
  ✓ Branch created
→ Staging and committing changes in delta-skill/ ...
  ✓ Changes committed
→ Adding skill to group manifest(s): group-1 ...
  ✓ Added to "group-1"
  ✓ Manifest changes committed
→ Pushing branch feature/delta-skill-update ...
To /workspace/skills-repo/../project-repo
 * [new branch]      feature/delta-skill-update -> feature/delta-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "delta-skill" pushed for review
   Branch: feature/delta-skill-update
   Groups: group-1
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "delta-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```

Verify manifest changes on feature branch in project-repo:

> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git log --oneline -2 feature/delta-skill-update`
```
57cae9c feat(delta-skill): add to groups group-1
584aeea feat(delta-skill): update skill instructions
```
> `git show feature/delta-skill-update:.manifest/group-1.json`
```
{
  "skills": [
    "delta-skill"
  ],
  "sub-configs": [
    "sub-group"
  ]
}
```

Merge the branch and verify on master:

> `git merge feature/delta-skill-update`
```
Updating 352ccf5..57cae9c
Fast-forward
 .manifest/group-1.json | 8 ++++++--
 delta-skill/SKILL.md   | 1 +
 delta-skill/info.json  | 4 ++++
 3 files changed, 11 insertions(+), 2 deletions(-)
 create mode 100644 delta-skill/SKILL.md
 create mode 100644 delta-skill/info.json
```
> `cat .manifest/group-1.json`
```
{
  "skills": [
    "delta-skill"
  ],
  "sub-configs": [
    "sub-group"
  ]
}
```

Back to skills-repo, pull, then create a new skill for new-group:

> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
> `skills pull`
```
→ Pulling latest skills ...
Already on 'master'
From /workspace/skills-repo/../project-repo
 * branch            master     -> FETCH_HEAD
   352ccf5..57cae9c  master     -> origin/master
✅ Skills updated successfully
```
> `skills create epsilon-skill`
```
✅ Skill "epsilon-skill" created at instructions/epsilon-skill
   → instructions/epsilon-skill/SKILL.md
   → instructions/epsilon-skill/info.json

Edit SKILL.md with your instructions, then use 'skills push' to propose it.
```
> `echo "# Epsilon Skill" > instructions/epsilon-skill/SKILL.md`
```
```
> `skills push epsilon-skill --groups new-group`
```
→ Creating branch feature/epsilon-skill-update ...
Switched to a new branch 'feature/epsilon-skill-update'
  ✓ Branch created
→ Staging and committing changes in epsilon-skill/ ...
  ✓ Changes committed
→ Adding skill to group manifest(s): new-group ...
  → Creating new group manifest: new-group.json
  ✓ Added to "new-group"
  ✓ Manifest changes committed
→ Pushing branch feature/epsilon-skill-update ...
To /workspace/skills-repo/../project-repo
 * [new branch]      feature/epsilon-skill-update -> feature/epsilon-skill-update
Switched to branch 'master'
  ✓ Branch pushed

✅ Skill "epsilon-skill" pushed for review
   Branch: feature/epsilon-skill-update
   Groups: new-group
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "epsilon-skill" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```

Verify new-group was created on project-repo feature branch:

> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git show feature/epsilon-skill-update:.manifest/new-group.json`
```
{
  "skills": [
    "epsilon-skill"
  ],
  "sub-configs": []
}
```
> `git merge feature/epsilon-skill-update`
```
Updating 57cae9c..595c251
Fast-forward
 .manifest/new-group.json | 6 ++++++
 epsilon-skill/SKILL.md   | 1 +
 epsilon-skill/info.json  | 4 ++++
 3 files changed, 11 insertions(+)
 create mode 100644 .manifest/new-group.json
 create mode 100644 epsilon-skill/SKILL.md
 create mode 100644 epsilon-skill/info.json
```
> `cat .manifest/new-group.json`
```
{
  "skills": [
    "epsilon-skill"
  ],
  "sub-configs": []
}
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```

## Phase 14: Final state

> `cat skills.json`
```
{
  "repo_url": "../project-repo",
  "groups": [
    "group-1"
  ],
  "extra_skills": [
    "alpha-skill",
    "beta-skill",
    "delta-skill",
    "epsilon-skill"
  ],
  "excluded_skills": [
    "gamma-skill"
  ]
}
```
> `skills list --json`
```
[
  {
    "name": "alpha-skill",
    "active": true,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "beta-skill",
    "active": true,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "delta-skill",
    "active": true,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "gamma-skill",
    "active": false,
    "description": "This skill provides _____. It can be used for _____. The main features include _____.",
    "owner": "Your_Name@domain.com"
  },
  {
    "name": "skills-cli",
    "active": true,
    "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
    "owner": "your-name@example.com"
  }
]
```
> `ls instructions/`
```
alpha-skill
beta-skill
delta-skill
skills-cli
```
> `ls instructions/.manifest/`
```
_global.json
group-1.json
sub-group.json
```

> `cd /workspace/project-repo`
```
/workspace/project-repo
```
> `git log --oneline --all`
```
57cae9c feat(delta-skill): add to groups group-1
595c251 feat(epsilon-skill): add to groups new-group
584aeea feat(delta-skill): update skill instructions
0071bd3 feat(epsilon-skill): update skill instructions
352ccf5 feat(beta-skill): update skill instructions
b75b762 feat(alpha-skill): update skill instructions
5b41aee feat(gamma-skill): update skill instructions
4ee631e feat(beta-skill): update skill instructions
a611368 feat(alpha-skill): update skill instructions
faf0c18 Initial commit
```
> `git branch --list`
```
  feature/alpha-skill-update
  feature/beta-skill-update
  feature/delta-skill-update
  feature/epsilon-skill-update
  feature/gamma-skill-update
* master
```
> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```
