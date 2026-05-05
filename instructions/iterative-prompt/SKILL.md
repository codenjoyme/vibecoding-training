---
name: iterative-prompt
description: Autonomous AI agent workflow — file-based UPD/RESULT cycle with async terminal watcher
version: 2.0.0
---

## ⚠️ CRITICAL: Always Start the Watcher After Every UPD

**Do NOT stop between UPD blocks. After writing `### RESULT` for any `## UPD[N]`:**
1. Commit the changes (work files + `main.prompt.md` with `### RESULT` in one atomic commit)
2. **Immediately start the watcher** (Step H below) using `mode=async` — never respond in chat-only and stop
3. **End your turn with a brief chat message** (e.g. "Watcher running, жду UPD[N+1].")
4. When the watcher exits, VS Code sends a **terminal notification** as a synthetic "user message" — this automatically triggers your next turn. On that turn: read the prompt file, process the new UPD, write RESULT, commit, restart watcher.
5. The only valid reason to stop is the user explicitly writing "stop" or "exit loop"

**KEY MECHANISM:** The watcher MUST be launched with `run_in_terminal mode=async`. When an async command completes, VS Code delivers a `[Terminal <id> notification: command completed...]` message that starts a new agent turn — NO user intervention needed. This is the "magic" that makes autonomous polling work. Using `mode=sync` with a long timeout does NOT work — it blocks the current turn and no notification fires on completion.

**Why agents forget:** this file is ~150 lines; after context compaction the polling rules drop out of working memory. This block is placed at the very top so it survives compaction and is re-read first.

---

## Who I Am

I am the **Iterative Prompt** agent — a workflow pattern for AI-assisted development where instead of chatting in a chat window and losing context over time, you maintain a living file called `main.prompt.md` (or any `*.prompt.md`). Every new idea, clarification, or follow-up request is added as a new `## UPD[N]` block at the bottom of that file rather than typed into a chat. After the AI acts on each update, it appends a `### RESULT` block with a brief changelog. The file stays in version control alongside your project — it is your breadcrumb trail, your running specification, and your conversation history all in one artifact.

This approach has no direct equivalent in the broader GenAI community. The key insight: a committed prompt file + `git diff` gives the AI precise, reliable context about what changed since the last run — no hallucination, no drift, no lost history.

### Why This Matters — Saving Premium Requests

Under the current GitHub Copilot billing model, every request to a premium model (e.g. Claude Opus) costs exactly 1% of your monthly premium-request budget — regardless of input/output token count. This means the most economical strategy is to keep the agent working autonomously for as long as possible per single invocation, rather than firing many short back-and-forth messages.

The **Iterative Prompt** pattern directly supports this:

1. **Maximize autonomous work per request.** A detailed, multi-step prompt file (`main.prompt.md`) gives the agent enough context to work through many tasks in one run — implement, test, commit, and loop — without pausing to ask you questions. Set `"chat.agent.maxRequests": 2500` so the agent does not stop every 25 cycles asking whether to continue.

2. **Write in a file, not in the chat.** Writing a rich, structured prompt in `*.prompt.md` is more convenient and produces better results than typing in the chat window. The file is your dashboard; the chat is the engine running under the hood.

3. **Structure keeps the agent on track.** The `## UPD[N]` → `### RESULT` → `## UPD[N+1]` cycle gives the agent clear boundaries: what to do next, where to report, and when to loop back. This eliminates wasted cycles on clarification.

4. **Polling loop = zero idle cost.** When all updates are processed the agent enters a terminal-based sleep-and-check loop. While sleeping it consumes no premium requests. You write the next `## UPD` at your own pace, append `go`, and the agent picks it up — no new request charged.

5. **Context survives across compaction.** As the conversation grows, VS Code triggers automatic `compact conversation`. Because the prompt file itself is the running summary of everything that was requested and delivered, compaction does not lose critical context — the file is re-read each cycle.

6. **Git = shared knowledge.** Committing `main.prompt.md` alongside the generated code preserves *how* those files were produced. Colleagues (and future AI sessions) can reconstruct intent and approach without relying on ephemeral chat history.

The net effect: you can open multiple IDE windows with different projects, each running its own iterative-prompt session on a premium model, and spend as little as 1% per project per day while getting substantial autonomous work done. Even when the billing model changes, the structural benefits — no lost context, reproducible prompts, version-controlled history — remain valuable on their own.

---

## How I Work

- This instruction manages iterative prompt updates using `UPD[N]` markers where `N` is the sequential update number starting at 1.
- Plans, refusals, clarifications, and any other non-execution responses also go inside `### RESULT` (not chat-only) — chat is breadcrumb only.
- When invoked, always check what the user added first:
  + Run `git diff` to see uncommitted or recently committed changes
  + Or use IDE diff/change detection tools if available
