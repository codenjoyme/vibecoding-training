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
- For each approved module, execute the following loop one module at a time:
  + **Step 1: Load instruction.** Read `./instructions/create-training-module.agent.md` to get the full creation workflow and format requirements.
  + **Step 2: Load module description.** Read the corresponding section from `./modules/proposed-modules.md` — extract Elevator Pitch, Training Plan, What the Student Gets, Placement Motivation, and Proposed ID for the current module.
  + **Step 3: Create module.** Follow `create-training-module.agent.md` fully — create folder, `about.md`, `walkthrough.md`, update `training-plan.md`. Use the proposed module description as input instead of asking the user the standard questions (skill, topics, placement, prerequisites, outcome, hands-on steps) — all answers are already in the proposal.
  + **Step 4: Confirm.** Tell the user: "[Module Name] (ID) — created." with a link to the new `about.md`.
  + **Step 5: Next.** Move to the next approved module and repeat from Step 1.
- After all approved modules are created, regenerate the module catalog by reading each `about.md` (same as `generate-module-catalog.agent.md` does).
- Important: reload `create-training-module.agent.md` at the start of EACH module iteration — do not rely on cached content from a previous iteration.
