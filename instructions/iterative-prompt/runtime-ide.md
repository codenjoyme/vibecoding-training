---
name: iterative-prompt-runtime-ide
description: IDE runtime for the iterative-prompt pattern — vscode_askQuestions (primary) + async watcher (fallback)
---

# Runtime: IDE (VS Code agent / Copilot Chat)

This file describes **how to keep the iterative-prompt loop alive inside a VS Code agent session**. The pattern itself (UPD/RESULT, atomic commits, file format) lives in [`SKILL.md`](./SKILL.md) — this is the runtime mechanics only.

## ⚠️ Critical: never end a turn without re-arming the loop

After every `### RESULT` is written and committed, re-arm the loop using **one of the two mechanisms** below. The **primary mechanism** is `vscode_askQuestions`. The watcher is a fallback for plugin versions that support terminal notifications (≥ 0.47).

---

## ✅ PRIMARY: vscode_askQuestions polling (recommended, plugin-version-independent)

Ask the user at the end of every turn:

```
vscode_askQuestions:
  question: "UPD[N] закрыт. Продолжить?"
  options: ["go", "стоп"]
```

When the answer is `go`:
1. Read the last 30 lines of the prompt file to find the new `## UPD[N+1]` block.
2. If a new block is found → run `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"`, retain its `hash`, process it (implement, write `### RESULT`, run `status.py --finish --started_from="<start-hash>"`, then commit).
3. If **no new block** is found (user pressed `go` but hasn't written a new UPD yet) → **auto-generate** a continuation block: append `## UPD[N+1]\n\nпродолжи. go\n` to the prompt file and process it as if the user wrote it. This keeps the loop alive without requiring the user to manually write a trivial "continue" request.
4. Ask again via `vscode_askQuestions`.

When the answer is a **question with options** (decision-point questions like "what to do next?"):
1. The user's selection (or freeText) **is the next UPD**. Auto-append to the prompt file: `## UPD[N+1]\n\n<user's answer text>\ngo\n`
2. Run `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"`, retain its `hash`, process it immediately (implement, write `### RESULT`, run `status.py --finish --started_from="<start-hash>"`, then commit).
3. Ask again via `vscode_askQuestions`.

### Re-poll when the user wants to write the next UPD themselves

If the user's answer is a **placeholder** — e.g. selects an option like "другое — впиши в UPD[N+1]", "I'll write it myself", "wait for my input", or freeText that explicitly says they will write the next UPD — **do NOT close the turn with "Жду UPD[N+1]"**. That breaks the loop.

Instead, run this re-poll algorithm at the end of every turn:

1. **Grep** the prompt file for the latest `^## UPD\d+` header (use `grep_search` with regex `^## UPD\d+`, take the highest N).
2. Read the lines from that header to end-of-file.
3. Decision:
   - **No `## UPD[K]` header newer than the last processed UPD** → call `vscode_askQuestions` again (same wheel: `["go", "стоп", "другое — впиши в UPD[N+1]"]`). The user may have written nothing yet; we re-poll.
   - **Header exists but body is empty** (only `## UPD[K]` line, no content under it) → same as above: re-poll via `vscode_askQuestions`.
   - **Header exists with body** → process it normally (implement → `### RESULT` → commit → ask again).
4. **Loop counter**: each re-poll iteration counts as a turn. Keep re-polling indefinitely as long as the user keeps answering anything other than `стоп`. The loop only terminates on explicit `стоп` / `stop` / `exit loop`.

**Never end a turn with a plain-text "waiting for UPD[N+1]" message and no `vscode_askQuestions` call.** That is the failure mode the user explicitly called out — the agent "falls asleep" and the human has to ping it manually. Re-poll is mandatory.

This eliminates the gap between "user picks an option" and "agent acts on it" — the user's choice is recorded in the prompt file as a proper UPD for traceability.

**Why this is primary:** works on any plugin version, no dependency on terminal notification mechanism or shell integration. Requires one explicit user interaction per UPD cycle.

**Loop stop condition:** user answers `стоп` or any message containing `stop` / `exit loop`.

### Recording user answers

When the user selects an option or provides freeText in `vscode_askQuestions`, copy their answer **verbatim** into the prompt file as the UPD body. Do not paraphrase, summarize, or reformat — the user's exact words become the UPD text.

### Language rules

- **RESULT blocks** in the prompt file: write in the same language the user used in the corresponding UPD.
- **`vscode_askQuestions` prompts** (question text, option labels): use the same language the user used in their last UPD.
- **Chat reflections** (thinking out loud in the chat panel): same language as the user's last UPD.
- **Production code, `.dark-factory/teams/` artifacts, instructions, factory files**: always English regardless of UPD language.

### Progress report before re-arming

Before calling `vscode_askQuestions` to re-arm the loop, write the compact post-commit report defined in [`SKILL.md`](./SKILL.md) as a preview. The tool's surrounding UI container may collapse this text after the operator answers, so it is not the durable visible receipt. This is the complete report shape:

```text
Request `UPD<N>` [<helm-file>:<upd-line>](<workspace-relative-helm-log>#L<upd-line>) closed.
Report `RESULT (UPD<N>)` [<helm-file>:<result-line>](<workspace-relative-helm-log>#L<result-line>).
Committed as:
   + In repository [<repo-folder>](<workspace-relative-repo-path>): `<sha>`, `<sha2>`
Tracked in [status.jsonl:<status-line>](<workspace-relative-status-log>#L<status-line>): `<start-hash>` : `<finish-hash>`
```

Build the helm-log links from the workspace-relative path and the 1-based `upd-line` and `result-lines` returned by `status.py --finish`; if there are several non-contiguous RESULT lines, emit a separate link for each. Count the physical finish-record line in `status.jsonl` after finish and use it as `status-line`. List the short commit hashes actually created by this UPD, grouped one line per touched repository. Translate the prose labels to the language of the processed UPD, but keep IDs, paths, and hashes unchanged. Do not re-tell what was done, which files changed, or what comes next — the detailed explanation remains in `### RESULT`.

Add an additional line only for something the file does **not** contain and the operator must act on now — a blocker, or a notice that `ITERATIVE_PROMPT_AUTOCOMMIT=false` left the changes uncommitted.

### Visible receipt after the question is answered

When `vscode_askQuestions` returns, start the next assistant response with the same compact report as ordinary text, followed by the exact question and answer:

```text
Request `UPD<N>` [<helm-file>:<upd-line>](<workspace-relative-helm-log>#L<upd-line>) closed.
Report `RESULT (UPD<N>)` [<helm-file>:<result-line>](<workspace-relative-helm-log>#L<result-line>).
Committed as:
   + In repository [<repo-folder>](<workspace-relative-repo-path>): `<sha>`, `<sha2>`
Tracked in [status.jsonl:<status-line>](<workspace-relative-status-log>#L<status-line>): `<start-hash>` : `<finish-hash>`
Re-arm question: `UPD<N> closed. Continue?` Answer: `<exact answer>`
```

This post-answer receipt must be the final text when the answer is `stop`, skipped, or a placeholder; do not put it before another `vscode_askQuestions` call. When the answer is `go`, emit the receipt first and then process the next UPD according to the normal re-poll rules. Translate the labels and question to the language of the processed UPD, preserve the exact answer text, and keep IDs, paths, hashes, and links unchanged.

### ⚠️ vscode_askQuestions must be the LAST and ONLY action of the turn

Empirical: when `vscode_askQuestions` is bundled in the same agent turn with other tool calls (especially long ones like `run_in_terminal` for commits, large file writes, multiple `read_file`s), the model API frequently returns an empty response — VS Code shows **"Sorry, no response was returned"** and the loop dies.

**Mandatory pattern for every turn that ends with re-arming:**

1. Do all work (reads, edits, terminal commands, **commit**) — these go in earlier tool batches.
2. Write the compact post-commit report preview to chat (plain text only, no tools).
3. Call `vscode_askQuestions` **alone** — no other tool in the same response.

If you forget and bundle them, hit "Try Again" (the retry usually succeeds) — but the discipline must hold turn-after-turn or the loop becomes unreliable on long sessions.

### Re-poll rules in detail (placeholder answers)

When the user picks an option that means "I'll write the next UPD myself" (e.g. `другая задача — впишу в UPD[N+1]`, `I'll write it`, `wait for my input`, or any equivalent freeText):

1. **Do NOT close the turn** with a chat message like "Жду содержимое UPD[N+1]" or "Waiting for your input". That breaks the loop — user is forced to ping manually.
2. **Immediately** run the grep-and-decide algorithm:
   - `grep_search` for `^## UPD\d+` in the prompt file, take the highest N.
   - If `N <= last_processed_upd` (no new header at all) → **re-poll**: call `vscode_askQuestions` again with the same wheel. The user is still typing.
   - If `N > last_processed_upd` but body is empty (only header line) → **re-poll** the same way. User started writing but didn't finish.
   - If `N > last_processed_upd` and body has content → process it as a normal UPD.
3. **Re-poll iterations are not failures** — they are the loop staying alive while the user thinks. Each re-poll is a fresh `vscode_askQuestions` call (one tool, one turn). Continue indefinitely until either:
   - User writes a UPD with body (process it), OR
   - User answers `стоп` / `stop` / `exit loop` (terminate loop).
4. **Never** end a placeholder-answer turn without `vscode_askQuestions`. The chat-text-only ending ("Жду UPD[N]…") is the explicit failure mode the user has called out multiple times.

> **Empirical:** the correct sequence is strictly: grep → if body present → process immediately (no `vscode_askQuestions`). `vscode_askQuestions` is called **only when body is absent**. Calling it before grepping is the anti-pattern — user may have already written the next UPD while the agent was processing the previous one.

---

## ⚙️ FALLBACK: async watcher (requires plugin ≥ 0.47)

> Use only when the user explicitly asks to switch to watcher-based auto-wake, OR when confirmed that plugin version ≥ 0.47 is installed.

Run via `run_in_terminal` with **`mode=async`**:

```powershell
python ./.dark-factory/bricks/iterative-prompt/scripts/watch_prompt.py .dark-factory/work/main.prompt.md
```

**Why `mode=async`, not `mode=sync`:** with `mode=sync` the agent's turn blocks until the command returns — by that time the platform has timed out the turn, no continuation fires. With `mode=async` the turn ends immediately, and when the watcher eventually exits VS Code fires the terminal notification → new agent turn starts.

**On terminal notification arrival:**

1. Use `get_terminal_output` with the terminal ID to see the watcher's stdout.
2. If stdout contains `NEW UPD ready` → run `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"`, retain its `hash`, read the prompt file and process the new `## UPD[N]`, write RESULT, run `status.py --finish --started_from="<start-hash>"`, then commit.
3. If exit code ≠ 0 → just restart the watcher (fallback Step H again).
4. After processing → write `### RESULT`, run `status.py --finish --started_from="<start-hash>"`, commit, and restart watcher.

**⚠️ Known limitation:** plugin version `0.44` does not deliver terminal notification as a new agent turn. Root cause confirmed in UPD182 — session `6989db14` (plugin `0.47.2026042905`) worked, session `df71bf15` (plugin `0.44.2026041004`) did not. Upgrade via: Extensions → GitHub Copilot Chat → Install Another Version → `0.47.2026042905`.

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
2. Run `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"`, retain its `hash`, and write the result as a `### RESULT` block inside the **active prompt file** (not chat-only).
3. Run `status.py --finish --started_from="<start-hash>"` before committing, then commit the changes.
4. Re-arm: use `vscode_askQuestions` (primary) or restart the watcher (fallback).

The only valid reason to stop the loop is an explicit `stop` / `exit loop`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent doesn't wake after watcher exits | Plugin version < 0.47 | Use `vscode_askQuestions` (primary mode) or upgrade plugin |
| Agent doesn't wake after watcher exits | Used `mode=sync` | Switch to `mode=async` |
| `Get-FileHash` / `PermissionError` crashes | Editor save lock (Windows) | Use Python watcher (has retries) |
| Watcher exits immediately | File already has ready UPD with `go` | Process it, then restart |
| Watcher never detects `go` | `go` is inside a sentence, not end-of-block | User must put `go` on its own line or as last word |
| Agent processes wrong UPD | Multiple unprocessed UPDs | Watcher finds last one without RESULT; agent processes all ready ones in order |
