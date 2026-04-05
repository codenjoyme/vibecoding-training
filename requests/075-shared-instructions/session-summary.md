# Session Summary: Module 075 Redesign

## What We're Working On

Redesigning or updating module **075 — Shared Instructions & Team Conventions** based on research exploring a more advanced, scalable approach to managing AI instructions across teams and services.

## Source Material

The research (`research.md`) documents a fully fleshed-out system with:

- A **central Git repository** as single source of truth for all AI instructions ("skills")
- A **manifest-driven** selection model (`_global.json` + per-group + per-agent via `.manifest/` folder)
- **Sparse checkout** to give developers only the skills they need
- A **Go CLI** (`skills` binary) that abstracts all Git operations and creates PRs automatically
- **Evaluation support** via `evals.json` per skill *(coming soon)*
- A proper **collaboration model** with ownership and approval requirements

This goes significantly further than the current module 075, which covers a simpler team repo + manual Git workflow.

---

## Decisions Made

### 1. Audience level

> **Answer:** The training is for everyone — including developers with no prior experience. Not just managers. All mentions of "managers / non-engineers" should be updated to reflect this broader audience.
>
> How non-technical participants handle the setup: there will be a `SKILL.md` in the module describing how to set up the CLI-based system. An AI agent that reads this skill will guide the user through the setup step by step — no prior technical knowledge required.

### 2. Go CLI — real thing or teaching concept?

> **Answer:** A **real tool** that we build and ship as part of the course.
>
> The module will contain a `tools/` subfolder with the production-ready Go CLI project. Users can download and use it directly. The setup and usage instructions will be in the module's `SKILL.md`. No separate repository — the CLI lives inside this module for now.

### 3. Scope of the module update

> **Answer:** Option C — **split into two modules:**
> - Module **075** stays as the intro (current content, lightly updated) — fundamentals and team adoption
> - Module **076** becomes the advanced system (`.manifest/` folder, sparse checkout, `skills` CLI, governance)

### 4. `evals.json` — include or not?

> **Answer:** Not in this module. Mark as **"coming soon"** in `SKILL.md` and in the research document. Instruction testing/evaluation is a separate topic for later.

### 5. IDE-specific wrappers

> **Answer:** Recommend the **tools-agnostic approach** from `creating-instructions.agent.md`: all instructions are stored as plain Markdown files in a dedicated folder, independent of any agent system or IDE. Each IDE/agent has its own thin adapter wrappers (pointers) to these files. This avoids vendor lock-in and keeps the skill content portable across IDEs (VSCode Copilot, Cursor, Claude Code, etc.).

---

## Plan Forward

Based on decisions above:

1. **Problem framing** — Why individual instructions don't scale across a team
2. **The central skills repo** — Structure, skill anatomy (`SKILL.md` + `README.md`)
3. **Manifest pattern** — `_global.json`, `_agents.json`, `<group-name>.json` via `.manifest/` folder; sub-configs for thematic groups
4. **Sparse checkout workflow** — Only pull what you need (`skills init --groups ...`)
5. **Contribution flow** — Branch → PR → owner review → merge → everyone gets it
6. **Ownership & governance** — Who owns global skills, approval requirements (advisory)
7. **`skills` CLI** — Real tool in `tools/` folder; `SKILL.md` guides setup
8. **evals** — Coming soon, mentioned but not taught

The current module 075 content (COIN adoption pattern, conflict resolution rules, folder structure) maps to points 1, 5, and 6 — reusable material.

---

## What We Are NOT Touching Yet

- Training program order / placement of this module
- Other modules in the curriculum

