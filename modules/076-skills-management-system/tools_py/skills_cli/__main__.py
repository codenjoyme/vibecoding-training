"""Executable entry point for ``python -m skills_cli``."""

import sys

from .commands.root import execute


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    _configure_stdio()
    sys.exit(execute(sys.argv[1:]))


if __name__ == "__main__":
    main()
