# Reverse Engineering Project Knowledge from Text - Hands-on Walkthrough

In this walkthrough, you'll learn the text-triangle principle — a powerful mental model for extracting hidden knowledge from existing project artifacts. You'll practice by taking real issue-diff pairs and reverse-engineering project instructions that capture how the team actually works.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **Understanding of the text-triangle principle** — why any two related texts can generate the third
- **A reverse-engineered instruction file** — extracted from real issue + diff pairs
- **A repeatable workflow** — for extracting project knowledge commit by commit
- **Practical experience** — with three different "triangle directions" on the same text set

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

## Step 2: Try it on a concrete example — forward direction

**What we're about to do:** Start with the "normal" direction to build intuition before reversing it.

Open the example files in `tools/`:

- [tools/example-issue.md](tools/example-issue.md) — a task description (the "issue")
- [tools/example-diff.md](tools/example-diff.md) — the implementation that was done (the "diff")
- [tools/example-conventions.md](tools/example-conventions.md) — the project conventions (the "knowledge")

First, try the standard direction. Give AI the **issue** + **conventions** and ask it to predict the implementation:

```
I have a task description and project conventions. Based on these two texts,
predict what the implementation diff would look like.

Do NOT write actual code — instead, describe:
1. Which files would be changed
2. What patterns/structures would be used
3. What naming conventions would apply
4. What the key decisions would be

## Task Description
[paste content of tools/example-issue.md]

## Project Conventions
[paste content of tools/example-conventions.md]
```

Now compare the AI's prediction with the actual diff in `tools/example-diff.md`. You'll notice the AI gets surprisingly close — because the conventions bridge the gap between "what to do" and "how to do it".

---

## Step 3: Reverse the direction — extract conventions from issue + diff

**What we're about to do:** This is the core skill. Feed the AI an issue and its implementation, and ask it to extract the project knowledge that connects them.

Use this prompt:

```
I have a completed task: the original issue description and the actual
implementation diff. Your job is to reverse-engineer the project conventions,
coding standards, and architecture decisions that guided this implementation.

Look at the GAP between what was asked (issue) and how it was done (diff).
The decisions that fill that gap ARE the project knowledge.

Extract:
1. Naming conventions (files, variables, functions, classes)
2. Architecture patterns (folder structure, layering, separation of concerns)
3. Code style rules (formatting, error handling, imports)
4. Workflow conventions (commit style, PR patterns)
5. Technology choices and their implications

Format the output as an instruction file (.agent.md) that could guide
a new developer on this project.

## Original Issue
[paste content of tools/example-issue.md]

## Implementation Diff
[paste content of tools/example-diff.md]
```

**What just happened:** The AI analyzed the transformation from issue to code and identified the implicit rules. You now have an instruction file that was never written by a human — it was reverse-engineered from actual behavior.

---

## Step 4: Third direction — reconstruct the issue from diff + conventions

**What we're about to do:** Complete the triangle by trying the third direction — useful for understanding undocumented changes.

```
I have a code diff and the project conventions. Reconstruct the original
task/issue that likely led to this implementation.

Based on what was changed and how it follows the conventions, infer:
1. What was the user-facing problem or feature request?
2. What were the acceptance criteria?
3. What technical context would have been in the issue?

## Implementation Diff
[paste content of tools/example-diff.md]

## Project Conventions
[paste content of tools/example-conventions.md]
```

Compare the AI's reconstructed issue with the original `tools/example-issue.md`. The match demonstrates that the triangle is complete — any two sides can reconstruct the third.

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

- ✅ You understand the text-triangle principle (1+2→3, 1+3→2, 2+3→1)
- ✅ You extracted project conventions from at least one issue + diff pair
- ✅ You tried all three triangle directions on the example texts
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
