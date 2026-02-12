# Elitea Platform MCP Integration - Hands-on Walkthrough

In this walkthrough, you'll learn how to integrate Elitea platform agents into your VS Code workflow using Model Context Protocol (MCP). You'll create a no-code agent on Elitea cloud platform and interact with it directly from your IDE through AI chat.

## Prerequisites

- VS Code installed with GitHub Copilot or Cursor IDE
- Active EPAM account with access to Elitea platform
- Python 3.10+ installed on your machine
- Completed Module 100 and Module 105 on MCP basics
- Internet connection for Elitea platform access

## What We'll Set Up

Before we begin, let's understand what we'll be installing and configuring:

- **Elitea Agent**: A cloud-based AI agent running on Elitea platform (no-code solution)
- **MCP Personal Token**: Authentication credential for API access to your Elitea agents
- **Python Virtual Environment**: Isolated Python environment for Elitea MCP client dependencies
- **Elitea MCP Client** (`alita-mcp`): Bridge between VS Code and Elitea API, installed via pipx
- **MCP Configuration**: Settings in `.vscode/mcp.json` to connect VS Code to Elitea server

This setup enables cloud-based agent execution without consuming local resources.

## Part 1: Elitea Platform Setup and Agent Creation

### What We'll Do
We'll login to Elitea platform, navigate to the Agents section, and create a simple "Hello World" agent. The agent will be configured to convert text to uppercase as a demonstration of cloud-based processing.

1. Open your web browser and navigate to https://next.elitea.ai/

2. Click "Login" button and authenticate with your EPAM credentials

3. After successful login, you'll see the Elitea dashboard with various sections

4. In the left sidebar, click on "Agents" section

5. Click the "Create" or "New Agent" button to start creating a new agent

6. In the agent creation form, fill in the following details:
   - **Agent Name**: `Hello World Agent`
   - **Description** (optional): `Simple processor for testing MCP integration`

7. In the "Instructions" field, add this exact text:
   ```
   You are a simple text processor. When you receive text input, convert it to uppercase and return only the uppercase version without any explanations or additional text.
   ```

8. **CRITICAL STEP**: In the "Tags" field, add the tag `mcp`
   - This tag is required for the agent to be discoverable through MCP protocol
   - Without this tag, your agent will not be accessible via VS Code even with correct configuration

9. Select a model for your agent (recommended: `gpt-4o` or `Claude Sonnet 4.5`)

10. Click "Save" or "Create" button to create the agent

### What Just Happened
You created a cloud-based AI agent with specific instructions. The "mcp" tag registered this agent for MCP protocol access. The agent now exists on Elitea infrastructure and can be invoked through API calls.

### Verify Agent in Elitea UI

1. In the Agents list, locate your "Hello World Agent"

2. Click on the agent to open its chat interface

3. Send this test message: `Hello world`

4. Verify the agent response shows `HELLO WORLD!` in uppercase

5. If the agent works correctly in Elitea UI, proceed to the next part

## Part 2: Generating MCP Personal Token

### What We'll Do
We'll generate an authentication token that allows the Elitea MCP client to access your agents through the API. This token acts as a password for programmatic access.

1. In Elitea platform, click on "Settings" in the left sidebar

2. Navigate to "Configuration" tab

3. Scroll down to find "Personal Tokens" section

4. Click "New personal token" or "Generate token" button

5. Fill in token details:
   - **Token Name**: `MCP Token`
   - **Expiration**: Select `30 days` (recommended for security)
   - You can choose longer expiration if needed, but shorter periods are more secure

6. Click "Generate" button

7. **IMPORTANT**: Copy the generated token immediately and save it securely
   - The token will only be shown once
   - If you lose it, you'll need to generate a new one
   - Do not commit this token to version control

8. Store the token in a secure location (password manager recommended)

### What Just Happened
You created an API access token with specific permissions and expiration. This token will be used by the MCP client to authenticate requests to Elitea API. Treat this token as a password - anyone with this token can access your Elitea agents.

## Part 3: Installing Python Virtual Environment and Elitea MCP Client

### What We'll Do
We'll create an isolated Python environment and install the Elitea MCP client tools. This keeps dependencies separate from your system Python and ensures reproducibility.

