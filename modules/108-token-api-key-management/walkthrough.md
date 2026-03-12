# Token & API Key Management - Hands-on Walkthrough

In this module you will set up the standard secrets management workflow used in every professional project. You will learn why API keys leak, how to keep them out of Git, and what to do when one is compromised.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Cover

- **Why keys leak** — the mechanics of accidental exposure
- **`.env` + `dotenv`** — the industry-standard pattern for local secrets
- **Environment variables** — how to set and read them in the terminal
- **Key rotation** — practice revoking and replacing a key
- **Pre-commit checklist** — your last line of defence before a push

---

## Step 1: Why Keys Leak

### What we'll do

Understand the real-world consequences of an exposed API key before setting up protection.

### How it happens

The most common causes of key exposure in order of frequency:

1. **Committed directly** — developer pastes the key into code and runs `git commit`
2. **Logged** — key included in a debug print statement that makes it into logs
3. **Config file forgotten** — `.env` or `config.json` not in `.gitignore`, committed accidentally
4. **Screenshot** — key visible in a terminal screenshot shared in a PR comment or Slack

### What happens next

GitHub scans every public push for known API key formats. Within seconds of a push:
- GitHub sends you an email: "We found a secret in your repository"
- Many providers (GitHub, OpenAI, AWS) **automatically revoke** the key
- Your application breaks immediately
- If the repo was public even briefly, bots have already scraped and used the key

### Hands-on

Search your current project folder for any file that might contain a raw key:

Windows (PowerShell):
```powershell
Get-ChildItem -Recurse -Include "*.py","*.js","*.json","*.env","*.yaml","*.yml" | 
  Select-String -Pattern "api_key|apikey|secret|token|password" -CaseSensitive:$false
```

macOS/Linux (bash):
```bash
grep -r -i "api_key\|apikey\|secret\|token\|password" \
  --include="*.py" --include="*.js" --include="*.json" \
  --include="*.env" --include="*.yaml" .
```

**Verify:** You can see which files in your project might contain sensitive values. Note any real keys you find — you will move them in the next step.

---

## Step 2: The `.env` + `dotenv` Pattern

### What we'll do

Create a `.env` file, add it to `.gitignore`, and load it from code.

### What is `.env`?

A `.env` file is a plain text file with one `KEY=VALUE` per line. It lives only on your machine, never in Git.

```
# .env
OPENAI_API_KEY=sk-proj-abc123...
GITHUB_TOKEN=github_pat_xyz...
DIAL_API_KEY=dial-key-456...
```

### Step 2a: Create the `.env` file

Navigate to your project folder. Create the file:

Windows (PowerShell):
```powershell
cd c:/workspace/hello-genai
New-Item .env -ItemType File
```

macOS/Linux:
```bash
cd ~/workspace/hello-genai
touch .env
```

Open `.env` in your editor and add one key-value pair for a key you currently have (use a fake value if you prefer):
```
MY_API_KEY=your-key-here
```

### Step 2b: Add `.env` to `.gitignore` IMMEDIATELY

This is the most important step. Do it before anything else:

```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

### Step 2c: Load `.env` in Python

Install `python-dotenv`:
```bash
pip install python-dotenv
```

In your Python script:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env from the current directory

api_key = os.getenv("MY_API_KEY")
print(f"Key loaded: {api_key[:6]}...")  # print only first 6 chars — never the full key
```

### Step 2d: Load `.env` in Node.js

Install `dotenv`:
```bash
npm install dotenv
```

In your Node.js script:
```javascript
require('dotenv').config();

const apiKey = process.env.MY_API_KEY;
console.log(`Key loaded: ${apiKey.substring(0, 6)}...`);
```

**Verify:** Run your script. You should see `Key loaded: your-k...` (first 6 chars). The key was loaded from `.env`, not hardcoded.

---

## Step 3: Environment Variables in the Terminal

### What we'll do

Set and read environment variables directly in PowerShell and bash — useful for one-off commands and CI/CD pipelines.

### Windows PowerShell

Set a variable for the current session:
```powershell
$env:MY_API_KEY = "your-key-here"
```

Read it back:
```powershell
echo $env:MY_API_KEY
```

Set permanently for your user account:
```powershell
[System.Environment]::SetEnvironmentVariable("MY_API_KEY", "your-key-here", "User")
```

Verify it persists (open a new PowerShell window then):
```powershell
echo $env:MY_API_KEY
```

### macOS/Linux bash/zsh

Set for current session:
```bash
export MY_API_KEY="your-key-here"
```

Read it back:
```bash
echo $MY_API_KEY
```

