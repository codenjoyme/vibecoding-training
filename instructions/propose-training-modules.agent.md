- Analyze the current training program module-by-module to identify gaps in coverage.
- Use the module catalog (`./modules/module-catalog.md`) and training plan (`./training-plan.md`) as primary sources.
- Read `about.md` from each module in `./modules/` to understand detailed content and dependencies.
- Compare covered topics against the broader GenAI/AI-assisted development landscape:
  + Security: code review, secret management, vulnerability scanning.
  + Testing: unit tests, snapshot testing, test generation.
  + Quality: output evaluation, hallucination metrics, cross-validation.
  + DevOps: CI/CD with AI agents, automated pipelines, deployment.
  + Team: shared instructions, onboarding, conventions, cost management.
  + Architecture: multi-agent orchestration, structured output, data pipelines.
  + Practical: refactoring, debugging, database design, data analysis.
- For each proposed module, produce a structured description containing:
  + **Proposed ID** — a 3-digit number fitting into the existing numbering scheme (gaps: `062-069`, `075-079`, `085-089`, `106-109`, `126-129`, `131-139`, `141-149`, `151-159`, `161-164`, `191-249`, `251-299`).
  + **Elevator Pitch** — 2-3 sentence hook explaining why this module matters.
  + **Training Plan** — step-by-step table (Step | What happens) with 4-8 concrete steps.
  + **What the Student Gets** — 3-5 bullet points of tangible outcomes.
  + **Placement Motivation** — why this ID, which modules it depends on, and why this position in the sequence is logical.
- Include special attention to any topics the user explicitly requests (e.g. snapshot testing, specific frameworks).
- At the end of the document, include:
  + A summary table of all proposed modules with ID, Name, and Phase.
  + An updated learning path showing all existing + proposed modules in sequence (mark new ones with ★).
  + A dependency graph showing what each new module depends on.
- Save the output file to `./modules/proposed-modules.md`.
- Use English for all file content, respond to user in their language.
- Do not create actual module folders during Phase 1 — this is a proposal document only.

## Phase 2: Module Creation (after user approval)

- After presenting the proposal, ask the user: "Which modules would you like to create? List the IDs, or say 'all' to create all proposed modules."
- Wait for explicit user confirmation before proceeding.
- Build the list of approved modules in ID order. Then process them **one module at a time**.

### ⚠️ MANDATORY LOOP — one full iteration per module, no exceptions

For EACH module, before doing anything else, execute ALL of the following steps in order. **No step may be skipped. No step may reference "already read above" or "read in a previous iteration". Every step is a fresh read.**

---

**STEP 1 — CALL `read_file` on `./instructions/create-training-module.agent.md` — READ THE ENTIRE FILE.**
- This is not optional. This is not "already done". Call it. Read it fresh. Read it FULLY — startLine=1, endLine=999 (or whatever covers the whole file).
- Do NOT read only a partial range (e.g. lines 42–80). That is a violation of this step. The full file must be loaded in one or two calls covering all lines.
- Context drift is real: a partial read silently omits quality checks, naming conventions, integration steps, and walkthrough structure — causing the output to deviate from the required format.
- Extract from it: folder structure rules, `about.md` required sections and order, `walkthrough.md` required sections and order, Prerequisites exact format, Integration steps (update training-plan.md), Naming Conventions, Quality Checklist.
- Do not proceed to Step 2 until the COMPLETE file content is in front of you as a result of a tool call in this iteration.

---

**STEP 2 — CALL `read_file` on `./modules/proposed-modules.md` and locate the section for the CURRENT module.**
- This is not optional. This is not "already seen". Call it. Read the relevant section fresh.
- Extract: Proposed ID, Name, Elevator Pitch, all rows of the Training Plan table, What the Student Gets bullets, Placement Motivation (contains prerequisite module IDs).
- Do not proceed to Step 3 until the content is in your current tool call result.

---

**STEP 3 — CREATE `about.md` for this module.**
- Folder: `./modules/[ID]-[descriptive-name]/about.md`
- Use the structure from Step 1 (create-training-module instruction), content from Step 2 (proposal).
- Required sections in order: Title, Duration (15 min), Skill (one actionable sentence), walkthrough link, Topics, Learning Outcome, Prerequisites.
- Prerequisites format EXACTLY as specified in the instruction from Step 1:
  - `### Required Modules` — each as `- [ID — Title](../folder/about.md)`
  - `### Required Skills & Tools` — plain bullet list

---

**STEP 4 — CREATE `walkthrough.md` for this module.**
- File: `./modules/[ID]-[descriptive-name]/walkthrough.md`
- Use the structure from Step 1 (create-training-module instruction), content from Step 2 (proposal).
- Required sections: title, intro paragraph, Prerequisites (reference to `about.md` only — no list), What We'll Cover, one section per Training Plan row (expanded with commands, examples, verification), Success Criteria (✅ checkboxes), Understanding Check (5-7 questions with answers), Troubleshooting, Next Steps.
- `walkthrough.md` must NOT duplicate the prerequisites list — only: `See [module overview](about.md) for full prerequisites list.`

---

**STEP 5 — UPDATE `./training-plan.md`.**
- Read the current file to find the correct insertion point by module ID order.
- Insert: `1. [Module Name](modules/[folder]/about.md) - Brief description`
- Use `replace_string_in_file` to insert at the exact correct position.

---

**STEP 6 — MARK the module as done in `./modules/proposed-modules.md`.**
- Edit the heading of the current module section: `## Module N: Name` → `## ✅ Module N: Name`
- This is the progress checkpoint. If the session is interrupted, this shows where to resume.

---

**STEP 7 — CONFIRM to user.**
- Output exactly: "✅ **[Module Name]** (`[ID]`) — created. → [modules/folder/about.md](modules/folder/about.md)"
- Then **go back to STEP 1** for the next module in the list. Do not skip STEP 1.

---

- After ALL modules are done: show a summary table (ID | Name | Folder | Status) and remind to commit to Git.

### ⚠️ PROHIBITED patterns — if you catch yourself doing any of these, stop and restart the loop step:
- "Step 1 already done in this session" → NO. Call `read_file` again.
- "Instruction read above" → NO. Call `read_file` again.
- "Section from proposed-modules.md seen earlier" → NO. Call `read_file` again.
- Creating two modules before confirming the first → NO. One module = complete Steps 1-7 = confirm = then next module.
- Batching `about.md` + `walkthrough.md` across multiple modules in one response → NO.
