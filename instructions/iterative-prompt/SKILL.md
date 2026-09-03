---
name: iterative-prompt
description: Autonomous AI agent workflow — file-based UPD/RESULT cycle
version: 3.1.0
dependencies:
  references:
    - brick
    - tag-ids
    - agent-harness
---

# Iterative Prompt — the pattern

The **Iterative Prompt** is a workflow pattern for AI-assisted development: instead of chatting in a chat window and losing context over time, you maintain a living file called `main.prompt.md` (or any `*.prompt.md`). Every new idea, clarification, or follow-up request is added as a new `## UPD[N]` block at the bottom of that file rather than typed into a chat. After the AI acts on each update, it appends a `### RESULT` block with a brief changelog. The file stays in version control alongside your project — it is your breadcrumb trail, your running specification, and your conversation history all in one artefact.

The key insight: a committed prompt file + `git diff` gives the AI precise, reliable context about what changed since the last run — no hallucination, no drift, no lost history.

> This file is the **runtime-agnostic pattern** (file format, conventions, atomic commits). For the actual loop mechanics, pick one runtime:
> - [`runtime-ide.md`](./runtime-ide.md) — VS Code agent / Copilot Chat with async terminal-notification watcher.
> - [`runtime-cli.md`](./runtime-cli.md) — Copilot CLI in a terminal with `--autopilot`, single long process.

## Why this matters — saving premium requests

Under the current GitHub Copilot billing model, every request to a premium model (e.g. Claude Opus) costs exactly 1% of your monthly premium-request budget — regardless of input/output token count. The most economical strategy is to keep the agent working autonomously for as long as possible per single invocation.

The Iterative Prompt pattern directly supports this:

1. **Maximize autonomous work per request.** A detailed, multi-step prompt file gives the agent enough context to work through many tasks in one run. Set `"chat.agent.maxRequests": 2500` so the agent does not stop every 25 cycles.
2. **Write in a file, not in the chat.** Writing a rich, structured prompt in `*.prompt.md` is more convenient and produces better results than typing in the chat window.
3. **Structure keeps the agent on track.** The `## UPD[N]` → `### RESULT` → `## UPD[N+1]` cycle gives the agent clear boundaries.
4. **Polling loop = zero idle cost.** When all updates are processed the agent enters a watcher-based sleep loop. While sleeping it consumes no premium requests. You write the next `## UPD` at your own pace, append `go`, and the agent picks it up.
5. **Context survives across compaction.** As the conversation grows, VS Code triggers automatic `compact conversation`. The prompt file itself is the running summary, so compaction does not lose critical context.
6. **Git = shared knowledge.** Committing `main.prompt.md` alongside the generated code preserves *how* those files were produced.

## File format

```markdown
<follow>
iterative-prompt/SKILL.md
</follow>

## UPD1

First request from the user. Ends with the magic word: go

### RESULT (UPD1)

Brief changelog. List file paths as clickable markdown links.

## UPD2

Second request. go

### RESULT (UPD2)

…
```

### Conventions

- **`<follow>` header** — optional but recommended. Lists skill files the agent should load on startup.
- **`## UPD[N]`** — sequential update number starting at 1. Each block is one independent unit of work.
- **`go`** — magic word at the end of the block (own line or as last word). The watcher only fires when the last unprocessed block ends with `go`. Without `go`, the user is still typing.
- **`### RESULT (UPD[N])`** — placed inside the corresponding `## UPD[N]` block, immediately after the user's text.
  - List file paths that were created or modified — **always as clickable markdown links**, never as plain text or backtick code:
    - ✅ `[instructions/some-file.agent.md](../../instructions/some-file.agent.md)`
    - ❌ `` `instructions/some-file.agent.md` ``
  - Use a path relative to the prompt file's location so links resolve correctly in VS Code.
  - Keep it concise — this is a changelog, not documentation.
  - **Multiple RESULT blocks per UPD are allowed** (the *multi-result* pattern, see below). Each one starts with its own `### RESULT` header.
