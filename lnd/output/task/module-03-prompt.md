# Module 03 — Completion Task

Congratulations on completing Module 03: Version Control with Git!

To verify your work, copy the prompt below and paste it into the same AI assistant session where you completed the module. The agent will collect the data and produce a report file. Once the report is generated, upload the resulting `work/module-03-report.txt` file back to the learning platform.

```
# Module 03 — Version Control with Git: Completion Report

You just completed Module 03 of the AI-assisted development training. Now generate a completion report so the autocheck system can verify your work.

## Instructions

Run the following commands in the project directory where you completed the module and collect the output. Then produce a report with the sections below.

### Data to collect

1. **Git identity:**
   ~~~
   git config user.name
   git config user.email
   ~~~

2. **Commit history (full log with stats):**
   ~~~
   git log --oneline --stat
   ~~~

3. **Number of commits:**
   ~~~
   git rev-list --count HEAD
   ~~~

4. **.gitignore contents:**
   ~~~
   cat .gitignore
   ~~~

5. **Current tracked files:**
   ~~~
   git ls-files
   ~~~

6. **Working tree status:**
   ~~~
   git status --short
   ~~~

## Report format

Produce a file called `work/module-03-report.txt` with this structure:

~~~markdown
# Module 03 Completion Report

## Git Identity
- Name: <user.name>
- Email: <user.email>

## Commit History
<paste full git log --oneline --stat output>

## Commit Count
<number>

## .gitignore Contents
<paste .gitignore content>

## Tracked Files
<paste git ls-files output>

## Working Tree Status
<paste git status --short output, or "clean" if nothing to report>
~~~

Save this report as `work/module-03-report.txt`.
```
