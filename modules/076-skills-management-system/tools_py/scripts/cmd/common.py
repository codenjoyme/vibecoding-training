"""Small helpers shared by command handlers."""

from __future__ import annotations

import re


def split_values(value: str) -> list[str]:
    return [part for part in re.split(r"[,\s]+", value.strip()) if part]
