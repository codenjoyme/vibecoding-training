# Existing Module 075 — Review Summary

**Module:** `075-shared-instructions-team-conventions`
**Duration:** 15 minutes
**Files:** `about.md`, `walkthrough.md`

---

## What's Already There

### Core Concept (Strong — Keep)

The module frames the central insight correctly: **instructions are organisational knowledge, not personal configuration**. The analogy — when Bob leaves the company, his prompt knowledge walks out with him — is compelling and relatable for a manager audience.

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
| **Manifest / skill selection** | Per-service, per-agent manifest.json | Not mentioned |
| **Sparse checkout** | Partial workspace, only relevant skills | Not mentioned |
| **Skill anatomy** | `skill.md` + `evals.json` + `README.md` per skill | Only `.agent.md` files |
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

## Recommendation Options

### Option A — Light Update (low effort)
Keep current module largely intact. Add a small section referencing the manifest/sparse-checkout pattern as "what a mature system looks like" — point to the research document as extended reading. No structural changes.

### Option B — Module Expansion (medium effort)
Extend the module to ~25–30 minutes. Add Part 7 covering: skill anatomy (`skill.md` + README), manifest pattern, and IDE-agnostic skill design. Keep COIN and conflict resolution.

### Option C — Split into Two Modules (higher effort)
- Module **075** stays as the intro (current content, lightly updated) — for managers
- Module **076** becomes the advanced system (manifest, sparse checkout, CLI concept, evals) — for technical leads

---

*Awaiting decisions from session-summary.md questions before proceeding.*
