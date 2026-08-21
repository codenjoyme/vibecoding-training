"""Exceptions shared by CLI libraries and command handlers."""


class ConfigError(RuntimeError):
    """Raised when the workspace configuration is missing or invalid."""


class ManifestError(RuntimeError):
    """Raised when a requested manifest cannot be loaded."""


class GitError(RuntimeError):
    """Raised when a git subprocess returns a non-zero status."""


class CommandError(RuntimeError):
    """Raised for an expected command-line error without a traceback."""
