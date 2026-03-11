# LND Module Plan — Vibe Coding for Managers

## Course Overview

**Title:** Vibe Coding for Managers  
**Target Audience:** Engineering Managers, Delivery Managers, Team Leads, and other non-developer roles who want to leverage AI coding assistants for automating routine management tasks.  
**Prerequisites:** No programming experience required. Basic computer literacy and access to a GitHub account.  
**Format:** Self-paced course with hands-on practice in VS Code + GitHub Copilot.

**Short Description (290 chars):**  
Want to automate your management routine without writing code? This course teaches you to build real tools — from Jira/Confluence dashboards to automated reports — using AI coding assistants, step by step, without prior programming experience.

**Course Goal:**  
By the end of this course, learners will be able to use AI coding assistants to build working automation tools for their management workflows, including Jira/Confluence integrations, automated reports, and data processing scripts.

---

## Practical Thread (Сквозное практическое задание)

**Project:** Jira/Confluence Automation Toolkit  

The course follows a single practical project that evolves across modules. By the end, the learner has a working set of tools for their management workflow.

**Project evolution by module:**

| Phase | Modules | What happens to the project |
|-------|---------|---------------------------|
| Foundation | 01-07 | Learner sets up tools, learns prompting, creates a technical specification (ТЗ) for their Jira/Confluence automation idea |
| Instructions & Skills | 08-11 | Builds custom instructions, skills, and MCP integrations for accessing Jira/Confluence |
| Automation | 12-13 | Processes bulk files, sets up development environment |
| Prototyping | 14-16 | Builds a working web prototype with SpecKit, tests with Chrome DevTools |
| Delegation & APIs | 17-18 | Delegates tasks to GitHub coding agent, connects to DIAL APIs |

**Practical task verification options:**
1. Export of chat sessions showing the student worked on the assigned topic and achieved results
2. Submission of generated artifacts (ТЗ document, instruction files, working prototype) to the LMS for review

**Note on Jira/Confluence access:** Early modules (01-09) do not require live Jira/Confluence access. The learner creates API tokens and a technical specification first. Actual integration happens in modules 10-11 when MCP/skills connect to real APIs. If access is unavailable, a mock dataset can be provided.

---

## Module Sequence

### Module 01: Installing VS Code + GitHub Copilot
- **Source:** `modules/010-installing-vscode-github-copilot/`
- **Status:** Include as-is
- **LND notes:** Entry-point module. Standard installation walkthrough. Include EPAM-specific license request path (Part 2.2). No changes to practical content needed.
- **Practical thread:** None yet — pure setup.
- **Quiz focus:** What is GitHub Copilot? How to verify it's working?

### Module 02: Installing Cursor (Optional)
- **Source:** `modules/020-installing-cursor/`  
- **Status:** Include as optional
- **LND notes:** Mark as optional in LMS. Some learners prefer Cursor. Keep brief.
- **Practical thread:** None — alternative IDE setup.
- **Quiz focus:** When would you choose Cursor over VS Code?

### Module 03: Version Control with Git
- **Source:** `modules/060-version-control-git/`
- **Status:** Include — moved earlier in sequence
- **LND notes:** Placed here because all subsequent modules require committing baby steps. Critical for the practical project. Teach git init, commit, push basics through AI agent.
- **Practical thread:** Initialize the project repository that will hold all future work.
- **Quiz focus:** Why commit after every small successful change? What is a baby step?

### Module 04: Model Selection
- **Source:** `modules/030-model-selection/`
- **Status:** Include
- **LND notes:** Practical understanding of which model to pick for which task. No changes needed.
- **Practical thread:** Experiment with different models on a sample prompt related to project management.
- **Quiz focus:** What factors determine model choice? When to use a stronger vs faster model?

### Module 05: Visual Context with Screenshots
- **Source:** `modules/035-visual-context-screenshots/`
- **Status:** Include
- **LND notes:** Teach screenshot sharing with AI. 
- **Practical thread:** **Create API tokens for Jira and Confluence** using screenshots as visual guides. Screenshots of the Jira/Confluence admin UI help the AI understand the exact interface. Tokens will be needed later for integrations.
- **Quiz focus:** When is a screenshot more effective than a text description?