Set permanently (add to `~/.zshrc` or `~/.bashrc`):
```bash
echo 'export MY_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### When to use env vars vs `.env`

| Scenario | Use |
|---|---|
| Local development project | `.env` file + dotenv |
| CI/CD pipeline (GitHub Actions) | Environment secrets in the platform UI |
| Shared server / container | Platform-level secrets manager |
| Quick one-off terminal command | `export` / `$env:` for the session |

**Verify:** You set a variable in the terminal and read it back with `echo`. Then opened a new terminal window and verified whether it persisted.

---

## Step 4: Rotate a Key

### What we'll do

Practice the full key rotation workflow — the procedure you will use when a key is compromised or expires.

### Why practice this now?

Key rotation under pressure (when a key leaks at 2am) is stressful. Practising it when calm builds muscle memory.

### Rotation steps

1. **Generate a new key** at the provider (GitHub → Settings → Developer settings → Personal access tokens → Generate new token)
2. **Update `.env`** with the new key value
3. **Test** that your application works with the new key
4. **Revoke the old key** at the provider
5. **Commit nothing** — `.env` stays out of Git

### Hands-on

Using your GitHub personal access token (or any other key you have):

1. Go to github.com → Profile → Settings → Developer settings → Personal access tokens
2. Create a new token with the same scopes as your current one
3. Update your `.env` file with the new value
4. Run any script that uses `GITHUB_TOKEN` to confirm it works
5. Revoke the old token from the GitHub settings page

**Verify:** Old token shows as "Revoked" in GitHub settings. New token works in your script.

---

## Step 5: Pre-Commit Checklist

### What we'll do

Create a checklist you run before every `git push` to ensure no secrets are staged.

### The checklist

Create `c:/workspace/hello-genai/secrets-checklist.md` (Windows) or `~/workspace/hello-genai/secrets-checklist.md` (macOS):

```markdown
# Pre-Commit Secrets Checklist

Run before every `git push` for any project that uses API keys.

## Quick checks

- [ ] Run: `git diff --staged | grep -i "api_key\|secret\|token\|password"`  
      → Result should be empty. If not, unstage the file and move the secret to `.env`.
- [ ] Is `.env` in `.gitignore`?  
      → Run: `cat .gitignore | grep ".env"`  — should show `.env`
- [ ] Does any staged file contain a key-shaped string (long random string)?  
      → Look at `git diff --staged` output manually for suspicious values.

## If a key is already committed

1. Revoke the key immediately at the provider
2. Generate a new key
3. Remove the key from Git history: `git filter-branch` or BFG Repo Cleaner
4. Force-push the cleaned history
5. Update `.env` with the new key
```

### Add to `.git/hooks` (optional automation)

You can automate the grep check as a pre-commit hook:

Windows (PowerShell — create the file):
```powershell
New-Item -Path ".git/hooks/pre-commit" -ItemType File
```

macOS/Linux:
```bash
touch .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Content of the hook:
```bash
#!/bin/sh
if git diff --staged | grep -qi "api_key\|apikey\|secret_key\|password\s*="; then
  echo "ERROR: Possible secret in staged files. Review with: git diff --staged"
  exit 1
fi
```

**Verify:** Stage the `secrets-checklist.md` file and commit it. The checklist is now in your project.

---

## Success Criteria

- ✅ `.env` file created and `.env` is in `.gitignore`
- ✅ At least one API key loaded from `.env` in a Python or Node.js script
- ✅ You set an environment variable in the terminal for your OS
- ✅ You practised key rotation: generated new key, updated `.env`, revoked the old one
- ✅ Secrets checklist file created and committed to the project

---

## Understanding Check

1. **A colleague commits their `.env` file to a public GitHub repo. What happens next?** *(Answer: GitHub's secret scanning detects it within seconds. Depending on the provider, the key may be automatically revoked. GitHub sends an email alert. If the repo was public even briefly, automated bots may have already copied and used the key.)*

2. **What is the correct order of operations when starting a new project?** *(Answer: 1. Create `.gitignore` with `.env` listed. 2. Create `.env`. 3. Add keys to `.env`. Never the other way — always gitignore before creating the file.)*

3. **A `.env` file works locally but the app fails in production. Why?** *(Answer: `.env` files are for local development only. Production environments use platform-level secrets: GitHub Actions secrets, AWS Secrets Manager, environment variables set in the hosting platform UI.)*

4. **What does `dotenv` actually do?** *(Answer: It reads the `.env` file from disk and sets each `KEY=VALUE` pair as an environment variable in the current process, making them accessible via `os.getenv()` or `process.env`.)*

5. **You discover a key was committed 3 commits ago and has already been pushed. Describe the steps.** *(Answer: 1. Revoke the key immediately. 2. Generate a replacement. 3. Use `git filter-branch` or BFG Repo Cleaner to remove the key from ALL commits in history. 4. Force-push. 5. Update `.env`. 6. Notify anyone who may have cloned the repo.)*

6. **Why should you never print a full API key in logs, even temporarily?** *(Answer: Logs are often stored, indexed, and may be shared. A key visible in a log can be extracted by anyone with log access, including future employees, external log monitoring tools, or breach attackers.)*

---

## Troubleshooting

**"`load_dotenv()` isn't finding my `.env` file."**  
→ By default, `load_dotenv()` looks for `.env` in the current working directory. Run your script from the directory where `.env` lives, or pass the path explicitly: `load_dotenv('/full/path/to/.env')`.

**"I added `.env` to `.gitignore` but `git status` still shows it."**  
→ The file was already tracked by Git. You need to untrack it: `git rm --cached .env` then commit. This removes it from Git history tracking without deleting the local file.

**"The pre-commit hook isn't running."**  
→ On macOS/Linux, the hook file needs execute permission: `chmod +x .git/hooks/pre-commit`. On Windows, Git hooks may need Git Bash to run shell scripts — use PowerShell-compatible syntax instead.

---

## Next Steps

Continue to [Module 110 — Development Environment Setup](../110-development-environment-setup/about.md) where you will install Node.js and Docker. You will apply the `.env` pattern immediately for all configuration in that environment.
