---
name: fill-docx-template
description: Fill a DOCX template by copying it and replacing <placeholder> tokens with values from a .properties file. The original template is never modified.
version: 1.0.0
---

- Use this skill when asked to **fill a DOCX template** with data from a properties file.
- Input: a `.docx` template with `<key>` placeholders + a `.properties` file with `key=value` lines.
- Output: a new `.docx` file — a filled copy of the template. Original is never touched.

## Placeholders

- Template placeholders use angle-bracket syntax: `<key>` (e.g. `<data1>`, `<fullName>`, `<date>`).
- Inspect all placeholders in a template by running:
  ```
  python -c "
  from docx import Document
  doc = Document('path/to/Template.docx')
  for p in doc.paragraphs:
      if p.text.strip(): print(p.text)
  "
  ```

## Properties file format

- One `key=value` pair per line.
- Lines starting with `#` are comments — ignored.
- Keys must match placeholder names exactly (without angle brackets).
- Example for a template with `<data1>`, `<data2>`, `<data3>`:
  ```properties
  # data.properties
  data1=Alice Johnson
  data2=Senior Engineer
  data3=Acme Corp
  ```

## Prerequisites

- Python 3.8+
- `pip install python-docx`

## How to invoke

- Script: [scripts/fill_docx_template.py](./scripts/fill_docx_template.py)

```
python instructions/fill-docx-template/scripts/fill_docx_template.py \
    --template path/to/Template.docx \
    --properties path/to/data.properties \
    --output path/to/Output.docx
```

- `--template` — path to the source `.docx` template (read-only, never modified).
- `--properties` — path to the `.properties` file with `key=value` pairs.
- `--output` — destination path for the filled `.docx`. Parent folder is created automatically.

### Example with the course test template

```
python instructions/fill-docx-template/scripts/fill_docx_template.py \
    --template work/test-docx/Template.docx \
    --properties work/test-docx/data.properties \
    --output work/test-docx/Filled.docx
```

Sample `data.properties` for `work/test-docx/Template.docx` (placeholders: `<data1>`–`<data6>`):
```properties
data1=Alice Johnson
data2=Software Engineer
data3=Acme Corp
data4=2024
data5=New York
data6=USA
```

## Behavior details

- The original template is **never modified** — the script copies it first, then edits the copy.
- Replacements happen in **all paragraphs and all table cells**.
- If a placeholder is split across multiple Word XML runs (can happen after copy-paste or autocorrect), the script merges those runs automatically — slight formatting loss only for that run.
- Properties keys with no matching placeholder in the template are silently ignored.
- Placeholders with no matching key in the properties file are left unchanged in the output.
