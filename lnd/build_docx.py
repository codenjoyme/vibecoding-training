"""Build a single DOCX from all module markdown files in lnd/output/.

Usage:
    python lnd/build_docx.py

Requires: pypandoc (will auto-download pandoc binary if missing).
Output: lnd/output/all-modules.docx
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import pypandoc
except ImportError:
    print("pypandoc is not installed. Install with: pip install pypandoc")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
DOCX_PATH = OUTPUT_DIR / "all-modules.docx"

# Files to skip (per user instruction in UPD2).
SKIP_FILES = {"module-02b-installing-claude-code-codemie.md"}

# Raw OpenXML page break — Pandoc passes this through into the .docx.
PAGE_BREAK = (
    "\n\n```{=openxml}\n"
    '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:r><w:br w:type="page"/></w:r></w:p>\n'
    "```\n\n"
)


def ensure_pandoc() -> None:
    """Make sure a pandoc binary is available; download if missing."""
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        print("Pandoc binary not found. Downloading...")
        pypandoc.download_pandoc()


def title_from_filename(stem: str) -> str:
    """Convert 'module-01-installing-vscode' -> 'Module 01 — Installing VSCode'."""
    m = re.match(r"^module-([0-9]+[a-z]?)-(.+)$", stem)
    if not m:
        return stem
    num, rest = m.group(1), m.group(2)
    words = [w.capitalize() for w in rest.split("-")]
    return f"Module {num} \u2014 {' '.join(words)}"


def collect_md_files() -> list[Path]:
    files = sorted(p for p in OUTPUT_DIR.glob("module-*.md"))
    return [p for p in files if p.name not in SKIP_FILES]


def strip_first_h1(text: str) -> str:
    """Remove the first H1 heading from a markdown body to avoid duplication
    with the synthetic title we add ourselves."""
    lines = text.splitlines()
    out = []
    removed = False
    for line in lines:
        if not removed and line.lstrip().startswith("# ") and not line.lstrip().startswith("##"):
            removed = True
            continue
        out.append(line)
    return "\n".join(out)


def build_combined_markdown(files: list[Path]) -> str:
    parts: list[str] = []
    for idx, path in enumerate(files):
        body = path.read_text(encoding="utf-8")
        body = strip_first_h1(body)
        title = title_from_filename(path.stem)
        if idx > 0:
            parts.append(PAGE_BREAK)
        parts.append(f"# {title}\n\n{body.strip()}\n")
    return "\n".join(parts)


def main() -> int:
    if not OUTPUT_DIR.is_dir():
        print(f"Output dir not found: {OUTPUT_DIR}")
        return 1

    ensure_pandoc()

    files = collect_md_files()
    if not files:
        print("No module-*.md files found.")
        return 1

    print(f"Combining {len(files)} module files...")
    for p in files:
        print(f"  - {p.name}")

    combined_md = build_combined_markdown(files)

    # Write the combined markdown to a temp file so Pandoc can resolve image
    # paths relative to lnd/output (where img/ lives).
    tmp_md = OUTPUT_DIR / "_all-modules.tmp.md"
    tmp_md.write_text(combined_md, encoding="utf-8")

    extra_args = [
        "--toc",
        "--toc-depth=2",
        "--standalone",
        f"--resource-path={OUTPUT_DIR}",
    ]

    try:
        pypandoc.convert_file(
            str(tmp_md),
            to="docx",
            format="gfm+raw_attribute",
            outputfile=str(DOCX_PATH),
            extra_args=extra_args,
        )
    finally:
        try:
            tmp_md.unlink()
        except OSError:
            pass

    print(f"OK -> {DOCX_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
