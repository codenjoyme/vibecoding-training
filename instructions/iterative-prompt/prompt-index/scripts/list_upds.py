#!/usr/bin/env python3
"""list_upds.py — compact line-number index of ## UPD[N] / ### RESULT blocks.

Scans a helm-log file (an iterative-prompt `*.prompt.md`, or any file that
follows the same `## UPD[N]` / `### RESULT` convention) and prints a
lightweight, plain-text index: block numbers, line ranges, done/pending
status, and (optionally) a short text preview. Nothing but the index is
printed — the model then uses `read_file` with the reported line ranges to
drill into any specific block it actually needs. This keeps huge (multi-
thousand-line) helm-logs out of the model's context by default.

No third-party dependencies — stdlib only.

Usage:
    python list_upds.py <path-to-prompt-file> [options]

Options:
    --last N        Only show the last N UPD blocks (applied after --pending).
    --pending       Only show UPD blocks that have no RESULT yet.
    --no-results    Do not print "+ RESULT (...)" sub-lines at all.
    --preview N     Max characters of preview text per block (default: 80).
                    Use 0 to omit preview text entirely (headers/ranges only).

Example output:

    File: /abs/path/to/main.prompt.md (52 total UPD blocks, showing 3)
    UPD blocks:
      - UPD50 (lines 1280-1288) [done] —
            "Фикс iterative prompt: убрать дублирующую опцию..."
        + RESULT (lines 1284-1288)
            "Модифицирован instructions/iterative-prompt/runtime-ide.md..."
      - UPD51 (lines 1290-1307) [done] —
            "Смотри есть файл .github/agents/iterative-prompt.agent.md..."
        + RESULT (lines 1298-1307)
            "Добавил в блок установки скила инструкцию..."
      - UPD52 (lines 1309-1318) [pending] —
            "Давай сделаем CLI в этот скил iterative prompt на питоне..."
"""

import argparse
import os
import re
import sys

UPD_RE = re.compile(r"^##\s+UPD(\d+)\b")
RESULT_RE = re.compile(r"^###\s+RESULT\b")


def parse_blocks(lines):
    """Return a list of UPD block dicts in file order.

    Each dict: {number, start (0-based), end (0-based, inclusive),
                results: [(start, end), ...]}
    """
    upd_starts = []
    for i, line in enumerate(lines):
        m = UPD_RE.match(line)
        if m:
            upd_starts.append((i, int(m.group(1))))

    result_starts = [i for i, line in enumerate(lines) if RESULT_RE.match(line)]

    blocks = []
    for idx, (start, number) in enumerate(upd_starts):
        end = (upd_starts[idx + 1][0] - 1) if idx + 1 < len(upd_starts) else len(lines) - 1
        block_results = [r for r in result_starts if start < r <= end]
        results = []
        for ridx, rstart in enumerate(block_results):
            rend = (block_results[ridx + 1] - 1) if ridx + 1 < len(block_results) else end
            results.append((rstart, rend))
        blocks.append({"number": number, "start": start, "end": end, "results": results})
    return blocks


def squeeze_text(raw_lines):
    """Join non-empty stripped lines into one compact single-line string."""
    parts = [ln.strip() for ln in raw_lines if ln.strip()]
    return " ".join(parts)


def truncate(text, limit):
    if limit <= 0 or not text:
        return ""
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def format_block(lines, block, preview_len, show_results):
    out = []
    status = "done" if block["results"] else "pending"
    upd_line1 = block["start"] + 1
    upd_line2 = block["end"] + 1
    out.append(f"  - UPD{block['number']} (lines {upd_line1}-{upd_line2}) [{status}] —")

    # Request text = everything between the UPD header and the first RESULT
    # header (or block end if there's no RESULT yet).
    req_end = block["results"][0][0] if block["results"] else block["end"] + 1
    req_lines = lines[block["start"] + 1:req_end]
    preview = truncate(squeeze_text(req_lines), preview_len)
    if preview:
        out.append(f'        "{preview}"')

    if show_results:
        for rstart, rend in block["results"]:
            r_line1 = rstart + 1
            r_line2 = rend + 1
            out.append(f"    + RESULT (lines {r_line1}-{r_line2})")
            r_body_lines = lines[rstart + 1:rend + 1]
            r_preview = truncate(squeeze_text(r_body_lines), preview_len)
            if r_preview:
                out.append(f'        "{r_preview}"')
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Compact line-number index of ## UPD[N] / ### RESULT blocks in a helm-log file.",
    )
    parser.add_argument("prompt_file", help="Path to the helm-log / *.prompt.md file to index.")
    parser.add_argument("--last", type=int, default=None, metavar="N",
                         help="Only show the last N UPD blocks.")
    parser.add_argument("--pending", action="store_true",
                         help="Only show UPD blocks that have no RESULT yet.")
    parser.add_argument("--no-results", action="store_true",
                         help='Do not print "+ RESULT (...)" sub-lines.')
    parser.add_argument("--preview", type=int, default=80, metavar="N",
                         help="Max characters of preview text per block (default: 80). 0 = no preview text.")
    args = parser.parse_args()

    if not os.path.isfile(args.prompt_file):
        print(f"error: file not found: {args.prompt_file}", file=sys.stderr)
        sys.exit(2)

    with open(args.prompt_file, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    all_blocks = parse_blocks(lines)
    blocks = all_blocks

    if args.pending:
        blocks = [b for b in blocks if not b["results"]]

    if args.last is not None:
        blocks = blocks[-args.last:] if args.last > 0 else []

    abs_path = os.path.abspath(args.prompt_file)
    print(f"File: {abs_path} ({len(all_blocks)} total UPD blocks, showing {len(blocks)})")
    print("UPD blocks:")
    for block in blocks:
        for out_line in format_block(lines, block, args.preview, not args.no_results):
            print(out_line)


if __name__ == "__main__":
    main()
