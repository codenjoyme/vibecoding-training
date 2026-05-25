# AI Delegation Mindset for Team Leads - Hands-on Walkthrough

In this walkthrough, you will delegate one real task to an AI agent, verify the result with a lightweight checklist, and set up a repeatable 30-day daily habit.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this module, you will have:

- A first delegation brief for a real task from your work
- A lightweight verification checklist for non-micromanaging oversight
- A 30-day delegation log to build a 1-task-per-day habit
- A reusable self-sustaining delegation loop for your team

This matters because strong delegation creates leverage: you spend less time doing each task yourself and more time improving the system that delivers reliable results.

## Part 1: Reframe Your Role from Doer to System Designer

### What we'll do

You will quickly compare the old execution style with an AI delegation style, then pick one concrete task for today.

1. Open your active project workspace (`c:/workspace/hello-genai/` on Windows or `~/workspace/hello-genai/` on macOS/Linux).
2. In your notes, list 5 common team-lead tasks from this week (for example: bug triage, small refactor, test gap fix, release note draft, onboarding checklist update).
3. For each task, write two lines:
   - **Old way:** how you usually do it manually
   - **AI delegation way:** what part the agent can execute while you keep oversight
4. Choose one task that is:
   - clear and bounded (can finish in one PR or one deliverable)
   - low-to-medium risk
   - easy to verify with tests, diffs, or checklist review

### What happened

You transformed delegation from an abstract idea into one concrete candidate task. This is the key to building daily execution consistency.

## Part 2: Write a Delegation Brief the Agent Can Execute

### What we'll do

You will prepare a brief with context, constraints, and acceptance criteria so the agent can run autonomously.

1. Open your AI assistant in **Agent Mode** and choose **Claude Sonnet 4.5** (recommended).
2. Paste this template into your AI assistant chat interface, fill it with your real task details, then send the complete filled template as one message in that same chat:

```markdown
Task: [one clear deliverable]

Context:
- Repository/project:
- Why this task matters now:
- Relevant files/modules:

Constraints:
- Do not change unrelated files
- Follow existing project conventions
- Keep changes minimal and testable

Acceptance criteria:
- [ ] Functional outcome is complete
- [ ] Existing tests pass (or justified if no tests exist)
- [ ] New/updated checks for changed behavior are included when needed
- [ ] PR description explains what changed and why

Verification evidence to return:
- Summary of files changed
- Test/lint/build commands executed and results
- Risks/edge cases considered
```

3. Add one explicit anti-micromanagement rule: "Make decisions autonomously within constraints; ask only for blockers."
4. Add one explicit anti-blind-trust rule: "Return verifiable evidence for each acceptance criterion."

### What happened

You converted leadership intent into an executable delegation contract. This is the core skill that determines agent quality.

## Part 3: Execute the Delegation and Monitor at the Right Level

### What we'll do

You will run the brief and supervise progress through checkpoints, not constant intervention.

1. Submit the brief to your agent.
2. Let the agent work without interrupting every step.
3. Check only at predefined points:
   - after plan creation
   - after first meaningful code/content change
   - before final validation and handoff
4. If the agent gets stuck, respond with constraint-level guidance (goals, boundaries, acceptance criteria), not line-by-line commands.

### What happened

You practiced oversight without micromanagement. You kept control through checkpoints and criteria, not through continuous manual steering.

## Part 4: Verify Results with a Lightweight Checklist

### What we'll do

You will verify outcomes fast and systematically, focusing on trust signals rather than full manual rework.

1. Use this checklist for today’s delegated task:

```markdown
Verification Checklist
- [ ] Scope is correct (no unrelated changes)
- [ ] Acceptance criteria are fully addressed
- [ ] Evidence is provided (tests, logs, diffs, screenshots when relevant)
- [ ] Risky areas reviewed (security, data integrity, production impact)
- [ ] Follow-up actions are captured (if anything is deferred)
```

2. Mark each item as pass/fail.
3. If any item fails, decide:
   - **Take back control now** when production risk is high or requirements were misunderstood critically.
   - **Improve the system** when failure is process-related (missing context, weak acceptance criteria, unclear instruction).

### What happened

You used a repeatable quality gate. This prevents both extremes: blind approval and time-consuming micromanagement.

## Part 5: Start the 30-Day 1-Task-Per-Day Habit Tracker

### What we'll do

You will create a simple log so delegation becomes a durable leadership behavior.

1. Create a file in your project notes area, for example:
   - `c:/workspace/hello-genai/delegation-log.md` (Windows)
   - `~/workspace/hello-genai/delegation-log.md` (macOS/Linux)
2. Paste this template:

```markdown
# 30-Day AI Delegation Log

| Day | Task | Brief Quality (1-5) | Verification Quality (1-5) | Time Saved | Main Lesson | Next Improvement |
|-----|------|----------------------|----------------------------|------------|-------------|------------------|
| 1   |      |                      |                            |            |             |                  |
```

3. Fill Day 1 immediately after this module.
4. Pre-select 3 additional tasks you can delegate next week.

### What happened

You moved from one-off experimentation to a repeatable operating rhythm. This is what builds long-term delegation leverage.

## Part 6: Design the Self-Sustaining Delegation Loop

1. Document this loop in your team notes:
   - Task selection
   - Delegation brief
   - Agent execution
   - Verification checklist
   - Feedback capture
   - Instruction/process improvement
2. Add one weekly review slot (15-30 minutes) to improve prompts, checklists, and guardrails based on failures.
3. Share one "delegation win" and one "delegation fix" with your team each week to normalize systematic learning.

## Success Criteria

- [✅] You wrote and executed at least one delegation brief
- [✅] You completed a verification checklist for that delegated task
- [✅] You created and started a 30-day delegation log
- [✅] You can clearly explain micromanagement vs systematic oversight
- [✅] You identified at least 3 real tasks to delegate next week

## Understanding Check

1. Why is delegation (not raw coding speed) a key leadership leverage point with AI?
   - **Expected answer:** Because leaders scale output through systems and delegation; AI increases this leverage when briefs and oversight are done well.

2. What is the purpose of the 1-task-per-day habit?
   - **Expected answer:** Build delegation muscle gradually, reduce risk, and create consistent practice over time.

3. What makes a delegation brief executable?
   - **Expected answer:** Clear context, constraints, acceptance criteria, and required verification evidence.

4. How is systematic oversight different from micromanagement?
   - **Expected answer:** Systematic oversight checks outcomes at defined checkpoints; micromanagement controls every intermediate action.

5. When should you take back control instead of improving the system?
   - **Expected answer:** When risk is high (security, production stability, critical requirement mismatch) and immediate correction is needed.

6. Give one example of "improve the system" after a failed delegation.
   - **Expected answer:** Strengthen acceptance criteria, add missing context, or expand verification checklist instead of rewriting everything manually.

## Troubleshooting

- **Problem:** The agent produces broad changes outside the task scope.  
  **Fix:** Tighten constraints in the brief and require explicit file-scope boundaries.

- **Problem:** Verification takes too long and feels like manual rework.  
  **Fix:** Use a fixed checklist and evidence format so review focuses on pass/fail signals.

- **Problem:** You keep intervening too often during execution.  
  **Fix:** Define checkpoint timing before execution and only step in at those points.

- **Problem:** Team members distrust delegated output.  
  **Fix:** Share verification evidence and review outcomes publicly to build confidence through transparency.

## Next Steps

Continue with [Export Chat Session](../250-export-chat-session/about.md) to capture delegation runs as reusable team knowledge and improve future briefs with real examples.
