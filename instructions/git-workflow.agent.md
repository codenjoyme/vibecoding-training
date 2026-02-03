# Git Workflow for AI-Assisted Development

## Core Philosophy: Baby Steps Approach

### The 7±2 Rule and Cognitive Load

**Why small commits matter:**
- Human working memory holds only 7±2 items simultaneously
- When you hear: "синий, стол, 12, марафон, бегать, мальчик, 56, число пи, красный, лук, изнашивается, 67..."
  - Each new word displaces previous ones from memory
- Large tasks contain dozens of details → inevitable confusion → time wasted untangling

**Time paradox:**
- Task split into 3×15 min sessions = 45 minutes total
- Same task done all at once = 2-3 hours (due to mental context switching and confusion)

**Solution:** Commit every 5-10-15 minutes. Imperfect but better than before.

---

## Git Installation and Setup

### Windows Installation

1. **Download Git:**
   ```powershell
   # Option 1: Using winget
   winget install --id Git.Git -e --source winget
   
   # Option 2: Download from https://git-scm.com/download/win
   ```

2. **Verify installation:**
   ```powershell
   git --version
   # Should output: git version 2.x.x
   ```

3. **Initial configuration:**
   ```powershell
   # Set your identity (required for commits)
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   
   # Verify settings
   git config --global --list
   ```

### macOS Installation

```bash
# Option 1: Using Homebrew
brew install git

# Option 2: Install Xcode Command Line Tools
xcode-select --install
```

### Linux Installation

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install git

# Fedora
sudo dnf install git

# Arch Linux
sudo pacman -S git
```

---

## Project Initialization

### Creating New Repository

```powershell
# Navigate to your project folder
cd path\to\your\project

# Initialize Git repository
git init

# Check status
git status
```

### Connecting to Remote Repository (GitHub)

1. **Create repository on GitHub:**
   - Go to https://github.com/new
   - Enter repository name
   - Choose public/private
   - Do NOT initialize with README (you already have local files)

2. **Link local repository to GitHub:**
   ```powershell
   # Add remote origin
   git remote add origin https://github.com/username/repository-name.git
   
   # Verify remote
   git remote -v
   ```

3. **First push:**
   ```powershell
   # Create initial commit (see below for staging files first)
   git add .
   git commit -m "Initial commit"
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

---

## .gitignore Configuration

**Critical:** Do NOT commit:
- ❌ Working/test files you're experimenting with
- ❌ Secrets and credentials (`.env`, `secrets.json`, API keys)
- ❌ Build artifacts (compiled files, `/dist`, `/build`, `*.exe`, `*.dll`)
- ❌ Dependencies (`node_modules/`, `venv/`, `.venv/`)
- ❌ IDE files (`.vscode/`, `.idea/`, `*.swp`)
- ❌ OS files (`.DS_Store`, `Thumbs.db`)

### Creating .gitignore

**Ask AI agent:**
```
Create .gitignore file for [Python/Node.js/Java/etc.] project.
Include patterns for:
- Dependencies
- Build artifacts
- Environment files with secrets
- IDE configuration
- OS-specific files
```

**Example Python .gitignore:**
```gitignore
# Virtual environments
venv/
.venv/
env/
ENV/

# Python cache
__pycache__/
*.py[cod]
*$py.class
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
eggs/
*.egg-info/
*.egg

# Environment variables and secrets
.env
.env.local
secrets.json
config/local.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db

# Working files (your experiments)
scratch/
temp/
test_*.tmp
playground/
```

**Example Node.js .gitignore:**
```gitignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build outputs
dist/
build/
out/

# Environment files
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/
```

---

## Daily Git Workflow

### The Baby Steps Process

```
Write code → Works slightly better → git add → Continue
                                         ↓
                                    Keep working
                                         ↓
                                  Feature complete → git commit
```

### 1. Staging Files (The "Чистовик")

**Why stage files:**
- AI might create solution, then break it while fixing something else
- When something works better (even slightly) → save that state
- Prevents wasting time trying to recreate what was working

**Staging via IDE (RECOMMENDED):**
- VSCode: Click `+` next to file in Source Control panel
- Cursor: Same interface
- Visual review of what you're adding

**Staging via terminal:**
```powershell
# Stage specific file
git add filename.py

# Stage multiple files
git add file1.js file2.js

# Stage all changed files (use carefully!)
git add .

# Check what's staged
git status
```

**⚠️ IMPORTANT:** Never let AI agent run git commands on your behalf. It may stage/commit unwanted files.

### 2. Reviewing Staged Files

**Ask AI before committing:**
```
Look at my staged files. Which are production-ready and which are scaffolding/temporary?
```

AI will analyze and categorize:
- ✅ Production-ready: Core functionality, tests, docs
- ❌ Scaffolding: Debug scripts, temporary helpers, experiments

