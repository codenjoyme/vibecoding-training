## Motivation

- When user downloaded course materials as ZIP (Module 025), they have no Git history or connection to remote.
- After learning Git basics (Module 060), they may want to receive course updates via `git pull` instead of re-downloading ZIP.
- This workflow connects local course folder to GitHub repository while preserving user's work in `work/` folder.
- Work folder is protected by .gitignore in repository, so it won't be affected by Git operations.
- Create backup before any Git operations for safety.

## When to Use

- User completed Module 025 (downloaded course as ZIP) and Module 060 (learned Git basics).
- User wants automatic updates instead of manual ZIP re-downloads.
- User has exercises/projects in `work/` folder they want to preserve.
- User understands basic Git commands and is comfortable with terminal.

## Prerequisites Check

- Course materials exist in `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux).
- Git installed and configured (`git --version` and `git config --global user.name` work).
- User completed Git training and understands `git init`, `git remote`, `git fetch`, `git reset`.
- Terminal/command line access available in IDE.

## Backup Creation

- Always create timestamped backup before Git operations for safety.
- Store backup outside project folder so it's not affected by Git.
- Windows PowerShell command:
  ```powershell
  cd c:/workspace/
  $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
  Compress-Archive -Path "hello-genai" -DestinationPath "hello-genai-backup-$timestamp.zip"
  ```
- macOS/Linux command:
  ```bash
  cd ~/workspace/
  timestamp=$(date +%Y%m%d-%H%M%S)
  zip -r "hello-genai-backup-$timestamp.zip" hello-genai
  ```
- Verify backup exists before proceeding with Git operations.

## Git Connection Workflow

- Navigate to course folder: `cd c:/workspace/hello-genai/` (Windows) or `cd ~/workspace/hello-genai/` (macOS/Linux).
- Remove existing `.git` folder if present (from previous experiments):
  + Windows: `if (Test-Path .git) { Remove-Item -Recurse -Force .git }`
  + macOS/Linux: `if [ -d .git ]; then rm -rf .git; fi`
- Initialize fresh Git repository: `git init`.
- Connect to course repository: `git remote add origin https://github.com/codenjoyme/vibecoding-training`.
- Download repository history: `git fetch origin`.
- Sync local files with remote: `git reset --hard origin/main`.
- User's `work/` folder remains intact because it's in repository's .gitignore.

## Verification Steps

- Check remote connection: `git remote -v` should show `origin https://github.com/codenjoyme/vibecoding-training`.
- Check current branch: `git branch` should show `* main` or `* master`.
- Verify work folder exists: `ls work/` should list user's exercise files.
- View commit history: `git log --oneline -5` should show official repository commits.
- Test pull command: `git pull origin main` should respond "Already up to date".
- Check status: `git status` should show "nothing to commit, working tree clean".
- Confirm work folder ignored: `git status work/` should show no tracked files.

## Future Updates

- User can now pull course updates: `git pull origin main`.
- Run pull before starting each learning session to get latest materials.
- Work folder is always safe during pulls (protected by .gitignore).
- If local modifications to course files exist, `git status` will show them.
- Usually should discard local changes to course files before pulling: `git checkout -- filename`.
- Never commit/push to course repository unless user wants to contribute.

## Troubleshooting

- If backup fails: check disk space, write permissions, correct directory.
- If "fatal: not a git repository": ensure in correct directory with `pwd` or `cd`.
- If "fatal: remote origin already exists": remove with `git remote remove origin`, then add again.
- If `git reset --hard` fails: ensure `git fetch origin` ran successfully first.
- If work folder disappeared: restore from backup ZIP, check .gitignore contains `work/`.
- If download very slow: repository is ~5-10 MB, should take 30-60 seconds; check internet.
- If pull asks for credentials: HTTPS should work read-only; use GitHub username/token if needed.

## Restoring from Backup

- If something goes wrong, delete course folder and extract backup.
- Windows: `Remove-Item -Recurse -Force c:/workspace/hello-genai/` then extract ZIP.
- macOS/Linux: `rm -rf ~/workspace/hello-genai/` then `unzip hello-genai-backup-TIMESTAMP.zip`.
- User returns to pre-connection state and can try again or continue with ZIP-based updates.

## Alternative Approach

- Instead of this workflow, user can continue downloading updated ZIP files from GitHub.
- Manual approach: download new ZIP, extract, manually copy their `work/` folder over.
- Git approach is cleaner for regular updates but adds complexity.
- This workflow is optional - both approaches (Git and manual ZIP) are valid.
