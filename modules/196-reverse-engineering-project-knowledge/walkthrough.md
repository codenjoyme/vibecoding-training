# Reverse Engineering Project Knowledge from Text - Hands-on Walkthrough

In this walkthrough, you'll learn the text-triangle principle — a powerful mental model for extracting hidden knowledge from existing project artifacts. You'll practice by taking real issue-diff pairs and reverse-engineering project instructions that capture how the team actually works.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **Understanding of the text-triangle principle** — why any two related texts can generate the third
- **A reverse-engineered instruction file** — extracted from real issue + diff pairs in a clean experiment
- **A comparison** — between AI-extracted conventions and real ones, showing what the technique captures and what it misses
- **A repeatable workflow** — for extracting project knowledge commit by commit

---

## Part 1: Understand the text-triangle principle

**What we're about to learn:** The foundational idea behind text reverse engineering — and why it works.

### The core insight

When a developer works on a task, three texts are always involved:

```
    [1] Issue / Task Description
              |
              |  (developer applies project knowledge)
              v
    [2] Implementation (code diff)
              |
              |  (implicit)
              v
    [3] Project Knowledge (conventions, architecture, patterns)
```

Normally, a developer reads the **issue** [1], applies their **project knowledge** [3], and produces the **implementation** [2]:

> **1 + 3 → 2** (the normal workflow)

But here's the key insight: **if any two of these three texts exist, an AI model can reconstruct the third.**

| You have | You want | Direction | Use case |
|----------|----------|-----------|----------|
| Issue + Diff | Project Knowledge | **3 = f(1, 2)** | Reverse-engineer conventions from completed work |
| Issue + Project Knowledge | Implementation | **2 = f(1, 3)** | Generate code from spec (standard AI coding) |
| Diff + Project Knowledge | Issue / Requirement | **1 = f(2, 3)** | Reconstruct what was asked from what was done |

The first direction — **extracting project knowledge from issue + diff** — is the most powerful for onboarding and documentation. And it's the one almost nobody uses.

The second direction (issue + conventions → code) you already practiced in [Module 070 — Custom Instructions](../070-custom-instructions/about.md). This module focuses on the **first** direction — the reverse.

### Why this works

An AI model is fundamentally a text-to-text transformation engine. When you give it two related texts:

- The **issue** describes *what* was asked
- The **diff** shows *how* it was done
- The **gap between them** — the decisions, conventions, patterns that guided the implementation — is the project knowledge

The model can identify this gap because it sees the input (issue) and the output (diff) and can infer the transformation rules. Those rules *are* your project conventions.

### A simple analogy

Think of it like algebra:

$$a + b = c$$

If you know $a$ and $c$, you can find $b = c - a$.

The same principle applies to texts. If the **issue** is $a$, the **diff** is $c$, then the **project knowledge** is $b$ — the hidden ingredient that transforms one into the other.

---

## Part 2: Reverse-engineer conventions from issue + diff

**What we're about to do:** The core skill of this module. We'll give an AI model a completed task (issue + diff) and ask it to extract the project conventions that guided the implementation. Then we'll compare with the real conventions to see how accurate the extraction is.

The `tools/task1/` folder has three example files — one for each side of the triangle:

