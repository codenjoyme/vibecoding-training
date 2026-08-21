"""Implementation of the ``skills init`` command."""

from __future__ import annotations

import io
import os
import stat
import shutil
from contextlib import redirect_stdout
from pathlib import Path

from ..lib import config, gitops, manifest
from ..lib.errors import CommandError
from .common import split_values
from .toggle import apply_extra_and_excluded, resolve_effective_groups


def print_init_help() -> None:
    print(
        """Initialize skills workspace from a central repository.

Clones the skills repository, resolves skills for the specified groups,
and applies sparse checkout so only the needed skills are present.

If --groups is omitted, only _global.json skills are initialized.
Use `skills enable group <name>` later to add group-specific skills.

Usage:
  skills init --repo <url-or-path> [--groups <group1>[,<group2>...]] [group...]

Flags:
  --repo    URL or local path to the central skills repository (required)
  --groups  Groups to initialize (comma-separated or repeated flag; positional args also accepted; optional)

Examples:
  skills init --repo https://github.com/org/skills
  skills init --repo https://github.com/org/skills --groups backend
  skills init --repo ../skills-repo --groups backend,security
  skills init --repo ../skills-repo backend security
"""
    )


def _parse_args(args: list[str]) -> tuple[str, list[str], bool]:
    repo = ""
    groups: list[str] = []
    show_help = False
    index = 0
    while index < len(args):
        value = args[index]
        if value in {"--help", "-h"}:
            show_help = True
            index += 1
            continue
        if value == "--repo":
            if index + 1 < len(args):
                repo = args[index + 1]
                index += 2
                continue
        elif value.startswith("--repo="):
            repo = value.split("=", 1)[1]
            index += 1
            continue
        if value == "--groups":
            if index + 1 < len(args):
                groups.extend(split_values(args[index + 1]))
                index += 2
                continue
        elif value.startswith("--groups="):
            groups.extend(split_values(value.split("=", 1)[1]))
            index += 1
            continue
        if not value.startswith("--"):
            groups.append(value)
        index += 1
    return repo, groups, show_help


def run_init(args: list[str]) -> None:
    repo, groups, show_help = _parse_args(args)
    if show_help:
        print_init_help()
        return

    if not repo:
        try:
            existing = config.load()
        except Exception as exc:
            raise CommandError(
                "Error: --repo is required (no existing skills.json found)\n"
                + _help_text()
            ) from exc

        print("-> Re-initializing from existing skills.json ...")
        repo_dir = config.REPO_SUB_DIR
        if repo_dir.exists():
            print("-> Removing old instructions/ ...")
            try:
                shutil.rmtree(repo_dir, onerror=_remove_read_only)
            except OSError as exc:
                raise CommandError(f"Error: failed to remove instructions/: {exc}") from exc

        print(f"-> Cloning skills repo from {existing.repo_url} ...")
        try:
            gitops.clone(existing.repo_url, repo_dir)
        except Exception as exc:
            raise CommandError(f"Error: clone failed: {exc}") from exc
        print("  ✓ Cloned")

        effective_groups = resolve_effective_groups(existing)
        print(f"-> Resolving skills for groups: {', '.join(effective_groups)} ...")
        try:
            skills = manifest.resolve_skills(repo_dir, effective_groups)
        except Exception as exc:
            raise CommandError(f"Error: manifest resolution failed: {exc}") from exc
        skills = apply_extra_and_excluded(skills, existing)
        print(f"  ✓ Resolved {len(skills)} skill(s): {', '.join(skills)}")

        print("-> Applying sparse checkout ...")
        try:
            gitops.setup_sparse_checkout(repo_dir, skills)
        except Exception as exc:
            raise CommandError(f"Error: sparse checkout failed: {exc}") from exc
        print("  ✓ Sparse checkout applied")

        try:
            config.save(existing)
        except OSError as exc:
            raise CommandError(f"Error: failed to save config: {exc}") from exc
        print("\n✅ Skills workspace re-initialized!")
        print(f"   Skills:     {', '.join(skills)}")
        return

    if not groups:
        print("ℹ No --groups specified. Initializing with _global.json skills only.")
        print("  Use `skills enable group <name>` later to add group-specific skills.")

    if config.CONFIG_FILE.exists():
        raise CommandError(
            "Error: workspace already initialized (skills.json exists)\n"
            "Run `skills pull` to update, or delete skills.json and instructions/ to re-initialize."
        )

    print(f"-> Cloning skills repo from {repo} ...")
    try:
        gitops.clone(repo, config.REPO_SUB_DIR)
    except Exception as exc:
        raise CommandError(f"Error: clone failed: {exc}") from exc
    print("  ✓ Cloned")

    group_label = ", ".join(groups) if groups else "(none - global only)"
    print(f"-> Resolving skills for groups: {group_label} ...")
    try:
        skills = manifest.resolve_skills(config.REPO_SUB_DIR, groups)
    except Exception as exc:
        raise CommandError(f"Error: manifest resolution failed: {exc}") from exc
    print(f"  ✓ Resolved {len(skills)} skill(s): {', '.join(skills)}")

    print("-> Applying sparse checkout ...")
    try:
        gitops.setup_sparse_checkout(config.REPO_SUB_DIR, skills)
    except Exception as exc:
        raise CommandError(f"Error: sparse checkout failed: {exc}") from exc
    print("  ✓ Sparse checkout applied")

    cfg = config.Config(repo, groups, [], [])
    try:
        config.save(cfg)
    except OSError as exc:
        raise CommandError(f"Error: failed to save config: {exc}") from exc

    group_display = ", ".join(groups) if groups else "(none - global only)"
    print("\n✅ Skills workspace initialized!")
    print(f"   Repository: {repo}")
    print(f"   Groups:     {group_display}")
    print(f"   Skills:     {', '.join(skills)}")
    print("   Location:   instructions/\n")
    print("Your AI agent can now read skills from instructions/<skill-name>/SKILL.md")


def _help_text() -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print_init_help()
    return buffer.getvalue().rstrip()


def _remove_read_only(function, path: str, _exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    function(path)
