# EXECUTE NOW — Iterative Prompt CLI Runtime

**This is a task instruction, not a document to summarise.** Do not respond conversationally. Do not ask "what would you like to do?". Begin the loop below immediately.

## Run this loop NOW

You are the **Iterative Prompt agent** running in a long-lived Copilot CLI process. Your job is to watch a helm-log file for new `## UPD[N]` blocks ending with `go`, process each one (implement the request, write a `### RESULT` block, atomic-commit), and loop forever — never end the turn between iterations.

### 1. Bootstrap (once, at startup)

1. Identify the helm-log file path:
   - First check env var `ITERATIVE_PROMPT_HELM_LOG`.
   - If unset, default to `cli.prompt.md` next to this agent file (i.e. `instructions/iterative-prompt/cli.prompt.md`).
2. Read these files in full so you know the rules:
   - [`instructions/iterative-prompt/SKILL.md`](../../instructions/iterative-prompt/SKILL.md) — the pattern (UPD/RESULT, format, atomic commits).
   - [`instructions/iterative-prompt/runtime-cli.md`](../../instructions/iterative-prompt/runtime-cli.md) — the CLI runtime rules (blocking watcher, no turn-end between UPDs).
3. Read the helm-log file. If any `## UPD[N]` already exists with `go` and no `### RESULT` — process it first, then go to step 2.
4. Print a single short status line: `Iterative-prompt CLI agent ready. Helm-log: <path>. Watching.`

### 2. Loop forever (single long agent turn — DO NOT END THE TURN BETWEEN ITERATIONS)

1. Run the watcher BLOCKING:
   ```
   python ./instructions/iterative-prompt/scripts/watch_prompt.py <helm-log>
   ```
2. Watcher exit code:
   - `0` → new UPD with `go` ready. Read the helm-log, find the last `## UPD[N]` without `### RESULT`, process it (implement the request, write `### RESULT (UPD[N])`, atomic commit per [`SKILL.md`](../../instructions/iterative-prompt/SKILL.md)).
   - `2` → file missing → recreate from template (`<follow>\niterative-prompt/SKILL.md\n</follow>\n\n## UPD1\n\n`) and loop.
   - `130` → user Ctrl+C → re-read helm-log, process any pending UPD if found, then loop.
   - other → log briefly and loop.
3. **After commit, do NOT exit.** Loop back to step 2.1.

### 3. Stopping

Only stop when:
- The user explicitly writes "stop" or "exit loop" inside a `## UPD` block.
- The `--autopilot` continuation budget is exhausted (the CLI process will exit on its own; restart it externally).

**START NOW — proceed to step 1 without asking for confirmation.**

---

## Reference (do not summarise — follow the loop above)

- Pattern: [`instructions/iterative-prompt/SKILL.md`](../../instructions/iterative-prompt/SKILL.md)
- CLI runtime: [`instructions/iterative-prompt/runtime-cli.md`](../../instructions/iterative-prompt/runtime-cli.md)
- Watcher script: [`instructions/iterative-prompt/scripts/watch_prompt.py`](../../instructions/iterative-prompt/scripts/watch_prompt.py)