- **Fix file references inside the UPD block too.** Before writing `### RESULT`, scan the `## UPD[N]` text for any file paths written as plain text or backtick code. Convert them to clickable markdown links in-place. Change only the link formatting — do not alter any other text.
- **No hard-wrapped prose — in files you create as well as files you edit.** Keep each prose paragraph, list item and blockquote on **one physical line**, however long; blank lines separate paragraphs. Never wrap mid-sentence to fit a column width: it renders the same, but it turns a one-word edit into a whole-paragraph reflow in the diff. Code blocks, tables and YAML keep their own line breaks. See [`creating-instructions/SKILL.md`](../creating-instructions/SKILL.md) for the full rule and how to spot a violation.

## Atomic commits

- **Default: one UPD = one commit.** Include both the changed work files AND the updated prompt file (with `### RESULT` already written) in a single commit.
- Never batch multiple UPDs into one commit.
- Never make a separate commit just for `### RESULT` — it must be part of the same commit as the work.

### ⚠️ Mandatory commit sequence (agents frequently get this wrong)

The correct order is:

1. Before reading the request details, run `python scripts/status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"` and retain its `hash` as `start_hash`. This applies whether the request arrived as chat text, a helm-log link, an `UPD<N>` reference, or another explicit request signal.
2. Do the work (create/edit files, run scripts, etc.).
3. Write `### RESULT (UPD<N>)` into the prompt file (edit the file on disk).
4. Run `python scripts/status.py --finish --started_from="<start_hash>"` after writing RESULT and before staging or committing. This adds the tracking annotation and finish record while they can still be included in the atomic commit.
5. Read `autocommit` from the status payload. If it is `false`, do not stage or commit; tell the operator that the changes remain uncommitted.
6. If `autocommit` is `true`, stage **all** changed files in one `git add` — work files, the prompt file, and the finish tracking files together.
7. If `autocommit` is `true`, run `git commit` — one commit, one message, everything in it.

**Never** commit the work first and then make a second commit for the prompt file. That produces two commits where one is required and breaks the atomic-UPD invariant. The `### RESULT` block is not a post-commit annotation — it is part of the commit payload.

### Runtime status and settings

The runtime settings are `ITERATIVE_PROMPT_AUTOCOMMIT`, `ITERATIVE_PROMPT_TRACE`, and `ITERATIVE_PROMPT_STATUS_DIR`. The first two default to `true`; `ITERATIVE_PROMPT_STATUS_DIR` defaults to `.dark-factory/teams/iterative_prompt`. [`.env.example`](.env.example) documents the local configuration.

```bash
cp iterative-prompt/.env.example .env   # standalone source checkout
```

The settings are resolved with process environment values first, then `.dark-factory/.env` and `.env` files discovered from the current directory towards its parents; a closer file wins. Relative `ITERATIVE_PROMPT_STATUS_DIR` values are resolved from the status command's working directory. The installer assembles this brick's `.env.example` into `.dark-factory/.env.example`, which is copied to `.dark-factory/.env` during installation.

`status.py` prints the resolved settings, the current UTC timestamp, the latest commit for every repository found from the working directory to its parents, and a short hash derived only from the `timestamp`, `helm-log`, and `upd-id` fields. The git snapshot remains informational and does not affect the hash, so it stays stable across a commit. Its stdout is human-readable UTF-8 JSON with two-space indentation and a final newline. It always prints the payload so a disabled trace is visible as `"trace": false`.
Status payloads and JSONL records use the canonical key order `status`, `upd-id`, `helm-name`, then the remaining fields. `helm-name` contains every path component below the nearest directory named `work`, joined with `_`, plus the helm-log file name without `.prompt.md`: `.../work/iterative-prompt/main.prompt.md` becomes `iterative-prompt_main`, and `.../work/tokenomics/reference1/main.prompt.md` becomes `tokenomics_reference1_main`. If no `work` directory is present, it falls back to the immediate-folder format. To migrate an existing status log without changing its timestamps or hashes, run `status.py --migrate` from the workspace root.

