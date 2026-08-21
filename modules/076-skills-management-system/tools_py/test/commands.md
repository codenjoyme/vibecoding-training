# Skills CLI - Python Smoke Test

## Phase 1: Clean fixture and help

> `bash /app/test/setup-fixture.sh`
```
```

> `python /app/skills.py help`
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

> `python /app/skills.py ai-help`
```
# Skills CLI - Quick Reference for AI Agents (Python)

The 'skills' CLI manages shared AI skills stored in a central Git repository. A skill is a folder with 'SKILL.md' and optional 'info.json'. The local project stores its configuration in 'skills.json' and receives selected skills under 'instructions/' through sparse checkout.

## Prerequisites

'''bash
python --version
git --version
python skills.py help
'''

Run from 'modules/076-skills-management-system/tools_py/', or install the project with 'python -m pip install .' and call 'skills' directly.

## Commands

'''text
skills init --repo <url|path> [--groups <g1>[,<g2>...]]
'''

Clone the central repository into 'instructions/', resolve '_global.json' plus selected groups/sub-configs, apply sparse checkout, and write 'skills.json'. Groups are optional; omit them for global skills only. If 'skills.json' exists and '--repo' is omitted, reinitialize from the saved config.

'''text
skills pull
'''

Checkout the detected default branch and pull the latest central repository changes.

'''text
skills push <skill-name> [--groups <g1> <g2> ...]
'''

Create 'feature/<skill-name>-update', commit changes under the skill, optionally create/update group manifests and commit them, then push the branch. Prints a PR URL for GitHub/GitLab; local repositories require manual review.

'''text
skills list [--verbose] [--json]
'''

List all top-level skills from Git. Active skills are marked. '--verbose' reads 'description' and 'owner' from 'info.json'; '--json' emits an indented array of '{name, active, description, owner}' objects. Inactive metadata can be read with 'git show' without checkout.

'''text
skills create <skill-name>
'''

Create 'instructions/<skill-name>/SKILL.md' and 'info.json' templates, add the skill to 'extra_skills', and extend sparse checkout.

'''text
skills enable group <group-name>
skills enable <skill-name>
'''

Append a group to 'skills.json' or add an individual skill to 'extra_skills'. If the individual skill was excluded, remove it from 'excluded_skills'. Reapply sparse checkout immediately.

'''text
skills disable [--force] group <group-name>
skills disable [--force] <skill-name>
'''

Remove a group or add an individual skill to 'excluded_skills'. Refuse to remove uncommitted skill changes unless '--force' is used; then stash tracked and untracked files and reapply sparse checkout.

'''text
skills init-repo <folder-name>
'''

Create '.manifest/' example files and the 'skills-cli/' starter skill. Run 'git init', 'git add .', and 'git commit' in the printed folder afterward.

'''text
skills ai-help
skills help
'''

Print this compact AI reference or the general human-oriented help.

## Resolution Priority

'''text
_global.json -> groups and recursive sub-configs -> extra_skills -> minus excluded_skills
'''

All JSON generated by the Python CLI is pretty-printed with two-space indentation. 'sub-configs' keeps its hyphenated manifest key for compatibility.
```

> `python /app/skills.py list; echo exit=$?`
```
Error: not a skills workspace - run 'skills init' first
exit=1
```

> `mkdir -p /workspace/global-project`
```
```

> `cd /workspace/global-project`
```
/workspace/global-project
```

> `python /app/skills.py init --repo ../skills-repo`
```
ℹ No --groups specified. Initializing with _global.json skills only.
  Use 'skills enable group <name>' later to add group-specific skills.
-> Cloning skills repo from ../skills-repo ...
  ✓ Cloned
-> Resolving skills for groups: (none - global only) ...
  ✓ Resolved 1 skill(s): creating-instructions
-> Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace initialized!
   Repository: ../skills-repo
   Groups:     (none - global only)
   Skills:     creating-instructions
   Location:   instructions/

Your AI agent can now read skills from instructions/<skill-name>/SKILL.md
```

> `test -d instructions/creating-instructions && echo global-skill-present`
```
global-skill-present
```

