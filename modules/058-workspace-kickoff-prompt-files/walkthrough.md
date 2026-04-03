# Workspace Kickoff Prompt Files - Hands-on Walkthrough

You're about to learn a technique for starting any AI-assisted investigation: dump all your materials into a folder, then write a single kickoff prompt file that tells the AI what's there and what you want. This file lives alongside the materials and becomes a permanent artifact — your breadcrumb trail for future reference.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

You'll create a small research workspace with sample materials and a kickoff prompt file named `phase1.prompt.md`. You'll then run it directly from the IDE and see how the AI picks up context from both the prompt and the surrounding files.

| Component | Purpose |
|---|---|
| Research folder | Holds all the raw materials (code, transcripts, notes) |
| `phase1.prompt.md` | Kickoff prompt — describes the materials and what you want done |
| 🎯N markers | Priority labels inside the prompt that sequence AI actions |

---

## Part 1: Understand the Problem This Solves

### Why not just type in the chat?

When you start a chat session, your prompt disappears into history. A week later, when you (or a teammate) open the same folder and wonder "how did this analysis start?" — the chat is gone or buried.

A `.prompt.md` file saved in the folder:
- Stays with the project in version control
- Can be run again at any time
- Shows future readers exactly what question kicked off the work
- Can be shared, reviewed, or improved like any other file

### When does this technique apply?

- You cloned a repository you've never seen and need to understand it quickly
- Someone shared meeting transcript files and you want to extract decisions
- You have scattered notes and chat excerpts and want to synthesize them
- You want to write a document, proposal, or summary from raw inputs

---

## Part 2: Set Up a Research Folder

### What we'll do

Create a small folder that simulates a real research scenario: a mix of materials you want AI to analyze.

### Steps

1. Create the practice folder for this module:
   - Windows: `c:/workspace/hello-genai/work/058-task/`
   - macOS/Linux: `~/workspace/hello-genai/work/058-task/`

   > This follows the course convention: all module exercises go into `work/[module-number]-task/`. The `work/` folder is gitignored, so it's safe to experiment here.

2. Open the folder in your IDE (File → Open Folder).

3. Add some raw materials to the folder. For this exercise, create or copy in at least two of the following kinds of files:
   - A short `.md` file with notes or ideas
   - A `.txt` file with a short meeting transcript (you can paste a few lines of a real or invented meeting)
   - A short code file from any project you're familiar with

   > These are your raw inputs. In a real scenario you might clone a repo here, copy chat excerpts, paste transcript text, or download documents.

4. Open the folder in the IDE file tree and confirm you see your materials listed.

### What just happened

You simulated the "landing zone" — a folder where all the raw inputs live. The `work/058-task/` folder acts as your research workspace for this exercise. The AI will be able to read everything in this folder when you run your kickoff prompt.

---

## Part 3: Write the Kickoff Prompt File

### What we'll do

Create `phase1.prompt.md` at the root of the research folder. This file does three things:
1. Tells the AI what materials are in the folder
2. Describes the goal in raw, natural language
3. Uses 🎯N markers to label priority actions and their order

### The 🎯N Marker Pattern

Inside the prompt, mark each action item with an emoji and a sequential number. Place the marker right before the verb that describes the action:

```
🎯1 Read all meeting transcripts in this folder
🎯2 Extract a list of open decisions
🎯3 Save a summary as summary.md next to this prompt
```

The AI treats these as ordered phases: it should complete preparatory steps before the main task. Add explicit instructions for this in your prompt.

### Steps

1. Create a file named `phase1.prompt.md` at the root of your `work/058-task/` folder.

2. Write the following structure (adapt the content to match your actual materials):

```markdown
# Research Kickoff

## What's in this folder

This folder contains:
- [describe file 1, e.g. "notes.md — my braindump on the project"]
- [describe file 2, e.g. "transcript-2024-11-15.txt — meeting with the team"]
- [any other materials]

## What I want

[Write your raw goal here — don't over-polish it. 
Example: "I want to understand what decisions were made in these meetings 
and what's still unresolved. Also flag anything that looks like a risk."]

## Instructions

In the text below I will mark action items with 🎯N where N is the order.
I will place the marker next to the action verb — convert each into a phase.
Important: do NOT work in parallel. Complete preparatory phases first,
then move to the main task.

🎯1 Read all files in this folder and understand their content.
🎯2 [Your second action, e.g. "Extract all open questions and decisions"]
🎯3 Save the result as `output.md` in the same folder as this prompt.
```

