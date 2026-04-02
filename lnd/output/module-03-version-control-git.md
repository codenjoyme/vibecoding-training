# Module 3: Version Control with `Git`

### Background
Imagine spending two hours building something that works perfectly — then asking the AI to "make one small improvement" and watching everything break. You try to undo, but the AI has already changed too many files. Your working version is gone.

This scenario happens to everyone who works with AI assistants without a safety net. `Git` is that safety net. It is a version control system that saves snapshots of your project at any point. If something goes wrong, you restore the last working snapshot in seconds.

In this module, you will learn the "baby steps" methodology: make one small change, verify it works, save a snapshot, then move on. This approach keeps your working memory manageable and your project always recoverable. You will use `Git` for every subsequent module in this course.
**Learning objectives.** Upon completion of this module, you will be able to:
- Initialize a `Git` repository and configure your identity.
- Apply the baby steps workflow: change → test → stage → commit.
- Recover from an AI-generated mistake by discarding uncommitted changes.
- Create a `.gitignore` file to exclude sensitive and temporary files.

## Page 1: Why Baby Steps Matter
### Background
Your brain can hold roughly 7±2 items in working memory simultaneously. When you try to implement three features at once, each new detail pushes out an earlier one, leading to confusion and mistakes. The baby steps approach respects this cognitive limit.

Consider two approaches to implementing three features:

Approach A (Baby steps): 3 sessions × 15 minutes = 45 minutes total. Each session focuses on one feature, commits it, and moves on with a clear head.

Approach B (All at once): 1 session of 2–3 hours. You keep all three features in your head, context-switch between them, and spend extra time untangling mistakes.

Baby steps are faster, safer, and less stressful — especially when working with an AI assistant that might occasionally break things while "improving" them.

The workflow is simple:
- Make a small change.
- Test it — does it work?
- If yes: save a snapshot (`git add` + `git commit`).
- If no: discard the change and try again (`git checkout`).
- Repeat.

One important clarification: "works" does not mean everything is perfect. It means the result is better than before and you are ready to lock in that progress. In practice, commits often get postponed — changes that were acceptable (even if not ideal) accumulate, and then a single breaking change ruins everything that had been working. The more frequently you commit, the easier recovery becomes.

This mindset does take some getting used to. After all, you will essentially be committing code you did not write yourself — the AI wrote it. That shifts the mental model: instead of reviewing your own work before committing, you are reviewing and accepting (or rejecting) the AI's output. Commit what works, discard what does not.

### ✅ Result
You understand why small, committed changes beat large, uncommitted ones — especially with AI assistants.

## Page 2: Set Up a Practice Project
### Background
Before learning `Git` commands, you need a small project to practice on. You will ask the AI assistant to generate a simple calculator project, then use `Git` to track changes to it throughout this module.

