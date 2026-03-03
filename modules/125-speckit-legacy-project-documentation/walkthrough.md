---
external_workspace: true
---

# SpecKit for Legacy Projects — Hands-on Walkthrough

In this module, you will take an **existing project** — one that was not built with SpecKit — and reverse-engineer a complete set of spec-driven documentation for it. By the end, the project will be fully "on SpecKit rails": it will have a constitution, specs, plans, data models, and a task list structure ready for future feature development.

This module runs in a **separate workspace** (`work/125-task/`) because SpecKit installs its own AI instruction files that would conflict with the course instructions.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Learn and Build

| Phase | Action |
|-------|--------|
| 1. Prepare | Set up a separate workspace with an existing project |
| 2. Initialize | Install SpecKit into the legacy project |
| 3. Constitution | Generate project principles from existing code patterns |
| 4. Reverse-Specify | Generate specs from what the code already does |
| 5. Reverse-Plan | Generate plan and data model from existing implementation |
| 6. Catalog Tasks | Document the current state as completed tasks |
| 7. New Feature | Add a brand-new feature using standard SpecKit workflow |

**The big idea:** SpecKit is not just for greenfield projects. You can "wrap" any existing codebase in spec-driven documentation and then manage it going forward as if it was built with SpecKit from day one.

---

## Part 1: Why Reverse-Document a Legacy Project?

### The Problem

Most real-world projects have:
- Little to no design documentation
- No written specs explaining WHY things were built the way they are
- Tribal knowledge locked in the heads of original developers
- No structured onboarding path for new team members

When a new developer (or an AI agent) joins the project, they must read code line-by-line to understand what is going on. This is slow, error-prone, and frustrating.

### The SpecKit Solution

SpecKit's artifacts (constitution, specs, plans, data models) are just Markdown files. They don't need to be generated before code — they can be generated **after** the code already exists. The AI can:

1. **Read** the entire codebase
2. **Analyze** its structure, patterns, and data models
3. **Generate** spec artifacts that describe the current state
4. **Produce** documentation as if the project had been spec-driven from the start

Once these artifacts exist, every future feature follows the standard SpecKit workflow. The project is now "on rails."

### What You Get

After this process, the project will have:

```
specs/
  constitution.md        ← Project principles, constraints, patterns
  000-existing-system/
    spec.md              ← What the system does today
    plan.md              ← How it is implemented
    data-model.md        ← Current database schema
    tasks.md             ← Completed tasks (historical record)
  001-new-feature/
    spec.md              ← First new feature, added the SpecKit way
    plan.md
    tasks.md
```

---

## Part 2: Choose Your Legacy Project

### Option A: Use Your Own Project

If you have an existing project you want to document, use it. Ideal candidates:
- A Node.js, Python, or Java application with at least 5-10 source files
- Has a database (SQL or NoSQL)
- Has some API endpoints or user-facing routes
- Has little or no documentation

### Option B: Use the Module 120 Output

If you completed Module 120 and built an application with SpecKit, you can use it for this exercise. Delete the `specs/` folder to simulate a "legacy" project:

```bash
# In your 120-task folder
rm -rf specs/
rm -rf instructions/
rm -f .github/copilot-instructions.md
```

Now the project looks like a legacy codebase with no spec artifacts.

### Option C: Clone a Small Open-Source Project

If you do not have a project available, clone a small open-source application:

```bash
# Example: a simple Express.js TODO app
git clone https://github.com/expressjs/express.git work/125-task
cd work/125-task
git checkout 4.x  # use a stable branch
```

Or any small project you find interesting — the key is that it has real code and no SpecKit artifacts.

---

## Part 3: Prepare the Workspace

### Step 1: Create the Practice Folder

From the course root directory:

```bash
mkdir -p work/125-task
```

### Step 2: Copy or Clone Your Project

Place your chosen project files into `work/125-task/`. If using your own project, copy the source code there. If cloning, clone directly into that folder.

### Step 3: Open a Second IDE Window

- In VSCode: Menu → **File → New Window**
- In Cursor: Menu → **File → New Window**

Open `work/125-task/` as the workspace in the second window.

### Step 4: Verify the Project Runs

Before starting the SpecKit process, make sure the project actually works:

```bash
# For Node.js projects
npm install
npm start

# For Python projects
pip install -r requirements.txt
python main.py

# For Docker-based projects
docker compose up --build
```