> `test ! -d instructions/code-review-base && echo group-skill-absent`
```
group-skill-absent
```

> `cd /workspace`
```
/workspace
```

> `python /app/skills.py init --help`
```
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

> `python /app/skills.py pull --help`
```
Update local skills from the remote repository.

Usage:
  skills pull
```

> `python /app/skills.py push --help`
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

> `python /app/skills.py list --help`
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

> `python /app/skills.py create --help`
```
Create a new skill in the local instructions/ folder.

Usage:
  skills create <skill-name>

Creates:
  instructions/<skill-name>/SKILL.md   - skill instructions template
  instructions/<skill-name>/info.json  - skill metadata (description, owner)
```

> `python /app/skills.py enable --help`
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

> `python /app/skills.py disable --help`
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

> `python /app/skills.py init-repo --help`
```
Initialize a new skills repository with base structure.

Creates a folder with:
  .manifest/_global.json      - global skills config
  .manifest/group-1.json      - example group config
  .manifest/sub-group.json    - example sub-config
  skills-cli/                 - skill: CLI usage, creating skills, IDE integration

Usage:
  skills init-repo <folder-name>

Examples:
  skills init-repo my-skills-repo
  skills init-repo ../shared-skills
```

## Phase 2: Initialize a grouped workspace

> `mkdir -p /workspace/project-repo`
```
```

> `cd /workspace/project-repo`
```
/workspace/project-repo
```

> `python /app/skills.py init --repo ../skills-repo --groups project-alpha`
```
-> Cloning skills repo from ../skills-repo ...
  ✓ Cloned
-> Resolving skills for groups: project-alpha ...
  ✓ Resolved 4 skill(s): code-review-base, creating-instructions, security-guidelines, style-guidelines
-> Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace initialized!
   Repository: ../skills-repo
   Groups:     project-alpha
   Skills:     code-review-base, creating-instructions, security-guidelines, style-guidelines
   Location:   instructions/

Your AI agent can now read skills from instructions/<skill-name>/SKILL.md
```

> `cat skills.json`
```
{
  "repo_url": "../skills-repo",
  "groups": [
    "project-alpha"
  ],
  "extra_skills": [],
  "excluded_skills": []
}
```

> `find instructions -maxdepth 2 -type f | sort`
```
instructions/.git/HEAD
instructions/.git/config
instructions/.git/config.worktree
instructions/.git/description
instructions/.git/index
instructions/.git/packed-refs
instructions/.manifest/_global.json
instructions/.manifest/project-alpha.json
instructions/.manifest/project-beta.json
instructions/.manifest/security.json
instructions/code-review-base/SKILL.md
instructions/code-review-base/info.json
instructions/creating-instructions/SKILL.md
instructions/creating-instructions/info.json
instructions/security-guidelines/SKILL.md
instructions/security-guidelines/info.json
instructions/style-guidelines/SKILL.md
instructions/style-guidelines/info.json
```

> `python /app/skills.py list`
```
Skills repository: ../skills-repo
Groups:           project-alpha

  ✅ code-review-base
  ✅ creating-instructions
  ✅ security-guidelines
  ✅ style-guidelines
  ○  test-writing

Active: 4  |  Total: 5
```

> `python /app/skills.py list --verbose`
```
Skills repository: ../skills-repo
Groups:           project-alpha

  ✅ code-review-base
     code-review-base description.
     Owner: owner@example.com
  ✅ creating-instructions
     creating-instructions description.
     Owner: owner@example.com
  ✅ security-guidelines
     security-guidelines description.
     Owner: owner@example.com
  ✅ style-guidelines
     style-guidelines description.
     Owner: owner@example.com
  ○  test-writing
     test-writing description.
     Owner: owner@example.com

