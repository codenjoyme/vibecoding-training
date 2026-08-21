"""Git subprocess operations used by the skills CLI."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .errors import GitError


def run(directory: str | Path | None, *args: str) -> str:
    command = ["git", *args]
    try:
        result = subprocess.run(
            command,
            cwd=str(directory) if directory else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        raise GitError(f"git {' '.join(args)}: {exc}") from exc
    output = result.stdout.strip()
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)}: {output}")
    return output


def clone(source_url: str, target_dir: str | Path) -> None:
    target = Path(target_dir)
    target.parent.mkdir(parents=True, exist_ok=True)
    run(None, "clone", source_url, str(target))


def setup_sparse_checkout(repo_dir: str | Path, skills: list[str]) -> None:
    run(repo_dir, "sparse-checkout", "init", "--cone")
    directories = [".manifest", *[_git_path(skill) for skill in skills]]
    run(repo_dir, "sparse-checkout", "set", *directories)


def default_branch(repo_dir: str | Path) -> str:
    try:
        output = run(repo_dir, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    except GitError:
        return "master"
    return output.rsplit("/", 1)[-1] if "/" in output else output


def checkout_branch(repo_dir: str | Path, branch: str) -> None:
    run(repo_dir, "checkout", branch)


def pull(repo_dir: str | Path) -> None:
    branch = default_branch(repo_dir)
    try:
        checkout_branch(repo_dir, branch)
    except GitError as exc:
        raise GitError(f"checkout {branch}: {exc}") from exc
    run(repo_dir, "pull", "origin", branch)


def list_all_skills(repo_dir: str | Path) -> list[str]:
    output = run(repo_dir, "ls-tree", "--name-only", "-d", "HEAD")
    return sorted(
        line.strip()
        for line in output.splitlines()
        if line.strip() and not line.strip().startswith(".")
    )


def create_branch(repo_dir: str | Path, branch_name: str) -> None:
    try:
        run(repo_dir, "checkout", "-b", branch_name)
    except GitError:
        try:
            run(repo_dir, "branch", "-D", branch_name)
        except GitError:
            pass
        run(repo_dir, "checkout", "-b", branch_name)


def stage_and_commit(repo_dir: str | Path, skill_name: str) -> None:
    add_to_sparse_checkout(repo_dir, skill_name)
    skill_path = f"{_git_path(skill_name)}/"
    run(repo_dir, "add", skill_path)
    run(repo_dir, "commit", "-m", f"feat({skill_name}): update skill instructions")


def add_to_sparse_checkout(repo_dir: str | Path, skill_name: str) -> None:
    current = run(repo_dir, "sparse-checkout", "list").splitlines()
    normalized = _git_path(skill_name)
    if any(line.strip() == normalized for line in current):
        return
    run(repo_dir, "sparse-checkout", "add", normalized)


def push(repo_dir: str | Path, branch_name: str) -> None:
    run(repo_dir, "push", "origin", branch_name)
    try:
        checkout_branch(repo_dir, default_branch(repo_dir))
    except GitError:
        pass


def get_remote_url(repo_dir: str | Path) -> str:
    return run(repo_dir, "remote", "get-url", "origin")


def current_branch(repo_dir: str | Path) -> str:
    return run(repo_dir, "rev-parse", "--abbrev-ref", "HEAD")


@dataclass
class SkillInfo:
    description: str
    owner: str


def load_skill_info(repo_dir: str | Path, skill_name: str) -> SkillInfo | None:
    info_path = Path(repo_dir) / skill_name / "info.json"
    try:
        raw = json.loads(info_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            return SkillInfo(str(raw.get("description", "")), str(raw.get("owner", "")))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        pass

    try:
        output = run(repo_dir, "show", f"HEAD:{_git_path(skill_name)}/info.json")
        raw = json.loads(output)
        if isinstance(raw, dict):
            return SkillInfo(str(raw.get("description", "")), str(raw.get("owner", "")))
    except (GitError, json.JSONDecodeError, TypeError, ValueError):
        return None
    return None


def has_uncommitted_changes(repo_dir: str | Path, skill_name: str) -> bool:
    try:
        output = run(repo_dir, "status", "--porcelain", f"{_git_path(skill_name)}/")
    except GitError:
        return False
    return bool(output.strip())


def stash_skill_changes(repo_dir: str | Path, skill_name: str) -> None:
    run(
        repo_dir,
        "stash",
        "push",
        "-u",
        "-m",
        f"skills-cli: auto-stash for {skill_name}",
        "--",
        f"{_git_path(skill_name)}/",
    )


def _git_path(value: str) -> str:
    return value.replace("\\", "/")
