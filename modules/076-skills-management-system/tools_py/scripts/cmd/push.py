"""Implementation of the ``skills push`` command."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from scripts.internal import config, gitops
from scripts.internal.errors import CommandError
from .common import split_values


def _parse_args(args: list[str]) -> tuple[str, list[str], bool]:
    skill_name = ""
    groups: list[str] = []
    show_help = False
    index = 0
    collecting_groups = False
    while index < len(args):
        value = args[index]
        if value in {"--help", "-h"}:
            show_help = True
            break
        if value == "--groups":
            collecting_groups = True
            index += 1
            continue
        if value.startswith("--groups="):
            groups.extend(split_values(value.split("=", 1)[1]))
            collecting_groups = True
            index += 1
            continue
        if collecting_groups:
            if value.startswith("--"):
                collecting_groups = False
            else:
                groups.extend(split_values(value))
                index += 1
                continue
        if not value.startswith("--") and not skill_name:
            skill_name = value
        index += 1
    return skill_name, groups, show_help


def print_push_help() -> None:
    print(
        """Create a branch, commit local changes to a skill, and push for review.

Usage:
  skills push <skill-name> [--groups <group1> <group2> ...]

The command will:
  1. Create branch: feature/<skill-name>-update
  2. Stage all changes in instructions/<skill-name>/
  3. Commit with a conventional commit message
  4. (optional) Add skill to specified group manifests and commit manifest changes
  5. Push the branch to origin
  6. Print the Pull Request URL (for GitHub/GitLab remotes)

Flags:
  --groups  Add skill to specified group manifests (creates group file if not found)

Examples:
  skills push my-skill
  skills push my-skill --groups backend security
  skills push my-skill --groups backend,frontend

Note: when --groups is used, manifest changes are included in the same PR branch.
If a group manifest does not exist, it will be created with the skill as its first entry.
"""
    )


def _add_skill_to_group_manifest(repo_dir: Path, skill_name: str, group_name: str) -> bool:
    manifest_dir = repo_dir / ".manifest"
    manifest_file = manifest_dir / f"{group_name}.json"
    if manifest_file.exists():
        try:
            raw = json.loads(manifest_file.read_text(encoding="utf-8"))
            data = raw if isinstance(raw, dict) else {}
        except (OSError, json.JSONDecodeError):
            data = {}
        skills = data.get("skills")
        if not isinstance(skills, list):
            skills = []
        if skill_name in skills:
            print(f'  ℹ Skill "{skill_name}" already in group "{group_name}"')
            return False
    else:
        manifest_dir.mkdir(parents=True, exist_ok=True)
        data = {}
        skills = []
        print(f"  -> Creating new group manifest: {group_name}.json")

    data["skills"] = sorted([*skills, skill_name])
    data.setdefault("sub-configs", [])
    manifest_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return True


def run_push(args: list[str]) -> None:
    skill_name, groups, show_help = _parse_args(args)
    if show_help:
        print_push_help()
        return
    if not skill_name:
        raise CommandError(
            "Error: skill name is required\n"
            "Usage: skills push <skill-name> [--groups <group1> <group2> ...]"
        )

    try:
        cfg = config.load()
    except Exception as exc:
        raise CommandError(str(exc)) from exc
    repo_dir = cfg.repo_path()
    branch_name = f"feature/{skill_name}-update"

    print(f"-> Creating branch {branch_name} ...")
    try:
        gitops.create_branch(repo_dir, branch_name)
    except Exception as exc:
        raise CommandError(
            f"Error: failed to create branch: {exc}\n"
            "Tip: if the branch already exists, delete it with:\n"
            f"     git -C instructions branch -D {branch_name}"
        ) from exc
    print("  ✓ Branch created")

    print(f"-> Staging and committing changes in {skill_name}/ ...")
    try:
        gitops.stage_and_commit(repo_dir, skill_name)
    except Exception as exc:
        try:
            gitops.checkout_branch(repo_dir, gitops.default_branch(repo_dir))
        except Exception:
            pass
        raise CommandError(
            f"Error: commit failed: {exc}\n"
            f"Tip: make sure you have changes to commit in instructions/{skill_name}/"
        ) from exc
    print("  ✓ Changes committed")

    if groups:
        print(f"-> Adding skill to group manifest(s): {', '.join(groups)} ...")
        manifest_changed = False
        for group in groups:
            try:
                changed = _add_skill_to_group_manifest(repo_dir, skill_name, group)
            except OSError as exc:
                print(f"Error: failed to update {group}.json: {exc}", file=sys.stderr)
                changed = False
            if changed:
                manifest_changed = True
                print(f'  ✓ Added to "{group}"')
        if manifest_changed:
            try:
                gitops.add_to_sparse_checkout(repo_dir, ".manifest")
                gitops.run(repo_dir, "add", ".manifest/")
                gitops.run(
                    repo_dir,
                    "commit",
                    "-m",
                    f"feat({skill_name}): add to groups {', '.join(groups)}",
                )
                print("  ✓ Manifest changes committed")
            except Exception as exc:
                print(f"Warning: failed to commit manifest changes: {exc}", file=sys.stderr)

    print(f"-> Pushing branch {branch_name} ...")
    try:
        gitops.push(repo_dir, branch_name)
    except Exception as exc:
        try:
            gitops.checkout_branch(repo_dir, gitops.default_branch(repo_dir))
        except Exception:
            pass
        raise CommandError(f"Error: push failed: {exc}") from exc
    print("  ✓ Branch pushed")

    print(f'\n✅ Skill "{skill_name}" pushed for review')
    print(f"   Branch: {branch_name}")
    if groups:
        print(f"   Groups: {', '.join(groups)}")

    try:
        remote_url = gitops.get_remote_url(repo_dir)
        pr_url = _build_pr_url(remote_url, branch_name)
    except Exception:
        pr_url = ""
    if pr_url:
        print(f"   Create PR: {pr_url}")
    else:
        print("   (local repository - request a review from the skill owner)")
    print(f'\n⚠  Note: switched back to the main branch - skill "{skill_name}" may not be visible locally.')
    print("   After the PR is merged, run `skills pull` to get it back.")


def _build_pr_url(remote_url: str, branch_name: str) -> str:
    normalized = remote_url.strip()
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    normalized = re.sub(r"^git@github\.com:", "https://github.com/", normalized)
    normalized = re.sub(r"^ssh://git@github\.com/", "https://github.com/", normalized)
    normalized = re.sub(r"^git@gitlab\.com:", "https://gitlab.com/", normalized)
    normalized = re.sub(r"^ssh://git@gitlab\.com/", "https://gitlab.com/", normalized)
    if "github.com" in normalized:
        return f"{normalized}/compare/{branch_name}?expand=1"
    if "gitlab.com" in normalized:
        return f"{normalized}/-/merge_requests/new?merge_request%5Bsource_branch%5D={branch_name}"
    return ""
