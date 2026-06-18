---
name: iterative-prompt
description: "Iterative Prompt agent — follows the UPD/RESULT cycle permanently, no context drift"
tools: [vscode/askQuestions, execute/getTerminalOutput, execute/killTerminal, execute/sendToTerminal, execute/createAndRunTask, execute/runInTerminal, read/problems, read/readFile, read/viewImage, read/terminalSelection, read/terminalLastCommand, agent/runSubagent, edit/createDirectory, edit/createFile, edit/editFiles, edit/rename, search/changes, search/codebase, search/fileSearch, search/listDirectory, search/textSearch, search/usages, web/fetch, todo]
---

Follow the `instructions/iterative-prompt/SKILL.md`. Ask questions after each UPD.

## Usage telemetry (optional)

If `modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py` exists, follow the **Agent integration block** in `modules/084-copilot-usage-telemetry/tools/SKILL.md` to record one telemetry row per run (`begin` + echo marker at the start, `end` after the commit).