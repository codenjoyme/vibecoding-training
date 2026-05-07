"""Iterative-prompt CLI runner — thin wrapper around `copilot` for CLI runtime.

Pure Copilot CLI invocation. NO orchestration framework dependency, NO mediator,
NO worker pool. Just builds the right command line and runs it in the foreground.

Architecture:
  -p @<runtime-agent-file>     points to a generated copy of `cli-agent.md` written
                               to the OS temp directory with the helm-log path baked
                               in (placeholder `{{HELM_LOG}}` substituted with the
                               resolved absolute path before launch). The temp file is
                               auto-removed when the runner exits. This is what makes
                               Copilot CLI actually start the watcher loop on the right
                               file — the model cannot reliably read env vars, so the
                               path must be inside the prompt text.

  ITERATIVE_PROMPT_HELM_LOG    env var pointing to the user's helm-log file. Used by the
                               runner as one possible source of the helm-log path (along
                               with the positional argument and `--helm-log`). Also
                               forwarded to the child process for any subordinate scripts
                               that look for it. By default the runner places the helm-log
                               next to the agent file (`<agent-dir>/cli.prompt.md`) and
                               auto-creates it from a template if missing. Override with
                               the positional argument or `--helm-log`.

  Session log                  copilot's stdout/stderr are tee'd to `<helm-log-dir>/session.log`
                               so you have a persistent record of every CLI run. Use
                               `--no-log` to disable, `--log <path>` to override the location.

Usage:
    python ./instructions/iterative-prompt/scripts/run_cli.py [helm-log]

Options (or env vars):
    --model <name>             COPILOT_MODEL                  default: claude-opus-4.6
    --continues <int>          COPILOT_AUTOPILOT_CONTINUES    default: 50  (0 = off)
    --copilot <path>           COPILOT_CLI                    default: search PATH
    --workspace <dir>          --add-dir target               default: cwd
    --agent <path>             override the agent instruction file (advanced)
    --no-auto-create           do NOT auto-create the helm-log file from template
    --log <path>               session log path (default: <helm-log-dir>/session.log)
    --no-log                   disable session log
    --print-cmd                print the resolved command and exit (no execution)

Exit codes:
    Same as `copilot` (forwarded). 127 if `copilot` not found.
"""
from __future__ import annotations

import argparse
import atexit
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

DEFAULT_AGENT = Path("instructions/iterative-prompt/cli-agent.md")
DEFAULT_HELM_LOG_NAME = "cli.prompt.md"   # placed next to the agent file by default
DEFAULT_LOG_NAME = "session.log"          # placed next to the helm-log by default
DEFAULT_MODEL = "claude-opus-4.6"
DEFAULT_CONTINUES = 50
GENERATED_AGENT_PREFIX = "iterative-prompt-cli-agent-"
GENERATED_AGENT_SUFFIX = ".md"
HELM_LOG_PLACEHOLDER = "{{HELM_LOG}}"

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


def materialize_agent(agent_template: Path, helm_log: Path) -> Path:
    """Read the agent template, substitute {{HELM_LOG}} with the absolute helm-log
    path, and write to a temp file. Returns the temp file path.

    The temp file is registered for cleanup at process exit — it never lives in
    the repo. Generated fresh on every launch so it always reflects the latest
    helm-log.
    """
    content = agent_template.read_text(encoding="utf-8")
    if HELM_LOG_PLACEHOLDER not in content:
        print(f"[run_cli] WARNING: agent template {agent_template} has no "
              f"{HELM_LOG_PLACEHOLDER} placeholder — model may not know which "
              f"helm-log to watch.", file=sys.stderr)
    abs_helm_log = str(helm_log.resolve())
    rendered = content.replace(HELM_LOG_PLACEHOLDER, abs_helm_log)

    fd, tmp_name = tempfile.mkstemp(
        prefix=GENERATED_AGENT_PREFIX, suffix=GENERATED_AGENT_SUFFIX, text=True,
    )
    runtime_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(rendered)
    except Exception:
        runtime_path.unlink(missing_ok=True)
        raise

    def _cleanup() -> None:
        try:
            runtime_path.unlink(missing_ok=True)
        except Exception:
            pass
    atexit.register(_cleanup)
    return runtime_path


def run_with_tee(cmd: list[str], env: dict[str, str], log_path: Path | None) -> int:
    """Run cmd in a subprocess, streaming combined stdout/stderr to this process's
    stdout AND (if log_path given) appending each line to the log file with a
    timestamp header for the session.
    """
    if log_path is None:
        try:
            return subprocess.call(cmd, env=env)
        except KeyboardInterrupt:
            return 130

    log_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"\n{'=' * 72}\n"
        f"[run_cli] session start: {datetime.now().isoformat(timespec='seconds')}\n"
        f"[run_cli] cmd: {' '.join(repr(a) if ' ' in a else a for a in cmd)}\n"
        f"{'=' * 72}\n"
    )
    with log_path.open("a", encoding="utf-8", errors="replace") as logf:
        logf.write(header)
        logf.flush()
        try:
            proc = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        except FileNotFoundError as e:
            print(f"[run_cli] ERROR: failed to launch copilot: {e}", file=sys.stderr)
            return 127

        assert proc.stdout is not None
        try:
            for line in proc.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                logf.write(line)
                logf.flush()
            return proc.wait()
        except KeyboardInterrupt:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
            return 130
        finally:
            footer = (
                f"[run_cli] session end:   {datetime.now().isoformat(timespec='seconds')}\n"
            )
            logf.write(footer)
            logf.flush()


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
    p.add_argument("--log", dest="log_path", default=None,
                   help=f"Session log path (default: <helm-log-dir>/{DEFAULT_LOG_NAME})")
    p.add_argument("--no-log", action="store_true",
                   help="Disable session log (no tee)")
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

    # Materialize the agent prompt with the helm-log path baked in.
    runtime_agent = materialize_agent(agent_file, prompt_path)

    cmd = build_command(
        copilot=copilot,
        agent_file=runtime_agent,
        workspace=Path(args.workspace),
        model=args.model,
        continues=args.continues,
    )

    if args.print_cmd:
        print(" ".join(repr(a) if " " in a else a for a in cmd))
        return 0

    # Resolve session log path (None disables).
    log_path: Path | None = None
    if not args.no_log:
        if args.log_path:
            log_path = Path(args.log_path)
        else:
            log_path = prompt_path.parent / DEFAULT_LOG_NAME

    print(f"[run_cli] copilot:    {copilot}", file=sys.stderr)
    print(f"[run_cli] agent:      {agent_file}  →  {runtime_agent.name} (in TEMP, helm-log baked in, auto-cleanup)", file=sys.stderr)
    print(f"[run_cli] helm-log:   {prompt_path.resolve()}", file=sys.stderr)
    print(f"[run_cli] model:      {args.model}", file=sys.stderr)
    print(f"[run_cli] autopilot:  {args.continues} continues", file=sys.stderr)
    print(f"[run_cli] workspace:  {Path(args.workspace).resolve()}", file=sys.stderr)
    if log_path is not None:
        print(f"[run_cli] log:        {log_path.resolve()}", file=sys.stderr)
    else:
        print(f"[run_cli] log:        (disabled)", file=sys.stderr)
    print("[run_cli] launching copilot (foreground, streaming stdout/stderr)...",
          file=sys.stderr)

    env = os.environ.copy()
    env["ITERATIVE_PROMPT_HELM_LOG"] = str(prompt_path.resolve())

    return run_with_tee(cmd, env=env, log_path=log_path)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
