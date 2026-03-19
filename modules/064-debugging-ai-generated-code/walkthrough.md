# Debugging AI-Generated Code - Hands-on Walkthrough

In this module you will learn a repeatable debugging workflow for AI-generated code. You will understand why simply pasting errors back into the chat often fails, and you will practice a structured approach that gets to the root cause faster.

> **How this walkthrough works:** Every step ends with a concrete action YOU do. The trainer shows what to look for — you execute and report back what you see. Do not move to the next step until you've completed the action.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Cover

- **The debug loop trap** — why naive error pasting fails
- **Error anatomy** — what to read and what to skip
- **Isolation technique** — reducing to a minimal reproduction
- **The debug prompt template** — the right way to ask AI to help
- **Escape hatches** — when to stop and rollback

---

## Part 1: The Debug Loop Trap

### The core concept

```
You: [paste error]
AI: Try changing line 42 to X
You: [tries, new error]
AI: Now change line 67 to Y
You: [tries, third error]
... (continues indefinitely)
```

**Why it happens:** AI has no memory of the previous fix attempts. Each reply is a fresh generation — it doesn't "know" it already tried X and Y. You're not debugging together — you're generating random patches.

**The three rules to remember:**

1. **Rule of 3:** If 3 patches don't fix it → stop. Switch to diagnosis mode.
2. **Ask for diagnosis:** Instead of "fix this error" → say "What is the root cause? Explain before fixing."
3. **Escape hatch:** If you don't understand what's happening → rollback to the last clean Git commit and restart.

### 🎯 Your action

Think of a time when you got stuck in this loop with AI. Now answer in chat:
- How many fix attempts did you make before stopping?
- What made you finally stop?