### Module 06: Agent Mode — How AI Works Under the Hood
- **Source:** `modules/040-agent-mode-under-the-hood/`
- **Status:** Include
- **LND notes:** Foundational theory. Explain context windows, tool use, function calling in accessible terms for non-developers.
- **Practical thread:** Observe agent mode behavior while performing a simple automation task.
- **Quiz focus:** What is a context window? Why does the agent sometimes "forget" earlier instructions?

### Module 07: Effective Prompting Without Arguing
- **Source:** `modules/050-effective-prompting-without-arguing/`
- **Status:** Include
- **LND notes:** Key skill — iterative refinement instead of confrontation. Practical prompting patterns.
- **Practical thread:** Practice prompting patterns on a management reporting scenario.
- **Quiz focus:** Why restart with a refined prompt instead of arguing? What makes a prompt specific?

### Module 08: Clarifying Requirements Before Start
- **Source:** `modules/055-clarifying-requirements-before-start/`
- **Status:** Include
- **LND notes:** Method for transforming a vague idea into an actionable plan. 
- **Practical thread:** **Create a Technical Specification (ТЗ) for the Jira/Confluence automation project.** The learner describes their automation idea (weekly status report, CR registry, contributor analytics — they choose), asks the AI to clarify requirements, and produces a structured markdown ТЗ file committed to the repo.
- **Quiz focus:** Why ask the AI to ask you questions first? What should a good ТЗ include?

### Module 09: Agent Memory Management
- **Source:** `modules/057-agent-memory-management/`
- **Status:** Include
- **LND notes:** Persistent memory across sessions. Critical for multi-session projects.
- **Practical thread:** **Convert the ТЗ into a structured task list (backlog)** stored in a markdown file. This becomes the project roadmap for remaining modules.
- **Quiz focus:** Why does the AI forget between sessions? What tools help maintain context?

### Module 10: Custom Instructions
- **Source:** `modules/070-custom-instructions/`
- **Status:** Include
- **LND notes:** Evolution from prompts to reusable instruction files. Key architecture concept.
- **Practical thread:** **Create first instruction files for Jira/Confluence workflows** — e.g., instruction for fetching issue data, instruction for updating Confluence pages. Based on the task list from Module 09.
- **Quiz focus:** What is the difference between a prompt and an instruction? When to create a new instruction?

### Module 11: Learning from Hallucinations
- **Source:** `modules/080-learning-from-hallucinations/`
- **Status:** Include
- **LND notes:** Transforming AI mistakes into instruction improvements. Practical debugging skill.
- **Practical thread:** **Improve the Jira/Confluence instructions** based on hallucinations encountered during Module 10. Document what went wrong and how instructions were refined.
- **Quiz focus:** What is a hallucination in AI context? How to turn a hallucination into an instruction improvement?

### Module 12: AI Skills & Tools Creation
- **Source:** `modules/090-ai-skills-tools-creation/`
- **Status:** Include
- **LND notes:** Combining instructions with tools for reliable automation. Formula: Instruction + Tool = Skill.
- **Practical thread:** **Build first automated skills for Jira/Confluence access** — parameterized tools that reliably fetch data from APIs without hallucination.
- **Quiz focus:** What is the difference between an instruction and a skill? Why add tools to instructions?

### Module 13: MCP — Model Context Protocol
- **Source:** `modules/100-mcp-model-context-protocol/`
- **Status:** Include
- **LND notes:** Foundational MCP module. Connecting AI to external data sources.
- **Practical thread:** **Explore MCP-based alternatives for some tasks from the backlog** — compare MCP approach vs skills approach for Jira/Confluence integration.
- **Quiz focus:** What is MCP? How does it differ from custom skills? When to use MCP vs custom tools?

### Module 14: MCP GitHub Integration — Issues
- **Source:** `modules/105-mcp-github-integration-issues/`
- **Status:** Include
- **LND notes:** Practical MCP usage with GitHub. Issue management automation.
- **Practical thread:** Create issues in the project repo from the task backlog. Practice managing project work through GitHub issues via AI agent.
- **Quiz focus:** How to configure GitHub MCP server? What can you automate with it?

