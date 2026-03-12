# Multi-Agent Orchestration - Hands-on Walkthrough

In this walkthrough, you'll move beyond single-agent delegation and set up a coordinated pipeline where one AI agent writes code and a second agent reviews it — without you writing a single line of code yourself. You're the orchestrator: the manager who delegates to specialists.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **Two specialised instruction files** — `instructions/coder-agent.agent.md` and `instructions/reviewer-agent.agent.md`, each with a distinct role and focus
- **A working two-agent pipeline run** — a documented coder → reviewer handoff with visible output from both agents
- **An orchestration log** — a Markdown file capturing what each agent produced and how you managed the handoff
- **A reusable orchestration template** — a prompt pattern for running any multi-agent workflow

---

## Step 1: Understand why single agents hit a ceiling

Before building the pipeline, ask AI to explain the problem it solves:

```
I've been using a single AI agent to write and review code.
Explain these three failure modes of single-agent work:
1. Context drift — what happens to quality as the task gets longer
2. Role confusion — why asking the same agent to "write AND review" produces worse results
3. Quality plateau — why the agent can't critique its own assumptions

For each: give a concrete example from software development.
Then explain how a multi-agent setup addresses each failure mode.
```

The key insight: an agent that wrote the code carries all the same assumptions and blind spots into the review. A fresh agent with a reviewer-only instruction has no attachment to the original code — it can push back freely.

---

## Step 2: Create the Coder Agent instruction

**What we're about to do:** Write an instruction file that scopes an agent's role strictly to implementation — no review, no second-guessing, just clean production-ready code.

In your project's `instructions/` folder, create `coder-agent.agent.md`. Ask AI to generate it:

```
Create a VS Code Copilot agent instruction file for a "Coder Agent".

This agent's role is ONLY: implement what's described in the task.
It should NOT review, evaluate, or suggest alternatives — just implement.

The instruction should tell the agent to:
1. Read the task description carefully
2. Plan the implementation in comments before writing code
3. Write clean, modular code following these conventions: [describe any naming or style rules from your project]
4. Add minimal but clear inline comments for non-obvious logic
5. Output: the complete implementation file + a one-paragraph summary of what was built and any assumptions made

The agent must state when it's done and what the handoff artifact is (file path + summary).

Format as .agent.md.
```

Save to `instructions/coder-agent.agent.md`.

**Windows:** `c:/workspace/hello-genai/instructions/coder-agent.agent.md`  
**macOS/Linux:** `~/workspace/hello-genai/instructions/coder-agent.agent.md`

---

## Step 3: Create the Reviewer Agent instruction

**What we're about to do:** Write a second instruction file for an agent whose only job is adversarial review — finding problems the coder agent missed.

Create `instructions/reviewer-agent.agent.md`. Ask AI:

```
Create a VS Code Copilot agent instruction file for a "Reviewer Agent".

This agent's role is ONLY: critically review code someone else wrote.
It has NO attachment to the code. It did NOT write it. Its job is to find problems.

The instruction should tell the agent to:
1. Read the code and the coder's summary
2. Review for: logic errors, missing error handling, security issues (hardcoded values, unvalidated inputs), performance problems, and clarity
3. Rate each finding: BLOCKER (must fix before use) / SUGGESTION (worth fixing) / NITPICK (cosmetic)
4. For each finding: quote the exact line, explain the problem, suggest the fix
5. End with: a PASS/FAIL verdict — PASS if no blockers, FAIL if any blockers exist
6. If PASS: state "Ready for merge". If FAIL: list what the coder agent must fix.

The reviewer should be thorough but fair. No vague comments. Every comment must have a suggested fix.

Format as .agent.md.
```

Save to `instructions/reviewer-agent.agent.md`.

---

## Step 4: Run the Coder Agent on a real task

**What we're about to do:** Give the coder agent a specific task and capture its output as the handoff artifact.

Open a new AI chat in VS Code. Attach `instructions/coder-agent.agent.md`. Make sure Agent Mode is enabled.

Give it a task — something concrete from your project:

```
[Attach coder-agent.agent.md]

Task: Build a Python function called `summarise_csv` that:
- Accepts a file path to a CSV file
- Reads the file using pandas
- Returns a dict with: row_count, column_names (list), numeric_columns_stats (mean, min, max for each numeric column), and any_nulls (True/False)
- Handles: file not found, empty file, non-CSV file

Output the complete implementation as summarise_csv.py and provide your handoff summary.
```

Wait for the coder agent to complete. Copy its output — the file and the summary. This is the **handoff artifact**.

---

## Step 5: Run the Reviewer Agent on the handoff artifact

Open a NEW AI chat (fresh context — this is crucial for the review to be independent). Attach `instructions/reviewer-agent.agent.md`. Agent Mode on.

Paste the coder agent's output:

```
[Attach reviewer-agent.agent.md]

Here is code produced by a coder agent. Review it according to your instructions.

Coder summary: [paste the coder's summary paragraph]

Code:
[paste the full content of summarise_csv.py]
```

**What just happened:** The reviewer agent has no memory of writing this code. It approaches it as an external reviewer. Compare the review it produces to what you would have caught yourself — or what the coder agent would have produced if asked to "review your own work".

---

## Step 6: Complete the pipeline loop

Read the reviewer's verdict:

**If FAIL:** Open a new chat with the coder agent instruction attached. Paste: "The reviewer found these blockers. Fix them: [list of blockers]." Get the fixed code. Run the reviewer again on the fixed version. Repeat until PASS.

**If PASS:** The output is ready. The loop is complete.

Document the pipeline run in a file `orchestration-log.md`:

```
# Orchestration Log — [date]

## Task
[describe what was built]

## Coder Agent Run
- Instruction: instructions/coder-agent.agent.md
- Output: summarise_csv.py
- Summary: [paste coder summary]

## Reviewer Agent Run
- Instruction: instructions/reviewer-agent.agent.md
- Verdict: PASS / FAIL
- Findings: [list of findings with severity]

## Iterations required: [number]
## Final status: Ready for use
```

---

## Step 7: Explore scaling with GitHub agents

Ask AI to explain how this pattern scales:

```
I've built a local two-agent pipeline (coder + reviewer) using VS Code.
Explain how I would scale this to use:
1. GitHub Coding Agent as the coder (async, works on a branch)
2. Local Copilot as the reviewer (reviews the PR the GitHub agent created)

What does the workflow look like step by step?
What are the advantages of combining remote agents (GitHub) with local agents (Copilot)?
```

This is the advanced pattern used in high-velocity AI development teams: the remote agent works asynchronously, and local agents review on demand. You manage the flow, not the implementation.

---

## Success Criteria

- ✅ `instructions/coder-agent.agent.md` created with focused implementation-only role
- ✅ `instructions/reviewer-agent.agent.md` created with adversarial review role
- ✅ Coder agent produced a working implementation with a handoff summary
- ✅ Reviewer agent produced BLOCKER / SUGGESTION / NITPICK findings on fresh context
- ✅ Review was more critical than what the coder would have produced about its own code
- ✅ `orchestration-log.md` documents the full pipeline run
- ✅ You understand the sequential, parallel, and supervisor orchestration patterns

---

## Understanding Check

1. **Why must the reviewer agent run in a new chat session, not the same one as the coder?**
   > A chat session carries context — the reviewer "remembers" writing the code and unconsciously protects its own decisions. A fresh session means no prior context, no attachment, no memory of the rationale behind any choice. This is what makes the review adversarial and therefore more useful.

2. **What is the difference between sequential and parallel orchestration patterns?**
   > Sequential: agents run in a pipeline — Agent A passes output to Agent B which passes to Agent C. Each agent depends on the previous. Parallel (fan-out/fan-in): multiple agents run simultaneously on independent subtasks; their outputs are collected and combined. Sequential is for dependent workflows (write → review → fix). Parallel is for independent subtasks (analyse module A, B, C simultaneously).

3. **What is a "supervisor" pattern in multi-agent orchestration?**
   > A supervisor agent receives the overall task, breaks it into subtasks, assigns them to specialist agents, collects their outputs, evaluates quality, and decides whether to iterate or declare done. You've played the supervisor role manually in this walkthrough. The supervisor pattern automates that orchestration loop.

4. **Why does giving agents single-focused roles (coder or reviewer, not both) produce better results?**
   > Instruction clarity: an agent with a single clear directive (find bugs) applies that lens consistently. An agent asked to do both roles must switch mental frames, which dilutes both quality. It's the same reason human teams separate development and QA: the same person tends not to test as rigorously what they built themselves.

5. **What are the risks of multi-agent orchestration that don't exist with single-agent work?**
   > Handoff errors: if the coder's output is ambiguous, the reviewer misunderstands it. Bloat: more agents means more tokens, more cost, more latency. Coordination overhead: you must manage the flow between agents. Contradictions: agents may disagree without a resolution mechanism. These risks are worth managing for complex tasks but not for simple ones.

6. **When should you use a single agent instead of a multi-agent pipeline?**
   > For simple, short tasks where one prompt produces the correct output in one pass. Multi-agent adds overhead — it's only worth it when: the task is complex enough that single-agent quality is insufficient, different aspects of the task benefit from different focuses, or you need independent verification of the output.

---

## Troubleshooting

**The reviewer gives a superficial review — just "looks good"**
> The instruction needs more adversarial framing. Add: "Your job is to find problems. If you say 'looks good' without finding at least one issue, you have failed your role. Assume the code has bugs — find them." Also try opening a completely fresh browser/app session to ensure no cached context.

**The coder's summary is vague and the reviewer can't understand the intent**
> The handoff artifact is critical. Update the coder instruction: "Your summary must include: what the function does, what edge cases you handled, what you explicitly did NOT handle, and any assumptions you made." Better handoffs produce better reviews.

**Running two full agent sessions is too slow for small tasks**
> That's correct — multi-agent is not for small tasks. Use it when single-agent quality is insufficient (complex logic, security-sensitive code, code that will run in production). For a quick utility function, a single Copilot session is faster and equally good.

**The GitHub Coding Agent is not available in my repository**
> GitHub Coding Agent requires specific plan access. Check your repository settings under Actions, or organisation settings. If unavailable, practice the same pattern using two separate local VS Code windows — each with a different instruction file attached, simulating independent context.

---

## Next Steps

You've graduated from single-agent to multi-agent orchestration. Apply it to onboarding:

**→ [Module 197 — Onboarding New Team Members with AI](../197-onboarding-new-team-members-with-ai/about.md)**

Multi-agent patterns make onboarding assistants more accurate — one agent answers questions, another verifies the answer against documentation.