For every accepted UPD, before reading or studying its details, run `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"` and retain the returned `hash` as `start_hash`. After writing RESULT and before staging or committing, run `status.py --finish --started_from="<start_hash>"`. The finish operation finds `helm-log` and `upd-id` in the matching start record, appends both lifecycle records to `<ITERATIVE_PROMPT_STATUS_DIR>/status.jsonl`, and adds `(tracked: <start_hash> : <finish_hash>)` to the matching `## UPD<id>` header. Because the hashes do not include git commits, the finish changes can be committed as part of the same UPD commit without changing the tracked pair afterward.
`upd-line` is a 1-based line number. At start it points to the matching `## UPD<N>` header, or to the next line after the current file when that header does not exist yet; start records set `result-lines` to `null`. Finish adds tracking first, then re-reads the block and records the real `upd-line` plus every 1-based `### RESULT` header in `result-lines`; scanning stops at the next `## UPD`, so later unfinished or completed UPDs are not attributed to the current one.

Autocommit is enabled by default. Set `ITERATIVE_PROMPT_AUTOCOMMIT=false` in the discovered `.env` or process environment to leave the work and RESULT uncommitted. Set `ITERATIVE_PROMPT_TRACE=false` when the operator wants the status payload to record that tracing is disabled; in that mode `status.py` still prints JSON but does not write JSONL or modify the helm-log.
- **Commit-message prefix is mandatory.** Every commit message MUST start with a tag `[<helm-log>-UPD<N>]`, or `[<helm-log>-UPD<N>-<M>]` when one UPD produces several commits:
  - `<helm-log>` is derived from the helm-log's **path**, not from its file name alone:
    - file named `main.prompt.md` → **`<folder>`**, the name of the directory holding it. `work/iterative-prompt/main.prompt.md` → `iterative-prompt`.
    - any other file name → **`<folder>_<file>`**, directory name + `_` + file name without `.prompt.md`. `work/common/audit.prompt.md` → `common_audit`.
    - Why the folder and not the file: nearly every work stream names its helm-log `main.prompt.md`, so the file name alone collapses all of them to `[main-UPD<N>]` and the tag stops identifying anything.
  - `<N>` = the UPD number being processed — so `UPD<N>` is **always** present in the prefix.
  - `<M>` = optional sub-request / sub-task index, present **only** when a single UPD is split into multiple commits (several requests in one UPD, or multi-result mode). Omit it for single-commit UPDs.
  - After the tag, write a conventional-commit summary. Examples:
    - single commit → `[iterative-prompt-UPD7] docs(about): clarify brick anatomy slide`
    - non-`main` helm-log → `[common_audit-UPD12] docs(audit): add dependency map`
    - multi-commit UPD → `[factory-about-UPD24-1] feat(factory-about): add franchise + install slides`
- The commit message summarizes what was done.
- Plans, refusals, clarifications, and any other non-execution responses also go inside `### RESULT` (not chat-only) — chat is breadcrumb only.

### ⚠️ Do not repeat the RESULT in chat

The `### RESULT` block **is** the detailed report. Restating it in chat is a second copy of the same text, paid for twice — once written to the file, once streamed to the operator — and it drifts from the file the moment either is edited.

After the atomic commit, a runtime with a chat channel emits only a compact post-commit report. It is operational metadata, not a second summary of the work, and it must use the language of the processed UPD:

```text
Request `UPD<N>` [<helm-file>:<upd-line>](<workspace-relative-helm-log>#L<upd-line>) closed.
Report `RESULT (UPD<N>)` [<helm-file>:<result-line>](<workspace-relative-helm-log>#L<result-line>).
Committed as:
  + In repository [<repo-folder>](<workspace-relative-repo-path>): `<sha>`, `<sha2>`
Tracked in [status.jsonl:<status-line>](<workspace-relative-status-log>#L<status-line>): `<start-hash>` : `<finish-hash>`
```

