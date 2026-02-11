# GitHub Coding Agent Delegation - Hands-on Walkthrough

You've learned how to create GitHub issues through MCP integration in Module 105. Now it's time to take it to the next level: **delegate complete implementation tasks to GitHub Copilot Coding Agent**. This autonomous agent will read your issue, analyze the codebase, write the code, and create a pull request—all while you work on other tasks.

## Prerequisites

- Completed [Module 105: MCP GitHub Integration - Issues](../105-mcp-github-integration-issues/about.md)
- Active GitHub Copilot subscription with access to GitHub Coding Agent
- GitHub repository with at least one issue created
- Understanding of Git pull requests and code review workflow
- Workspace with `.github/copilot-instructions.md` or instruction files

## What We'll Build

In this hands-on walkthrough, you'll:
- Understand GitHub Copilot Coding Agent capabilities and limitations
- Assign an agent to a GitHub issue for autonomous implementation
- Monitor agent progress through GitHub interface
- Review agent's work log and implementation decisions
- Perform code review on agent-generated pull request
- Iterate with the agent through review comments
- Accept and merge the pull request
- Handle agent errors and instruction file improvements

**Time required:** 20-30 minutes

---

## Part 1: Understanding GitHub Copilot Coding Agent

### What Makes Coding Agent Different

GitHub Copilot has multiple components:
- **IDE Assistant** (VS Code/Cursor): Real-time code suggestions, chat-based coding
- **Coding Agent**: Autonomous task execution on GitHub's infrastructure
- **PR Reviews**: Automated code review feedback

**Coding Agent characteristics:**
- **Autonomous**: Works independently after assignment
- **Server-side**: Runs on GitHub's infrastructure, not your machine
- **Full repository access**: Reads entire codebase for context
- **Creates PRs**: Generates pull requests with complete implementation
- **Session logs**: Provides detailed work log for transparency
- **Model selection**: Can choose from multiple models (GPT-5.2-Codex, Claude Opus 4.6, Claude Sonnet 4.5, etc.) or use Auto mode
- **Different from IDE**: Server-side models may behave differently than your IDE's Claude assistant

### When to Use Coding Agent

**Ideal for:**
- Well-defined tasks with clear requirements
- Repetitive implementation work (similar patterns)
- Tasks that can be validated through tests
- Multiple features to implement in parallel
- Creating boilerplate code structures
- Refactoring with clear specifications

**Not ideal for:**
- Exploratory work requiring human judgment
- Complex architectural decisions
- Tasks requiring external tool access
- Urgent fixes (agent takes 15-30 minutes)
- Vague or ambiguous requirements

### The Key Success Factor: Instruction Files

The agent's behavior is guided by instruction files in your repository. These files **must be created and maintained** for the agent to work correctly.

**Critical instruction files (learned in [Module 070: Custom Instructions](../070-custom-instructions/about.md)):**
- `.github/copilot-instructions.md` - Main entry point for agent
- `./instructions/*.agent.md` - Domain-specific instruction files (e.g., `create-tool.agent.md`, `testing-tool.agent.md`)
- Project-specific configuration files

In Module 070, you learned how to create reusable instruction files that guide AI behavior consistently. GitHub Coding Agent uses these same instruction files to understand your project conventions and coding standards.

**Without proper instructions:**
- Agent may misunderstand requirements
- Implementation style won't match your standards
- Agent might miss critical project conventions
- You'll spend more time fixing than if you coded yourself

**The golden rule:** If the agent makes mistakes, **update your instruction files** to prevent the same mistakes in future sessions.

---

## Part 2: The Complete Agent Delegation Workflow

### Overview of the Process

Here's the complete workflow you'll learn:

1. **Preparation** (in IDE):
   - Create a well-defined GitHub issue (already learned in Module 105)
   - Ensure instruction files are up to date
   - Commit and push latest code

2. **Assignment** (two options):
   - **Option A:** Through GitHub web interface (shown in this walkthrough)
   - **Option B:** Using GitHub MCP from IDE (same as Module 105)
   - Navigate to the issue and assign GitHub Copilot
   - Provide optional custom instructions

3. **Monitoring** (background):
   - Agent works autonomously
   - Check progress through GitHub issue comments
   - Continue working on other tasks

4. **Review** (GitHub web interface):
   - Review generated pull request
   - Check agent's work log
   - Add review comments for changes

5. **Iteration** (if needed):
   - Agent responds to review comments
   - Makes requested changes
   - Updates pull request

6. **Completion**:
   - Approve and merge pull request
   - Update instruction files based on learnings
   - Close the issue

Let's walk through each step in detail.

---

## Part 3: Preparation - Creating the Task

### What We'll Do

We'll use the issue created in Module 105 as our task. In Module 105, you already learned how to create GitHub issues through MCP integration using AI chat. If you don't have an issue yet, we'll create one now using the same technique.

### Step 1: Create or Locate GitHub Issue

