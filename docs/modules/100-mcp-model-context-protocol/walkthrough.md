# Model Context Protocol (MCP) - Hands-on Walkthrough

You've learned how to create skills by pairing instruction files with tools. But what if your AI assistant could connect directly to databases, APIs, file systems, and other data sources **without writing custom code every time**? That's exactly what the Model Context Protocol (MCP) enables—a standardized way to give AI assistants powerful capabilities through simple configuration.

## Prerequisites

- Basic understanding of AI Skills concept from [Module 090](../090-ai-skills-tools-creation/about.md)
- Familiarity with JSON configuration files
- Access to VS Code or Cursor IDE
- PowerShell (Windows) or Bash (Linux/macOS) available

## What We'll Build

In this module, you'll:
- Learn **why MCP is a game-changer** for AI-assisted development
- Set up your first MCP server (a simple echo server that requires no external dependencies)
- Configure MCP for **VS Code** or **Cursor** (different config locations and formats)
- Test MCP tools through AI chat
- Understand tool approval workflow and context management
- Build your own custom MCP server for file system operations

**Time required:** Approximately 15-20 minutes for complete walkthrough

---

## Part 1: Why MCP Matters

### The Problem Before MCP

Before MCP, if you wanted your AI assistant to:
- Access GitHub issues
- Query a database
- Read files from a specific directory
- Connect to an API

You had to:
1. Write custom code/scripts for each integration
2. Create instruction files explaining how to use them
3. Hope the AI would correctly invoke your tools
4. Repeat this process for every new data source

**Result:** Fragmentation, duplication, and lots of manual work.

### The MCP Solution

MCP is an **open protocol** (created by Anthropic) that standardizes how AI assistants connect to data sources and tools. Think of it like USB for AI capabilities:

- **One standard configuration format** - Add any MCP server with simple JSON
- **Plug-and-play servers** - Community-built servers for GitHub, databases, file systems, APIs
- **Auto-discovery** - AI assistant automatically sees available tools
- **Consistent interface** - All MCP servers use the same JSON-RPC protocol

**Key benefit:** Write once, use everywhere. The AI community shares MCP servers, so you don't reinvent the wheel.

### Real-World MCP Use Cases

1. **GitHub Integration** - Manage issues, PRs, and repos directly from chat
2. **Database Access** - Query PostgreSQL, MySQL, MongoDB without writing SQL scripts
3. **File System Operations** - Search, read, write files with proper permissions
4. **API Connectors** - Connect to Slack, Jira, Confluence, and more
5. **Custom Business Logic** - Expose your company's internal tools to AI

**The power:** MCP turns your AI assistant into a universal interface for all your development tools.

---

## Part 2: Setting Up Your First MCP Server

### What We'll Do

We'll set up a simple **echo MCP server** that demonstrates three basic tools:
- `echo` - Returns text back (tests communication)
- `get_time` - Returns current timestamp
- `calculate` - Performs basic arithmetic

This server is written in **PowerShell** (Windows) and **Bash** (Linux/macOS), requiring **zero external dependencies**—no Node.js, no Python, nothing to install. Perfect for learning!

### 2.1 Configuration for VS Code

**Important:** VS Code uses a different configuration format than Cursor!

1. **Locate your configuration file**
   
   Open or create: `.vscode/mcp.json` in your workspace root
   
   Path example: `c:/workspace/hello-genai/.vscode/mcp.json` (Windows) or `~/workspace/hello-genai/.vscode/mcp.json` (macOS/Linux)

2. **Copy the VS Code configuration template**
   
   A template file is provided at: `./docs/modules/100-mcp-model-context-protocol/tools/.vscode/mcp.json`
   
   Copy it to your workspace's `.vscode/` folder, or create a new file with this content:
   
   ```json
   {
     "servers": {
       "echo-windows": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.ps1"]
       },
       "echo-unix": {
         "command": "bash",
         "args": ["./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.sh"]
       }
     }
   }
   ```
   
   **Key field:** `servers` (not `mcpServers`)

