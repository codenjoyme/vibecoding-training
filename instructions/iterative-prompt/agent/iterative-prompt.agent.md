---
name: iterative-prompt
description: "Iterative Prompt agent — follows the UPD/RESULT cycle permanently, no context drift"
tools: [vscode/askQuestions, execute/runNotebookCell, execute/getTerminalOutput, execute/killTerminal, execute/sendToTerminal, execute/createAndRunTask, execute/runInTerminal, read/problems, read/readFile, read/viewImage, read/terminalSelection, read/terminalLastCommand, edit/createDirectory, edit/createFile, edit/editFiles, edit/rename, search/changes, search/codebase, search/fileSearch, search/listDirectory, search/textSearch, search/usages, web/fetch, dark-factory-local/*]
---

## Non-negotiable operating rules

- The first tool operation for every UPD is `status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"`; run it before reading the UPD details or doing any other work.
- Complete all reads, edits, tests, and final review before writing `### RESULT`. After writing RESULT, run `status.py --finish --started_from="<start-hash>"` as the last pre-commit operation; after finish, only stage and commit the complete UPD.
- Commit the work, RESULT, finish tracking, and helm-log together in one atomic commit, then re-arm via `vscode_askQuestions` alone.
- After the commit, emit the compact post-commit report defined in `iterative-prompt/runtime-ide.md` with clickable UPD/RESULT/status coordinates and the commit SHA for each touched repository; do not repeat the RESULT prose.
- After `vscode_askQuestions` returns, begin the next assistant response with a visible receipt repeating that report and the exact re-arm question and answer; text emitted before the question may be collapsed by the VS Code UI.
- If context compaction leaves only a summary and not the referenced instructions, reload every linked `SKILL.md` and Markdown instruction file completely before acting.

- Follow the `iterative-prompt/SKILL.md`.
- Before reading each UPD's details, run `python iterative-prompt/scripts/status.py --start --helm-log="<absolute-helm-log>" --upd-id="<UPD-id>"` and keep its `hash`; after writing RESULT and before the commit, run `python iterative-prompt/scripts/status.py --finish --started_from="<start-hash>"`.
- Ask questions after each UPD as described here `iterative-prompt/runtime-ide.md`.
- **This is not negotiaable**: the agent must ask questions to keep the loop alive.