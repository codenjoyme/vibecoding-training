#!/usr/bin/env python3
"""
extract_placeholders.py — Extract all <key> placeholder names from a DOCX template.

Prints one placeholder name per line (without angle brackets), in order of first
appearance. Handles placeholders split across multiple XML runs by scanning the
raw XML directly, so it catches everything python-docx would miss.

Usage:
    python extract_placeholders.py --template path/to/Template.docx
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path


def extract_placeholders(template_path: str) -> list:
    """Return ordered unique list of placeholder key names found in the DOCX."""
    template = Path(template_path)
    if not template.exists():
        print(f"Error: template not found: {template}", file=sys.stderr)
        sys.exit(1)

    with zipfile.ZipFile(str(template), "r") as zf:
        with zf.open("word/document.xml") as f:
            xml = f.read().decode("utf-8")

    # Placeholders appear as &lt;key&gt; in the XML (HTML-escaped)
    raw = re.findall(r"&lt;([^&<>]+)&gt;", xml)

    # Deduplicate while preserving order
    seen = set()
    keys = []
    for k in raw:
        if k not in seen:
            seen.add(k)
            keys.append(k)
    return keys


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract <placeholder> names from a DOCX template."
    )
    parser.add_argument(
        "--template",
        required=True,
        metavar="TEMPLATE.docx",
        help="Path to the .docx template file.",
    )
    args = parser.parse_args()

    keys = extract_placeholders(args.template)
    for key in keys:
        print(key)


if __name__ == "__main__":
    main()