**If you already have an issue from Module 105:**
- Locate the issue you created for a new training module (e.g., "New Module: AI-Generated API Documentation" - Module 165)
- This issue contains requirements for creating a new training module about generating API documentation
- Note the issue number (e.g., #5)
- Skip to Step 2

**If you need to create a new issue:**

Use the same process you learned in Module 105 - conduct an interactive requirements interview with AI and create a GitHub issue through MCP. 

In Module 105, you practiced creating an issue for a new training module by interviewing AI about module requirements. Now you'll delegate the implementation of that module to GitHub Coding Agent.

For details on the interview process, refer to [Module 105, Part 5: Interactive Requirements Interview](../105-mcp-github-integration-issues/walkthrough.md#part-5-interactive-requirements-interview).

The issue should have:
- Clear title describing the task
- Detailed requirements and acceptance criteria
- Links to relevant instruction files (if applicable)
- Proper labels

**Once you have an issue ready, continue to Step 2.**

### Step 2: Review Issue Quality

Open the issue you created (either in Module 105 or just now) on GitHub.

**Check that the issue has:**
- ✅ Clear, descriptive title
- ✅ Detailed requirements with numbered steps
- ✅ Technical specifications
- ✅ Links to relevant instruction files
- ✅ Expected outcome
- ✅ Acceptance criteria (optional but helpful)

**Why this matters:**
The agent will use this issue as its primary source of truth. Poor issue quality = poor implementation.

### Step 3: Verify Instruction Files

The agent will read your instruction files to understand project conventions. Let's verify they exist.

**These are the instruction files you created in Module 070.** They guide both your IDE assistant and GitHub Coding Agent to work consistently with your project standards.

Ask your AI assistant:
```
Check if we have these instruction files and show me their locations:
- .github/copilot-instructions.md (or similar)
- ./instructions/*.agent.md files
```

**Expected output:**
```
Found instruction files:
- .github/copilot-instructions.md
- instructions/main.agent.md
- instructions/create-training-module.agent.md
- instructions/git-workflow.agent.md
... (other instruction files from Module 070)
```

**If instruction files are missing:**
- Review [Module 070: Custom Instructions](../070-custom-instructions/about.md) to create them
- Create `.github/copilot-instructions.md` as the main entry point
- Ensure instruction files follow the pattern you want the agent to use

**Example .github/copilot-instructions.md:**
```markdown
# Copilot Agent Instructions

- Always read ./instructions/main.agent.md first
- This file contains links to all other instruction files
- Follow instructions for the specific task type
```

**Why this matters:**
In Module 070, you learned to create instructions that work in the IDE. The same instruction files guide GitHub Coding Agent on the server. This ensures consistent behavior across all AI tools in your workflow.

### Step 4: Commit and Push Latest Changes

Before assigning the agent, ensure your latest code is on GitHub.

Ask your AI assistant:
```
Check if there are uncommitted changes and push them to GitHub
```

**Why this matters:**
The agent works with the latest code on GitHub. Any uncommitted local changes won't be visible to the agent.

---

## Part 4: Assigning the Agent to Issue

### What We'll Do

Now we'll assign GitHub Copilot Coding Agent to our issue. You have two options:

**Option A: GitHub Web Interface** (shown in this walkthrough)
- Visual, intuitive interface
- Good for learning and understanding the process
- See all assignment options clearly

**Option B: GitHub MCP from IDE** (learned in Module 105)
- Stay in your IDE, no browser context-switching
- Use AI assistant to assign agent with a simple command
- Faster once you're familiar with the process

**For this walkthrough, we'll use Option A (web interface)** to see the complete process visually. After mastering it, you can switch to Option B for efficiency.

### Option A: Assigning Through Web Interface

### Step 1: Navigate to Issue on GitHub

Open your browser and navigate to:
```
https://github.com/YOUR-USERNAME/YOUR-REPO/issues/ISSUE-NUMBER
```

For example:
```
https://github.com/codenjoyme/vibecoding-training/issues/1
```

You should see your issue with all the details you created.

### Step 2: Locate "Assign to Copilot" Button

On the issue page, look in the **right sidebar** under the **"Assignees"** section.

You'll see:
- "No one — Assign yourself" link
- **"Assign to Copilot"** button with Copilot icon

The button is clearly visible in the Assignees section and doesn't require any additional clicks or menu navigation.

### Step 3: Click "Assign Copilot"

Click the button to start the assignment dialog.

**What happens:**
- GitHub checks your Copilot subscription
- Validates you have permission to use Coding Agent
- Opens configuration dialog for the assignment

### Step 4: Configure Agent Assignment

The assignment dialog opens with the title **"Assign Copilot to issue"**.

**Dialog components:**

**1. Description at the top:**
"Copilot will open a pull request using the issue's description, comments, and the additional prompt if you provide one. Choose a custom agent to tailor Copilot for specific tasks."

**2. Optional prompt:**
- Large text area with placeholder: "Provide additional instructions for Copilot"
- Additional context beyond the issue description
- Constraints or preferences for this specific task
- Examples: "Use pytest for testing" or "Follow existing code style in X module"

**3. Models selection (dropdown):**
- **Auto** (default, marked with checkmark) - Let Copilot choose the best model
- **Claude Opus 4.6** (3×) - More powerful, uses more resources
- **GPT-5.2-Codex** (1×) - GitHub's specialized coding model
- **GPT-5.1-Codex-Max** (1×) - Extended context version
- **Claude Sonnet 4.5** (1×) - Balance of speed and capability

The multipliers (1×, 3×) indicate how many premium requests the model consumes.

**4. Agents selection:**
- **Copilot** (default) - Standard GitHub Copilot agent
- **Create a custom agent** - Configure specialized agent for specific tasks

**5. Repository selection:**
- Dropdown showing your repository (e.g., `codenjoyme/vibecoding-for-managers...`)
- Can select different repository if working across multiple repos
- Search functionality to find specific repository

**6. Base branch selection:**
- Click to open "Select base branch" dialog
- Shows: "Pick the starting point that Copilot will use when it creates a new branch"
- Default: `main` (marked as "default")
- Search field to find specific branch
- Agent will create new branch from selected base

**7. Action buttons:**
- **Cancel** - Close dialog without assigning
- **Assign** - Confirm and start agent work

**For this walkthrough:**
- Leave model as **"Auto"** (recommended for learning)
- Keep agent as **"Copilot"** (standard agent)
- Keep repository as your current repository
- Keep base branch as **"main"**
- Leave "Optional prompt" empty (we'll rely on instruction files from Module 070)
- Ready to click "Assign"

**Advanced usage notes:**
- **Model selection**: Choose specific model when you know task requirements (e.g., Claude Opus for complex logic, GPT-5.2-Codex for standard coding)
- **Custom agents**: Create specialized agents for recurring task types (e.g., "Testing Agent", "Documentation Agent")
- **Repository selection**: Useful when agent needs to work across multiple repos or forks
- **Branch selection**: Select feature branch if you want agent to build on existing work

### Step 5: Confirm Assignment

Click **"Assign"** or **"Assign GitHub Copilot to issue #5"**

**What happens immediately:**
1. GitHub assigns Copilot user to the issue
2. Copilot comments: "Thanks for asking me to work on this. I will get started..."
3. Issue status remains Open
4. Agent begins working in the background

### Step 6: Verify Assignment

After clicking assign, you should see:

**In the issue timeline:**
- Event: "Copilot assigned Copilot and codenjoyme" (or your username)
- Comment from Copilot: Initial acknowledgment

**In the right sidebar:**
- Assignees: Shows Copilot icon
- Labels: May auto-add labels like "work-in-progress"

**What we accomplished:**
- Delegated a complete implementation task to an autonomous agent
- Agent has full context (issue + instruction files + codebase)
- You're free to work on other tasks while agent works

---

### Option B: Assigning Through GitHub MCP (Alternative)

If you prefer to stay in your IDE (as learned in Module 105), you can assign the agent using GitHub MCP.

**Ask your AI assistant:**
```
Assign GitHub Copilot coding agent to issue #5 in this repository
```

**What happens:**
- AI uses GitHub MCP tool: `mcp_github_assign_copilot_to_issue`
- Parameters: repository, issue number, optional base branch, optional custom instructions
- Approval dialog shows the assignment details
- Click "Allow" to confirm

**Approval dialog shows:**
- Tool: `mcp_github_assign_copilot_to_issue`
- Parameters:
  ```json
  {
    "owner": "YOUR-USERNAME",
    "repo": "YOUR-REPO",
    "issue_number": 5,
    "base_ref": "main"
  }
  ```

**Benefits of MCP approach:**
- No context-switching to browser
- Faster workflow once familiar
- Can script multiple agent assignments
- Consistent with other MCP operations learned in Module 105

**Result is the same:**
- Agent is assigned to the issue
- Agent comments on the issue
- Agent begins working in background
- You receive the same notifications and PR

**Choose the approach that fits your workflow:**
- Web interface: Better for learning, visual feedback
- GitHub MCP: Better for efficiency, staying in flow

---

## Part 5: Monitoring Agent Progress

### What We'll Do

While the agent works (typically 15-30 minutes), you can monitor progress without blocking your own work.

### Step 1: Check Issue Comments

The agent provides status updates through issue comments.

**Navigate back to the issue page:**
```
https://github.com/YOUR-USERNAME/YOUR-REPO/issues/ISSUE-NUMBER
```

**Look for Copilot comments:**
- "Copilot started work on behalf of codenjoyme X minutes ago"
- Progress updates (if any)
- Links to view the work session

### Step 2: View Work Session (Optional)

Some comments include a **"View session"** button.

**Clicking "View session" shows:**
- Agent's development log
- Files being read and analyzed
- Decisions being made
- Code being written
- Tools being executed

**What to look for in the session log:**
- Does agent start by reading instruction files? (Good sign!)
- Is it reading relevant files from your codebase?
- Are tool executions successful or failing?
- Any error messages or misunderstandings?

**Example good session start:**
```
I'll start by exploring the repository structure to understand the training modules...

Reading: ./instructions/main.agent.md
Reading: ./instructions/create-training-module.agent.md
Reading: docs/modules/160-bulk-file-processing-with-ai/about.md (for reference)
Reading: docs/training-plan.md (to determine module number)
```

**Example concerning session start:**
```
I'll create the new training module about API documentation...
[Directly starts creating files without reading create-training-module.agent.md instructions]
```

If you see the concerning pattern, you may want to:
- Cancel the agent (close the issue)
- Improve your `.github/copilot-instructions.md` to emphasize reading instructions first
- Add explicit instruction to "Always start by reading ./instructions/main.agent.md"

### Step 3: Understand Agent Model Differences

**Critical insight:**

The GitHub Copilot Coding Agent can use **different models** than your IDE. While your IDE typically uses Claude Sonnet 4.5, the agent offers multiple model choices:
- **Auto mode** (default) - GitHub selects the best model for the task
- **GPT-5.2-Codex** / **GPT-5.1-Codex-Max** - Specialized for code generation
- **Claude Opus 4.6** / **Claude Sonnet 4.5** - Strong reasoning capabilities

**Key implications:**
- Different models = different behavior and capabilities
- Instructions that work perfectly in IDE (Claude) may need adjustment for Agent models
- Each model has different strengths:
  - **GPT Codex**: Extensive training on public GitHub code, excellent for common patterns
  - **Claude**: Strong reasoning, better for complex logic and architecture decisions
- Environment differences: Server-side execution vs. your local IDE environment
- You may need separate instructions for IDE vs Agent
- Test agent behavior with your chosen model and refine instructions accordingly

**Important note:**
You may need to tune the instruction files that you fine-tuned for working with GitHub Copilot in the IDE, since different models are available in Copilot Agent and the environment on the server is not the same as yours in the IDE. This will lead to errors that you'll need to investigate and respond to.

**Recommendation for learning:**
Start with **Auto mode** to let GitHub choose the optimal model. As you gain experience, experiment with specific models for different task types (e.g., Claude Opus for complex architecture, GPT Codex for standard implementations).

### Step 4: Continue Your Work

**The beauty of agent delegation:**
While the agent works, you can:
- Implement other features
- Review other pull requests
- Write documentation
- Conduct planning sessions
- Take a break ☕

**No need to:**
- Wait for agent to finish
- Monitor constantly
- Remain in GitHub web interface

**Best practice:**
- Check back in 15-20 minutes
- Agent will notify you via GitHub notifications when PR is ready

---

## Part 6: Reviewing Agent's Work

### What We'll Do

The agent has finished and created a pull request. Now we'll review its work thoroughly.

### Step 1: Locate the Pull Request

**Option 1: From issue page**
- Navigate back to the issue
- Look for comment: "Copilot finished work on behalf of codenjoyme"
- Click the PR link in the comment

**Option 2: From Pull Requests tab**
- Navigate to: `https://github.com/YOUR-USERNAME/YOUR-REPO/pulls`
- Look for PR with title matching your issue
- Example: "[WIP] Create Module 165: AI-Generated API Documentation #3"

**PR indicators:**
- Title includes `[WIP]` or `[Draft]` - Work In Progress
- Shows branch: `copilot-fix-XXX-XXXX` → `main`
- Author: Copilot
- Reviewers: May auto-request you

### Step 2: Review PR Description

Open the pull request and read the description.

**Good PR description includes:**
- Summary of what was implemented
- Files changed
- Key decisions made
- Testing performed
- Links to related issue

**Example PR description:**
```
✅ Complete Implementation

Created new training module with the following structure:
- docs/modules/165-ai-generated-api-documentation/about.md - Module overview and metadata
- docs/modules/165-ai-generated-api-documentation/walkthrough.md - Hands-on step-by-step guide
- Updated docs/training-plan.md - Added module to sequence

✅ Module Components Implemented

1. about.md - Module description
   - Duration: 5-7 minutes
   - Skill description: Generate comprehensive API documentation using AI
   - Learning outcomes and prerequisites
   - Topics covered

2. walkthrough.md - Practical guide
   - Complete hands-on instructions
   - Step-by-step exercises
   - Success criteria checklist
   - Understanding check questions
   - Troubleshooting section

3. training-plan.md - Integration
   - Added module link in correct sequence
   - Proper numbering (Module 165)
```

### Step 3: Review Changed Files

Click the **"Files changed"** tab in the pull request.

**Review each file:**
- Does it match requirements from the issue?
- Is code quality acceptable?
- Are there any temporary/debug files included? (Bad!)
- Does it follow project conventions?
- Are there any security concerns?

**Example review checklist:**
- ✅ `docs/modules/165-ai-generated-api-documentation/about.md` - Module overview looks correct
- ✅ `docs/modules/165-ai-generated-api-documentation/walkthrough.md` - Step-by-step guide is comprehensive
- ✅ `docs/training-plan.md` - Module properly added to sequence
- ❌ `test-module.md` - Temporary file, should not be in PR
- ❌ `docs/modules/165-ai-generated-api-documentation/draft.md` - Draft file, should not be committed

### Step 4: Check Work Session Log

Before diving into code review, check the agent's work session for insights.

**Navigate back to the issue and find "View session" link.**

**Look for:**
- Did agent follow instruction files?
- What files did it read for context?
- Were there any errors during development?
- Did it run tests? What were the results?
- Any commands executed?

**Example session log:**
```
View docs/modules
  View ./instructions/main.agent.md
  View ./instructions/create-training-module.agent.md
  Read existing modules for structure reference
  Read docs/training-plan.md to determine module number
  Create about.md following template
  Create walkthrough.md with hands-on steps
  Update training-plan.md with new module link
```

**Good sign:** Agent systematically read relevant instruction files.

**Red flag:** Agent skipped instructions and went straight to coding.

### Step 5: Add Review Comments

Now perform detailed code review with specific feedback.

**Important advice:**
Don't submit each comment individually, as this will start a new session, which will cost you 1 premium request. Collect all your comments and send them in a single transaction.

**Step-by-step commenting:**

1. **Click "Review changes" button** (top-right of Files changed tab)

2. **For each issue, add inline comment:**
   - Click the line number where issue exists
   - Click "+" icon that appears
   - Write specific comment
   - Example: "❌ Please do not leave temporary files that you used for testing in the final PR."

3. **Don't submit yet!** Just click "Add single comment" for now

4. **Continue adding comments for all issues:**
   - "Remove test-module.md - temporary file"
   - "Remove draft.md from module directory"
   - "Add Understanding Check section to walkthrough.md"
   - "Fix module numbering in training-plan.md"
   - etc.

5. **After adding ALL comments, finalize review** (next step)

**Pro tip:** You can also chat with Copilot about specific files:
- Click "Ask Copilot" button
- Select files to discuss
- Ask questions about implementation decisions

### Step 6: Submit Review with Request Changes

After adding all inline comments, submit your review.

**Click "Review changes" button again** (top-right)

**In the review dialog:**

1. **Write summary comment:**
   ```
   Please fix comments:
   - Remove temporary files (test-module.md, draft.md)
   - Add Understanding Check section with 5-7 questions
   - Fix module numbering inconsistency
   ```

2. **Select "Request changes"**
   - NOT "Approve" (we need fixes first)
   - NOT "Comment" (just feedback, no action required)
   - "Request changes" = agent will work on fixes

3. **Click "Submit review"**

**What happens next:**
- Copilot receives your review
- Copilot comments on the PR acknowledging the feedback
- Copilot starts working on requested changes
- Copilot updates the same PR with new commits

**Example Copilot response:**
```
@codenjoyme I have uploaded the changes from my.uws-developer/.display as asked about in the future. Created: Promise 💓 before

Let me check the latest and respond to what you implemented
```

---

## Part 7: Reviewing Updated Pull Request

### What We'll Do

Copilot has responded to your review comments with new commits. Let's verify the fixes.

### Step 1: Check New Commits

Navigate to the PR's **"Commits"** tab or conversation timeline.

**Look for:**
- New commit(s) from Copilot
- Commit messages referencing your review comments
- Timestamps showing when work was done

**Example commit messages:**
```
2f1a285  Create Module 165: AI-Generated API Documentation with complete structure
95d796e  Final cleanup and add Understanding Check section to walkthrough
```

### Step 2: Review Changes

Go back to **"Files changed"** tab.

**Check that your requested changes were made:**
- ❌ Were temporary files removed? (test-module.md, draft.md)
- ❌ Was Understanding Check section added?
- ❌ Was module numbering fixed?
- ❌ Were all review comments addressed?

**Use the file filter if needed:**
- GitHub shows "Changes from all commits" by default
- You can filter to see only latest changes

### Step 3: Check PR Status Indicators

Look at the PR overview for status indicators:

**Green checkmarks indicate:**
- ✅ No conflicts with base branch
- ✅ All checks passed (if CI/CD configured)
- ✅ Merging can be performed automatically

**"This pull request is still a work in progress" means:**
- PR is in Draft mode
- Copilot may not be finished with requested changes
- May need to mark as "Ready for review" manually

### Step 4: Approve the Pull Request

If all issues are resolved:

1. **Click "Review changes"** button again

2. **Add final comment:**
   ```
   Changes reviewed:
   ✅ Temporary files removed
   ✅ Understanding Check section added with 7 questions
   ✅ Module structure follows training-module guidelines
   ✅ training-plan.md properly updated
   
   LGTM! (Looks Good To Me)
   ```

3. **Select "Approve"** (labeled 3 in review dialog)

4. **Click "Submit review"**

**What approval means:**
- You've verified the implementation
- Code quality meets standards
- Ready to merge into main branch
- No blocking issues remain

---

## Part 8: Merging the Pull Request

### What We'll Do

The PR is approved and ready to merge. Let's complete the workflow.

### Step 1: Verify Merge Readiness

On the PR page, scroll to the bottom merge section.

**Check these indicators:**
- ✅ "Changes reviewed" - 1 change suggested by reviewers with write access
- ✅ "No conflicts with base branch" - Merging can be performed automatically
- ✅ All checks passed (if CI/CD configured)

### Step 2: Choose Merge Strategy

GitHub offers several merge strategies:

**1. Create a merge commit** (default)
- Preserves full commit history
- Shows exact work done by agent
- Best for transparency and auditing
- Choose this for learning/training

**2. Squash and merge**
- Combines all commits into one
- Cleaner history
- Lose detailed agent work log
- Good for production workflows

**3. Rebase and merge**
- Replays commits on top of base branch
- Linear history
- More advanced, use with caution

**For this walkthrough, use "Squash and merge":**

**Why squash?**
- Agent may create multiple small commits
- You want one commit representing the complete feature
- Commit message summarizes the entire task

### Step 3: Customize Merge Commit Message

When you click "Squash and merge", a dialog appears.

**Customize the commit message:**

**Title:**
```
Create Module 165: AI-Generated API Documentation
```

**Description:**
```
Creates new training module as described in issue #1

Summary of what's added:
✅ Complete Module Structure
- Created docs/modules/165-ai-generated-api-documentation/ directory
- Added about.md with module overview
- Added walkthrough.md with hands-on guide

✅ Module Components
- about.md - Duration, skill description, topics, prerequisites
- walkthrough.md - Step-by-step instructions, success criteria, understanding check
- training-plan.md - Updated with Module 165 link

Closes #1
```

**Why customize?**
- Default message may be too verbose or unclear
- Your message appears in `git log`
- "Closes #5" automatically closes the linked issue

### Step 4: Confirm and Merge

Click **"Confirm squash and merge"** button.

**What happens:**
1. All agent commits squashed into one
2. New commit created on main branch
3. PR status changes to "Merged"
4. Linked issue automatically closes (if you used "Closes #5")
5. Agent's branch may be auto-deleted

**Success message appears:**
```
Pull request successfully merged and closed
```

### Step 5: Verify Merge

**Check the main branch:**
- Navigate to repository home
- Verify new commit appears in commit history
- Check that files are present in main branch

**Check the issue:**
- Navigate back to original issue
- Status should be "Closed"
- Timeline shows: "Closed via #3" (your PR number)

**Local workspace (in your IDE):**
Ask your AI assistant:
```
Pull the latest changes from GitHub main branch
```

Verify the new files appear in your local workspace.

---

## Part 9: Handling Errors and Improving Instructions

### Understanding Agent Failures

**Important point:**
If the Agent fails to resolve the issue or if there are any errors, you will see this in the message. Review it and comment on what it should do. However, it is better to correct the instruction files for the future so that it does not stop in the future. Our task is to make Agent completely independent.

### Common Agent Errors

**1. Missing instruction files**
```
Error: Cannot find ./instructions/main.agent.md
```

**Solution:**
- Create the missing instruction file
- Update `.github/copilot-instructions.md` to reference it
- Close issue, improve instructions, create new issue

**2. Environment differences**
```
Error: Command not found: python
```

**Root cause:** Agent's environment differs from your IDE
- Your IDE: Windows, Python in PATH
- Agent server: Linux, different Python location

**Solution:**
- Update instruction files with environment-agnostic commands
- Use `python3` instead of `python`
- Specify full paths or use virtual environment activation

**3. Misunderstanding requirements**
```
Agent implements feature differently than expected
```

**Root cause:** Vague issue description or missing examples

**Solution:**
- Improve issue template
- Add more specific acceptance criteria
- Include code examples in issue
- Reference existing similar implementations

**4. Ignoring instruction files**
```
Agent doesn't follow ./testing-tool.agent.md
```

**Root cause:** `.github/copilot-instructions.md` doesn't emphasize reading instructions

**Solution:**
Update `.github/copilot-instructions.md`:
```markdown
# CRITICAL: Always follow these steps

1. **FIRST:** Read ./instructions/main.agent.md
2. This file contains links to ALL other instruction files
3. Follow instructions for your specific task type
4. Do NOT proceed without reading instructions
```

### Improving Instruction Files

**After each agent session, ask yourself:**
- What mistakes did the agent make?
- Which instructions were ignored?
- What should be added to prevent this in the future?

**Instruction improvement cycle:**
1. Agent makes mistake
2. You identify root cause
3. Update relevant instruction file
4. Test with new issue
5. Repeat until agent is reliable

**Example improvements:**

**Before:**
```markdown
# Testing Tools

Run tests after creating a tool.
```

**After:**
```markdown
# Testing Tools

## When to Test
- ALWAYS after creating new tool
- ALWAYS after modifying existing tool
- BEFORE creating pull request

## How to Test
1. Activate virtual environment: `source venv/bin/activate`
2. Run: `pytest tests/tools/test_YOUR_TOOL.py -v`
3. Verify all tests pass
4. If tests fail, fix issues before PR

## What to Test
- Happy path: Tool works with valid inputs
- Error handling: Tool handles invalid inputs gracefully
- Edge cases: Empty inputs, special characters, etc.
```

**Result:** Agent understands WHEN, HOW, and WHAT to test.

---

## Part 10: Advanced Patterns

### Running Multiple Agents in Parallel

**Key insight:**
You can run several agents at once, each working on its own issue. You get your own junior staff.

**How to parallelize:**

1. **Create multiple well-defined issues:**
   - Issue #1: Create Module 165: AI-Generated API Documentation
   - Issue #2: Create Module 170: DIAL API Key and cURL Access
   - Issue #3: Update Module 055 with new examples
   - Issue #4: Add screenshots to Module 150

2. **Assign agent to each issue:**
   - Navigate to each issue
   - Click "Assign Copilot"
   - Agents work independently

3. **Work on your own tasks:**
   - Write documentation
   - Design architecture
   - Code review other PRs
   - Plan next sprint

4. **Review PRs as they complete:**
   - Agents finish at different times
   - Review each PR independently
   - Merge approved PRs
   - Request changes as needed

**Benefits:**
- 4x productivity (4 tasks in parallel)
- You focus on high-value work (architecture, planning)
- Agents handle repetitive implementation
- Faster iteration cycles

**Limitations:**
- Each agent consumes 1 premium request
- May hit GitHub API rate limits with many parallel agents
- PR review workload increases

### Asking About Task Progress from IDE

**Key insight:**
After some time, you can ask Copilot in the IDE, "What is the progress of this task?" and receive a comprehensive answer.

**How to check progress from IDE:**

1. **While agent works, open AI chat in IDE**

2. **Ask about task status:**
   ```
   What is the progress on issue #1 (New training module about API documentation)?
   ```

3. **AI assistant checks GitHub:**
   - Reads issue comments
   - Checks PR status
   - Reviews agent's session log
   - Summarizes progress

4. **You receive comprehensive answer:**
   ```
   Issue #1 Status: ✅ Completed and Merged
   
   - Agent finished implementation 2 hours ago
   - Created PR #3 with complete module structure
   - You requested changes (remove temporary files, add Understanding Check)
   - Agent addressed all comments
   - PR merged into main branch 1 hour ago
   
   The new Module 165: AI-Generated API Documentation is now available in main branch.
   ```

**Use cases:**
- Check if agent has finished (without opening browser)
- Monitor progress on long-running tasks
- Get summary of what was implemented
- Identify if agent is stuck

**Pro tip:** Create a local temporary branch to test the agent's work before merging:
```
Ask AI: "Create a local branch from the agent's PR and let me test it"
```

### When Agent Gets Stuck

Sometimes the agent may encounter issues it cannot resolve independently.

**Symptoms:**
- No progress for 30+ minutes
- Error messages in work session
- Agent asks for clarification in PR comments

**Actions:**

**1. Review work session log:**
- Identify where agent got stuck
- Look for error messages
- Understand what agent attempted

**2. Provide clarification:**
- Add comment to issue with more details
- Explain the blocked area
- Provide example code

**3. Cancel and restart:**
- Close the PR
- Update issue with better requirements
- Improve instruction files
- Assign agent again

**4. Take over manually:**
- Pull agent's branch locally
- Complete the remaining work
- Push changes
- Merge PR

---

## Success Criteria

You've successfully completed this module when you can check off:

✅ Understand GitHub Copilot Coding Agent capabilities and limitations  
✅ Know when to use agent delegation vs. coding yourself  
✅ Create well-defined GitHub issues suitable for agent assignment  
✅ Verify instruction files are in place before assigning agent  
✅ Assign GitHub Copilot to issue through GitHub web interface  
✅ Monitor agent progress through issue comments and work sessions  
✅ Understand GPT-4 vs Claude differences in agent behavior  
✅ Review agent-generated pull requests thoroughly  
✅ Add review comments efficiently (collect all, then submit once)  
✅ Approve and merge pull requests with proper commit messages  
✅ Identify agent errors and improve instruction files  
✅ Run multiple agents in parallel on different issues  
✅ Check task progress from IDE without opening browser  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **What model does GitHub Copilot Coding Agent use, and why does it matter?**
   
   Expected answer: The agent uses GPT-4, while the IDE uses Claude Sonnet 4.5. This matters because different models have different behaviors, reasoning patterns, and strengths. Instructions that work perfectly in the IDE may need adjustment for the agent. You need to test agent behavior and refine instructions accordingly.

2. **Why should you collect all review comments before submitting, rather than submitting each comment individually?**
   
   Expected answer: Each submission triggers a new agent session, consuming one premium request. By collecting all comments and submitting them together, you minimize premium request usage and give the agent complete context for all required changes at once.

3. **What are the critical success factors for effective agent delegation?**
   
   Expected answer: (1) Well-defined GitHub issues with clear requirements, (2) Comprehensive instruction files that agent reads first, (3) Up-to-date codebase on GitHub, (4) Clear acceptance criteria, (5) Willingness to iterate and improve instructions based on agent behavior.

4. **When should you use GitHub Coding Agent vs. coding yourself in the IDE?**
   
   Expected answer: Use agent for well-defined tasks, repetitive work, tasks that can be validated by tests, and when you want to parallelize development. Code yourself for exploratory work, complex architectural decisions, urgent fixes, and tasks requiring external tools or human judgment.

5. **What should you do if the agent makes mistakes?**
   
   Expected answer: Review the mistake, identify the root cause, and UPDATE INSTRUCTION FILES to prevent the same mistake in future sessions. The goal is to make the agent increasingly independent by improving its guidance. Don't just fix the code—fix the instructions.

6. **How can you run multiple agents in parallel, and what are the benefits?**
   
   Expected answer: Create multiple well-defined issues and assign Copilot to each one. Agents work independently on GitHub's infrastructure. Benefits: parallelize development work, focus on high-value tasks (architecture, planning), faster iteration, handle multiple features simultaneously. Limitations: consumes multiple premium requests, increases review workload.

7. **What information should you look for in the agent's work session log?**
   
   Expected answer: Check if agent reads instruction files first (good sign), what files it reads for context, whether commands/tools execute successfully, any error messages, and the overall approach to solving the problem. This helps identify if agent followed your guidance or needs better instructions.

---

## Troubleshooting

### Problem: "Assign Copilot" button not visible

**Symptoms:** Cannot find button to assign agent to issue

**Solutions:**
- Verify GitHub Copilot subscription is active and includes Coding Agent access
- Check you have write access to the repository
- Try refreshing the page
- Look in right sidebar under "Assignees" or "..." menu
- Ensure issue is Open (cannot assign to closed issues)

### Problem: Agent creates PR with temporary/test files

**Symptoms:** PR includes files like test.sh, test.txt, calculator.js

**Root cause:** Agent didn't clean up after testing

**Solutions:**
- Add review comment: "Remove temporary files used for testing"
- Update instruction files with cleanup checklist:
  ```markdown
  ## Before Creating PR
  - [ ] Remove all temporary test files
  - [ ] Remove debug print statements
  - [ ] Verify only necessary files are included
  ```

### Problem: Agent doesn't follow instruction files

**Symptoms:** Agent makes mistakes covered in your instructions

**Root cause:** `.github/copilot-instructions.md` doesn't emphasize reading instructions

**Solutions:**
1. Make instructions more prominent in main instruction file
2. Add explicit: "CRITICAL: Always read ./instructions/main.agent.md FIRST"
3. Move critical instructions earlier in files
4. Use stronger language: "MUST", "CRITICAL", "ALWAYS"

### Problem: Agent gets stuck or times out

**Symptoms:** No progress for 30+ minutes, no PR created

**Solutions:**
- Check work session log for error messages
- Simplify the issue (break into smaller tasks)
- Provide more specific requirements
- Check if required tools/libraries are accessible in agent environment
- Cancel and restart with improved issue description

### Problem: PR merge conflicts with main branch

**Symptoms:** "Cannot automatically merge" warning on PR

**Root cause:** Main branch changed while agent worked

**Solutions:**
- Ask agent to rebase on latest main (add comment to PR)
- Manually resolve conflicts:
  1. Pull agent's branch locally
  2. Merge main into agent's branch
  3. Resolve conflicts
  4. Push updated branch
- Prevention: Work on stable main branch, coordinate with team

### Problem: Agent implements wrong solution

**Symptoms:** Code works but doesn't match requirements

**Root cause:** Vague issue description or missing examples

**Solutions:**
- Improve issue template with:
  - Specific acceptance criteria
  - Code examples showing expected usage
  - Links to similar existing implementations
  - "Definition of Done" checklist
- Request changes with clearer explanation
- Consider taking over manually if agent is far off track

---

## Next Steps

**Congratulations!** You've mastered GitHub Coding Agent delegation and parallel development workflows. Here's what comes next:

1. **Practice the complete workflow**
   
   Apply agent delegation to real projects:
   - Create 3-5 well-defined issues
   - Assign agents in parallel
   - Review and merge PRs
   - Iterate on instruction files based on results

2. **Build your instruction file library**
   
   Continuously improve your instructions:
   - Document your coding standards
   - Capture common patterns
   - Create task-specific instruction files
   - Share instruction files across team

3. **Optimize your development workflow**
   
   Combine all skills learned:
   - Use IDE for exploratory work (Claude)
   - Delegate implementation to agents (GPT-4)
   - Focus on architecture and planning
   - Review and improve agent outputs

4. **Scale to team usage**
   
   Extend agent delegation to your team:
   - Create shared instruction file repository
   - Establish PR review standards for agent work
   - Train team on effective issue writing
   - Monitor and improve agent success rates

5. **Continue to Module 160: Bulk File Processing with AI**
   
   Learn how to process multiple files at once, preparing for advanced automation workflows.

---

## Additional Resources

- [GitHub Copilot Coding Agent Documentation](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks)
- [Writing Effective GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/quickstart)
- [Code Review Best Practices](https://google.github.io/eng-practices/review/)
- [Module 105: MCP GitHub Integration](../105-mcp-github-integration-issues/about.md) - Review issue creation
- [Module 055: Clarifying Requirements](../055-clarifying-requirements-before-start/about.md) - Improve issue quality

---

**Ready to continue your training?** Head to [Module 160: Bulk File Processing with AI](../160-bulk-file-processing-with-ai/about.md)
