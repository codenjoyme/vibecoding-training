# Export Chat Session

**Duration:** 5-7 minutes

**Skill:** Extract, preserve, and share AI chat sessions from VS Code as portable HTML files for knowledge retention, team collaboration, and project documentation.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Where VS Code stores your chat sessions locally
- Extracting sessions with the export script (HTML, JSON, JSONL)
- Token leakage risks when sharing exported sessions
- Creating session summaries for future reference
- Using exported sessions as knowledge base and reference materials

## Learning Outcome

You will be able to find, export, and share your GitHub Copilot chat sessions. You'll understand the value of preserving AI conversations as project documentation, know how to create summaries from sessions, and be aware of security risks (token leakage) when sharing exports.

## Prerequisites

### Required Modules

- [070 — Custom Instructions](../070-custom-instructions/about.md)

### Required Skills & Tools

- VS Code with GitHub Copilot — at least one chat session in history
- Python 3 installed (`python --version` should work in terminal)
- Basic understanding of command line operations

## When to Use

- After completing a significant feature or fix — export and summarize for future reference
- When handing off work to a colleague — share the session as context
- When creating release notes — use session exports as source material
- When you need to search through past AI interactions across multiple sessions
- When documenting "how we built this" for the team

## Resources

- Export script: [copilot_chat_export.py](tools/copilot_chat_export.py)
- Agent instruction: [export-chat-session.agent.md](../../instructions/export-chat-session.agent.md)
