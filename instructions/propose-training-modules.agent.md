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
- Build a list of modules to create from the user's answer. Work through them **one at a time**, in ID order.
- For EACH module in the list, execute this exact loop — **do not skip any step, do not batch steps across modules**:

  ### Loop iteration for one module:

  + **Step 1 — READ instruction file (MANDATORY, every iteration).**
    * Call `read_file` on `./instructions/create-training-module.agent.md`.
    * Do NOT skip this even if you read it in a previous iteration. Each iteration is independent.
    * This gives you: folder structure, `about.md` format, `walkthrough.md` format, Prerequisites format, Integration steps, Quality checks.

  + **Step 2 — READ the module section from proposal (MANDATORY, every iteration).**
    * Call `read_file` on `./modules/proposed-modules.md` and extract the full section for the current module.
    * Identify: Proposed ID, Name, Elevator Pitch, Training Plan table, What the Student Gets, Placement Motivation (which contains prerequisite module IDs and dependency reasoning).

  + **Step 3 — CREATE the module folder and files.**
    * Derive folder name from ID and module name: `./modules/[ID]-[descriptive-name]/`.
    * Create `about.md` following exactly the structure from Step 1:
      - Title, Duration (15 min based on course standard), Skill (one actionable sentence), walkthrough link.
      - Topics section — derived from Training Plan steps.
      - Learning Outcome — derived from "What the Student Gets".
      - Prerequisites section with `### Required Modules` (links to actual module folders) and `### Required Skills & Tools` — derived from Placement Motivation dependency list.
    * Create `walkthrough.md` following exactly the structure from Step 1:
      - Introduction paragraph, Prerequisites reference to `about.md`.
      - "What We'll Build/Learn" section.
      - All numbered steps — one step per row in the Training Plan table, expanded into actionable instructions with commands, examples, verification points.
      - Success Criteria section with ✅ checkboxes.
      - Understanding Check section with 5-7 questions and expected answers.
      - Troubleshooting section.
      - Next Steps section.

  + **Step 4 — UPDATE `training-plan.md`.**
    * Read current `./training-plan.md` to find the correct insertion point (based on module ID order).
    * Insert the new module link in the Module Sequence list at the correct position.
    * Format: `1. [Module Name](modules/[folder-name]/about.md) - Brief description`

  + **Step 5 — MARK as done in proposal file.**
    * Edit `./modules/proposed-modules.md`: add `✅` prefix to the module's heading line (e.g., `## ✅ Module N: Name`).
    * This tracks progress and makes it easy to resume if interrupted.

  + **Step 6 — CONFIRM to user.**
    * Report: "✅ **[Module Name]** (`[ID]`) — created. → [modules/folder/about.md](modules/folder/about.md)"
    * Then immediately begin the next module's loop from Step 1.

- After ALL modules in the list are created:
  + Report a summary table: ID | Name | Folder | Status.
  + Remind user to review `training-plan.md` and commit changes to Git.

- **Critical rules:**
  + Never batch-create multiple modules in one step — always complete Steps 1-6 for one module before starting the next.
  + Never skip Step 1 (read instruction) or Step 2 (read proposal) — stale context causes format drift.
  + Always use the actual prerequisite module folder names (check `./modules/` listing if unsure).
  + `walkthrough.md` must NOT contain a prerequisites list — only a reference line to `about.md`.
