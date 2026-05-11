# Module 01 — Completion Task

Congratulations on completing Module 01: Installing VS Code + GitHub Copilot!

To verify your work, copy the prompt below and paste it into the same AI assistant session where you completed the module. The agent will collect the data and produce a report file. Once the report is generated, copy the contents of `work/module-01-report.md` and paste them into the answer text field on the learning platform.

```
# Module 01 — Installing VS Code + GitHub Copilot: Completion Report

You just completed Module 01 of the AI-assisted development training. Now generate a completion report so the autocheck system can verify your setup.

## Instructions

Collect the following information from the current environment and produce a report with the sections below.

### Data to collect

1. **VS Code version:**
   ~~~
   code --version
   ~~~

2. **Installed extensions (filter for Copilot):**
   ~~~
   code --list-extensions | findstr -i copilot
   ~~~
   On macOS/Linux use:
   ~~~
   code --list-extensions | grep -i copilot
   ~~~

3. **Workspace folder contents:**
   ~~~
   ls
   ~~~
   or on Windows:
   ~~~
   dir
   ~~~

4. **Test Copilot Chat:** Ask Copilot: "What is a variable in programming?" and capture the first 2–3 sentences of the response.

## Report format

Produce a file called `work/module-01-report.md` with this structure:

~~~markdown
# Module 01 Completion Report

## VS Code Version
<paste code --version output>

## Copilot Extensions
<paste filtered extension list>

## Workspace Folder
- Path: <current workspace path>
- Contents: <list of files/folders>

## Copilot Chat Test
- Question: What is a variable in programming?
- Response (first 2–3 sentences): <paste response excerpt>
~~~

Save this report as `work/module-01-report.md`.
```
