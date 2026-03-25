# Shared Instructions & Team Conventions - Hands-on Walkthrough

In this module you will build a shared instructions repository that your whole team can contribute to and pull from. By the end you will have a structure, a contribution workflow, and a plan to introduce it to your team.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

- A shared `instructions/` folder structure ready for a team
- A Git-based contribution workflow (fork → PR → merge)
- A conflict resolution rule set
- An adoption guide document

---

## Part 1: The Problem — Why Individual Prompting Fails at Team Scale

### What we'll do

Understand the cost of every team member having their own ad-hoc prompts.

### The inconsistency problem

| Team member | Their prompt for "review this code" | AI output quality |
|---|---|---|
| Alice | "Review this code" | Generic |
| Bob | "Review for security, performance, and readability" | Better |
| Carol | Uses the full code review instruction from module 070 | Consistent, structured |

The team ships code reviewed at three different quality levels depending on who happened to do the review. Every time Bob leaves the company, his prompt knowledge walks out with him.

### The fix: instructions as organisational knowledge

Instructions are code. They belong in a repository. When Carol improves the review instruction, Bob gets it on his next `git pull`.

**Verify:** You can articulate one specific way inconsistent AI usage costs your team time or quality right now.

---

## Part 2: Shared Repo Structure

### What we'll do

Create the canonical folder structure for a team instructions repository.

### Folder layout

```
team-instructions/
├── README.md                    ← What this repo is, how to use it
├── instructions/
│   ├── main.agent.md            ← Catalog (same pattern as personal instructions)
│   ├── code-review.agent.md     ← How to review PRs
│   ├── debugging.agent.md       ← Debug workflow (from module 064)
│   ├── refactoring.agent.md     ← Refactoring conventions
│   ├── security-review.agent.md ← Security checklist
│   └── onboarding.agent.md      ← How to onboard new joiners
├── conventions/
│   ├── git-commit-messages.md   ← Commit message format
│   ├── code-style.md            ← Language-specific conventions
│   └── pr-checklist.md          ← What every PR needs
└── templates/
    ├── bug-report.md
    └── feature-request.md
```

### Hands-on

Create this structure locally. You don't need content in every file yet — just the folders and empty files.

Windows:
```powershell
mkdir c:/workspace/team-instructions/instructions
mkdir c:/workspace/team-instructions/conventions
mkdir c:/workspace/team-instructions/templates
```

macOS/Linux:
```bash
mkdir -p ~/workspace/team-instructions/{instructions,conventions,templates}
```

Then create `README.md` with a one-paragraph explanation of how to use the repo.

**Verify:** The folder structure exists at `team-instructions/` with three sub-folders.

---

## Part 3: Populate the First Instruction

### What we'll do

Move your personal code review instruction (or create one) into the shared repo.

### Copy an existing instruction

Take any `.agent.md` file you created in module 070. Copy it into `team-instructions/instructions/`.

If you don't have one yet, create `team-instructions/instructions/code-review.agent.md` with:

```markdown
- Review code for: correctness, security, performance, readability — in that priority order.
- Flag any hardcoded secrets, magic numbers, or unsanitised user input.
- Suggest the simplest possible fix, not a full rewrite.
- If logic is unclear, ask a clarifying question before guessing intent.
- Output as a numbered list, one issue per item.
```

### Create the catalog

Create `team-instructions/instructions/main.agent.md`:

```markdown
# Team Instructions Catalog

- `code-review.agent.md` — Structured code review: correctness, security, performance, readability.
  + Keywords: review, PR, pull request, code quality
```

**Verify:** `main.agent.md` links to at least one instruction file.

---

## Part 4: Git-Based Distribution

### What we'll do

Push the shared repo to GitHub and set up the contribution workflow.

### Initial push

```bash
cd c:/workspace/team-instructions     # Windows
# or
cd ~/workspace/team-instructions      # macOS/Linux

git init
git add .
git commit -m "Initial team instructions structure"
```

Create a new repository on github.com (name it `team-instructions`). Then:

```bash
git remote add origin https://github.com/[your-org]/team-instructions.git
git branch -M main
git push -u origin main
```

### Contribution workflow

When a team member wants to improve an instruction:
1. Fork or create a branch: `git checkout -b improve/code-review`
2. Edit the instruction file
3. Commit: `git commit -m "Add output format guidance to code review"`
4. Push and open a Pull Request
5. Team reviews the PR — yes, you review instructions like code
6. Merge → everyone gets the improvement on next `git pull`

