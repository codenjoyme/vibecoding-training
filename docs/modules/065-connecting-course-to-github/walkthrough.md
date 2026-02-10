# Connecting Course Folder to GitHub - Hands-on Walkthrough

In this walkthrough, you'll connect your local course folder (downloaded in Module 025) to the official GitHub repository. This allows you to receive updates with `git pull` while keeping your `work/` folder with exercises safe.

## Prerequisites

- Completed Module 025 (Downloading Course Materials)
- Completed Module 060 (Version Control with Git)
- Git installed and configured with your identity
- Course materials in `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux)
- Terminal access in your IDE

---

## What We'll Do

Before we begin, let's understand the process:

**Current state:**
- You have course files from Module 025 (downloaded as ZIP)
- No .git folder (or maybe you experimented with `git init`)
- Your `work/` folder contains exercises and practice projects

**After this module:**
- Connected to official GitHub repository
- Full Git history from the repository
- Your `work/` folder preserved (it's in .gitignore)
- Can run `git pull` to get course updates
- Backup ZIP created for safety

**What's safe:**
- `work/` folder - listed in repository's .gitignore
- Any other gitignored files
- Your backup ZIP with original state

**What gets replaced:**
- All tracked course files sync with GitHub version
- Any modifications to course modules will be overwritten

---

## Step-by-Step Instructions

### Part 1: Create Backup

**What we'll do:** Create a timestamped ZIP backup of your entire course folder before any Git operations.

#### For Windows (PowerShell):

1. Open your IDE (VS Code or Cursor)

1. Open a terminal: **Terminal > New Terminal**

1. Copy and paste this command:

   ```powershell
   cd c:/workspace/
   $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
   Compress-Archive -Path "hello-genai" -DestinationPath "hello-genai-backup-$timestamp.zip"
   Write-Host "✅ Backup created: hello-genai-backup-$timestamp.zip"
   ```

1. Press `Enter` to execute

1. Wait for compression to complete (10-30 seconds)

1. Verify: Check that backup ZIP appears in `c:/workspace/` folder

#### For macOS (Bash):

1. Open your IDE (VS Code or Cursor)

1. Open a terminal: **Terminal > New Terminal**

1. Copy and paste this command:

   ```bash
   cd ~/workspace/
   timestamp=$(date +%Y%m%d-%H%M%S)
   zip -r "hello-genai-backup-$timestamp.zip" hello-genai
   echo "✅ Backup created: hello-genai-backup-$timestamp.zip"
   ```

1. Press `Enter` to execute

1. Wait for compression to complete (10-30 seconds)

1. Verify: Check that backup ZIP appears in `~/workspace/` folder

#### For Linux (Bash):

1. Open your IDE (VS Code or Cursor)

1. Open a terminal: **Terminal > New Terminal**

1. Copy and paste this command:

   ```bash
   cd ~/workspace/
   timestamp=$(date +%Y%m%d-%H%M%S)
   zip -r "hello-genai-backup-$timestamp.zip" hello-genai
   echo "✅ Backup created: hello-genai-backup-$timestamp.zip"
   ```

1. Press `Enter` to execute

1. Wait for compression to complete (10-30 seconds)

1. Verify: Check that backup ZIP appears in `~/workspace/` folder

**What just happened:** You created a full backup of your course folder with a timestamp like `hello-genai-backup-20260210-143052.zip`. This backup is stored outside the project folder, so it won't be affected by Git operations.

### Part 2: Connect to GitHub Repository

**What we'll do:** Initialize Git, remove any previous Git experiments, and connect to the official course repository.

#### For Windows (PowerShell):

1. In the same terminal, copy and paste these commands:

   ```powershell
   cd c:/workspace/hello-genai/

   # Remove existing .git if present (from previous experiments)
   if (Test-Path .git) { 
       Write-Host "Removing existing .git folder..."
       Remove-Item -Recurse -Force .git 
   }

   # Initialize fresh Git repository
   git init
   Write-Host "✅ Initialized Git repository"

   # Connect to course repository
   git remote add origin https://github.com/codenjoyme/vibecoding-training
   Write-Host "✅ Connected to remote repository"

   # Download repository history and files
   Write-Host "Downloading course files from GitHub..."
   git fetch origin

   # Sync with remote (your work/ folder is safe - it's in .gitignore)
   git reset --hard origin/main

   Write-Host "✅ Successfully connected! Your work/ folder is preserved."
   ```

1. Press `Enter` to execute all commands

1. Wait for the download (may take 30-60 seconds)

1. Watch the output for any errors

#### For macOS/Linux (Bash):

1. In the same terminal, copy and paste these commands:

   ```bash
   cd ~/workspace/hello-genai/

   # Remove existing .git if present (from previous experiments)
   if [ -d .git ]; then
       echo "Removing existing .git folder..."
       rm -rf .git
   fi

   # Initialize fresh Git repository
   git init
   echo "✅ Initialized Git repository"

   # Connect to course repository
   git remote add origin https://github.com/codenjoyme/vibecoding-training
   echo "✅ Connected to remote repository"

   # Download repository history and files
   echo "Downloading course files from GitHub..."
   git fetch origin

   # Sync with remote (your work/ folder is safe - it's in .gitignore)
   git reset --hard origin/main

   echo "✅ Successfully connected! Your work/ folder is preserved."
   ```

1. Press `Enter` to execute all commands

1. Wait for the download (may take 30-60 seconds)

1. Watch the output for any errors

**What just happened:** 
1. Removed any existing .git folder from previous experiments (if it existed)
2. Created a fresh Git repository
3. Connected to the official course repository on GitHub
4. Downloaded all commit history and files
5. Synced your local files with GitHub (your `work/` folder is protected by .gitignore)

**⚠️ Note:** If you see "Reinitialized existing Git repository" - that's OK, it means you experimented with Git before. The `git reset --hard` cleaned everything up.

### Part 3: Verify Connection

1. Check remote connection:

   ```powershell
   git remote -v
   ```

   **Expected output:**
   ```
   origin  https://github.com/codenjoyme/vibecoding-training (fetch)
   origin  https://github.com/codenjoyme/vibecoding-training (push)
   ```

1. Check current branch:

   ```powershell
   git branch
   ```

   **Expected output:**
   ```
   * main
   ```
   (or `* master` depending on repository)

1. Verify your work folder still exists:

   **Windows:**
   ```powershell
   ls work/
   ```

   **macOS/Linux:**
   ```bash
   ls work/
   ```

   **Expected:** You should see your exercise files and project folders

1. View recent commit history:

   ```powershell
   git log --oneline -5
   ```

   **Expected:** Shows 5 most recent commits from the official repository

1. In your IDE's file explorer, check that:
   - `docs/` folder exists with all modules
   - `work/` folder exists with YOUR exercises
   - `scripts/` and other folders are present
   - No extra files that shouldn't be there

**What to verify:**
- ✅ Remote points to `https://github.com/codenjoyme/vibecoding-training`
- ✅ You're on `main` or `master` branch
- ✅ Your `work/` folder and files are still there
- ✅ Git log shows official course commits
- ✅ All course folders are present in IDE

