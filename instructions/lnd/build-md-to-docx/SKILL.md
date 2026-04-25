---
name: build-md-to-docx
description: Convert a list of markdown files (with images, code blocks, quizzes) into a single landscape DOCX with TOC, page breaks between files, shaded inline-code, and uniform image scaling
version: 1.0.0
---

- Use this skill whenever the user asks to **combine, export, or build a DOCX** from a set of markdown files (typical case: LND module markdowns in `lnd/output/`).
- Skill produces **one DOCX** with: synthetic title per source file, hard page break between files, table of contents (depth 2), shaded inline `code`, uniform image scaling, landscape 14×11" page with 0.5" margins.
- Source files must be plain CommonMark (with `commonmark_x+raw_attribute-fancy_lists` extensions) — works for the LND module style produced by [lnd/generate-lnd-modules.agent.md](../generate-lnd-modules.agent.md).

## Prerequisites

- **Python 3.10+** (uses `from __future__ import annotations` and modern typing).
- **Pandoc binary.** Either install system-wide or let the script auto-download via `pypandoc`.
  + Windows (winget): `winget install --id JohnMacFarlane.Pandoc -e`
  + macOS (Homebrew): `brew install pandoc`
  + Ubuntu/Debian: `sudo apt-get install -y pandoc`
  + Auto-download fallback: the script calls `pypandoc.download_pandoc()` if no binary is found (writes into `%LOCALAPPDATA%\Pandoc` on Windows, `~/.local/share/pandoc` on Linux/macOS).
  + Verify: `pandoc --version` should print **3.0 or higher**.
- **Python packages:**
  ```
  python -m pip install pypandoc Pillow
  ```
  + `pypandoc` (≥ 1.13) — drives Pandoc.
  + `Pillow` (≥ 10.0) — reads native image dimensions used for uniform scaling.

## How to invoke

- Script: [scripts/build_docx.py](./scripts/build_docx.py)
- Reference template: [scripts/reference.docx](./scripts/reference.docx) (regenerated on every run from Pandoc's default; do not hand-edit).

```
python instructions/lnd/build-md-to-docx/scripts/build_docx.py \
    --output path/to/result.docx \
    --resource-path path/to/folder/with/img \
    path/to/file1.md path/to/file2.md ...
```

- **Required arguments:**
  + `--output PATH` — destination `.docx` file. Parent folder must exist.
  + Positional `INPUT [INPUT ...]` — one or more markdown files to combine in the given order. Globs are expanded by the shell; use quoting if the shell does not expand them.
- **Optional arguments:**
  + `--resource-path PATH` — folder Pandoc uses to resolve relative image paths (`![](img/foo.png)`). Defaults to the **parent folder of the first input file**. Override when images live somewhere else (e.g. all inputs share `lnd/output/img/`).
  + `--reference-docx PATH` — override the bundled reference template. By default uses [scripts/reference.docx](./scripts/reference.docx). The template is auto-regenerated on every run.
  + `--shared-scale FLOAT` — override uniform image scale (default `0.89`, ≈ 108 DPI). Lower → smaller images. The same factor is applied to every image so on-screenshot text stays the same physical size across the document.
  + `--no-toc` — skip the table of contents.
  + `--toc-depth N` — TOC heading depth (default `2`).
  + `--title-from-filename` — derive each file's H1 title from its filename (`module-01-installing-vscode` → `Module 01 — Installing Vscode`) and strip the existing first H1 from the file body. Default behaviour: keep file content as-is, no synthetic title.
  + `--skip FILENAME` — repeatable; skip an input by basename (does not error if not present).

### Examples

- **One file (test run):**
  ```
  python instructions/lnd/build-md-to-docx/scripts/build_docx.py \
      --output /tmp/one.docx \
      lnd/output/module-01-installing-vscode.md
  ```
- **Several explicit files in order:**
  ```
  python instructions/lnd/build-md-to-docx/scripts/build_docx.py \
      --output lnd/output/three-modules.docx \
      --resource-path lnd/output \
      --title-from-filename \
      lnd/output/module-01-installing-vscode.md \
      lnd/output/module-02-installing-cursor.md \
      lnd/output/module-03-version-control-git.md
  ```
- **All LND modules (the original `lnd/output/all-modules.docx` use case):**
  ```
  python instructions/lnd/build-md-to-docx/scripts/build_docx.py \
      --output lnd/output/all-modules.docx \
      --resource-path lnd/output \
      --title-from-filename \
      --skip module-02b-installing-claude-code-codemie.md \
      lnd/output/module-*.md
  ```
  + On Windows PowerShell, expand the glob explicitly: `(Get-ChildItem lnd/output/module-*.md).FullName`.

## What the skill produces (technical details)

- **Page setup:** custom landscape `14"×11"` with `0.5"` margins on all sides (text area `13"×10"` ≈ `1248×960 px` at 96 DPI). This prevents Word from auto-shrinking wide screenshots to fit a narrower page.
- **Inline code shading:** the `VerbatimChar` character style in the reference template is patched to render with light-gray (`#EEEEEE`) background — visually highlights inline `` `code` `` spans.
- **Image scaling:** every image gets `{width="Npx"}` appended, where `N = round(native_width_px * SHARED_SCALE)`. The same factor is applied universally — no per-image cap — so the physical size of any text rendered inside a screenshot stays constant from one image to the next. Adjust globally via `--shared-scale`.
- **Page breaks:** raw OpenXML `<w:br w:type="page"/>` is injected between each pair of input files (passed through Pandoc as `` ```{=openxml} `` block).
- **TOC:** generated by Pandoc (`--toc --toc-depth=N`).
- **Pandoc input format:** `commonmark_x+raw_attribute-fancy_lists`.
  + `commonmark_x` enables Pandoc's `+attributes` extension required for the `{width="Npx"}` syntax.
  + `+raw_attribute` lets the page-break OpenXML pass through verbatim.
  + `-fancy_lists` disables the alphabetical list marker so quiz items like `(a)`, `(b)`, `(c)` render as text inside bullet points instead of being interpreted as nested ordered lists.

## Troubleshooting

- **`Permission denied` when writing the output `.docx`** — the file is open in Word/LibreOffice/Explorer preview. Close it and re-run.
- **Image reference shows up as alt text only** — the file does not exist at the resolved path. Check `--resource-path` and the relative path inside the markdown.
- **Pandoc binary not found** — install via the OS package manager or let the script auto-download (requires network access on first run).
- **TOC links/headings look broken in Word** — open the document, right-click the TOC, choose "Update Field" → "Update entire table".
- **Wide screenshots still look shrunk** — Word may apply its own maximum picture size in a particular template. The skill uses landscape 14×11" by default; if the user's OS Word still shrinks, lower `--shared-scale` to e.g. `0.7`.

## Style references
- See [scripts/build_docx.py](./scripts/build_docx.py) for the actual implementation. Constants at the top of the file (`SHARED_SCALE`, `PAGE_W_TWIPS`, `INLINE_CODE_SHADE`, etc.) document the calibration choices arrived at iteratively.
