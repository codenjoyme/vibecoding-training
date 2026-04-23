# Proposed New Modules — Elevator Pitches & Training Plans

> This document describes 15 new modules proposed for the Vibecoding for Everyone program.  
> Each module includes: elevator pitch, training plan outline, what the student gets, proposed placement in the curriculum, and motivation for that placement.

---

## Current Numbering Map (for reference)

```
010  Installing VSCode + GitHub Copilot
020  Installing Cursor
025  Downloading Course Materials
030  Model Selection
035  Visual Context with Screenshots
040  Agent Mode & AI Mechanics
050  Effective Prompting
055  Clarifying Requirements with AI
056  Prompt Engineering Toolkit
057  Agent Memory Management
060  Version Control with Git
070  Custom Instructions
080  Learning from Hallucinations
090  AI Skills & Tools Creation
100  MCP
103  CLI
104  Port to Skills
105  MCP GitHub Integration
110  Dev Environment Setup
120  Rapid Prototyping with SpecKit
125  SpecKit for Legacy Projects
130  QA with Chrome DevTools MCP
140  Advanced MCP Integration
150  GitHub Coding Agent Delegation
160  Bulk File Processing
165  Elitea Platform MCP
168  Elitea Remote MCP
170  DIAL API Key
180  DIAL + Python + Langchain
185  Prompt Templates
190  RAG
250  Export Chat Session
300  DMtools
```

Available gaps: `062-069`, `075-079`, `085-089`, `106-109`, `126-129`, `131-139`, `141-149`, `151-159`, `161-164`, `191-249`, `251-299`.

---

## ✅ Module 1: AI-Assisted Test Generation & Snapshot Testing

**Proposed ID:** `132`  
**Proposed Name:** AI-Assisted Test Generation & Snapshot Testing

### Elevator Pitch

You built a working prototype — but how do you know it still works after the next change? This module teaches you to generate tests with AI and introduces **snapshot testing** — a black-box approach where you run your code, record the output, commit it to Git, and let Git show you exactly what changed. No assertions to write. No test framework expertise needed. Just run → record → commit → diff.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Concept: Why test AI-generated code?** — Code you didn't write is code you don't understand. Tests are your safety net. Brief overview of test types: unit, integration, snapshot. |
| 2 | **AI generates unit tests** — Take a function from the PoC (module 120). Ask AI to generate tests. Run them. See what breaks. Understand coverage. |
| 3 | **Snapshot testing from scratch** — Write a simple runner script that executes your application as a black box (HTTP call, CLI command, function call) and dumps the output to a `.snapshot` file. |
| 4 | **Commit the snapshot** — `git add` the snapshot file. This is your baseline. The snapshot IS the assertion. |
| 5 | **Break something, re-run** — Change a piece of code. Re-run the snapshot script. The `.snapshot` file changes. `git diff` shows exactly what's different. |
| 6 | **Accept or reject** — If the change is intentional → `git add` the new snapshot (it becomes the new baseline). If not → revert. This is the entire workflow. |
| 7 | **Scale it** — Multiple snapshot files for different endpoints/scenarios. AI generates  the runner scripts for you. |
| 8 | **Integration with CI (conceptual)** — How snapshot tests plug into a pipeline: if snapshot differs from committed version → test fails. |

### What the Student Gets

- A working snapshot testing setup for their PoC
- Understanding that `git diff` is the most powerful assertion engine
- Ability to ask AI to generate tests for any code
- A mental model: "record → commit → diff → accept/reject"

### Placement Motivation

> **After 130 (QA with Chrome DevTools MCP)**, because 130 introduces QA concepts and browser testing. Module 132 extends this with code-level testing and the snapshot approach. It's a natural "and now test your code too" follow-up. Depends on: 060 (Git basics for diff/commit), 110+ (working PoC to test against).

---

## ✅ Module 2: AI Code Security Review

**Proposed ID:** `134`  
**Proposed Name:** AI Code Security Review

### Elevator Pitch

