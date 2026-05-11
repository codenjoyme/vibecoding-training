# Create Module Task Artifacts

- Generate three verification artifacts for a training module: **student prompt**, **reference report**, and **autocheck prompt**.
- All artifacts are placed in `lnd/output/task/` with naming convention `module-NN-{prompt,report,autocheck}.md`.
- Replace `NN` with the zero-padded module number (e.g. `03`, `10`).
- Use `lnd/output/task/module-03-*` files as the reference example — follow their structure, tone, and formatting.

## Inputs

- Module number and title (e.g. "Module 03 — Version Control with Git").
- Module walkthrough (`modules/NNN-*/walkthrough.md`) — to understand what the student actually does.
- Module about (`modules/NNN-*/about.md`) — to get learning objectives.
- Corresponding LND module file (`lnd/output/module-NN-*.md`) — load to understand what the student sees and works with during the session.

## Artifact 1: Student Prompt (`module-NN-prompt.md`)

- Purpose: student copies this prompt into their AI assistant session to generate a completion report.
- Structure:
  + Congratulatory intro paragraph.
  + Instruction to copy the prompt block and paste into the same session.
  + Single fenced code block (` ``` `) containing the full copyable prompt.
  + Inside the code block, use `~~~` instead of ` ``` ` for any nested fences.
- The copyable prompt inside must include:
  + A title: `# Module NN — <Title>: Completion Report`.
  + `## Instructions` — what commands to run or data to collect.
  + `## Report format` — exact markdown structure for the output file.
  + Explicit save path: `Save this report as work/module-NN-report.md`.
- Reference the session context, not a specific directory:
  + Use "Run the following commands in the project directory where you completed the module" — NOT a hardcoded path.
- The outer wrapper tells student to copy the contents of `work/module-NN-report.md` and paste them into the answer text field on the learning platform (NOT upload as attachment).

## Artifact 2: Reference Report (`module-NN-report.md`)

- Purpose: benchmark showing what a correct completion report looks like.
- Use a fictional identity (e.g. "Jane Developer", `jane.developer@example.com`) — NOT a real student.
- Fill all sections with realistic but clearly fictional data.
- Must satisfy all required criteria from the autocheck prompt.
- The autocheck uses this to detect copy-pasted submissions — if a student submits this verbatim, it triggers fraud detection.

## Artifact 3: Autocheck Prompt (`module-NN-autocheck.md`)

- Purpose: hidden grading prompt for the verification system (not shown to students).
- Structure:
  + `## Expected input structure` — the markdown format the student report should follow.
  + `## Verification criteria` — table with columns: #, Criterion, How to verify, Weight (Required/Optional).
  + `## Scoring` — PASS / PARTIAL / NEEDS REVIEW thresholds based on required criteria count.
  + `## Fraud detection` — list of suspicious signals (fabricated data, copy-pasted reference, impossible timeline, missing raw data, structure mismatch).
  + `## Output format` — return a verdict (`PASS`, `PARTIAL`, `NEEDS_REVIEW`, `SUSPICIOUS`) with a brief human-readable summary. If suspicious, list the specific fraud indicators.
- Keep output format as plain text verdict + summary — no JSON.
- Fraud detection must include a check for the reference report being submitted verbatim.

## Quality Checklist

- All three files are consistent: report structure in prompt matches expected structure in autocheck.
- Reference report satisfies all required criteria from autocheck.
- No hardcoded directory paths — use session-relative references.
- Nested code fences inside the student prompt use `~~~` (not ` ``` `).
- Module number is consistent across all three filenames and content.
- Verification criteria are NOT visible to the student — they live only in the autocheck file.
- Student prompt says "paste contents into the answer text field" — NOT "upload the file".
- Autocheck output format is plain text (verdict + summary) — NOT JSON.
