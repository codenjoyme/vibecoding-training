# MCP GitHub Integration - Issues Management - Hands-on Walkthrough

You've learned how to set up MCP servers and understand the protocol. Now it's time to connect your AI assistant to **GitHub**—one of the most powerful MCP integrations available. This module teaches you to manage repositories, remotes, and issues directly from AI chat, automating workflows that typically require constant browser-IDE switching.

## Prerequisites

- Completed [Module 100: Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)
- Understanding of `mcp.json` configuration for your IDE
- Active GitHub account with authentication token
- Git installed and configured in your environment
- Current workspace with Git repository initialized

## What We'll Build

In this hands-on walkthrough, you'll:
- Configure the **GitHub MCP server** (HTTP-based, no installation needed)
- Authenticate with GitHub API
- List your repositories through AI chat
- Create a new empty repository on GitHub
- Add a new Git remote named `fork` pointing to the new repository
- Push code to the new remote: `git push fork master`
- Verify the code appeared on GitHub
- Conduct an **interactive requirements interview** (like Module 055)
- Create a GitHub issue with interview findings for future implementation

**Time required:** 15-20 minutes

---

## Part 1: Understanding GitHub MCP Server

### What Makes GitHub MCP Special

Unlike the echo server from Module 100, the GitHub MCP server:
- **HTTP-based** - Connects to GitHub's official API endpoint
- **No local installation** - Runs on GitHub's infrastructure
- **Authentication-based** - Requires GitHub token for access
- **Rich functionality** - Repositories, issues, PRs, branches, commits

### Why Use MCP Instead of CLI?

**Traditional workflow:**
1. Open browser → Navigate to GitHub
2. Create repository manually
3. Copy repository URL
4. Switch to terminal → Add remote
5. Push code
6. Switch to browser → Create issue
7. Write issue description
8. Repeat for each task

**MCP workflow:**
1. Ask AI in chat: "Create a new repo and push my code there"
2. Approve tool calls
3. Done

---

## Part 2: Configuration Setup

### Step 1: Locate or Create mcp.json File

**Important:** Configuration location differs between IDEs!

**For VS Code users:**
- Create or open: `.vscode/mcp.json` in your workspace root
- Example path: `c:/workspace/hello-genai/.vscode/mcp.json` (Windows) or `~/workspace/hello-genai/.vscode/mcp.json` (macOS/Linux)

**For Cursor users:**
- Create or open: `.cursor/mcp.json` in your workspace root
- Example path: `c:/workspace/hello-genai/.cursor/mcp.json` (Windows) or `~/workspace/hello-genai/.cursor/mcp.json` (macOS/Linux)

**Quick reference from Module 100:**
- **VS Code** uses `.vscode/mcp.json` with root key `"servers"`
- **Cursor** uses `.cursor/mcp.json` with root key `"mcpServers"`

If the file doesn't exist, create it based on your IDE:

**VS Code template:**
```json
{
  "servers": {}
}
```

**Cursor template:**
```json
{
  "mcpServers": {}
}
```

### Step 2: Add GitHub MCP Server

Add the GitHub server configuration to your `mcp.json`:

**For VS Code (`.vscode/mcp.json`):**
```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

**For Cursor (`.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

**Key differences from local servers:**
- **type: "http"** - Connects to remote endpoint (not local script)
- **url** - Points to GitHub's official MCP API
- **No `command` or `args`** - Server runs on GitHub's infrastructure

### Step 3: Reload IDE Window

After saving `mcp.json`:
1. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Type "Reload Window"
3. Press Enter

This connects your IDE to GitHub MCP server.

### What Just Happened

Your IDE:
1. Read the updated `mcp.json` configuration
2. Connected to `https://api.githubcopilot.com/mcp/` via HTTP
3. Discovered available GitHub tools (repositories, issues, branches, etc.)
4. Made these tools available to your AI assistant

**Check connection:** Open Output panel (View → Output) and select "Model Context Protocol". You should see:
```
[info] Starting HTTP server github
[info] Connection state: Running
```

---

## Part 3: GitHub Authentication

