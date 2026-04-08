# Existing Module 075 — Review Summary

**Module:** `075-shared-instructions-team-conventions`
**Duration:** 15 minutes
**Files:** `about.md`, `walkthrough.md`
**Audience:** All developers and team members — beginners to experienced. Not limited to managers.

---

## What's Already There

### Core Concept (Strong — Keep)

The module frames the central insight correctly: **instructions are organisational knowledge, not personal configuration**. The analogy — when Bob leaves the company, his prompt knowledge walks out with him — is compelling and relatable for any audience.

### Structure (Part by Part)

| Part | Topic | Assessment |
|---|---|---|
| **Part 1** | The Inconsistency Problem | ✅ Strong. Good table showing Alice/Bob/Carol getting different AI quality. Clear business framing. |
| **Part 2** | Shared Repo Folder Structure | ✅ Solid. Practical `team-instructions/` layout with `instructions/`, `conventions/`, `templates/`. Hands-on shell commands included. |
| **Part 3** | Populate First Instruction | ✅ Good entry point. Building on module 070 output, easy first step. |
| **Part 4** | Git-Based Distribution | ✅ Covers init, push to GitHub, fork/branch PR workflow. Practical and correct. |
| **Part 5** | Conflict Resolution | ✅ Useful. The 4-rule priority system (specific > general, last-merged wins, explicit > implicit, when in doubt open an issue) is actionable. |
| **Part 6** | Adoption Strategy | ✅ The COIN pattern (Copy → Observe → Improve → Normalise) is the most unique and valuable piece of this module. Very practical for managers. |

### Learning Outcome

> "You have a template shared-instructions repository structure, understand instructions-as-code workflow, and have a concrete adoption playbook to introduce shared instructions to your team."

This is a **good, achievable outcome** for 15 minutes. Scope is appropriate.

---

## What Could Be Improved

### Gaps compared to the research

| Gap | Research has | Current module has |
|---|---|---|
| **Manifest / skill selection** | Per-project `.manifest/` folder with `global.json`, `agents.json`, and `<project-name>.json` files | Not mentioned |
| **Sparse checkout** | Partial workspace, only relevant skills | Not mentioned |
| **Skill anatomy** | `SKILL.md` + `evals.json` *(coming soon)* + `README.md` per skill | Only `.agent.md` files |
| **Ownership model** | Owner field in README, approval gates | Mentioned briefly in conflict resolution |
| **IDE-agnostic core** | Central `skill.md`, thin IDE wrappers | Somewhat VSCode/Cursor aware, no clear pattern |
| **CLI abstraction** | Go binary hides Git complexity | Manual Git commands throughout |
| **Evaluation** | `evals.json` for testing instruction quality | Not mentioned |

### Minor issues

- Folder structure uses `.agent.md` naming which is VSCode-specific; `skill.md` from the research is more IDE-agnostic
- The `instructions pull` step for consumers feels underpowered — just `git pull`, no mention of sparse checkout updates
- No mention of what happens when the central repo grows to 50+ skills — discoverability problem

---

## What Definitely Should Stay

| Element | Why keep it |
|---|---|
| The inconsistency problem framing (Part 1) | Best business case hook in the module |
| The COIN adoption pattern (Part 6) | Unique, practical, manager-relevant |
| Conflict resolution rules (Part 5) | Concrete, actionable, fills a real gap |
| Git PR contribution workflow (Part 4) | Core mechanic — must stay |
| Hands-on commands | Keeps it practical |

---

## Recommendation: Decision Made

**Option C selected** — split into two modules:

### Module 075 (stays, light update)

Keep all current content. Audience framing updated from “managers” to “everyone”. Add a reference to module 076 at the end as the next step for teams ready to go deeper.

### Module 076 (new) — Advanced Skills Management System

Covers the full system from `research.md`:
- `.manifest/` folder with `_global.json`, `_agents.json`, `<group-name>.json`, sub-configs
- `SKILL.md` convention and skill anatomy
- `skills` CLI (real tool in `tools/` folder)
- Sparse checkout workflow
- Ownership & governance (advisory)
- `evals.json` — coming soon

*A `SKILL.md` inside the module will guide any user (including beginners) through CLI setup with the help of an AI agent.*
