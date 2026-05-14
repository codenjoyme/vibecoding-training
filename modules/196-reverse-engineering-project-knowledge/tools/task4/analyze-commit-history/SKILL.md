---
name: analyze-commit-history
description: 'Analyze git commit history to extract SDLC instruction files. Use when: reverse-engineering workflows from commits, extracting coding patterns from diffs, building agent instructions from real code changes, generating automation knowledge base from commit history. Iterates through commits, extracts per-file diffs, invokes Copilot CLI (Claude Opus 4.6) to identify and document reusable SDLC patterns.'
argument-hint: 'Options: --ticket XYZA-233, --last 5, --prefix XYZA, --skip-research, --dry-run, --review'
---

# Analyze Commit History

Extract reusable SDLC instruction files from git commit history using AI-powered diff analysis.

## When to Use

- Turn real commit diffs into actionable agent instructions for future automation.
- Reverse-engineer development workflows from actual code changes.
- Build a knowledge base of project-specific SDLC patterns.
- Understand how features were implemented across layers (entity → DTO → mapper → service → controller → test).

## Prerequisites

- Python 3.11+
- GitHub Copilot CLI (`copilot.bat`) — auto-detected from VS Code extensions
- Node.js in PATH (required by Copilot CLI)
- Git repository with commit history

## Procedure

### Option A — Manifest-Driven Workflow (recommended for full history coverage)

Use this when you want to process specific commits, including commits without ticket prefixes.

**Step 1 — Generate the commit manifest:**

```bash
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --generate-manifest
```

This creates `.dark-factory/config/commits-manifest.md` listing every commit in the repo:
- `[x]` = already processed
- `[ ]` = available, not yet selected
- `[>]` = selected by user to process next
- `[-]` = explicitly skipped (not relevant for analysis — e.g., factory meta, merge commits, docs-only)

**Step 2 — Select commits:**  
Open `commits-manifest.md` and change `[ ]` → `[>]` for any commits you want to analyze.

**Step 3 — Process selected commits:**

```bash
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --from-manifest
```

The script processes every `[>]` entry in order, runs the AI agent per commit, auto-commits instructions, and updates `[>]` → `[x]` in the manifest as each commit is completed.

**Monitoring (observer agent):** After each commit is processed, update the manifest checkbox from `[>]` to `[x]` if doing manual monitoring.

---

### Option B — Prefix-Filtered Workflow (fast path for ticket-based repos)

1. Run the analysis script from repository root. The script automatically runs a **Research Phase** first:
   - Scans all commits and extracts ticket-like prefix patterns (e.g., `XYZA`, `ACT`, `FEAT`)
   - Writes `analysis/commit-stats.txt` with prefix counts
   - Uses Copilot CLI to classify prefixes as relevant vs. noise
   - Saves result to `analysis/discovered-prefixes.json`
   - Only commits matching relevant prefixes proceed to diff analysis

   Use `--prefix XYZA` to skip auto-discovery and specify prefixes manually.  
   Use `--skip-research` to process all ticket-like commits without LLM classification.
   Use `--all-commits` to process every commit regardless of prefix (includes commits without ticket IDs).

```bash
# Auto-discover relevant prefixes, then analyze all matching commits
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py

# Specific ticket
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --ticket XYZA-233

# Last N commits
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --last 5

# Commit range
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --from abc123 --to def456

# Manually specify prefixes (skips auto-discovery)
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --prefix XYZA --prefix ACT

# Skip research phase — process all ticket-like commits
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --skip-research

# Process ALL commits including those without ticket prefixes
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --all-commits

# Dry run (extract diffs only, skip AI agent)
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --dry-run

# Review instruction relevance (standalone)
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --review

# Process commits then review
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --from abc123 --to def456 --review

# Process in batches of 5 (oldest first), with one instruction commit per source commit
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --batch 5

# Process all commits with per-commit instruction commits
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py

# Skip auto-commit of instructions
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --no-commit
```

2. Review generated output in `analysis/` directory.

3. Promote best instruction files to `./instructions/` and register in catalog.

## How It Works

For each run the [script](./scripts/analyze-commits.py) performs:

