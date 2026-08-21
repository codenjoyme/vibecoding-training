"""Implementation of the ``skills enable`` and ``skills disable`` commands."""

from __future__ import annotations

import sys

from scripts.internal import config, gitops, manifest
from scripts.internal.errors import CommandError


def run_enable(args: list[str]) -> None:
    if not args or args[0] in {"--help", "-h"}:
        print_enable_help()
        return
    if args[0] == "group":
        if len(args) < 2:
            raise CommandError("Error: group name is required\nUsage: skills enable group <group-name>")
        _enable_group(args[1])
        return
    _enable_skill(args[0])


def run_disable(args: list[str]) -> None:
    if not args or args[0] in {"--help", "-h"}:
        print_disable_help()
        return
    force = "--force" in args
    filtered = [value for value in args if value != "--force"]
    if not filtered:
        raise CommandError("Error: skill or group name is required")
    if filtered[0] == "group":
        if len(filtered) < 2:
            raise CommandError("Error: group name is required\nUsage: skills disable group <group-name>")
        _disable_group(filtered[1], force)
        return
    _disable_skill(filtered[0], force)


def _enable_group(name: str) -> None:
    cfg = _load_config()
    if name in cfg.groups:
        raise CommandError(f'Group "{name}" is already enabled')
    cfg.groups.append(name)
    _save_config(cfg)
    print(f'✅ Group "{name}" enabled')
    _reapply_sparse_checkout(cfg)


def _disable_group(name: str, force: bool) -> None:
    cfg = _load_config()
    if name not in cfg.groups:
        raise CommandError(f'Group "{name}" is not currently enabled')
    cfg.groups = [group for group in cfg.groups if group != name]

    before_cfg = config.Config(
        cfg.repo_url,
        [*cfg.groups, name],
        list(cfg.extra_skills),
        list(cfg.excluded_skills),
    )
    before = _resolve_all_skills(before_cfg)
    after = _resolve_all_skills(cfg)
    after_set = set(after)
    dirty = [
        skill
        for skill in before
        if skill not in after_set
        and gitops.has_uncommitted_changes(config.REPO_SUB_DIR, skill)
    ]
    if dirty and not force:
        raise CommandError(
            f'Error: cannot disable group "{name}" - uncommitted changes in: {", ".join(dirty)}\n'
            "Commit or discard your changes first, or use --force to override."
        )
    if force:
        for skill in dirty:
            try:
                gitops.stash_skill_changes(config.REPO_SUB_DIR, skill)
                print(f'  ⚠ Stashed uncommitted changes for "{skill}" (use `git stash list` to review)')
            except Exception as exc:
                print(f'Warning: failed to stash "{skill}": {exc}', file=sys.stderr)

    _save_config(cfg)
    print(f'✅ Group "{name}" disabled')
    _reapply_sparse_checkout(cfg)


def _enable_skill(name: str) -> None:
    cfg = _load_config()
    if name in cfg.excluded_skills:
        cfg.excluded_skills = [skill for skill in cfg.excluded_skills if skill != name]
        _save_config(cfg)
        print(f'✅ Skill "{name}" re-enabled (removed from exclusion list)')
        _reapply_sparse_checkout(cfg)
        return
    if name in cfg.extra_skills:
        raise CommandError(f'Skill "{name}" is already enabled')
    cfg.extra_skills.append(name)
    _save_config(cfg)
    print(f'✅ Skill "{name}" enabled')
    _reapply_sparse_checkout(cfg)


def _disable_skill(name: str, force: bool) -> None:
    cfg = _load_config()
    if gitops.has_uncommitted_changes(config.REPO_SUB_DIR, name):
        if not force:
            raise CommandError(
                f'Error: cannot disable skill "{name}" - uncommitted local changes detected\n'
                "Commit or discard your changes first, or use --force to override."
            )
        try:
            gitops.stash_skill_changes(config.REPO_SUB_DIR, name)
            print(f'  ⚠ Stashed uncommitted changes for "{name}" (use `git stash list` to review)')
        except Exception as exc:
            print(f'Warning: failed to stash "{name}": {exc}', file=sys.stderr)

    cfg.extra_skills = [skill for skill in cfg.extra_skills if skill != name]
    if name in cfg.excluded_skills:
        raise CommandError(f'Skill "{name}" is already disabled')
    cfg.excluded_skills.append(name)
    _save_config(cfg)
    print(f'✅ Skill "{name}" disabled')
    _reapply_sparse_checkout(cfg)


def _load_config() -> config.Config:
    try:
        return config.load()
    except Exception as exc:
        raise CommandError(str(exc)) from exc


def _save_config(cfg: config.Config) -> None:
    try:
        config.save(cfg)
    except OSError as exc:
        raise CommandError(f"Error: {exc}") from exc


def print_enable_help() -> None:
    print(
        """Enable a group or individual skill in this workspace.

Usage:
  skills enable group <group-name>   Add a group to the workspace
  skills enable <skill-name>         Add an individual skill

Sparse checkout is re-applied automatically after enabling.

Examples:
  skills enable group security
  skills enable my-custom-skill
"""
    )


def print_disable_help() -> None:
    print(
        """Disable a group or individual skill in this workspace.

Usage:
  skills disable group <group-name>   Remove a group from the workspace
  skills disable <skill-name>         Exclude an individual skill

Flags:
  --force   Force disable even if there are uncommitted local changes

If the skill has uncommitted local changes, the command will refuse
to disable it. Use --force to override - changes will be stashed
automatically (use `git stash list` inside instructions/ to review).

Sparse checkout is re-applied automatically after disabling.

Examples:
  skills disable group security
  skills disable security-guidelines
  skills disable security-guidelines --force
"""
    )


def resolve_effective_groups(cfg: config.Config) -> list[str]:
    return list(dict.fromkeys(cfg.groups))


def apply_extra_and_excluded(resolved: list[str], cfg: config.Config) -> list[str]:
    skills = set(resolved)
    skills.update(cfg.extra_skills)
    skills.difference_update(cfg.excluded_skills)
    return sorted(skills)


def _resolve_all_skills(cfg: config.Config) -> list[str]:
    try:
        resolved = manifest.resolve_skills(config.REPO_SUB_DIR, resolve_effective_groups(cfg))
    except Exception:
        resolved = []
    return apply_extra_and_excluded(resolved, cfg)


def _reapply_sparse_checkout(cfg: config.Config) -> None:
    skills = _resolve_all_skills(cfg)
    print(f"-> Applying sparse checkout ({len(skills)} skill(s)) ...")
    try:
        gitops.setup_sparse_checkout(config.REPO_SUB_DIR, skills)
    except Exception as exc:
        print(f"Warning: sparse checkout failed: {exc}", file=sys.stderr)
        print("Run `skills init` to re-apply manually.", file=sys.stderr)
        return
    print("  ✓ Sparse checkout applied")
