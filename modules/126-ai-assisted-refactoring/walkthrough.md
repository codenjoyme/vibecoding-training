# AI-Assisted Refactoring - Hands-on Walkthrough

In this walkthrough, you'll take the messy AI-generated code from your PoC project and systematically clean it using AI as your refactoring partner. You'll apply the "one change, one commit, verify" discipline — so you can always roll back if something breaks — and end up with a reusable refactoring instruction for your team.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **A refactored PoC module** — at least one file from your existing project cleaned up through 3 targeted refactoring passes
- **A refactoring instruction file** — a reusable `.agent.md` instruction that enforces code style, naming conventions, and complexity limits when AI writes future code
- **A Git history** — a clean sequence of atomic commits showing each refactoring step, verifiable by `git log`

These are practical, reusable artifacts your team can apply to any existing codebase.

---

## Step 1: Choose a target file

Open your PoC project folder (from module 120 or 125). Browse the files and pick one that looks messy. Signs of a good refactoring candidate:

- Long functions — more than 30–40 lines inside a single function
- Repetitive code blocks that look almost identical
- Variable names like `result`, `data`, `temp`, `x`, or single letters
- A function that does more than one thing (reads from API *and* writes to file *and* formats output)

Open the file in your editor. Read it. Don't worry if it's confusing — that confusion is the signal.

**Before we start:** Use AI to confirm your choice. In a new AI chat with Agent Mode enabled, paste the file content and ask:

```
Look at this code and identify the top 3 refactoring opportunities.
For each one, explain: what's wrong, what the fix is, and how risky the change is.
```

Read the response. Pick the **lowest-risk** opportunity to start with. Safe first.

---

## Step 2: Create a safety baseline commit

Before touching any code, make sure your current state is committed. This is your rollback point.

**What we're about to do:** We'll commit all current changes so that `git diff` shows exactly what each refactoring step changes — and `git checkout` can undo it.

Open a terminal in your project folder:

**Windows (PowerShell):**
```
cd c:/workspace/hello-genai/
git status
git add .
git commit -m "baseline: before refactoring pass"
```

**macOS/Linux:**
```
cd ~/workspace/hello-genai/
git status
git add .
git commit -m "baseline: before refactoring pass"
```

**What just happened:** You've created a safe checkpoint. Every refactoring change from here can be compared against this commit. If anything breaks, `git checkout -- .` brings you back. This is the baby-step discipline in practice.

---

## Step 3: Refactoring pass 1 — Extract a function

Take the longest block of code inside your target function. Ask AI to extract it:

```
Here is a block of code inside a function. Extract it into a well-named helper function.
Rules:
- The function name must describe what it does, not how it does it
- Use clear parameter names that describe what the inputs represent
- Keep the original function intact — just replace the block with a call to the new helper
- Do not change any logic

[paste the code block here]
```

Apply the change. Then immediately:

1. Run your code or tests to verify nothing broke
2. Check `git diff` to see exactly what changed
3. If it works: `git add . && git commit -m "refactor: extract [function name]"`
4. If it breaks: `git checkout -- .` to revert and discuss with AI what went wrong

**Verify that:** The output of your program is identical before and after. Refactoring must never change behaviour.

---

## Step 4: Refactoring pass 2 — Rename for clarity

Look for variables or parameters with unclear names in your target file. Give AI context:

```
Here are variable names that I want to improve. For each one, suggest a clearer name
that describes what the variable represents (not what type it is, not "data", not "result").
Explain why your suggestion is better.

Names to improve:
[list the unclear names with 1-2 lines of context showing how they're used]
```

Review the suggestions. Accept the ones that make sense. Apply them manually or ask AI to do a find-and-replace:

```
Apply these renames consistently across the file:
- old_name → new_name
- ...
Make sure every occurrence is updated, including function signatures, calls, and comments.
```

Commit the change: `git commit -m "refactor: rename variables for clarity"`

---

## Step 5: Refactoring pass 3 — Simplify logic

Look for `if/else` chains, deeply nested loops, or complex conditions that are hard to read. Ask AI:

```
This logic is hard to read. Suggest a simpler version that:
- Does exactly the same thing (no logic changes)
- Uses fewer levels of nesting
- Can be understood in one reading

[paste the complex block]
```

AI might suggest early returns, guard clauses, list comprehensions, or extracting conditions into named booleans. Review carefully — complexity reductions carry more risk than renames. If unsure, skip and move on.

If you apply the change: commit immediately, run your code, verify output matches.

---

## Step 6: Review the full diff

Look at everything you've done:

```
git log --oneline
git diff HEAD~3 HEAD
```

You should see 3 (or more) clean commits, each with a single purpose. This is what professional refactoring looks like — a traceable history of deliberate improvements.

Ask AI for a final review:

```
Here is the refactored version of my file. Compare it to the original. 
Tell me: what improved most? What could still be better? 
What would you call out in a code review?
```