### Step 3.1: Create Python Virtual Environment

1. Open terminal or command prompt

2. Navigate to a suitable location for your Python environments:
   ```bash
   # Windows
   cd c:/workspace/
   
   # macOS/Linux
   cd ~/workspace/
   ```

3. Create a new virtual environment:
   ```bash
   python -m venv python_env
   ```
   
   This creates a folder `python_env` with isolated Python installation.

4. Activate the virtual environment:
   ```bash
   # Windows (Command Prompt)
   .\python_env\Scripts\activate
   
   # Windows (PowerShell)
   .\python_env\Scripts\Activate.ps1
   
   # macOS/Linux
   source python_env/bin/activate
   ```
   
   You should see `(python_env)` prefix in your terminal prompt.

### Step 3.2: Install Required Packages

1. With virtual environment activated, install `pipx`:
   ```bash
   pip install pipx
   ```

2. Configure pipx path:
   ```bash
   python -m pipx ensurepath
   ```

3. Install Elitea MCP client:
   ```bash
   pipx install alita-mcp
   ```

4. Ensure pipx is in PATH:
   ```bash
   pipx ensurepath
   ```

5. **IMPORTANT**: Close and reopen your terminal/command prompt to refresh PATH

6. Verify installation:
   ```bash
   alita-mcp --version
   ```
   
   You should see version information if installation was successful.

### What Just Happened
You installed `pipx` (a tool for installing Python CLI applications) and the `alita-mcp` client. The `ensurepath` command updated your system PATH so the `alita-mcp` command is available globally. Closing and reopening the terminal ensures the PATH changes take effect.

## Part 4: Bootstrap Configuration

### What We'll Do
We'll run the bootstrap command to configure the MCP client with your Elitea credentials and settings. This creates a configuration file that the client will use for all future connections.

1. Open a new terminal (to ensure PATH is updated)

2. Run the bootstrap command:
   ```bash
   alita-mcp bootstrap
   ```

3. The command will prompt you for several values. Enter them as follows:

   **Deployment URL**: 
   ```
   https://nexus.elitea.ai
   ```
   This is the Elitea API endpoint. Use exactly this URL.

   **Authentication token**: 
   Paste the MCP token you generated in Part 2. Press Enter after pasting.

   **Host**: 
   ```
   0.0.0.0
   ```
   This is the local host address for the MCP server.

   **Port**: 
   ```
   8000
   ```
   This is the port number for local MCP server communication.

   **Project ID**: 
   You need to find this in Elitea UI. In Elitea platform:
   - Click on "Projects" in sidebar
   - Your project name should be visible
   - The Project ID is usually displayed in the URL or project settings
   - It's typically a numeric value like `123` or `456`
   Enter your project ID number.

   **Server Name** (optional): 
   You can leave this blank or enter a custom name like `my-elitea-server`. Press Enter.

4. The bootstrap command will save configuration to a config file (location will be displayed)

5. Note the configuration file location for troubleshooting if needed

### What Just Happened
The bootstrap process created a configuration file containing your Elitea credentials and server settings. The `alita-mcp` command will read this file automatically when connecting to Elitea. The configuration is stored locally on your machine.

## Part 5: Configuring MCP in VS Code

### What We'll Do
We'll add Elitea server configuration to VS Code's MCP settings, telling VS Code to spawn the `alita-mcp` process and use it as an MCP server.

1. In VS Code, open your workspace (any project folder)

2. Create or open the file `.vscode/mcp.json` in your workspace root:
   ```bash
   # Windows
   c:/workspace/hello-genai/.vscode/mcp.json
   
   # macOS/Linux
   ~/workspace/hello-genai/.vscode/mcp.json
   ```

3. If the file doesn't exist, create it. If it exists, add to the "servers" section.

