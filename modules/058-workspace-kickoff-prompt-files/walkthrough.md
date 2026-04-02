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

1. Create a new folder called `research-workspace` inside `./workspace/hello-genai/`:
   - Windows: `c:/workspace/hello-genai/research-workspace/`
   - macOS/Linux: `~/workspace/hello-genai/research-workspace/`

2. Open the folder in your IDE (File → Open Folder).

3. Add some raw materials to the folder. For this exercise, create or copy in at least two of the following kinds of files:
   - A short `.md` file with notes or ideas
   - A `.txt` file with a short meeting transcript (you can paste a few lines of a real or invented meeting)
   - A short code file from any project you're familiar with

   > These are your raw inputs. In a real scenario you might clone a repo here, copy chat excerpts, paste transcript text, or download documents.

4. Open the folder in the IDE file tree and confirm you see your materials listed.

### What just happened

You simulated the "landing zone" — a folder where all the raw inputs live. The AI will be able to read everything in this folder when you run your kickoff prompt.

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

1. Create a file named `phase1.prompt.md` at the root of your `research-workspace/` folder.

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

## Success Criteria

- ✅ Created a research workspace folder with at least 2 materials
- ✅ Wrote a `phase1.prompt.md` with a goal description and 🎯N action markers
- ✅ Ran the prompt from the IDE in Agent Mode
- ✅ Verified the AI completed phases in order (preparatory first, main task second)
- ✅ Confirmed the output file was saved in the same folder as the prompt

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

Next module: [Version Control with Git](../060-version-control-git/about.md)
