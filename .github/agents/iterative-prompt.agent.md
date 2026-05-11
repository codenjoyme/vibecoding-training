---
name: iterative-prompt
description: "Iterative Prompt agent — follows the UPD/RESULT cycle permanently, no context drift"
tools: [vscode/askQuestions, execute, read/problems, read/readFile, read/viewImage, read/terminalSelection, read/terminalLastCommand, edit/createDirectory, edit/editFiles, edit/rename, search, web/fetch, 'chrome-devtools/*']
---

Follow the `instructions/iterative-prompt/SKILL.md`. Ask questions after each UPD. 