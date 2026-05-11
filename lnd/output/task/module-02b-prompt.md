# Module 02b — Completion Task

Congratulations on completing Module 02b: Installing Claude Code via Codemie!

To verify your work, copy the prompt below and paste it into the same AI assistant session where you completed the module. The agent will collect the data and produce a report file. Once the report is generated, copy the contents of `work/module-02b-report.md` and paste them into the answer text field on the learning platform.

```
# Module 02b — Installing Claude Code via Codemie: Completion Report

You just completed Module 02b of the AI-assisted development training. Now generate a completion report so the autocheck system can verify your setup.

## Instructions

Collect the following information from the current environment and produce a report with the sections below.

### Data to collect

1. **Node.js version:**
   ~~~
   node --version
   ~~~

2. **npm version:**
   ~~~
   npm --version
   ~~~

3. **Codemie version:**
   ~~~
   codemie --version
   ~~~

4. **Claude Code extension:** Check if the Claude Code extension is installed in VS Code (look in the Extensions panel or run `code --list-extensions | findstr -i claude` on Windows, or `code --list-extensions | grep -i claude` on macOS/Linux).

5. **AI Chat test:** Ask Claude Code: "Create a simple hello world function in Python" and capture the generated code.

## Report format

Produce a file called `work/module-02b-report.md` with this structure:

~~~markdown
# Module 02b Completion Report

## Node.js Version
<paste node --version output>

## npm Version
<paste npm --version output>

## Codemie Version
<paste codemie --version output>

## Claude Code Extension
- Installed: <Yes/No>
- Extension ID: <extension identifier if available>

## AI Chat Test
- Request: Create a simple hello world function in Python
- Generated code:
<paste the generated Python code>
~~~

Save this report as `work/module-02b-report.md`.
```