**Unstage scaffolding:**
```powershell
# Unstage specific file
git reset HEAD filename.tmp

# Unstage all
git reset HEAD
```

### 3. Committing

**When to commit:**
- Feature works (even if not perfect)
- Tests pass
- No obvious bugs
- 5-15 minutes of work accumulated

**Good commit messages:**
```powershell
# Format: Short description (50 chars or less)
git commit -m "Add user authentication endpoint"
git commit -m "Fix validation bug in email field"
git commit -m "Improve error handling in API client"

# Longer format with details:
git commit -m "Add user authentication endpoint" -m "- Implement JWT token generation
- Add password hashing with bcrypt
- Create login and logout routes
- Add authentication middleware"
```

**Bad commit messages:**
```powershell
git commit -m "fix"
git commit -m "changes"
git commit -m "work in progress"
git commit -m "asdfasdf"
```

### 4. Pushing to Remote

```powershell
# Push to GitHub
git push
```

---

## Recovery and Undo Operations

### Discard Unstaged Changes

```powershell
# Discard changes in specific file
git checkout -- filename.py

# Discard all unstaged changes (CAREFUL!)
git checkout -- .
```

### Undo Last Commit (Keep Changes)

```powershell
# Undo commit but keep changes staged
git reset --soft HEAD~1

# Undo commit and unstage changes
git reset HEAD~1
```

### Return to Previous Commit

```powershell
# See commit history
git log --oneline

# Return to specific commit (creates new commit)
git revert commit-hash

# Hard reset to commit (DESTRUCTIVE - loses all changes after)
git reset --hard commit-hash
```

### Recover Lost Work

```powershell
# See all actions (including deleted commits)
git reflog

# Recover to specific state
git reset --hard HEAD@{2}
```

---

## Common Scenarios

### Scenario 1: AI Broke Working Code

```powershell
# If changes not staged yet:
git checkout -- filename.py

# If changes staged but not committed:
git reset HEAD filename.py
git checkout -- filename.py

# If already committed:
git revert HEAD
```

### Scenario 2: Need to See What Changed

```powershell
# See unstaged changes
git diff

# See staged changes
git diff --cached

# See changes in specific file
git diff filename.py
```

### Scenario 3: Accidentally Committed Secrets

```powershell
# Remove file from last commit (keep local file)
git rm --cached .env
git commit --amend -m "Remove secrets file"

# If already pushed:
# 1. Remove from commit (as above)
# 2. Force push (use with caution)
git push --force

# 3. IMPORTANT: Rotate all exposed secrets immediately!
```

---

## Best Practices Summary

### Do's ✅

- **Commit frequently** (every 5-15 minutes when something improves)
- **Stage files manually** through IDE interface
- **Review staged files** before committing
- **Write descriptive commit messages**
- **Use .gitignore** to exclude unnecessary files
- **Ask AI** to identify production-ready vs scaffolding code
- **Push regularly** to remote (backup + collaboration)

### Don'ts ❌

- **Never let AI** run git commands for you
- **Don't commit secrets** (.env, API keys, passwords)
- **Don't commit build artifacts** (node_modules, dist, *.dll)
- **Don't commit working files** (scratch.py, test.tmp)
- **Don't use vague commit messages** ("fix", "changes")
- **Don't commit when it's broken** (unless explicitly creating WIP commit)

---

## Integration with AI Agents

### Safe Delegation Pattern

**You control:**
- `git add` (staging files)
- `git commit` (creating commits)
- `git push` (uploading to remote)
- `.gitignore` review and approval

**AI agent can help:**
- Generate `.gitignore` content
- Review which files are production-ready
- Suggest commit messages
- Explain git errors
- Recommend branching strategy

**Example prompts:**
```
"Create .gitignore for Python Django project"
"Review my staged files - which should be committed?"
"Suggest a commit message for these changes"
"Explain this git error: [paste error]"
"How do I undo my last commit?"
```

---

## Troubleshooting

### "Permission denied (publickey)"

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

### "Failed to push some refs"

```powershell
# Remote has changes you don't have
# Pull first, then push
git pull origin main
git push
```

### "Merge conflict"

```powershell
# Open conflicted files, look for:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> branch-name

# Edit file to resolve conflict
# Then:
git add resolved-file.py
git commit -m "Resolve merge conflict"
```

---

## Quick Reference

```powershell
# Daily workflow
git status                    # Check what changed
git add filename             # Stage file
git commit -m "message"      # Commit staged files
git push                     # Upload to remote

# Undo operations
git checkout -- file         # Discard unstaged changes
git reset HEAD file          # Unstage file
git reset --soft HEAD~1      # Undo last commit (keep changes)
git reset --hard abc1234     # Go back to commit (DESTRUCTIVE)

# Information
git log --oneline           # Commit history
git diff                    # See unstaged changes
git diff --cached           # See staged changes
```

---

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Visualizing Git](https://git-school.github.io/visualizing-git/)
