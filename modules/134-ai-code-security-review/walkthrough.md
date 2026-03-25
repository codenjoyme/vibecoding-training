# AI Code Security Review - Hands-on Walkthrough

In this walkthrough, you'll run a structured security review on your PoC code using AI. You'll learn the vulnerabilities AI tends to generate, build a reusable review instruction, and fix any real issues found in your project.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **A security review instruction** — `instructions/security-review.agent.md` that runs a structured analysis on any code
- **A clean codebase** — all secrets moved to `.env`, common vulnerabilities fixed
- **A security checklist** — a personal reference for what to check before any commit
- **Verified `.gitignore`** — confirming secrets can't leak to Git

---

## Part 1: The OWASP Top 10 in 5 minutes

**What we're about to do:** Ground ourselves in what AI commonly gets wrong before looking at any code.

Open AI chat with Agent Mode enabled and ask:

```
Give me the OWASP Top 10 vulnerabilities, but focus only on the 5 that 
are most commonly introduced by AI code generators (Copilot, ChatGPT, etc.).

For each one:
1. One-sentence plain-English description
2. The most common way AI introduces it
3. A tiny code example showing vulnerable vs. safe version
```

Read through the response. The patterns you'll most likely see:
- **Hardcoded credentials** — API keys, passwords, tokens in source files
- **SQL injection** — string concatenation in queries instead of parameterized queries
- **Missing input validation** — trusting user input without sanitising
- **Insecure defaults** — `debug=True`, `verify=False`, open CORS, no authentication
- **Path traversal** — using user-controlled strings in file paths

These are the exact vulnerabilities you'll look for in your own code.

---

## Part 2: Review your code with AI

Take your PoC project. Open a file — the main application file, or the one with the most API interaction. Ask AI to review it:

```
You are a security reviewer. Review this code for security vulnerabilities.

Focus on:
1. Hardcoded secrets (API keys, passwords, tokens)
2. SQL injection (if there are database queries)
3. Missing input validation (unvalidated user inputs going into logic)
4. Insecure configuration (debug mode, SSL verification disabled, open CORS)
5. Path traversal (user input used in file paths)
6. Any other serious issues you find

For each issue found:
- Describe the vulnerability
- Show the exact line(s) where it occurs
- Explain the impact if exploited
- Show the fixed version

[paste your file content here]
```

Review the findings. Some will be real issues. Some may be false positives — AI sometimes flags things that are intentionally that way. Your job is to evaluate each finding, not blindly apply every fix.

---

## Part 3: Fix hardcoded secrets

This is the highest-priority finding. If AI found any credentials in code, fix them now.

**What we're about to do:** Move secrets from code into a `.env` file that cannot be committed to Git.

**Step 3a — Create the `.env` file:**

Create `.env` in your project root:

```
# Windows
type nul > .env

# macOS/Linux
touch .env
```

Move every hardcoded secret into `.env`:

```
# .env file
OPENAI_API_KEY=sk-your-actual-key-here
DATABASE_URL=sqlite:///./app.db
GITHUB_TOKEN=ghp_your-token-here
```

**Step 3b — Add `.env` to `.gitignore`:**

Open (or create) `.gitignore` in your project root. Make sure this line exists:

```
.env
```

Verify Git doesn't track it:

```
git status
```

The `.env` file should show as "Untracked" or not appear at all — never as "modified" or "staged".

**Step 3c — Load from `.env` in code:**

Ask AI to update your code to read secrets from environment variables:

```
Replace all hardcoded values in this code with environment variable reads.
Use python-dotenv for Python or dotenv for Node.js.
Show the complete updated file and the required import/install line.

Current hardcoded values:
[list them]
```

Install the library and test that your application still works after the change.

**What just happened:** Your secrets are now in a file that Git will never touch. Even if someone gets your source code, they don't get the keys.

---

## Part 4: Fix the highest-priority vulnerabilities

Work through the other findings AI reported in Part 2. For each, ask for a fix:

```
Fix this vulnerability in my code:
[describe the issue]
[paste the vulnerable code]

Requirements:
- Keep the same functionality
- Use the safest standard approach for this language/framework
- Explain what the fix does and why it's safer
```

For SQL injection the fix is always parameterised queries:
```python
# Vulnerable
cursor.execute(f"SELECT * FROM users WHERE email = '{user_email}'")

# Safe
cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
```

For input validation, the fix is always: validate length, type, and format before using the value.

Apply each fix. Run your application after each change. Run snapshot tests (from module 132) to verify output is unchanged.

---

## Part 5: Scan Git history for leaked secrets

**What we're about to do:** Check whether any secret was ever committed in the past — even if it's been deleted from the current files.

```
git log --all --oneline
git grep -i "api_key\|password\|secret\|token" $(git rev-list --all)
```

If anything appears, it means a secret was committed at some point and is still in Git history. Even if you deleted the file, the history contains it.

Ask AI what to do:

