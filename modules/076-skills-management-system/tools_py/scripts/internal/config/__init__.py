"""Workspace configuration package."""

from .config import CONFIG_FILE, REPO_SUB_DIR, Config, load, save

__all__ = ["CONFIG_FILE", "REPO_SUB_DIR", "Config", "load", "save"]