AI writes code fast. But does it write _safe_ code? This module teaches you to use AI as a security reviewer — catching hardcoded secrets, SQL injection, XSS, and insecure defaults in code that AI itself generated. You'll build a reusable security review prompt and learn to spot the patterns that AI consistently gets wrong.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The OWASP Top 10 in 5 minutes** — Quick overview of the most common vulnerabilities, focused on what AI tends to generate (hardcoded credentials, unsanitized inputs, missing auth checks). |
| 2 | **Hands-on: Review AI-generated code** — Take code from PoC module. Ask AI to find security issues. Review findings together. |
| 3 | **Build a security review instruction** — Create a reusable `./instructions/*.agent.md` that triggers security analysis on any code. |
| 4 | **Secret scanning** — How to detect API keys and tokens in code. `.env` patterns, `.gitignore` rules. Practical exercise. |
| 5 | **Fix with AI** — For each vulnerability found, ask AI to fix it. Verify the fix is real, not cosmetic. |

### What the Student Gets

- A security review instruction they can apply to any project  
- Awareness of top AI-generated code vulnerabilities  
- Practical `.env` + `.gitignore` security setup  

### Placement Motivation

> **After 132 (Snapshot Testing)** — follows the "verify your code" theme. After you test that it works (132), verify that it's safe (134). Depends on: 070 (instructions), 110+ (PoC code to review).

---

## ✅ Module 3: Token & API Key Management

**Proposed ID:** `108`  
**Proposed Name:** Token & API Key Management

### Elevator Pitch

Every module in this course uses API keys. But where do you put them? This module covers the practical side: `.env` files, environment variables, secret managers, and the one rule — never commit a key. You'll set up a proper secrets workflow that works for local dev and doesn't break when you push to GitHub.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Why keys leak** — Real examples of leaked tokens. What happens when a key hits GitHub. |
| 2 | **`.env` + `dotenv` pattern** — Create `.env`, add to `.gitignore`, load in Python/Node.js. Hands-on. |
| 3 | **Environment variables in terminal** — Set and read env vars in PowerShell and bash. |
| 4 | **Rotate a key** — Practice revoking and re-creating an API key. |
| 5 | **Checklist** — A simple checklist: before every commit, verify no secrets in staged files. |

### What the Student Gets

- A working `.env` setup for their projects  
- Muscle memory: "add `.env` to `.gitignore` first"  
- A secrets management checklist  

### Placement Motivation

> **After 105 (MCP GitHub) and before 110 (Dev Environment Setup)** — by this point the student has used multiple API keys (DIAL, GitHub, MCP servers). This is the right moment to formalize secrets management before the PoC phase where keys multiply. Depends on: 060 (Git, `.gitignore`), 100-105 (experience with API keys).

---

## ✅ Module 4: Evaluating AI Output Quality

**Proposed ID:** `085`  
**Proposed Name:** Evaluating AI Output Quality

### Elevator Pitch

How do you know the AI's answer is good? Not "feels right" — actually good. This module gives you a practical framework for assessing AI output: completeness, accuracy, hallucination detection, and consistency. You'll learn to score AI responses and make informed decisions about when to trust, verify, or reject.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The trust spectrum** — When to trust AI blindly, when to verify, when to reject. Framework based on task type and risk. |
| 2 | **Hallucination detection patterns** — Recognize common markers: confident but wrong, plausible but fabricated, outdated information. |
| 3 | **Practical scoring** — Take 5 AI responses to the same prompt. Score them on: correctness, completeness, relevance, safety. |
| 4 | **Cross-validation technique** — Ask two models the same question. Compare. Differences reveal uncertainty. |
| 5 | **Build a quality checklist** — Create a reusable "AI output review" checklist for your team. |

### What the Student Gets

- A mental framework for evaluating any AI output  
- Hallucination detection skills  
- A reusable quality assessment checklist  

### Placement Motivation

> **After 080 (Hallucinations) and before 090 (Skills & Tools)** — module 080 teaches that hallucinations happen and how to fix instructions. Module 085 adds a systematic quality evaluation layer. This understanding then motivates 090: "tools eliminate hallucinations because you can verify output programmatically."

---

## ✅ Module 5: CI/CD Pipeline with AI Agents

**Proposed ID:** `155`  
**Proposed Name:** CI/CD Pipeline with AI Agents

### Elevator Pitch