### Understanding GitHub MCP Authentication

The GitHub MCP server uses your **GitHub Copilot subscription** for authentication. This means:
- No need to create personal access tokens manually
- Automatic authentication through your IDE's GitHub login
- Permissions inherit from your GitHub account

### Step 1: Verify GitHub Login in IDE

**VS Code:**
1. Look at bottom-left corner for GitHub account indicator
2. Click the account icon if not signed in
3. Select "Sign in to GitHub"
4. Complete authentication in browser

**Cursor:**
1. Open Settings (gear icon)
2. Navigate to "Accounts"
3. Ensure GitHub account is connected
4. If not, click "Sign in with GitHub"

### Step 2: Test Authentication

Open AI chat and ask:
```
List my GitHub repositories using the GitHub MCP server
```

**Expected behavior:**
- AI detects the `list_repositories` tool from GitHub MCP
- Shows approval dialog with tool call details
- After approval, returns your repository list

**If authentication fails:**
- Error message: "Authentication required" or "Unauthorized"
- Solution: Sign out and re-sign in to GitHub in your IDE
- Verify GitHub Copilot subscription is active

### Switching GitHub Accounts (Important!)

If you need to switch to a different GitHub account for the MCP server:

**VS Code method (recommended):**
1. Open your `.vscode/mcp.json` file
2. Hover over the GitHub server configuration
3. Click the **"More..."** link that appears above the server name
4. Select **"Disconnect Account"** from the menu
5. The server will restart and prompt you to authenticate with a different account
6. Complete authentication in the browser with your desired GitHub account

**Alternative method:**
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "MCP" to see MCP-related commands
3. Look for options to manage server connections

**Why this matters:**
- GitHub MCP uses its own authentication, separate from VS Code's GitHub login
- Changing the account in VS Code's bottom-left corner does NOT change MCP authentication
- You must disconnect the MCP server account specifically using the steps above

**After switching accounts:**
- Reload the IDE window if needed
- Verify new account by asking AI to check current user
- Create repositories under the correct account

### Step 3: Review Available GitHub Tools

To see all GitHub MCP tools, ask AI:
```
What GitHub tools are available through MCP?
```

You should have access to:
- **Repositories:** Create, list, get details, delete
- **Issues:** Create, list, update, close, add comments
- **Pull Requests:** Create, list, review, merge
- **Branches:** Create, list, delete
- **Commits:** List, get details
- **Files:** Read content, create, update, delete

For this walkthrough, we'll focus on **repositories** and **issues**.

---

## Part 4: Practical Task - Repository and Remote Management

### What We'll Do

This hands-on section walks through the complete workflow:
1. List existing repositories
2. Create a new empty repository
3. Add new remote named `fork` to current workspace
4. Push code to the new remote
5. Verify code appeared on GitHub

### Step 1: List Your Repositories

Ask AI:
```
Show me all my GitHub repositories using the github MCP tool
```

**Review the approval dialog:**
- Tool name: `list_repositories`
- Parameters: May include filters (public/private, organization, etc.)

Click "Allow" and review the output. You'll see:
- Repository names
- Visibility (public/private)
- URLs
- Descriptions

**Note the repository count** - you'll verify the new one appears here later.

### Step 2: Create a New Empty Repository

Before creating, let's understand what we're building. Ask AI:
```
Create a new GitHub repository with these details:
- Name: vibecoding-fork-test
- Description: Test repository for MCP GitHub integration training
- Visibility: Public
- No README, .gitignore, or license (empty repository)
```

**Approval dialog shows:**
- Tool: `create_repository`
- Parameters:
  ```json
  {
    "name": "vibecoding-fork-test",
    "description": "Test repository for MCP GitHub integration training",
    "private": false,
    "auto_init": false
  }
  ```

**Click "Allow"** - GitHub creates the repository.

**What just happened:**
- AI called GitHub API through MCP
- Created repository under your GitHub account
- Returned repository URL and details

**Verify:** Ask AI to list repositories again. The new repository should appear in the list.

### Step 3: Add New Git Remote

