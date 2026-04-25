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
  6. **After all `## UPD` blocks are processed:** enter an active terminal-based polling loop:
     + **Step A:** Run a blocking wait command in the terminal to pause for a timeout interval:
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
       1. Re-read the **full content** of `instructions/iterative-prompt.agent.md` (this file).
       2. Re-read any other instruction files referenced via `<follow>` in the active prompt file's header (e.g. `training-mode-iterative-prompt.agent.md`).
       3. Re-read any standing user rules previously stated in the conversation (e.g. "no commits", "respond in Russian").
       4. Reset the counter to 0.
       This compensates for context drift during long-running sessions — the polling loop can run for hours, and earlier in the conversation the agent may have loaded these instructions only once. Without periodic refresh, the agent may forget polling rules, commit policy, or language preference. Do NOT skip this step even if "nothing has changed" — the point is to refresh the agent's working memory, not the file content.
     + This loop continues **indefinitely** until the user explicitly stops the agent.
     + Do NOT print "waiting for instructions" to the chat and stop. The agent must keep itself alive via the terminal sleep loop.
     + **Step H — Wake-on-change watcher (preferred over plain sleep):** Instead of sleeping for a fixed 60s and re-reading the file every cycle, run a single longer-lived terminal command that does the polling internally and **only returns to the agent when something actually changed**. This frees the agent from one premium request per 60 s of idle time — the watcher prints a `CHANGED` line to stdout and exits, and the agent sees that line in the terminal output and reacts.

       Use the watcher command appropriate for the OS. The file path is the active prompt file (the `*.prompt.md` that triggered this session).

       **Windows (PowerShell):**
       ```powershell
       $f = 'requests/<folder>/main.prompt.md'
       $h0 = (Get-FileHash $f).Hash
       Write-Host "WATCH baseline=$h0"
       for ($i = 1; $i -le 120; $i++) {
         Start-Sleep -Seconds 60
         $h = (Get-FileHash $f).Hash
         if ($h -ne $h0) { Write-Host "CHANGED after $i min hash=$h"; break }
         Write-Host "[$i min] no change"
       }
       ```

       **Linux / macOS (bash):**
       ```bash
       f='requests/<folder>/main.prompt.md'
       h0=$(sha256sum "$f" | awk '{print $1}')
       echo "WATCH baseline=$h0"
       for i in $(seq 1 120); do
         sleep 60
         h=$(sha256sum "$f" | awk '{print $1}')
         if [ "$h" != "$h0" ]; then echo "CHANGED after $i min hash=$h"; break; fi
         echo "[$i min] no change"
       done
       ```

       Run via `run_in_terminal` in **sync** mode with a timeout matching the loop budget (e.g. 120 minutes → `timeout: 7300000` ms). When the command returns:
       1. Re-read the prompt file.
       2. If a new `## UPD[N]` ending with `go` is found → process it (Step E).
       3. If the file changed but no new ready-to-go UPD is present (user is still typing, no `go` yet) → restart the watcher (back to Step H).
       4. If the watcher hit its 120-min budget without changes → restart the watcher (back to Step H). Also do the Step G anti-drift refresh on every restart.

       **Why this matters:** while the watcher is blocked in `Start-Sleep` / `sleep`, the agent consumes **zero premium requests**. Earlier sessions used the raw "sleep 60 → re-read → sleep again" loop (Steps A–G), which costs one request per cycle. The watcher collapses many cycles into one request. The user can also write **multiple** `## UPD` blocks in parallel — once the watcher fires on any change, the agent processes every ready `## UPD` that has `go`, so previously-completed `go`-blocks waiting for their RESULT can be unblocked in a single wake.

       **Fallback:** if the watcher command fails on the host (no PowerShell, no `sha256sum`, file path with unusual characters, etc.) — fall back to the plain Steps A–F sleep-and-recheck loop above. The plain loop is the backup; the watcher is the preferred path.
     + **⛔ CRITICAL: Chat messages do NOT break the loop.** If the user sends a message in the VS Code chat window while the polling loop is running, do NOT exit the loop and respond only in chat. Instead:
       1. Apply any fix or instruction from the chat message
       2. Write the result of that fix as a `### RESULT` block inside the **active prompt file** (not only in chat)
       3. Commit the changes
       4. Immediately return to Step A (sleep again)
       The only valid reason to permanently stop the loop is the user explicitly saying "stop", "exit loop", or closing the session.
- When asked to create a new prompt file inside folder, immediately produce a ready-to-use file:
  + Use the following starter template:
    ```markdown
    <follow>
    iterative-prompt.agent.md
    </follow>

    ## UPD1
    ```
  + User will write the actual task or requirement under `## UPD1`
  + Name the file `main.prompt.md` and place it in the selected folder.