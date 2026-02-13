# Export Chat Session - Hands-on Walkthrough

In this walkthrough, you'll discover that every AI chat session you've had in VS Code is stored locally on your computer. You'll learn to extract these sessions into a portable HTML file, understand security risks of sharing them, and create useful summaries that serve as project documentation and team knowledge base.

## Prerequisites

- Completed Module 070: Custom Instructions
- VS Code with GitHub Copilot — at least one chat session in history
- Python 3 installed (`python --version` should work in terminal)
- No external Python packages needed — script uses only standard library

---

## Step-by-Step Instructions

### Part 1: Understanding What's Stored on Your Computer

Every time you chat with GitHub Copilot in VS Code, the entire conversation is saved locally.

**What we'll learn:**

- Where exactly VS Code stores chat data
- What information is preserved in each session
- Why this data is valuable beyond the chat window

**The Key Insight:**

1. VS Code stores chat sessions in its workspace storage directory:
   - Windows: `%APPDATA%/Code/User/workspaceStorage/` (or `Code - Insiders`)
   - macOS: `~/Library/Application Support/Code/User/workspaceStorage/`
   - Linux: `~/.config/Code/User/workspaceStorage/`

1. Each workspace gets a folder with a 32-character hex ID

1. Inside that folder, chat sessions are stored as `.jsonl` files — one per conversation