Now connect your current workspace to the new repository. Ask AI:
```
Add a new Git remote named "fork" pointing to the repository "vibecoding-fork-test" we just created
```

**What the AI will do:**
1. Get the repository URL (e.g., `https://github.com/your-username/vibecoding-fork-test.git`)
2. Run: `git remote add fork <repository-url>`
3. Verify the remote was added

**Approval dialog shows:**
- Tool: Likely uses terminal execution or Git commands
- Command: `git remote add fork https://github.com/your-username/vibecoding-fork-test.git`

**Click "Allow"**

### Step 4: Verify Remotes

Ask AI:
```
Show me all Git remotes in this workspace
```

Expected output:
```
origin    https://github.com/original-repo/project.git (fetch)
origin    https://github.com/original-repo/project.git (push)
fork      https://github.com/your-username/vibecoding-fork-test.git (fetch)
fork      https://github.com/your-username/vibecoding-fork-test.git (push)
```

**You now have two remotes:**
- `origin` - Your original repository
- `fork` - The new test repository

### Step 5: Push Code to Fork Remote

Ask AI:
```
Push the current branch (master) to the fork remote
```

**What happens:**
- AI determines current branch (likely `master` or `main`)
- Executes: `git push fork master`
- Pushes all commits to the new repository

**Approval dialog:**
- Command: `git push fork master`
- Explanation: Pushing local commits to remote

**Click "Allow"** and watch the output. You should see:
```
Counting objects: X, done.
Delta compression using up to Y threads.
Compressing objects: 100% (Z/Z), done.
Writing objects: 100% (X/X), done.
To https://github.com/your-username/vibecoding-fork-test.git
 * [new branch]      master -> master
```

### Step 6: Verify on GitHub

Ask AI:
```
Open the vibecoding-fork-test repository URL in my browser
```

Or manually navigate to: `https://github.com/your-username/vibecoding-fork-test`

**Verify:**
- Repository contains your code files
- Commit history matches your local branch
- File structure is identical to your workspace

**Success!** You've created a repository, configured a remote, and pushed code entirely through AI chat.

---

## Part 5: Interactive Requirements Interview

### Understanding the Workflow

In [Module 055: Clarifying Requirements Before Start](../055-clarifying-requirements-before-start/about.md), you learned how AI can interview users to gather requirements before implementation. Now we'll **combine that skill with GitHub MCP** to create a complete workflow:

1. AI interviews you about a new feature/module
2. AI captures requirements, goals, and technical details
3. AI creates a GitHub issue with the interview summary
4. Issue becomes a task for future implementation

### What We'll Do

We'll ask AI to:
- Review the instructions for creating training modules
- Interview you about a new skill/module you want to add to the course
- Find the logical place in the course structure
- Create a GitHub issue with all findings (NOT implement the module yet)

This demonstrates **delegation through GitHub Issues**—documenting work for later execution.

### Step 1: Load Module Creation Instructions

Ask AI:
```
Read the file ./instructions/create-training-module.agent.md to understand how to create new training modules
```

AI will read the instructions file and confirm understanding of:
- Module structure (about.md, walkthrough.md)
- Numbering scheme (increments of 10, with 5 for insertions)
- Required sections in both files
- Integration with training-plan.md

### Step 2: Start Interactive Interview

Ask AI:
```
Interview me about a new training module I want to add to this course. Follow the questions from create-training-module.agent.md. After gathering all information, create a GitHub issue with the findings—do NOT implement the module yet.
```

### Step 3: Answer AI's Questions

AI will ask questions like:
- What specific skill will this module teach?
- Where should it be placed in the learning sequence (after which module)?
- What are the main topics to cover (3-5 bullet points)?
- What are the prerequisites (which modules should be completed first)?
- What practical outcome should the learner achieve?
- What are the concrete hands-on steps to practice this skill?

**Example interview:**

**AI:** What specific skill will this module teach?

**You:** I want to teach developers how to use AI to generate API documentation from code comments and function signatures. The module should show how to parse Python code, extract docstrings, and generate Markdown documentation automatically.