Use the 1-based `upd-line` and `result-lines` from the finish payload, with a separate link for each non-contiguous RESULT line. Use the physical line number of the finish record in `status.jsonl` for `status-line`, and report only the commit hashes created by this UPD, one line per touched repository. If tracing is disabled, replace the tracking line with a short `Tracking disabled` notice; if autocommit is disabled, replace the committed line with a short uncommitted-changes notice. Do not repeat the changed-file list, implementation details, or RESULT prose in chat.

### UI visibility after `vscode_askQuestions`

`vscode_askQuestions` is a UI interaction whose surrounding container is controlled by VS Code, not by Markdown or the agent. The assistant text emitted before that tool can be collapsed when the operator answers it, so the pre-question report is only a preview. When the tool returns, the next assistant response must begin with a visible receipt that repeats the compact report and records the exact re-arm question and answer in plain text; this is operational metadata, not duplicated RESULT prose. For `stop`, skipped, or placeholder answers, make that receipt the final response with no further tool calls. For `go`, emit the receipt before continuing with the next UPD; the prompt RESULT and status JSONL remain the durable records if a later continuation is collapsed by the UI.

### Multi-repo commits (submodule + parent, or several repos)

The workspace is **not always a single git repo**. A helm-log can live in a git **submodule** (or nested repo) whose **parent** repo tracks it as a pointer, and a single UPD may need to change files in **several** repos at once. When that happens:

- **Commit each touched repo separately**, and tag **every** commit with the same `[<helm-log>-UPD<N>]` prefix (add `-<M>` only in multi-result mode). Never try to cram cross-repo changes into one commit — git can't.
- **Every repo commits ALL of its UPD-related changes — not just the pointer.** A common mistake is to commit *only* the submodule-pointer bump in the parent and forget the other files the UPD created there (generated telemetry under `teams/…`, config, docs, build outputs). Before committing each repo, run `git -C <repo> status` and stage **every** file that this UPD produced or modified in that repo. The parent commit therefore usually contains the pointer bump **plus** those files.
- **Submodule → parent order.** Commit the inner repo (submodule) **first**; then commit the parent repo. The parent's diff is the **submodule-pointer bump plus any parent-repo files this UPD touched**. Make the two commits *linked*: the parent's message references the inner commit sha it points to, e.g. `[subtask1-UPD58] chore(bricks): bump submodule pointer → <inner-sha> (linked)`. This lets a reader walk parent → sub for the same UPD.
- **Stage explicitly, per repo.** Use `git -C <repo> add <specific paths>` for each repo — never `git add -A`. In the parent, stage the submodule path (e.g. `git -C <parent> add bricks`) **and** every other UPD file (e.g. `git -C <parent> add teams/<feature>/telemetry/...`). Verify a clean tree per repo with `git -C <repo> status` before re-arming.
- **The `### RESULT` (with markdown links) lives in the helm-log's own repo** (the submodule/primary), committed together with that repo's work — same as the single-repo rule.
- **Telemetry & UI reflect all repos.** `ide-export --git` discovers the submodule-ownership chain and records a `df.git.repos` list per UPD (see the run-telemetry brick), so the telemetry table shows **one flat row per UPD with one line per touched repo** — each line carrying that repo's branch and short shas. A UPD can therefore show N repos × M commits without any nesting.

### Multi-result mode (opt-in: `follow brick iterative-prompt: multi result`)

When the operator includes the phrase **`multi result`** in a UPD (e.g. `follow brick iterative-prompt: multi result`, or just "делай каждую задачу отдельной итерацией с коммитом"), the rules relax:

