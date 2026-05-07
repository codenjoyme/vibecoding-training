---
name: iterative-prompt-runtime-cli
description: CLI runtime for the iterative-prompt pattern — Copilot CLI with --autopilot inside one long process
---

# Runtime: CLI (Copilot CLI in a terminal)

This file describes **how to run the iterative-prompt loop directly from a terminal** using the Copilot CLI (`copilot`) — no IDE required, no agent platform notifications. The pattern itself (UPD/RESULT, atomic commits, file format) lives in [`SKILL.md`](./SKILL.md).

## ⚠️ Critical differences from IDE runtime

| Aspect | IDE runtime | CLI runtime |
|--------|-------------|-------------|
| Watcher invocation | `mode=async` + terminal notifications | **blocking foreground subprocess inside one long agent turn** |
| Turn lifecycle | Many short turns, one per UPD | **ONE long turn that processes UPDs in a loop** |
| Wake mechanism | VS Code synthetic terminal-notification message | `--autopilot` continuation messages from the CLI itself |
| `mode=async` rules from [`runtime-ide.md`](./runtime-ide.md) | Apply | **Do NOT apply — they are platform-specific** |

In CLI runtime there is no inbound channel after launch. The agent **must not end the turn** between UPDs — once the process exits, nothing can wake it back up. `--autopilot --max-autopilot-continues N` keeps the model alive past natural turn-end points (such as `git commit`).

## How to run

### Quickstart (recommended)

```powershell
python ./instructions/iterative-prompt/scripts/run_cli.py [helm-log]
```

The positional `helm-log` argument is optional. Resolution order:

1. `--helm-log <path>` option (highest priority)
2. positional argument
3. `ITERATIVE_PROMPT_HELM_LOG` env var
4. **default: `<agent-file-dir>/cli.prompt.md`** (i.e. next to the agent file)

Defaults:
- `--model claude-opus-4.6` (override with env `COPILOT_MODEL` or `--model`)
- `--max-autopilot-continues 50` (override with env `COPILOT_AUTOPILOT_CONTINUES` or `--continues`)
- Auto-creates the helm-log file from a template if it doesn't exist (disable with `--no-auto-create`)
- Streams `copilot` stdout/stderr live to the terminal

### Manual invocation (no script)

The `-p @<file>` argument is the **agent instruction file** (executable identity), not the helm-log. Because Copilot CLI cannot reliably read environment variables from inside the model, the helm-log path must be **substituted directly into the agent prompt text** before launch. The wrapper script [`run_cli.py`](./scripts/run_cli.py) does this automatically: it reads [`cli-agent.md`](./cli-agent.md), replaces the `{{HELM_LOG}}` placeholder with the resolved absolute path, writes the result to a **temp file** (`$env:TEMP/iterative-prompt-cli-agent-XXXXXX.md`, auto-cleaned on exit — nothing in your repo), and passes that to `copilot`. It also tees copilot's stdout/stderr to `<helm-log-dir>/session.log` for a persistent record.

If you must run `copilot` by hand, do the same substitution yourself first:

```powershell
# 1. Substitute the placeholder into a temp file
$helm = (Resolve-Path .github/work/cli.prompt.md).Path
$agent = New-TemporaryFile | Rename-Item -NewName { $_.Name + '.md' } -PassThru
(Get-Content instructions/iterative-prompt/cli-agent.md -Raw).Replace('{{HELM_LOG}}', $helm) `
  | Set-Content $agent.FullName -Encoding UTF8

# 2. Launch copilot with the substituted file
copilot `
    -p "@$($agent.FullName)" `
    --add-dir "$PWD" `
    --allow-all --no-ask-user -s `
    --autopilot --max-autopilot-continues 50 `
    --model claude-opus-4.6

# 3. Cleanup
Remove-Item $agent.FullName
```

The agent file [`cli-agent.md`](./cli-agent.md) starts with an imperative `EXECUTE NOW` block that tells the model to read [`SKILL.md`](./SKILL.md) + this runtime, then run the watcher loop on the substituted helm-log path. Without an explicit agent file, Copilot CLI does not understand the `<follow>` tag (that's IDE-only) and treats the helm-log as a plain prompt.

## The CLI run loop (what the agent does inside the long turn)

1. **Bootstrap (once):**
   - Read [`SKILL.md`](./SKILL.md) for the pattern (UPD/RESULT, file format, atomic commits).
   - Read this file for the runtime rules.
   - The helm-log path is **already in the agent prompt** (substituted from `{{HELM_LOG}}` by the runner before launch). No env-var lookup needed.2. **Loop forever (single long turn — DO NOT END THE TURN BETWEEN ITERATIONS):**
   1. Run watcher BLOCKING:
      ```
      python ./instructions/iterative-prompt/scripts/watch_prompt.py <helm-log>
      ```
   2. Watcher exit code:
      - `0` → new UPD with `go` ready → process it (read prompt, implement, write `### RESULT`, atomic commit).
      - `2` → file missing → recreate from template, loop.
      - `130` → user Ctrl+C → check file then loop.
      - other → log and retry.
   3. **After commit, do NOT exit. Loop back to step 2.1.** `--autopilot` will hand control back so the model stays alive.

## Why `--autopilot` is required

Copilot CLI normally ends the turn after a clear completion point (e.g. a successful `git commit`). Without `--autopilot`, the process exits after the first UPD and no more UPDs are picked up. With `--autopilot --max-autopilot-continues N` the model can self-continue up to `N` times, which lets the watcher loop iterate.

A single value of `N=50` is enough for one work session. For long-running orchestration, set `N=999` or restart the CLI process whenever continues are exhausted.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| CLI process exits after first UPD | `--autopilot` flag missing | Add `--autopilot --max-autopilot-continues N` |
| CLI summarises the agent file and asks "what would you like to do?" | Agent file reads as documentation, not as a task | Put an imperative `EXECUTE NOW` block at the very top (see [`cli-agent.md`](./cli-agent.md)) |
| CLI just answers the first UPD message and exits | Passed the helm-log as `-p` instead of an agent file | Pass [`cli-agent.md`](./cli-agent.md) as `-p` (or use [`run_cli.py`](./scripts/run_cli.py) which handles substitution automatically) |
| CLI exits after 1–2 UPDs even with `--max-autopilot-continues 999` | Agent ran the watcher in a **background/named shell** (e.g. `shellId: watcher-loop`); the watcher's exit didn't feed back into the agent turn, so autopilot ran out of work and the CLI shut down | The watcher MUST be invoked as a **synchronous foreground tool call** that blocks until it returns. The current [`cli-agent.md`](./cli-agent.md) step 2.1 forbids backgrounding explicitly. If you customise the agent file, keep that rule. |
| CLI defaults to `cli.prompt.md` next to the agent file instead of the helm-log you wanted | The model cannot read env vars reliably; helm-log path must be **substituted into the prompt text** | Use [`run_cli.py`](./scripts/run_cli.py) (does substitution) or substitute `{{HELM_LOG}}` manually in [`cli-agent.md`](./cli-agent.md) before launch |
| Watcher returns immediately | `## UPD` already ends with `go` | Process it then loop |
| `copilot: command not found` | CLI not installed | `npm install -g @anthropic-ai/copilot` |
| 402 quota error | No or invalid token | Set `GH_TOKEN` to a fine-grained PAT with `Copilot Requests` permission |

## Concurrency

Multiple CLI runners on **different** prompt files (`cli-projectA.prompt.md`, `cli-projectB.prompt.md`) run safely in parallel. Multiple runners on the **same** prompt file are unsupported — they will race on the file and on the git index.