**AI:** Where should it be placed in the learning sequence? After which module?

**You:** After Module 160 (Bulk File Processing with AI), since it involves processing multiple Python files.

**AI:** What are the main topics to cover?

**You:** 
- Parsing Python files for function signatures
- Extracting docstrings and type hints
- Generating Markdown documentation
- Automating documentation updates
- Integrating with CI/CD pipelines

**AI:** What are the prerequisites?

**You:**
- Module 160: Bulk File Processing with AI
- Module 180: Python integration basics
- Basic understanding of Python docstrings

**AI:** What practical outcome should the learner achieve?

**You:** Learners should be able to automatically generate API documentation for any Python project by pointing AI at the source code directory.

**AI:** What are the concrete hands-on steps?

**You:**
- Create a sample Python project with multiple modules
- Write an AI prompt to parse Python files
- Extract function/class information
- Generate structured Markdown output
- Save documentation to docs/ folder
- Verify generated documentation is accurate

### Step 4: AI Creates GitHub Issue

After gathering all information, AI will say something like:
```
I have all the information needed. I'll now create a GitHub issue to document this new module.
```

**Approval dialog shows:**
- Tool: `create_issue`
- Parameters:
  ```json
  {
    "repository": "vibecoding-for-managers",
    "title": "New Module: AI-Generated API Documentation",
    "body": "## Module Overview\n\n**Skill:** Generate API documentation from Python code using AI\n\n**Placement:** After Module 160 (Bulk File Processing)\n\n**Module Number:** 165\n\n## Topics to Cover\n\n- Parsing Python files for function signatures\n- Extracting docstrings and type hints\n- Generating Markdown documentation\n- Automating documentation updates\n- Integrating with CI/CD pipelines\n\n## Prerequisites\n\n- Module 160: Bulk File Processing with AI\n- Module 180: Python integration basics\n- Basic understanding of Python docstrings\n\n## Learning Outcome\n\nLearners will be able to automatically generate API documentation for any Python project by pointing AI at the source code directory.\n\n## Hands-on Steps\n\n1. Create a sample Python project with multiple modules\n2. Write an AI prompt to parse Python files\n3. Extract function/class information\n4. Generate structured Markdown output\n5. Save documentation to docs/ folder\n6. Verify generated documentation is accurate\n\n## Implementation Notes\n\n- Use AI to parse Python AST (Abstract Syntax Tree)\n- Consider using existing tools like pydoc or sphinx as examples\n- Focus on automation rather than manual documentation writing\n",
    "labels": ["enhancement", "training-module", "documentation"]
  }
  ```

**Click "Allow"** - The issue is created on GitHub.

### Step 5: Verify the Issue

Ask AI:
```
Show me the issue we just created
```

Or navigate to your repository's Issues tab in the browser.

**You should see:**
- Issue title: "New Module: AI-Generated API Documentation"
- Complete description with all interview findings
- Labels: enhancement, training-module, documentation
- Status: Open

**What we accomplished:**
- Documented a new feature without implementing it
- Created a structured task for future work
- Preserved all requirements and context in GitHub

**This is the power of MCP + GitHub Issues:**
- No context-switching to browser
- Structured requirements capture
- Backlog management through AI chat
- Delegation to future AI sessions (or human developers)

---

## Part 6: Understanding the Workflow

### Why This Workflow Matters

Traditional development:
1. Idea emerges during conversation
2. Write it down in notes/Slack/email
3. Later, try to remember context
4. Manually create GitHub issue
5. Implementation happens (maybe)

**MCP + GitHub workflow:**
1. Idea emerges during AI conversation
2. AI interviews you to clarify details
3. AI creates structured GitHub issue immediately
4. Issue contains complete context for future implementation
5. No information loss, no manual data entry

### Real-World Applications

**Use Case 1: Feature Brainstorming**
- Discuss multiple feature ideas with AI
- For each idea, run quick interview
- Create GitHub issues for top 3 priorities
- Backlog is populated without leaving IDE