- [tools/task1/example-issue.md](tools/task1/example-issue.md) — a task description (the "issue")
- [tools/task1/example-diff.md](tools/task1/example-diff.md) — the implementation that was done (the "diff")
- [tools/task1/example-conventions.md](tools/task1/example-conventions.md) — the real project conventions (the "answer key" — we'll use it ONLY for comparison after the experiment)

### ⚠️ Clean experiment protocol

**IMPORTANT for trainers:** The training agent has likely already read all three files (or will be tempted to). To keep the experiment scientifically honest, the user must run the extraction in a **fresh chat session** where the model has NOT seen the "answer key" (`example-conventions.md`).

**Instructions for the user:**

1. **Open a new chat session** (Ctrl+L in VS Code / Cmd+L on Mac)
2. **Paste the prompt below** into the new session
3. **Wait for the result** — the model will create an extracted conventions file
4. **Return to this session** to compare with the real conventions

**Prompt to paste in the NEW session:**

```
Read these two files:
- ./modules/196-reverse-engineering-project-knowledge/tools/task1/example-issue.md
- ./modules/196-reverse-engineering-project-knowledge/tools/task1/example-diff.md

Based ONLY on these two files, reverse-engineer the project conventions
that guided this implementation.

Do NOT read or look at example-conventions.md — that's the answer key.

Look at the GAP between what was asked (issue) and how it was done (diff).
The decisions that fill that gap ARE the project knowledge.

Create a file ./work/196-task/extracted-conventions.md
with the extracted conventions:
1. Naming conventions (files, variables, functions, classes)
2. Architecture patterns (folder structure, layering, separation of concerns)
3. Code style rules (formatting, error handling, imports)
4. Technology choices and their usage patterns
5. Security and authorization patterns
6. Testing conventions

Format it as an instruction file that could guide a new developer on this project.
```

---

## Part 3: Compare extracted conventions with the real ones

**After the user returns from the new session:**

Open both files side by side:
- `work/196-task/extracted-conventions.md` — what the AI reverse-engineered
- `tools/task1/example-conventions.md` — the actual project conventions (ground truth)

Compare them section by section. Key questions to discuss:

1. **What did the AI get right?** — Which conventions were accurately extracted from just the issue + diff?
2. **What did the AI miss?** — Which conventions exist in the ground truth but couldn't be inferred from a single issue-diff pair?
3. **What did the AI invent?** — Did it hallucinate any conventions not actually present in the project?
4. **What did the AI discover that isn't in the ground truth?** — Sometimes the AI spots patterns that the team follows but never documented.

This comparison demonstrates both the power and the limitations of single-pair extraction — and motivates why processing multiple issue-diff pairs (Step 5) produces better results.

---

## Part 4: (Optional) Third direction — reconstruct the issue from diff + conventions

**What we're about to do:** Complete the triangle by trying the third direction — useful for understanding undocumented changes.

This direction is less common but valuable when you find commits without linked issues, or need to reconstruct lost context.

### ⚠️ Clean experiment — new session

This time the model should NOT have seen `example-issue.md` (the answer key).

**Instructions for the user:**

1. **Open a new chat session** (Ctrl+L / Cmd+L)
2. **Paste the prompt below** into the new session
3. **Wait for the result** — the model will create a reconstructed issue
4. **Return to this session** to compare

**Prompt to paste in the NEW session:**

```
Read these two files:
- ./modules/196-reverse-engineering-project-knowledge/tools/task1/example-diff.md
- ./modules/196-reverse-engineering-project-knowledge/tools/task1/example-conventions.md

Based ONLY on these two files, reconstruct the original task/issue
that likely led to this implementation.

Do NOT read or look at example-issue.md — that's the answer key.

Based on what was changed and how it follows the conventions, infer:
1. What was the user-facing problem or feature request?
2. What were the acceptance criteria?
3. What technical context would have been in the issue?

Create a file ./work/196-task/reconstructed-issue.md
with your reconstructed issue description.
```

**After the user returns:** Compare `work/196-task/reconstructed-issue.md` with the original `tools/task1/example-issue.md`. The match demonstrates that the triangle is complete — any two sides can reconstruct the third.

---

## Part 5: Scale it — extract knowledge from multiple commits

**What we're about to do:** Apply the technique to multiple issue-diff pairs to build cumulative project knowledge. Each pair reveals new conventions; together they form a comprehensive instruction file.

### The cumulative extraction prompt

Here's the prompt pattern for iterative extraction. Each run adds only new insights to the growing conventions document:

```
Here is a completed task (issue + diff) from our project.
Extract any project conventions, patterns, or rules visible in how
this task was implemented. Focus only on NEW insights — things not
already in the existing conventions document.

## Existing Conventions So Far
[paste accumulated conventions from previous iterations]

## Issue #N
[paste issue text]

## Diff for Issue #N
[paste diff]

Add any new conventions discovered to the existing document.
Mark new additions with "Source: Issue #N" so we can trace where
each convention was discovered.
```

This prompt is a good template for understanding the logic — but manually pasting issue text and diffs doesn't scale. In practice, you need to:

1. **Get the issue text programmatically** — if your project uses GitHub Issues, you can fetch them via GitHub MCP integration ([Module 105](../105-mcp-github-integration-issues/about.md)) or GitHub CLI (`gh issue view <number>`)
2. **Get the commit diff** — use `git log --oneline` to find the commit hash, then `git show <hash>` to see the diff. For squash-merged PRs, the diff is clean and self-contained.

For a single pair, you can do this manually. But for 5-10 pairs, you need automation — which is exactly what we'll build in the next steps.

---

## Part 6: Create a reverse-engineering instruction file

**What we're about to do:** Turn the extraction prompt into a proper instruction file that an AI agent can follow autonomously. This is the key step — an instruction file is reusable, composable, and can be fed to automation scripts.

Following the [instruction creation guidelines](../../instructions/creating-instructions.agent.md), create an instruction file that:

1. Takes an issue text and a commit diff as input
2. Optionally accepts an existing conventions document to accumulate into
3. Extracts project conventions from the gap between issue and diff
4. Outputs a structured conventions document with source tracing

A reference example of such an instruction file is provided in [tools/task2/reverse-engineer-conventions.agent.md](tools/task2/reverse-engineer-conventions.agent.md).

**Your task:** Create your own version of this instruction file at `./instructions/reverse-engineer-conventions.agent.md` using this prompt in a new chat session (Ctrl+L):

```
Read the instruction creation guidelines:
- ./instructions/creating-instructions.agent.md

Then create a new instruction file ./instructions/reverse-engineer-conventions.agent.md
that describes the following workflow:

Given an issue description and a commit diff, extract project conventions
that guided the implementation. The instruction should:

- Accept two inputs: issue text and commit diff
- Optionally accept existing conventions to accumulate into
- Look at the gap between what was asked (issue) and how it was done (diff)
- Extract: naming conventions, architecture patterns, code style rules,
  technology choices, security patterns, testing conventions
- Mark each discovered convention with its source (e.g., "Source: Issue #47")
- Output a structured instruction file format
- When accumulating, only add NEW insights not already present

Also add the new instruction to ./instructions/main.agent.md catalog
with keywords: reverse engineer, conventions, extract, project knowledge, onboarding
```

**After you create this file, return here.** We'll use it in the next step to process multiple issue-diff pairs automatically.

---

## Part 7: Run bulk extraction on your own project

**What we're about to do:** Apply the instruction from Step 6 to multiple issue-diff pairs from a real project. This uses the same approach as [Module 160 — Bulk File Processing](../160-bulk-file-processing-with-ai/about.md) — running the same instruction repeatedly over different inputs.

### Pick a repository and gather issue-diff pairs

1. **Pick a repository** you have access to

1. **Find 5-10 completed issues** with associated commits. If using GitHub MCP ([Module 105](../105-mcp-github-integration-issues/about.md)):
   ```
   List the last 10 closed issues in [owner/repo] that have associated commits
   ```

1. **Get the diffs** for each issue's commits:
   ```
   git log --oneline --all | Select-Object -First 20
   git show <commit-hash>
   ```

### Run the extraction iteratively

You can do this manually (opening new chats per commit) or use the automation script in [tools/task3/extract_conventions.py](tools/task3/extract_conventions.py) which calls GitHub Copilot CLI deterministically for each commit — the same approach as [Module 160](../160-bulk-file-processing-with-ai/about.md).

**Manual approach** — for each issue-diff pair, open a new chat session and run:

```
Follow the instruction ./instructions/reverse-engineer-conventions.agent.md

## Issue #N
[issue text or: fetch issue #N from owner/repo using GitHub MCP]

## Diff
[paste diff or: run git show <hash>]

## Existing Conventions
[paste accumulated result from previous iterations, or "None yet" for the first run]

Save the result to ./work/196-task/accumulated-conventions.md
```

After processing all pairs, ask the AI to deduplicate and organize the accumulated conventions into a clean instruction file.

### Validate the result

1. Review `work/196-task/accumulated-conventions.md` — does it feel like a real project guide?
1. Check source tracing — can you see which issue contributed which convention?
1. Ask a teammate: "Does this match how we actually work?"

**What just happened:** You built a project instruction file entirely from behavioral evidence — not from anyone's memory or opinions, but from what the team actually does. And you did it using a reusable instruction that can be run on any project.

---

## Part 8: Manifest-driven workflow — tracking what you've processed

**What we're about to learn:** When you're analyzing a real project with hundreds of commits, you need a way to track which commits have been processed, which are queued, and which should be skipped. The manifest pattern solves this.

### The problem with bulk processing

In Part 7, the simple script just iterates through all commits. But in practice you need:

- **Resume capability** — stop and continue later without re-processing
- **Selective processing** — skip merge commits, docs-only changes, CI config
- **Progress visibility** — see at a glance how much of the history is covered
- **Team coordination** — multiple people can review and select commits to analyze

### The manifest file

The advanced tool in [tools/task4/analyze-commit-history](tools/task4/analyze-commit-history/SKILL.md) introduces a **commit manifest** — a markdown file with checkboxes for every commit in the repo:

```markdown
# Commit Manifest

- [x] a1b2c3d4 — PROJ-101: Add user entity and repository
- [x] e5f6g7h8 — PROJ-102: Add user service and controller
- [ ] i9j0k1l2 — PROJ-103: Add pagination to user list
- [>] m3n4o5p6 — PROJ-104: Add user profile endpoint
- [-] q7r8s9t0 — Merge branch 'develop' into feature/users
```

**Checkbox legend:**
| Marker | Meaning |
|--------|---------|
| `[x]` | Already processed — instructions extracted |
| `[ ]` | Available — not yet selected |
| `[>]` | Selected — queued for next processing run |
| `[-]` | Skipped — not relevant (merge commits, CI, docs-only) |

### Try it yourself

1. Open the skill documentation: [tools/task4/analyze-commit-history/SKILL.md](tools/task4/analyze-commit-history/SKILL.md)
2. Read the "Option A — Manifest-Driven Workflow" section
3. In a real project, you would run:
   ```
   python scripts/analyze-commits.py --generate-manifest
   ```
   This scans `git log --reverse` and creates the manifest with `[ ]` for every commit.
4. You then manually review the manifest, mark commits as `[>]` (to process) or `[-]` (to skip), and run:
   ```
   python scripts/analyze-commits.py --from-manifest
   ```
5. After each commit is processed, its marker changes from `[>]` to `[x]` automatically.

**Key insight:** The manifest is a human-in-the-loop control mechanism. The AI processes commits, but YOU decide which ones are worth analyzing. This prevents wasting credits on merge commits, typo fixes, or config changes.

### Branch classification

For projects with multiple branches (e.g., a feature branch for the analysis + a production `develop` branch), the tool offers `--classify-branch develop` which automatically marks non-production commits as `[-]`:

```
python scripts/analyze-commits.py --classify-branch develop
```

This is especially useful when you're working on a separate branch and want to analyze only production code changes.

---

## Part 9: Research phase — let AI classify what's worth analyzing

**What we're about to learn:** Before processing commits one by one, you can ask the AI to classify entire groups of commits by their ticket prefixes — automatically filtering signal from noise.

### The research phase

Most enterprise projects use ticket IDs in commit messages: `PROJ-101`, `ACT-45`, `FEAT-12`. The advanced tool's **research phase** exploits this:

1. **Scan** all commit messages for patterns like `[A-Z]+-\d+`
2. **Count** how many commits each prefix has → `analysis/commit-stats.txt`
3. **Classify** each prefix using an AI model call — is `PROJ` a feature prefix? Is `CI` an infrastructure prefix?
4. **Filter** — only commits with "relevant" prefixes proceed to analysis

```
$ python scripts/analyze-commits.py

🔍 Research phase — scanning commit prefixes...
   PROJ: 47 commits — classified as: feature development ✅
   ACT:  12 commits — classified as: infrastructure/CI ❌
   DOC:   8 commits — classified as: documentation ❌
   FEAT: 23 commits — classified as: feature development ✅

→ Processing 70 commits from prefixes: PROJ, FEAT
```

### When to skip research

- `--skip-research` — process all ticket-like commits without classification
- `--prefix PROJ --prefix FEAT` — manually specify which prefixes to include
- `--all-commits` — process everything, even commits without ticket IDs
- `--from-manifest` — manifest mode doesn't need research (you selected commits manually)

### The classification instruction

The AI classification is powered by [tools/task4/analyze-commit-history/references/discover-prefixes.instruction.md](tools/task4/analyze-commit-history/references/discover-prefixes.instruction.md). It tells the model to look at commit statistics and decide which prefixes represent actual feature work vs. infrastructure/meta changes.

**Why this matters for cost control:** If your project has 500 commits but only 200 are feature work, the research phase saves you from spending AI credits on 300 irrelevant diffs.

---

## Part 10: From conventions to SDLC instructions

**What we're about to learn:** The leap from extracting passive conventions ("we use camelCase") to generating actionable SDLC workflow instructions ("how to add a new REST endpoint, step by step").

### Conventions vs. instructions — what's the difference?

| Aspect | Conventions (Parts 2-7) | SDLC Instructions (Part 10) |
|--------|------------------------|----------------------------|
| **Format** | Descriptive rules | Step-by-step workflows |
| **Example** | "Services use `*Service.ts` suffix" | "1. Create entity → 2. Create DTO → 3. Create mapper → 4. Add service → 5. Add controller → 6. Add migration → 7. Write tests" |
| **Audience** | Human developers (onboarding docs) | AI agents (autonomous execution) |
| **Reuse** | Reference while coding | Feed to an agent that generates code |
| **File format** | `conventions.md` | `add-endpoint.agent.md`, `create-migration.agent.md` |

### How the advanced tool generates instructions

The [analyze-commit-diff.instruction.md](tools/task4/analyze-commit-history/references/analyze-commit-diff.instruction.md) tells the model to:

1. Read the diff for a commit
2. Identify which **layers** are affected (entity, DTO, mapper, service, controller, migration, test)
3. Determine the **sequence** of changes across files
4. Look for **repeating patterns** across commits
5. Write (or update) `.agent.md` instruction files in `./instructions/`

Each instruction file covers **one workflow** (Single Responsibility Principle):
- `add-endpoint.agent.md` — steps for adding a new REST endpoint
- `create-migration.agent.md` — steps for creating a database migration
- `add-entity-field.agent.md` — steps for adding a field to an existing entity

### The key difference from Part 7

In Part 7, you ran a simple script that accumulated everything into one `accumulated-conventions.md`. The advanced tool:

- Writes **multiple instruction files** (one per workflow pattern)
- **Updates existing files** when new commits reveal the same pattern
- **Auto-commits** each instruction alongside the analysis (`git commit -m "analyze(instructions): <sha>"`)
- Includes a **review phase** (`--review`) where AI checks if generated instructions are still relevant

### Try it conceptually

You don't need to run the full pipeline right now. Instead, take the conventions you extracted in Part 7 and transform them manually:

1. Open your `work/196-task/accumulated-conventions.md`
2. Group the conventions by **workflow** — which ones relate to "adding an endpoint"? Which to "writing tests"?
3. For each group, write a step-by-step instruction:
   ```markdown
   # Add a New REST Endpoint

   1. Create the entity class in `domain/entities/`
   2. Create a DTO in `domain/dtos/` — mirror entity fields, add validation annotations
   3. Create a mapper in `domain/mappers/` using MapStruct
   4. Add service methods in `domain/services/`
   5. Add controller in `api/controllers/` — follow RESTful naming
   6. Add Flyway migration in `db/migrations/`
   7. Write unit tests co-located with source files
   8. Write integration test in `tests/integration/`
   ```
4. This is exactly what the advanced tool automates.

### Deploying the skill to your project

When you're ready to use the full advanced tool on your own project, follow the deployment process from [Module 104 — Port to Skills](../104-port-to-skills/about.md):

1. Copy [tools/task4/analyze-commit-history/](tools/task4/analyze-commit-history/) to your project's skill/instruction directory
2. Adjust paths in `SKILL.md` and `scripts/analyze-commits.py` to match your project structure
3. Run `--generate-manifest` to create your commit manifest
4. Start processing commits in batches: `--from-manifest --batch 10`

---

## Success Criteria

After completing this walkthrough, verify:

- ✅ You understand the text-triangle principle and why issue+diff→conventions is the most useful direction
- ✅ You extracted project conventions from an issue + diff pair in a clean experiment
- ✅ You compared extracted conventions with real ones and understand what the technique captures vs. misses
- ✅ You created a reusable instruction file for convention extraction
- ✅ You understand how to scale the technique across multiple commits using bulk processing
- ✅ You produced an instruction file from reverse-engineered knowledge
- ✅ You understand the manifest-driven workflow for tracking progress across large commit histories
- ✅ You understand how the research phase classifies commits by prefix to save AI credits
- ✅ You can explain the difference between extracted conventions and actionable SDLC instructions

---

## Understanding Check

1. **Why does the text-triangle principle work?** What is the AI actually doing when it "reverse-engineers" conventions from an issue + diff pair?
   > It identifies the transformation rules between input (issue) and output (diff). Those rules represent the implicit project knowledge — naming, architecture, patterns — that guided the implementation.

2. **Which direction is most useful for onboarding, and why?**
   > Issue + Diff → Conventions (direction 3 = f(1,2)). It extracts how the team actually works, not how they think they work, producing grounded documentation.

3. **Why is processing multiple issue-diff pairs better than a single pair?**
   > Each pair reveals different conventions. One might show naming rules, another shows error handling patterns. Together they build comprehensive knowledge. Individual pairs may also contain one-off decisions that multiple pairs help filter out.

4. **How would you validate the extracted conventions?**
   > Compare them with what the team actually does. Ask a teammate to review. Cross-check against recent PRs. The conventions should predict how new issues will be implemented.

5. **What's the practical difference between this approach and just reading the code?**
   > Reading code shows *what* exists. Issue + diff shows *why* it was built that way and *what changed*. The delta (diff) against the context (issue) reveals decisions, not just state.

6. **When would the third direction (diff + conventions → issue) be useful?**
   > When you find undocumented commits, need to understand why a change was made, or want to reconstruct lost issue descriptions for audit or knowledge management.

7. **Can this technique produce wrong conventions?**
   > Yes. A single issue-diff pair might reflect a one-time exception, not a rule. That's why you process multiple pairs and look for patterns that repeat. Validation with the team is essential.

8. **Why use a commit manifest instead of just processing all commits?**
   > Not all commits are worth analyzing — merge commits, CI config changes, typo fixes add noise and waste AI credits. The manifest gives you human-in-the-loop control: you see the full history and decide what's worth the investment.

9. **How does the research phase save costs?**
   > It classifies commit prefixes (PROJ, CI, DOC) in one cheap AI call, then filters out entire groups of irrelevant commits. This can cut processing by 50-70% on a typical project.

10. **What makes SDLC instructions more valuable than conventions for AI agents?**
    > Conventions describe rules ("use camelCase"), but instructions describe workflows ("create entity → DTO → mapper → service → controller → test"). An AI agent can follow instructions to generate complete implementations autonomously, while conventions only inform individual decisions.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| AI generates generic conventions, not project-specific | Include more of the diff — the AI needs to see actual file names, patterns, and structure to extract specific rules |
| Extracted conventions contradict each other across commits | This is valuable signal — it may indicate inconsistency in the team or an evolving convention. Note both and ask the team which is current |
| Diff is too large for the context window | Split into logical chunks (e.g., by file or feature area). Process each chunk separately and merge the results |
| Can't find issues with clean commits | Look for squash-merged PRs — they often have one clean diff per issue. Or use `git log --grep="ISSUE-123"` to find related commits |
| Model hallucinates conventions not in the diff | Be explicit in the prompt: "Only extract conventions that are directly evidenced in the diff. Quote the specific lines that support each convention." |
| Manifest has hundreds of `[ ]` entries | Use `--classify-branch` to auto-skip non-production commits, then process in batches with `--batch 10` |
| Research phase classifies a relevant prefix as noise | Override with `--prefix PROJ --prefix FEAT` to manually specify which prefixes to include |
| Generated SDLC instructions are too generic | Include more diffs from the same workflow pattern — the model needs multiple examples of the same type of change to extract specific steps |
| `copilot.bat` not found | Ensure GitHub Copilot CLI is installed. Run `where.exe copilot` to verify. The script auto-detects the path from VS Code extensions |

---

## Next Steps

With reverse-engineered project knowledge in hand, you're ready for:

- [197 — Onboarding New Team Members with AI](../197-onboarding-new-team-members-with-ai/about.md) — use your extracted instructions to power an AI onboarding system
