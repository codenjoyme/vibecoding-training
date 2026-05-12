---
name: iterative-prompt-runtime-ide
description: IDE runtime for the iterative-prompt pattern — vscode_askQuestions (primary) + async watcher (fallback)
---

# Runtime: IDE (VS Code agent / Copilot Chat)

This file describes **how to keep the iterative-prompt loop alive inside a VS Code agent session**. The pattern itself (UPD/RESULT, atomic commits, file format) lives in [`SKILL.md`](./SKILL.md) — this is the runtime mechanics only.

## ⚠️ Critical: never end a turn without re-arming the loop

After every `### RESULT` is written and committed, re-arm the loop using **one of the two mechanisms** below. The **primary mechanism** is `vscode_askQuestions`. The watcher is a fallback for plugin versions that support terminal notifications (< 0.44).

> **Cross-IDE note:** VS Code has the built-in `vscode_askQuestions` tool. Cursor likely has a similar mechanism for asking structured questions — search for it in your Cursor agent tools. Other IDEs may have equivalents. If your IDE has such a tool, use it as the primary mechanism. If not, fall back to the async watcher below.

---

## ✅ PRIMARY: vscode_askQuestions polling (recommended, plugin-version-independent)

Ask the user at the end of every turn:

```
vscode_askQuestions:
  question: "UPD[N] closed. Continue?"
  options: ["go", "stop"]
```

The freeform text input field is always visible by default (`allowFreeformInput: true`). Do **NOT** add an "Other" option — it duplicates the built-in freeform input and clutters the UI. Several options (depend on context) + freeform field = these ways to respond, which is exactly right.

When the answer is `go`:
1. Read the last 30 lines of the prompt file to find the new `## UPD[N+1]` block.
2. If a new block is found → process it (implement, write `### RESULT`, commit).
3. If **no new block** is found (user pressed `go` but hasn't written a new UPD yet) → **auto-generate** a continuation block: append `## UPD[N+1]\n\ncontinue. go\n` to the prompt file and process it as if the user wrote it. This keeps the loop alive without requiring the user to manually write a trivial "continue" request.
4. Ask again via `vscode_askQuestions`.

When the answer is a **question with options** (decision-point questions like "what to do next?"):
1. The user's selection (or freeText) **is the next UPD**. Auto-append to the prompt file: `## UPD[N+1]\n\n<user's answer text>\ngo\n`
2. Process it immediately (implement, write `### RESULT`, commit).
3. Ask again via `vscode_askQuestions`.

This eliminates the gap between "user picks an option" and "agent acts on it" — the user's choice is recorded in the prompt file as a proper UPD for traceability.

**Why this is primary:** works on any plugin version, no dependency on terminal notification mechanism or shell integration. Requires one explicit user interaction per UPD cycle.

**Loop stop condition:** user answers `stop` or any message containing `stop` / `exit loop`.

### Recording user answers

When the user selects an option or provides freeText in `vscode_askQuestions`, copy their answer **verbatim** into the prompt file as the UPD body. Do not paraphrase, summarize, or reformat — the user's exact words become the UPD text.

### Language rules

- **RESULT blocks** in the prompt file: write in the same language the user used in the corresponding UPD.
- **`vscode_askQuestions` prompts** (question text, option labels): use the same language the user used in their last UPD.
- **Chat reflections** (thinking out loud in the chat panel): same language as the user's last UPD.
- **Production code, project artifacts, instructions**: always English regardless of UPD language.

### Progress report before re-arming

Before calling `vscode_askQuestions` to re-arm the loop, provide a brief progress report in the chat:
- What was done in the current UPD cycle (files changed, key outcomes)
- Current state (what's next, any blockers)
- Pending items if any (open questions)

This ensures the user has context before deciding whether to `go` or redirect.

---

## ⚙️ FALLBACK: async watcher (requires plugin < 0.44)

> Use only when the user explicitly asks to switch to watcher-based auto-wake, OR when confirmed that plugin version < 0.44 is installed.

Run via `run_in_terminal` with **`mode=async`**:

```powershell
python ./instructions/iterative-prompt/scripts/watch_prompt.py .github/work/main.prompt.md
```

**Why `mode=async`, not `mode=sync`:** with `mode=sync` the agent's turn blocks until the command returns — by that time the platform has timed out the turn, no continuation fires. With `mode=async` the turn ends immediately, and when the watcher eventually exits VS Code fires the terminal notification → new agent turn starts.

**On terminal notification arrival:**

1. Use `get_terminal_output` with the terminal ID to see the watcher's stdout.
2. If stdout contains `NEW UPD ready` → read the prompt file and process the new `## UPD[N]`.
3. If exit code ≠ 0 → just restart the watcher (fallback Step H again).
4. After processing → write `### RESULT`, commit, restart watcher.

**⚠️ Known limitation:** some plugin versions (e.g. `0.44`) do not deliver terminal notification as a new agent turn. If the watcher exits but the agent does not wake — switch to `vscode_askQuestions` (primary mode) or upgrade the plugin to ≥ `0.44`.

---

## Anti-drift refresh (every 30 UPD cycles)

Maintain an internal counter of processed UPDs. After every 30:

1. Re-read this file and [`SKILL.md`](./SKILL.md).
2. Re-read any other instruction files referenced via `<follow>` in the active prompt file's header.
3. Re-read any standing user rules previously stated in the conversation (e.g. "no commits", "respond in Russian").
4. Reset the counter.

This compensates for context drift during long-running sessions.

## Watcher resilience (fallback mode only)

If the watcher subprocess exits unexpectedly (empty output, non-zero exit, error) → **immediately restart it**. Do NOT pause, do NOT ask the user.

**User-interrupted watcher = "check the file now" signal.** If the user manually stops the watcher (Ctrl+C, exit code 130), treat it as a deliberate hint: **read the last 30 lines of the prompt file before restarting**. If a new `## UPD[N]` block ending with `go` is found, process it before restarting.

**Fallback (if Python is unavailable):** plain sleep-and-recheck loop with `Start-Sleep -Seconds 60` (Windows) or `sleep 60` (POSIX) in `mode=sync`, then re-read the file in the next turn.

## ⛔ Chat messages do NOT break the loop

If the user sends a chat message while the loop is running:

1. Apply the fix or instruction from the chat message.
2. Write the result as a `### RESULT` block inside the **active prompt file** (not chat-only).
3. Commit the changes.
4. Re-arm: use `vscode_askQuestions` (primary) or restart the watcher (fallback).

The only valid reason to stop the loop is an explicit `stop` / `exit loop`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent doesn't wake after watcher exits | Plugin version < 0.44 | Use `vscode_askQuestions` (primary mode) or upgrade plugin |
| Agent doesn't wake after watcher exits | Used `mode=sync` | Switch to `mode=async` |
| `Get-FileHash` / `PermissionError` crashes | Editor save lock (Windows) | Use Python watcher (has retries) |
| Watcher exits immediately | File already has ready UPD with `go` | Process it, then restart |
| Watcher never detects `go` | `go` is inside a sentence, not end-of-block | User must put `go` on its own line or as last word |
| Agent processes wrong UPD | Multiple unprocessed UPDs | Watcher finds last one without RESULT; agent processes all ready ones in order |
