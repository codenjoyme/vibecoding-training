---
agent: iterative-prompt
description: |
  Start an iterative-prompt session: poll a *.prompt.md file for UPD blocks,
  implement them, write RESULT, commit, and loop autonomously via async watcher.
---

Start an iterative-prompt session **now**. Follow [`./.dark-factory/bricks/iterative-prompt/SKILL.md`](../../.dark-factory/bricks/iterative-prompt/SKILL.md) and its IDE runtime [`./.dark-factory/bricks/iterative-prompt/runtime-ide.md`](../../.dark-factory/bricks/iterative-prompt/runtime-ide.md).

Target prompt file(s): arguments passed with this invocation. If none — pick the most recently modified `*.prompt.md` under `.dark-factory/work/` and ask the user to confirm before processing.

Workflow per invocation:
1. Scan the target file for the latest unprocessed `## UPD[N]` block ending in `go`.
2. Process it: implement → append `### RESULT (UPD[N])` → atomic commit (work + prompt file).
3. After RESULT, re-arm by asking a clarifying question via `vscode_askQuestions` so the loop stays alive (per `runtime-ide.md`).
4. Do not wait silently — every turn must end with either a tool call that advances the work or a question to the operator.