4. Add this configuration (replace `123` with your actual Project ID and `YOUR_AGENT_ID` with your agent's ID):
   ```json
   {
     "servers": {
       "elitea-mcp": {
         "command": "alita-mcp",
         "args": ["run", "--project-id", "123", "YOUR_AGENT_ID"]
       }
     }
   }
   ```
   
   **Note**: If you already have other MCP servers configured, add the "elitea-mcp" entry to your existing "servers" object.

5. **Important**: Replace `123` with your actual Project ID from Part 4

6. **Important**: Replace `YOUR_AGENT_ID` with your agent's ID. To find your agent ID:
   - In Elitea platform, click on your "Hello World Agent"
   - Look at the URL in your browser - it will contain the agent ID
   - Or check the agent settings page for the ID field
   - The ID typically looks like `i1818` or similar alphanumeric code

7. Save the file

### What Just Happened
You configured VS Code to launch the `alita-mcp` process with specific parameters. When VS Code starts, it will run this command, which connects to Elitea API using the bootstrap configuration. The MCP server discovers agents tagged with "mcp" and exposes them as tools to VS Code AI chat.

## Part 6: Testing Connection and Verification

### What We'll Do
We'll reload VS Code to activate the new MCP server, verify the connection is working, and test communication with your Elitea agent.

### Step 6.1: Reload VS Code

1. Press the command palette shortcut (menu: View → Command Palette)

2. Type `Reload Window` and press Enter

3. Wait for VS Code to reload (takes 5-10 seconds)

### Step 6.2: Verify Server Connection

1. Open the Output panel (menu: View → Output)

2. In the Output panel dropdown, select "Model Context Protocol"

3. Look for messages about "elitea-mcp" server

4. You should see a line like:
   ```
   [elitea-mcp] Discovered Tools: ...
   ```
   
   This indicates the server connected successfully and discovered your agents.

5. If you see error messages, proceed to Troubleshooting section

### Step 6.3: Test Agent Through AI Chat

1. Open AI chat in VS Code (GitHub Copilot chat panel or Cursor AI chat)

2. Send this message:
   ```
   Send "Hello World" to my Elitea agent
   ```

3. The AI should detect available tools from elitea-mcp server

4. You may see a prompt asking to approve tool execution - click "Allow" or "Approve"

5. Wait for the agent to process (may take 5-15 seconds for first request)

6. Verify the response shows "HELLO WORLD!" from your agent

7. The response should come from the cloud-based agent, not from the local AI model

### What Just Happened
VS Code spawned the `alita-mcp` process which connected to Elitea API. The server discovered your agent (tagged with "mcp") and registered it as an available tool. When you sent a message through AI chat, VS Code invoked the Elitea agent tool, which made an API call to your cloud agent, received the response, and displayed it in the chat.

## Part 7: Understanding the System

Now that everything is working, let's understand what happens when you interact with your Elitea agent:

1. **You send a message** in VS Code AI chat requesting to use Elitea agent
2. **VS Code AI** recognizes the request and checks available MCP tools
3. **MCP Server** (alita-mcp process) exposes Elitea agent as a tool
4. **Tool invocation** sends request to Elitea API with your authentication token
5. **Elitea platform** receives request, executes your agent with provided input
6. **Agent processes** input according to its instructions (e.g., converts to uppercase)
7. **Response returns** through API → MCP server → VS Code → AI chat
8. **You see the result** directly in your IDE without leaving the development environment

This architecture enables:
- **Zero local resources** used for AI processing (runs in Elitea cloud)
- **Enterprise security** with token-based authentication
- **Team collaboration** with shared cloud agents
- **Centralized management** of agent configurations
- **Professional infrastructure** without maintaining servers

## Success Criteria

You should be able to check off these accomplishments:

✅ Successfully logged in to Elitea platform  
✅ Created agent with "mcp" tag  
✅ Generated and saved MCP personal token  
✅ Created Python virtual environment  
✅ Installed Elitea MCP client via pipx  
✅ Completed bootstrap configuration with deployment URL and token  
✅ Added Elitea server to `.vscode/mcp.json`  
✅ Reloaded VS Code and saw "Discovered Tools" in Output panel  
✅ Sent test message to agent through VS Code AI chat  
✅ Received agent response in IDE (HELLO WORLD!)  
✅ Understand cloud agent benefits vs local tools  

## Understanding Check

Test your comprehension with these questions:

### Question 1: Why is the "mcp" tag required for agents on Elitea?

**Expected answer**: The "mcp" tag makes the agent discoverable and accessible through MCP protocol. Without this tag, the agent won't be visible to MCP clients even if configured correctly. It acts as a filter that tells the Elitea API which agents should be exposed through the MCP interface.

### Question 2: What's the difference between Elitea agents and local MCP servers (like echo from Module 100)?

**Expected answer**: Elitea agents run in the cloud (no-code solution, no local installation), while local MCP servers run scripts on your machine. Elitea provides enterprise-grade agent infrastructure with professional security and team collaboration, while local servers are for custom tools and scripts that need direct file system access.

### Question 3: Why do we need a Python virtual environment for Elitea MCP client?

**Expected answer**: Virtual environment isolates dependencies and prevents conflicts with other Python projects. It ensures clean installation and reproducibility. If you install packages globally, they might conflict with other projects or system Python packages, causing version compatibility issues.

### Question 4: What information does bootstrap configuration collect?

**Expected answer**: Bootstrap collects: Deployment URL (Elitea API endpoint), authentication token (for API access), host/port (local server settings for MCP communication), project ID (to identify your Elitea project), and optional server name (for identification in logs and config).

### Question 5: How does VS Code discover Elitea agents?

**Expected answer**: VS Code runs the `alita-mcp` command specified in `mcp.json`, which connects to Elitea API using credentials from bootstrap config. The server queries Elitea API for agents tagged with "mcp" in your project and exposes them as MCP tools. VS Code AI can then invoke these tools when you request agent functionality.

### Question 6: What should you do if the MCP token expires?

**Expected answer**: Generate a new token in Elitea Settings → Personal Tokens, then re-run `alita-mcp bootstrap` with the new token, or manually update the authentication token in the configuration file (location shown during bootstrap). After updating, reload VS Code window to reconnect with new credentials.

### Question 7: Why use cloud-based agents instead of running everything locally?

**Expected answer**: Cloud agents provide: no local resource usage (CPU/RAM/GPU), enterprise security and compliance, team collaboration (shared agents), centralized management (one place to update), professional infrastructure (no maintenance), and consistent availability. Good for production workflows and team environments. Local tools are better for custom scripts and development tasks requiring file system access.

## Troubleshooting

### Problem: "alita-mcp: command not found"

**Symptoms**: Bootstrap command fails with command not found error

**Solutions**:
1. Ensure pipx is installed: `pip install pipx`
2. Run ensurepath: `python -m pipx ensurepath`
3. Close and restart terminal/CLI after installation
4. Verify installation: `pipx list` (should show alita-mcp)
5. Check if pipx binary directory is in PATH
6. On Windows, try running as administrator if permission issues occur

### Problem: "Authentication failed" in bootstrap

**Symptoms**: Cannot connect to Elitea API during bootstrap or when testing

**Solutions**:
1. Verify token was copied correctly (no extra spaces or newlines)
2. Check token hasn't expired in Elitea Settings → Personal Tokens
3. Ensure deployment URL is exactly: `https://nexus.elitea.ai` (no trailing slash)
4. Confirm EPAM account has Elitea platform access
5. Try generating a new token and running bootstrap again
6. Check if there are any network/proxy restrictions blocking access to Elitea

### Problem: "No tools discovered" in VS Code

**Symptoms**: Elitea agents not visible in AI chat, no tools listed in Output panel

**Solutions**:
1. **Most common**: Verify agent has "mcp" tag in Elitea UI
2. Check project ID matches in `mcp.json` and bootstrap config
3. Reload VS Code window (Command Palette → Reload Window)
4. Check Output panel (Model Context Protocol) for error messages
5. Verify server shows "Running" status or similar in MCP output
6. Ensure you're using correct agent ID in mcp.json args
7. Confirm bootstrap configuration completed successfully

### Problem: Agent created but not showing in MCP

**Symptoms**: Agent works in Elitea UI but not accessible via MCP in VS Code

**Solutions**:
1. **Critical**: Ensure "mcp" tag is set on agent (check in Elitea agent settings)
2. Wait 1-2 minutes for agent indexing in Elitea system
3. Reload VS Code window completely
4. Verify project ID is correct in configuration
5. Check agent is not in Draft status (must be published/active)
6. Try removing and re-adding the agent tag
7. Check if agent ID in mcp.json matches the actual agent ID

### Problem: MCP server fails to start

**Symptoms**: Error in Output panel when VS Code loads, server not running

**Solutions**:
1. Verify Python virtual environment is activated when running tests
2. Re-run `alita-mcp bootstrap` to reconfigure
3. Check `mcp.json` syntax is valid JSON (use online JSON validator)
4. Verify project ID and agent ID are provided as strings in the args array
5. Try absolute path to alita-mcp executable in mcp.json command field
6. Check if port 8000 is already in use (change port in bootstrap if needed)
7. Review bootstrap configuration file for any obvious errors

### Problem: Agent response is slow or times out

**Symptoms**: Long wait times when invoking agent, timeout errors

**Solutions**:
1. Elitea cloud processing may take 10-30 seconds for first request (cold start)
2. Subsequent requests should be faster (warm state)
3. Check your internet connection speed
4. Verify Elitea platform status (not under maintenance)
5. Try with a simpler agent instruction or lighter model
6. Check if your organization has any network throttling policies

## Next Steps

After completing this module, you should:

### Experiment with Agent Capabilities

1. **Create different agent types**:
   - Code review agent with specific quality criteria
   - Documentation generator agent
   - Test case creation agent
   - Data transformation agent

2. **Test various models**:
   - Compare GPT-4 vs Claude vs other models
   - Evaluate response quality and speed
   - Find best model for your use cases

3. **Explore agent toolkits**:
   - Add tools to your agents in Elitea UI
   - Enable file access, API calls, or database queries
   - Create multi-capability agents

### Integrate into Your Workflows

1. **Use Elitea agents for regular tasks**:
   - Code review automation
   - Documentation updates
   - Data validation and transformation
   - Report generation

2. **Team collaboration**:
   - Share agents with team members
   - Create organization-wide agents
   - Standardize processing logic

3. **Build production workflows**:
   - Integrate agents into CI/CD pipelines
   - Use for automated quality checks
   - Create specialized processing services

### Continue Learning

Proceed to **[Module 170: DIAL API Key CURL Access](../170-dial-api-key-curl-access/about.md)**:
- Learn direct API access to DIAL/Elitea
- Understand low-level API interactions
- Build custom integrations without MCP
- Send requests via cURL for testing
- Prepare for building Python applications

## Additional Notes

### Security Best Practices

1. **Token Management**:
   - Never commit MCP tokens to version control
   - Use `.gitignore` to exclude configuration files with tokens
   - Rotate tokens regularly (every 30-90 days)
   - Use separate tokens for different environments
   - Revoke tokens immediately if compromised

2. **Agent Design**:
   - Keep agent instructions clear and specific
   - Test agents thoroughly in Elitea UI before MCP deployment
   - Document agent capabilities for team members
   - Consider agent purpose: simple processing vs complex workflows
   - Use appropriate model for task complexity

3. **Access Control**:
   - Limit project access to authorized team members
   - Review agent permissions regularly
   - Use project-level isolation for sensitive data
   - Monitor agent usage and API calls

### Technical Architecture

The Elitea MCP integration works through these components:

1. **Elitea Platform**: Cloud infrastructure hosting your AI agents
2. **RESTful API**: Provides programmatic access to agents
3. **MCP Client** (`alita-mcp`): Bridge between VS Code and Elitea API
4. **Bootstrap Config**: Local file storing credentials and settings
5. **VS Code MCP Extension**: Spawns and manages MCP server processes
6. **AI Chat Interface**: User interface for interacting with tools

When you send a request:
- VS Code AI detects tool invocation
- MCP protocol communicates with alita-mcp server
- Server makes authenticated API call to Elitea
- Elitea executes agent with your input
- Response flows back through the chain
- Result appears in VS Code chat

This architecture provides:
- **Separation of concerns**: VS Code handles UI, Elitea handles AI processing
- **Scalability**: Cloud infrastructure scales automatically
- **Security**: Token-based authentication with expiration
- **Flexibility**: Add/remove agents without VS Code changes
- **Reliability**: Professional infrastructure with monitoring and support

---

**Note**: This module requires an active EPAM employee account with Elitea platform access. External users should check alternative AI agent platforms with MCP support, such as Claude MCP servers, Langchain MCP integrations, or other enterprise AI platforms.