**Use Case 2: Bug Reports**
- Discover a bug during development
- Describe symptoms to AI
- AI asks clarifying questions (reproduction steps, expected behavior)
- AI creates detailed bug report issue

**Use Case 3: Code Review Findings**
- AI analyzes codebase and identifies improvements
- For each finding, AI creates an issue with:
  - Current state
  - Proposed improvement
  - Affected files
  - Suggested implementation approach

**Use Case 4: Learning Path Planning**
- Interview learners about their skills and goals
- AI recommends training modules
- Create GitHub issues for custom modules
- Track learning progress through issue completion

### The Agent Delegation Pattern

What we practiced here is called **Agent Delegation**:

1. **Current AI session** (interviewer):
   - Gathers requirements
   - Documents context
   - Creates structured task

2. **Future AI session** (implementer):
   - Reads GitHub issue
   - Has complete context
   - Implements the solution
   - Closes issue when done

**Benefits:**
- Work can be split across multiple sessions
- Context is preserved in structured format
- No information loss between sessions
- Clear task boundaries

---

## Success Criteria

You've successfully completed this module when you can check off:

✅ Understand how to configure GitHub MCP server (HTTP-based)  
✅ Know the difference between local MCP servers and HTTP-based servers  
✅ Successfully authenticate with GitHub through your IDE  
✅ List repositories using GitHub MCP tools  
✅ Create a new GitHub repository through AI chat  
✅ Add a new Git remote (`fork`) pointing to the new repository  
✅ Push code to the fork remote using `git push fork master`  
✅ Verify code appeared on GitHub  
✅ Conduct an interactive requirements interview (Module 055 pattern)  
✅ Create a GitHub issue with interview findings  
✅ Understand the Agent Delegation pattern  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **What's the difference between GitHub MCP server and the echo server from Module 100?**
   
   Expected answer: GitHub MCP is HTTP-based (connects to remote API) with no local installation, while echo server is local (PowerShell/Bash script). GitHub requires authentication, echo server doesn't. GitHub provides production-grade tools for real workflows.

2. **Why use MCP for GitHub instead of just using the GitHub website?**
   
   Expected answer: MCP eliminates context-switching between IDE and browser. You can manage repositories, issues, and remotes entirely through AI chat. This speeds up workflows and keeps you in the development environment.

3. **How does GitHub MCP authentication work?**
   
   Expected answer: It uses your GitHub Copilot subscription and IDE's GitHub login. No need to create personal access tokens manually—authentication inherits from your GitHub account.

4. **What is the Agent Delegation pattern?**
   
   Expected answer: One AI session (interviewer) gathers requirements and creates a GitHub issue. A future AI session (implementer) reads the issue and implements the solution. Context is preserved through structured documentation.

5. **Why create GitHub issues instead of implementing immediately?**
   
   Expected answer: Issues serve as backlog for planned work. They preserve context, allow prioritization, enable asynchronous implementation, and provide a record of decisions. Not all ideas should be implemented immediately.

6. **What information should a good GitHub issue include?**
   
   Expected answer: Clear title, detailed description, context/background, requirements, acceptance criteria, technical notes, labels, and links to related issues/PRs. Enough information for someone (human or AI) to implement without additional questions.

7. **How do multiple Git remotes (origin, fork) enable collaboration?**
   
   Expected answer: `origin` points to main repository, `fork` points to personal copy. You can fetch updates from `origin`, develop on local branches, and push to `fork` for testing. Then create PRs from fork to origin. This is the standard open-source contribution workflow.

---

## Troubleshooting

### Problem: "GitHub MCP server not found"

**Symptoms:** AI says GitHub tools are unavailable

**Solutions:**
- Verify `mcp.json` has correct URL: `https://api.githubcopilot.com/mcp/`
- Check you're editing the right file (`.vscode/mcp.json` vs `.cursor/mcp.json`)
- Reload IDE window after configuration changes
- Check Output panel for connection errors

### Problem: "Authentication failed" when using GitHub tools

**Symptoms:** Tool calls fail with "Unauthorized" or "Authentication required"

