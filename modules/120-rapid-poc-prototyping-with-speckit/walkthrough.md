# Rapid Prototyping with SpecKit - Hands-on Walkthrough

In this module, you will learn and practice the **SpecKit** spec-driven development methodology. First, you will go through the theory of each SpecKit phase. Then you will open a second IDE window as a fresh workspace and run through the full SpecKit workflow to build a real full-stack Node.js application deployed in Docker.

## Prerequisites

Before starting, ensure you have:
- Completed [Module 110: Development Environment Setup](../110-development-environment-setup/about.md) — Node.js ≥ 20 and Docker must be working
- Completed [Module 070: Custom Instructions](../070-custom-instructions/about.md)
- Completed [Module 040: Agent Mode & AI Mechanics](../040-agent-mode-under-the-hood/about.md)
- GitHub Copilot with Agent Mode enabled (VSCode or Cursor)
- `uv` package manager available (see installation in Part 1)

## What We'll Learn and Build

**Theory (Parts 1–9):** Deep dive into each SpecKit phase and what it produces.

**Practice (Part 10):** Open a second IDE window, initialize SpecKit, and build a full-stack application of your choice using:

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + React Router v6 + Vite |
| Backend | Node.js ≥ 20 + Express 4 |
| Database | PostgreSQL 15 |
| Infrastructure | Docker + Docker Compose |
| Dev Workflow | SpecKit (spec-driven development) |

---

## Part 1: What is SpecKit?

### The Problem SpecKit Solves

When you ask an AI to "build a task manager app," it starts writing code immediately — without understanding your real requirements, edge cases, or constraints. The result is often:
- Code that doesn't match what you actually needed
- Incorrect database schema that requires painful rewrites
- No documentation of what was built and why

**SpecKit introduces a discipline: spec before code.**

### The Core Idea

SpecKit is a spec-driven development framework for AI-assisted coding. Instead of jumping straight to implementation, it enforces a structured workflow:

```
Idea → Spec → Clarify → Plan → Tasks → Analyze → Implement → Checklist
```

Every step produces a **file** in your `specs/` folder. These files become:
- The source of truth for what the feature does
- A reference for the AI during implementation
- Documentation for the team

### How SpecKit Works

SpecKit installs **slash commands** into your AI assistant. In Agent Mode, you type `/speckit.specify My idea here` and the AI generates a structured spec file. Each command is a prompt template that knows what to produce and how.

When SpecKit is initialized in a project, it adds:
- An instructions file that teaches the AI the full workflow
- PowerShell (or bash) scripts for each slash command
- A `specs/` folder structure for the artifacts

### The Output: A Specs Folder

After going through the workflow, your project will contain:

```
specs/
  001-feature-name/
    spec.md          ← WHAT and WHY (no implementation details)
    plan.md          ← HOW (technical decisions)
    data-model.md    ← Database schema
    tasks.md         ← Ordered list of implementation tasks
    contracts/       ← API request/response contracts
    checklists/      ← QA validation criteria
```

This folder is committed to version control alongside code. Future developers (and AI agents) can understand not just what was built, but why decisions were made.

---

## Part 2: SpecKit Slash Commands Overview

SpecKit provides 8 commands, used in order. Each command is a phase in the workflow.

```
/speckit.constitution        ← once per project: establish principles
/speckit.specify <desc>      ← create spec.md from plain English
/speckit.clarify             ← Q&A to resolve ambiguities
/speckit.plan <tech stack>   ← generate plan.md, data-model.md
/speckit.tasks               ← generate tasks.md
/speckit.analyze             ← consistency check before coding
/speckit.implement           ← execute tasks one by one
/speckit.checklist           ← QA validation
```

**Key principle:** You should not skip steps. Each phase builds on the previous one. The AI is instructed to refuse to implement until a valid spec and plan exist.

Think of these commands as **gateways** — each one produces a document that unlocks the next step.

---

## Part 3: `/speckit.constitution` — Establishing Principles

### What It Does

This command is run **once per project**. It creates the foundational rules the AI will follow for everything else in this codebase.