### Part 4: Test Update Workflow

Let's test that you can receive updates:

1. Run the pull command:

   ```powershell
   git pull origin main
   ```

   **Expected output:**
   ```
   Already up to date.
   ```

   (Since you just synced, there are no new changes)

1. Check status to confirm everything is clean:

   ```powershell
   git status
   ```

   **Expected output:**
   ```
   On branch main
   Your branch is up to date with 'origin/main'.
   nothing to commit, working tree clean
   ```

1. Verify your work folder was not touched:

   **Windows:**
   ```powershell
   git status work/
   ```

   **macOS/Linux:**
   ```bash
   git status work/
   ```

   **Expected output:**
   ```
   On branch main
   nothing to commit (use -u to show untracked files)
   ```

   This confirms `work/` is properly ignored

**What just happened:** You tested the update workflow. When the course repository has new modules or updates, you'll run `git pull origin main` and receive them automatically. Your `work/` folder will never be affected.

---

## Success Criteria

Congratulations! You've successfully completed this module if:

✅ Backup ZIP created in `c:/workspace/` (or `~/workspace/`) with timestamp  
✅ Git initialized in `hello-genai/` folder  
✅ Remote connected to `https://github.com/codenjoyme/vibecoding-training`  
✅ `git log` shows official course commit history  
✅ Your `work/` folder with exercises is still present  
✅ `git status` shows clean working tree  
✅ `git pull` command works without errors  
✅ Your personal files in `work/` are not tracked by Git

## Understanding Check

