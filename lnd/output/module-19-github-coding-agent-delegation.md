# Module 19: `GitHub` Coding Agent Delegation

### Background
Up to this point, every task was completed by you and your AI assistant working together in the IDE. You described the task, the AI proposed a solution, you reviewed and approved it — all in real time. But what if you could delegate a task to an autonomous AI `agent` that works independently on `GitHub`'s servers while you do something else? `GitHub Copilot Coding Agent` does exactly that: you assign it a `GitHub` issue, and it reads the codebase, writes the code, and creates a pull request — without your involvement until it is time for code review. This module teaches you how to delegate effectively, monitor progress, and review the results.

**Learning Objectives**

Upon completion of this module, you will be able to:
- Explain the difference between `GitHub Copilot` IDE assistant and Coding Agent and when to use each.
- Prepare a well-defined `GitHub` issue with clear requirements and acceptance criteria for autonomous implementation.
- Assign a task to `GitHub Copilot Coding Agent` and monitor its progress.
- Review an agent-generated pull request and improve `instruction` files based on the `agent`'s mistakes.

## Page 1: What is `GitHub` Coding Agent
### Background
`GitHub Copilot` has several components. The **IDE assistant** (what you have been using in `VS Code`) provides real-time suggestions and chat. The **Coding Agent** is different — it runs on `GitHub`'s servers, works autonomously, and creates pull requests.

Key characteristics:
- **Autonomous:** Works independently after you assign a task. No need to sit and watch.
- **Server-side:** Runs on `GitHub`'s infrastructure, not your machine. Your laptop can be closed.
- **Full repository access:** Reads the entire codebase for context, including your instruction files from `Module 10`.
- **Creates pull requests:** Delivers a complete implementation as a PR for your review.
- **Session logs:** Provides a detailed work log so you can see every decision it made.
- **Model selection:** Can use different AI models (`GPT-5.2-Codex`, `Claude Opus`, `Claude Sonnet`, or `Auto` mode).

**Important note on model differences:** The Coding Agent runs on `GitHub`'s servers with different models than your IDE. `Instructions` that work perfectly with `Claude Sonnet` in `VS Code` may need adjustment for the `agent`'s server environment. Start with `Auto` mode, and if the `agent` makes unexpected decisions, check whether the model difference is the cause.

**When to use it:**
- Well-defined tasks with clear requirements (from your backlog).
- Repetitive implementation work (similar patterns across features).
- Multiple features to implement in parallel (assign different issues to different `agent` sessions).
- You are busy with meetings, planning, or other work and want coding to continue.

**When NOT to use it:**
- Exploratory work that needs human judgment.
- Complex architectural decisions.
- Urgent fixes (the `agent` takes 15-30 minutes to finish).
- Vague or ambiguous requirements (the `agent` will guess, and guess wrong).

### Steps
1. Ask the AI: "Explain the difference between `GitHub Copilot` IDE assistant and `GitHub Copilot Coding Agent`."
2. Read the response and note the key differences: real-time vs. autonomous, local vs. server-side.

### ✅ Result
You understand what the Coding Agent is and when to use it.

## Page 2: Preparing a Task for Delegation
### Background
The Coding Agent's quality depends entirely on the quality of input it receives. It reads three things: (1) the `GitHub` issue you assign it to, (2) the instruction files in your repository, and (3) the codebase itself.

A poorly written issue produces a poor implementation. A well-written issue with good instruction files produces a clean PR that needs minimal review.

**Good task description checklist:**
- Clear, specific title (not "Fix the thing").
- Detailed requirements with numbered steps.
- Technical constraints (e.g., "Use `Express` Router, not raw http module").
- Expected outcome ("The endpoint returns a `JSON` array of...").
- Links to relevant instruction files (e.g., "Follow instructions/create-training-module.agent.md").
- Acceptance criteria (how to verify the task is done).

### Steps
1. Open your project backlog (`BACKLOG.md` or `GitHub` Issues from `Module 14`).
2. Choose a task that is well-defined and self-contained. Good candidates:
   - Add a new feature to the prototype (a new page, a new API endpoint).
   - Fix a known bug from the QA report (`Module 18`).
   - Create documentation for an existing feature.
3. If using an existing `GitHub` issue, review it. Does it have enough detail for an autonomous agent?
4. If the issue is too vague, update it: ask the AI `Improve this GitHub issue description to make it suitable for autonomous implementation by a coding agent. Add acceptance criteria`
5. Verify your `instruction` files are committed and pushed. The `agent` reads them from `GitHub` — not from your local machine.

### ✅ Result
You have a well-defined `GitHub` issue ready for delegation and `instruction` files pushed to `GitHub`.

## Page 3: Assigning the Coding Agent
### Background
There are two ways to assign the Coding Agent to an issue: through the `GitHub` web interface or through the `GitHub` `MCP` from your IDE (as in `Module 14`). Both produce the same result. This walkthrough shows the web interface approach for clarity.

