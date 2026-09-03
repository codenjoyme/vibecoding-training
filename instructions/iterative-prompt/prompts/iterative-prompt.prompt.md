---
agent: iterative-prompt
description: |
  Start an iterative-prompt session: process ready UPD blocks, write RESULT,
  make atomic commits, and keep the selected runtime loop alive.
---

Start an iterative-prompt session **now**. Follow [`instructions/iterative-prompt/SKILL.md`](../SKILL.md) and, for an IDE session, [`instructions/iterative-prompt/runtime-ide.md`](../runtime-ide.md).

Target prompt file(s): arguments passed with this invocation. If none, identify the active `*.prompt.md` file from the editor context or ask which helm-log to use.

Workflow per invocation:
1. Scan the target file for the latest unprocessed `## UPD[N]` block ending in `go`.
2. Process it with the mandatory lifecycle: `status.py --start` → implement → append `### RESULT (UPD[N])` → `status.py --finish` → atomic commit.
3. After the commit, re-arm through the selected runtime; IDE sessions use `vscode_askQuestions` as the primary mechanism.
4. Do not wait silently — every IDE turn must end with the runtime's re-arm action.
