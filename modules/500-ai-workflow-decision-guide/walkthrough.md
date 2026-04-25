# AI Workflow Decision Guide — Hands-on Walkthrough

In this module you will practice selecting and combining AI tools across 10 real-world developer scenarios. By the end you will have a personal AI workflow playbook — a reference you can reach for on any workday.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## The AI Tool Decision Framework

Before diving into scenarios, internalize the core question you should ask yourself when any task arrives:

> **"What kind of output do I need, and what is the fastest reliable path there?"**

Use this table as your compass:

| Task Type | Start Here |
|---|---|
| Requirement is unclear | AI interview → clarified spec |
| Known bug, unknown cause | Describe symptom in chat → locate → fix |
| New teammate needs context | Agent reads codebase → onboarding doc |
| Legacy code, unknown shape | SpecKit reverse-docs |
| Many files to transform | Agent mode bulk automation |
| New idea, need working code fast | SpecKit PoC |
| Need to recall past AI work | Export Chat Session |
| Manual repetitive task | Pattern → CLI skill |
| UI misbehaves | Chrome DevTools MCP |
| Sprint needs prioritized backlog | AI interview → GitHub issues |

---

## Part 1: Vague Feature Request

### What we'll do
A stakeholder sends you a vague request. Instead of asking for clarification in a meeting, you use AI to run an interview, produce a spec, create a GitHub issue, and optionally delegate to a coding agent.

### Steps

1. Open a new AI chat and paste the vague request as-is.
2. Use the `coaching/interview-sdlc.agent.md` instruction prompt to run a structured clarification interview.
3. At the end of the interview, ask the AI to produce a one-page spec in markdown.
4. Use the MCP GitHub tool to create a GitHub issue from that spec.
5. Optionally: assign the issue to GitHub Copilot for implementation.

### Verify
You should see a newly created GitHub issue with a structured description, acceptance criteria, and labels.

---

## Part 2: Bug Report

### What we'll do
A bug arrives with only a symptom description. You will use AI chat to locate the root cause, apply a fix using baby-step commits, and push the change.

### Steps

1. Paste the bug description into AI chat with relevant file context.
2. Ask: "What are the most likely causes of this behaviour? List them ranked by probability."
3. Read through the AI's analysis and navigate to the suspected location.
4. Apply the fix with AI assistance.
5. Commit using baby-step methodology: one small commit per logical change.
6. Verify: run the project and confirm the bug no longer reproduces.

### Verify
Git log shows a clean, atomic commit. The symptom is gone.

---

## Part 3: Onboard a New Developer

### What we'll do
A new engineer joins your team. Instead of writing onboarding docs manually, you let the AI agent read the codebase and generate a structured document.

### Steps

1. Open AI agent mode in your IDE.
2. Use this prompt: "Read the codebase in `./workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux). Produce a developer onboarding document covering: project purpose, folder structure, key entry points, how to run locally, and common pitfalls."
3. Review the generated document and add any missing team-specific details.
4. Save to `docs/onboarding.md` in the repository.

### Verify
A non-technical reader can follow the document and run the project in under 15 minutes.

---

## Part 4: Legacy Project Feature

### What we'll do
You need to add a feature to an unfamiliar legacy codebase. SpecKit will help you reverse-document the project and identify safe insertion points.

### Steps

1. Run SpecKit in reverse-docs mode on the legacy project folder.
2. Review the generated architecture overview.
3. Ask the AI: "Where is the safest place to add [your feature]? Show me 2-3 options with pros and cons."
4. Pick an option and implement using AI assistance.
5. Verify no existing tests break.

### Verify
AI proposes concrete file paths and line ranges as insertion candidates. The feature works and existing behavior is unchanged.

---

## Part 5: Bulk File Processing

### What we'll do
You have 50 configuration or log files that need the same transformation. You use AI agent mode to batch process them automatically.

### Steps

1. Put all target files in a single folder.
2. Open AI agent mode and describe the transformation rule precisely (example: "For each `.json` file in `./configs/`, rename key `oldKey` to `newKey`").
3. Let the agent run. Watch it process files one by one.
4. Spot-check 3-5 output files to verify correctness.

### Verify
All files are transformed uniformly. No files are skipped or corrupted.

---

## Part 6: Prototype an Idea in 2 Hours

### What we'll do
You have a product idea and need a working demo. You will use SpecKit to go from idea to a runnable full-stack PoC in under 2 hours.

### Steps

1. Write a one-paragraph description of your idea (problem + desired outcome).
2. Run SpecKit: provide the description as input, select full-stack template.
3. Review the generated spec — adjust scope to fit 2 hours.
4. Let the AI agent scaffold the project.
5. Run the PoC and verify the core user journey works end-to-end.

### Verify
A working app is running locally that demonstrates the core concept.

---

## Part 7: Review What AI Did Across Sessions

