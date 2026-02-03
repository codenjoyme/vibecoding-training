# Git Baby Steps Walkthrough

> **Time:** 15-20 minutes  
> **Goal:** Practice baby steps methodology with real Git workflow

---

## Introduction: Why Baby Steps Matter

### The 7±2 Rule

Your brain can hold only **7±2 items** in working memory simultaneously.

**Quick experiment - try memorizing:**
> синий, стол, 12, марафон, бегать, мальчик, 56, число пи, красный, лук, изнашивается, 67, компьютер, окно, 89...

Notice how new words push out earlier ones? This is your cognitive limit in action.

### The Time Paradox

**Scenario:** Task requires implementing 3 features

- **Approach A (Small steps):** 3 sessions × 15 min = **45 minutes total**
  - Session 1: Feature 1 → commit
  - Session 2: Feature 2 → commit  
  - Session 3: Feature 3 → commit

- **Approach B (All at once):** 1 session = **2-3 hours**
  - Keep all 3 features in head simultaneously
  - Context switching between features
  - Confusion accumulates
  - Time wasted untangling mistakes

### Git as Your Safety Net

**Problem:** AI creates working solution → then breaks it while "improving"

**Solution:** Stage files (`git add`) when anything works better, even slightly.

- Changes staged = safe checkpoint
- Can recover instantly if next change fails
- No time wasted recreating what worked

---

## Prerequisites Check

Before starting, verify you have:

- [ ] Empty project folder (or create new one)
- [ ] Git installed (run `git --version` in terminal)
- [ ] GitHub account (optional but recommended)
- [ ] Code editor (VSCode or Cursor)

