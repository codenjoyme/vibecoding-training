#!/usr/bin/env python3
"""Entry point for the Python Skills CLI."""

import sys
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_ROOT.parent))

from scripts.cmd.root import execute


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    _configure_stdio()
    sys.exit(execute(sys.argv[1:]))


if __name__ == "__main__":
    main()