```
I found that a secret [describe what] was committed in my Git history. 
The project is not yet public. What are the safest options for removing 
this from history? What are the risks of each option?
Never publish a repo with a committed secret — what should I do right now?
```

The immediate action is always to **revoke and rotate the secret** — regardless of what you do to Git history. An exposed key is a compromised key.

---

## Part 6: Build a reusable security review instruction

Now capture everything you learned as a reusable instruction. Ask AI to create it:

```
Create a security review instruction file for a VS Code Copilot agent.
The instruction should tell the agent to:

1. Scan for hardcoded secrets: API keys, passwords, connection strings, tokens
2. Check for SQL injection: any query using string concatenation or f-strings
3. Check for missing input validation: any user input used in logic without sanitizing
4. Check for insecure defaults: debug=True, verify=False, permissive CORS, no auth checks
5. Check for path traversal: user input used in file paths without validation
6. For each finding, provide: description, vulnerable code snippet, fixed code snippet, severity (High/Medium/Low)

Format as a .agent.md instruction file.
```

Save to `instructions/security-review.agent.md` in your project.

**Using it:** In future sessions, attach this instruction when asking AI to review new code. It will consistently apply the same security lens every time.

---

## Success Criteria

- ✅ You ran a structured AI security review on your PoC code
- ✅ All hardcoded secrets moved to `.env`
- ✅ `.env` is in `.gitignore` and confirmed not tracked by Git
- ✅ At least one other vulnerability was identified and fixed
- ✅ Snapshot tests still pass after all security fixes
- ✅ `instructions/security-review.agent.md` created and saved
- ✅ Git history was checked for leaked secrets

---

## Understanding Check

1. **Why does moving a secret to `.env` only help if `.env` is in `.gitignore`?**
   > If `.env` is tracked by Git, it gets committed whenever it changes — and then it's in the repository forever, accessible in history even after deletion. `.gitignore` is what prevents Git from ever seeing the file. Both steps are required: create `.env` AND add it to `.gitignore`.

2. **Why should you rotate (revoke and regenerate) an API key even if you delete it from Git history?**
   > Deleting from history is not instant or guaranteed to propagate everywhere (forks, clones, CI caches may still have copies). The key may have been scraped by automated bots that scan GitHub in real time. Revocation is the only certain fix — the key is invalid from the moment you revoke it, regardless of who has it.

3. **What makes parameterised SQL queries safe against injection?**
   > The database driver sends the query template and the parameters separately. The database engine never interprets the parameters as SQL — they're always treated as data values. Even if a user enters `'; DROP TABLE users; --`, it's stored as a literal string, not executed.

4. **What is an "insecure default" and why do AI code generators produce them?**
   > Insecure defaults are configurations that prioritise convenience over security — `debug=True`, `verify=False` in SSL calls, `allow_origins=["*"]` in CORS config. AI generates them because the training data contains examples from tutorials, quick-starts, and Stack Overflow answers that prioritise "getting it to work" over production security.

5. **Your code review instruction file will be used by the team. What should you do before sharing it?**
   > Test it on real code examples and verify the AI produces useful results. Check that it doesn't produce too many false positives (noisy). Review it yourself using the security knowledge from this module. Ideally, have a security-aware colleague review the instruction itself.

6. **If `git grep` finds an old API key in history, and the project is already public on GitHub, what are your first two actions?**
   > (1) Immediately revoke and regenerate the key — before doing anything else. The key is compromised the moment it appears in a public repository. (2) Check your API provider's logs to see if the key was used by anyone other than you. History cleanup is the third step, not the first.

---

## Troubleshooting

**AI review is very long and lists many false positives**
> Ask AI: "Focus only on High and Medium severity findings. Skip Low severity. For each finding, confirm whether this is a real vulnerability or a false positive and explain why."

**Application breaks after moving to `.env`**
> The most common cause: the package that reads `.env` wasn't loaded before the application tried to use the variable. In Python, `load_dotenv()` must be called before any `os.getenv()`. Check that your code calls this at the very start.

**`git grep` shows nothing but I know a secret was committed**
> Try searching with case variations: `git grep -i "KEY\|key\|Key"`. Or look at specific commits: `git show [commit-hash]:path/to/file`. The secret might be in a config file, not in Python/JS code.

**`.env` shows as untracked but appears in `git status` as modified**
> This means `.gitignore` is not being applied. Check: (1) the file is named exactly `.gitignore` (no extension), (2) the entry is exactly `.env` with no extra spaces, (3) the file isn't already tracked — run `git rm --cached .env` to untrack it if it was previously committed.

---

## Next Steps

You've built, tested, and secured your PoC. The next phase is integration — connecting it with advanced AI tooling:

**→ [Module 140 — Advanced MCP Integration in PoC](../140-advanced-mcp-integration-in-poc/about.md)**

With a secure, tested application, you're ready to extend it with external services through MCP.