3. **Choose the right server for your OS**
   
   - **Windows users:** Keep only `echo-windows`, remove `echo-unix` section
   - **Linux/macOS users:** Keep only `echo-unix`, remove `echo-windows` section
   - **Why?** Running both will cause errors if the other OS's shell isn't available
   
   **Windows final config:**
   ```json
   {
     "servers": {
       "echo-windows": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.ps1"]
       }
     }
   }
   ```
   
   **Linux/macOS final config:**
   ```json
   {
     "servers": {
       "echo-unix": {
         "command": "bash",
         "args": ["./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.sh"]
       }
     }
   }
   ```

4. **Make the bash script executable (Linux/macOS only)**
   
   Open terminal and run:
   ```bash
   chmod +x ./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.sh
   ```

5. **Reload VS Code window**
   
   - Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
   - Type "Reload Window"
   - Press Enter
   
   This activates the MCP server.

### 2.2 Configuration for Cursor

**Important:** Cursor uses a different configuration format and location!

1. **Locate your configuration file**
   
   Open or create: `.cursor/mcp.json` in your workspace root
   
   Path example: `c:/workspace/hello-genai/.cursor/mcp.json` (Windows) or `~/workspace/hello-genai/.cursor/mcp.json` (macOS/Linux)

2. **Copy the Cursor configuration template**
   
   A template file is provided at: `./docs/modules/100-mcp-model-context-protocol/tools/.cursor/mcp.json`
   
   Copy it to your workspace's `.cursor/` folder, or create a new file with this content:
   
   ```json
   {
     "mcpServers": {
       "echo-windows": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.ps1"]
       },
       "echo-unix": {
         "command": "bash",
         "args": ["./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.sh"]
       }
     }
   }
   ```
   
   **Key field:** `mcpServers` (not `servers` like VS Code)

3. **Choose the right server for your OS**
   
   Same as VS Code—keep only the section for your operating system:
   
   - **Windows:** Keep `echo-windows`, remove `echo-unix`
   - **Linux/macOS:** Keep `echo-unix`, remove `echo-windows`

4. **Reload Cursor window**
   
   - Open Command Palette
   - Type "Reload Window"
   - Press Enter

### What Just Happened

After reloading, your IDE:
1. Read the `mcp.json` configuration
2. Started the MCP server process (PowerShell or Bash script)
3. Connected to the server using JSON-RPC protocol
4. Discovered available tools (`echo`, `get_time`, `calculate`)
5. Made these tools available to your AI assistant

**Check the Output panel** (View → Output → select "Model Context Protocol") to see connection status. You should see: "Discovered 3 tools"

---

## Part 3: Testing Your MCP Server

### What We'll Do

Now that your MCP server is running, let's test each tool through AI chat and understand the approval workflow.

1. **Open AI chat in your IDE**
   
   - VS Code: Open GitHub Copilot Chat panel
   - Cursor: Open Cursor Chat (Cmd/Ctrl + L)

2. **Test the echo tool**
   
   Type in chat:
   ```
   Use the echo tool to send the message: "Hello MCP!"
   ```
   
   **What happens:**
   - AI detects the available `echo` tool
   - Prepares a tool call with your text
   - **Shows approval dialog** with the tool name and parameters
   - Waits for you to click "Allow"

3. **Understand the approval dialog**
   
   The dialog shows:
   - **Tool name:** `echo` (from your MCP server)
   - **Input parameters:** `{"text": "Hello MCP!"}`
   - **Warning:** "Note that MCP servers or malicious conversation content may attempt to misuse 'Code - Insiders' through tools"
   
   This is a **security feature**. MCP tools can execute code, read files, or access APIs, so you must explicitly approve each call.
   
   **Click "Allow"** to proceed.

4. **Verify the response**
   
   You should see: `Echo: Hello MCP!`
   
   **What happened:**
   - Your approval triggered the tool execution
   - IDE sent JSON-RPC request to MCP server
   - PowerShell/Bash script processed the request
   - Returned result through MCP protocol
   - AI received the response and showed it to you

5. **Test the time tool**
   
   Ask AI:
   ```
   What time is it right now? Use the get_time tool.
   ```
   
   Approve the tool call. You'll see current timestamp.

