# Module 17 — Completion Task

Congratulations on completing Module 17: Rapid Prototyping (SpecKit)!

To verify your work, copy the prompt below and paste it into the same AI assistant session where you completed the module. The agent will collect the data and produce a report file. Once the report is generated, copy the contents of `work/module-17-report.md` and paste them into the answer text field on the learning platform.

```
# Module 17 — Rapid Prototyping (SpecKit): Completion Report

You just completed Module 17 of the AI-assisted development training. Now generate a completion report so the autocheck system can verify your work.

## Instructions

Collect the following data from your prototype project and produce a report.

### Data to collect

1. **Specification file:** Paste the contents of your `specification.md` (or equivalent spec document).

2. **Commit history:** Run in the prototype project directory:
   ~~~
   git log --oneline
   ~~~

3. **Number of commits:**
   ~~~
   git rev-list --count HEAD
   ~~~

4. **Project file listing:**
   ~~~
   git ls-files
   ~~~

5. **Brief description:** In 2–3 sentences, describe what your prototype does and how the specification guided the implementation.

## Report format

Produce a file called `work/module-17-report.md` with this structure:

~~~markdown
# Module 17 Completion Report

## Prototype Description
<2–3 sentence description>

## Specification Contents
<paste specification.md contents>

## Commit History
<paste git log --oneline output>

## Commit Count
<number>

## Project Files
<paste git ls-files output>
~~~

Save this report as `work/module-17-report.md`.
```