3. Save the file.

### What just happened

The prompt file is now part of the research workspace. It captures your intent in your own words, links to the materials via folder co-location, and sequences the AI's work with 🎯N markers.

---

## Part 4: Run the Kickoff Prompt from the IDE

### What we'll do

Open the prompt file and run it directly in the IDE. In VS Code with GitHub Copilot, you can run `.prompt.md` files without copying the content into the chat.

### Steps

1. Open `phase1.prompt.md` in the editor.

2. In VS Code: look for the **Run Prompt** option:
   - Open the Command Palette and search for "Run Prompt in New Chat"
   - Or use the play button that appears at the top of the editor when a `.prompt.md` file is open

   In Cursor: open the file, select all content, and use it as a chat input with the folder as context.

3. Make sure the AI assistant is in **Agent Mode** and has access to the workspace folder.

4. Trigger the prompt and watch the AI work through the 🎯N phases in sequence.

5. After it finishes, check that `output.md` (or whatever you named the result file in 🎯3) was created in the same folder.

### What just happened

The AI read everything in the folder, understood the context, and worked through your action items in order. The kickoff prompt file remains in place — the chat will end, but the prompt stays.

---

## Part 5: Save It as a Breadcrumb Trail

### Why this matters

Chat sessions can be closed, lost, or buried. But the `phase1.prompt.md` file:
- Stays in the folder alongside the outputs
- Gets committed to version control with the rest of the project
- Shows anyone who opens the folder later where the analysis started
- Can be re-run at any time to reproduce the initial exploration

### Good practices

- Keep the filename meaningful: `phase1.prompt.md`, `onboarding-kickoff.prompt.md`, `codebase-overview.prompt.md`
- Don't over-clean the raw language inside — the imperfect wording is part of the artifact
- If you export a chat session, it may include code snippets and sensitive fragments; the kickoff prompt file is a safer, leaner artifact to preserve
- You can chain phases: after `phase1.prompt.md` produces output, write `phase2.prompt.md` for the next step

---

## Part 6: Grow the Prompt Incrementally with UPD Markers

### Why this matters

A kickoff prompt is rarely final. As your investigation evolves, you think of new angles, clarifications, or follow-up instructions. Instead of opening a new chat and re-explaining context from scratch, you can extend the original prompt file in place.

The pattern: add `UPDN` blocks at the bottom of the file, where `N` is a sequential counter starting from `UPD1`.

### How it works

Each `UPDN` block is a self-contained update. When you reference the file from a new chat conversation, the AI sees the original instructions **plus** all accumulated updates in one read. You don't repeat yourself — you just say "see the prompt file, I added UPD2."

```markdown
## UPD1

Actually, also check for any budget-related discussions in the transcripts.
Flag them with a section header `## Budget mentions` in the output file.

## UPD2

The output format changed — use a table instead of a bullet list for the decisions.
Keep the same `output.md` file.
```

### What makes this different from just editing the prompt

Editing the original text loses history. An `UPDN` block:
- Preserves the original intent at the top
- Shows the evolution of the task in chronological order
- Makes it obvious to a reader what changed and when

### Add a header instruction block to make re-runs reliable

When you re-run a prompt file that has grown UPD blocks, the AI needs to know which parts are "already done" and which are new. The pattern described in this part has been formalized as **Iterative Prompt** — a reusable agent instruction you can install in any workspace:

```
Setup https://github.com/codenjoyme/vibecoding-training/blob/main/instructions/iterative-prompt.agent.md
```

Once installed, add a `<follow>` block at the very top of any prompt file that uses the UPD pattern:

```markdown
<follow>
iterative-prompt.agent.md
</follow>

## UPD1

