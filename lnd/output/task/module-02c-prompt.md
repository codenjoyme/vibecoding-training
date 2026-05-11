# Module 02c — Completion Task

Congratulations on completing Module 02c: Getting to Know Your IDE!

To verify your work, copy the prompt below and paste it into the same AI assistant session where you completed the module. The agent will collect the data and produce a report file. Once the report is generated, copy the contents of `work/module-02c-report.md` and paste them into the answer text field on the learning platform.

```
# Module 02c — Getting to Know Your IDE: Completion Report

You just completed Module 02c of the AI-assisted development training. Now generate a completion report so the autocheck system can verify your work.

## Instructions

Collect the following information from the current environment and produce a report with the sections below.

### Data to collect

1. **Current workspace path:**
   ~~~
   pwd
   ~~~
   or on Windows:
   ~~~
   Get-Location
   ~~~

2. **Files in workspace:**
   ~~~
   ls
   ~~~
   or on Windows:
   ~~~
   Get-ChildItem
   ~~~

3. **Confirm notes.md exists:** Check if the file `notes.md` was created during the module (it should contain a welcome message created by the AI assistant).
   ~~~
   cat notes.md
   ~~~
   or on Windows:
   ~~~
   Get-Content notes.md
   ~~~

4. **Terminal verification:** Run any simple command to confirm the terminal works (e.g. `echo hello`).

5. **AI Chat verification:** Ask the AI: "List the five main areas of the VS Code interface" and capture the first 2–3 sentences of the response.

## Report format

Produce a file called `work/module-02c-report.md` with this structure:

~~~markdown
# Module 02c Completion Report

## Workspace
- Path: <current workspace path>
- Files: <list of files and folders>

## notes.md Content
<paste contents of notes.md, or "not found" if it does not exist>

## Terminal Test
- Command: <command you ran>
- Output: <paste output>

## AI Chat Test
- Question: List the five main areas of the VS Code interface
- Response (first 2–3 sentences): <paste response excerpt>
~~~

Save this report as `work/module-02c-report.md`.
```
