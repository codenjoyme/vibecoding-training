## Purpose

- Extract project conventions from the gap between what was asked (issue) and how it was done (commit diff).
- Build a living conventions document that accumulates knowledge across multiple issues.
- Each discovered convention is traceable to the issue/commit that revealed it.

## Inputs

- **Issue text** — the problem description, acceptance criteria, or feature request (required).
- **Commit diff** — the actual implementation changes: `git diff` or PR diff (required).
- **Existing conventions file** — a previously generated conventions document to accumulate into (optional).
  + When provided, only add NEW insights not already captured.
  + Preserve all existing entries and their sources unchanged.

## Workflow

- Read the issue text — understand what was requested, what constraints were stated.
- Read the commit diff — understand what was actually done, how decisions were made.
- Identify the gap — what the diff reveals that the issue did NOT explicitly ask for.
  + Implicit decisions: why this folder, this naming, this pattern, this library.
  + Structural choices: file placement, module boundaries, layer separation.
  + Style choices: formatting, naming conventions, error handling patterns.
  + Safety choices: validation, security measures, access control patterns.
- Extract conventions into categories (see Output Format below).
- If existing conventions file is provided:
  + Compare each discovered convention against existing entries.
  + Skip duplicates — do not re-add what is already documented.
  + Add only genuinely new insights with proper source attribution.
- Output the structured conventions file.

## What to Extract

- **Naming conventions** — file naming, variable naming, function naming, branch naming, commit message patterns.
  + Example: "Service files use `*Service.ts` suffix" — Source: Issue #47
- **Architecture patterns** — folder structure, layer separation, dependency direction, module boundaries.
  + Example: "Business logic lives in `domain/` folder, never in controllers" — Source: Issue #12
- **Code style rules** — formatting, import ordering, error handling, logging patterns, comment conventions.
  + Example: "All public API methods have JSDoc with `@throws` annotation" — Source: Issue #33
- **Technology choices** — libraries, frameworks, tools, versions, and why they were chosen over alternatives.
  + Example: "Use `zod` for runtime validation, not `joi`" — Source: Issue #8
- **Security patterns** — input validation, authentication, authorization, secrets handling, OWASP considerations.
  + Example: "All user input is sanitized via `sanitizeHtml()` before storage" — Source: Issue #55
- **Testing conventions** — test file placement, naming, coverage expectations, test data patterns, mocking approach.
  + Example: "Unit tests co-located with source files as `*.test.ts`" — Source: Issue #21
- **Git & workflow conventions** — branch naming, commit message format, PR structure, review process.
  + Example: "Commits follow Conventional Commits: `feat:`, `fix:`, `chore:`" — Source: Issue #3

## Source Attribution

- Every convention entry must end with `— Source: Issue #N` (or PR, commit SHA — whatever identifies the origin).
- When a convention is confirmed by multiple issues, list all sources: `— Source: Issue #12, Issue #47`.
- Source attribution enables traceability — anyone can verify why a convention exists.

## Output Format

- Output a markdown file with the following structure:

```markdown
# Project Conventions

> Auto-extracted from issue/commit history. Each convention includes its source for traceability.

## Naming Conventions
- [convention entry] — Source: Issue #N

## Architecture Patterns
- [convention entry] — Source: Issue #N

## Code Style Rules
- [convention entry] — Source: Issue #N

## Technology Choices
- [convention entry] — Source: Issue #N

## Security Patterns
- [convention entry] — Source: Issue #N

## Testing Conventions
- [convention entry] — Source: Issue #N

## Git & Workflow Conventions
- [convention entry] — Source: Issue #N
```

- Omit empty sections — only include categories where conventions were actually found.
- Keep entries concise — one line per convention, actionable, no lengthy explanations.

## Accumulation Mode

- When an existing conventions file is provided as input:
  + Parse all existing entries and their sources.
  + Run the extraction workflow on the new issue + diff.
  + For each newly found convention, check if the same or equivalent rule already exists.
  + If equivalent exists — optionally append the new source to the existing entry's source list.
  + If genuinely new — add it under the appropriate category with its source.
  + Never remove or rewrite existing entries.
- This enables incremental knowledge building across the project's history.

## Edge Cases

- If the diff contains only mechanical changes (dependency bumps, auto-formatting) — note that no meaningful conventions were found.
- If the issue is vague but the diff reveals strong patterns — extract conventions from the diff alone, noting limited issue context.
- If conventions conflict with each other across issues — flag the conflict explicitly and list both sources.