### Steps
1. Open the `GitHub` issue in your browser.
2. In the right sidebar, find the **Assignees** section.
3. Click **"Assign to `Copilot`"** (the button with the `Copilot` icon).
4. A configuration dialog opens with options:
   - **Optional `prompt`:** Additional instructions beyond the issue description. Leave empty for now (rely on your instruction files).
   - **Model:** Select "Auto" (recommended — lets `GitHub` choose the best model for the task).
   - **Agent:** Keep "`Copilot`" (default).
   - **Base branch:** Keep "main" (agent will create a new branch from main).
5. Click **"Assign."**
6. The `agent` will immediately comment on the issue: "Thanks for asking me to work on this. I will get started..."
7. You are now free to do other work. The `agent` runs autonomously.

**Alternative — assign from IDE:** Ask the AI `Assign GitHub Copilot coding agent to issue #N in this repository`. The AI will use `GitHub` `MCP` to send the assignment command without leaving your IDE.

### ✅ Result
The Coding Agent is assigned and working. You can close the browser and do other work.

## Page 4: Monitoring and Reviewing the Pull Request
### Background
The `agent` typically takes 15-30 minutes to finish. When it is done, it creates a pull request linked to the original issue. You will receive a `GitHub` notification. Your job now is to review the PR — the same code review process that happens in any software team.

### Steps
1. Wait for the `GitHub` notification (email or `GitHub` web notification) that the PR is ready.
2. Open the pull request on `GitHub`.
3. Read the **PR description.** The `agent` writes a summary of what it implemented.
4. Click **"Files changed"** to review the code changes:
   - Does the implementation match the issue requirements?
   - Did the `agent` follow your `instruction` files?
   - Are there any temporary or debug files that should not be committed?
5. Click **"View session"** (link in the issue or PR) to see the agent's work log:
   - Did it start by reading your instruction files? (Good sign.)
   - Did it read relevant files from the codebase for context? (Good sign.)
   - Were there any errors during implementation? (Check what it did about them.)
6. If everything looks good → click **"Approve"** and merge the PR.
7. If changes are needed → write review comments (inline on specific lines) and submit with **"Request changes."** The `agent` will read your comments and push updated commits.

**Important:** Collect all review comments before submitting. Each "Request changes" submission triggers a new `agent` session (costs one premium request). Submit all feedback at once.

### ✅ Result
You have reviewed the `agent`'s PR and either merged it or requested changes.

## Page 5: Learning from `Agent` Behavior
### Background
The Coding Agent's mistakes are feedback on your `instruction` files. If the `agent` misunderstood a convention, your `instruction` files were not clear enough. If the `agent` missed a requirement, the issue description was incomplete. Every `agent` interaction is an opportunity to improve your `instructions` for future tasks.

### Steps
1. After merging (or after requesting changes), reflect on what the `agent` did well and what it got wrong.
2. For each mistake:
   - Was it caused by a vague issue description? → Improve the issue template.
   - Was it caused by missing `instructions`? → Update the relevant `instruction` file.
   - Was it caused by project conventions not documented? → Add them to the constitution or `copilot-instructions.md`.
3. Ask the AI: `Based on the PR review from the coding agent, what improvements should I make to our instruction files? Check '.github/copilot-instructions.md' and the 'instructions/' folder`
4. Apply the improvements and commit them.
5. Next time you assign the `agent`, it will use the updated `instructions` — and make fewer mistakes.

### ✅ Result
You have improved your `instruction` files based on `agent` feedback, making future delegations more effective.

## Summary
Remember the question from the introduction — what if you could delegate a task to an AI agent that works on its own while you attend meetings or plan the next sprint? That is exactly what you did in this module.

You prepared a well-defined issue, assigned it to `GitHub Copilot Coding Agent`, and received a pull request with a complete implementation — all without sitting in the IDE. The quality of the result depended on the quality of your issue description and instruction files, and you improved both based on the experience.

Key takeaways:
- The Coding Agent works autonomously on `GitHub`'s servers — no need to watch it work.
- Issue quality directly determines implementation quality. Clear requirements = clean PR.
- `Instruction` files from `Module 10` guide the `agent`'s behavior on the server just as they guide the IDE assistant locally.
- **Parallel delegation:** You can assign multiple issues to different `agent` sessions simultaneously. While 4 `agents` implement 4 features, you focus on architecture, planning, or code review. This is the "junior staff" pattern — the `agents` work in parallel, each producing a PR for your review.
- Always review the work session log to understand the `agent`'s decision process.
- Submit all review comments at once to avoid multiple `agent` sessions.
- Treat every `agent` mistake as an `instruction` improvement opportunity.