*(If you haven't experienced this yet — describe what you think might make you stop.)*

---

## Part 2: Reading Error Messages

### The concept

Most people read a stack trace top-to-bottom and get lost in library internals. The right strategy: **read bottom-up and extract only what matters**.

```
Traceback (most recent call last):        ← SKIP this header
  File "app.py", line 23, in <module>     ← YOUR file + line — KEEP
    result = fetch_data(url)
  File "app.py", line 47, in fetch_data   ← YOUR file — KEEP
    response = requests.get(url, timeout=timeout)
  File ".../requests/api.py", line 73     ← library internals — SKIP
    ...
requests.exceptions.ConnectionError:     ← ERROR TYPE — KEEP
  Max retries exceeded with url: /data   ← ERROR MESSAGE — KEEP
```

**What to include in your debug prompt:**
- ✅ Error type + message (last 2 lines of the traceback)
- ✅ Your file + line number (lines with YOUR filename, not library paths)
- ✅ 5–10 lines of YOUR code around that line
- ❌ Anything from `.../site-packages/...` or `node_modules`

### 🎯 Your action

Open a terminal and run this command:

```
python -c "import nonexistent_module"
```

You will see an error. Look at it and tell me:
1. What is the **error type**? (last line, before the colon)
2. What is the **error message**? (the text after the colon)
3. Is there a file + line number that belongs to YOUR code, or is it all Python internals?

Paste what you see in chat.

---

## Part 3: Isolation Technique

### The concept

An AI that sees 200 lines of code will try to "fix" all 200. An AI that sees 10 lines will fix the right 10.

**Isolation algorithm:**
1. Comment out everything except the section that errors
2. Run — does the minimal version still fail?
3. **Yes** → you have your minimal reproduction
4. **No** → the bug is in the commented part — uncomment piece by piece until error returns

### 🎯 Your action — step by step

**Step 1.** Create the file `c:\workspace\hello-genai\bug1.py` (Windows) or `~/workspace/hello-genai/bug1.py` (macOS) with this content:

```python
def calculate_total(items):
    total = 0
    for item in items:
        subtotal = item["price"] * item["qty"]
    return total

print(calculate_total([{"price": 10, "qty": 2}, {"price": 5, "qty": 3}]))
```

**Step 2.** Run it:
```
python c:\workspace\hello-genai\bug1.py
```

Tell me: what did it print? What did you expect it to print?

*(Do not look for the bug yet — just run and report the output.)*

---

## Part 4: The Debug Prompt Template

### The concept

The difference between "here's my error, fix it" and a structured debug prompt is the difference between a random patch and a root-cause diagnosis.

**Template:**

```
I have a [language] script that produces wrong output:

**What I expect it to do:**
[one sentence — intended behaviour]

**What it actually does:**
[one sentence — actual behaviour]

**The relevant code:**
```python
[paste only the isolated code — under 15 lines]
```

What is the root cause, and what is the minimal fix?
```

**Why it works:**
- `root cause` → forces AI to diagnose, not patch
- `minimal fix` → prevents rewriting code that isn't broken
- `expect / actually` → anchors the answer to YOUR intent, not just "make it run"

### 🎯 Your action

Using the output from Part 3 (the `bug1.py` file), fill in the debug prompt template above. Replace all `[placeholders]` with real values from what you observed.

Then send that filled-in prompt to me in chat.

*(I will respond as the AI being asked for root cause — not as the trainer.)*

---

## Part 5: Off-By-One — Second Bug

### 🎯 Your action — step by step

**Step 1.** Create `c:\workspace\hello-genai\bug3.py` (Windows) or `~/workspace/hello-genai/bug3.py` (macOS):

```python
items = ["a", "b", "c"]
for i in range(1, len(items) + 1):
    print(items[i])
```

**Step 2.** Run it:
```
python c:\workspace\hello-genai\bug3.py
```

**Step 3.** Look at the output and the error. Tell me:
- What printed before the error?
- What is the error type and message?
- What line number in YOUR file caused it?

*(Again — do not fix it yet. Just report what you see.)*

---

## Part 6: Escape Hatches

### The concept

Sometimes the right move is not to debug — it's to stop.

| Signal | Action |
|---|---|
| 5+ patches, still failing | Rewrite the function from scratch with a cleaner prompt |
| You don't understand the error | Ask AI to **explain** the error first — not fix it |
| The approach is fundamentally wrong | `git checkout` to the last clean commit |
| The fix works but you don't know why | Ask AI to explain the fix before accepting |

**The rewrite prompt:**
```
Forget the broken version. Here is what this function needs to do:
[describe in plain language]
Write it from scratch.
```

**The rollback commands:**
```bash
# See recent commits
git log --oneline -10

# Restore a single file to a specific commit
git checkout [commit-hash] -- path/to/file.py
```

### 🎯 Your action

Open a terminal and run:
```
git log --oneline -5
```

Tell me: how many commits do you see, and what are the last 2 commit messages?

*(This confirms you have a safety net before we proceed.)*

---

## Success Criteria

- ✅ You can explain why the "paste error → get fix" loop fails
- ✅ You can read a stack trace and identify the exact line in YOUR code that caused the error
- ✅ You reduced a broken script to a minimal reproduction under 15 lines
- ✅ You used the debug prompt template and received a root-cause diagnosis from AI
- ✅ You fixed all 3 practice bugs using the systematic workflow
- ✅ You successfully used `git checkout` to escape a broken state

---

## Understanding Check

1. **You've applied 4 different AI-suggested fixes and the error keeps changing. What should you do?** *(Answer: Stop patching. Switch to diagnosis mode: isolate the problem, build a minimal reproduction, and use the debug prompt template to get a root cause analysis.)*

2. **What is the most important line to include from a stack trace, and what should you omit?** *(Answer: Include the error type, error message, and your own file/line numbers. Omit library internals from site-packages or node_modules.)*

3. **Why does "what I expect it to do / what it actually does" improve AI debug responses?** *(Answer: It anchors the response to your intent, preventing AI from "fixing" the code in a way that technically runs but does something different from what you need.)*

4. **When is rewriting from scratch better than debugging?** *(Answer: When you've applied 5+ patches with no progress, when you don't understand the current code well enough to reason about it, or when the architecture is fundamentally wrong.)*

5. **What Git command restores a single file to a specific commit state?** *(Answer: `git checkout [commit-hash] -- path/to/file`)*

---

## Troubleshooting

**"I can't find the minimal reproduction — commenting out code makes the error disappear."**  
→ This means the error is caused by an interaction between parts. Try: uncomment one piece at a time, from the top of the file down, until the error reappears. The last piece you uncommented is involved in the root cause.

**"AI keeps suggesting library-level fixes I don't understand."**  
→ Add to your debug prompt: "Do not suggest changes to library configuration. Focus only on my application code."

**"Git checkout shows 'error: Your local changes would be overwritten'."**  
→ Git won't overwrite uncommitted changes. Either `git stash` your changes first, or `git checkout -- .` to discard all unstaged changes.

---

## Next Steps

Continue to [Module 070 — Custom Instructions](../070-custom-instructions/about.md) where you'll codify the debugging patterns you just learned into reusable instructions so AI applies them automatically on future projects.