The constitution captures:
- Coding standards and conventions
- Architecture decisions that apply everywhere
- What the project is for and who it serves
- Non-negotiable constraints (security, performance, etc.)

### What It Produces

A `constitution.md` file (or equivalent) in the project root or `specs/` folder. This document is loaded by the AI every time it works in this project.

### When to Run It

- At the very beginning of a new project
- Before writing any code or creating any specs
- After a major pivot that changes fundamental assumptions

### Why It Matters

Without a constitution, different AI sessions may make contradictory decisions. With a constitution, every AI interaction is anchored to the same principles. The AI "knows" that your project uses PostgreSQL, not MongoDB — so it won't suggest the wrong database in a plan.

---

## Part 4: `/speckit.specify` — Writing the Spec

### What It Does

You provide a plain English description of what you want to build. The AI transforms it into a structured `spec.md` file with:
- **Feature title** and concise summary
- **Problem statement** — why this feature exists
- **User stories** — who does what and why
- **Acceptance criteria** — how you know it's done
- **Out of scope** — what the feature deliberately does NOT do
- **Open questions** — things that need clarification

### Example

```
/speckit.specify Allow users to register and log in with Google OAuth
```

The AI generates a full spec file, not code. It answers: **WHAT** the feature is and **WHY** it's needed — not HOW to build it.

### Why No Tech Decisions in the Spec?

The spec describes behavior, not implementation. This separation is intentional:
- The spec can be reviewed by non-technical stakeholders
- The same spec could be implemented with different tech stacks
- It forces you to think about what you need before how to build it

### What the Output Looks Like

```markdown
# Feature: Google OAuth Registration and Login

## Problem
Users need a way to authenticate without managing passwords...

## User Stories
- As a new user, I want to sign up with my Google account so that I don't need to create a password
- As a returning user, I want to log in with Google so that I can access my data securely

## Acceptance Criteria
- [ ] User can click "Sign in with Google" and be redirected to Google
- [ ] After Google approval, user is logged into the app
- [ ] User session persists across page reloads
...

## Out of Scope
- Email/password authentication
- Two-factor authentication
```

---

## Part 5: `/speckit.clarify` — Resolving Ambiguities

### What It Does

After generating the spec, the AI reviews it and asks targeted questions about anything ambiguous, undefined, or potentially conflicting. You answer the questions and the spec gets updated.

This is a **dialogue phase** — the AI is essentially doing requirements elicitation.

### Example Questions the AI Might Ask

- "Should existing users who signed up with email be able to link a Google account later?"
- "What happens if Google returns an email that already exists in the database?"
- "Should the session expire after a fixed time, or only on explicit logout?"
- "Do you need role-based access or is all users equal for now?"

### Why This Step Exists

Ambiguities caught in the spec phase cost minutes to fix. The same ambiguity caught during implementation or testing can cost hours or days. The `/speckit.clarify` step is an explicit investment in upfront thinking.

### What You Do

1. Run `/speckit.clarify`
2. The AI presents a numbered list of questions
3. Answer each question (can be short answers)
4. The AI updates `spec.md` to reflect your answers
5. Repeat until no open questions remain

---

## Part 6: `/speckit.plan` — Technical Planning

### What It Does

Now that the **WHAT** is clear, this command answers **HOW**. You provide the technology stack, and the AI generates:
- `plan.md` — technical implementation approach
- `data-model.md` — database schema (tables, columns, indexes, constraints)
- `contracts/` — API endpoint contracts (request/response shapes)

### Example Usage

```
/speckit.plan React 18 + Vite frontend, Node.js + Express backend, PostgreSQL 15, Docker
```

### What `plan.md` Contains

- Component breakdown (which new files/modules are needed)
- Data flow (how data moves from user action → API → DB → response)
- Security approach
- Error handling strategy
- Performance considerations
- Integration points with existing code

### What `data-model.md` Contains

