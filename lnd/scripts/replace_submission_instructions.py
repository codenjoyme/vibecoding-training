"""Replace email-based submission instructions with autocheck-based ones in
every lnd/output/module-*.md file.

Per UPD13: keep the structure, but submission goes to an autocheck system
(currently being prepared in parallel) instead of an email reviewer. The
module-specific subject line is dropped because the autocheck does not need
the module name.

Idempotent: matches the original email pattern; once replaced, re-running has
no effect.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

# Match the email submission step (numbered item N) and its two sub-bullets:
#   N. Send [it/them/to]: `Oleksandr_Baglai@epam.com`
#      - Subject line: `Module XX ...`
#      - Attach/Paste/Include ...
EMAIL_BLOCK_RE = re.compile(
    r"^(?P<indent>\s*)(?P<num>[0-9]+\.)\s*Send (?:it |them |to |both files |both )?to:?\s*`Oleksandr_Baglai@epam\.com`\s*\n"
    r"(?:^(?P=indent)\s+-\s+Subject line:.*\n)?"
    r"(?:^(?P=indent)\s+-\s+(?:Attach|Paste|Include).*\n)?",
    re.MULTILINE,
)

# Heading line "**Submit your X for review:**".
HEADING_RE = re.compile(r"\*\*Submit your (.+?) for review:\*\*")

# "The reviewer will check ..." line.
REVIEWER_RE = re.compile(r"The reviewer will check")

REPLACEMENT_TEMPLATE = (
    "{indent}{num} Submit it to the `autocheck` system "
    "(the submission endpoint is being set up in parallel; "
    "instructions for accessing it will be shared once it is available).\n"
)


def transform(text: str) -> tuple[str, int]:
    changes = 0

    def repl_block(m: re.Match[str]) -> str:
        nonlocal changes
        changes += 1
        return REPLACEMENT_TEMPLATE.format(indent=m.group("indent"), num=m.group("num"))

    text2 = EMAIL_BLOCK_RE.sub(repl_block, text)

    text3, n = HEADING_RE.subn(r"**Submit your \1 for automated check:**", text2)
    changes += n

    text4, n = REVIEWER_RE.subn("The `autocheck` system will check", text3)
    changes += n

    return text4, changes


def main() -> int:
    files = sorted(OUTPUT_DIR.glob("module-*.md"))
    if not files:
        print("No module files found.")
        return 1

    total_changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        updated, count = transform(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            total_changed += 1
            print(f"  updated: {path.name} ({count} replacements)")
        else:
            print(f"  ok:      {path.name}")

    print(f"\nDone. {total_changed}/{len(files)} files modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