### What we'll do
You need to recall a decision made two weeks ago in a past AI session. You will use the Export Chat Session tool to find it.

### Steps

1. Run the export tool from module 250 to export recent sessions to text or HTML.
2. Open the exported files and use your IDE's full-text search to find the relevant conversation.
3. Extract the key decision or code snippet.
4. Optionally: save it to a team knowledge base file.

### Verify
You find the target decision in under 2 minutes without opening every old chat window.

---

## Part 8: Automate a Repetitive Weekly Task

### What we'll do
You have a task you do manually every week. You will identify its pattern and build a CLI skill to automate it.

### Steps

1. Write out the task as a numbered list of manual steps.
2. Show the list to the AI: "Turn this into a PowerShell (Windows) or Bash (macOS/Linux) script."
3. Review and test the generated script.
4. Register it as a CLI skill following the `103-cli-command-line-interface` module.
5. Run it end-to-end and verify the output matches your manual result.

### Verify
The task that used to take 15 minutes now runs in under 30 seconds with one command.

---

## Part 9: Web UI Bug Hunting

### What we'll do
A UI bug was reported but only reproduces on a specific flow. You will use Chrome DevTools MCP to let AI emulate user actions and identify the issue.

### Steps

1. Open the Chrome DevTools MCP server (from module 130).
2. Describe the user flow that triggers the bug.
3. Ask the AI agent to emulate the flow step by step using the MCP tools.
4. Read the AI's report: which element, which event, which network call failed?
5. Fix the issue and re-run the emulation to confirm resolution.

### Verify
The AI produces a precise bug report with element selectors and failure point. Fix resolves it.

---

## Part 10: Sprint Planning — Prioritized Backlog

### What we'll do
Sprint planning starts in 30 minutes and the backlog is unstructured. You will run an AI interview to extract feature ideas and produce a prioritized GitHub issues list.

### Steps

1. Open AI chat and run a quick product interview: "I'm going to describe features for our next sprint. For each one, ask me one clarifying question, then produce a GitHub issue draft."
2. Describe your features one by one.
3. Review the drafted issues and adjust priority labels.
4. Use the MCP GitHub tool to create all issues in one session.

### Verify
GitHub shows a set of well-formed issues with titles, descriptions, acceptance criteria, and priority labels — ready for sprint planning.

---

## Part 11: Your Own Task

Now apply the framework to a real task from your current work.

### Steps

1. Write one sentence describing a task you need to do this week.
2. Use the Decision Framework table at the top of this walkthrough to identify the right tool(s).
3. Execute the workflow.
4. Note: how long did it take vs. doing it manually?

---

## Success Criteria

- ✅ You completed at least 5 of the 10 scenarios above
- ✅ You can name the right AI tool for each scenario type without looking at the table
- ✅ You applied the framework to a real task from your own work
- ✅ You have a personal AI workflow playbook (or started one)

---

## Understanding Check

1. **A stakeholder sends a one-line requirement. What is your first move?** — Run an AI clarification interview before writing a single line of code. Output is a spec, not a guess.
2. **You need to transform 80 files the same way. Which approach is fastest?** — AI agent mode in bulk processing. Describe the transformation rule precisely and let the agent run.
3. **Why use SpecKit for legacy projects instead of just asking the AI questions?** — SpecKit reverse-documents the full structure first, giving the AI accurate context rather than relying on what you can describe manually.
4. **What is the key question of the AI Tool Decision Framework?** — "What kind of output do I need, and what is the fastest reliable path there?"
5. **A new teammate is starting Monday. You have 20 minutes to prepare. What do you do?** — Use agent mode to read the codebase and generate an onboarding doc automatically.
6. **You fixed a UI bug last month using AI. How do you find what you did?** — Export the relevant chat sessions and full-text search the exports.
7. **What makes baby-step commits valuable when working with AI?** — Each commit is a checkpoint. If the AI makes an error, you can revert to the last good state without losing all your work.

---

## Troubleshooting

**AI gives a vague spec after the interview**  
Ask explicitly: "Add acceptance criteria as a numbered list. Each criterion must be testable."

**Agent mode stops mid-batch**  
Break the task into smaller batches (10 files at a time). AI context windows have limits.

**SpecKit generates inaccurate architecture overview**  
Point it at a specific subfolder rather than the entire monorepo. Narrow scope → more accurate output.

**MCP GitHub tool fails to create issues**  
Check that your authentication token has `repo` and `issues` write scopes.

**Chrome DevTools MCP emulation skips steps**  
Use explicit numbered steps in your prompt. Vague descriptions lead to skipped interactions.

---

## Next Steps

You have completed the capstone module. Your next move is to apply this decision framework weekly:

- Every time a task arrives, name the tool before you open it
- After 2 weeks, review which tools you used most — those are your power tools
- Share your AI workflow playbook with your team