```sql
-- users table
CREATE TABLE users (
  id          SERIAL PRIMARY KEY,
  google_id   TEXT UNIQUE NOT NULL,
  email       TEXT UNIQUE NOT NULL,
  name        TEXT,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

The data model is reviewed **before** writing migrations. Mistakes in schema design are caught here, not during implementation.

### Why Tech Stack Goes Here, Not in the Spec

The spec is technology-agnostic. The plan is where you commit to specific choices. This allows you to change tech stack decisions without touching the feature requirements.

---

## Part 7: `/speckit.tasks` — Generating the Task List

### What It Does

Based on the spec, plan, and data model, the AI generates an ordered list of implementation tasks in `tasks.md`. Each task is small, specific, and independently verifiable.

### What a Good Task List Looks Like

```markdown
# Tasks: Google OAuth Login

## Phase 1: Infrastructure
- [ ] 1. Create `migrations/001-users-table.sql` with users table schema
- [ ] 2. Add `google-auth-library` and `jsonwebtoken` to package.json
- [ ] 3. Create `.env.example` with GOOGLE_CLIENT_ID, JWT_SECRET variables

## Phase 2: Backend
- [ ] 4. Create `src/auth/google.js` — OAuth callback handler
- [ ] 5. Create `src/auth/jwt.js` — token signing and verification utilities
- [ ] 6. Mount auth routes at `/auth` in `app.js`
- [ ] 7. Create `src/middleware/requireAuth.js` — JWT cookie middleware

## Phase 3: Frontend
- [ ] 8. Add "Sign in with Google" button to login page
- [ ] 9. Handle OAuth redirect and token storage
- [ ] 10. Create `AuthContext` for global auth state

## Phase 4: Tests
- [ ] 11. Write unit tests for JWT utilities
- [ ] 12. Write integration test for OAuth callback endpoint
```

### Why Task Granularity Matters

Tasks should be small enough that:
- Each can be implemented and tested independently
- A failed task doesn't break other tasks
- The AI can focus on one thing at a time

Vague tasks like "implement auth" are not useful. Specific tasks like "create JWT signing utility" are.

---

## Part 8: `/speckit.analyze` — Consistency Check

### What It Does

Before any code is written, the AI performs a consistency check across all the spec artifacts:
- Does the `plan.md` cover all acceptance criteria from `spec.md`?
- Does the `data-model.md` support all the data needs from the plan?
- Are all API contracts defined for each task that needs them?
- Are there any contradictions between documents?
- Are any tasks missing or out of order?

### What It Reports

The AI outputs a structured analysis:
- **Gaps** — things mentioned in the spec but not covered in the plan
- **Contradictions** — conflicting statements across documents
- **Missing artifacts** — API contracts that haven't been defined
- **Risk flags** — tasks that might need special attention

### Why This Step Exists

It is a pre-flight check. The cost of finding an inconsistency in specs is minutes. The cost of finding it mid-implementation is hours.

This step is especially valuable in complex features where the spec, plan, and data model were written in separate sessions.

---

## Part 9: `/speckit.implement` and `/speckit.checklist`

### `/speckit.implement` — Executing Tasks

This command tells the AI to start implementing tasks from `tasks.md`, one by one. The AI:
1. Reads the current task
2. Refers back to `spec.md`, `plan.md`, `data-model.md`, and relevant contracts
3. Writes the code
4. Marks the task as done in `tasks.md`
5. Moves to the next task

**Key behavior:** The AI will not write code that is not covered by a task. If it finds something missing, it will ask you to add a task first rather than improvising.

### `/speckit.checklist` — QA Validation

After implementation, this command generates QA checklists in `specs/001-feature/checklists/` and validates:
- All acceptance criteria from `spec.md` are met
- API contracts match actual implementation
- Edge cases are handled
- No regressions in existing functionality

The checklist is a living document — you mark items as verified after manual or automated testing.

---

## Part 10: Practice — Build Your Own App with SpecKit

### What We'll Do

You will now apply everything from Parts 1–9 in a real project. The practice runs in a **second IDE window** — a separate, clean workspace — while this training window stays open for reference.

**Why a separate workspace?**

SpecKit installs its own instruction files that take control of the AI agent's behavior in that workspace. Running it in the training workspace would conflict with the existing course instructions. By opening a second IDE window, you keep both environments clean and independent.

You can share context between windows using screenshots (see [Module 035: Visual Context with Screenshots](../035-visual-context-screenshots/about.md)).

---

### Step 1: Prepare the Second Workspace

**Open a second IDE window:**

- In VSCode: Menu → **File → New Window**
- In Cursor: Menu → **File → New Window**

**Create an empty workspace folder:**

```
# Windows
c:/workspace/speckit-poc/

