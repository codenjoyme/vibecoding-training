#!/usr/bin/env python3
"""Deterministic trig-table CLI example (requires Python 3.9+)."""

import argparse
import json
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a trigonometric value table.")
    parser.add_argument("--start", type=int, required=True, help="Start angle in degrees.")
    parser.add_argument("--end", type=int, required=True, help="End angle in degrees.")
    parser.add_argument("--step", type=int, required=True, help="Step in degrees, must be > 0.")
    parser.add_argument(
        "--format",
        choices=("md", "json", "csv"),
        default="md",
        help="Output format.",
    )
    parser.add_argument("--output", help="Optional output file path.")
    args = parser.parse_args()

    if args.step <= 0:
        parser.error("--step must be greater than 0")
    if args.end < args.start:
        parser.error("--end must be greater than or equal to --start")

    return args


def generate_rows(start: int, end: int, step: int) -> list[dict[str, float]]:
    rows = []
    for degree in range(start, end + 1, step):
        radians = math.radians(degree)
        rows.append(
            {
                "degree": degree,
                "sin": round(math.sin(radians), 6),
                "cos": round(math.cos(radians), 6),
                "tan": round(math.tan(radians), 6),
            }
        )
    return rows


def to_markdown(rows: list[dict[str, float]]) -> str:
    lines = [
        "| degree | sin | cos | tan |",
        "|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['degree']} | {row['sin']} | {row['cos']} | {row['tan']} |")
    return "\n".join(lines)


def to_json(rows: list[dict[str, float]]) -> str:
    return json.dumps(rows, indent=2)


def to_csv(rows: list[dict[str, float]]) -> str:
    if not rows:
        return ""
    headers = ["degree", "sin", "cos", "tan"]
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(row[h]) for h in headers))
    return "\n".join(lines)


def render(rows: list[dict[str, float]], output_format: str) -> str:
    if output_format == "md":
        return to_markdown(rows)
    if output_format == "json":
        return to_json(rows)
    return to_csv(rows)


def main() -> None:
    args = parse_args()
    rows = generate_rows(args.start, args.end, args.step)
    content = render(rows, args.format)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content + "\n", encoding="utf-8")
        return

    print(content)


if __name__ == "__main__":
    main()
