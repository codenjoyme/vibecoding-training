Module 3: Version Control with Git

Background
Imagine spending two hours building something that works perfectly — then asking the AI to "make one small improvement" and watching everything break. You try to undo, but the AI has already changed too many files. Your working version is gone.

This scenario happens to everyone who works with AI assistants without a safety net. Git is that safety net. It is a version control system that saves snapshots of your project at any point. If something goes wrong, you restore the last working snapshot in seconds.

In this module, you will learn the "baby steps" methodology: make one small change, verify it works, save a snapshot, then move on. This approach keeps your working memory manageable and your project always recoverable. You will use Git for every subsequent module in this course.

Page 1: Why Baby Steps Matter
Background
Your brain can hold roughly 7±2 items in working memory simultaneously. When you try to implement three features at once, each new detail pushes out an earlier one, leading to confusion and mistakes. The baby steps approach respects this cognitive limit.

Consider two approaches to implementing three features:

Approach A (Baby steps): 3 sessions × 15 minutes = 45 minutes total. Each session focuses on one feature, commits it, and moves on with a clear head.

Approach B (All at once): 1 session of 2–3 hours. You keep all three features in your head, context-switch between them, and spend extra time untangling mistakes.

Baby steps are faster, safer, and less stressful — especially when working with an AI assistant that might occasionally break things while "improving" them.

The workflow is simple:
- Make a small change.
- Test it — does it work?
- If yes: save a snapshot (git add + git commit).
- If no: discard the change and try again (git checkout).
- Repeat.

✅ Result
You understand why small, committed changes beat large, uncommitted ones — especially with AI assistants.

Page 2: Set Up a Practice Project
Background
Before learning Git commands, you need a small project to practice on. You will ask the AI assistant to generate a simple calculator project, then use Git to track changes to it throughout this module.

Steps
1. In your IDE, open the workspace folder: c:/workspace/hello-genai/ (Windows) or ~/workspace/hello-genai/ (macOS/Linux).
2. Create a subfolder: work/060-task. All course exercises go in work/[module-number]-task.
3. Open the terminal in your IDE (Terminal menu > New Terminal) and navigate to the work/060-task folder.
4. Ask the AI assistant:
   Create a simple Python calculator project with:
   - calculator.py with add() and subtract() functions
   - main.py that uses the calculator
   - README.md with project description
   Place these files in the current directory.
5. Verify that three files appear in work/060-task/: calculator.py, main.py, and README.md.

✅ Result
You have a small practice project with three files ready for version control.

Page 3: Initialize Git and Configure Identity
Background
Git needs to be initialized in your project folder before it can track changes. You also need to tell Git who you are — your name and email appear in every commit, creating an audit trail of who changed what.

Steps
1. In the terminal (make sure you are inside work/060-task/), run:
   git init
2. Run:
   git status
   You should see all project files listed as "Untracked" — Git knows the files exist but is not tracking them yet.
3. Configure your identity. Ask the AI:
   I need to configure Git with my identity. My name is [Your Name] and email is [your@email.com]. What commands should I run?
4. The AI will suggest:
   git config --global user.name "Your Name"
   git config --global user.email "your@email.com"
5. Run those commands, then verify:
   git config --global --list

✅ Result
Git is initialized in your project folder. Your name and email are configured.

Page 4: Create .gitignore and First Commit
Background
Not every file belongs in version control. Secrets (API keys, passwords), temporary files, and IDE configuration should be excluded. A .gitignore file tells Git which files to skip.

Steps
1. Ask the AI:
   Create a .gitignore file for a Python project. Include virtual environments, cache files, secrets/environment files, IDE configuration, and any files in a temp/ directory.
2. Review the generated .gitignore — make sure it includes .env and other sensitive file patterns.
3. Now stage all project files for your first commit. In the IDE, open the Source Control panel (look for the branch icon in the left sidebar). You should see all changed files listed.
4. Click the + icon next to each file to stage it (or run git add . in terminal to stage everything).
5. Type a commit message: Initial calculator with add and subtract.
6. Click the commit button (or run git commit -m "Initial calculator with add and subtract" in terminal).

✅ Result
Your first commit is saved. You now have a baseline snapshot to return to at any time.

