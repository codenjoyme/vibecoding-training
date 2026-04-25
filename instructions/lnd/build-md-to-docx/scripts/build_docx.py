"""Build a single DOCX from a list of markdown files.

Usage:
    python build_docx.py --output OUT.docx [options] FILE [FILE ...]

See instructions/lnd/build-md-to-docx/SKILL.md for full documentation.

Requires: pypandoc (will auto-download pandoc binary if missing) and Pillow.
"""
from __future__ import annotations

import argparse
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
DEFAULT_REFERENCE_DOCX = SCRIPT_DIR / "reference.docx"

# Shading color for inline `code` (light gray).
INLINE_CODE_SHADE = "EEEEEE"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Page text-area dimensions used for image-overflow diagnostics only.
PAGE_TEXT_WIDTH_INCHES = 13.0
PAGE_TEXT_HEIGHT_INCHES = 10.0
PANDOC_DEFAULT_DPI = 96

# Page physical size (landscape, custom 14×11") and margins (0.5" all sides),
# applied to reference.docx so wide screenshots are not auto-shrunk to page
# width by Word. Numbers are in twentieths of a point (1 inch = 1440).
PAGE_W_TWIPS = 14 * 1440
PAGE_H_TWIPS = 11 * 1440
PAGE_MARGIN_TWIPS = 720  # 0.5"

# Default uniform scale factor applied to every image's native pixel size.
# 1.0 = render at native pixel size (96 DPI in pandoc).
# 0.89 ≈ 108 DPI (calibrated empirically).
DEFAULT_SHARED_SCALE = 0.89

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
    """Add background shading to the `VerbatimChar` style so inline `code` is
    visually highlighted in the rendered DOCX."""
    ET.register_namespace("w", W_NS)
    root = ET.fromstring(styles_xml)
    target = None
    for style in root.findall(f"{{{W_NS}}}style"):
        if style.get(f"{{{W_NS}}}styleId") == "VerbatimChar":
            target = style
            break
    if target is None:
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


def _modify_document_xml(document_xml: bytes) -> bytes:
    """Set custom landscape page size + small margins on the section properties
    so wide images are not auto-shrunk by Word to fit a narrower page."""
    ET.register_namespace("w", W_NS)
    root = ET.fromstring(document_xml)
    body = root.find(f"{{{W_NS}}}body")
    if body is None:
        return document_xml
    sect = body.find(f"{{{W_NS}}}sectPr")
    if sect is None:
        return document_xml

    for tag in ("pgSz", "pgMar"):
        for el in sect.findall(f"{{{W_NS}}}{tag}"):
            sect.remove(el)

    pgsz = ET.SubElement(sect, f"{{{W_NS}}}pgSz")
    pgsz.set(f"{{{W_NS}}}w", str(PAGE_W_TWIPS))
    pgsz.set(f"{{{W_NS}}}h", str(PAGE_H_TWIPS))
    pgsz.set(f"{{{W_NS}}}orient", "landscape")

    pgmar = ET.SubElement(sect, f"{{{W_NS}}}pgMar")
    pgmar.set(f"{{{W_NS}}}top", str(PAGE_MARGIN_TWIPS))
    pgmar.set(f"{{{W_NS}}}right", str(PAGE_MARGIN_TWIPS))
    pgmar.set(f"{{{W_NS}}}bottom", str(PAGE_MARGIN_TWIPS))
    pgmar.set(f"{{{W_NS}}}left", str(PAGE_MARGIN_TWIPS))
    pgmar.set(f"{{{W_NS}}}header", "720")
    pgmar.set(f"{{{W_NS}}}footer", "720")
    pgmar.set(f"{{{W_NS}}}gutter", "0")

    return ET.tostring(root, xml_declaration=True, encoding="UTF-8")


