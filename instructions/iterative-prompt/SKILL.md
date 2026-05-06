---
name: iterative-prompt
description: Autonomous AI agent workflow — file-based UPD/RESULT cycle
version: 3.0.0
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
- **Fix file references inside the UPD block too.** Before writing `### RESULT`, scan the `## UPD[N]` text for any file paths written as plain text or backtick code. Convert them to clickable markdown links in-place. Change only the link formatting — do not alter any other text.

## Atomic commits

- **One UPD = one commit.** Include both the changed work files AND the updated prompt file (with `### RESULT` already written) in a single commit.
- Never batch multiple UPDs into one commit.
- Never make a separate commit just for `### RESULT` — it must be part of the same commit as the work.
- The commit message summarizes what was done.
- Plans, refusals, clarifications, and any other non-execution responses also go inside `### RESULT` (not chat-only) — chat is breadcrumb only.

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
| [`scripts/watch_prompt.py`](./scripts/watch_prompt.py) | Polls a prompt file; exits 0 when last UPD ends with `go`. | Both runtimes. |
| [`scripts/run_cli.py`](./scripts/run_cli.py) | Thin `copilot` CLI wrapper with `--autopilot` and the right flags for iterative-prompt mode. | CLI runtime only. Pure `copilot` commands, no orchestration framework dependency. |
| [`cli-agent.md`](./cli-agent.md) | Executable agent-identity file passed to `copilot -p`. Tells the CLI agent to run the watcher loop. | CLI runtime only. |

How each script is invoked differs per runtime — see the runtime files.

### Watcher exit codes

| Code | Meaning |
|------|---------|
| 0 | `go` detected — agent should process |
| 2 | File not found |
| 130 | User Ctrl+C (clean exit) |
