"""Implementation of the ``skills create`` command."""

from __future__ import annotations

from ..lib import config, gitops
from ..lib.errors import CommandError

SKILL_TEMPLATE = """# Skill: {name}

## Purpose

_Describe what this skill teaches or enables._

## Instructions

_Write the detailed instructions for the AI agent here._
"""

INFO_TEMPLATE = """{
  "description": "This skill provides _____. It can be used for _____. The main features include _____.",
  "owner": "Your_Name@domain.com"
}
"""


def print_create_help() -> None:
    print(
        """Create a new skill in the local instructions/ folder.

Usage:
  skills create <skill-name>

Creates:
  instructions/<skill-name>/SKILL.md   - skill instructions template
  instructions/<skill-name>/info.json  - skill metadata (description, owner)
"""
    )


def run_create(args: list[str]) -> None:
    if "--help" in args or "-h" in args:
        print_create_help()
        return
    positional = [value for value in args if not value.startswith("--")]
    if not positional:
        raise CommandError("Error: skill name is required\n" + _help_text())
    skill_name = positional[0]
    try:
        config.load()
    except Exception as exc:
        raise CommandError(str(exc)) from exc

    skill_dir = config.REPO_SUB_DIR / skill_name
    if skill_dir.exists():
        raise CommandError(f'Error: skill "{skill_name}" already exists at {skill_dir}')
    try:
        skill_dir.mkdir(parents=True)
        skill_path = skill_dir / "SKILL.md"
        info_path = skill_dir / "info.json"
        skill_path.write_text(SKILL_TEMPLATE.format(name=skill_name), encoding="utf-8")
        info_path.write_text(INFO_TEMPLATE, encoding="utf-8")
    except OSError as exc:
        raise CommandError(f"Error: failed to create skill: {exc}") from exc

    try:
        gitops.add_to_sparse_checkout(config.REPO_SUB_DIR, skill_name)
    except Exception:
        pass

    cfg = config.load()
    if skill_name not in cfg.extra_skills:
        cfg.extra_skills.append(skill_name)
        config.save(cfg)

    print(f'✅ Skill "{skill_name}" created at {skill_dir}')
    print(f"   -> {skill_path}")
    print(f"   -> {info_path}")
    print("\nEdit SKILL.md with your instructions, then use `skills push` to propose it.")


def _help_text() -> str:
    return """Create a new skill in the local instructions/ folder.

Usage:
  skills create <skill-name>"""