def ensure_reference_docx(reference_path: Path) -> Path:
    """Generate a fresh reference.docx with shaded inline-code style and a
    custom landscape page size. Always regenerates so the script is the
    single source of truth."""
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

        reference_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(default_path, "r") as zin:
            with zipfile.ZipFile(reference_path, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == "word/styles.xml":
                        data = _modify_styles_xml(data)
                    elif item.filename == "word/document.xml":
                        data = _modify_document_xml(data)
                    zout.writestr(item, data)
    finally:
        try:
            default_path.unlink()
        except OSError:
            pass

    return reference_path


def title_from_filename(stem: str) -> str:
    """Convert 'module-01-installing-vscode' -> 'Module 01 — Installing Vscode'.

    For non-`module-*` filenames, capitalises hyphen-separated words and
    returns the result.
    """
    m = re.match(r"^module-([0-9]+[a-z]?)-(.+)$", stem)
    if m:
        num, rest = m.group(1), m.group(2)
        words = [w.capitalize() for w in rest.split("-")]
        return f"Module {num} \u2014 {' '.join(words)}"
    return " ".join(w.capitalize() for w in stem.split("-"))


def strip_first_h1(text: str) -> str:
    """Remove the first H1 heading from a markdown body to avoid duplication
    with a synthetic title."""
    lines = text.splitlines()
    out: list[str] = []
    removed = False
    for line in lines:
        if (
            not removed
            and line.lstrip().startswith("# ")
            and not line.lstrip().startswith("##")
        ):
            removed = True
            continue
        out.append(line)
    return "\n".join(out)


def build_combined_markdown(files: list[Path], use_synthetic_title: bool) -> str:
    parts: list[str] = []
    for idx, path in enumerate(files):
        body = path.read_text(encoding="utf-8")
        if idx > 0:
            parts.append(PAGE_BREAK)
        if use_synthetic_title:
            body = strip_first_h1(body)
            title = title_from_filename(path.stem)
            parts.append(f"# {title}\n\n{body.strip()}\n")
        else:
            parts.append(f"{body.strip()}\n")
    return "\n".join(parts)


# Match a markdown image NOT already followed by a `{...}` Pandoc attribute.
_IMG_RE = re.compile(r"(!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\))(?!\{)")


def _image_size(rel_path: str, base_dir: Path) -> tuple[int, int] | None:
    clean = rel_path.split("#", 1)[0].split("?", 1)[0]
    img_path = (base_dir / clean).resolve()
    if not img_path.is_file():
        return None
    try:
        with Image.open(img_path) as im:
            return (int(im.size[0]), int(im.size[1]))
    except Exception:
        return None


def add_image_widths(md: str, base_dir: Path, shared_scale: float) -> str:
    """Append `{width="Npx"}` to every standalone image reference, computed
    as `native_width_px * shared_scale`."""
    matches = list(_IMG_RE.finditer(md))
    sizes: dict[str, tuple[int, int]] = {}
    for m in matches:
        rel = m.group(2)
        if rel in sizes:
            continue
        s = _image_size(rel, base_dir)
        if s is not None and s[0] > 0 and s[1] > 0:
            sizes[rel] = s

    if not sizes:
        return md

    target_w_px = PAGE_TEXT_WIDTH_INCHES * PANDOC_DEFAULT_DPI
    target_h_px = PAGE_TEXT_HEIGHT_INCHES * PANDOC_DEFAULT_DPI
    over_w = sum(1 for w, _ in sizes.values() if w * shared_scale > target_w_px)
    over_h = sum(1 for _, h in sizes.values() if h * shared_scale > target_h_px)
    print(
        f"  image scaling: shared scale = {shared_scale}, "
        f"page area = {int(target_w_px)}x{int(target_h_px)}px, "
        f"images overflowing W/H: {over_w}/{over_h}"
    )

    def repl(m: re.Match[str]) -> str:
        rel = m.group(2)
        if rel not in sizes:
            return m.group(0)
        w, _ = sizes[rel]
        rendered_w_int = max(1, int(round(w * shared_scale)))
        return f'{m.group(1)}{{width="{rendered_w_int}px"}}'

    return _IMG_RE.sub(repl, md)


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build a single DOCX from a list of markdown files.",
    )
    p.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help="Markdown files to combine, in order.",
    )
    p.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination .docx file.",
    )
    p.add_argument(
        "--resource-path",
        type=Path,
        default=None,
        help="Folder Pandoc uses to resolve relative image paths. "
        "Defaults to the parent folder of the first input file.",
    )
    p.add_argument(
        "--reference-docx",
        type=Path,
        default=DEFAULT_REFERENCE_DOCX,
        help=f"Reference .docx template (default: {DEFAULT_REFERENCE_DOCX.name} "
        "next to this script).",
    )
    p.add_argument(
        "--shared-scale",
        type=float,
        default=DEFAULT_SHARED_SCALE,
        help=f"Uniform scale factor for image widths (default: {DEFAULT_SHARED_SCALE}).",
    )
    p.add_argument(
        "--no-toc",
        action="store_true",
        help="Skip the table of contents.",
    )
    p.add_argument(
        "--toc-depth",
        type=int,
        default=2,
        help="TOC heading depth (default: 2).",
    )
    p.add_argument(
        "--title-from-filename",
        action="store_true",
        help="Derive a synthetic H1 title from each filename and strip the "
        "existing first H1 from the file body.",
    )
    p.add_argument(
        "--skip",
        action="append",
        default=[],
        metavar="FILENAME",
        help="Skip an input by basename. Repeatable.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    skip_set = set(args.skip)
    files = [p for p in args.inputs if p.name not in skip_set]
    missing = [p for p in files if not p.is_file()]
    if missing:
        for p in missing:
            print(f"Input not found: {p}")
        return 2
    if not files:
        print("No input files after applying --skip.")
        return 1

    resource_path = args.resource_path or files[0].parent
    if not resource_path.is_dir():
        print(f"Resource path not found: {resource_path}")
        return 1

    output_path: Path = args.output.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ensure_pandoc()
    ref_path = ensure_reference_docx(args.reference_docx.resolve())
    print(f"Reference docx: {ref_path}")

    print(f"Combining {len(files)} files...")
    for p in files:
        print(f"  - {p}")

    combined_md = build_combined_markdown(files, args.title_from_filename)
    combined_md = add_image_widths(
        combined_md, resource_path.resolve(), args.shared_scale
    )

    tmp_md = resource_path.resolve() / "_build_docx_combined.tmp.md"
    tmp_md.write_text(combined_md, encoding="utf-8")

    extra_args = [
        "--standalone",
        f"--resource-path={resource_path.resolve()}",
        f"--reference-doc={ref_path}",
    ]
    if not args.no_toc:
        extra_args.insert(0, f"--toc-depth={args.toc_depth}")
        extra_args.insert(0, "--toc")

    try:
        pypandoc.convert_file(
            str(tmp_md),
            to="docx",
            format="commonmark_x+raw_attribute-fancy_lists",
            outputfile=str(output_path),
            extra_args=extra_args,
        )
    finally:
        try:
            tmp_md.unlink()
        except OSError:
            pass

    print(f"OK -> {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