You've delegated tasks to the GitHub coding agent. Now automate the whole loop. This module sets up a GitHub Actions pipeline that runs tests, triggers AI reviews, and validates code quality — all automatically on every push. The AI agent becomes part of your continuous integration.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **GitHub Actions basics** — Create a `.github/workflows/ci.yml`. Trigger on push. Run a simple test. |
| 2 | **Add AI to the pipeline** — Configure Copilot code review as a step. See AI comments on PRs. |
| 3 | **Snapshot tests in CI** — Run snapshot tests from module 132 in the pipeline. Fail on diff. |
| 4 | **Notifications** — Get notified when pipeline fails. Simple webhook or email setup. |
| 5 | **The full loop** — Create issue → Agent codes PR → CI runs → Tests pass → Merge. Hands-on walkthrough. |

### What the Student Gets

- A working CI/CD pipeline with AI-powered checks  
- Understanding of automated quality gates  
- Experience with the full delegation-to-merge loop  

### Placement Motivation

> **After 150 (GitHub Coding Agent Delegation)** — module 150 teaches delegation. Module 155 adds the automated verification layer. Together they form a complete "delegate → verify → merge" workflow. Depends on: 132 (tests to run in CI), 150 (agent delegation).

---

## ✅ Module 6: AI-Assisted Code Review

**Proposed ID:** `152`  
**Proposed Name:** AI-Assisted Code Review

### Elevator Pitch

Reading someone else's code — or code AI wrote for you — is hard. This module teaches you to use AI as your code reviewer. You'll review PRs with AI assistance, catch bugs, suggest improvements, and build a review checklist that works for human and AI-generated code alike.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Why review AI code** — AI code compiles but may be subtly wrong. Examples of "looks good but isn't" code. |
| 2 | **Review with Copilot** — Open a PR from module 150. Use AI to summarize changes and flag concerns. |
| 3 | **Build a review instruction** — Create an instruction that structures AI code review: logic, security, performance, readability. |
| 4 | **Practice: Find the bug** — Pre-made examples with intentional issues. Use AI to find them. |
| 5 | **Review protocol** — A lightweight protocol for teams: what to always check in AI-generated PRs. |

### What the Student Gets

- Ability to review AI-generated code effectively  
- A reusable code review instruction  
- A team-ready review protocol  

### Placement Motivation

> **After 150 (GitHub Coding Agent)** and before 155 (CI/CD) — once you can delegate to an agent, you need to review what it produced. This is the human-in-the-loop step before automation (155). Depends on: 150 (PRs to review), 070 (instructions for review prompts).

---

## ✅ Module 7: Shared Instructions & Team Conventions

**Proposed ID:** `075`  
**Proposed Name:** Shared Instructions & Team Conventions

### Elevator Pitch

You've built personal instructions that work for you. But your team reinvents the same prompts every day. This module teaches you to create a shared instruction repository — versioned, reviewed, and distributed via Git. One team member finds a better prompt → everyone benefits.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The problem** — Every team member has different AI quality because everyone prompts differently. |
| 2 | **Shared repo structure** — Create a shared instructions folder: team conventions, code style, review checklists. |
| 3 | **Git-based distribution** — Clone, update, PR. Instructions as code. |
| 4 | **Conflict resolution** — When two instructions contradict, how to merge. Priority rules. |
| 5 | **Adoption strategy** — How to introduce shared instructions to a team that's never used them. |

### What the Student Gets

- A template shared-instructions repository  
- Understanding of instructions-as-code workflow  
- An adoption playbook for their team  

### Placement Motivation

> **After 070 (Custom Instructions)** — module 070 teaches creating personal instructions. Module 075 extends this to the team level. This prepares the student for 080+ where instructions become more sophisticated. Depends on: 070 (instructions), 060 (Git).

---

## ✅ Module 8: AI Cost Optimization

**Proposed ID:** `083`  
**Proposed Name:** AI Cost Optimization & Token Economics

### Elevator Pitch

