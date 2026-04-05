# Instructions Management System
## Git + Sparse Checkout + Go CLI

---

## Overview

This document defines a lightweight, scalable system for managing AI instructions (prompts) across multiple microservices and teams. The system is based on Git as the source of truth, sparse checkout for partial workspace usage, and a cross-platform Go-based CLI distributed as a single binary.

The system is designed to support:

- Multi-repository environments
- Cross-team collaboration
- Reusable and composable instruction units ("skills")
- Minimal infrastructure (no heavy LLMOps platform)

---

## Core Principles

| Principle | Description |
|---|---|
| **Git is the single source of truth** | All instructions are stored in a single central Git repository. |
| **Instructions are modular** | Each instruction is a self-contained "skill" stored in its own directory. |
| **No duplication** | Each skill exists only once and can be reused across services. |
| **Selection via manifest** | A global manifest defines which skills are used by which services or agents. |
| **Partial workspace via sparse checkout** | Developers only pull the subset of skills they need. |
| **CLI abstraction** | A Go CLI abstracts Git operations, sparse checkout, and PR workflows. |

---

## Repository Structure

All instructions are stored in a single flat repository, where each skill is a directory:

```
.instructions/repo/
├── manifest.json
├── code-review-base/
│   ├── skill.md
│   ├── evals.json
│   └── README.md
├── code-review-gpt/
│   ├── skill.md
│   ├── evals.json
│   └── README.md
├── security-guidelines/
│   ├── skill.md
│   └── README.md
├── style-guidelines/
│   ├── skill.md
│   └── README.md
└── agent-copilot/
    ├── skill.md
    ├── evals.json
    └── README.md
```

**Key rules:**

- Each directory = one skill
- `skill.md` = main instruction content
- `evals.json` = optional test cases
- `README.md` = metadata (owner, description)
- No nested hierarchy required (flat structure)

---

## Manifest Configuration

The manifest defines which skills are used by which services and agents.

**Example `manifest.json`:**

```json
{
  "global": ["style-guidelines"],
  "services": {
    "service1": ["code-review-base", "security-guidelines"],
    "service2": ["code-review-gpt", "security-guidelines"],
    "service3": ["code-review-base", "code-review-gpt"]
  },
  "agents": {
    "copilot": ["agent-copilot"],
    "cursor": []
  }
}
```

**Rules:**

- `"global"` skills are always included for everyone
- `services` defines per-microservice skill usage
- `agents` defines tool-specific skill usage
- Skills are referenced by directory name

---

## Local Workflow

All operations are performed via CLI.

### Initialization

```bash
instructions init --service <service-name>
```

**Behavior:**
1. Clone the central repository into `.instructions/repo`
2. Read `manifest.json`
3. Resolve required skills: `global` + `services[service-name]`
4. Perform sparse checkout for only required skill directories

**Result:** Only relevant skills exist locally.

### Working with Skills

Developers edit files directly:

```
.instructions/repo/<skill-name>/skill.md
```

Optionally also update:
- `evals.json`
- `README.md`

### Push Changes

```bash
instructions push <skill-name>
```

**Behavior:**
1. Create a new branch: `feature/<skill-name>-update`
2. Stage only modified files
3. Commit changes
4. Push to remote
5. Automatically create Pull Request
6. Return PR URL

### Pull Updates

```bash
instructions pull
```

**Behavior:**
- `git pull` on repository
- Re-apply sparse checkout if needed

---

## Sparse Checkout Strategy

Sparse checkout is used to limit local files to only what's needed.

CLI internally executes:

```bash
git sparse-checkout init --cone
git sparse-checkout set <skill-1> <skill-2> ...
```

Skills are resolved from the manifest automatically.

**Advantages:**
- Minimal local footprint
- No duplication
- Full Git compatibility
- Clean diffs and commits

---

## Skill Design

Each skill directory contains:

### `skill.md`

Main instruction content — written in plain Markdown, IDE-agnostic.

### `evals.json` *(optional)*

Test cases for automated validation:

```json
[
  {
    "input": "example code",
    "expected": "should mention error handling"
  }
]
```

### `README.md`

Metadata for the skill:

- **Description** — what this skill does
- **Owner** — who is responsible
- **Usage context** — when to apply it

---

## Prompt Composition

The final prompt is constructed dynamically by concatenating:

```
final_prompt = global skills + service skills + model-specific skills (optional)
```

Model-specific variants can be implemented as separate skills:

| Skill | Target model |
|---|---|
| `code-review-base` | Any model |
| `code-review-gpt` | GPT-4 optimized |
| `code-review-claude` | Claude optimized |

---

## Versioning

Versioning is handled entirely via Git:

- **Commit hash** = version identifier
- **Branches** for development and review
- **Tags** for releases *(optional)*

---

## Collaboration Model

- Each skill has an **owner** (defined in `README.md`)
- **PR required** for all changes — no direct commits to main
- Minimum **1 approval** from skill owner before merge
- **Global skills require 2 approvals** (they affect everyone)

---

## Conflict Management

Best practices to minimize conflicts:

- Small, focused PRs
- One logical change per PR
- Avoid editing multiple skills in one PR
- Prefer splitting large prompts into multiple skills

---

## Go CLI Architecture

### Overview

The CLI is implemented in Go and distributed as a single binary.

**Key properties:**

- Cross-platform (Windows, macOS, Linux)
- No runtime dependencies
- Single executable file

### CLI Commands

| Command | Description |
|---|---|
| `instructions init --service <name>` | Initialize workspace with sparse checkout |
| `instructions pull` | Update local instructions from remote |
| `instructions push <skill-name>` | Push changes and create a PR |
| `instructions list` | List all available skills |
| `instructions eval <skill-name>` | Run evals for a skill against LLM |

### Internal Modules (Go)

| Module | Responsibility |
|---|---|
| **manifest loader** | Read `manifest.json`, resolve skill dependencies |
| **git manager** | Clone repo, pull updates, create branches, commit and push |
| **sparse manager** | Configure sparse checkout, update selected skills |
| **PR integration** | Create pull requests via Git provider API |
| **eval runner** | Run eval cases against LLM |

---

## Distribution

The CLI is compiled into platform-specific binaries:

| Platform | Binary |
|---|---|
| Windows | `instructions.exe` |
| Linux / macOS | `instructions` |

**Distribution methods:**

- GitHub Releases (public or private)
- Internal artifact storage / package registry

---

## Limitations

This system does **NOT** provide:

- Real-time runtime updates (instructions are loaded at startup)
- Built-in A/B testing infrastructure
- Advanced observability dashboards

These can be added later as extensions if needed.

---

## Future Extensions

- Add logging of prompt usage per service
- Add evaluation pipelines in CI/CD
- Add remote prompt registry layer
- Add dynamic runtime fetching for hot-reload

---

## Summary

This system provides:

| Feature | Implementation |
|---|---|
| Centralized instruction management | Single Git repository |
| Modular reusable skills | One directory per skill |
| Partial workspace | Git sparse checkout |
| Cross-platform tooling | Go CLI single binary |
| Scalable collaboration | PR-based workflow with owners |

> It achieves ~80–90% of LLMOps functionality with minimal infrastructure complexity.
