"""Implementation of the ``skills list`` command."""

from __future__ import annotations

import json

from ..lib import config, gitops, manifest
from ..lib.errors import CommandError
from .toggle import apply_extra_and_excluded, resolve_effective_groups


def print_list_help() -> None:
    print(
        """List all available skills in the repository.

Usage:
  skills list [--verbose] [--json]

Flags:
  --verbose  Show description and owner from info.json
  --json     Output skills as JSON array

Active skills (checked out in this workspace) are marked with ✅.
Other skills exist in the repo but are not part of your current groups.
"""
    )


def run_list(args: list[str]) -> None:
    if "--help" in args or "-h" in args:
        print_list_help()
        return

    verbose = "--verbose" in args
    json_output = "--json" in args
    try:
        cfg = config.load()
    except Exception as exc:
        raise CommandError(str(exc)) from exc

    repo_dir = cfg.repo_path()
    try:
        all_skills = gitops.list_all_skills(repo_dir)
    except Exception as exc:
        raise CommandError(f"Error: failed to list skills: {exc}") from exc

    groups = resolve_effective_groups(cfg)
    try:
        resolved = manifest.resolve_skills(repo_dir, groups)
    except Exception:
        resolved = []
    active = set(apply_extra_and_excluded(resolved, cfg))

    if json_output:
        items: list[dict[str, object]] = []
        for skill in all_skills:
            item: dict[str, object] = {"name": skill, "active": skill in active}
            info = gitops.load_skill_info(repo_dir, skill)
            if info:
                item["description"] = info.description
                item["owner"] = info.owner
            items.append(item)
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return

    print(f"Skills repository: {cfg.repo_url}")
    print(f"Groups:           {', '.join(cfg.groups)}\n")
    active_count = 0
    for skill in all_skills:
        if skill in active:
            print(f"  ✅ {skill}")
            active_count += 1
        else:
            print(f"  ○  {skill}")
        if verbose:
            info = gitops.load_skill_info(repo_dir, skill)
            if info:
                print(f"     {info.description}")
                print(f"     Owner: {info.owner}")
    print(f"\nActive: {active_count}  |  Total: {len(all_skills)}")