**Solutions:**
1. **Disconnect MCP server account (recommended):**
   - Open `.vscode/mcp.json` file
   - Hover over GitHub server configuration
   - Click **"More..."** link above server name
   - Select **"Disconnect Account"**
   - Re-authenticate when prompted
   
2. **Alternative solutions:**
   - Verify GitHub Copilot subscription is active
   - Check internet connection (HTTP-based server requires network)
   - Try reloading IDE window
   - Check Output panel (View → Output → Model Context Protocol) for detailed errors

**Important:** Changing the GitHub account in VS Code's bottom-left corner does NOT affect MCP authentication. You must disconnect the MCP server account specifically.

### Problem: Repository created under wrong GitHub account

**Symptoms:** 
- Repository appears under unexpected GitHub account (e.g., `coparent` instead of `codenjoyme`)
- MCP uses different account than shown in VS Code

**Root cause:** GitHub MCP has its own authentication, separate from VS Code's GitHub login

**Solution:**
1. Open `.vscode/mcp.json` in your workspace
2. Hover over the `"github"` server configuration
3. Click the **"More..."** link that appears above the server
4. From the dropdown menu, select **"Disconnect Account (coparent)"** (shows current account)
5. Server will restart and prompt for authentication
6. Complete authentication with your desired GitHub account in browser
7. Reload IDE window: `Ctrl+Shift+P` → "Reload Window"
8. Verify account changed by asking AI to check current user

**Alternative workaround:**
- Manually create repository on GitHub under desired account
- Add it as remote: `git remote add fork https://github.com/your-username/repo.git`
- Continue with the walkthrough

### Problem: Git push fails with "permission denied"

**Symptoms:** `git push fork master` fails

**Solutions:**
- Verify Git authentication is configured (SSH keys or credential manager)
- Check repository permissions on GitHub (you must have write access)
- Ensure repository URL is correct (verify with `git remote -v`)
- Try HTTPS URL instead of SSH if SSH keys aren't configured

### Problem: "Repository already exists" error

**Symptoms:** Cannot create repository with chosen name

**Solutions:**
- Repository names must be unique within your account
- Check if you already have a repository with this name
- Choose a different name
- Delete old repository if it's no longer needed

### Problem: AI creates issue in wrong repository

**Symptoms:** Issue appears in different repository than expected

**Solutions:**
- Explicitly specify repository name in your prompt
- Verify workspace is connected to correct Git repository
- Check `git remote -v` output for correct repository URL
- Be specific: "Create issue in repository vibecoding-for-managers"

---

## Next Steps

**Congratulations!** You've mastered GitHub MCP integration and the Agent Delegation pattern. Here's what comes next:

1. **Practice the workflow**
   
   Apply what you learned to real projects:
   - Interview yourself about upcoming features
   - Create GitHub issues for each feature
   - Implement one issue at a time using AI
   - Close issues as you complete work

2. **Explore advanced GitHub MCP tools**
   
   Beyond repositories and issues:
   - Pull Requests: Create, review, merge through AI
   - Branches: Create feature branches, switch, delete
   - Code Search: Find code patterns across repositories
   - Workflows: Trigger GitHub Actions from AI chat

3. **Combine MCP servers**
   
   Use multiple MCP servers together:
   - GitHub MCP for issue management
   - File system MCP for code operations
   - Database MCP for data queries
   - AI orchestrates across all servers

4. **Continue to Module 110: Development Environment Setup**
   
   Learn to set up complete development environments using AI, building on your Git and GitHub skills.

---

## Additional Resources

- [GitHub MCP Server Documentation](https://github.com/github/github-copilot-mcp)
- [GitHub REST API Reference](https://docs.github.com/en/rest)
- [Git Remotes Documentation](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- [Module 055: Clarifying Requirements](../055-clarifying-requirements-before-start/about.md) - Review interview techniques
- [Module 150: GitHub Coding Agent Delegation](../150-github-coding-agent-delegation/about.md) - Advanced delegation patterns

---

**Ready to continue your training?** Head to [Module 110: Development Environment Setup](../110-development-environment-setup/about.md)