- **Manifest** (`--generate-manifest`): scans all commits via `git log --reverse`, checks which are already analyzed (by inspecting `analyze(instructions): <sha>` entries in current branch git log), writes `commits-manifest.md` with `[x]`/`[ ]` checkboxes. User edits `[ ]` → `[>]` to select; `--from-manifest` reads `[>]` entries and processes them, updating to `[x]` as each completes.
- **Research** (auto, skipped with `--prefix`, `--skip-research`, `--all-commits`, or `--from-manifest`): scans `git log --format=%s`, extracts all `[A-Z]+-\d+` patterns, writes `analysis/commit-stats.txt`, invokes Copilot CLI with [discovery instruction](./references/discover-prefixes.instruction.md) to classify prefixes → reads `analysis/discovered-prefixes.json` for the list of relevant prefixes.
- **Extract**: `git diff SHA~1 SHA` split into per-file `.diff` files → `analysis/TICKET-NNN-XXXXXXXX/diff/`
- **Analyze**: Copilot CLI invoked with [CLI agent instruction](./references/analyze-commit-diff.instruction.md), reads diffs, identifies SDLC patterns
- **Write**: Agent produces `./instructions/*.agent.md` per pattern and a `summary.md`
- **Review** (optional): After all commits, AI agent reviews all instructions for relevance — flags one-time/obsolete files for removal

## Output Structure

```
analysis/
├── commit-stats.txt             # prefix statistics from research phase
├── discovered-prefixes.json     # LLM classification output
├── XYZA-233-a1b2c3d4/
│   ├── commit-info.txt          # SHA, subject, ticket
│   ├── diff/                    # per-file diffs
│   │   ├── src__main__java__...Entity.java.diff
│   │   └── ...
│   └── summary.md               # agent-generated analysis summary
├── XYZA-286-e5f6g7h8/
│   └── ...
```

Directory names include 8-char commit hash to avoid collisions when the same ticket has multiple commits.

## Iterative Refinement

- Each run enriches existing instructions — new patterns appended, never overwritten.
- After each successfully processed source commit, the script automatically runs `git add instructions/` and `git commit -m "analyze(instructions): <sha> — <subject>"` — one instruction git commit per source commit (1:1 ratio).
- In `--from-manifest` mode, the manifest file is also updated (`[>]` → `[x]`) after each commit and staged alongside instructions.
- Use `--batch 5` to process only the 5 oldest matching commits per run (oldest first), letting you advance incrementally. `--batch 0` (default) processes all matching commits.
- Use `--no-commit` to skip auto-commits.
- Use `--all-commits` to include commits without ticket prefixes in a regular (non-manifest) run.
- Run per-feature or per-sprint for growing knowledge base.
- After review, promote results: copy to `./instructions/`, register in `main.agent.md`.

## Working from a Non-Production Branch

When you work on a long-lived feature branch (e.g. `feature/dark-factory`) and want to analyze only production commits from `develop`, use the **classify-by-branch** workflow:

### Full sync cycle

```bash
# 1. Pull latest production commits
git pull origin develop

# 2. Regenerate manifest (picks up new commits)
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --generate-manifest

# 3. Classify: mark non-develop and merge commits as [-]
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --classify-branch develop

# 4. Review candidates, mark [>] for selected, run analysis
python .dark-factory/instructions/analyze-commit-history/scripts/analyze-commits.py --from-manifest --batch 20
```

### How `--classify-branch` works

1. Finds the **last `[x]` commit** in the manifest as the baseline.
2. Queries `origin/<branch>` for all SHAs after that baseline.
3. For each `[ ]` entry in the manifest:
   - **Not on the branch** → `[-]` (factory/docs/meta commit, not production)
   - **Merge commit** on the branch → `[-]` (merge commits carry no unique diffs)
   - **Otherwise** → stays `[ ]` (production candidate for analysis)

### Key rules for incremental analysis

- **Forward-only**: always process commits **after** the last `[x]` processed commit. Never go backwards — later instructions override earlier ones.
- **The script is not intelligent**: it just lists commits and preserves markers. The **model** (or operator) decides which `[ ]` to promote to `[>]` based on production relevance.
- **`[-]` is permanent**: once skipped, a commit stays skipped. The script preserves `[-]` across regenerations.
- **Branch affinity**: the manifest tracks commits on the **current branch** (where you run the script). Classification against a production branch is a post-generation step.

## Resources

- [Python script](./scripts/analyze-commits.py) — main orchestrator
- [Commit manifest](../../config/commits-manifest.md) — all-commits tracking file with checkboxes (generated by `--generate-manifest`); lives in `.dark-factory/config/` as part of project configuration
- [CLI agent instruction](./references/analyze-commit-diff.instruction.md) — passed to Copilot CLI per commit
- [Review instruction](./references/review-instructions.instruction.md) — passed to Copilot CLI for `--review` relevance check
- [Discovery instruction](./references/discover-prefixes.instruction.md) — passed to Copilot CLI for research phase prefix classification