# macOS/Linux
~/workspace/speckit-poc/
```

Open this empty folder in the new IDE window.

**Verify you have `uv` installed** (needed for SpecKit CLI):

```powershell
uv --version
```

If not installed:

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### Step 2: Copy the Architecture Reference

Before starting SpecKit, copy the architecture blueprint into your new workspace so the AI can reference it.

1. In your new workspace, create a `tools/` folder
2. Copy [tools/architecture.md](../120-rapid-poc-prototyping-with-speckit/tools/architecture.md) from this module into `tools/architecture.md` in the new workspace

This file describes the full-stack Node.js + Docker architecture that the AI will use during the `/speckit.plan` phase.

---

### Step 3: Decide What to Build

Before initializing SpecKit, think of something you actually want to build. It should be a real application with:
- User-facing functionality (not just "hello world")
- A reason to exist (solves a real or imagined problem)
- At least 2–3 distinct features

**Examples to spark ideas:**
- Personal expense tracker with categories and monthly summary
- Simple team task board (Kanban-lite) with card assignment
- Recipe book with ingredient search and shopping list generation
- Movie watchlist with ratings and "watched/unwatched" status
- Daily journal with mood tracking and calendar view

Write down your idea in one sentence — you will use it as the first SpecKit input.

---

### Step 4: Initialize SpecKit in the New Workspace

Switch to the **second IDE window**. Open Agent Mode (Claude Sonnet 4.5 recommended) and paste the following prompt:

```
I want to implement everything using the spec-driven approach from https://speckit.org

Please initialize the project for me and install everything required by SpecKit.

Next, I want to use the following technology stack.
See the file in /tools/architecture.md for the architecture description.
```

**What will happen:**

The AI will:
1. Read the SpecKit documentation
2. Install `uv` if needed and run `uv tool install specify-cli`
3. Run `specify init --here --force --ai copilot --script ps --no-git`
4. Create the initial project structure with `instructions/` and `.github/copilot-instructions.md`
5. Confirm the tech stack from your `tools/architecture.md`

**Verify initialization succeeded.** You should see:
- `instructions/` folder with at least `main.agent.md` and `spec-kit.agent.md`
- `.github/copilot-instructions.md` that references `main.agent.md`
- `specs/` folder (may be empty at this point)

---

### Step 5: Run `/speckit.constitution`

In the **second IDE window**, in Agent Mode, type:

```
/speckit.constitution
```

The AI will ask you questions about the project's principles, constraints, and goals. Answer them based on your application idea.

**Typical questions include:**
- What is the purpose of this application?
- Who are the users?
- What are the most important non-functional requirements (security, performance, simplicity)?
- Are there any hard constraints (specific auth method, deployment target, etc.)?

After answering, verify that a constitution file was created in your project.

---

### Step 6: Run `/speckit.specify`

Type in Agent Mode:

```
/speckit.specify [your one-sentence app idea here]
```

For example:
```
/speckit.specify A personal expense tracker where users log daily expenses by category and view a monthly summary dashboard
```

The AI will generate `specs/001-[feature-name]/spec.md`. Review the generated spec:
- Does it capture the right problem?
- Are the user stories accurate?
- Are the acceptance criteria complete?

Take a screenshot of the spec and share it with the training window if you want feedback.

---

### Step 7: Run `/speckit.clarify`

```
/speckit.clarify
```

Answer all the questions the AI raises. This typically takes 5–10 minutes of back-and-forth. Do not rush — good answers here prevent implementation mistakes later.

---

### Step 8: Run `/speckit.plan`

```
/speckit.plan React 18 + Vite frontend, Node.js Express backend, PostgreSQL 15, Docker Compose, JWT auth
```

The AI will read `tools/architecture.md` and generate:
- `specs/001-[feature-name]/plan.md`
- `specs/001-[feature-name]/data-model.md`
- `specs/001-[feature-name]/contracts/` (API contracts)

Review the data model carefully — this is the most expensive thing to change later.

---

### Step 9: Run `/speckit.tasks`

```
/speckit.tasks
```

The AI generates `specs/001-[feature-name]/tasks.md` — an ordered list of implementation tasks.

Review the task list:
- Are the tasks specific enough?
- Is the order logical (DB migrations before code that uses them)?
- Are there any obvious missing tasks?

If something is missing, ask the AI to add it before proceeding.

---

### Step 10: Run `/speckit.analyze`

```
/speckit.analyze
```

Review the analysis report. Address any gaps or contradictions the AI identifies before moving to implementation.

---

### Step 11: Run `/speckit.implement`

```
/speckit.implement
```

The AI will begin implementing tasks from `tasks.md` one by one. Let it work. Monitor progress by checking `tasks.md` as items get marked done.

For a small application, this phase typically takes 15–30 minutes with active monitoring.

---

### Step 12: Run `/speckit.checklist`

```
/speckit.checklist
```

Review the generated QA checklist. Manually verify items that cannot be automated.

Start the Docker containers and test your application:

```bash
docker compose up --build
```

Navigate to `http://localhost:3000` and walk through the acceptance criteria from the original `spec.md`.