If the project does not run, fix it first. SpecKit documents what exists — it needs working code to analyze.

---

## Part 4: Initialize SpecKit in the Legacy Project

### What We'll Do

We will install SpecKit into the existing project. This adds SpecKit's AI instruction files without touching the existing source code.

### Step 5: Initialize SpecKit

In the **second IDE window**, open Agent Mode (Claude Sonnet 4.5 recommended) and type:

```
I want to adopt spec-driven development from https://speckit.org for this EXISTING project.

This is a legacy codebase — it was NOT built with SpecKit. I want to reverse-document it.

Please initialize SpecKit here. Do NOT modify any existing source code. Only add SpecKit's own files (instructions, specs folder).

Run: specify init --here --force --ai copilot --script ps --no-git
```

**What will happen:**

The AI will:
1. Install SpecKit CLI via `uv tool install specify-cli` (if not already installed)
2. Run `specify init` to add SpecKit instruction files
3. Create `instructions/` folder and `.github/copilot-instructions.md`
4. Create empty `specs/` folder

**Verify:** You should see:
- `instructions/` folder with `main.agent.md` and `spec-kit.agent.md`
- `.github/copilot-instructions.md`
- `specs/` folder (empty for now)
- All original source code **untouched**

---

## Part 5: Generate the Constitution from Existing Code

### What We'll Do

Normally, `/speckit.constitution` asks you to define principles from scratch. For a legacy project, we want the AI to **discover** the principles by reading the existing code.

### Step 6: Generate the Constitution

In Agent Mode, type:

```
/speckit.constitution

This is an existing project. Please READ the entire codebase first — look at the directory structure, source files, configuration files, package.json / requirements.txt, Dockerfiles, database migrations, and any existing README or docs.

Based on what you find, generate the constitution that reflects the ACTUAL patterns and decisions in this codebase. Do not invent new principles — document what is already there.
```

**What the AI will produce:** A constitution file documenting:
- The project's purpose and domain
- Technology stack (as discovered from code)
- Coding conventions (as observed from existing files)
- Architecture patterns (as found in the structure)
- Constraints and dependencies

**Review the constitution carefully.** The AI may miss or misinterpret some patterns. Correct anything that does not match reality. This document will guide all future SpecKit work on this project.

---

## Part 6: Reverse-Specify the Existing System

### What We'll Do

Now we create a spec that describes **what the system currently does**. Think of it as writing a requirements document for code that already exists.

### Step 7: Generate the Reverse Spec

In Agent Mode, type:

```
/speckit.specify Reverse-document the existing system

READ all source code files in this project. Generate a spec.md that describes:
- What this application does (problem statement, from the code's behavior)
- User stories (what can a user currently do with this system)
- Acceptance criteria (what currently works — treat working features as met criteria)
- Out of scope (what the system explicitly does NOT do)

Put this in specs/000-existing-system/spec.md

This is a REVERSE spec — we are documenting what already exists, not proposing something new.
```

**What the AI will produce:** A `specs/000-existing-system/spec.md` that reads like a proper feature spec but is derived entirely from existing code.

**Review:** Does the spec accurately describe what the app does? Are any features missing? Did the AI misinterpret any functionality?

### Step 8: Clarify the Reverse Spec

Run the clarify phase to catch anything the AI missed:

```
/speckit.clarify

Remember: this is a reverse-documentation of an existing system. The answers to your questions are in the code. Read the code to resolve ambiguities rather than asking me.
```

The AI will identify gaps in the spec and try to resolve them by reading more code. You may need to answer some questions that cannot be determined from code alone (business intent, future plans, etc.).

---

## Part 7: Reverse-Plan and Data Model

### What We'll Do

Generate the technical plan and data model based on the **actual implementation**, not hypothetical design decisions.

### Step 9: Generate the Reverse Plan

```
/speckit.plan

This is a reverse-plan. READ the existing source code and generate:
- plan.md — describing HOW the system is currently implemented (not how it should be)
- data-model.md — documenting the ACTUAL database schema (from migrations, ORM models, or SQL files)

If there are API endpoints, create contracts/ with the actual request/response shapes.

Document what IS, not what should be.
```

**What the AI will produce:**
- `specs/000-existing-system/plan.md` — actual architecture documentation
- `specs/000-existing-system/data-model.md` — actual database schema
- `specs/000-existing-system/contracts/` — actual API contracts (if applicable)

**This is the most valuable artifact.** A new developer joining the project can read these files and understand the architecture in minutes instead of hours.

