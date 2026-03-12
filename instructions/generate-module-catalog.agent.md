## Motivation

- Quickly generate a structured overview of all training modules in the course.
- Useful for documentation, onboarding, README files, or sharing course structure with stakeholders.
- Ensures consistent format across all module listings.

## Process

- Scan `./modules/` directory for all module folders.
- Skip any non-module folders (folders without `about.md`).
- For each module folder, read `about.md` to extract:
  + **Title** — first `# heading` in the file.
  + **Description** — the `**Skill:**` line value, or first paragraph after the title if Skill is missing.
- Sort modules by folder name (alphabetical = numeric order due to zero-padded IDs).
- Extract **ID** from folder name — the leading 3-digit number (e.g. `010`, `025`, `300`).
- Generate a markdown table with columns: `№`, `ID`, `Name`, `Description`.
  + `№` — sequential row number starting from 1.
  + `ID` — 3-digit module prefix from folder name.
  + `Name` — extracted title from `about.md`.
  + `Description` — extracted skill/description from `about.md`.
- Add total count summary below the table: `Total: **N modules** in the course.`

## Output Format

- Default: display table in chat response.
- If user asks to save — write to a file they specify (e.g. `readme.md`, `docs/module-list.md`).
- Language: English (module content is always in English per project rules).

## Example Output

```markdown
| № | ID | Name | Description |
|---|-----|------|-------------|
| 1 | 010 | Installing VSCode + GitHub Copilot | Set up your first AI coding environment |
| 2 | 020 | Installing Cursor | Set up alternative AI-native IDE |
| ... | ... | ... | ... |

Total: **33 modules** in the course.
```