Every AI call costs money. This module teaches you to read the meter: how tokens are counted, what context windows cost, and how to cut your AI bill in half without losing quality. Essential knowledge for any manager approving AI tool budgets.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Token economics 101** — What's a token, how pricing works, input vs. output costs. |
| 2 | **Measure your usage** — Check your Copilot/API usage dashboard. Understand the numbers. |
| 3 | **Cost reduction techniques** — Smaller context, smarter models for simple tasks, caching, prompt compression. |
| 4 | **Model routing** — Use cheap models for easy tasks, expensive models for hard ones. Decision matrix. |
| 5 | **Budget planning** — How to estimate monthly AI costs for a team of N people. |

### What the Student Gets

- Ability to read and interpret AI usage dashboards  
- Concrete cost reduction techniques  
- A budget estimation template for team AI usage  

### Placement Motivation

> **After 080 (Learning from Hallucinations) and before 085 (Evaluating AI Output Quality)** — by module 080 the student has solid AI usage experience across many tasks. Module 083 gives economic context at the right moment: when they're already experienced enough to appreciate cost implications for a team. Marked as optional — primarily relevant for managers and team leads. Depends on: 030 (Model Selection).

---

## ✅ Module 9: Onboarding with AI

**Proposed ID:** `197`  
**Proposed Name:** Onboarding New Team Members with AI

### Elevator Pitch

New team member joins. Instead of 2 weeks of reading wikis, they open the IDE and ask the AI: "How does the auth module work?" This module shows how to set up AI-powered onboarding: project-aware instructions, codebase Q&A, and SpecKit documentation as the onboarding backbone.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The onboarding problem** — Why traditional onboarding is slow. Knowledge is scattered, docs are stale. |
| 2 | **Project-aware instructions** — Create an onboarding instruction that explains project structure, conventions, key decisions. |
| 3 | **Codebase Q&A** — Use AI to answer "where is X?", "how does Y work?", "why was Z chosen?". |
| 4 | **SpecKit as knowledge base** — Connect SpecKit docs (from module 125) to make AI answers grounded in real documentation. |
| 5 | **The 30-minute onboarding** — Simulate new-joiner experience: open repo, activate instructions, ask 10 key questions. Evaluate quality. |

### What the Student Gets

- An onboarding instruction template  
- A tested workflow for AI-assisted onboarding  
- Understanding of how documentation quality affects AI onboarding quality  

### Placement Motivation

> **After 190 (RAG)** — this is an applied use case that combines RAG (190), SpecKit (125), and instructions (070). It's a capstone-style module that shows how earlier skills create team-level value. Depends on: 070, 125, 190.

---

## ✅ Module 10: Multi-Agent Orchestration

**Proposed ID:** `195`  
**Proposed Name:** Multi-Agent Orchestration

### Elevator Pitch

One agent writes code. Another reviews it. A third runs tests. You're the manager who delegates to all three. This module introduces multi-agent patterns: how to split work, coordinate agents, and get higher-quality results than any single agent can produce alone.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Why multi-agent** — Single agent limitations: context drift, role confusion, quality plateau. |
| 2 | **Agent roles** — Define specialized agents: planner, coder, reviewer, tester. Each with its own instruction. |
| 3 | **Orchestration patterns** — Sequential (pipeline), parallel (fan-out/fan-in), supervisor. When to use which. |
| 4 | **Hands-on: Two-agent pipeline** — Agent 1 writes code, Agent 2 reviews it. Set up in VS Code with sub-agents. |
| 5 | **Scaling with GitHub agents** — Combine local agents (Copilot) with remote agents (GitHub coding agent) for parallel work. |

### What the Student Gets

- Understanding of multi-agent architecture patterns  
- A working two-agent pipeline (coder + reviewer)  
- Mental model for when to use multi-agent vs. single agent  

### Placement Motivation

> **After 190 (RAG) and before 197 (Onboarding)** — by this point the student has mastered individual agent skills. Module 195 is the graduation to orchestrating multiple agents. Comes before the applied capstone modules (197, 250+). Depends on: 070 (instructions per agent), 150 (delegation patterns).

---

## ✅ Module 11: AI for Data Analysis & Reporting

**Proposed ID:** `200`  
**Proposed Name:** AI for Data Analysis & Reporting

### Elevator Pitch

