"""Iterative-prompt CLI runner — thin wrapper around `copilot` for CLI runtime.

Pure Copilot CLI invocation. NO orchestration framework dependency, NO mediator,
NO worker pool. Just builds the right command line and runs it in the foreground.

Architecture:
  -p @<agent-file>             always points to `instructions/iterative-prompt/cli-agent.md`
                               (the executable instruction telling the CLI agent to run
                               the watcher loop). This is what makes Copilot CLI actually
                               start the loop instead of treating the helm-log as a
                               one-shot prompt.

  ITERATIVE_PROMPT_HELM_LOG    env var pointing to the user's helm-log file (the file
                               where ## UPD[N] blocks are written). The CLI agent reads
                               this env var on startup. By default the runner places the
                               helm-log next to the agent file (`<agent-dir>/cli.prompt.md`)
                               and auto-creates it from a template if missing. Override
                               with the positional argument or `--helm-log`.

Usage:
    python ./instructions/iterative-prompt/scripts/run_cli.py [helm-log]

Options (or env vars):
    --model <name>             COPILOT_MODEL                  default: claude-opus-4.6
    --continues <int>          COPILOT_AUTOPILOT_CONTINUES    default: 50  (0 = off)
    --copilot <path>           COPILOT_CLI                    default: search PATH
    --workspace <dir>          --add-dir target               default: cwd
    --agent <path>             override the agent instruction file (advanced)
    --no-auto-create           do NOT auto-create the helm-log file from template
    --print-cmd                print the resolved command and exit (no execution)

Exit codes:
    Same as `copilot` (forwarded). 127 if `copilot` not found.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_AGENT = Path("instructions/iterative-prompt/cli-agent.md")
DEFAULT_HELM_LOG_NAME = "cli.prompt.md"   # placed next to the agent file by default
DEFAULT_MODEL = "claude-opus-4.6"
DEFAULT_CONTINUES = 50

TEMPLATE = "<follow>\niterative-prompt/SKILL.md\n</follow>\n\n## UPD1\n\n"


def find_copilot(override: str | None) -> str | None:
    if override:
        p = Path(override)
        return str(p) if p.exists() else None
    env = os.environ.get("COPILOT_CLI")
    if env:
        p = Path(env)
        if p.exists():
            return str(p)
    found = shutil.which("copilot") or shutil.which("copilot.cmd")
    return found


def auto_create_prompt(prompt_path: Path) -> None:
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(TEMPLATE, encoding="utf-8")
    print(f"[run_cli] created helm-log from template: {prompt_path}", file=sys.stderr)


def build_command(
    copilot: str,
    agent_file: Path,
    workspace: Path,
    model: str,
    continues: int,
) -> list[str]:
    # The -p argument is the AGENT instruction file (executable identity), NOT the helm-log.
    # The helm-log is passed via ITERATIVE_PROMPT_HELM_LOG env var (read by the agent).
    agent_arg = f"@{agent_file.resolve()}"
    cmd: list[str] = []
    if sys.platform == "win32":
        cmd = ["cmd", "/c", copilot]
    else:
        cmd = [copilot]
    cmd += [
        "-p", agent_arg,
        "--add-dir", str(workspace.resolve()),
        "--allow-all",
        "--no-ask-user",
        "-s",
    ]
    if continues > 0:
        cmd += ["--autopilot", "--max-autopilot-continues", str(continues)]
    if model:
        cmd += ["--model", model]
    return cmd


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Iterative-prompt CLI runner (thin copilot wrapper).",
    )
    p.add_argument("prompt", nargs="?", default=None,
                   help=f"Helm-log prompt file. Default: <agent-dir>/{DEFAULT_HELM_LOG_NAME} "
                        f"(env ITERATIVE_PROMPT_HELM_LOG also overrides if positional is omitted).")
    p.add_argument("--helm-log", dest="prompt_opt", default=None,
                   help="Same as positional argument. Takes precedence over the positional one.")
    p.add_argument("--model",
                   default=os.environ.get("COPILOT_MODEL", DEFAULT_MODEL),
                   help=f"Model name (default: {DEFAULT_MODEL}, env COPILOT_MODEL)")
    p.add_argument("--continues", type=int,
                   default=int(os.environ.get("COPILOT_AUTOPILOT_CONTINUES", DEFAULT_CONTINUES)),
                   help=f"--max-autopilot-continues value, 0 disables autopilot "
                        f"(default: {DEFAULT_CONTINUES}, env COPILOT_AUTOPILOT_CONTINUES)")
    p.add_argument("--copilot", default=None,
                   help="Path to copilot binary (default: search PATH, env COPILOT_CLI)")
    p.add_argument("--workspace", default=".",
                   help="--add-dir target for copilot (default: cwd)")
    p.add_argument("--agent", default=str(DEFAULT_AGENT),
                   help=f"Agent instruction file passed via -p (default: {DEFAULT_AGENT})")
    p.add_argument("--no-auto-create", action="store_true",
                   help="Do NOT auto-create the helm-log file from template if missing")
    p.add_argument("--print-cmd", action="store_true",
                   help="Print resolved command and exit (no execution)")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    copilot = find_copilot(args.copilot)
    if not copilot:
        print("[run_cli] ERROR: copilot CLI not found. "
              "Install: npm install -g @anthropic-ai/copilot, "
              "or set COPILOT_CLI env var.", file=sys.stderr)
        return 127

    agent_file = Path(args.agent)
    if not agent_file.exists():
        print(f"[run_cli] ERROR: agent file not found: {agent_file}", file=sys.stderr)
        return 2

    # Resolve helm-log path with priority:
    #   1. --helm-log option, 2. positional argument, 3. ITERATIVE_PROMPT_HELM_LOG env,
    #   4. <agent-dir>/cli.prompt.md (default).
    helm_log_arg = args.prompt_opt or args.prompt or os.environ.get("ITERATIVE_PROMPT_HELM_LOG")
    if helm_log_arg:
        prompt_path = Path(helm_log_arg)
    else:
        prompt_path = agent_file.parent / DEFAULT_HELM_LOG_NAME

    if not prompt_path.exists():
        if args.no_auto_create:
            print(f"[run_cli] ERROR: helm-log file not found: {prompt_path}", file=sys.stderr)
            return 2
        auto_create_prompt(prompt_path)

    cmd = build_command(
        copilot=copilot,
        agent_file=agent_file,
        workspace=Path(args.workspace),
        model=args.model,
        continues=args.continues,
    )

    if args.print_cmd:
        print(" ".join(repr(a) if " " in a else a for a in cmd))
        return 0

    print(f"[run_cli] copilot:    {copilot}", file=sys.stderr)
    print(f"[run_cli] agent:      {agent_file}", file=sys.stderr)
    print(f"[run_cli] helm-log:   {prompt_path}  (via ITERATIVE_PROMPT_HELM_LOG)", file=sys.stderr)
    print(f"[run_cli] model:      {args.model}", file=sys.stderr)
    print(f"[run_cli] autopilot:  {args.continues} continues", file=sys.stderr)
    print(f"[run_cli] workspace:  {Path(args.workspace).resolve()}", file=sys.stderr)
    print("[run_cli] launching copilot (foreground, streaming stdout/stderr)...",
          file=sys.stderr)

    env = os.environ.copy()
    env["ITERATIVE_PROMPT_HELM_LOG"] = str(prompt_path.resolve())

    try:
        return subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
