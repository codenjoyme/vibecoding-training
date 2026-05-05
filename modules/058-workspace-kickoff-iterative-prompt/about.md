# Workspace Kickoff with Iterative Prompt

**Duration:** 5-7 minutes  
**Skill:** Start any AI-assisted investigation by creating a `development log` (`main.prompt.md`) that evolves with `## UPD[N]` blocks — a living document that stays in version control alongside your work

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why a saved prompt file beats chat history as a starting point
- Setting up a research folder with gathered materials (source code, transcripts, notes, chat excerpts)
- Writing a kickoff prompt that converts raw thoughts into structured AI action items
- Running a `.prompt.md` file directly from the IDE
- Leaving breadcrumbs for your future self and teammates
- Growing the prompt incrementally with `## UPD[N]` / `### RESULT` blocks
- Using `iterative-prompt/SKILL.md` to formalize the pattern across projects
- Saving premium requests by keeping the agent in a polling loop

## Learning Outcome

Ability to kick off any AI-assisted research or exploration by creating a `development log` (`main.prompt.md`) that describes materials and goals — and then grow it with `## UPD[N]` blocks as the investigation evolves, without losing context or starting new chat sessions. The `development log` stays in the repository as a permanent artifact showing how and why the work was done.

## Prerequisites

### Required Modules

- [040 — Agent Mode & AI Mechanics](../040-agent-mode-under-the-hood/about.md)
- [057 — Agent Memory Management](../057-agent-memory-management/about.md) *(optional, recommended)*

### Required Skills & Tools

- VS Code with GitHub Copilot (Agent Mode) OR Cursor IDE
- A folder with at least a few documents or files to analyze

## When to Use

- Starting research on an unfamiliar codebase you just cloned
- Analyzing a batch of meeting transcripts to extract decisions or action items
- Onboarding to a new project using existing documents and notes
- Any time you dump a pile of materials into a folder and want AI to make sense of them
- When you want to preserve the starting point of an investigation in version control
- When you have an ongoing task that evolves over multiple sessions and you want a single file to track all updates
- When you want to save premium requests by keeping the agent working autonomously

## Resources

- **Iterative Prompt Skill** — the formalized instruction for the `UPD[N]` pattern. Install it in any workspace with:
  ```
  Setup https://github.com/codenjoyme/vibecoding-training/blob/main/instructions/iterative-prompt/SKILL.md
  ```
