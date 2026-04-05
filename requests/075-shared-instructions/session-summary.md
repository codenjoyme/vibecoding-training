# Session Summary: Module 075 Redesign

## What We're Working On

Redesigning or updating module **075 — Shared Instructions & Team Conventions** based on research exploring a more advanced, scalable approach to managing AI instructions across teams and services.

## Source Material

The research (`research.md`) documents a fully fleshed-out system with:

- A **central Git repository** as single source of truth for all AI instructions ("skills")
- A **manifest-driven** selection model (global + per-service + per-agent)
- **Sparse checkout** to give developers only the skills they need
- A **Go CLI** (`instructions` binary) that abstracts all Git operations and creates PRs automatically
- **Evaluation support** via `evals.json` per skill
- A proper **collaboration model** with ownership and approval requirements

This goes significantly further than the current module 075, which covers a simpler team repo + manual Git workflow.

---

## Clarifying Questions Before We Start

Before touching the module, I need your decisions on the following:

### 1. Audience level

> The current module targets managers / non-engineers learning AI-assisted development. The research system (Go CLI, sparse checkout, `.manifest/` folder) is **developer/DevOps territory**.
>
> **Question:** Are we redesigning this for a technical audience, or do we need to keep it accessible for non-engineers? Or split into two tiers?

### 2. Go CLI — real thing or teaching concept?

> The research describes a Go CLI as a distribution mechanism. Building one is a full engineering sprint, not a training exercise.
>
> **Question:** Should the CLI be:
> - (a) A **real tool** we build and publish as part of the course?
> - (b) A **conceptual teaching example** — "here's what a mature system looks like"?
> - (c) **Out of scope** — focus on Git + manifest pattern only, teach the concept without building the binary?

### 3. Scope of the module update

> Right now module 075 is 15 minutes and covers basic shared repo structure + Git workflow.
>
> **Question:** Is the goal to:
> - (a) **Replace** the current module entirely with the new system?
> - (b) **Extend** it — keep current content as foundation, add the advanced system as a separate "Part 2" or a new module (e.g., 076)?
> - (c) **Keep the current module** as-is but add a reference/appendix to the advanced approach?

### 4. `evals.json` — include or not?

> The research includes an evaluation framework for instructions (test cases that run against an LLM).
>
> **Question:** Is evaluation / testing of instructions something we want to teach in this module, or is that a separate topic for later?

### 5. IDE-specific wrappers

> The research system is IDE-agnostic at the core. The current module 075 mentions VSCode + Cursor compatibility but doesn't go deep.
>
> **Question:** Should we include a section on how the central `skill.md` files map to IDE-specific wrapper formats (`.github/prompts/`, `.cursor/rules/`)?

---

## Preliminary Plan (pending your answers)

Based on the research, the likely structure of the updated/new module would be:

1. **Problem framing** — Why ad-hoc individual instructions don't scale across a team
2. **The central skills repo** — Structure, skill anatomy (`skill.md` + `README.md`)
3. **Manifest pattern** — Global (`global.json`), agent-specific (`agents.json`), and per-project (`<project-name>.json`) skill selection via `.manifest/` folder
4. **Sparse checkout workflow** — Only pull what you need
5. **Contribution flow** — Branch → PR → owner review → merge → everyone gets it
6. **Ownership & governance** — Who owns global skills, approval requirements
7. **CLI concept** — Abstract Git complexity away (build vs. concept TBD)
8. **evals** — Optional: how to test instruction quality

The current module's content (COIN adoption pattern, conflict resolution rules, folder structure) maps partially to points 1, 5, and 6 — so there's reusable material.

---

## What We Are NOT Touching Yet

- Training program order / placement of this module
- Other modules in the curriculum
