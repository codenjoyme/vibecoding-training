Module 9: Agent Memory Management

Background
You spent 30 minutes in a productive AI session — the agent understood your project, made good decisions, and completed half the work. You close the chat, come back later, and... the AI has no idea what you were working on. It asks basic questions you already answered. All that context is gone.

AI agents do not naturally remember anything between sessions. Each conversation starts from zero. This is not a bug — it is how the technology works. But it is also a problem you can solve. In this module, you will learn three techniques for giving AI agents persistent memory, and you will apply one of them to convert your Technical Specification into a structured task backlog for the rest of the course.

Page 1: Why AI Agents Forget
Background
AI models process each message independently within a single conversation. When you close the chat, the context window — the shared canvas from Module 6 — is discarded. The next conversation starts with an empty canvas.

This creates problems for multi-session projects:
- The AI does not know what tasks were completed.
- It may redo work or contradict earlier decisions.
- You waste time re-explaining context every session.
- Complex projects stall because the agent cannot maintain a plan.

The solution: create external memory that persists between sessions. The AI reads this memory at the start of each conversation and writes updates at the end.

Three approaches to external memory:
1. Built-in todo tool — visual task list that appears above the chat (single-session).
2. External markdown todo list — a file in your project that the AI reads and updates (multi-session).
3. Project documents — specification + task list combination for complex projects (multi-session, multi-document).

✅ Result
You understand why AI agents forget between sessions and the three approaches to solving it.

Page 2: Built-in Todo Tool
Background
Most AI coding assistants have a built-in todo tool that creates a visual task list above the chat window. This is useful for real-time progress tracking during a single session.

How to find built-in tools:
- In VS Code: click the wrench icon (🔧) or the keys icon next to the model name in the Copilot Chat panel. You will see tools like: agent, edit, execute, read, search, todo.
- In Cursor: click the tools icon near the model selector in the AI Chat panel.

The AI uses the todo tool automatically when you ask for multi-step work. Items turn from pending → in-progress → completed as the agent works.

Steps
1. Open your AI chat in Agent Mode.
2. Give the AI a multi-step task:
   "I need to create three files in a folder called 'reports': template.md with a status report template, instructions.md with how to fill it out, and example.md with a filled-in example. Create a todo list and work through each item step by step."
3. Watch the todo list appear above the chat.
4. Notice items update as the agent completes each step.
5. When done, observe the final state — all items should be marked complete.

✅ Result
You can trigger and observe the built-in todo tool for real-time progress tracking.

Page 3: External Markdown Todo Lists
Background
Built-in todos disappear when you close the chat. For multi-session projects, you need a persistent todo list — a markdown file in your project that survives between conversations.

The pattern:
1. Create a TODO.md file with checkboxes for each task.
2. Reference it in your prompt using @-mention: "@TODO.md".
3. Ask the AI to read the file, work through items, and update checkboxes as tasks complete.
4. When you start a new session, the AI reads the file and continues from the next uncompleted item.

Example TODO.md structure:
```markdown
# Project Tasks

## Phase 1: Setup
- [x] Create project repository
- [x] Configure .gitignore
- [ ] Set up development environment

## Phase 2: Implementation
- [ ] Create data fetching module
- [ ] Build report template
- [ ] Add formatting logic

## Progress Notes
_AI updates this section as work progresses_
```

Steps
1. Create a file called TODO.md in your project root.
2. Add 5-6 tasks organized in phases with checkboxes (use the format above as a starting point).
3. Open your AI chat and type: "Read @TODO.md and work through the uncompleted items in Phase 1. Update the checkboxes as you complete each task."
4. Watch the AI work through items and update the file.
5. Close the chat, open a new session, and type: "Check @TODO.md and continue where you left off."
6. Verify the AI picks up from the correct task.

✅ Result
You can create and use external markdown todo lists for persistent task tracking across sessions.

