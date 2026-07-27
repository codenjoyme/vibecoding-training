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

**Scope:** `vscode_askQuestions` is used **only** to ask the user whether to continue or stop the loop between UPD cycles. It is **not** used for clarifying/domain questions about the task itself — those go into the helm-log file (see "Clarifying questions go into the helm-log" below).

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

When the answer is anything else (freeform text, or a message containing a redirect/new instruction): treat it as the next UPD. Auto-append to the prompt file: `## UPD[N+1]\n\n<user's answer text>\ngo\n`, process it immediately (implement, write `### RESULT`, commit), then ask again via `vscode_askQuestions`.

**Why this is primary:** works on any plugin version, no dependency on terminal notification mechanism or shell integration. Requires one explicit user interaction per UPD cycle.

**Loop stop condition:** user answers `stop` or any message containing `stop` / `exit loop`.

### Recording user answers

When the user replies via `vscode_askQuestions` (option or freeText), copy their answer **verbatim** into the prompt file as the next UPD body. Do not paraphrase, summarize, or reformat — the user's exact words become the UPD text.

## 📋 Clarifying questions go into the helm-log (not vscode_askQuestions)

When the user explicitly asks to be asked questions (e.g. "задай мне вопросы", "ask me questions", "what do you need to know before starting?") **within an UPD's work**, do **not** use `vscode_askQuestions` for that. Instead:

1. Write the questions directly into the `### RESULT (UPD[N])` block in the helm-log file — numbered, with recommended choices marked (e.g. "*рекомендую*" / "recommended"), same as any other RESULT content.
2. Ask the user to reply inside a new `## UPD[N+1]` block ending with `go`, same as any other update.
3. Commit as usual (this RESULT is the deliverable for that UPD — a set of questions is a valid outcome, not a placeholder).
4. Re-arm the loop via `vscode_askQuestions` (go/stop) as normal — that popup only asks "continue or stop", never repeats the domain questions.

This keeps clarifying questions in the same versioned, language-preserving artifact as everything else, rather than a transient UI popup that isn't recorded anywhere.

## 🔀 Mid-task vscode_askQuestions → intermediate RESULT

If, while working through a single UPD, the agent still ends up calling `vscode_askQuestions` for some ad-hoc confirmation (not a full clarifying-questions request — see above), the answer **must** be persisted immediately:

1. As soon as `vscode_askQuestions` returns an answer, append it as an **intermediate** result segment inside the current UPD block: `### RESULT (UPD[N]) — interim: <short topic>`, with the question asked and the user's verbatim answer.
2. Commit is optional at this point (do it if the intermediate state is meaningful on its own); otherwise continue working.
3. Continue the task. When the whole UPD is complete, write the **final** `### RESULT (UPD[N])` summarizing the full outcome (the interim segment can stay as history above it, or be folded into the final summary — do not delete it).

This ensures mid-task Q&A survives even if the session is interrupted or compacted before the UPD finishes.

### Language rules

- **`vscode_askQuestions` question text and option labels**, and **any clarifying questions written into the helm-log**: always the same language as the helm-log (i.e., the language of the user's most recent `## UPD` block).
- **`### RESULT` blocks** (including interim ones): same language as the corresponding UPD.
- **Internal reasoning / chat "thinking out loud"**: may be in English regardless of the helm-log's language, to save tokens — as long as it is not the actual question or RESULT text shown/recorded for the user.
- **Production code, project artifacts, instructions, script comments**: always English regardless of helm-log language.

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