Active: 4  |  Total: 5
```

> `python /app/skills.py list --json`
```
[
  {
    "name": "code-review-base",
    "active": true,
    "description": "code-review-base description.",
    "owner": "owner@example.com"
  },
  {
    "name": "creating-instructions",
    "active": true,
    "description": "creating-instructions description.",
    "owner": "owner@example.com"
  },
  {
    "name": "security-guidelines",
    "active": true,
    "description": "security-guidelines description.",
    "owner": "owner@example.com"
  },
  {
    "name": "style-guidelines",
    "active": true,
    "description": "style-guidelines description.",
    "owner": "owner@example.com"
  },
  {
    "name": "test-writing",
    "active": false,
    "description": "test-writing description.",
    "owner": "owner@example.com"
  }
]
```

## Phase 3: Enable, disable, and create

> `python /app/skills.py enable group project-beta`
```
✅ Group "project-beta" enabled
-> Applying sparse checkout (5 skill(s)) ...
  ✓ Sparse checkout applied
```

> `test -d instructions/test-writing && echo test-writing-present`
```
test-writing-present
```

> `python /app/skills.py disable group project-beta`
```
✅ Group "project-beta" disabled
-> Applying sparse checkout (4 skill(s)) ...
  ✓ Sparse checkout applied
```

> `test ! -d instructions/test-writing && echo test-writing-removed`
```
test-writing-removed
```

> `python /app/skills.py enable test-writing`
```
✅ Skill "test-writing" enabled
-> Applying sparse checkout (5 skill(s)) ...
  ✓ Sparse checkout applied
```

> `python /app/skills.py disable test-writing`
```
✅ Skill "test-writing" disabled
-> Applying sparse checkout (4 skill(s)) ...
  ✓ Sparse checkout applied
```

> `python /app/skills.py create local-skill`
```
✅ Skill "local-skill" created at instructions/local-skill
   -> instructions/local-skill/SKILL.md
   -> instructions/local-skill/info.json

Edit SKILL.md with your instructions, then use 'skills push' to propose it.
```

> `cat instructions/local-skill/info.json`
```
{
  "description": "This skill provides _____. It can be used for _____. The main features include _____.",
  "owner": "Your_Name@domain.com"
}
```

> `cat skills.json`
```
{
  "repo_url": "../skills-repo",
  "groups": [
    "project-alpha"
  ],
  "extra_skills": [
    "local-skill"
  ],
  "excluded_skills": [
    "test-writing"
  ]
}
```

## Phase 4: Push a skill and update its group manifests

> `printf '\n- Smoke-test review check\n' >> instructions/code-review-base/SKILL.md`
```
```

> `python /app/skills.py push code-review-base --groups project-beta extra-group`
```
-> Creating branch feature/code-review-base-update ...
  ✓ Branch created
-> Staging and committing changes in code-review-base/ ...
  ✓ Changes committed
-> Adding skill to group manifest(s): project-beta, extra-group ...
  ✓ Added to "project-beta"
  -> Creating new group manifest: extra-group.json
  ✓ Added to "extra-group"
  ✓ Manifest changes committed
-> Pushing branch feature/code-review-base-update ...
  ✓ Branch pushed

✅ Skill "code-review-base" pushed for review
   Branch: feature/code-review-base-update
   Groups: project-beta, extra-group
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "code-review-base" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```

> `cd /workspace/skills-repo`
```
/workspace/skills-repo
```

> `git branch --list`
```
  feature/code-review-base-update
* master
```

> `git log --oneline --all`
```
40ebdd5 feat(code-review-base): add to groups project-beta, extra-group
827ad07 feat(code-review-base): update skill instructions
dc7ee95 init: smoke-test skills repository
```

> `git checkout master`
```
Already on 'master'
```

> `git merge feature/code-review-base-update`
```
Updating dc7ee95..40ebdd5
Fast-forward
 .manifest/extra-group.json  | 6 ++++++
 .manifest/project-beta.json | 5 ++++-
 code-review-base/SKILL.md   | 2 ++
 3 files changed, 12 insertions(+), 1 deletion(-)
 create mode 100644 .manifest/extra-group.json
```

> `cd /workspace/project-repo`
```
/workspace/project-repo
```

> `python /app/skills.py pull`
```
-> Pulling latest skills ...
✅ Skills updated successfully
```

> `printf '\n- Second smoke-test review check\n' >> instructions/code-review-base/SKILL.md`
```
```

> `python /app/skills.py push code-review-base`
```
-> Creating branch feature/code-review-base-update ...
  ✓ Branch created