1. These files contain **everything**:
   - Every message you sent to the AI
   - Every response the AI generated
   - Every tool call (file reads, terminal commands, file edits)
   - Tool call results and outputs
   - Thinking blocks (the AI's reasoning process)
   - Model name, token counts, timing data
   - File attachments and screenshots you shared

1. This data persists even after you close VS Code — it's on your disk

**Why This Matters:**

- You have a complete record of every AI interaction per project
- This is like a detailed log of your development process
- It captures not just what was built, but **how** and **why**
- Most people don't know this data exists and never use it

### Part 2: Setting Up the Export Tool

**What we'll do:**

We'll use a ready-made Python script that reads VS Code's internal storage and converts sessions to human-readable formats. The script has no external dependencies.

1. Open your project workspace in VS Code (the course workspace `c:/workspace/hello-genai/` on Windows or `~/workspace/hello-genai/` on macOS/Linux)

1. Open the terminal in VS Code

1. Verify the export script exists — it's already part of this course:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py --help
   ```

1. You should see available commands: `workspaces`, `sessions`, `export`, `search`

1. If you get an error, make sure you're in the course root directory and Python 3 is installed

### Part 3: Finding Your Chat Sessions

**What we'll do:**

We'll discover which workspaces have chat sessions and list them.

1. List all VS Code workspaces that have chat history:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py workspaces
   ```

1. You should see output like:
   ```
   === VS Code Insiders ===
   Workspace: 483957ea... | vibecoding-for-managers | 3 sessions
   Workspace: a1b2c3d4... | my-other-project       | 1 session
   ```

1. Copy the workspace ID (the hex string) for the workspace you want to explore

1. List all sessions in that workspace:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py sessions <workspace_id>
   ```
   Replace `<workspace_id>` with the actual ID you copied.

1. You should see a list with session titles, message counts, dates, and file sizes

1. **Observe:** Notice the message count and file size — long sessions can be several megabytes of rich data

### Part 4: Exporting a Session to HTML

**What we'll do:**

We'll export a session as a standalone HTML file you can open in any browser and share with anyone.

1. Pick a session ID from the list (UUID format like `2c0613e1-856f-4ea3-b0c3-9e186ca196f5`)

1. Export it to HTML:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py export <workspace_id> <session_id> --output-dir ./work/copilot_export --format html
   ```

1. You should see:
   ```
   Exporting <session_id>...
   ✅ ./work/copilot_export/chat_<short_id>_<date>.html
   ```

1. Open the generated HTML file in your browser

1. **Explore what you see:**
   - Dark theme with readable formatting
   - User messages with attached context (files, screenshots)
   - Assistant responses with full markdown rendering
   - Collapsible tool call blocks — click them to expand:
     * Terminal commands with output
     * File reads and edits
     * MCP tool calls
     * Todo list management
   - Grouped tool calls matching VS Code's native grouping
   - Request metadata: model name, token counts, timing, status

1. **Key observation:** This is a complete, self-contained record of the AI interaction — no VS Code needed to view it

### Part 5: Understanding Token Leakage Risks

**⚠️ Security Warning — Read Carefully**

Before sharing any exported session, you must understand the risks.

**What gets captured in the export:**

1. **Your code** — every file the AI read or wrote is embedded in the session

1. **Terminal output** — command results may contain:
   - API keys and tokens
   - Environment variables
   - Database connection strings
   - Internal URLs and endpoints

1. **File paths** — reveal your username, directory structure, project organization

1. **Attachments** — screenshots may contain sensitive information

1. **Tool call arguments** — show exact commands executed, including passwords passed in arguments

**What to do before sharing:**

1. Open the HTML in a browser and review it thoroughly

1. Search for patterns like:
   - API keys: `sk-`, `ghp_`, `Bearer`
   - Passwords in terminal commands
   - Internal URLs containing tokens
   - Environment variables with secrets

1. Consider who you're sharing with:
   - Same team, same project → usually safe
   - External person → review carefully for secrets
   - Public sharing → strip all sensitive data first

1. Alternatively, export as JSON and write a script to redact sensitive patterns:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py export <workspace_id> <session_id> --format json
   ```

**Rule of thumb:** Treat exported sessions like you treat server logs — they may contain secrets.

### Part 6: Creating Session Summaries for Future Reference

This is where exported sessions become truly powerful.

**Why create summaries?**

1. A raw session export can be hundreds of kilobytes — too long to read

1. A summary captures **what was done, why, and how** in a few paragraphs

1. Summaries are searchable, linkable, and easy to share

1. They become your project's "what happened" documentation

**How to create a summary:**

1. Export the session as HTML or JSON (you already know how)

1. Open a new AI chat in VS Code

1. Attach the exported file to the chat (drag and drop, or use the paperclip icon)

1. Ask the AI to summarize:
   ```
   Summarize this chat session. Include:
   - What was the goal
   - What was accomplished
   - Key decisions made
   - Problems encountered and how they were solved
   - Files created or modified
   - Remaining open items
   Format as a markdown document.
   ```

1. Save the summary to your project, for example:
   - `./work/session-summaries/2026-02-13-export-tool-development.md`
   - `./work/session-summaries/2026-02-12-mcp-setup.md`

1. Over time you build a library of "what was done when"

**Practical use cases for summaries:**

- **Onboarding a colleague:** "Read these summaries to understand how we built the MCP integration"
- **Returning to a project after a break:** "What did I do last week? Let me check the session summaries"
- **Creating release notes:** "Summarize sessions from the last sprint into release notes"
- **Code reviews:** "Here's the AI session that produced this PR — see the reasoning"

### Part 7: Using Sessions as Reference for Future Work

**The most powerful pattern:**

1. You've built something using AI and exported the session

1. Now a colleague needs to build something similar

1. Instead of explaining from scratch, you say:
   ```
   Here's the session where I built the MCP file server.
   Use it as a reference and follow the same approach for the database connector.
   ```

1. The colleague attaches the HTML/JSON to their own AI session:
   ```
   I'm attaching a reference session showing how a colleague built
   an MCP file server. I need to build something similar but for
   a database connector. Study the approach and apply the same patterns.
   ```

1. The AI now has a complete example to follow — code, decisions, problems, solutions

**Building a knowledge base:**

1. Create a folder in your project for session exports and summaries:
   ```
   ./work/
     session-summaries/      ← markdown summaries
     copilot_export/         ← full HTML/JSON exports
   ```

1. After significant development milestones, export and summarize

1. Reference these in your instructions or README:
   ```markdown
   ## Development History
   - [MCP Server Setup](work/session-summaries/2026-02-11-mcp-setup.md)
   - [Export Tool Creation](work/session-summaries/2026-02-13-export-tool.md)
   ```

1. When creating custom instructions for AI, reference past sessions:
   ```
   Study the approach used in ./work/copilot_export/chat_xxx.html
   and apply the same patterns to this task.
   ```

### Part 8: Searching Across Sessions

**What we'll do:**

Find specific information across all your past sessions.

1. Use the search command to find sessions containing specific text:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py search "MCP server"
   ```

1. The script searches across all workspaces and all sessions

1. You'll see which sessions contain the text, along with workspace names

1. This is much faster than manually opening VS Code and scrolling through chat history

1. **Practical example:** "When did we set up the GitHub MCP? Let me search."
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py search "github mcp"
   ```

### Part 9: Other Export Formats

**JSON format** — for programmatic processing:

1. Export as JSON:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py export <workspace_id> <session_id> --format json
   ```

1. Use this when you want to:
   - Write scripts that analyze session data
   - Extract specific information programmatically
   - Feed session data into other tools

**JSONL format** — raw session data copy:

1. Export as JSONL:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py export <workspace_id> <session_id> --format jsonl
   ```

1. This copies the raw VS Code internal format — useful for backup or archival

**Batch export** — all sessions from one workspace:

1. Export all sessions from a specific workspace:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py export <workspace_id> * --output-dir ./work/copilot_export
   ```

1. Useful for creating a backup of a single workspace's chat history

### Part 10: Batch Export ALL Sessions from ALL Workspaces

**What we'll do:**

Export every session from every workspace in one command — a full backup of all your AI conversations.

1. Run the batch export script:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py
   ```

1. The script automatically:
   - Discovers all VS Code workspaces (both Code and Code Insiders)
   - Lists all sessions in each workspace
   - Exports them to HTML, preserving the structure
   - Skips sessions that have already been exported (safe to re-run)

1. Default output structure in `./work/copilot_export_all/`:
   ```
   work/copilot_export_all/
   ├── Code/
   │   ├── my-project/
   │   │   ├── chat_abc123_20260213_120000.html
   │   │   └── chat_def456_20260213_120001.html
   │   └── another-project/
   │       └── ...
   ├── Code_-_Insiders/
   │   ├── main-workspace/
   │   │   └── ...
   │   └── ...
   ```

1. You can customize the output:
   ```
   # Custom output directory
   python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py --output-dir ./my_backup

   # Export as JSON instead of HTML
   python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py --format json
   ```

1. **Key feature:** The script is idempotent — running it again will only export new sessions that appeared since the last run

### Part 11: Finding Your Current Session with a Marker String

**The Problem:**

You're in the middle of a chat session and want to export it. But how do you find the right session ID among hundreds of sessions?

**The Trick: Use a Unique Marker String**

1. Type a unique, random string in your chat message — something that won't appear anywhere else:
   ```
   XYZZY_EXPORT_ME_12345
   ```
   It can be anything unique — just make sure it's not a common word.

1. Now use the search command to find the session containing this marker:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py search "XYZZY_EXPORT_ME_12345"
   ```

1. The script will return exactly one match — your current session — with the workspace ID and session ID

1. Export it:
   ```
   python ./docs/modules/250-export-chat-session/tools/copilot/chat_export.py export <workspace_id> <session_id> --output-dir ./work/copilot_export
   ```

**Why this works:**

- VS Code saves chat messages to disk in real-time (as `.jsonl` deltas)
- The unique string is immediately searchable
- No need to guess which session is yours among dozens in the workspace
- Works even if the session has no title or a generic title like "untitled"

**Pro tip:** You can even ask the AI agent to do all three steps for you:
```
I just typed XYZZY_MARKER_123 in this chat.
Use the search command to find this session, then export it to HTML.
```

---

## Success Criteria

Congratulations! You've completed this module if:

✅ You understand where VS Code stores chat sessions on your computer  
✅ You can list workspaces and sessions using the export script  
✅ You've exported at least one session to HTML and opened it in a browser  
✅ You understand the token leakage risks and know what to check before sharing  
✅ You know how to create a session summary using AI  
✅ You understand how to use exported sessions as reference material for colleagues  
✅ You can search across sessions for specific information  
✅ You know the difference between HTML, JSON, and JSONL export formats  
✅ You can batch export ALL sessions from ALL workspaces using `export_all.py`  
✅ You know the marker string trick to find and export the current session  

## Understanding Check

1. **Where does VS Code store your chat sessions?**
   - In the workspace storage directory under `%APPDATA%/Code/User/workspaceStorage/` (Windows) or equivalent on other OS. Each workspace has a folder with a hex ID containing `.jsonl` session files.

1. **What information is stored in a chat session besides the text messages?**
   - Tool calls (file reads, edits, terminal commands), tool results, thinking blocks, model name, token counts, timing data, file attachments, screenshots, error details, and metadata.

1. **Why is it dangerous to share raw session exports publicly?**
   - Sessions may contain API keys, passwords, internal URLs, environment variables, file paths with usernames, and other secrets that appeared in terminal output or tool arguments.

1. **How can session summaries help in a team environment?**
   - They provide searchable documentation of what was built, how, and why. Colleagues can read summaries for onboarding, use them as references for similar tasks, create release notes, or understand the reasoning behind code decisions.

1. **What's the advantage of passing an exported session to a new AI conversation?**
   - The AI gets a complete example with code, decisions, problems, and solutions — it can follow the same patterns and approach for a similar task, dramatically improving output quality.

1. **When would you use JSON export instead of HTML?**
   - When you need to process session data programmatically — write analysis scripts, extract specific information, feed data into other tools, or perform automated processing.

1. **How do you find a specific past session without remembering its ID?**
   - Use the `search` command with keywords: `python chat_export.py search "keywords"` — it searches across all workspaces and sessions.

1. **How can you export ALL sessions at once?**
   - Use the `export_all.py` script: `python ./docs/modules/250-export-chat-session/tools/copilot/export_all.py` — it exports every session from every workspace, preserving the directory structure.

1. **How do you find and export the session you're currently in?**
   - Type a unique marker string (like `XYZZY_MARKER_123`) in the chat, then use `search` to find the session by that marker and export it by ID.

## Troubleshooting

**Script shows 0 workspaces**
- Make sure VS Code (or VS Code Insiders) has been used with Copilot chat at least once
- Check that the script auto-detects the correct VS Code variant
- Try specifying the path manually: `--vscode-path "%APPDATA%/Code - Insiders"`

**Batch export skips everything (all sessions "already exist")**
- This means all sessions were exported in a previous run
- To re-export, delete the output directory or use a different `--output-dir`

**Session shows 0 messages**
- The session may still be active and not fully flushed to disk
- Close the chat tab in VS Code, wait a moment, then try again

**Unicode errors on Windows**
- The script handles UTF-8 encoding automatically
- If issues persist, run `chcp 65001` in the terminal before running the script

**HTML export looks broken or has layout issues**
- This is a self-contained HTML file — open it in a modern browser (Chrome, Firefox, Edge)
- If you see vertical text or broken layout, report it — the tool is actively maintained

**Export file is very large (10+ MB)**
- Long sessions with many tool calls generate large exports
- This is normal — the file contains all tool inputs and outputs
- Use JSON format and write a filter script if you need a smaller subset

## Next Steps

Now that you can extract and preserve your AI chat sessions, you have a powerful tool for team knowledge sharing and project documentation. Consider creating a workflow where you export and summarize sessions after each significant milestone — this builds a searchable history of how your project evolved.