### Module 15: Bulk File Processing with AI
- **Source:** `modules/160-bulk-file-processing-with-ai/`
- **Status:** Include
- **LND notes:** Three approaches for processing multiple files. Practical script-based automation.
- **Practical thread:** Process a batch of project files (e.g., analyze meeting notes, extract action items from multiple documents).
- **Quiz focus:** What are the three approaches to bulk processing? When to use each?

### Module 16: Development Environment Setup
- **Source:** `modules/110-development-environment-setup/`
- **Status:** Include
- **LND notes per feedback:** Add explanations of what Node.js is and why it's needed, what Docker is and why, what npm and nvm are — at least one sentence each. Assume the learner has never written a line of code. Explain each tool's purpose in plain language before installation.
- **Practical thread:** Set up the full development environment needed for prototyping in the next module.
- **Quiz focus:** What is Node.js and why do we need it? What is Docker? What does npm do?

### Module 17: Rapid Prototyping with SpecKit
- **Source:** `modules/120-rapid-poc-prototyping-with-speckit/`
- **Status:** Include
- **LND notes:** Full SpecKit workflow: specify → clarify → plan → tasks → analyze → implement → checklist. 
- **Practical thread:** **Build the Jira/Confluence automation prototype** — a working web application that connects to APIs and displays/manages data according to the ТЗ from Module 08.
- **Quiz focus:** What are the SpecKit phases? Why specify before implementing?

### Module 18: AI-Powered QA with Chrome DevTools MCP
- **Source:** `modules/130-chrome-devtools-mcp-qa-emulation/`
- **Status:** Include
- **LND notes:** Automated testing of the web application built in Module 17.
- **Practical thread:** **Test the prototype** — run AI-driven QA on the web app, find and fix issues, build basic QA documentation.
- **Quiz focus:** How does Chrome DevTools MCP work? What can the AI test automatically?

### Module 19: GitHub Coding Agent Delegation
- **Source:** `modules/150-github-coding-agent-delegation/`
- **Status:** Include
- **LND notes:** Delegating implementation tasks to an autonomous cloud agent.
- **Practical thread:** **Delegate a feature or bug fix** from the project backlog to the GitHub coding agent. Review the resulting PR.
- **Quiz focus:** What tasks are good candidates for delegation? How to write a good task description for the agent?

### Module 20: DIAL API Key and cURL Access
- **Source:** `modules/170-dial-api-key-curl-access/`
- **Status:** Include
- **LND notes:** Connecting to EPAM AI DIAL for custom model access. Final module — expands the toolkit.
- **Practical thread:** Test DIAL API access and explore how it could extend the project with custom model capabilities.
- **Quiz focus:** What is DIAL? How to test an API connection without programming?

---

## Excluded Modules (per feedback agreement)

| Module | Reason |
|--------|--------|
| 025-downloading-course-materials | Not needed for LND format |
| 056-prompt-engineering-toolkit | Overkill — prompting already covered sufficiently |
| 103-cli-command-line-interface | Too advanced for target audience |
| 104-port-to-skills | Too deep — MCP is enough |
| 140-advanced-mcp-integration-in-poc | Too advanced even for developers |
| 165-elitea-platform-mcp-integration | Covered in separate EliteA Level 2 course |
| 168-elitea-remote-mcp-http-integration | Same as above |
| 180-dial-langchain-python-integration | Too complex — marked as optional, not included |
| 185-prompt-templates-dynamic-queries | Same as above |
| 250-export-chat-session | Technique used for assessment, not a standalone module |
| 300-dmtools-agent-skill | Not part of core course |

---

## Assessment Strategy

**Per-module assessment:**
- 2-3 quiz questions after each module (multiple choice, 3 options, feedback on each answer)
- Practical task verification via chat session export or artifact submission

**Final course assessment options:**
1. **Chat session export review** — learner exports their chat session on the practical project topic, reviewer checks that the student actually worked through the assignments and achieved results
2. **Artifact submission** — learner submits key project artifacts:
   - Technical Specification (ТЗ) markdown file
   - Custom instructions/skills files
   - Working prototype (GitHub repo link)
   - QA test results documentation

**Grading:** Pass/Fail based on completeness of practical artifacts and quiz scores.

---

## Next Steps

1. Review and approve this plan
2. Generate Module 01 as a pilot — validate format with LND
3. Generate remaining modules following the approved format
4. Final review against SME Self-Review Checklist
5. Submit to LND for LMS upload