You have a CSV export from Jira, a spreadsheet of test results, or a log file with 10,000 lines. Instead of opening Excel, you paste it into the AI chat and ask: "What's the trend? Build me a chart." This module teaches managers to use AI for the analysis they actually need — without writing pandas code from scratch.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **AI as analyst** — Paste CSV data, ask questions. See AI generate insights, summaries, anomalies. |
| 2 | **Structured analysis** — Ask AI to create pivot tables, group data, compute metrics. |
| 3 | **Visualization** — Generate charts (matplotlib, mermaid) from data. Export as images. |
| 4 | **Report generation** — Ask AI to write a summary report from raw data. With conclusions and recommendations. |
| 5 | **Automation** — Build a Python script that reads a file, runs analysis, and outputs a report. Reusable. |

### What the Student Gets

- Ability to analyze any CSV/Excel data through AI chat  
- A reusable data-analysis Python script  
- A report generation workflow  

### Placement Motivation

> **After 195 (Multi-Agent) and before 250 (Export Chat)** — this is a standalone "manager skill" module. Placed in the 200 range because it's an applied use case that uses Python (180), prompt templates (185), and general AI fluency. Doesn't block other modules.

---

## ✅ Module 12: Structured Output & JSON Mode

**Proposed ID:** `187`  
**Proposed Name:** Structured Output & JSON Mode

### Elevator Pitch

AI gives you prose. Your code needs JSON. This module teaches you to get structured, machine-readable output from any LLM — JSON schemas, typed responses, and validation. Essential for building real integrations where AI output feeds directly into your application.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The problem** — AI says "here are 3 items" but the format changes every time. You can't parse it. |
| 2 | **JSON mode** — Enable structured output in API calls. See consistent JSON responses. |
| 3 | **Schema definition** — Define expected output shape. Validate responses against schema. |
| 4 | **Langchain output parsers** — Use Langchain's `PydanticOutputParser` to get typed Python objects from AI. |
| 5 | **Integration** — Build a mini-pipeline: prompt → structured JSON → save to file. |

### What the Student Gets

- Ability to get reliable JSON from any LLM  
- Working code with Langchain output parsers  
- A template for structured AI-to-application pipelines  

### Placement Motivation

> **After 185 (Prompt Templates) and before 190 (RAG)** — module 185 teaches parameterized prompts. Module 187 adds structured output: now you control both input AND output format. This is a prerequisite for robust RAG (190) where output structure matters. Depends on: 180 (Python + Langchain), 185 (prompt templates).

---

## ✅ Module 13: AI-Assisted Refactoring

**Proposed ID:** `126`  
**Proposed Name:** AI-Assisted Refactoring

### Elevator Pitch

Your PoC works but the code is a mess — AI generated it in one pass and it shows. This module teaches you to use AI to refactor: extract functions, rename variables, simplify logic, and restructure files. You'll learn when and how to ask AI to clean up after itself.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **When to refactor** — Signs of messy AI code: 200-line functions, copy-paste duplication, unclear naming. |
| 2 | **Safe refactoring with Git** — Baby step approach: refactor one thing, commit, verify. Rollback if broken. |
| 3 | **AI as refactoring partner** — Prompts: "extract this into a function", "simplify this logic", "rename for clarity". |
| 4 | **Hands-on** — Take PoC code from module 120/125. Apply 3 refactoring passes. Compare before/after. |
| 5 | **Refactoring instruction** — Create a reusable refactoring instruction: code style rules, naming conventions, complexity limits. |

### What the Student Gets

- Practical AI-assisted refactoring skills  
- A refactoring instruction template  
- Understanding of safe refactoring in baby steps  

### Placement Motivation

> **After 125 (SpecKit for Legacy Projects)** — module 125 documents existing code. Module 126 improves it. Natural sequence: understand → document → improve. Uses Git baby steps from 060. Depends on: 060 (Git), 070 (instructions), 120/125 (code to refactor).

---

## ✅ Module 14: Database Schema Design with AI

**Proposed ID:** `128`  
**Proposed Name:** Database Schema Design with AI

### Elevator Pitch

