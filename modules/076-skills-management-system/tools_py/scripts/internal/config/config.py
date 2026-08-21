"""Workspace configuration loading and persistence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..errors import ConfigError

CONFIG_FILE = Path("skills.json")
REPO_SUB_DIR = Path("instructions")


@dataclass
class Config:
    repo_url: str
    groups: list[str]
    extra_skills: list[str]
    excluded_skills: list[str]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Config":
        return cls(
            repo_url=str(raw.get("repo_url", "")),
            groups=_string_list(raw.get("groups")),
            extra_skills=_string_list(raw.get("extra_skills")),
            excluded_skills=_string_list(raw.get("excluded_skills")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "repo_url": self.repo_url,
            "groups": self.groups,
            "extra_skills": self.extra_skills,
            "excluded_skills": self.excluded_skills,
        }

    def repo_path(self) -> Path:
        return REPO_SUB_DIR


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def load() -> Config:
    try:
        raw_text = CONFIG_FILE.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ConfigError("not a skills workspace - run `skills init` first") from exc
    except OSError as exc:
        raise ConfigError(f"failed to read config: {exc}") from exc

    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"corrupted config ({CONFIG_FILE}): {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"corrupted config ({CONFIG_FILE}): expected a JSON object")
    return Config.from_dict(raw)


def save(cfg: Config) -> None:
    CONFIG_FILE.write_text(
        json.dumps(cfg.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
