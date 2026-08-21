"""Command dispatch for the skills CLI."""

import sys
from typing import Sequence

from ..lib.errors import CommandError
from .help import print_help


def execute(args: Sequence[str]) -> int:
    """Dispatch command-line arguments and return a process exit code."""
    if not args or args[0] in {"help", "--help", "-h"}:
        print_help()
        return 0

    command = args[0]
    try:
        if command == "init":
            from .init import run_init

            run_init(list(args[1:]))
        elif command == "pull":
            from .pull import run_pull

            run_pull(list(args[1:]))
        elif command == "push":
            from .push import run_push

            run_push(list(args[1:]))
        elif command == "list":
            from .list import run_list

            run_list(list(args[1:]))
        elif command == "create":
            from .create import run_create

            run_create(list(args[1:]))
        elif command == "enable":
            from .toggle import run_enable

            run_enable(list(args[1:]))
        elif command == "disable":
            from .toggle import run_disable

            run_disable(list(args[1:]))
        elif command == "ai-help":
            from .aihelp import run_ai_help

            run_ai_help()
        elif command == "init-repo":
            from .initrepo import run_init_repo

            run_init_repo(list(args[1:]))
        else:
            print(f'Error: unknown command "{command}"', file=sys.stderr)
            print(file=sys.stderr)
            print_help()
            return 1
    except CommandError as exc:
        message = str(exc)
        if not message.startswith("Error:"):
            message = f"Error: {message}"
        print(message, file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
