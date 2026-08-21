"""Implementation of the ``skills ai-help`` command."""

from __future__ import annotations

from pathlib import Path

from ..lib.errors import CommandError


def run_ai_help() -> None:
    candidates = [
        Path(__file__).resolve().parents[1] / "SKILL-CLI.md",
        Path(__file__).resolve().parents[2] / "SKILL-CLI.md",
        Path.cwd() / "SKILL-CLI.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                print(candidate.read_text(encoding="utf-8"))
                return
            except OSError:
                continue
    raise CommandError(
        "Error: SKILL-CLI.md not found.\n"
        "See https://github.com/codenjoyme/apm-lite/blob/master/SKILL-CLI.md\n"
        "Or use `skills help` for basic usage."
    )
