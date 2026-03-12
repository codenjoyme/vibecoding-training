# Debugging AI-Generated Code - Hands-on Walkthrough

In this module you will learn a repeatable debugging workflow for AI-generated code. You will understand why simply pasting errors back into the chat often fails, and you will practice a structured approach that gets to the root cause faster.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Cover

- **The debug loop trap** — why naive error pasting fails
- **Error anatomy** — what to read and what to skip
- **Isolation technique** — reducing to a minimal reproduction
- **The debug prompt template** — the right way to ask AI to help
- **Escape hatches** — when to stop and rollback

---

## Step 1: The Debug Loop Trap

### What we'll do

Understand the pattern that wastes hours and how to recognise when you're in it.

### The trap

```
You: [paste error]
AI: Try changing line 42 to X
You: [tries, new error]
AI: Now change line 67 to Y
You: [tries, third error]
... (continues indefinitely)
```

**Why it happens:** AI has no memory of the previous fix attempts. Each reply is a fresh probability distribution over tokens. It doesn't "know" it already tried X and Y. You're not debugging together — you're generating random patches.

### How to recognise you're in the trap

- You've applied more than 3 fixes and the code still fails
- Each fix introduces a different error rather than making progress
- AI is suggesting increasingly unrelated changes
- You no longer understand what the code is supposed to do

### The exit rule

**If 3 patches don't fix it → stop patching. Switch to diagnosis mode.**

---

## Step 2: Reading Error Messages

### What we'll do

Learn to extract just the useful parts of an error for your debug prompt.

### Anatomy of an error

```
Traceback (most recent call last):        ← ignore this header
  File "app.py", line 23, in <module>     ← FILE and LINE — keep this
    result = fetch_data(url)
  File "app.py", line 47, in fetch_data   ← the actual call stack
    response = requests.get(url, timeout=timeout)
  File ".../requests/api.py", line 73     ← library internals — SKIP
    ...
requests.exceptions.ConnectionError:     ← ERROR TYPE — keep this
  HTTPSConnectionPool(host='api.example.com', port=443):
  Max retries exceeded with url: /data    ← ERROR MESSAGE — keep this
```

### What to include in your debug prompt

✅ Error type: `requests.exceptions.ConnectionError`  
✅ Error message: `Max retries exceeded with url: /data`  
✅ Your file + line: `app.py line 23` and `app.py line 47`  
✅ The 5–10 lines of YOUR code around those lines  
❌ Library internals (`.../site-packages/...`)  
❌ The full 100-line traceback  

### Hands-on

Open a terminal. Run a Python or Node.js script that you know produces an error (use any broken script from previous modules, or create a simple one: `python -c "import nonexistent"`).

Read the error. Identify: type, message, and the one line in YOUR code that triggered it.

**Verify:** You can point to the single line of your own code that caused the error — not a library line.

---

## Step 3: Isolation Technique

### What we'll do

Reduce the problem to the smallest piece of code that still reproduces the error.

### Why isolate?

An AI that sees 200 lines of code will try to fix all of them. An AI that sees 10 lines will fix the right one.

### Isolation steps

1. **Comment out** everything except the section that errors
2. **Test** — does the minimal version still fail?
3. **If yes** → you have your minimal reproduction. Proceed.
4. **If no** → the error is in the commented-out section. Comment it back in piece by piece.

### Example

Original 80-line script fails somewhere. Isolate:

```python
# Minimal reproduction
import requests

url = "https://api.example.com/data"
# Just this one call — does it fail?
response = requests.get(url, timeout=5)
print(response.json())
```

If this 5-line version fails → that's all AI needs to see.

### Hands-on

Take a broken script (or create one with a deliberate error). Reduce it to fewer than 15 lines that still reproduce the exact same error message.

Windows: save it as `c:/workspace/hello-genai/debug-test.py`  
macOS/Linux: save it as `~/workspace/hello-genai/debug-test.py`

**Verify:** Your minimal reproduction is under 15 lines and produces the same error as the original.

---

## Step 4: The Debug Prompt Template

### What we'll do

Construct a debug prompt that gives AI exactly what it needs — nothing more, nothing less.

### The template

```
I have a [language] script that produces this error:

**Error:**
[error type]: [error message]
File [filename], line [N]

**The relevant code (~10 lines):**
```[language]
[paste only the isolated section]
```

**What I expect it to do:**
[one sentence describing the intended behaviour]

**What it actually does:**
[one sentence describing the failure]

What is the root cause, and what is the minimal fix?
```

### Why this works

- "Root cause" forces AI to diagnose, not patch
- "Minimal fix" prevents AI from rewriting unrelated code
- The expected/actual framing focuses the answer on YOUR intent

### Hands-on

Take the minimal reproduction from Step 3. Fill in the debug prompt template. Send it to AI (Copilot chat in Agent Mode with Claude Sonnet 4.5). Compare the quality of the response to a simple "here's my error, fix it" prompt.

**Verify:** AI's response identifies a specific root cause rather than suggesting random changes.

---

## Step 5: Practice — Fix 3 Bugs

### What we'll do

Apply the full workflow (isolate → template → fix) on three pre-built broken examples.

### Bug 1: Wrong variable scope (Python)

Create `c:/workspace/hello-genai/bug1.py` (Windows) or `~/workspace/hello-genai/bug1.py` (macOS):

```python
def calculate_total(items):
    total = 0
    for item in items:
        subtotal = item["price"] * item["qty"]
    return total  # Bug: returns 0 instead of sum

print(calculate_total([{"price": 10, "qty": 2}, {"price": 5, "qty": 3}]))
```

Apply the workflow. Find the bug. Fix it.

### Bug 2: Missing await (JavaScript/Node.js)

Create `bug2.js`:

```javascript
async function getData() {
  const response = fetch("https://jsonplaceholder.typicode.com/todos/1");
  console.log(response.json()); // Bug: response is a Promise, not a Response
}
getData();
```

Apply the workflow.

### Bug 3: Off-by-one (any language)

```python
items = ["a", "b", "c"]
for i in range(1, len(items) + 1):  # Bug: starts at 1, not 0
    print(items[i])
```

Apply the workflow.

**Verify:** All three bugs fixed, and you can explain the root cause of each without asking AI.

---

## Step 6: Escape Hatches

### What we'll do

Learn when to stop debugging and choose a different strategy.

### Stop debugging when

| Signal | Action |
|---|---|
| 5+ patches, still failing | Rewrite the function from scratch |
| You don't understand the error at all | Ask AI to **explain** the error first, before fixing |
| The whole approach seems wrong | Rollback to last clean Git commit |
| The fix works but you don't know why | Ask AI to explain the fix before accepting |

### The rewrite option

Sometimes a fresh generation is faster than debugging. Ask AI:

```
Forget the broken version. Here is what this function needs to do:
[describe in plain language]
Write it from scratch.
```

### The rollback option

```bash
# See your recent commits
git log --oneline -10

# Rollback to a specific commit
git checkout [commit-hash] -- path/to/file.py

# Or rollback the whole directory
git checkout [commit-hash]
```

Windows and macOS: same Git commands work in both terminals.

### Hands-on

Intentionally break a file, make 3 failed attempts to fix it, then use `git checkout` to restore the clean version. Verify the file is back to its working state.

**Verify:** You successfully used `git checkout` to escape a broken state.

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
