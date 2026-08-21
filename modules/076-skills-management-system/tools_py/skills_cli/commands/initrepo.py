"""Implementation of the ``skills init-repo`` command."""

from __future__ import annotations

from pathlib import Path

from ..lib.errors import CommandError

GLOBAL_JSON = """{
  "skills": [
    "skills-cli"
  ]
}
"""

GROUP1_JSON = """{
  "skills": [],
  "sub-configs": ["sub-group"]
}
"""

SUBGROUP_JSON = """{
  "skills": [],
  "sub-configs": []
}
"""

SKILLS_CLI_INFO = """{
  "description": "Skills CLI reference: commands, creating skills, IDE integration (VSCode/Copilot, Cursor, Claude Code).",
  "owner": "your-name@example.com"
}
"""


def print_initrepo_help() -> None:
    print(
        """Initialize a new skills repository with base structure.

Creates a folder with:
  .manifest/_global.json      - global skills config
  .manifest/group-1.json      - example group config
  .manifest/sub-group.json    - example sub-config
  skills-cli/                 - skill: CLI usage, creating skills, IDE integration

Usage:
  skills init-repo <folder-name>

Examples:
  skills init-repo my-skills-repo
  skills init-repo ../shared-skills
"""
    )


def run_init_repo(args: list[str]) -> None:
    if "--help" in args or "-h" in args:
        print_initrepo_help()
        return
    positional = [value for value in args if not value.startswith("--")]
    if not positional:
        raise CommandError("Error: folder name is required\n" + _help_text())
    folder = Path(positional[0])
    if folder.exists():
        raise CommandError(f'Error: folder "{folder}" already exists')

    print(f"-> Creating skills repository at {folder} ...")
    try:
        (folder / ".manifest").mkdir(parents=True)
        (folder / "skills-cli").mkdir()
        _write(folder / ".manifest" / "_global.json", GLOBAL_JSON)
        _write(folder / ".manifest" / "group-1.json", GROUP1_JSON)
        _write(folder / ".manifest" / "sub-group.json", SUBGROUP_JSON)
        _write(folder / "skills-cli" / "SKILL.md", _load_skill_cli_md())
        _write(folder / "skills-cli" / "info.json", SKILLS_CLI_INFO)
        _write(folder / ".gitignore", "# Skills repo .gitignore\n")
    except OSError as exc:
        raise CommandError(f"Error: {exc}") from exc

    print("  ✓ Files created")
    print(f"\n✅ Skills repository initialized at {folder}")
    print("\nNext steps:")
    print(f"  cd {folder}")
    print('  git init && git add . && git commit -m "init: skills repository"')
    print("  # Then push to your Git hosting")


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _load_skill_cli_md() -> str:
    candidates = [
    Path(__file__).resolve().parents[1] / "SKILL-CLI.md",
        Path(__file__).resolve().parents[2] / "SKILL-CLI.md",
        Path.cwd() / "SKILL-CLI.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return candidate.read_text(encoding="utf-8")
            except OSError:
                pass
    return "# Skills CLI\n\nSee SKILL-CLI.md in the skills-cli package for full reference.\n"


def _help_text() -> str:
    return """Initialize a new skills repository with base structure.

Usage:
  skills init-repo <folder-name>"""