Every app needs data. This module teaches you to design database schemas, generate migrations, and write queries — all through AI. From "I need a users table with roles" to a working SQL schema in 5 minutes.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Schema from requirements** — Describe your data model in plain language. AI generates the schema. |
| 2 | **Review and iterate** — Check relationships, indexes, constraints. Ask AI to improve. |
| 3 | **Migration files** — Generate SQL migration scripts. Understand up/down migrations. |
| 4 | **Query generation** — Ask AI to write complex queries. Join tables, aggregate data, filter. |
| 5 | **Integration into PoC** — Add database layer to your SpecKit project. See it work end-to-end. |

### What the Student Gets

- A working database schema for their PoC  
- Understanding of schema design through AI conversation  
- Reusable migration and query generation workflow  

### Placement Motivation

> **After 126 (Refactoring)** and before 130 (QA) — at this point the student has a working PoC (120), documented it (125), cleaned it up (126). Adding a data layer (128) completes the "real application" stack before QA (130) and MCP integration (140). Depends on: 110 (dev environment), 120 (PoC to extend).

---

## ✅ Module 15: Debugging AI-Generated Code

**Proposed ID:** `064`  
**Proposed Name:** Debugging AI-Generated Code

### Elevator Pitch

The code AI wrote doesn't work. The error message means nothing to you. And if you paste the error back, AI goes in circles. This module teaches you a systematic debugging approach: read the error, isolate the problem, provide the right context, and break the infinite "fix → new error → fix" loop.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The debug loop trap** — Why naive "paste error → get fix → new error" fails. AI lacks state between turns. |
| 2 | **Reading error messages** — Anatomy of an error: type, message, stack trace, location. What to paste, what to skip. |
| 3 | **Isolation technique** — Reduce the problem: comment out code, test in isolation, find the minimal reproduction. |
| 4 | **Context loading** — Give AI the right files, the right error, and the right question. The "debug prompt" template. |
| 5 | **Practice: Fix 3 bugs** — Pre-made broken code. Apply the debugging workflow. AI assists, you drive. |
| 6 | **Escape hatches** — When to stop debugging and rewrite. When to rollback (Git baby steps). When to ask a human. |

### What the Student Gets

- A systematic debugging workflow for AI-generated code  
- A reusable "debug prompt" template  
- The ability to break out of infinite error loops  

### Placement Motivation

> **After 060 (Git) and before 070 (Custom Instructions)** — the student has been writing code with AI for several modules. By module 064 they've hit bugs. This is the "rescue kit" module. It comes before instructions (070) because debugging understanding motivates writing better instructions. Depends on: 050 (prompting), 060 (Git for rollbacks).

---

## Summary: All Proposed Modules in Course Order

| ID | Name | Phase |
|----|------|-------|
| **083** | AI Cost Optimization & Token Economics | Setup & Understanding |
| **064** | Debugging AI-Generated Code | Techniques |
| **075** | Shared Instructions & Team Conventions | Tools |
| **085** | Evaluating AI Output Quality | Tools |
| **108** | Token & API Key Management | Integration |
| **126** | AI-Assisted Refactoring | Integration |
| **128** | Database Schema Design with AI | Integration |
| **132** | AI-Assisted Test Generation & Snapshot Testing | Integration |
| **134** | AI Code Security Review | Integration |
| **152** | AI-Assisted Code Review | Orchestration |
| **155** | CI/CD Pipeline with AI Agents | Orchestration |
| **187** | Structured Output & JSON Mode | Advanced |
| **195** | Multi-Agent Orchestration | Advanced |
| **197** | Onboarding New Team Members with AI | Applied |
| **200** | AI for Data Analysis & Reporting | Applied |

### Updated Learning Path (with new modules marked ★)

