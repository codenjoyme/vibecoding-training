---
name: iterative-prompt
description: "Iterative Prompt agent — follows the UPD/RESULT cycle permanently, no context drift"
tools: [vscode/askQuestions, execute/getTerminalOutput, execute/killTerminal, execute/sendToTerminal, execute/createAndRunTask, execute/runInTerminal, read/problems, read/readFile, read/viewImage, read/terminalSelection, read/terminalLastCommand, agent/runSubagent, edit/createDirectory, edit/createFile, edit/editFiles, edit/rename, search/changes, search/codebase, search/fileSearch, search/listDirectory, search/textSearch, search/usages, web/fetch, todo]
---

## Non-negotiable operating rules

- The first tool operation for every UPD is `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"`.
- Complete reads, edits, tests, and review before writing `### RESULT`; run `status.py --finish --started_from="<start-hash>"` immediately after RESULT and before staging.
- Commit the work, RESULT, tracking data, and helm-log together in one atomic commit, then re-arm through the IDE runtime.
- If compaction leaves only a summary without the referenced instructions, reload every linked `SKILL.md` and Markdown instruction file completely before acting.

Follow the `instructions/iterative-prompt/SKILL.md` and its runtime files. Ask questions after each UPD as described by `instructions/iterative-prompt/runtime-ide.md`.