# Connecting Course Folder to GitHub

**Duration:** 5-7 minutes

**Skill:** Connect your local course folder to the GitHub repository to receive updates while preserving your work.

**👉 [Start hands-on walkthrough](walkthrough.md)**

---

## Topics Covered

- Creating timestamped backups before Git operations
- Removing existing Git configuration safely
- Connecting local folder to remote GitHub repository
- Syncing with remote while preserving local work folder
- Verifying Git connection and remote configuration

## Learning Outcome

By the end of this module, your `c:/workspace/hello-genai/` (Windows) or `~/workspace/hello-genai/` (macOS/Linux) folder will be connected to the official course repository on GitHub. You'll be able to pull updates with `git pull` while your personal `work/` folder with exercises remains safe.

## Prerequisites

- **Module 025**: Downloading Course Materials (completed)
- **Module 060**: Version Control with Git (Git installed and configured)
- Basic understanding of Git concepts from Module 060
- Your `work/` folder contains exercises you want to preserve

## When to Use This Module

**Complete this module if:**
- You want to receive course updates without re-downloading ZIP files
- You're ready to use Git for managing course materials
- You want proper Git history from the official repository
- You'd like to contribute or report issues via GitHub

**Skip this module if:**
- You prefer to manually re-download ZIP for updates
- You haven't started exercises in `work/` folder yet
- You're practicing Git on separate projects first
- You want to keep course materials completely offline

## What You'll Achieve

After completing this module:

- **Backup safety:** Timestamped ZIP backup of your entire course folder
- **Clean Git history:** Full commit history from the official repository
- **Preserved work:** Your `work/` folder with exercises stays intact
- **Easy updates:** Run `git pull` to get latest course materials
- **GitHub integration:** Can create issues, pull requests, or fork the repository

## Important Safety Notes

- Your `work/` folder is protected by .gitignore in the repository
- Backup is created automatically before any Git operations
- If anything goes wrong, restore from `hello-genai-backup-TIMESTAMP.zip`
- This is a one-time setup - future updates are just `git pull`

## Next Steps

After completing this module, you'll have a fully Git-managed course environment and can continue learning with the confidence that updates won't overwrite your personal work.
