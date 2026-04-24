"""Reformat image references inside lnd/output/module-*.md so that:

- Each "image-only" line becomes its own paragraph (blank line before and after).
- If the image belongs to a list item, it is indented to match the list-item
  continuation indent (matches the depth of nesting).
- Inline images (image inside a paragraph with text on the same line) are NOT
  touched — only standalone image lines are reformatted.
- Code-fenced regions (``` ... ```) are skipped entirely.

Idempotent: running twice is a no-op.

Usage:
    python lnd/format_md_images.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"

IMG_LINE_RE = re.compile(r"^(\s*)(!\[[^\]]*\]\([^)]+\))\s*$")
LIST_ITEM_RE = re.compile(r"^(\s*)((?:[0-9]+\.|[-*+]))\s+\S")
FENCE_RE = re.compile(r"^\s*```")


def compute_target_indent(prev_lines: list[str]) -> str:
    """Look back through already-emitted lines to determine how the image
    line should be indented."""
    for j in range(len(prev_lines) - 1, -1, -1):
        prev = prev_lines[j]
        if prev.strip() == "":
            continue
        lm = LIST_ITEM_RE.match(prev)
        if lm:
            item_indent = lm.group(1)
            marker = lm.group(2)
            cont = len(item_indent) + len(marker) + 1
            return " " * cont
        prev_indent_len = len(prev) - len(prev.lstrip(" "))
        return " " * prev_indent_len
    return ""


def process_text(text: str) -> str:
    lines = text.split("\n")

    # Mark lines that fall inside ``` code fences (so we leave them alone).
    in_code = False
    code_mask = [False] * len(lines)
    for i, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_code = not in_code
            code_mask[i] = True  # the fence line itself
            continue
        code_mask[i] = in_code

    new_lines: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not code_mask[i] and IMG_LINE_RE.match(line):
            m = IMG_LINE_RE.match(line)
            assert m is not None
            img = m.group(2)
            target_indent = compute_target_indent(new_lines)

            # Ensure blank line before.
            if new_lines and new_lines[-1].strip() != "":
                new_lines.append("")

            new_lines.append(target_indent + img)

            # Ensure blank line after.
            i += 1
            if i < len(lines) and lines[i].strip() != "":
                new_lines.append("")
            continue

        new_lines.append(line)
        i += 1

    return "\n".join(new_lines)


def main() -> int:
    if not OUTPUT_DIR.is_dir():
        print(f"Output dir not found: {OUTPUT_DIR}")
        return 1

    files = sorted(OUTPUT_DIR.glob("module-*.md"))
    if not files:
        print("No module-*.md files found.")
        return 1

    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        updated = process_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"  updated: {path.name}")
        else:
            print(f"  ok:      {path.name}")

    print(f"\nDone. {changed}/{len(files)} files modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