6. **Test the calculator**
   
   Ask AI:
   ```
   Calculate 42 multiplied by 17 using the calculate tool
   ```
   
   When the approval dialog appears, notice:
   - **Tool:** `calculate`
   - **Parameters:** `{"a": 42, "b": 17, "operation": "multiply"}`
   
   Approve it. Result: `Result: 42 multiply 17 = 714`

### Multiple Tool Approvals

Try asking something that requires multiple tools:

```
Echo the message "Starting calculation", then calculate 100 divided by 4, then echo "Done"
```

You'll see **three approval dialogs**—one for each tool call. This demonstrates:
- AI can chain multiple MCP tools
- Each tool call requires separate approval
- Tools execute in sequence

---

## Part 4: Managing MCP Tools and Context

### Enabling and Disabling MCP Servers

1. **Check active servers**
   
   Open the Output panel (View → Output) and select "Model Context Protocol"
   
   You'll see connection logs:
   ```
   [info] Starting server echo-windows
   [info] Connection state: Running
   [info] Discovered 3 tools
   ```

2. **Disable a server temporarily**
   
   Edit your `mcp.json` file and comment out the server:
   
   ```json
   {
     "servers": {
       // "echo-windows": {
       //   "command": "powershell",
       //   "args": ["-ExecutionPolicy", "Bypass", "-File", "./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.ps1"]
       // }
     }
   }
   ```
   
   Reload window. The server stops, and tools disappear from AI's context.

3. **Why disable tools?**
   
   Each MCP tool's description is added to the AI's context. With many servers:
   - **Context window fills up faster** (tool schemas take space)
   - **Slower response times** (more tools to evaluate)
   - **Higher costs** (if using paid API)
   
   **Best practice:** Enable only the MCP servers you're actively using.

### Managing Tool Approvals

1. **Per-session approvals**
   
   By default, each tool call requires approval. This is secure but can be tedious during development.

2. **Trust settings (if available)**
   
   Some IDEs allow configuring trusted MCP servers. Check your IDE settings:
   - VS Code: Settings → Extensions → GitHub Copilot → MCP
   - Cursor: Settings → MCP → Trusted Servers
   
   **Warning:** Only trust MCP servers from reliable sources!

3. **Reviewing tool calls before execution**
   
   Always review the approval dialog:
   - **Check tool name** - Is this the intended tool?
   - **Check parameters** - Do they match your request?
   - **Check file paths** - No access to sensitive directories?
   
   **Security tip:** If a tool call looks suspicious, click "Skip" and investigate why AI chose that tool.

---

## Part 5: Practical Task - Build Your Own MCP Server

### The Challenge

Create a custom MCP server with file system operations:
- `read_file` - Read file content with optional line range
- `write_file` - Write or append text to a file
- `list_files` - List files in a directory with optional filtering
- `search_files` - Search for text within files

This demonstrates how to build production-grade MCP tools for real workflows.

### Setup Steps

1. **Create the task directory**
   
   ```
   c:/workspace/hello-genai/work/100-task/
   ```
   
   or
   
   ```
   ~/workspace/hello-genai/work/100-task/
   ```

2. **Ask AI to scaffold the MCP server**
   
   Open AI chat and say:
   
   ```
   Create a MCP server in PowerShell (for Windows) at:
   ./work/100-task/mcp-filesystem.ps1
   
   Requirements:
   - Implement JSON-RPC 2.0 protocol (same structure as mcp-echo.ps1)
   - Four tools: read_file, write_file, list_files, search_files
   - read_file should accept: filepath, start_line (optional), end_line (optional)
   - write_file should accept: filepath, content, mode (write/append)
   - list_files should accept: directory, pattern (optional filter like *.txt)
   - search_files should accept: directory, search_text, file_pattern (optional)
   - Include proper error handling for missing files, invalid paths
   - Return results in MCP content format
   ```
   
   **For Linux/macOS users:** Request a Bash version instead:
   ```
   Create a MCP server in Bash at:
   ./work/100-task/mcp-filesystem.sh
   
   [same requirements as above]
   ```

