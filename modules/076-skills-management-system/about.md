# Advanced Skills Management System

**Duration:** 30 minutes

**Skill:** Set up a centralized AI skills repository with manifest-driven sparse checkout and the `skills` CLI to manage team-wide AI instructions at scale.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why individual AI instructions don't scale across teams and repositories
- Central skills repository structure: the `.manifest/` pattern with `_global.json`, `_agents.json`, and per-group config files
- The `SKILL.md` convention — IDE-agnostic, plain Markdown skill content
- Installing and using the `skills` CLI (cross-platform Go binary)
- Sparse checkout — pull only the skills your project needs
- Contribution workflow — branch → PR → owner review → merge → team-wide update
- Ownership and governance model (advisory)

## Learning Outcome

You have a working centralized skills repository with a proper manifest structure, sparse checkout configured for two independent project workspaces, and the `skills` CLI installed and tested — ready to introduce to your team.

## Prerequisites

### Required Modules

- [075 — Shared Instructions & Team Conventions](../075-shared-instructions-team-conventions/about.md)
- [060 — Version Control with Git](../060-version-control-git/about.md)
- [103 — CLI (Command Line Interface)](../103-cli-command-line-interface/about.md) *(optional, recommended)*

### Required Skills & Tools

- Git installed and configured (version 2.25 or later for sparse checkout support)
- Terminal / Command Prompt access
- Text editor or IDE (VS Code, Cursor, or any editor)
- Go 1.21+ (we install this as part of the module)

## When to Use

Apply this module when:

- Your team has outgrown a single shared instructions file and needs per-project skill selection
- Multiple teams or services need different subsets of a shared instruction library
- You want a scalable, Git-based workflow for creating, reviewing, and distributing AI instructions
- You need `skills` CLI to automate sparse checkout and PR creation

## Resources

- [Go official downloads](https://go.dev/dl/) — for installing Go
- [Git sparse checkout docs](https://git-scm.com/docs/git-sparse-checkout) — reference
- [Module 075 — Shared Instructions](../075-shared-instructions-team-conventions/about.md) — foundation concepts
- `tools/SKILL.md` — operator guide for the skills management system (read this with your AI agent)
