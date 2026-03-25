## Motivation

- LND module markdown files reference screenshots added during manual review.
- Screenshots are initially pasted by the author with auto-generated names (`image.png`, `image-1.png`, etc.) directly into `lnd/output/`.
- These names are meaningless, cluttering the output folder and making it impossible to identify images without opening the markdown.
- This instruction standardizes image organization: structured folders, descriptive filenames, and consistent markdown references.

## Naming Convention

- Images are stored in: `lnd/output/img/module-NN/MM-short-description.png`
  + `NN` — two-digit module number (e.g., `01`, `12`, `20`).
  + `MM` — two-digit sequential image number within the module, starting from `01`.
  + `short-description` — 2-5 lowercase words separated by hyphens, derived from the markdown alt text (`![alt text](...)`) or from surrounding context if alt text is absent.
  + Extension: always `.png` (convert if original is `.jpg`, `.gif`, etc.).
- Examples:
  + `lnd/output/img/module-01/01-vscode-ide-with-copilot.png`
  + `lnd/output/img/module-01/02-download-vscode.png`
  + `lnd/output/img/module-05/01-screenshot-paste-into-chat.png`

## Markdown Reference Format

- After renaming, the markdown image reference must use a relative path from the module file:
  + `![Alt text](img/module-NN/MM-short-description.png)`
- Alt text should be kept as-is from the original (or improved if it was generic like "image").
- If the same image is referenced multiple times in the same module, all references point to the same file. The sequential number (`MM`) is assigned at the first occurrence.

## Workflow — Organize Images for a Module

When the user asks to organize/clean up images for a module (or multiple modules):

1. **Read the module markdown file** — find all `![...](...)` image references.
2. **List existing image files** — check which files exist in `lnd/output/` (flat) or already in `lnd/output/img/module-NN/`.
3. **Assign sequential numbers** — in order of first appearance in the markdown, starting from `01`.
4. **Generate new filename** — from the alt text or surrounding context:
   + Lowercase, hyphens instead of spaces, strip special characters.
   + Keep it short: 2-5 descriptive words.
   + Prefix with `MM-`.
5. **Create the target folder** if it does not exist: `lnd/output/img/module-NN/`.
6. **Move (rename) each image file** from its current location to the new path.
7. **Update all image references** in the markdown file to use the new relative path `img/module-NN/MM-short-description.png`.
8. **Handle duplicates** — if the same source file is referenced more than once, move it once (using the index from the first occurrence) and update all references to point to the same new path.
9. **Report** — list all moves performed and confirm the markdown is updated.

## Edge Cases

- If an image file referenced in the markdown does not exist on disk — warn the user, leave the markdown reference as-is for manual review.
- If images already exist in `lnd/output/img/module-NN/` with the correct naming — skip them, do not re-move.
- If the user asks to process "all modules" — iterate over each `module-*.md` file and apply the workflow per module.
- Preserve any images that are NOT referenced from any module markdown — warn the user about orphaned files.