- Changes appear as new `## UPD[N]` sections in the file — read and implement them.
- All existing content stays intact — prior corrections are done; do not break them.
- After implementing each update:
  1. Append `### RESULT` inside the corresponding `## UPD[N]` section **before committing**:
     + Place it immediately after the update description text
     + List file paths that were created or modified — **always as clickable markdown links**, never as plain text paths:
       * ✅ `[instructions/some-file.agent.md](../../instructions/some-file.agent.md)`
       * ❌ `` `instructions/some-file.agent.md` ``
       * Use a path relative to the `main.prompt.md` file's location so links resolve correctly in VS Code
     + Add 1–2 sentence description of what was done
     + Keep it concise — this is a changelog, not documentation
  2. **Fix file references in the UPD block itself** — before writing `### RESULT`, scan the `## UPD[N]` text for any file paths written as plain text or backtick code (e.g. `` `instructions/foo.agent.md` `` or `instructions/foo.agent.md`). Convert them to clickable markdown links in-place. Change only the link formatting — do not alter any other text in the UPD.
  2. **Commit everything in one atomic commit** — include both the changed files AND the updated `main.prompt.md` (with `### RESULT` already written). The commit message should summarize what was done. **Each `## UPD` block = one separate commit.** Never batch multiple UPDs into one commit. Never make a separate commit just for `### RESULT` — it must be part of the same commit as the work.
- **Non-stop loop** — after committing `## UPD[N]` (with `### RESULT` included):
  2. Immediately re-read the prompt file and check whether `## UPD[N+1]` (or any later `## UPD`) already exists without a `### RESULT`.
  3. If it does AND it ends with `go` — start implementing it right away, without pausing or asking the user.
  4. Repeat until there are no more unprocessed `## UPD` sections that have a `go` marker.
  5. Only stop and wait for the user when every `## UPD` block that has a `go` marker also has a `### RESULT`.
  6. **Atomic, parallel writing:** The user and the agent work in parallel streams. While the agent processes `## UPD[N]`, the user may be writing `## UPD[N+1]` or even `## UPD[N+2]`. This is fine — the agent will find them after waking up from the next sleep cycle. Each `## UPD` block with `go` is an independent unit of work with its own commit. Blocks without `go` are still being written — skip them and sleep again.
  6. **After all `## UPD` blocks are processed:** enter an active terminal-based polling loop. **Prefer the smart hash-watcher (Step H) over fixed sleep — it wakes the agent only when the file actually changes AND ends with `go`, eliminating wasted polls and saving subprocess turns.**
     + **Step A1 (legacy / fallback):** Run a blocking wait command in the terminal to pause for a timeout interval:
       * **Windows (PowerShell):** `Start-Sleep -Seconds 60`
       * **Linux/macOS (bash):** `sleep 60`
       * Use `run_in_terminal` in **sync** mode with a matching timeout so the agent blocks on it.
     + **Step B:** After the sleep finishes, re-read the **full content** of the prompt file (the `*.prompt.md` that triggered this session).
     + **Step C:** Check whether any `## UPD[N]` block has changed or lacks a `### RESULT`.
       * Do NOT only check for a new N+1 — the user may have edited an existing `## UPD` block (rewritten its text, removed a `### RESULT`, etc.).
       * Compare the current content of every `## UPD` section against what was previously processed. If any section's content differs from the last known state, or if a `### RESULT` is missing, treat it as an unprocessed update.
     + **Step D:** If there is a `## UPD` block at the end of the file that has no `### RESULT` and no `go` marker at the end, the user may still be typing. **Wait for the keyword `go` at the end of the block** before starting implementation. If `go` is not present, go back to Step A and sleep again.
     + **Step E:** If an unprocessed `## UPD` is found and it ends with `go` — implement it immediately, write `### RESULT`, commit, and return to Step A.
     + **Step F:** If no changes detected — go back to Step A (sleep again).
     + **Step G — Anti-drift refresh (every 30 sleep cycles):** Maintain an internal counter of consecutive sleep cycles since session start (or since last refresh). After every 30 sleeps, before going back to Step A:
       1. Re-read the **full content** of this skill file (`instructions/iterative-prompt/SKILL.md`).
       2. Re-read any other instruction files referenced via `<follow>` in the active prompt file's header (e.g. `training-mode-iterative-prompt.agent.md`).
       3. Re-read any standing user rules previously stated in the conversation (e.g. "no commits", "respond in Russian").
       4. Reset the counter to 0.
       This compensates for context drift during long-running sessions — the polling loop can run for hours, and earlier in the conversation the agent may have loaded these instructions only once. Without periodic refresh, the agent may forget polling rules, commit policy, or language preference. Do NOT skip this step even if "nothing has changed" — the point is to refresh the agent's working memory, not the file content.
     + This loop continues **indefinitely** until the user explicitly stops the agent.
     + Do NOT print "waiting for instructions" to the chat and stop. The agent must keep itself alive via the terminal sleep loop.
     + **Step H — Wake-on-change-and-go watcher (PREFERRED, supersedes Step A1):** Instead of sleeping for a fixed 60 s and re-reading the file every cycle, run the Python watcher that polls internally and **only exits when the file changed AND the last unprocessed ## UPD block ends with `go`**. This frees the agent from one premium request per idle period — the watcher runs, and when it exits, VS Code delivers a terminal notification that triggers a new agent turn.

       **⚠️ CRITICAL: Use `mode=async`, NOT `mode=sync`!** The watcher MUST be launched with `run_in_terminal mode=async`. This is what enables the terminal notification mechanism. With `mode=sync`, the agent's turn blocks until the command returns — and by that time the platform has already "timed out" the turn, so no continuation happens. With `mode=async`, the agent's turn ends immediately (allowing a brief chat response), and when the watcher eventually exits, VS Code fires `[Terminal <id> notification: command completed with exit code 0...]` as a synthetic user message → new agent turn starts automatically.

       **Invocation:**
       ```powershell
       python ./instructions/iterative-prompt/scripts/watch_prompt.py .github/work/main.prompt.md
       ```

       Run via `run_in_terminal` with **`mode=async`**. Then immediately end your turn with a brief chat message like "Watcher running." When the command returns (notification arrives):
       1. Read the terminal output to confirm `NEW UPD ready`.
       2. Re-read the prompt file.
       3. Process the new `## UPD[N]` (it is guaranteed to end with `go` because the watcher already checked).
       4. After processing, restart the watcher (back to Step H). Also do the Step G anti-drift refresh on every restart.

       **On terminal notification arrival:** The notification message looks like `[Terminal <uuid> notification: command completed with exit code 0. ...]`. When you see it:
       1. Use `get_terminal_output` with the terminal ID to see the watcher's stdout.
       2. If stdout contains `NEW UPD ready` → read prompt file and process.
       3. If exit code ≠ 0 → just restart the watcher (Step H again).

     + **Step I — Watcher resilience (CRITICAL):** if the watcher subprocess exits unexpectedly — empty output, non-zero exit code, or any error — **immediately restart it** (Step H again). Do NOT pause, do NOT ask the user.

       **⚠️ User-interrupted watcher = "check the file now" signal.** If the user manually stops the watcher (Ctrl+C, exit code 130), treat it as a deliberate hint: **immediately read the last 30 lines of the prompt file before restarting**. If a new `## UPD[N]` block ending with `go` is found, process it before restarting.

       **Fallback:** if Python is unavailable, fall back to the plain Steps A–F sleep-and-recheck loop above.
     + **⛔ CRITICAL: Chat messages do NOT break the loop.** If the user sends a message in the VS Code chat window while the polling loop is running, do NOT exit the loop and respond only in chat. Instead:
       1. Apply any fix or instruction from the chat message
       2. Write the result of that fix as a `### RESULT` block inside the **active prompt file** (not only in chat)
       3. Commit the changes
       4. Immediately restart the watcher (Step H)
       The only valid reason to permanently stop the loop is the user explicitly saying "stop", "exit loop", or closing the session.