### Steps
1. In your IDE, open the workspace folder: `c:\workspace\hello-genai\` (`Windows`) or `~/workspace/hello-genai/` (`macOS`/`Linux`).
2. Create a subfolder: `work/module03-task`. All course exercises go in `work/`[module-number]-task.
![Create new folder](image.png)
3. Open the chat and ask the AI assistant in `Agent` mode:
   Create a simple `Python` calculator project with:
   - `calculator.py` with add() and subtract() functions
   - `main.py` that uses the calculator
   - `README.md` with project description
   Place these files in the `work/module03-task` directory.
![Ask to create file - VSCode](image-1.png)
![Ask to create file - Cursor](image-2.png)
4. Verify that three files appear in `work/module03-task`: `calculator.py`, `main.py`, and `README.md`.
![Check result - VSCode](image-3.png)
![Check result - Cursor](image-4.png)

### ✅ Result
You have a small practice project with three files ready for version control.

> **Note:** Next in this module, screenshots are shown for one IDE only. Since `VS Code` and `Cursor` share the same foundation, the same functionality is easy to locate in the other — they are like twin brothers. If you see a screenshot from `VS Code` and you are using `Cursor`, the interface will look nearly identical.

## Page 3: Initialize `Git` and Configure Identity
### Background
`Git` needs to be initialized in your project folder before it can track changes. You also need to tell `Git` who you are — your `name` and `email` appear in every commit, creating an audit trail of who changed what.

### Steps
1. In the terminal (make sure you are inside work/060-task/), run:
   git init
2. Run:
   git status
   You should see all project files listed as "Untracked" — `Git` knows the files exist but is not tracking them yet.
3. Configure your identity. Ask the AI:
   I need to configure `Git` with my identity. My name is [Your Name] and email is [your@email.com]. What commands should I run?
4. The AI will suggest:
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
5. Run those commands, then verify:
   git config --global --list

### ✅ Result
`Git` is initialized in your project folder. Your name and email are configured.

## Page 4: Create `.gitignore` and First Commit
### Background
Not every file belongs in version control. Secrets (`API keys`, passwords), temporary files, and IDE configuration should be excluded. A `.gitignore` file tells `Git` which files to skip.

### Steps
1. Ask the AI:
   Create a `.gitignore` file for a `Python` project. Include virtual environments, cache files, secrets/environment files, IDE configuration, and any files in a temp/ directory.
2. Review the generated `.gitignore` — make sure it includes `.env` and other sensitive file patterns.
3. Now stage all project files for your first commit. In the IDE, open the `Source Control` panel (look for the branch icon in the left sidebar). You should see all changed files listed.
4. Click the + icon next to each file to stage it (or run git add . in terminal to stage everything).
5. Type a commit message: Initial calculator with add and subtract.
6. Click the commit button (or run git commit -m "Initial calculator with add and subtract" in terminal).

### ✅ Result
Your first commit is saved. You now have a baseline snapshot to return to at any time.

## Page 5: Practice the Baby Steps Workflow
### Background
Now that you have a baseline, practice the core loop: make a change → test → stage → commit. You will also practice recovering from a mistake — the most valuable skill when working with AI.

### Steps
1. Ask the AI:
   Add a multiply() function to `calculator.py`
2. After the AI adds the function, test it — run the code and verify multiply works.
3. Stage `calculator.py` immediately (click + in `Source Control` or run git add `calculator.py`). Do not commit yet — you are building up a feature.
4. Ask the AI:
   Update `main.py` to demonstrate the multiply() function
5. Test that both files work together. Stage `main.py`.
6. Ask the AI:
   Update `README.md` to document the multiply function
7. Review the README. Stage it. Now commit:
   git commit -m "Add multiply function"

The feature took three small steps instead of one big confusing change. Each step was verified before moving on.

**Tip: not every AI-generated file belongs in `Git`.** As your project grows, the AI may create temporary scripts, test data, or scaffolding files. Before staging everything with git add ., ask the AI:
   Which of my project files are production code and which are temporary scaffolding? List them in two groups.
Then stage only the production files and add scaffolding patterns to `.gitignore`.

### ✅ Result
You completed a feature using baby steps: three small changes, each tested and staged, then committed as one unit.

## Page 6: Recover from an AI Mistake
### Background
This is the most important exercise in the module. You will deliberately create a situation where the AI breaks your code — and then recover using `Git`. This builds the muscle memory you need when it happens for real (and it will).

### Steps
1. Ask the AI:
   Add a divide() function to `calculator.py`
2. Do NOT stage or commit yet.
3. Now ask the AI to do something risky:
   Refactor `calculator.py` to use a class-based structure
4. Check if `main.py` still works. It likely does not — the refactoring changed too much.
5. Since you did not stage the refactoring, discard it:
   - IDE: Right-click `calculator.py` in `Source Control` → Discard Changes.
   - Terminal: git checkout -- `calculator.py`
6. Notice that your divide() function is also gone — it was never staged.
7. This demonstrates the lesson: if you had staged divide() when it worked, you could recover it now. Always stage working code immediately.

**What if you already committed the bad change?** If you committed the refactoring before realizing it broke things, you have two options:
- git revert HEAD — creates a new commit that undoes the last one (safe, preserves history).
- git reset --hard HEAD~1 — removes the last commit entirely (destructive, use with caution).

Page 6 covers the more common case (discarding unstaged changes), but knowing both recovery paths ensures you are never stuck.

### ✅ Result
You practiced recovering from an AI mistake using git checkout. You understand why staging after each working change is critical — and you know how to undo a committed mistake if needed.

## Page 7: Push to `GitHub` (Optional)
### Background
Pushing your repository to `GitHub` creates a remote backup. If your local machine has issues, your code is safe in the cloud. This step is optional but recommended — you will use `GitHub` features in later modules.

This is also the moment to initialize the repository you will use for the practical project throughout the course. In Module 08, you will define a `Jira`/Confluence automation project — but you can create the repo for it now.

### Steps
1. Go to [https://github.com/new](https://github.com/new) in your browser.
2. Name the repository: jira-confluence-automation (or git-baby-steps-practice if you prefer to start with a generic name and rename later).
3. Choose Public or Private (your preference).
4. Do NOT check "Initialize this repository" — you already have local files.
5. Click Create repository.
6. Ask the AI:
   I created a `GitHub` repo at https://github.com/[username]/git-baby-steps-practice. How do I connect my local repository and push?
7. The AI will provide commands like:
   git remote add origin https://github.com/[username]/git-baby-steps-practice.git
   git branch -M main
   git push -u origin main
8. Run the commands. Your code is now on `GitHub`.

### ✅ Result
Your project is backed up to `GitHub`. You can continue making baby steps and push regularly.

**Practical project note:** This repository will become the home for your `Jira`/Confluence Automation Toolkit — a project you will define in Module 08 and build throughout the rest of the course. Every module from here on uses the baby steps workflow you just learned: change → test → stage → commit → push.

## Summary
Remember the scenario from the introduction — two hours of work destroyed by one careless AI refactoring? With the baby steps workflow, that situation is impossible. Every working change is staged, every complete feature is committed, and recovery is one command away.

Key takeaways:
- `Git` is your safety net when working with an AI assistant. Stage and commit after every successful change.
- Baby steps keep your working memory manageable and your project always recoverable.
- If the AI breaks something, discard the changes and try again — never lose working code.
- The AI generates code and suggests changes, but you control `Git`. You decide what gets staged, committed, and pushed.
- The workflow: change → test → stage → (repeat) → commit.

## Quiz
1. Why is it important to commit after every small successful change when working with an AI assistant?
   a) Because each commit creates a recovery point you can return to if the AI breaks something in a later change.
   b) Because `Git` repositories have a maximum file size and frequent commits keep files small.
   c) Because the AI assistant reads the commit history to understand your project better.
   Correct answer: a.
   - (a) is correct because each commit is a snapshot you can restore if a subsequent AI-generated change breaks your project.
   - (b) is incorrect because `Git` does not require frequent commits for file size reasons — it handles large files independently of commit frequency.
   - (c) is incorrect because while some AI tools can read `Git` history, the primary reason for frequent commits is recoverability, not AI context.

2. Your AI assistant refactored `calculator.py` and broke the existing functionality. You have not staged or committed the refactoring. What is the most appropriate next step?
   a) Ask the AI to undo its own changes by describing what the code looked like before.
   b) Discard the uncommitted changes using git checkout to restore the last staged or committed version, then try a different approach.
   c) Copy the broken code into a separate file for reference, then manually rewrite the original.
   Correct answer: b.
   - (a) is incorrect because asking the AI to undo its own changes risks introducing additional errors — the AI may not accurately remember the previous state.
   - (b) is correct because discarding uncommitted changes restores the last known working state instantly, which is faster and more reliable than any other recovery method.
   - (c) is incorrect because manually copying and rewriting wastes time when `Git` can restore the file in one command.

3. What is the purpose of a `.gitignore` file in a project repository?
   a) It lists file patterns that `Git` should not track — such as `API keys`, environment files, temporary caches, and IDE configuration.
   b) It speeds up `Git` operations by indexing only the files listed inside it.
   c) It encrypts sensitive files so they can be safely committed to the repository.
   Correct answer: a.
   - (a) is correct because the `.gitignore` file tells `Git` to exclude files matching specific patterns from version control, preventing secrets and machine-specific files from being accidentally committed.
   - (b) is incorrect because `.gitignore` has no effect on `Git`'s speed or indexing mechanism. It only controls which files are tracked.
   - (c) is incorrect because `.gitignore` does not encrypt anything — it simply prevents files from being tracked. Encryption requires separate tools.
