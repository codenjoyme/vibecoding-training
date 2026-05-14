# Instruction Relevance Review

You are a relevance reviewer for SDLC instruction files. Your task:

1. Read ALL `.agent.md` files in `./instructions/` (root level only, skip subdirectories).
2. Read ALL `summary.md` files from `./analysis/*/summary.md` to understand commit history.
3. For each instruction file, determine if it is **still useful** for ongoing development or **one-time/obsolete**.

## ⚠️ MANDATORY READING DISCIPLINE — DO NOT OPTIMIZE

This is a quality gate, not a context-saving exercise. **You MUST read the FULL contents of every `.agent.md` file** — never the first N lines, never a partial range, never a summary heuristic.

**Forbidden patterns (these WILL produce a degraded report and waste a premium request):**
- Reading only `L1:5` or any other partial line range to "save tokens"
- Skipping a file because its title sounds like a one-time setup — you cannot tell without reading the body
- Skipping `summary.md` files because there are many — read all of them
- Treating an empty `Search (glob) "analysis/*/summary.md" → No matches found` as final — if `analysis/` exists but glob returns empty, the files may be `.gitignore`-hidden; explicitly try `Read` on `analysis/<dir>/summary.md` for each directory listed by `List directory analysis`

**Required pattern for every file:**
- Use `Read <file>` with NO line range arguments → reads the entire file
- If the file is large, read it in full sequential chunks (`L1:200`, `L201:400`, …) until EOF — do not stop early

**Why this matters:** an instruction file's first 5 lines typically contain only the title and a one-line summary. The classification (KEEP / REMOVE) depends on the body — concrete examples, file paths it touches, whether the workflow describes one-time setup vs. a repeatable pattern. Reading 5 lines means classifying 35+ files blindly. That run will be discarded and the review will be re-launched, costing another premium request.

**Self-check before producing the report:** every file in `./instructions/*.agent.md` must appear in your read history with its FULL line count (matches what `wc -l` would return), not `L1:5`. If any file shows `L1:5` in your reads, go back and re-read it in full BEFORE producing the table.

## Classification Criteria

**KEEP** — instruction covers a repeatable workflow that will be used for future features:
- Adding endpoints, entities, fields, relationships, migrations, tests
- Adding feature flags, validation rules, exception handling
- Any pattern that recurs with each new feature or ticket

**REMOVE** — instruction covers a one-time setup that is already done and won't repeat:
- Initial project bootstrap (language migration, POM setup)
- One-time infrastructure setup (security config created once, initial DB connection)
- Patterns that were relevant only for the first few commits

**KEEP (meta)** — instruction is about the instruction system itself (catalog, creation guide).

## Output Format

Print a **markdown table** to stdout with these columns:

| File | Status | Reason |
|------|--------|--------|

Where:
- **File** — filename without path (e.g., `add-endpoint.agent.md`)
- **Status** — one of: `KEEP`, `REMOVE`, `KEEP (meta)`
- **Reason** — one sentence explaining why

After the table, print:
- Total files reviewed
- Count of KEEP / REMOVE / KEEP (meta)
- A list of files recommended for removal (if any)

## Rules

- Be conservative — if in doubt, mark as KEEP.
- Do NOT delete any files yourself. Only produce the review report.
- Use English for all output.
- Do NOT create or modify any files — this is a read-only analysis.