If Git not installed, see [git-workflow.agent.md](../../../instructions/git-workflow.agent.md#git-installation-and-setup).

---

## Part 1: Project Setup (5 minutes)

### Step 1: Create Test Project

Create a simple project to practice Git workflow. We'll use Python as example, but you can use any language.

**Prompt for AI:**
```
Create a simple Python calculator project with:
- calculator.py with add() and subtract() functions
- main.py that uses the calculator
- README.md with project description
```

**Expected structure:**
```
my-project/
├── calculator.py
├── main.py
└── README.md
```

### Step 2: Initialize Git Repository

**In terminal (from project folder):**
```powershell
# Initialize Git
git init

# Check status
git status
```

**What you see:**
- Git created `.git` folder (hidden)
- All project files shown as "Untracked"

### Step 3: Configure Git Identity

**⚠️ Required before first commit:**

**Prompt for AI:**
```
I need to configure Git with my identity. My name is [Your Name] and email is [your@email.com].
What commands should I run?
```

**AI will suggest:**
```powershell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

**Run those commands, then verify:**
```powershell
git config --global --list
```

### Step 4: Create .gitignore

**⚠️ CRITICAL:** Don't commit secrets, build artifacts, or temporary files.

**Prompt for AI:**
```
Create .gitignore file for Python project. Include:
- Virtual environments
- Cache files
- Secrets/environment files
- IDE configuration
- My working files in temp/ directory
```

**Review the generated .gitignore** - make sure it includes `.env` and other secret files specific to your project.

---

## Part 2: Baby Steps Workflow (8 minutes)

### Step 5: First Commit (Baseline)

**Using IDE (RECOMMENDED):**
1. Open Source Control panel (Ctrl+Shift+G in VSCode)
2. See all changed files
3. Click `+` next to each file to stage
4. Skip staging .gitignore for now (we'll use it as practice later)

**Or via terminal:**
```powershell
git add calculator.py
git add main.py
git add README.md
```

**Check what's staged:**
```powershell
git status
```

**Commit:**
```powershell
git commit -m "Initial calculator with add and subtract"
```

**✅ Checkpoint saved!** You can now experiment safely.

### Step 6: Add Feature with Baby Steps

**Prompt for AI:**
```
Add multiply() function to calculator.py
```

**After AI adds the function:**

1. **Test it** - run the code, verify multiply works
2. **Stage immediately** (via IDE or `git add calculator.py`)
3. **Don't commit yet** - we're building up a feature

**Why stage now?**
- Works better than before (had no multiply)
- If next change breaks it, you can recover
- This is your safety checkpoint

### Step 7: Expand Feature

**Prompt for AI:**
```
Update main.py to demonstrate multiply() function
```

**After change:**

1. **Test both files** - calculator.py and main.py work together?
2. **Stage main.py** (via IDE or `git add main.py`)
3. **Still don't commit** - feature not complete yet

### Step 8: Complete Feature

**Prompt for AI:**
```
Update README.md to document the multiply function
```

**After change:**

1. **Review README** - looks good?
2. **Stage README.md**
3. **NOW COMMIT** - feature is complete

**In IDE:**
- Write commit message: `Add multiply function`
- Click commit button

**Or terminal:**
```powershell
git commit -m "Add multiply function"
```

**✅ Feature complete!** Took 3 small steps instead of one big confusing change.

### Step 9: AI Makes Mistake (Intentional Practice)

**Prompt for AI:**
```
Add divide() function to calculator.py
```

**But DON'T stage/commit yet!**

Now deliberately break something:

**Prompt for AI:**
```
Refactor calculator.py to use class-based structure
```

**This might break existing code.** Check if main.py still works.

**If broken:**

1. **Discard the refactoring** (we didn't stage it - good!)
   - IDE: Right-click file → Discard Changes
   - Terminal: `git checkout -- calculator.py`

2. **Your divide() function is gone!** But it was never staged, so no big loss.

**This demonstrates:** If you had staged divide() when it worked, you could recover it now.

---

## Part 3: Asking AI for Guidance (4 minutes)

### Step 10: Review Files Before Commit

Let's create some temporary test files:

**Prompt for AI:**
```
Create:
- test_calculator.py with unit tests
- debug.py with some debugging code I used to test things
- temp_notes.txt with my personal notes
```

**Now stage everything:**
```powershell
git add .
```

**Before committing, ask AI:**
```
Look at my staged files. Which are production-ready and which are scaffolding/temporary?

Staged files:
[paste output of: git status]
```

**AI will categorize:**
- ✅ **Production:** test_calculator.py (real tests), divide() function if you re-added it
- ❌ **Scaffolding:** debug.py (temporary), temp_notes.txt (personal notes)

**Unstage scaffolding:**
```powershell
git reset HEAD debug.py
git reset HEAD temp_notes.txt
```

**Add them to .gitignore:**

**Prompt for AI:**
```
Update .gitignore to exclude debug.py and temp_notes.txt
```

**Now commit the good stuff:**
```powershell
git add .gitignore
git commit -m "Add tests and update gitignore"
```

---

## Part 4: Remote Repository (Optional, 3 minutes)

If you want to backup to GitHub:

### Step 11: Create GitHub Repository

1. Go to https://github.com/new
2. Name: `git-baby-steps-practice`
3. Public or Private (your choice)
4. **Do NOT initialize** (we have local files already)
5. Click "Create repository"

### Step 12: Connect and Push

**GitHub shows commands, but ask AI to be sure:**

**Prompt:**
```
I created GitHub repo: https://github.com/[username]/git-baby-steps-practice
How do I connect my local repository and push?
```

**AI will provide:**
```powershell
git remote add origin https://github.com/[username]/git-baby-steps-practice.git
git branch -M main
git push -u origin main
```

**Run those commands.**

**✅ Your work is backed up!** Now you can continue baby steps and push regularly.

---

## Part 5: Recovery Practice (2 minutes)

### Step 13: Intentional Mistake

**Prompt for AI:**
```
Add division by zero check to divide() function
```

**Commit it:**
```powershell
git add calculator.py
git commit -m "Add division by zero check"
```

**Now break it:**

**Prompt for AI:**
```
Rewrite entire calculator.py using advanced Python features
```

**This probably broke everything. Test it.**

### Step 14: Undo the Mistake

**Option A: Revert last commit**
```powershell
git revert HEAD
```

This creates new commit that undoes the advanced rewrite.

**Option B: Reset to previous commit**
```powershell
git log --oneline          # Find commit hash before mistake
git reset --hard abc1234   # Replace abc1234 with actual hash
```

This removes the bad commit entirely.

**✅ Recovered!** This is why baby steps matter - easy to undo small changes.

---

## Key Takeaways

### What You Practiced

1. **Baby steps cycle:**
   ```
   Code → Test → Works better? → Stage → Continue
                                    ↓
                              Feature done? → Commit
   ```

2. **Staging = Safety checkpoint**
   - Stage when anything improves (even slightly)
   - Don't wait for perfection
   - Can recover if next change fails

3. **Commit = Complete feature**
   - 5-15 minutes of work
   - Tests pass
   - No obvious bugs

4. **AI is helper, not git operator**
   - AI generates code
   - AI reviews files
   - AI suggests commit messages
   - **YOU control git commands**

### Cognitive Load Management

**Before Git:**
- Hold all changes in head
- Hope nothing breaks
- Waste time untangling mistakes

**With Git Baby Steps:**
- Checkpoint every improvement
- Never lose more than 5-15 min of work
- Clear mind → focus on next small step

---

## Next Steps

### Apply to Real Project

Use this workflow on your actual AI-assisted projects:

1. **Start coding session:**
   - `git status` - clean slate?
   - `git pull` - get latest changes (if team project)

2. **During coding:**
   - Works better? → `git add`
   - Feature done? → `git commit`
   - Major milestone? → `git push`

3. **End of session:**
   - All good work committed?
   - Nothing important left unstaged?
   - Push to backup

### Workflow Variations

**For experiments:**
```powershell
git checkout -b experiment-feature
# Try risky changes
# If works → merge back
# If fails → delete branch
```

**For collaboration:**
```powershell
git checkout -b feature-branch
# Complete feature in baby steps
git push -u origin feature-branch
# Create Pull Request on GitHub
```

---

## Common Questions

**Q: How small is "baby step"?**
**A:** If you can explain the change in one sentence - it's good size.

**Q: Should I commit broken code?**
**A:** No! But you can stage broken code as checkpoint while debugging.

**Q: Can AI commit for me?**
**A:** No! You control what goes into history. AI might commit secrets or junk.

**Q: What if I forgot what I changed?**
**A:** `git diff` shows unstaged changes. Review before staging.

**Q: Should I commit every file AI creates?**
**A:** No! Ask AI to categorize production vs scaffolding. Only commit production.

---

## Troubleshooting

**"I staged the wrong file!"**
```powershell
git reset HEAD filename.py
```

**"I committed too early!"**
```powershell
git reset --soft HEAD~1  # Undo commit, keep changes staged
```

**"I pushed secrets to GitHub!"**
```powershell
# Remove from last commit
git rm --cached .env
git commit --amend -m "Remove secrets"
git push --force

# ⚠️ CRITICAL: Rotate all exposed secrets immediately!
```

**"Everything is broken, I want yesterday's version!"**
```powershell
git log --oneline        # Find good commit
git checkout abc1234     # Go back to that commit
# Test if it works
git checkout -b recovery # Save this as recovery branch
```

---

## Reference: Complete Workflow Cheatsheet

```powershell
# Daily cycle
git status                          # What changed?
git add filename                    # Stage improvements  
git commit -m "descriptive message" # Save feature
git push                            # Backup to remote

# Safety operations
git diff                    # See unstaged changes
git diff --cached           # See staged changes
git checkout -- filename    # Discard unstaged changes
git reset HEAD filename     # Unstage file

# Recovery
git log --oneline          # See history
git revert HEAD            # Undo last commit (safe)
git reset --soft HEAD~1    # Undo commit, keep changes
git reset --hard abc1234   # Go back to specific commit (DESTRUCTIVE)

# Branching
git checkout -b new-branch  # Create branch
git checkout main           # Switch to main
git merge feature-branch    # Merge branch

# Information
git remote -v              # Show remote URLs
git branch                 # List branches
git log --oneline -10      # Last 10 commits
```

---

## Further Reading

For detailed reference see: [git-workflow.agent.md](../../../instructions/git-workflow.agent.md)

Topics covered in detail:
- Complete installation instructions
- .gitignore templates for all languages
- GitHub SSH setup
- Advanced recovery scenarios
- Merge conflict resolution
- Team collaboration workflows