```
010  Installing VSCode + GitHub Copilot
020  Installing Cursor
025  Downloading Course Materials
030  Model Selection
035  Visual Context with Screenshots
040  Agent Mode & AI Mechanics
050  Effective Prompting
055  Clarifying Requirements with AI
056  Prompt Engineering Toolkit
057  Agent Memory Management
060  Version Control with Git
064  ★ Debugging AI-Generated Code
070  Custom Instructions
075  ★ Shared Instructions & Team Conventions
080  Learning from Hallucinations
083  ★ AI Cost Optimization & Token Economics *(optional)*
085  ★ Evaluating AI Output Quality
090  AI Skills & Tools Creation
100  MCP
103  CLI
104  Port to Skills
105  MCP GitHub Integration
108  ★ Token & API Key Management
110  Dev Environment Setup
120  Rapid Prototyping with SpecKit
125  SpecKit for Legacy Projects
126  ★ AI-Assisted Refactoring
128  ★ Database Schema Design with AI
130  QA with Chrome DevTools MCP
132  ★ AI-Assisted Test Generation & Snapshot Testing
134  ★ AI Code Security Review
140  Advanced MCP Integration
150  GitHub Coding Agent Delegation
152  ★ AI-Assisted Code Review
155  ★ CI/CD Pipeline with AI Agents
160  Bulk File Processing
165  Elitea Platform MCP
168  Elitea Remote MCP
170  DIAL API Key
180  DIAL + Python + Langchain
185  Prompt Templates
187  ★ Structured Output & JSON Mode
190  RAG
195  ★ Multi-Agent Orchestration
197  ★ Onboarding New Team Members with AI
200  ★ AI for Data Analysis & Reporting
250  Export Chat Session
300  DMtools
```

### Dependency Graph (new modules only)

```
083 (Cost)         ← 030 (Model Selection)
064 (Debugging)    ← 050 (Prompting) + 060 (Git)
075 (Team Instr.)  ← 070 (Custom Instructions) + 060 (Git)
085 (Quality Eval) ← 080 (Hallucinations)
108 (Secrets)      ← 060 (Git) + 100-105 (API key experience)
126 (Refactoring)  ← 060 (Git) + 120/125 (PoC code)
128 (DB Schema)    ← 110 (Dev Env) + 120 (PoC)
132 (Snapshot Test) ← 060 (Git) + 110+ (PoC to test)
134 (Security)     ← 070 (Instructions) + 110+ (code to review)
152 (Code Review)  ← 150 (Delegation) + 070 (Instructions)
155 (CI/CD)        ← 132 (Tests) + 150 (Delegation)
187 (JSON Mode)    ← 180 (Python) + 185 (Templates)
195 (Multi-Agent)  ← 070 (Instructions) + 150 (Delegation)
197 (Onboarding)   ← 070 + 125 (SpecKit) + 190 (RAG)
200 (Data Analysis) ← 180 (Python) + 185 (Templates)
193 (LangGraph)    ← 180 (Python) + 190 (RAG) + 195 (Multi-Agent)
220 (Study Buddy)  ← 050 (Prompting) + 056 (Toolkit)
230 (Module Create) ← 070 (Instructions) + 060 (Git)
```

---

## ✅ Module 16: LangGraph & Advanced Agent Frameworks

**Proposed ID:** `193`  
**Proposed Name:** LangGraph & Advanced Agent Frameworks

### Elevator Pitch

Module 195 teaches multi-agent patterns as concepts. This module gets your hands dirty with a real framework — LangGraph. You'll build a stateful multi-agent pipeline with conditional routing, persistence, and human-in-the-loop approval. When one agent's output is bad, the pipeline automatically retries with a different strategy. This is how production AI applications are built.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **Why frameworks matter** — The gap between "two agents in chat" and a production pipeline. State management, error recovery, persistence. |
| 2 | **LangGraph fundamentals** — Nodes, edges, state. Build a minimal graph: input → process → output. |
| 3 | **Conditional routing** — Add branching: if quality score < threshold → retry with different prompt. |
| 4 | **Multi-agent graph** — Three nodes: Coder → Reviewer → Fixer. Reviewer can send back to Coder. |
| 5 | **Human-in-the-loop** — Add an interrupt point: graph pauses, asks human for approval, continues. |
| 6 | **Persistence** — Save graph state to disk. Resume interrupted workflows. |
| 7 | **Compare frameworks** — Brief overview of CrewAI, AutoGen, and when each fits. |

### What the Student Gets

- A working LangGraph pipeline with 3 agents and conditional logic
- Understanding of stateful vs stateless agent orchestration
- Ability to choose the right framework for their use case
- A reusable multi-agent graph template

### Placement Motivation

> **After 190 (RAG) and before 195 (Multi-Agent Orchestration concepts)** — actually placed at 193 to complement 195. Module 195 gives the conceptual patterns (sequential, parallel, supervisor). Module 193 implements these patterns in a real framework. Together they form a complete multi-agent chapter. Depends on: 180 (Python + Langchain), 190 (RAG for grounded agents).

