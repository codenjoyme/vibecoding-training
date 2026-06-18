---
name: iterative-prompt
description: "Iterative Prompt agent — follows the UPD/RESULT cycle permanently, no context drift"
tools: [vscode/askQuestions, execute/getTerminalOutput, execute/killTerminal, execute/sendToTerminal, execute/createAndRunTask, execute/runInTerminal, read/problems, read/readFile, read/viewImage, read/terminalSelection, read/terminalLastCommand, agent/runSubagent, edit/createDirectory, edit/createFile, edit/editFiles, edit/rename, search/changes, search/codebase, search/fileSearch, search/listDirectory, search/textSearch, search/usages, web/fetch, todo]
---

Follow the `instructions/iterative-prompt/SKILL.md`. Ask questions after each UPD.

## Usage telemetry (optional)

If `modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py` exists, track each UPD run:

1. **At the start of a UPD**, before doing the work, run `usage_track.py begin "UPD<N>"`. It prints a unique `marker`. **Echo that marker on its own line into the chat** so it lands in the session log (this is how the run is later matched to the right log).
2. **At the end of the UPD**, after the `### RESULT` is written and committed, ask the user two quick numbers — minutes spent writing the prompt and minutes spent reading the result — then run `usage_track.py end <run_id> --write-min <W> --read-min <R>`.

The two marker echoes (begin/end) bracket the run inside the log. Never block the UPD on telemetry — if a telemetry command fails, note it and continue.