Page 4: Create Your Project Backlog
Background
Now you will apply the memory management technique to your practical project. You have a Technical Specification (PROJECT_SPEC.md) from Module 8. The next step is to convert it into a structured task backlog — a detailed list of implementation steps that will guide the work in modules 10-20.

This backlog becomes the AI's "memory" of your project. Every future session starts with the AI reading this file to understand what has been done and what comes next.

Steps
1. Open your AI chat in Agent Mode.
2. Reference both your specification and the interview technique:
   "Read @PROJECT_SPEC.md. Break it down into a detailed implementation backlog with specific, actionable tasks. Organize tasks into phases: Setup, Core Features, Integration, Testing, Documentation. Use checkboxes. Save as BACKLOG.md. Before creating it, ask me clarifying questions about priorities and phasing."
3. Answer the AI's questions about priorities (which features first, any dependencies, any time constraints).
4. Review the generated BACKLOG.md.
5. Verify it covers all requirements from your ТЗ.
6. If anything is missing, ask the AI to add it.
7. Commit the file to your repository.

✅ Result
You have a structured project backlog (BACKLOG.md) committed to your repository. This will guide your work for the rest of the course.

Page 5: Combining Documents for Complex Projects
Background
For large projects, a single todo list is not enough. The most effective pattern combines two documents:

1. PROJECT_SPEC.md — the "why" and "what" (high-level goals, requirements, quality standards). You created this in Module 8.
2. BACKLOG.md — the "how" and "when" (specific tasks, phases, progress). You created this on the previous page.

When starting a new AI session, reference both:
"Read @PROJECT_SPEC.md for project context and @BACKLOG.md for current progress. Continue where we left off."

The AI now has:
- Strategic context (what the project is about and what quality standards apply).
- Tactical context (what has been done, what is next).
- Persistent memory across sessions.

Tips for maintaining these documents:
- Ask the AI to update BACKLOG.md at the end of each session.
- Periodically ask: "Verify @BACKLOG.md reflects actual completion status."
- Add a "Decisions Made" section to record important choices (technology selections, architecture decisions).

✅ Result
You understand how to combine specification and backlog documents for persistent project memory across multiple AI sessions.

Summary
In this module, you learned that AI agents do not remember anything between sessions — the context window is discarded when the chat closes. You practiced three techniques for giving agents persistent memory: built-in todo tools for single-session tracking, external markdown todo lists for multi-session persistence, and combined project documents for complex work. You applied these techniques to create a project backlog from your Technical Specification.

Key takeaways:
- AI agents forget everything between sessions — this is by design, not a bug.
- Built-in todo tools provide visual progress tracking during a single session.
- External markdown todo lists (TODO.md, BACKLOG.md) persist between sessions.
- The most effective pattern combines a specification document (the "why") with a backlog (the "how").
- Your PROJECT_SPEC.md + BACKLOG.md pair will guide all remaining practical work.

Quiz
1. Why does the AI agent not remember what you discussed in a previous chat session?
   a) It has a memory limit that resets every hour
   b) The context window (shared canvas) is discarded when the chat closes — each new conversation starts from zero
   c) You need to pay for a premium plan to enable memory
   Correct answer: b. AI models process text within a context window that exists only for the duration of the conversation. Closing the chat means losing that context entirely.

2. What is the most effective way to maintain project context across multiple AI sessions?
   a) Copy and paste your entire previous conversation into the new chat
   b) Use external markdown files (like PROJECT_SPEC.md and BACKLOG.md) that the AI reads at the start of each session and updates at the end
   c) Keep the same chat window open permanently and never close it
   Correct answer: b. External files provide persistent, updateable context. The AI reads them to understand project state and updates them to reflect progress, creating reliable memory across sessions.

3. What should a good project backlog include?
   a) Only a list of features with no details
   b) Specific, actionable tasks organized in phases with checkboxes, plus a progress notes section for AI updates
   c) A copy of the project specification without any changes
   Correct answer: b. A backlog breaks down high-level requirements into specific, trackable tasks with clear completion criteria and progress tracking.