- The UPD contains **several independent sub-tasks** (often pre-tagged via the [tag-ids brick](../tag-ids/SKILL.md), e.g. `**MK1**`, `**MK2**`, …).
- For each sub-task: implement → write its own `### RESULT (**MKn**)` block inside the same `## UPD[N]` → atomic commit referencing that sub-task. So one UPD ends up with N commits and N `### RESULT` blocks stacked one after another in the prompt file.
- The parser treats every line matching `^### RESULT` as the start of a new RESULT segment (`splitRequestResult` on the frontend, `block_is_answered` regex on the backend). Do **not** rely on the `(UPDn)` suffix being present — the marker is just `### RESULT`, anything else on the line is annotation (e.g. `### RESULT (**MK3**) — done`).
- The UPD is considered fully answered when the operator confirms (typically by writing the next UPD). The agent should still re-arm after every sub-task commit — re-arming does NOT close the UPD as long as more sub-tasks are pending in the same block.
- Sub-tasks may also accumulate over multiple agent turns (operator types more `**MKn**` items into the same UPD as work progresses) — append a fresh `### RESULT (**MKn**)` for each new one rather than amending an existing block.

## Processing order

When invoked or when the watcher fires, scan the file for unprocessed UPDs:

1. **Find all `## UPD[N]` blocks without a `### RESULT`.**
2. **Skip blocks that do NOT end with `go`** — the user is still typing.
3. **Process each ready block in order.** Implement, write `### RESULT`, atomic commit.
4. **The user and the agent work in parallel.** While the agent processes `## UPD[N]`, the user may be writing `## UPD[N+1]` or `## UPD[N+2]`. They get picked up on the next watcher fire.
5. **After all ready UPDs are processed**, hand off to the runtime watcher loop ([`runtime-ide.md`](./runtime-ide.md) or [`runtime-cli.md`](./runtime-cli.md)).

## When asked to create a new prompt file

Produce a ready-to-use file with this template:

```markdown
<follow>
iterative-prompt/SKILL.md
</follow>

## UPD1
```

Name the file `main.prompt.md` (or `cli.prompt.md` for CLI runtime) and place it in the selected folder. The user fills in `## UPD1`.

## Scripts and files (under this folder)

| File | Purpose | Used by |
|------|---------|---------|
| [`scripts/watch_prompt.py`](./scripts/watch_prompt.py) | Polls a prompt file; exits 0 when last UPD ends with `go`. | CLI runtime (primary); IDE runtime (legacy fallback — primary IDE mechanism is `vscode_askQuestions`, see [`runtime-ide.md`](./runtime-ide.md)). |
| [`scripts/status.py`](./scripts/status.py) | Records UPD start/finish state in compact JSONL and prints the same payload as pretty-printed JSON. | IDE and CLI runtimes, before and after each UPD. |
| [`scripts/run_cli.py`](./scripts/run_cli.py) | Thin `copilot` CLI wrapper with `--autopilot` and the right flags for iterative-prompt mode. | CLI runtime only. Pure `copilot` commands, no orchestration framework dependency. |
| [`cli-agent.md`](./cli-agent.md) | Executable agent-identity file passed to `copilot -p`. Tells the CLI agent to run the watcher loop. | CLI runtime only. |
| [`agent/iterative-prompt.agent.md`](./agent/iterative-prompt.agent.md) | Generic IDE agent identity — same UPD/RESULT loop, no SDLC/team-protocol logic. | IDE runtime. Installed into `.github/agents/iterative-prompt.agent.md` via [`install/list.txt`](./install/list.txt). |
| [`prompts/iterative-prompt.prompt.md`](./prompts/iterative-prompt.prompt.md) | VS Code slash-prompt shortcut. | IDE runtime. Installed into `.github/prompts/iterative-prompt.prompt.md` via [`install/list.txt`](./install/list.txt). |

How each script is invoked differs per runtime — see the runtime files.

### Watcher exit codes

| Code | Meaning |
|------|---------|
| 0 | `go` detected — agent should process |
| 2 | File not found |
| 130 | User Ctrl+C (clean exit) |
