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

## Step 1: Understand the text-triangle principle

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

## Step 2: Reverse-engineer conventions from issue + diff

**What we're about to do:** The core skill of this module. We'll give an AI model a completed task (issue + diff) and ask it to extract the project conventions that guided the implementation. Then we'll compare with the real conventions to see how accurate the extraction is.

The `tools/` folder has three example files — one for each side of the triangle:

- [tools/example-issue.md](tools/example-issue.md) — a task description (the "issue")
- [tools/example-diff.md](tools/example-diff.md) — the implementation that was done (the "diff")
- [tools/example-conventions.md](tools/example-conventions.md) — the real project conventions (the "answer key" — we'll use it ONLY for comparison after the experiment)

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
- ./modules/196-reverse-engineering-project-knowledge/tools/example-issue.md
- ./modules/196-reverse-engineering-project-knowledge/tools/example-diff.md

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

## Step 3: Compare extracted conventions with the real ones

**After the user returns from the new session:**

Open both files side by side:
- `work/196-task/extracted-conventions.md` — what the AI reverse-engineered
- `tools/example-conventions.md` — the actual project conventions (ground truth)

Compare them section by section. Key questions to discuss:

1. **What did the AI get right?** — Which conventions were accurately extracted from just the issue + diff?
2. **What did the AI miss?** — Which conventions exist in the ground truth but couldn't be inferred from a single issue-diff pair?
3. **What did the AI invent?** — Did it hallucinate any conventions not actually present in the project?
4. **What did the AI discover that isn't in the ground truth?** — Sometimes the AI spots patterns that the team follows but never documented.

This comparison demonstrates both the power and the limitations of single-pair extraction — and motivates why processing multiple issue-diff pairs (Step 5) produces better results.

---

## Step 4: (Optional) Third direction — reconstruct the issue from diff + conventions

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
- ./modules/196-reverse-engineering-project-knowledge/tools/example-diff.md
- ./modules/196-reverse-engineering-project-knowledge/tools/example-conventions.md

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

**After the user returns:** Compare `work/196-reconstructed-issue.md` with the original `tools/example-issue.md`. The match demonstrates that the triangle is complete — any two sides can reconstruct the third.

---

## Step 5: Scale it — extract knowledge from multiple commits

**What we're about to do:** Apply the technique to multiple issue-diff pairs to build cumulative project knowledge. Each pair reveals new conventions; together they form a comprehensive instruction file.

In a real project, you would:

1. Pick 5-10 completed issues with clean, self-contained commits
1. For each issue, get the diff: `git log --oneline` to find the commit, then `git show <hash>` for the diff
1. Feed each issue + diff pair to the AI with this prompt:

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

1. After processing all pairs, ask the AI to deduplicate and organize the accumulated conventions into a clean instruction file

**What just happened:** You built a project instruction file entirely from behavioral evidence — not from anyone's memory or opinions, but from what the team actually does.

---

## Step 6: Apply to your own project

**What we're about to do:** Use the technique on a real project you work on.

1. **Pick a repository** you have access to

1. **Find 3-5 completed issues** with associated commits. If using GitHub MCP (module 105):
   ```
   List the last 10 closed issues in [owner/repo] that have associated commits
   ```

1. **Get the diffs** for each issue's commits:
   ```
   git log --oneline --all | head -20
   git show <commit-hash>
   ```

1. **Run the extraction prompt** from Step 3 for each pair

1. **Accumulate and organize** the results into an instruction file

1. **Validate** — ask a teammate: "Does this match how we actually work?"

---

## Success Criteria

After completing this walkthrough, verify:

- ✅ You understand the text-triangle principle and why issue+diff→conventions is the most useful direction
- ✅ You extracted project conventions from an issue + diff pair in a clean experiment
- ✅ You compared extracted conventions with real ones and understand what the technique captures vs. misses
- ✅ You understand how to scale the technique across multiple commits
- ✅ You produced an instruction file from reverse-engineered knowledge

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

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| AI generates generic conventions, not project-specific | Include more of the diff — the AI needs to see actual file names, patterns, and structure to extract specific rules |
| Extracted conventions contradict each other across commits | This is valuable signal — it may indicate inconsistency in the team or an evolving convention. Note both and ask the team which is current |
| Diff is too large for the context window | Split into logical chunks (e.g., by file or feature area). Process each chunk separately and merge the results |
| Can't find issues with clean commits | Look for squash-merged PRs — they often have one clean diff per issue. Or use `git log --grep="ISSUE-123"` to find related commits |
| Model hallucinates conventions not in the diff | Be explicit in the prompt: "Only extract conventions that are directly evidenced in the diff. Quote the specific lines that support each convention." |

---

## Next Steps

With reverse-engineered project knowledge in hand, you're ready for:

- [197 — Onboarding New Team Members with AI](../197-onboarding-new-team-members-with-ai/about.md) — use your extracted instructions to power an AI onboarding system
