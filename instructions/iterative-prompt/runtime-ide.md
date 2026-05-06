---
name: iterative-prompt-runtime-ide
description: IDE runtime for the iterative-prompt pattern — async watcher + terminal notification mechanism
---

# Runtime: IDE (VS Code agent / Copilot Chat)

This file describes **how to keep the iterative-prompt loop alive inside a VS Code agent session**. The pattern itself (UPD/RESULT, atomic commits, file format) lives in [`SKILL.md`](./SKILL.md) — this is the runtime mechanics only.

## ⚠️ Critical: never end a turn without re-arming the watcher

After every `### RESULT` is written and committed:

1. Launch the watcher in **`mode=async`** (see Step H below).
2. End your turn with a brief chat message (e.g. `Watcher running, жду UPD[N+1]`).
3. When the watcher exits, VS Code delivers `[Terminal <id> notification: command completed...]` as a synthetic user message → next turn starts automatically.

The only valid reason to stop is an explicit user instruction (`stop`, `exit loop`, `закрой сессию`).

## Step H — Wake-on-change-and-go watcher (canonical)

Run via `run_in_terminal` with **`mode=async`**:

```powershell
python ./instructions/iterative-prompt/scripts/watch_prompt.py .github/work/main.prompt.md
```

**Why `mode=async`, not `mode=sync`:** with `mode=sync` the agent's turn blocks until the command returns — by that time the platform has timed out the turn, no continuation fires. With `mode=async` the turn ends immediately, and when the watcher eventually exits VS Code fires the terminal notification → new agent turn starts.

**On terminal notification arrival:**

1. Use `get_terminal_output` with the terminal ID to see the watcher's stdout.
2. If stdout contains `NEW UPD ready` → read the prompt file and process the new `## UPD[N]`.
3. If exit code ≠ 0 → just restart the watcher (Step H again).
4. After processing → write `### RESULT`, commit, restart watcher.

## Step G — Anti-drift refresh (every 30 sleep cycles)

Maintain an internal counter of consecutive sleep cycles. After every 30 sleeps, before going back to Step H:

1. Re-read this file and [`SKILL.md`](./SKILL.md).
2. Re-read any other instruction files referenced via `<follow>` in the active prompt file's header.
3. Re-read any standing user rules previously stated in the conversation (e.g. "no commits", "respond in Russian").
4. Reset the counter.

This compensates for context drift during long-running sessions.

## Step I — Watcher resilience

If the watcher subprocess exits unexpectedly (empty output, non-zero exit, error) → **immediately restart it**. Do NOT pause, do NOT ask the user.

**User-interrupted watcher = "check the file now" signal.** If the user manually stops the watcher (Ctrl+C, exit code 130), treat it as a deliberate hint: **read the last 30 lines of the prompt file before restarting**. If a new `## UPD[N]` block ending with `go` is found, process it before restarting.

**Fallback (if Python is unavailable):** plain sleep-and-recheck loop with `Start-Sleep -Seconds 60` (Windows) or `sleep 60` (POSIX) in `mode=sync`, then re-read the file in the next turn.

## ⛔ Chat messages do NOT break the loop

If the user sends a chat message while the polling loop is running:

1. Apply the fix or instruction from the chat message.
2. Write the result as a `### RESULT` block inside the **active prompt file** (not chat-only).
3. Commit the changes.
4. Immediately restart the watcher (Step H).

The only valid reason to stop the loop is an explicit `stop` / `exit loop`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent doesn't wake after watcher exits | Used `mode=sync` | Switch to `mode=async` |
| `Get-FileHash` / `PermissionError` crashes | Editor save lock (Windows) | Use Python watcher (has retries) |
| Watcher exits immediately | File already has ready UPD with `go` | Process it, then restart |
| Watcher never detects `go` | `go` is inside a sentence, not end-of-block | User must put `go` on its own line or as last word |
| Agent processes wrong UPD | Multiple unprocessed UPDs | Watcher finds last one without RESULT; agent processes all ready ones in order |
