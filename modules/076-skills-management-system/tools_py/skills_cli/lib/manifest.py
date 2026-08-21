"""Manifest loading and deterministic skill resolution."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .errors import ManifestError


def _read_json(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"manifest file not found: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid {path.name}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ManifestError(f"invalid {path.name}: expected a JSON object")
    return raw


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item]


def resolve_skills(repo_path: str | Path, groups: list[str]) -> list[str]:
    manifest_dir = Path(repo_path) / ".manifest"
    skill_set: set[str] = set()

    global_path = manifest_dir / "_global.json"
    if global_path.exists():
        global_manifest = _read_json(global_path)
        skill_set.update(_string_list(global_manifest.get("skills")))

    visited_configs: set[str] = set()

    def resolve_group(name: str, top_level: bool = False) -> None:
        if name in visited_configs:
            return
        visited_configs.add(name)

        path = manifest_dir / f"{name}.json"
        try:
            group_manifest = _read_json(path)
        except ManifestError:
            if top_level:
                raise ManifestError(f'group "{name}": manifest file not found: {name}.json')
            print(f'Warning: config "{name}" not found, skipping', file=sys.stderr)
            return

        skill_set.update(_string_list(group_manifest.get("skills")))
        for sub_config in _string_list(group_manifest.get("sub-configs")):
            resolve_group(sub_config)

    for group in groups:
        resolve_group(group, top_level=True)

    return sorted(skill_set)