1. **Why did we create a backup before connecting to GitHub?**
   - Safety measure - if anything goes wrong, we can restore from backup; the backup contains our complete state including work folder

1. **What does `git reset --hard origin/main` do?**
   - Makes local files exactly match the remote repository main branch; replaces modified course files but respects .gitignore

1. **Why is the `work/` folder safe during reset?**
   - It's listed in the repository's .gitignore file, so Git never tracks or modifies it

1. **How do you receive course updates in the future?**
   - Run `git pull origin main` in the course folder; new modules and fixes will download automatically

1. **What happens if you modify a course module file locally?**
   - `git status` will show it as modified; `git pull` may conflict; usually should discard local changes or stash them

1. **Can you still work on exercises after this setup?**
   - Yes! The `work/` folder is yours; create projects, edit files freely; Git ignores everything in that folder

1. **Where is the backup stored and what's it called?**
   - In `c:/workspace/` (or `~/workspace/`), named `hello-genai-backup-TIMESTAMP.zip` with current date/time

## Troubleshooting

**Backup command fails or ZIP not created?**
- Make sure you're in the correct directory (`c:/workspace/` or `~/workspace/`)
- Check you have write permissions
- Verify disk space is available (need ~10-20 MB)
- Try creating backup manually: compress `hello-genai/` folder via file manager

**"fatal: not a git repository" error?**
- Make sure you're in the correct directory: `c:/workspace/hello-genai/` (or `~/workspace/hello-genai/`)
- Check you ran `git init` successfully
- Try running `pwd` (macOS/Linux) or `cd` (Windows) to confirm location

**"fatal: remote origin already exists" error?**
- Previous remote exists; remove it: `git remote remove origin`
- Then run `git remote add origin` command again

**"error: failed to push" or authentication errors?**
- This module only pulls/fetches (read access); no push needed
- If you want to contribute later, set up SSH keys or personal access token

**`git reset --hard` says "fatal: bad revision"?**
- Make sure you ran `git fetch origin` first
- Check remote is connected: `git remote -v`
- Try: `git fetch origin main` explicitly

**My `work/` folder disappeared!**
- This shouldn't happen if .gitignore is correct
- Restore from backup: extract `hello-genai-backup-TIMESTAMP.zip`
- Check .gitignore contains: `work/`

**`git pull` asks for credentials?**
- HTTPS URLs require credentials
- For read-only access, credentials shouldn't be needed
- If prompted, you can use GitHub username/password or Personal Access Token
- Or continue without pushing - pulls should work

**Files in `work/` showing in `git status`?**
- Check `.gitignore` contains `work/` line
- Verify you're looking at the root `.gitignore`
- If needed, add manually: `echo "work/" >> .gitignore`
- Commit the .gitignore update

**Download/fetch is very slow?**
- Repository is ~5-10 MB, should take 30-60 seconds
- Check internet connection
- Try again later if GitHub is slow
- Use backup if you need to restore and skip this module

## When to Pull Updates

**Run `git pull origin main` when:**
- Course instructor announces new modules
- You see issues in course materials that might be fixed
- Starting a new learning session (check for updates)
- Every few weeks to stay current

**Before pulling updates:**
- Commit or stash any experiments in tracked files
- Make sure `git status` is clean
- Your `work/` folder is always safe (gitignored)

## Restoring from Backup

If something goes wrong and you need to restore:

1. Delete the `hello-genai/` folder:
   ```powershell
   # Windows
   Remove-Item -Recurse -Force c:/workspace/hello-genai/
   
   # macOS/Linux
   rm -rf ~/workspace/hello-genai/
   ```

1. Extract backup ZIP:
   ```powershell
   # Windows
   Expand-Archive -Path "c:/workspace/hello-genai-backup-TIMESTAMP.zip" -DestinationPath "c:/workspace/"
   
   # macOS/Linux
   cd ~/workspace/
   unzip hello-genai-backup-TIMESTAMP.zip
   ```

1. You're back to pre-connection state; can try again or continue with ZIP-based updates

## Next Steps

Now that your course folder is connected to GitHub:

1. Continue with remaining modules (070 onwards)
1. Pull updates regularly with `git pull origin main`
1. Your `work/` folder is your playground - experiment freely!
1. Consider learning Git branching and advanced workflows in Module 060's additional materials

**Pro tip:** Before starting each learning session, run `git pull` to make sure you have the latest course materials. Your work is always safe!