-> Staging and committing changes in code-review-base/ ...
  ✓ Changes committed
-> Pushing branch feature/code-review-base-update ...
  ✓ Branch pushed

✅ Skill "code-review-base" pushed for review
   Branch: feature/code-review-base-update
   (local repository - request a review from the skill owner)

⚠  Note: switched back to the main branch - skill "code-review-base" may not be visible locally.
   After the PR is merged, run 'skills pull' to get it back.
```

## Phase 5: Force disable and reinitialize

> `printf 'local uncommitted note\n' > instructions/security-guidelines/untracked.txt`
```
```

> `python /app/skills.py disable security-guidelines`
```
Error: cannot disable skill "security-guidelines" - uncommitted local changes detected
Commit or discard your changes first, or use --force to override.
```

> `python /app/skills.py disable security-guidelines --force`
```
  ⚠ Stashed uncommitted changes for "security-guidelines" (use 'git stash list' to review)
✅ Skill "security-guidelines" disabled
-> Applying sparse checkout (4 skill(s)) ...
  ✓ Sparse checkout applied
```

> `git -C instructions stash list`
```
stash@{0}: On master: skills-cli: auto-stash for security-guidelines
```

> `python /app/skills.py init`
```
-> Re-initializing from existing skills.json ...
-> Removing old instructions/ ...
-> Cloning skills repo from ../skills-repo ...
  ✓ Cloned
-> Resolving skills for groups: project-alpha ...
  ✓ Resolved 4 skill(s): code-review-base, creating-instructions, local-skill, style-guidelines
-> Applying sparse checkout ...
  ✓ Sparse checkout applied

✅ Skills workspace re-initialized!
   Skills:     code-review-base, creating-instructions, local-skill, style-guidelines
```

> `python /app/skills.py list --json`
```
[
  {
    "name": "code-review-base",
    "active": true,
    "description": "code-review-base description.",
    "owner": "owner@example.com"
  },
  {
    "name": "creating-instructions",
    "active": true,
    "description": "creating-instructions description.",
    "owner": "owner@example.com"
  },
  {
    "name": "security-guidelines",
    "active": false,
    "description": "security-guidelines description.",
    "owner": "owner@example.com"
  },
  {
    "name": "style-guidelines",
    "active": true,
    "description": "style-guidelines description.",
    "owner": "owner@example.com"
  },
  {
    "name": "test-writing",
    "active": false,
    "description": "test-writing description.",
    "owner": "owner@example.com"
  }
]
```

## Phase 6: Bootstrap another central repository

> `python /app/skills.py init-repo /workspace/generated-repo`
```
-> Creating skills repository at /workspace/generated-repo ...
  ✓ Files created

✅ Skills repository initialized at /workspace/generated-repo

Next steps:
  cd /workspace/generated-repo
  git init && git add . && git commit -m "init: skills repository"
  # Then push to your Git hosting
```

> `find /workspace/generated-repo -maxdepth 3 -type f | sort`
```
/workspace/generated-repo/.gitignore
/workspace/generated-repo/.manifest/_global.json
/workspace/generated-repo/.manifest/group-1.json
/workspace/generated-repo/.manifest/sub-group.json
/workspace/generated-repo/skills-cli/SKILL.md
/workspace/generated-repo/skills-cli/info.json
```

> `python -c "import json; print(json.dumps(json.load(open('/workspace/generated-repo/.manifest/_global.json')), indent=2))"`
```
{
  "skills": [
    "skills-cli"
  ]
}
```

## Phase 7: Error paths

> `python /app/skills.py unknown-command`
```
Error: unknown command "unknown-command"

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

> `python /app/skills.py list`
```
Skills repository: ../skills-repo
Groups:           project-alpha

  ✅ code-review-base
  ✅ creating-instructions
  ○  security-guidelines
  ✅ style-guidelines
  ○  test-writing

Active: 3  |  Total: 5
```