### For consumers: pulling updates

```bash
cd team-instructions
git pull origin main
```

**Verify:** The repo is on GitHub and you can see it in your browser.

---

## Part 5: Conflict Resolution

### What we'll do

Define priority rules for when two instructions give contradictory guidance.

### Conflicts happen

Alice writes: "Always add error handling to every function."  
Bob writes: "Keep functions minimal — no defensive code unless at system boundary."

Both are in the repo. What does AI do?

### Resolution rules to add to README.md

```markdown
## Conflict Resolution Rules

1. **More specific wins over general.** A rule in `security-review.agent.md` 
   overrides a general rule in `code-review.agent.md`.
2. **Last-merged wins for overlapping rules.** Check git log to see which was updated last.
3. **Explicit beats implicit.** If one instruction says "always X" and another 
   says "prefer X", "always X" applies.
4. **When in doubt, ask.** Open a GitHub issue titled "Instruction conflict: [topic]".
```

Add these rules to your `README.md`.

**Verify:** README.md contains a conflict resolution section.

---

## Part 6: Adoption Strategy

### What we'll do

Create a one-page plan to introduce shared instructions to your team.

### The COIN adoption pattern

| Stage | Action | Timeline |
|---|---|---|
| **C**opy | Share one existing instruction that solved a real problem | Week 1 |
| **O**bserve | Let 2–3 willing teammates try it for a week | Week 2 |
| **I**mprove | Collect their feedback, update the instruction | Week 3 |
| **N**ormalise | Add to onboarding checklist, reference in team wiki | Week 4+ |

### Hands-on

Create `team-instructions/ADOPTION.md`:

```markdown
# Adoption Plan

## Goal
Reduce inconsistency in AI-assisted code review across the team.

## Pilot
- 3 volunteers use `code-review.agent.md` for 1 sprint
- Collect feedback in this document

## Success metric
PR review comments are more consistent (ask reviewers to rate quality 1-5 after pilot)

## Week 1 champion: [Your Name]
```

**Verify:** `ADOPTION.md` exists and has a concrete first pilot plan.

---

## Success Criteria

- ✅ `team-instructions/` folder structure created with instructions, conventions, templates
- ✅ At least one instruction file in the shared repo
- ✅ `main.agent.md` catalog created and links to the instruction
- ✅ Repo pushed to GitHub
- ✅ Conflict resolution rules documented in README
- ✅ Adoption plan document created

---

## Understanding Check

1. **A team member improves the code review instruction. How do other team members get the update?** *(Answer: They run `git pull origin main` in the team-instructions folder.)*

2. **Two instructions conflict. One says "always validate input" (general), one says "skip validation for internal API calls" (specific). Which wins?** *(Answer: The specific one wins — more specific beats general.)*

3. **Why should instructions go through a PR review process?** *(Answer: Instructions are organisational knowledge that affects everyone's AI quality. New or changed instructions need the same review as code changes.)*

4. **What is the main risk of using AI instructions without version control?** *(Answer: Drift — instructions change over time with no history, no rollback, and no team awareness of what changed.)*

5. **Your team uses both VSCode Copilot and Cursor. Can the same shared instructions repo serve both?** *(Answer: Yes — instructions are IDE-agnostic markdown. Only the thin wrapper files (`.github/prompts/`, `.cursor/rules/`) are IDE-specific. The instructions themselves are shared.)*

---

## Troubleshooting

**"Two people edited the same instruction file — merge conflict."**  
→ Open the file, look for `<<<<<<` markers. Keep both meaningful additions, remove duplicates, resolve contradictions using the conflict resolution rules. Commit the resolved file.

**"Team members aren't pulling updates."**  
→ Add a `git pull team-instructions` step to on your team's sprint start checklist, or set up a Slack/Teams notification when main is updated.

**"I don't have admin rights to create a GitHub org repo."**  
→ Start with a personal repo under your account. Share the URL. Teams can fork it. Later migrate to an org repo when you have approval.

---

## Next Steps

Continue to [Module 080 — Learning from Hallucinations](../080-learning-from-hallucinations/about.md) where you will learn to improve instructions based on AI mistakes — a powerful technique that keeps your shared instruction library getting better over time.