3. **Review the generated code**
   
   AI will create a complete MCP server. Key sections to verify:
   - **Protocol handling** - Responds to `initialize`, `tools/list`, `tools/call`
   - **Tool schemas** - Each tool has proper `inputSchema` describing parameters
   - **Tool implementation** - Each tool performs the requested file operation
   - **Error handling** - Returns errors for invalid paths, permission issues

4. **Add your server to MCP configuration**
   
   Edit `.vscode/mcp.json` or `.cursor/mcp.json`:
   
   **VS Code (Windows):**
   ```json
   {
     "servers": {
       "echo-windows": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.ps1"]
       },
       "filesystem": {
         "command": "powershell",
         "args": ["-ExecutionPolicy", "Bypass", "-File", "./work/100-task/mcp-filesystem.ps1"]
       }
     }
   }
   ```
   
   **Cursor (Linux/macOS):**
   ```json
   {
     "mcpServers": {
       "echo-unix": {
         "command": "bash",
         "args": ["./docs/modules/100-mcp-model-context-protocol/tools/mcp-echo.sh"]
       },
       "filesystem": {
         "command": "bash",
         "args": ["./work/100-task/mcp-filesystem.sh"]
       }
     }
   }
   ```

5. **Reload window and verify**
   
   Reload your IDE window. Check the Output panel (Model Context Protocol):
   ```
   [info] Starting server filesystem
   [info] Discovered 4 tools
   ```

6. **Test each tool**
   
   **Test read_file:**
   ```
   Use the read_file tool to read lines 1-10 of the file ./readme.md
   ```
   
   **Test write_file:**
   ```
   Use write_file to create a file at ./work/100-task/test.txt with content:
   "Hello from MCP filesystem server!"
   ```
   
   **Test list_files:**
   ```
   Use list_files to show all .md files in the ./docs/modules/ directory
   ```
   
   **Test search_files:**
   ```
   Use search_files to find the word "MCP" in all files under ./docs/modules/100-mcp-model-context-protocol/
   ```

7. **Observe the workflow**
   
   For each tool:
   - AI selects the appropriate tool
   - Constructs parameters from your request
   - Shows approval dialog with full details
   - Executes after approval
   - Formats the result for you
   
   **This is the power of MCP:** You just described what you want. AI figured out which tool to use and how to call it.

### Advanced Challenge (Optional)

Enhance your MCP server with:
- `create_directory` - Create directories with parents
- `delete_file` - Remove files with confirmation
- `file_stats` - Get file size, modification date, permissions
- `backup_file` - Copy file to backup location

This turns your MCP server into a complete file management interface!

---

## Success Criteria

You've successfully completed this module when you can check off all of these:

✅ Understand why MCP standardizes AI tool integration  
✅ Configure MCP for either VS Code or Cursor  
✅ Know the difference between `.vscode/mcp.json` (servers) and `.cursor/mcp.json` (mcpServers)  
✅ Successfully run the echo MCP server and test all three tools  
✅ Approve tool calls and understand the security implications  
✅ Manage MCP servers by enabling/disabling them  
✅ Explain how multiple MCP tools affect context and performance  
✅ Build a custom MCP server for file system operations  
✅ Test custom tools through AI chat interface  

---

## Understanding Check

Answer these questions to verify your comprehension:

1. **What problem does MCP solve?**
   
   Expected answer: MCP standardizes how AI assistants connect to data sources and tools, eliminating the need to write custom integrations for each data source. It provides a plug-and-play system where community-built servers can be added with simple configuration.

2. **What's the difference between VS Code and Cursor MCP configuration?**
   
   Expected answer: VS Code uses `.vscode/mcp.json` with `"servers"` as the root key, while Cursor uses `.cursor/mcp.json` with `"mcpServers"` as the root key. The structure is otherwise identical.

3. **Why does each MCP tool call require approval?**
   
   Expected answer: Security. MCP tools can execute code, access files, call APIs, and modify data. Approval prevents malicious or unintended operations. You review the tool name and parameters before execution.