---

## Success Criteria

✅ SpecKit CLI installed and initialized in the second workspace  
✅ `instructions/` and `.github/copilot-instructions.md` created by SpecKit  
✅ Constitution file created via `/speckit.constitution`  
✅ `spec.md` generated with correct user stories and acceptance criteria  
✅ Clarification questions answered and spec updated  
✅ `plan.md` and `data-model.md` generated with correct tech stack  
✅ `tasks.md` generated with ordered, specific tasks  
✅ Consistency check passed via `/speckit.analyze`  
✅ Implementation completed — all tasks checked off in `tasks.md`  
✅ Application running in Docker via `docker compose up`  
✅ QA checklist generated and reviewed via `/speckit.checklist`  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **Why does SpecKit separate the spec from the plan?**

   Expected answer: The spec captures WHAT and WHY (requirements, user stories, acceptance criteria) without technology assumptions. The plan captures HOW (technical decisions, components, data model). This separation means non-technical stakeholders can review and validate the spec, and tech decisions can change without invalidating requirements.

2. **What is the purpose of `/speckit.clarify` and when would you skip it?**

   Expected answer: It resolves ambiguities in the spec through AI-driven Q&A. You should never skip it — ambiguities caught in the spec phase cost minutes. The same ambiguity found during implementation can require significant rework. Even if you think the spec is clear, the AI often catches edge cases you haven't considered.

3. **Why does SpecKit insist on small, specific tasks in `tasks.md`?**

   Expected answer: Small tasks are independently implementable and testable. They prevent the AI from making large decisions autonomously. If a task fails, it doesn't break others. They also serve as progress indicators and a historical record of what was built and when.

4. **What problem does `/speckit.analyze` solve?**

   Expected answer: It performs a consistency check across all spec artifacts before coding starts. It catches gaps (acceptance criteria not covered in plan), contradictions (conflicting statements), and missing artifacts (undefined API contracts). This is a pre-flight check — finding issues at this stage is much cheaper than mid-implementation.

5. **Why do we use a separate workspace for the SpecKit practice?**

   Expected answer: SpecKit installs its own AI instruction files that take control of the agent's behavior. Running SpecKit in the training workspace would overwrite or conflict with the course's own instruction files. A separate workspace keeps both environments isolated so you can reference training materials while working in the SpecKit project.

6. **What is the role of `tools/architecture.md` in this workflow?**

   Expected answer: It is a technology blueprint that the AI references during `/speckit.plan`. It defines the full-stack architecture — layers, directory structure, patterns, Docker setup, and environment variables. By providing it upfront, you ensure the AI generates a plan consistent with your team's standards rather than inventing arbitrary technology choices.

