"""Implementation of the ``skills pull`` command."""

from __future__ import annotations

from ..lib import config, gitops
from ..lib.errors import CommandError


def run_pull(args: list[str]) -> None:
    if "--help" in args or "-h" in args:
        print(
            """Update local skills from the remote repository.

Usage:
  skills pull
"""
        )
        return

    try:
        cfg = config.load()
    except Exception as exc:
        raise CommandError(str(exc)) from exc

    print("-> Pulling latest skills ...")
    try:
        gitops.pull(cfg.repo_path())
    except Exception as exc:
        raise CommandError(f"Error: pull failed: {exc}") from exc
    print("✅ Skills updated successfully")