[Your first task here]
```

Alternatively, add an inline instruction block near the top of the file to get the same behaviour without the agent instruction:

```markdown
<instructions>
This prompt file uses UPD[N] prefixes, where N is an incremental update number.
When running this prompt:
- Check the latest changes (git diff, IDE diff view, or file history) to identify what was recently added.
- Treat the latest UPD[N] block as the active instruction — execute it.
- Treat all earlier content (no UPD prefix, or lower N) as context only — it has already been acted on. Do not re-execute it.
</instructions>
```

This turns the prompt file into a self-describing artifact: anyone (or any AI) who opens it knows exactly what to do with it.

### Steps

1. Reopen `phase1.prompt.md` from the earlier exercise.

2. Add the `<instructions>` block near the top of the file (after the title).

3. At the bottom of the file, add a new section:

```markdown
## UPD1

[Write a clarification or addition to the original task.
Example: "Also extract any action items assigned to specific people. Add them to output.md under a separate heading."]
```

4. Save the file.

5. In a new chat session, reference the file without re-typing the full context:
   > "See `work/058-task/phase1.prompt.md` — the latest UPD1 is what I need done now."

6. Observe that the AI reads both the original goal and your update without you repeating the setup.

### What just happened

The prompt file is now a living document. It holds your original intent, your action items, and your refinements — all in version control, all in one place. Future readers (including your future self) can reconstruct the full story of the investigation by reading one file.

---

## Success Criteria

- ✅ Created `work/058-task/` with at least 2 sample materials
- ✅ Wrote a `phase1.prompt.md` with a goal description and 🎯N action markers
- ✅ Ran the prompt from the IDE in Agent Mode
- ✅ Verified the AI completed phases in order (preparatory first, main task second)
- ✅ Confirmed the output file was saved in the same folder as the prompt
- ✅ Added at least one `UPD1` block to the prompt file and ran it from a new chat session

---

## Understanding Check

1. **Why save the kickoff prompt as a file instead of typing in the chat?**  
   Key points: chat history is temporary and hard to rediscover; a file is permanent, version-controlled, and re-runnable.

2. **What does the 🎯N marker do?**  
   Key points: it labels action items with a priority index directly inside the raw text; the AI converts each into a sequential phase and avoids parallelizing them.

3. **Why should preparatory phases run before the main task?**  
   Key points: the AI needs to read and understand the materials before it can produce meaningful output; doing it in parallel risks shallow analysis.

4. **What's the risk of exporting a full chat session vs. keeping a kickoff prompt file?**  
   Key points: chat exports can include code fragments, `.env` contents, or other sensitive data; a prompt file contains only your intent and is safe to commit.

5. **When would you create a `phase2.prompt.md`?**  
   Key points: when the output of phase 1 becomes new input for further analysis; it extends the breadcrumb trail and keeps each step's intent explicit.

6. **Can you re-run a kickoff prompt file on updated materials?**  
   Key points: yes — because the prompt is a file, you can rerun it as the folder contents evolve, effectively "refreshing" the analysis.

7. **What should the folder contain before you write the kickoff prompt?**  
   Key points: all the raw materials (code, transcripts, notes, chat excerpts) should already be placed in the folder so the AI can access them when the prompt runs.

8. **What is the purpose of `UPDN` blocks, and how do they differ from editing the original prompt text?**  
   Key points: `UPDN` blocks extend the prompt incrementally without overwriting the original intent; they preserve a chronological record of how the task evolved; when reusing the file in a new chat, all the context — original goal plus all updates — is visible in one read without re-explanation.

---

## Troubleshooting

**The AI didn't read all my files**  
Make sure Agent Mode is active and the folder is open as the workspace root. In VS Code, the AI reads files relative to the open workspace — if the research folder is a subfolder, you may need to open it as its own workspace.

**The 🎯N markers were ignored**  
Add an explicit instruction at the top of the prompt: "Complete each 🎯N phase in order. Do not start the next phase until the previous one is done."

**The output file was saved in the wrong location**  
Be specific in your 🎯3 instruction: "Save as `output.md` in the same folder as this prompt file." The AI interprets relative paths from wherever it's currently working.

**The prompt file doesn't have a Run button in VS Code**  
Check that you have a recent version of the GitHub Copilot extension. The `.prompt.md` runner was introduced in later releases. Alternatively, open the file, select all, and paste into the Copilot chat manually.

---

## Next Steps

This technique pairs well with the IDE Workspace as Knowledge Base module — where you learn to set up an entire workspace folder as a persistent knowledge base for ongoing AI conversations, not just one-time kickoffs.