7. **What does the `docker compose up --build` command do in the final step?**

   Expected answer: It builds Docker images from the Dockerfiles (including building the React frontend with Vite and embedding it into the backend image), creates all defined containers (backend, PostgreSQL), connects them via a Docker network, and starts the entire application stack. The `--build` flag forces image rebuild even if the image already exists, ensuring the latest code is running.

---

## Troubleshooting

### Problem: `uv` command not found after installation

**Symptoms:** Running `uv --version` shows "command not recognized"

**Solutions:**
1. Close and reopen the terminal — PATH changes require a new session
2. On Windows, restart the IDE entirely after installing `uv`
3. Check that `~/.cargo/bin` or `~/.local/bin` is in your PATH
4. Reinstall using the official script from https://astral.sh/uv

---

### Problem: `specify init` fails or produces no files

**Symptoms:** The init command runs but no `instructions/` folder appears

**Solutions:**
1. Ensure you are in the correct workspace folder before running init
2. Try with explicit flags: `specify init --here --force --ai copilot --script ps --no-git`
3. Check if spec-kit was installed correctly: `uv tool list`
4. Reinstall: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git --force`

---

### Problem: Slash commands are not recognized in Agent Mode

**Symptoms:** Typing `/speckit.specify` does nothing or returns "unknown command"

**Solutions:**
1. Ensure Agent Mode is active (not regular chat or inline completion)
2. Verify `.github/copilot-instructions.md` exists and points to `instructions/main.agent.md`
3. Check that `instructions/spec-kit.agent.md` exists with the slash command definitions
4. Reload the IDE window to force re-reading of instruction files
5. Try opening a new Agent Mode chat session after initialization

---

### Problem: AI skips SpecKit phases and starts coding immediately

**Symptoms:** After typing `/speckit.specify`, the AI generates code instead of a spec

**Solutions:**
1. The AI may not have read the SpecKit instruction file — remind it: "Read `instructions/spec-kit.agent.md` before proceeding"
2. Check that `copilot-instructions.md` correctly references the main instructions file
3. Start a fresh Agent Mode session after verifying instruction files are in place
4. Use Claude Sonnet 4.5 — it follows custom instructions more reliably

---

### Problem: `docker compose up --build` fails with port conflicts

**Symptoms:** Error "port is already allocated" when starting Docker Compose

**Solutions:**
1. Stop other running Docker containers: `docker compose down` in any other project folders
2. Check what is using the port:
   ```powershell
   # Windows
   netstat -ano | findstr :3000
   ```
   ```bash
   # macOS/Linux
   lsof -i :3000
   ```
3. Edit `docker-compose.yml` to use different host ports (e.g., `3001:3000`)

---

### Problem: PostgreSQL container fails to start

**Symptoms:** `docker compose up` starts but backend crashes with "connection refused"

**Solutions:**
1. Check container logs: `docker compose logs postgres`
2. Ensure the `DATABASE_URL` environment variable matches `docker-compose.yml` service name and credentials
3. Wait for postgres to finish initializing — add a `healthcheck` or `depends_on` with condition in `docker-compose.yml`
4. Delete the postgres volume and restart: `docker compose down -v` then `docker compose up --build`

---

## Next Steps

You have now completed the full SpecKit spec-driven workflow and have a running full-stack Node.js application in Docker. Here's what comes next:

1. **Add more features with SpecKit**

   For each new feature, start again from `/speckit.specify`. The `specs/` folder will grow with one subfolder per feature, building a comprehensive specification history for the project.

2. **Continue to Module 130: QA with Chrome DevTools MCP**

   Learn how to test web applications using AI assistance and Chrome DevTools MCP integration — a natural next step after building your prototype.

3. **Explore Module 150: GitHub Coding Agent Delegation**

   Delegate entire SpecKit features to the GitHub Coding Agent — combine spec-driven development with autonomous PR creation for even faster delivery.

---

## Additional Resources

- [SpecKit Official Site](https://speckit.org/)
- [spec-kit GitHub Repository](https://github.com/github/spec-kit)
- [uv Python Package Manager](https://astral.sh/uv)
- [React + Vite Documentation](https://vitejs.dev/guide/)
- [Express.js Documentation](https://expressjs.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