4. **How do many MCP tools affect your AI assistant?**
   
   Expected answer: Each tool's description is added to the AI's context. Many tools consume more context space, lead to slower responses, and increase costs (for paid APIs). Best practice: enable only needed servers.

5. **What are the three core MCP protocol methods?**
   
   Expected answer: 
   - `initialize` - Establishes connection and exchanges capabilities
   - `tools/list` - Returns available tools with schemas
   - `tools/call` - Executes a specific tool with parameters

6. **When would you create a custom MCP server vs. using an existing one?**
   
   Expected answer: Create custom when:
   - No existing server fits your needs
   - Integrating proprietary business systems
   - Need specialized operations with specific logic
   Use existing when:
   - Standard functionality (GitHub, databases, file systems)
   - Community-tested and maintained
   - Saves development time

7. **What information appears in the MCP tool approval dialog?**
   
   Expected answer: Tool name, input parameters (with values), and a security warning. This lets you verify the AI is calling the correct tool with expected data before execution.

---

## Troubleshooting

### Problem: "Server failed to start" error

**Symptoms:** Output panel shows connection errors

**Solutions:**
- Verify the script path is correct (relative to workspace root)
- Check file permissions (Linux/macOS: run `chmod +x script.sh`)
- Ensure PowerShell/Bash is available on your system
- Try absolute paths instead of relative paths in configuration

### Problem: "No tools discovered"

**Symptoms:** Server starts but no tools appear in AI chat

**Solutions:**
- Check Output panel for protocol errors
- Verify your script implements `tools/list` method correctly
- Ensure JSON-RPC responses are valid (use a JSON validator)
- Try restarting the MCP server (disable and re-enable in config)

### Problem: Tool approval dialog doesn't appear

**Symptoms:** AI mentions tools but doesn't call them

**Solutions:**
- Verify server is in "Running" state (check Output panel)
- Reload window to refresh MCP connections
- Check IDE settings for MCP tool access permissions
- Try explicitly asking AI to "use the [tool_name] tool"

### Problem: Bash script fails on Windows

**Symptoms:** Linux/macOS script doesn't work on Windows

**Solutions:**
- Use PowerShell version for Windows (`mcp-echo.ps1`)
- Remove `echo-unix` section from Windows configuration
- If you need bash on Windows, install Git for Windows which includes Git Bash
- Update script path to use Git Bash: `"C:\\Program Files\\Git\\bin\\bash.exe"`

### Problem: "Context length exceeded" error

**Symptoms:** AI stops responding or shows token limit errors

**Solutions:**
- Disable unused MCP servers (they consume context with tool descriptions)
- Break complex requests into smaller steps
- Use focused prompts instead of open-ended questions
- Clear chat history and start fresh conversation

---

## Next Steps

**Congratulations!** You've mastered the Model Context Protocol fundamentals. Here's what comes next:

1. **Module 105: MCP GitHub Integration** - Connect your AI assistant to GitHub for issue management
   
   Learn to:
   - Set up the official GitHub MCP server
   - Manage issues, PRs, and repos through chat
   - Use GitHub as a backlog for AI-generated ideas

2. **Explore the MCP ecosystem**
   
   Browse community MCP servers:
   - [Anthropic MCP Servers](https://github.com/modelcontextprotocol/servers) - Official collection
   - [MCP Server Registry](https://mcpregistry.org) - Community servers
   - Look for servers for databases, APIs, cloud services you use

3. **Build production MCP servers**
   
   Take your custom server further:
   - Add authentication and authorization
   - Implement rate limiting for API calls
   - Package as npm module or Docker container
   - Share with community (contribute to MCP ecosystem!)

4. **Combine MCP with AI Skills**
   
   Remember Module 090? MCP is the modern evolution:
   - MCP servers = standardized tools
   - Instruction files = guidance for using MCP tools
   - Together = powerful, reusable skills

---

## Additional Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/docs) - Official protocol documentation
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) - Build servers in TypeScript
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Build servers in Python
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) - Curated list of community servers

---

**Ready to connect your AI to GitHub?** Continue to [Module 105: MCP GitHub Integration](../105-mcp-github-integration-issues/about.md)