---

## ✅ Module 17: AI Study Buddy — Learning New Tech

**Proposed ID:** `220`  
**Proposed Name:** AI Study Buddy — Learning New Tech

### Elevator Pitch

You need to learn Kubernetes. Or Terraform. Or a new framework your team adopted. Instead of spending days on documentation, you open a chat and start a structured learning conversation. AI explains concepts at your level, quizzes you, gives practice tasks, and checks your solutions. This module teaches the Feynman method powered by AI — the fastest way to go from zero to functional understanding of any technology.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The learning problem** — Why traditional docs/tutorials fail for busy managers. The Feynman technique: explain it simply → find gaps → go deeper. |
| 2 | **The Study Buddy prompt** — Create a structured prompt: "I need to learn X. My background is Y. Start with fundamentals, then quiz me." |
| 3 | **Concept exploration** — Pick a real unfamiliar technology. Ask AI to explain core concepts. Practice the "explain like I'm five" → "now give me the real version" pattern. |
| 4 | **Active recall** — Ask AI: "Give me 5 questions to test my understanding." Answer them. AI evaluates. |
| 5 | **Practice tasks** — "Give me a hands-on exercise I can do in 10 minutes." Complete it. AI reviews your solution. |
| 6 | **Knowledge map** — Ask AI to generate a topic map (Mermaid diagram) showing what you've learned and what's left. |
| 7 | **Build a study instruction** — Create a reusable `.agent.md` instruction that automates this learning workflow for any topic. |

### What the Student Gets

- A proven methodology for AI-assisted learning of any technology
- A reusable "study buddy" instruction file
- Experience with active recall and Feynman technique via AI
- A knowledge map visualization of their learning progress

### Placement Motivation

> **After 200 (Data Analysis) and before 250 (Export Chat)** — this is a standalone applied module. By module 220 the student has mastered all core AI skills. Now they learn to use AI for their own professional growth. Placed in the 200+ range as an "applied skill" module. Depends on: 050 (prompting basics), 056 (prompt engineering toolkit for advanced techniques).

---

## ✅ Module 18: Creating Training Modules from Articles

**Proposed ID:** `230`  
**Proposed Name:** Creating Training Modules from Articles

### Elevator Pitch

You found an amazing article about a new GenAI approach. Now you want to turn it into a training module for your team — with structure, walkthrough, prerequisites, and hands-on exercises. This module teaches you to feed an article (or any source material) to an AI agent and get back a complete, formatted training module that follows course conventions. One article in → one ready-to-use module out.

### Training Plan

| Step | What happens |
|------|-------------|
| 1 | **The module factory pattern** — How our course modules are structured: `about.md` + `walkthrough.md`. Required sections, formatting rules, prerequisites format. |
| 2 | **Source material preparation** — How to feed an article/blog/video-transcript to AI: paste text, provide URL context, highlight the key concept to teach. |
| 3 | **The creation prompt** — Build the master prompt: "Here's an article. Create a training module following these instructions. Module ID is X. Figure out dependencies." |
| 4 | **Hands-on: Create a module** — Take a real article about a GenAI topic. Feed it to AI with the creation instructions. Get `about.md` + `walkthrough.md`. |
| 5 | **Quality review** — Check generated module against the quality checklist: correct prerequisites format, understanding questions, troubleshooting section, cross-platform paths. |
| 6 | **Integration** — Add the new module to `training-plan.md`, verify folder naming, commit to Git. |
| 7 | **Fork & PR workflow** — For shared course repos: fork, add module, submit PR. The "contribute a module" workflow. |

### What the Student Gets

- Ability to create course-quality training modules from any source material
- Understanding of the module structure and quality standards
- A reusable "module creation" prompt/instruction
- Experience with fork & PR contribution workflow

### Placement Motivation

> **After 220 (AI Study Buddy) and before 250 (Export Chat)** — this is a meta-module about creating content for the course itself. By module 230 the student has consumed many modules and understands the format intuitively. Now they learn to produce modules. Depends on: 070 (custom instructions — understanding instruction format), 060 (Git — for committing and PR workflow).