### Step 10: Generate the Historical Task List

```
/speckit.tasks

Generate a tasks.md for the existing system. All tasks should be marked as DONE (checked off) since they represent work that has already been completed.

Group tasks by logical phases (infrastructure, backend, frontend, etc.) based on what the code shows.
```

This creates a historical record — a "what was built" checklist. It is useful for:
- Understanding the scope of the existing system
- Identifying which areas have the most complexity
- Providing a template for future task lists

---

## Part 8: Validate the Documentation

### Step 11: Run the Consistency Check

```
/speckit.analyze

Analyze the reverse-documented spec artifacts for the existing system (specs/000-existing-system/). Check:
- Does spec.md accurately reflect what the code does?
- Does plan.md match the actual architecture?
- Does data-model.md match the actual schema?
- Are there features in the code not covered in the spec?
- Are there spec items not found in the code?
```

This step often reveals:
- Dead code (features in code that are not documented because they are unused)
- Orphaned routes or endpoints
- Schema columns that are never read or written
- Incomplete features that were started but never finished

**Document any findings** — they are valuable for understanding the true state of the project.

---

## Part 9: The Payoff — Add a New Feature on SpecKit Rails

### What We'll Do

Now that the legacy project is fully documented, adding a new feature follows the standard SpecKit workflow. The AI already knows the entire project context from the reverse-documentation phase.

### Step 12: Specify a New Feature

Think of a small feature to add to the project. In Agent Mode:

```
/speckit.specify [your new feature description]
```

For example:
```
/speckit.specify Add a search endpoint that allows filtering items by name and date range
```

**Notice the difference:** The AI now has full context — constitution, existing spec, plan, and data model. It will generate a spec that fits naturally into the existing architecture.

### Step 13: Complete the SpecKit Workflow

Run through the remaining phases for the new feature:

```
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
/speckit.checklist
```

The AI will:
- Write the spec consistent with the existing system
- Plan the feature using patterns already present in the codebase
- Generate tasks that reference existing files and patterns
- Implement code that matches the existing coding style

**This is the payoff.** A project that had zero documentation now has structured specs AND can receive new features through a disciplined, repeatable workflow.

---

## Part 10: What Just Happened

Let us review what you accomplished:

```
Legacy project (no docs)
        ↓
  SpecKit init (add instruction files)
        ↓
  /constitution (discover principles from code)
        ↓
  /specify (reverse-document features)
        ↓
  /clarify (verify completeness against code)
        ↓
  /plan + data-model (document actual architecture)
        ↓
  /tasks (mark existing work as done)
        ↓
  /analyze (consistency check)
        ↓
  PROJECT IS NOW ON SPECKIT RAILS
        ↓
  /specify new feature → normal SpecKit workflow
```

The project went from "code with no docs" to "spec-driven project with full documentation." Any future development follows the standard SpecKit process. New team members can read the `specs/` folder and understand the project in minutes.

---

## Success Criteria

✅ SpecKit initialized in the legacy project without modifying existing source code  
✅ Constitution generated from actual code patterns and conventions  
✅ `specs/000-existing-system/spec.md` accurately describes current functionality  
✅ Clarification phase completed — spec reviewed against actual code  
✅ `plan.md` documents actual architecture and component structure  
✅ `data-model.md` reflects the real database schema  
✅ `tasks.md` created with all existing work marked as completed  
✅ `/speckit.analyze` consistency check passed with findings documented  
✅ New feature added using standard SpecKit workflow  
✅ New feature implementation matches existing code patterns and style  

---

## Understanding Check

1. **Why is reverse-documentation valuable even if you wrote the code yourself?**

   Expected answer: Memory fades quickly. What seems obvious today will be unclear in 3 months. Structured specs serve as persistent documentation that both humans and AI agents can reference. They also make it possible to delegate future work — another person or an AI agent can understand the project from the specs without having to reverse-engineer the code again.

2. **What is the difference between running `/speckit.constitution` on a new project vs. a legacy project?**

   Expected answer: On a new project, you define principles from scratch — you tell the AI what you want. On a legacy project, you ask the AI to discover principles from what already exists in the code. The constitution should reflect reality (actual patterns, conventions, tech stack), not aspirations. If the code uses callbacks but you prefer promises, the constitution should document callbacks as the current standard, and a future spec can propose migration.

