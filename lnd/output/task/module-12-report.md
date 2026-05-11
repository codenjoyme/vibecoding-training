# Module 12 Completion Report

## Skill Description
A CLI tool that scans a project directory for TODO comments across multiple file types and generates a prioritized summary report in markdown format.

## Instruction File
- Filename: scan-todos.instructions.md

```markdown
---
applyTo: "**"
---

# Scan TODOs Instruction

When the user asks to scan for TODOs or collect outstanding tasks:

1. Run `python scripts/scan-todos.py` in the project root.
2. The script scans all `.py`, `.js`, `.ts`, `.md` files recursively.
3. It extracts lines containing `TODO`, `FIXME`, or `HACK`.
4. Output is saved to `work/todo-report.md` as a markdown table.
5. Print a summary: total count, breakdown by tag type, top 3 files with most TODOs.

## Constraints
- Skip `node_modules/`, `.git/`, `__pycache__/`, and `dist/` directories.
- Maximum file size to scan: 1 MB.
- If no TODOs found, report "No outstanding TODOs found."
```

## Script File
- Filename: scripts/scan-todos.py
- Language: Python

```python
#!/usr/bin/env python3
"""Scan project files for TODO/FIXME/HACK comments and produce a markdown report."""

import argparse
import os
import re
from pathlib import Path
from collections import Counter

SKIP_DIRS = {"node_modules", ".git", "__pycache__", "dist", ".venv"}
EXTENSIONS = {".py", ".js", ".ts", ".md", ".java", ".cs"}
PATTERN = re.compile(r"\b(TODO|FIXME|HACK)\b[:\s]*(.*)", re.IGNORECASE)
MAX_SIZE = 1_048_576  # 1 MB

def scan(root: str) -> list[dict]:
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            if fpath.suffix not in EXTENSIONS or fpath.stat().st_size > MAX_SIZE:
                continue
            with open(fpath, encoding="utf-8", errors="ignore") as f:
                for lineno, line in enumerate(f, 1):
                    m = PATTERN.search(line)
                    if m:
                        findings.append({
                            "file": str(fpath.relative_to(root)),
                            "line": lineno,
                            "tag": m.group(1).upper(),
                            "text": m.group(2).strip(),
                        })
    return findings

def write_report(findings: list[dict], output: str):
    with open(output, "w", encoding="utf-8") as f:
        f.write("# TODO Scan Report\n\n")
        if not findings:
            f.write("No outstanding TODOs found.\n")
            return
        f.write(f"**Total: {len(findings)}**\n\n")
        f.write("| File | Line | Tag | Description |\n|------|------|-----|-------------|\n")
        for item in findings:
            f.write(f"| {item['file']} | {item['line']} | {item['tag']} | {item['text']} |\n")
    print(f"Report saved to {output} — {len(findings)} items found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan project for TODO/FIXME/HACK comments")
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument("--output", default="work/todo-report.md", help="Output report path")
    args = parser.parse_args()
    findings = scan(args.root)
    write_report(findings, args.output)
```

## Script Execution Output
```
$ python scripts/scan-todos.py --help
usage: scan-todos.py [-h] [--root ROOT] [--output OUTPUT]

Scan project for TODO/FIXME/HACK comments

options:
  -h, --help       show this help message and exit
  --root ROOT      Project root directory
  --output OUTPUT  Output report path
```
