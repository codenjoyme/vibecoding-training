# Bulk File Processing with AI Agents - Hands-on Walkthrough

In this walkthrough, you'll learn three evolutionary approaches to processing multiple files with AI agents. You'll experience the limitations of each approach and implement the most efficient solution using GitHub Copilot CLI automation.

## Prerequisites

- GitHub Copilot extension installed and authorized in VS Code
- Access to a project with 6+ similar files (we'll use the training modules)
- Basic command line skills
- Python 3.10+ installed

## Part 1: Approach #1 - Single IDE Agent Request (Context Drift Problem)

Let's start with the simplest approach: asking the AI agent in IDE to process all files at once.

1. Open VS Code Agent Mode (chat panel)

2. Copy this prompt and send it:
   ```
   Review all walkthrough.md files in ./modules/ directory. For each file, check if it has:
   - Success Criteria section with checkboxes
   - Troubleshooting section
   - Next Steps section
   
   Create a summary of missing elements for each module.
   ```

3. Watch what happens as the agent processes files

You should see: The agent starts well, processes 3-5 files accurately, but then quality degrades. Later files get generic responses or hallucinated information. This is **context drift** - as conversation history grows, the model loses focus and accuracy decreases.

**Problem:** Works for ~5 files, fails for 20+. The agent's context window fills up with previous responses, causing hallucinations and inconsistencies.

## Part 2: Approach #2 - Iterative Prompting with Re-reading (Token Waste)

Now let's try being more explicit: tell the agent to re-read instructions for each file.

1. Create a file `validation-task.md` in `c:/workspace/hello-genai/work/160-task/` (Windows) or `~/workspace/hello-genai/work/160-task/` (macOS/Linux):
   ```markdown
   ## Validation Rules
   
   Every walkthrough.md must have:
   1. Success Criteria section with ✅ checkboxes
   2. Troubleshooting section with common problems
   3. Next Steps section pointing to next module
   4. No keyboard shortcuts mentioned
   5. Uses ./workspace/hello-genai/ as default path
   ```

2. Send this prompt to AI agent:
   ```
   For each walkthrough.md file in ./modules/:
   1. Read validation-task.md file
   2. Read the walkthrough.md file
   3. Check against validation rules
   4. Report issues
   5. Move to next file
   6. REPEAT from step 1
   
   Process modules: 010, 020, 030, 040, 050, 055
   ```

3. Observe the execution

You should see: The agent re-reads validation-task.md for EACH file. While this reduces context drift, it wastes tokens. For 20 files with 500-token instruction file, you're using 10,000+ tokens just re-reading the same instructions.

**Problem:** Better quality than Approach #1, but expensive and slow. Token costs multiply by number of files.

## Part 3: Approach #3 - Script-Based Automation (Best Practice)

The optimal solution: write a script that calls AI agent deterministically for each file with the same instruction.

### Step 3.1: Install GitHub Copilot CLI

Follow the complete guide: [GitHub Copilot CLI Installation](../../instructions/github-copilot-cli-installation.agent.md)

Quick steps (Windows):

1. Install nvm-windows from https://github.com/coreybutler/nvm-windows/releases

2. Install Node.js:
   ```powershell
   nvm install 20.19.0
   nvm use 20.19.0
   ```

3. Verify copilot CLI:
   ```powershell
   where.exe copilot
   ```

### Step 3.2: Test Copilot CLI

1. Set PATH (replace with your nvm path):
   ```powershell
   $env:PATH = "C:\Java\nvm\v20.19.0;$env:PATH"
   ```

2. Test with simple question:
   ```powershell
   copilot -p "What is 2+2?" --allow-all -s
   ```

You should see: Direct answer "4" without extra context or stats.

### Step 3.3: Examine the Automation Script

1. Navigate to module tools directory:
   ```powershell
   cd ./modules/160-bulk-file-processing-with-ai/tools
   ```

2. Open `validate_walkthroughs.py` in editor

3. Examine key parts:
   - **Line 14-17**: Configuration paths (nvm, copilot location)
   - **Line 32-34**: Finds all walkthrough.md files
   - **Line 44-48**: Changes to each module directory
   - **Line 52-58**: Calls copilot CLI with instruction file
   - **Line 64-66**: Checks for created todo.md file

Notice: The instruction file is read once by Copilot CLI for each module, but we don't pay token cost multiple times - CLI handles it efficiently.

### Step 3.4: Update Script Configuration

1. Find your nvm path:
   ```powershell
   where.exe nvm
   ```

2. Find your copilot path:
   ```powershell
   where.exe copilot
   ```

3. Edit `validate_walkthroughs.py`, update lines 16-17 with your paths

### Step 3.5: Run the Script

1. Return to workspace root:
   ```powershell
   cd ../../..
   ```

2. Run the validation script:
   ```powershell
   python ./modules/160-bulk-file-processing-with-ai/tools/validate_walkthroughs.py
   ```

You should see: For each module, the script changes directory, calls Copilot CLI, and creates `todo.md` with validation results. Output appears in real-time as each module processes.

3. Check results in any module:
   ```powershell
   cat ./modules/010-installing-vscode-github-copilot/todo.md
   ```

Verify that: Each `todo.md` contains specific issues found in that module's walkthrough.

### Step 3.6: Compare Approaches

Create comparison table:

| Approach | Token Cost | Quality | Speed | Files Limit |
|----------|------------|---------|-------|-------------|
| #1: Single Request | Low | Poor (drift) | Fast | ~5 files |
| #2: Iterative Re-read | High | Good | Slow | 20+ files |
| #3: Script Automation | Optimal | Excellent | Fast | Unlimited |

**Why Approach #3 Wins:**
- **No context drift**: Each file processed in fresh context
- **Token efficient**: Instruction read once per file by CLI, not accumulated
- **Deterministic**: Same instruction applied consistently
- **Scalable**: Works for 100+ files
- **Auditable**: Each result saved in separate file

## Success Criteria

✅ Attempted Approach #1 and observed context drift after ~5 files  
✅ Attempted Approach #2 and recognized token waste from re-reading  
✅ Installed GitHub Copilot CLI with Node.js via nvm-windows  
✅ Verified copilot CLI works with test question  
✅ Configured and ran validate_walkthroughs.py script  
✅ Generated todo.md files in all processed module directories  
✅ Understand trade-offs: context drift vs. token cost vs. automation

## Troubleshooting

### Issue: "copilot: command not found"

**Solution:** Copilot CLI is installed with VS Code Copilot extension. Verify:
```powershell
where.exe copilot
```

If not found, reinstall GitHub Copilot extension in VS Code.

### Issue: Python script fails with "No module named 'subprocess'"

**Solution:** Update Python to 3.10+:
```powershell
python --version
```

### Issue: Copilot CLI asks questions instead of executing

**Solution:** Use `--no-ask-user` flag:
```powershell
copilot -p "@instruction.md" --add-dir "." --allow-all --no-ask-user -s
```

### Issue: Script creates empty todo.md files

**Solution:** Check instruction file path is correct relative to module directory. The script changes to each module directory, so paths must be relative from there.

### Issue: "The command line is too long"

**Solution:** Use file references with `@` prefix instead of inline text:
```powershell
# Bad: passing large text inline
copilot -p "very long instruction text..."

# Good: reference file
copilot -p "@instruction.md" --allow-all -s
```

## When to Use Each Approach

**Approach #1 - Single IDE Agent Request:**
- Quick ad-hoc checks
- 3-5 files maximum
- Acceptable quality loss
- No automation needed

**Approach #2 - Iterative Re-reading:**
- 10-15 files
- High quality required
- One-time operation (token cost acceptable)
- No time to write script

**Approach #3 - Script Automation:**
- 20+ files
- Consistent quality critical
- Repeated operations
- Integration into CI/CD pipelines
- Token efficiency matters

## Next Steps

You've mastered bulk file processing with AI agents! This pattern works for any repetitive AI task: code reviews, documentation generation, test writing, refactoring checks.

Next module: **170-github-issues-mass-processing** - Apply this pattern to process GitHub issues and PRs at scale.

---

**Key Takeaway:** When processing many files with AI, don't fight context drift - embrace script automation with fresh contexts per file. Model Claude Sonnet 4.5 with Agent Mode enabled provides best results for these operations.