Page 5: Practice the Baby Steps Workflow
Background
Now that you have a baseline, practice the core loop: make a change → test → stage → commit. You will also practice recovering from a mistake — the most valuable skill when working with AI.

Steps
1. Ask the AI:
   Add a multiply() function to calculator.py
2. After the AI adds the function, test it — run the code and verify multiply works.
3. Stage calculator.py immediately (click + in Source Control or run git add calculator.py). Do not commit yet — you are building up a feature.
4. Ask the AI:
   Update main.py to demonstrate the multiply() function
5. Test that both files work together. Stage main.py.
6. Ask the AI:
   Update README.md to document the multiply function
7. Review the README. Stage it. Now commit:
   git commit -m "Add multiply function"

The feature took three small steps instead of one big confusing change. Each step was verified before moving on.

✅ Result
You completed a feature using baby steps: three small changes, each tested and staged, then committed as one unit.

Page 6: Recover from an AI Mistake
Background
This is the most important exercise in the module. You will deliberately create a situation where the AI breaks your code — and then recover using Git. This builds the muscle memory you need when it happens for real (and it will).

Steps
1. Ask the AI:
   Add a divide() function to calculator.py
2. Do NOT stage or commit yet.
3. Now ask the AI to do something risky:
   Refactor calculator.py to use a class-based structure
4. Check if main.py still works. It likely does not — the refactoring changed too much.
5. Since you did not stage the refactoring, discard it:
   - IDE: Right-click calculator.py in Source Control → Discard Changes.
   - Terminal: git checkout -- calculator.py
6. Notice that your divide() function is also gone — it was never staged.
7. This demonstrates the lesson: if you had staged divide() when it worked, you could recover it now. Always stage working code immediately.

✅ Result
You practiced recovering from an AI mistake using git checkout. You understand why staging after each working change is critical.

Page 7: Push to GitHub (Optional)
Background
Pushing your repository to GitHub creates a remote backup. If your local machine has issues, your code is safe in the cloud. This step is optional but recommended — you will use GitHub features in later modules.

Steps
1. Go to https://github.com/new in your browser.
2. Name the repository: git-baby-steps-practice.
3. Choose Public or Private (your preference).
4. Do NOT check "Initialize this repository" — you already have local files.
5. Click Create repository.
6. Ask the AI:
   I created a GitHub repo at https://github.com/[username]/git-baby-steps-practice. How do I connect my local repository and push?
7. The AI will provide commands like:
   git remote add origin https://github.com/[username]/git-baby-steps-practice.git
   git branch -M main
   git push -u origin main
8. Run the commands. Your code is now on GitHub.

✅ Result
Your project is backed up to GitHub. You can continue making baby steps and push regularly.

Summary
In this module, you learned the baby steps methodology for working with AI assistants: make one small change, test it, stage it, commit it, then move on. You also practiced the most critical skill — recovering from an AI mistake by discarding uncommitted changes.

Key takeaways:
- Git is your safety net when working with an AI assistant. Stage and commit after every successful change.
- Baby steps keep your working memory manageable and your project always recoverable.
- If the AI breaks something, discard the changes and try again — never lose working code.
- The workflow: change → test → stage → (repeat) → commit.

Quiz
1. Why is it important to commit after every small successful change when working with an AI assistant?
   a) To generate a longer commit history
   b) Because each commit creates a recovery point you can return to if the AI breaks something
   c) Because Git requires frequent commits to function properly
   Correct answer: b. Each commit is a snapshot you can restore if a subsequent AI-generated change breaks your project.

2. What should you do if the AI refactors your code and breaks existing functionality?
   a) Ask the AI to fix it, adding more changes on top
   b) Discard the uncommitted changes using git checkout and try a different approach
   c) Delete the project and start over
   Correct answer: b. Discarding uncommitted changes restores the last known working state, which is faster and safer than trying to fix broken refactoring.

3. What is the purpose of a .gitignore file?
   a) It tells Git to ignore all files in the project
   b) It lists file patterns that Git should not track — such as secrets, temporary files, and IDE configuration
   c) It prevents other developers from reading your code
   Correct answer: b. The .gitignore file excludes sensitive, temporary, and machine-specific files from version control.