---

## Step 7: Create a reusable refactoring instruction

Now encode what you learned. In your project's `instructions/` folder, create a new file called `refactoring.agent.md`:

Ask AI to generate it:

```
Create a refactoring instruction file for our project. It should guide an AI agent to:
1. Identify refactoring candidates before making any changes
2. Apply only one refactoring at a time and explain each change
3. Never change logic — only structure, naming, and organisation
4. Follow these conventions:
   - Function names: verbs describing what the function does (e.g., fetchUserData, not getData)
   - Variables: descriptive nouns (no single letters, no "temp", no "result")
   - Max function length: 30 lines
   - Max nesting depth: 3 levels
5. Always output the changed code with a summary of what changed and why

Format it as a Copilot agent instruction file (.agent.md).
```

Save the file. Use it in future AI sessions by attaching it when working with code.

---

## Success Criteria

- ✅ You identified at least 3 refactoring candidates in a real file
- ✅ You applied 3 refactoring passes: extract function, rename variables, simplify logic
- ✅ Each pass was committed separately with a clear commit message
- ✅ The program output is identical before and after all 3 passes
- ✅ `git log --oneline` shows a clean history of refactoring commits
- ✅ You created a `refactoring.agent.md` instruction file for future use
- ✅ You ran `git diff HEAD~3 HEAD` and can read what changed

---

## Understanding Check

1. **Why do we commit before each refactoring step rather than at the end?**
   > Each commit is a rollback point. If step 2 breaks something, you can revert to the commit after step 1 without losing step 1's work. Committing at the end gives you only one rollback target: the beginning.

2. **What is the rule that defines whether something is "refactoring" or "rewriting"?**
   > Refactoring never changes observable behaviour. The output, side effects, and error cases must all remain identical. If the program does something different after the change, it was not a refactor.

3. **Why is "extract function" usually the lowest-risk refactoring?**
   > You're only moving code, not changing it. The logic stays identical — you just give it a name and move it to a new scope. The risk is limited to scope/variable access issues, which are quickly caught by running the code.

4. **What makes a good function name? What makes a bad one?**
   > Good names describe *what* the function does from the caller's perspective: `fetchUserById`, `validateEmailFormat`. Bad names describe *how* it does it (`useRegexToCheckEmail`), or are too vague: `process`, `handle`, `do_thing`.

5. **Why prompt AI with explicit rules ("never change logic", "one change at a time") instead of just asking it to "refactor the code"?**
   > Without constraints, AI will "improve" the code by changing logic it thinks is suboptimal — which is not refactoring, it's rewriting. Explicit rules keep the AI focused on structural changes only and make the output predictable and reviewable.

6. **A colleague says: "I don't need to commit before refactoring. I'll just undo with Ctrl+Z if something breaks." What's the problem with this approach?**
   > Undo history is lost when the editor closes, crashes, or when you switch files. Git commits are durable, shareable, and tied to a specific state of the entire project — not just one open file. You can compare, share, and restore any commit regardless of editor state.

7. **When should you stop refactoring and ask a human for help rather than continuing with AI?**
   > When the same change breaks multiple places in unexpected ways, when the AI's suggested fix introduces new complexity rather than reducing it, or when you can no longer verify that the behaviour is preserved. These are signals that the code structure needs architectural understanding, not just cosmetic changes.

---

## Troubleshooting

**AI keeps changing the logic even when I say "don't change logic"**
> Be more specific: "I need a pure structural refactoring. The output of the function for any given input must be bitwise identical before and after. If you cannot achieve this, say so instead of changing the logic."

**After renaming, the file throws a NameError / ReferenceError**
> AI missed an occurrence. Ask: "Find all references to `old_name` in this file and replace them, including inside string templates, comments, and function calls." Then run the code to verify.

**`git diff` shows hundreds of lines changed across the file**
> This usually means AI reformatted the entire file (changed indentation, whitespace, or quote style) in addition to the refactoring. Commit the formatting change separately: `git commit -m "style: reformat file"`, then commit the refactoring.

**"I can't tell if the output changed — there are no tests"**
> This is exactly why snapshot testing (module 132) exists. For now, run the program manually with the same inputs before and after and compare the output visually. If the program talks to an API, check the API call parameters haven't changed by adding temporary log lines.

**The AI-generated refactoring instruction file looks generic**
> Add your project's specific conventions: paste 2–3 examples of function names from your codebase and ask AI to derive the naming pattern from them. The instruction should reflect your actual code, not a generic style guide.

---

## Next Steps

You now have a production-ready refactoring workflow. The natural next step is to extend your PoC with data persistence:

**→ [Module 128 — Database Schema Design with AI](../128-database-schema-design-with-ai/about.md)**

You've cleaned up the PoC code. Now add a data layer to it using AI-designed schemas, migrations, and queries.