3. **Why do we use `specs/000-existing-system/` instead of `specs/001-...`?**

   Expected answer: The `000` prefix signals that this is the baseline — documentation of what existed before SpecKit was adopted. All future features start from `001` and above. This makes it clear in the `specs/` folder which artifacts describe the original system and which describe new additions.

4. **What might `/speckit.analyze` reveal about a legacy project that surprises you?**

   Expected answer: Dead features (code that exists but is never called), incomplete implementations (half-finished features), inconsistencies between the database schema and the code (columns that are never read or written), orphaned API endpoints, and security gaps (routes without authentication). The analyze step effectively performs a code audit through the lens of spec consistency.

5. **How does having reverse-documentation change the way AI implements new features?**

   Expected answer: Without documentation, the AI must guess at patterns, conventions, and architecture decisions — often producing code that clashes with the existing style. With reverse-documentation, the AI has explicit context: it knows the tech stack, coding conventions, data model, and existing patterns. New code will match existing code in style, naming, error handling, and architecture, because the AI is working from specs rather than guessing.

6. **Can you apply this reverse-documentation technique to a project in any language?**

   Expected answer: Yes. SpecKit artifacts are language-agnostic Markdown files. The AI can read and understand code in any language — Python, Java, TypeScript, Go, Rust, etc. The constitution, specs, plans, and data models describe behavior and architecture, not language-specific implementation details. The same technique works for monolith applications, microservices, CLI tools, or libraries.

7. **What should you do if the AI's reverse-spec misses an important feature?**

   Expected answer: Correct the spec manually or guide the AI to the specific code files it missed. The `/speckit.clarify` phase is designed exactly for this — you can point the AI to code it overlooked and ask it to update the spec. You can also add features to the spec yourself and then run `/speckit.analyze` to verify consistency. The specs are collaborative documents, not AI-only output.

---

## Troubleshooting

### Problem: AI generates a generic spec instead of reading the actual code

**Symptoms:** The spec contains generic placeholder content that does not match your project

**Solutions:**
1. Be explicit: "READ the source code files. Do not generate a generic spec."
2. Point the AI to specific directories: "Look at `src/routes/`, `src/models/`, and `src/services/` to understand what the system does."
3. Start a fresh Agent Mode chat — the AI may have context pollution from a previous conversation
4. Verify that SpecKit instruction files are loaded by checking `.github/copilot-instructions.md`

---

### Problem: Reverse data model does not match actual database

**Symptoms:** `data-model.md` describes tables or columns that do not exist, or misses existing ones

**Solutions:**
1. Point the AI to the actual source of truth: migration files, ORM models, or SQL dumps
2. Connect to the running database and export the schema: `pg_dump --schema-only` for PostgreSQL
3. Paste the actual schema into the chat and ask the AI to correct `data-model.md`
4. Run `/speckit.analyze` after corrections to verify consistency

---

### Problem: The constitution describes aspirational patterns, not actual ones

**Symptoms:** Constitution says "the project uses TypeScript strict mode" but the code is plain JavaScript

**Solutions:**
1. Explicitly instruct: "Document what IS, not what SHOULD BE. Describe the patterns you observe in the code."
2. Review the constitution line by line and correct any aspirational statements
3. If you want to adopt new patterns in the future, add them as a separate "Future Directions" section rather than mixing them with current conventions

---

### Problem: Too many findings in `/speckit.analyze`

**Symptoms:** The consistency check produces a very long list of gaps and contradictions

**Solutions:**
1. This is normal for legacy projects — it means the analysis is working
2. Prioritize: fix critical gaps first (missing features in spec, wrong data model)
3. Document non-critical issues as "known debt" — they can be addressed in future specs
4. Do not try to fix everything at once — the goal is to get baseline documentation, not perfection

---

## Next Steps

1. **Share the documentation with your team**

   The `specs/` folder is designed to be committed to version control. Other team members (and AI agents) can read it to understand the project without asking you questions.

2. **Continue adding features with SpecKit workflow**

   Every new feature from this point forward should go through `/speckit.specify` → `/speckit.implement`. The project is now on rails.

3. **Continue to Module 130: QA with Chrome DevTools MCP**

   Test your application (original and newly added features) with AI-assisted QA using Chrome DevTools MCP integration.

---

## Additional Resources

- [SpecKit Official Site](https://speckit.org/)
- [spec-kit GitHub Repository](https://github.com/github/spec-kit)
- [uv Python Package Manager](https://astral.sh/uv)
