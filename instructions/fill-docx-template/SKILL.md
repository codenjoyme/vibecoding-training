---
name: fill-docx-template
description: Fill a DOCX template interactively — extracts <placeholder> names via CLI, asks the user for each value with vscode_askQuestions, then produces a filled copy. The original template is never modified.
version: 2.0.0
---

- Use this skill when asked to **fill a DOCX template** with data.
- Input: a `.docx` template path + desired output path.
- Placeholders are discovered automatically from the template — no properties file needed.
- Agent asks the user for every placeholder value using the `vscode_askQuestions` tool.
- Output: a new `.docx` file — a filled copy. Original template is never touched.

## Step-by-step agent workflow

**Step 1 — get template and output paths**
- If the user has not provided both, ask them (one `vscode_askQuestions` call with two questions):
  + `template` — path to the `.docx` template file.
  + `output` — desired path for the filled output file.

**Step 2 — extract placeholders via CLI**
- Run the extractor script and capture the output:
  ```
  python instructions/fill-docx-template/scripts/extract_placeholders.py \
      --template <template-path>
  ```
- Each line of stdout is one placeholder key name (without angle brackets), e.g. `data1`, `fullName`.
- If no placeholders are found — inform the user and stop.

**Step 3 — ask the user for values**
- Build one `vscode_askQuestions` call with one question per placeholder:
  + `header` — the placeholder key (e.g. `data1`).
  + `question` — `"Enter value for <data1>:"` (show the angle-bracket form so the user sees what it replaces).
- Send **all questions in a single call** — do not loop one-by-one.
- Example call structure:
  ```json
  {
    "questions": [
      { "header": "data1", "question": "Enter value for <data1>:" },
      { "header": "data2", "question": "Enter value for <data2>:" },
      { "header": "data3", "question": "Enter value for <data3>:" }
    ]
  }
  ```

**Step 4 — fill the template**
- Run the fill script, passing each answer as a `--set key=value` argument:
  ```
  python instructions/fill-docx-template/scripts/fill_docx_template.py \
      --template <template-path> \
      --output <output-path> \
      --set data1="Alice Johnson" \
      --set data2="Software Engineer" \
      --set data3="Acme Corp"
  ```
- `--properties` is optional and can be omitted in the interactive flow.

**Step 5 — confirm**
- Report the output file path to the user.
- Optionally show a summary table of key → value used.

## Scripts reference

- `extract_placeholders.py` — prints placeholder names (one per line) from a DOCX.
  + Script: [scripts/extract_placeholders.py](./scripts/extract_placeholders.py)
  + Args: `--template TEMPLATE.docx`
- `fill_docx_template.py` — copies template and replaces `<key>` tokens.
  + Script: [scripts/fill_docx_template.py](./scripts/fill_docx_template.py)
  + Args: `--template`, `--output`, `--set key=value` (repeatable), `--properties` (optional).

## Placeholder format

- Templates use angle-bracket syntax: `<key>` (e.g. `<data1>`, `<fullName>`, `<date>`).
- Placeholders may appear in body paragraphs and table cells.
- Placeholders split across XML runs are handled automatically.

## Prerequisites

- Python 3.8+
- `pip install python-docx`

## Alternative: properties-file mode (non-interactive)

- Still supported for batch / CI scenarios:
  ```
  python instructions/fill-docx-template/scripts/fill_docx_template.py \
      --template path/to/Template.docx \
      --properties path/to/data.properties \
      --output path/to/Output.docx
  ```
- Properties file format — one `key=value` per line, `#` lines are comments:
  ```properties
  data1=Alice Johnson
  data2=Senior Engineer
  ```