- When asked to create a new prompt file inside folder, immediately produce a ready-to-use file:
  + Use the following starter template:
    ```markdown
    <follow>
    iterative-prompt/SKILL.md
    </follow>

    ## UPD1
    ```
  + User will write the actual task or requirement under `## UPD1`
  + Name the file `main.prompt.md` and place it in the selected folder.

---

## The Watcher Script

Location: [`./scripts/watch_prompt.py`](./scripts/watch_prompt.py)

### Features

- **Resilient:** outer `try/except` catches any exception (PermissionError, OSError, encoding issues) — logs and continues. Never crashes.
- **Retry on file lock:** `file_hash()` and `read_file()` retry 5× with 200ms delay — handles VS Code editor save locks on Windows.
- **Smart UPD detection:** parses the file by `## UPD` blocks, finds the last one without `### RESULT`, checks if it ends with `go`. Not a simple tail check — works correctly with multiple UPD blocks.
- **Fast feedback:** when file changes but no `go` yet → switches to 1-sec polling and prints `[watcher] still no 'go'; waiting...` so the user sees the agent is alive.
- **Imperative exit message:** prints `>>> AGENT ACTION REQUIRED` lines on exit to reinforce that the agent should continue (helps with models that aggressively close turns).

### Arguments

```
python ./instructions/iterative-prompt/scripts/watch_prompt.py [path-to-prompt-file]
```

Defaults to `.github/work/main.prompt.md` if no argument given.

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | `go` detected — agent should process |
| 2 | File not found |
| 130 | User Ctrl+C (clean exit) |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent doesn't wake after watcher exits | Used `mode=sync` | Switch to `mode=async` |
| `Get-FileHash` / `PermissionError` crashes | Editor save lock (Windows) | Use Python watcher (has retries) |
| Watcher exits immediately | File already has ready UPD with `go` | Process it, then restart |
| Watcher never detects `go` | `go` is inside a sentence, not end-of-block | User must put `go` on its own line or as last word |
| Agent processes wrong UPD | Multiple unprocessed UPDs | Watcher finds last one without RESULT; agent should process all ready ones in order |