## Quiz
1. What is the key difference between `GitHub Copilot` in the IDE and `GitHub Copilot Coding Agent`?
   a) The IDE assistant provides suggestions in real time, while the Coding Agent processes tasks in a scheduled batch at the end of each day
   b) The IDE assistant works in real-time with your guidance, while the Coding Agent runs autonomously on `GitHub`'s servers — reading the codebase, implementing tasks, and creating pull requests without your involvement until review
   c) The IDE assistant works with the full repository, while the Coding Agent can access only the files mentioned in the issue
   Correct answer: b.
   - (a) Incorrect. The Coding `Agent` does not batch tasks or wait for a schedule. It starts working immediately after assignment and typically completes within 15-30 minutes.
   - (b) Correct. The IDE assistant is interactive — you `prompt`, it responds, you approve. The Coding `Agent` is autonomous — you assign a task and it works independently, delivering a complete PR for your review. They complement each other.
   - (c) Incorrect. The Coding `Agent` has full repository access. It reads the entire codebase for context, including `instruction` files, configuration, and all source files — not just the ones mentioned in the issue.

2. What should you do if the Coding Agent makes mistakes in its implementation?
   a) Stop using the agent and implement everything yourself
   b) Analyze whether the mistake was caused by a vague issue description or unclear instruction files — then improve the instructions so the agent does not repeat the mistake in future tasks
   c) Reassign the same issue to the agent repeatedly until it gets it right
   Correct answer: b.
   - (a) Incorrect. Abandoning the `agent` wastes its potential. Most mistakes are caused by unclear inputs, not by `agent` limitations. Improving your `instructions` makes the `agent` more effective over time.
   - (b) Correct. `Agent` mistakes are feedback on your documentation. A vague issue → improve the issue template. Missing convention → update your `instruction` files. Each improvement makes all future delegations more effective.
   - (c) Incorrect. Reassigning without changing the inputs is likely to produce the same result. The `agent` reads the same issue and the same `instructions` each time. To get different output, you need to improve the input.

3. Why should you submit all review comments at once instead of one at a time?
   a) `GitHub` displays review comments as a batch, so submitting them individually makes the conversation harder to follow
   b) Each "Request changes" submission triggers a new agent session that costs a premium request — submitting all feedback at once means only one session is needed to address all comments
   c) The agent prioritizes the first comment and may ignore comments submitted later in separate reviews
   Correct answer: b.
   - (a) Incorrect. While readability matters, the primary concern is resource usage. `GitHub` does display individual comments fine, but each review submission triggers a new agent work session.
   - (b) Correct. Every review submission starts a new `agent` work session. If you submit 5 comments one by one, the `agent` runs 5 separate sessions. Submitting them together means one session handles everything — saving time and premium request quota.
   - (c) Incorrect. The `agent` reads all comments in a review submission equally. It does not prioritize or ignore based on submission order. The issue is that separate submissions trigger separate sessions, not that comments are lost.

## Practical Task

You have delegated a development task to `GitHub Copilot Coding Agent` and reviewed the resulting pull request.

**Submit your `report.md` for automated check:**

1. In your AI agent (`Copilot` / `Cursor` / `Claude Code`), open your project workspace and run the prompt below. The agent will inspect your project and create a `report.md` file in the project root, in the exact format the `autocheck` expects:

   ````markdown
   You are helping me prepare a submission report for an `autocheck` system. Inspect my current project workspace and create a file named `report.md` in the project root with EXACTLY the structure shown below. Replace bracketed placeholders with real values from my project. Do not add extra sections, do not omit sections, do not invent data. If a value is genuinely unknown or missing, write `N/A`.

   Source: the `GitHub` issue I assigned to the coding agent during Module 19, and the pull request the agent created. Use the `GitHub` `MCP` server (if available) or `gh` CLI to fetch the data. Then write `report.md`:

   # Coding Agent Delegation Report
   - Module: 19 — `GitHub` Coding Agent Delegation
   - Repository: `[owner/repo]`

   ## Issue
   - Number: `#[N]`
   - URL: `[full URL]`
   - Title: `[issue title]`
   - Description quality: [one sentence — does it have a clear description with acceptance criteria? Yes/No + brief reason.]

   ## Pull Request
   - Number: `#[N]`
   - URL: `[full URL]`
   - Title: `[PR title]`
   - Created at: `[ISO date]`
   - Status: `[open | closed | merged]`
   - Author: `[bot/agent username]`
   - Created by the coding `agent` (not manually committed): [Yes | No]

   ## Review Workflow
   - Review comments submitted all at once (single review batch): [Yes | No]
   - Total review comments: [N]
   - `Agent` mistakes treated as `instruction` improvement opportunities: [Yes | No]
   - Instruction file(s) updated as a result: `[list paths or N/A]`
   ````

2. Submit `report.md` to the `autocheck` system (the submission endpoint is being set up in parallel; instructions for accessing it will be shared once it is available).
3. The `autocheck` system will check that:
   - The `GitHub` issue has a clear description with acceptance criteria.
   - The PR was created by the coding `agent` (not manually committed).
   - You submitted all review comments at once (not one by one).
   - Any `agent` mistakes were treated as `instruction` improvement opportunities.
