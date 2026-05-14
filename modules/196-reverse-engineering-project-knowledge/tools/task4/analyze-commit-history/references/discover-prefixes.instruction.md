# Commit Prefix Discovery Instruction

You are a commit history analyst. Your task is to classify ticket-like prefixes found in this repository's commit history.

## Input

Read the file `analysis/commit-stats.txt` — it contains ticket-like prefixes extracted from git commit subjects and their occurrence counts.

## Analysis

For each prefix, classify it as **RELEVANT** or **NOISE**:

**RELEVANT** — represents real feature/bugfix development work tracked in an issue tracker:
- Multiple commits with consistent naming (e.g., `XYZA-233`, `XYZA-286`)
- Follows a project ticket format (Jira, Linear, GitHub Issues, YouTrack, etc.)
- Pattern suggests incremental feature delivery over time

**NOISE** — one-off, infrastructure, CI/CD, merge, or miscellaneous commits:
- Very few occurrences (1–2 commits) unless clearly a real ticket
- Names like `CI`, `BUMP`, `BOT`, `CHORE`, `WIP`, `MERGE`, `HOTFIX` with no numbering pattern
- Auto-generated or tooling commits

## Output

Write ONLY the following JSON to `analysis/discovered-prefixes.json` using file tools:

```json
{
  "relevant_prefixes": ["PREFIX1", "PREFIX2"],
  "noise_prefixes": ["NOISE1"],
  "reasoning": "One sentence explaining the classification"
}
```

## Rules

- Write the JSON file using file write tools. Do NOT print it to stdout.
- Use UPPERCASE prefix names without the numeric part (e.g., `"XYZA"` not `"XYZA-233"`).
- If `analysis/commit-stats.txt` is missing or empty, write `{"relevant_prefixes": [], "noise_prefixes": [], "reasoning": "No data found"}`.
- Be inclusive — if unsure, classify as RELEVANT.
- Do NOT create or modify any other files.
