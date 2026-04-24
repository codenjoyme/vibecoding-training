"""Build a single DOCX from all module markdown files in lnd/output/.

Usage:
    python lnd/build_docx.py

Requires: pypandoc (will auto-download pandoc binary if missing).
Output: lnd/output/all-modules.docx
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import pypandoc
except ImportError:
    print("pypandoc is not installed. Install with: pip install pypandoc")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Install with: pip install Pillow")
    sys.exit(1)


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output"
DOCX_PATH = OUTPUT_DIR / "all-modules.docx"
REFERENCE_DOCX = SCRIPT_DIR / "reference.docx"

# Shading color for inline `code` (light gray).
INLINE_CODE_SHADE = "EEEEEE"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Page text-area width used for image scaling. Default reference.docx uses
# Letter (8.5") with ~1.25" margins, leaving ~6.0" for content. We pick the
# largest source image and scale it to this width; every other image is then
# scaled by the same factor — this keeps the rendered text size on screenshots
# uniform across the whole document.
PAGE_TEXT_WIDTH_INCHES = 6.0
PANDOC_DEFAULT_DPI = 96

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


def _modify_styles_xml(styles_xml: bytes) -> bytes:
    """Add a background shading to the `VerbatimChar` character style so that
    inline `code` is visually highlighted in the rendered DOCX."""
    ET.register_namespace("w", W_NS)
    root = ET.fromstring(styles_xml)
    target = None
    for style in root.findall(f"{{{W_NS}}}style"):
        if style.get(f"{{{W_NS}}}styleId") == "VerbatimChar":
            target = style
            break
    if target is None:
        # Style not present in default reference — leave as-is.
        return styles_xml

    rpr = target.find(f"{{{W_NS}}}rPr")
    if rpr is None:
        rpr = ET.SubElement(target, f"{{{W_NS}}}rPr")
    for shd in rpr.findall(f"{{{W_NS}}}shd"):
        rpr.remove(shd)
    shd = ET.SubElement(rpr, f"{{{W_NS}}}shd")
    shd.set(f"{{{W_NS}}}val", "clear")
    shd.set(f"{{{W_NS}}}color", "auto")
    shd.set(f"{{{W_NS}}}fill", INLINE_CODE_SHADE)
    return ET.tostring(root, xml_declaration=True, encoding="UTF-8")


def ensure_reference_docx() -> Path:
    """Generate `lnd/reference.docx` with a shaded inline-code style.

    Always regenerates so the script remains the single source of truth.
    """
    pandoc_bin = pypandoc.get_pandoc_path()

    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        default_path = Path(tmp.name)

    try:
        with default_path.open("wb") as f:
            subprocess.run(
                [pandoc_bin, "--print-default-data-file=reference.docx"],
                check=True,
                stdout=f,
            )

        with zipfile.ZipFile(default_path, "r") as zin:
            with zipfile.ZipFile(REFERENCE_DOCX, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == "word/styles.xml":
                        data = _modify_styles_xml(data)
                    zout.writestr(item, data)
    finally:
        try:
            default_path.unlink()
        except OSError:
            pass

    return REFERENCE_DOCX


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


# Match a markdown image NOT already followed by a `{...}` Pandoc attribute.
_IMG_RE = re.compile(r"(!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\))(?!\{)")


def _image_pixel_width(rel_path: str, base_dir: Path) -> int | None:
    clean = rel_path.split("#", 1)[0].split("?", 1)[0]
    img_path = (base_dir / clean).resolve()
    if not img_path.is_file():
        return None
    try:
        with Image.open(img_path) as im:
            return int(im.size[0])
    except Exception:
        return None


def add_image_widths(md: str, base_dir: Path) -> str:
    """Append `{width="Npx"}` to every standalone image reference using a
    single shared scale factor: the largest image fills the page text width;
    smaller images shrink proportionally so on-screenshot text stays the same
    physical size in the rendered DOCX."""
    matches = list(_IMG_RE.finditer(md))
    widths: dict[str, int] = {}
    for m in matches:
        rel = m.group(2)
        if rel in widths:
            continue
        w = _image_pixel_width(rel, base_dir)
        if w is not None and w > 0:
            widths[rel] = w

    if not widths:
        return md

    max_px = max(widths.values())
    target_max_px = PAGE_TEXT_WIDTH_INCHES * PANDOC_DEFAULT_DPI
    scale = target_max_px / max_px
    print(
        f"  image scaling: largest source = {max_px}px wide, "
        f"target page width = {int(target_max_px)}px, scale = {scale:.3f}"
    )

    def repl(m: re.Match[str]) -> str:
        rel = m.group(2)
        if rel not in widths:
            return m.group(0)
        rendered = max(1, int(round(widths[rel] * scale)))
        return f'{m.group(1)}{{width="{rendered}px"}}'

    return _IMG_RE.sub(repl, md)


def main() -> int:
    if not OUTPUT_DIR.is_dir():
        print(f"Output dir not found: {OUTPUT_DIR}")
        return 1

    ensure_pandoc()
    ref_path = ensure_reference_docx()
    print(f"Reference docx: {ref_path}")

    files = collect_md_files()
    if not files:
        print("No module-*.md files found.")
        return 1

    print(f"Combining {len(files)} module files...")
    for p in files:
        print(f"  - {p.name}")

    combined_md = build_combined_markdown(files)
    combined_md = add_image_widths(combined_md, OUTPUT_DIR)

    # Write the combined markdown to a temp file so Pandoc can resolve image
    # paths relative to lnd/output (where img/ lives).
    tmp_md = OUTPUT_DIR / "_all-modules.tmp.md"
    tmp_md.write_text(combined_md, encoding="utf-8")

    extra_args = [
        "--toc",
        "--toc-depth=2",
        "--standalone",
        f"--resource-path={OUTPUT_DIR}",
        f"--reference-doc={REFERENCE_DOCX}",
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
