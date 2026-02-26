# Elitea Remote MCP — HTTP Integration - Hands-on Walkthrough

In this walkthrough, you'll learn how to configure Remote MCP servers on the Elitea platform. Remote MCP connects Elitea agents to cloud services like GitHub and Atlassian via HTTP/HTTPS — no local installation, no Python environments, no CLI tools. Everything is configured through the Elitea web UI.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Set Up

Before we begin, let's understand what we'll be configuring:

- **Remote MCP Server**: A cloud-based MCP connection configured in Elitea UI that talks to external services over HTTP/HTTPS
- **Bearer Token Authentication**: API key in HTTP headers for simple authentication (used for GitHub example)
- **OAuth 2.0 Authentication**: Browser-based authorization flow for enterprise services (used for Atlassian example)
- **Tool Discovery**: Automatic detection of available tools from the remote MCP endpoint
- **Agent Integration**: Attaching Remote MCP tools to Elitea agents, pipelines, and chat

Unlike Module 165 (Stdio MCP), Remote MCP requires **zero local installation** — no Python, no virtual environments, no CLI tools. Everything runs in the cloud.

## Part 1: Understanding Remote vs Stdio MCP

### What We'll Do
Before configuring anything, let's understand why Remote MCP exists and when to choose it over the Stdio approach from Module 165.

### Key Differences

| Aspect | Remote MCP (this module) | Stdio MCP (Module 165) |
|--------|-------------------------|----------------------|
| Connection | HTTP/HTTPS over network | Local process (stdin/stdout) |
| Location | Remote server (cloud) | Your local machine |
| Authentication | Bearer tokens, OAuth 2.0 | Environment variables, local config |
| Installation | None (web UI only) | Python, pipx, alita-mcp client |
| Scalability | High (server-managed) | Limited (local resources) |
| Sharing | Multi-user, multi-project | Single user/machine |
| Latency | Network-dependent | Minimal (local) |
| Use Case | Cloud APIs (GitHub, Jira) | Local tools, file system access |

### When to Use Remote MCP

Choose Remote MCP when you need:
- Cloud-based integrations (GitHub, Atlassian, Figma)
- Enterprise SaaS tools requiring OAuth authentication
- Team-wide shared tool access across multiple users
- No local installation requirements
- Centralized credential management

### When to Use Stdio MCP

Choose Stdio MCP when you need:
- Local development tools (file system, browser automation)
- Custom tooling specific to your machine
- Minimal network latency for time-sensitive operations
- Tools requiring local system access

### What Just Happened
You now understand the architectural difference between Remote and Stdio MCP. Remote MCP communicates over HTTP — the MCP server runs somewhere in the cloud, and Elitea sends HTTP requests to it. Stdio MCP runs a local process that communicates via standard input/output streams.

## Part 2: Authentication Methods Overview

### What We'll Do
We'll review the three authentication methods available for Remote MCP before configuring a real connection.

### Method 1: Bearer Token (API Key)

The simplest approach. You provide an API token in HTTP headers:

```json
{
  "Authorization": "Bearer your-api-token-here"
}
```

**When to use**: GitHub Personal Access Tokens, internal corporate APIs, development/testing scenarios.

### Method 2: OAuth 2.0 Client Credentials

Enterprise-standard authentication used by GitHub, Atlassian, and most SaaS providers:

1. You click "Get / Sync tools" in Elitea
1. If OAuth is required, an authorization modal appears
1. You click "Authorize" and complete the flow in your browser
1. Elitea stores access and refresh tokens automatically
1. Tokens are refreshed automatically when they expire

**When to use**: Enterprise SaaS integrations, team-shared configurations, services requiring granular permission scopes.

### Method 3: Custom Authentication Headers

For services with proprietary authentication schemes:

```json
{
  "X-API-Key": "your-custom-key",
  "X-Client-ID": "your-client-id",
  "X-Project": "project-name"
}
```

**When to use**: Internal tools with proprietary auth, multi-header authentication, services requiring additional metadata.

### What Just Happened
You reviewed three authentication approaches. In the next parts, we'll use Bearer Token authentication for GitHub (simpler) and OAuth for Atlassian (enterprise-grade). Both are configured entirely through the Elitea web UI.

## Part 3: Creating a GitHub Remote MCP (Bearer Token)

### What We'll Do
We'll configure a Remote MCP server in Elitea that connects to GitHub API using a Personal Access Token. This enables Elitea agents to create issues, manage pull requests, search code, and more — all through the Elitea web interface.

### Step 3.1: Generate GitHub Personal Access Token

1. Open your browser and navigate to GitHub: https://github.com/settings/tokens

1. Click "Generate new token" → "Generate new token (classic)"

1. Fill in the token details:
   - **Note**: `Elitea MCP Access`
   - **Expiration**: Select `30 days` (recommended for security)
   - **Select scopes**:
     - ✔️ `repo` (Full control of private repositories)
     - ✔️ `read:org` (Read org and team membership)
     - ✔️ `workflow` (Update GitHub Actions workflows)
     - ✔️ `read:user` (Read user profile data)

1. Click "Generate token"

1. **IMPORTANT**: Copy the generated token immediately and save it securely
   - The token starts with `ghp_`
   - It will only be shown once
   - Do not commit this token to version control

### Step 3.2: Create Remote MCP in Elitea

1. Open your browser and navigate to https://next.elitea.ai/

1. Login with your EPAM credentials

1. In the left sidebar, click on "MCPs" section

1. Click the "+ Create" button

1. Select "Remote MCP" type from the form

### Step 3.3: Configure GitHub MCP Connection

1. Fill in the basic settings:
   - **Name**: `GitHub MCP`
   - **Description**: `GitHub integration for repository management, issues, and pull requests`

1. Configure the connection URL:
   - **URL**: `https://api.githubcopilot.com/mcp/`
   
   This is the official GitHub MCP endpoint.

1. Configure authentication headers:
   - **Headers**: Enter this JSON (replace `ghp_yourGitHubTokenHere` with your actual token):
   ```json
   {
     "Authorization": "Bearer ghp_yourGitHubTokenHere"
   }
   ```

1. Configure advanced settings (optional but recommended):
   - **Timeout**: `60` seconds (default)
   - **Enable Caching**: ✔️ Enabled
   - **Cache TTL**: `300` seconds (5 minutes)

### Step 3.4: Discover GitHub Tools

1. Click "Get / Sync tools" button

1. Wait for Elitea to connect to the GitHub MCP server and discover available tools

1. You should see a list of tools appear, including:

   | Tool Name | Description | Use Case |
   |-----------|-------------|----------|
   | `create_issue` | Create a GitHub issue | Bug reports, feature requests |
   | `create_pull_request` | Create a new pull request | Submit code changes |
   | `list_repositories` | List accessible repositories | Repository discovery |
   | `get_repository` | Get repository details | Repository information |
   | `list_pull_requests` | List PRs in a repository | PR review workflows |
   | `get_pull_request` | Get PR details | Review specific PR |
   | `create_comment` | Add comment to issue/PR | Automated responses |
   | `search_code` | Search code across repositories | Code analysis |
   | `get_file_contents` | Read file from repository | Code review, analysis |
   | `list_commits` | List commits in repository | History tracking |

1. By default, all tools are enabled. You can uncheck specific tools to exclude them if needed

1. Click "Save" to create the GitHub MCP

### What Just Happened
You created a Remote MCP configuration in Elitea that connects to GitHub's MCP endpoint over HTTPS. The Bearer token in the Authorization header authenticates every request. Elitea discovered available tools by querying the MCP server's tool list. These tools are now available to any agent, pipeline, or chat in your Elitea project.

## Part 4: Testing MCP Tools in Elitea

### What We'll Do
We'll test the GitHub MCP tools directly in the Elitea UI to verify the connection works correctly before using them in agents.

1. Navigate to "MCPs" in the left sidebar

1. Click on your "GitHub MCP" to open its details

1. Locate the "TEST SETTINGS" panel displaying all available tools

1. Select a read-only tool first — click on `list_repositories`

1. Click "Run" to execute the tool

1. Review the results — you should see a list of repositories accessible with your token

1. Now test a more specific tool — select `get_repository`:
   - Fill in required parameters (e.g., repository owner and name)
   - Click "Run"
   - Verify the repository details appear in the output

1. If all tests pass, your GitHub Remote MCP is working correctly

### What Just Happened
You verified that the Remote MCP connection is functional by executing tools directly in the Elitea UI. The TEST SETTINGS panel sends actual API calls through the MCP server, confirming that authentication, network connectivity, and tool execution all work correctly.

> **Best Practice**: Always test with read-only tools (like `list_repositories`, `get_repository`) before testing write operations (like `create_issue`, `create_pull_request`).

## Part 5: Creating an Atlassian Remote MCP (OAuth 2.0)

### What We'll Do
We'll configure a Remote MCP that connects to Atlassian (Jira and Confluence) using OAuth 2.0. Unlike the GitHub example that used a Bearer token, Atlassian uses browser-based OAuth authorization — you'll log in with your Atlassian account directly.

### Step 5.1: Check Atlassian Prerequisites

Before starting, verify you have:
- ✔️ An Atlassian account with access to Jira and/or Confluence
- ✔️ An Atlassian Cloud site (e.g., `your-company.atlassian.net`)
- ✔️ Appropriate permissions for the operations you want to perform
- ✔️ A modern browser for completing the OAuth 2.1 authorization flow

> **Note**: You do NOT need to create OAuth applications or obtain credentials in advance. Simply log in with your Atlassian account when prompted during the OAuth flow.

### Step 5.2: Create Atlassian Remote MCP

1. In Elitea platform, navigate to "MCPs" in the left sidebar

1. Click "+ Create" button

1. Select "Remote MCP" type

1. Fill in basic settings:
   - **Name**: `Atlassian MCP`
   - **Description**: `Jira and Confluence integration for project management and documentation`

1. Configure connection URL:
   - **URL**: `https://mcp.atlassian.com/v1/mcp`
   
   This is the official Atlassian Rovo MCP endpoint.

1. Configure advanced settings:
   - **Timeout**: `120` seconds (Atlassian operations can be slow)
   - **Enable Caching**: ✔️ Enabled
   - **Cache TTL**: `300` seconds (5 minutes)

1. Leave authentication fields empty (OAuth will handle this automatically):
   - **Headers**: `{}` (leave empty)
   - **Client ID**: (leave empty)
   - **Client Secret**: (leave empty)
   - **Scopes**: (leave empty)

### Step 5.3: Authorize via OAuth

1. Click "Get / Sync tools" button

1. An authorization modal appears automatically

1. Click "Authorize" to proceed

1. A new browser tab opens with the Atlassian OAuth page

1. Select your Atlassian site and approve the requested permissions

1. After approval, Atlassian redirects back to Elitea

1. Tools load automatically after successful authorization

### Step 5.4: Review Atlassian Tools

1. After successful authorization, you should see tools appear in two categories:

   **Jira Tools**:

   | Tool Name | Description | Use Case |
   |-----------|-------------|----------|
   | `jira_create_issue` | Create new Jira issue | Bug reports, tasks, stories |
   | `jira_get_issue` | Get issue details | Issue analysis |
   | `jira_update_issue` | Update existing issue | Status changes, assignments |
   | `jira_search_issues` | Search with JQL | Finding related issues |
   | `jira_get_board` | Get board information | Sprint planning |
   | `jira_get_sprint` | Get sprint details | Sprint management |
   | `jira_list_projects` | List accessible projects | Project discovery |
   | `jira_add_comment` | Add comment to issue | Collaboration |

   **Confluence Tools**:

   | Tool Name | Description | Use Case |
   |-----------|-------------|----------|
   | `confluence_create_page` | Create new page | Documentation generation |
   | `confluence_get_page` | Retrieve page content | Reading documentation |
   | `confluence_update_page` | Update existing page | Documentation updates |
   | `confluence_search_content` | Search Confluence | Finding documentation |
   | `confluence_list_spaces` | List Confluence spaces | Space discovery |

1. Click "Save" to create the Atlassian MCP

### What Just Happened
You configured a Remote MCP that uses OAuth 2.0 for authentication. Unlike the GitHub Bearer token approach, OAuth requires a browser-based authorization flow where you log in with your Atlassian account. Elitea stores the access and refresh tokens automatically and refreshes them when they expire. This is the enterprise-standard approach for team-shared integrations.

## Part 6: Using Remote MCP in Agents

### What We'll Do
We'll attach the configured Remote MCP to an Elitea agent so it can use GitHub and Atlassian tools during conversations.

### Step 6.1: Add Remote MCP to an Agent

1. In Elitea platform, click "Agents" in the left sidebar

1. Click "+ Create" for a new agent, or select an existing agent to edit

1. In the agent configuration, find the "TOOLKITS" section

1. Click the "+MCP" icon

1. Choose your Remote MCP from the list (e.g., "GitHub MCP")

1. The MCP will be added to your agent with all configured tools available

1. If the MCP requires OAuth and you're not already connected:
   - A "Log In" button appears next to the MCP
   - Click "Log In" to open the authorization modal
   - Complete the OAuth flow without leaving the agent editor
   - Once authorized, the MCP is ready to use

1. Click "Save" to save the agent configuration

### Step 6.2: Test Agent with MCP Tools

1. Open the agent's chat interface in Elitea

1. Send a test message that would trigger a GitHub tool:
   ```
   List my GitHub repositories
   ```

1. The agent should invoke the `list_repositories` tool from your GitHub MCP

1. Verify the response shows your actual GitHub repositories

1. Try another request:
   ```
   Show me the latest pull requests in repository [your-repo-name]
   ```

1. The agent should use the `list_pull_requests` tool and show real PR data

### What Just Happened
You attached a Remote MCP to an Elitea agent. The agent now has access to all GitHub tools and can invoke them during conversations. When you ask the agent to do something GitHub-related, it recognizes the relevant MCP tool and calls it automatically, passing parameters extracted from your message.

## Part 7: Using Remote MCP in Pipelines and Chat

### What We'll Do
Beyond agents, Remote MCPs can also be used in pipelines (automated workflows) and direct chat sessions.

### In Pipelines

1. Navigate to "Pipelines" in the sidebar

1. Create or edit a pipeline

1. In the "TOOLKITS" section, click "+MCP"

1. Choose your Remote MCP from the list

1. The MCP tools are now available for use in pipeline nodes

1. If OAuth is required, complete the authorization flow when prompted

### In Chat

1. Navigate to "Chat" in the sidebar

1. Start a new conversation or open an existing one

1. In the chat Participants section, look for the "MCP" element

1. Click "+MCP" to add the MCP

1. Choose your Remote MCP from available options

1. The MCP tools are now available in your conversation

1. If OAuth is required, complete the authorization flow when prompted

1. You can now directly interact with your Remote MCP by asking questions or requesting actions

### What Just Happened
Remote MCPs are not limited to agents — they integrate into Elitea's full ecosystem. Pipelines enable automated multi-step workflows using MCP tools. Chat allows ad-hoc tool usage without creating a dedicated agent. All three surfaces (agents, pipelines, chat) share the same Remote MCP configuration.

## Part 8: Understanding the Architecture

Now that everything is working, let's understand the complete flow:

1. **You configure Remote MCP** in Elitea UI with a URL and credentials
1. **Elitea connects** to the remote MCP server over HTTP/HTTPS
1. **Tool discovery** — Elitea queries the server for available tools
1. **You attach MCP** to an agent, pipeline, or chat
1. **User sends a request** that requires an external tool
1. **Agent selects tool** from available MCP tools based on request
1. **Elitea sends HTTP request** to the MCP server with tool parameters
1. **MCP server processes** the request (e.g., calls GitHub API)
1. **Response returns** through HTTP → Elitea → agent → user
1. **You see the result** in the Elitea chat interface

### Remote MCP vs Stdio MCP Architecture

```
Remote MCP (this module):
  Elitea UI → HTTP/HTTPS → Remote MCP Server → External API (GitHub, Jira)

Stdio MCP (Module 165):
  VS Code → stdin/stdout → Local alita-mcp process → Elitea API → Agent
```

### Benefits of Remote MCP

- **Zero local installation** — no Python, no pipx, no CLI tools
- **Team sharing** — one MCP configuration serves the entire team
- **Centralized management** — update credentials in one place
- **Enterprise security** — OAuth 2.0 with automatic token refresh
- **Scalability** — no local resource constraints
- **Reliability** — enterprise-grade hosting and availability

## Success Criteria

You should be able to check off these accomplishments:

✅ Understand the difference between Remote MCP and Stdio MCP  
✅ Know when to use each authentication method (Bearer, OAuth, Custom)  
✅ Created GitHub Remote MCP with Bearer token authentication  
✅ Discovered and reviewed available GitHub tools  
✅ Tested MCP tools using the TEST SETTINGS panel  
✅ Created Atlassian Remote MCP with OAuth 2.0 (if you have Atlassian access)  
✅ Attached Remote MCP to an Elitea agent  
✅ Tested agent interaction with MCP tools  
✅ Understand how to use Remote MCP in pipelines and chat  
✅ Understand the end-to-end architecture of Remote MCP  

## Understanding Check

Test your comprehension with these questions:

### Question 1: What is the key difference between Remote MCP and Stdio MCP?

**Expected answer**: Remote MCP connects to external services over HTTP/HTTPS — the MCP server runs on remote infrastructure and is accessed via network. Stdio MCP runs a local process on your machine and communicates via standard input/output streams. Remote MCP requires no local installation, while Stdio MCP needs Python, pipx, and local dependencies.

### Question 2: When would you choose Bearer token authentication over OAuth 2.0?

**Expected answer**: Bearer token is simpler and works well for individual use with API keys (like GitHub Personal Access Tokens). OAuth 2.0 is better for enterprise/team scenarios where you need granular permission scopes, automatic token refresh, and browser-based authorization. Services like Atlassian require OAuth because they don't support simple API keys.

### Question 3: Why is it important to test with read-only tools before write operations?

**Expected answer**: Read-only tools (like `list_repositories`, `get_issue`) verify that authentication and connectivity work without modifying any data. If there's a configuration error, you won't accidentally create issues, modify PRs, or change project data. It's a safe way to validate the entire MCP pipeline before enabling destructive operations.

### Question 4: How does Elitea handle expired OAuth tokens?

**Expected answer**: Elitea automatically refreshes OAuth tokens using refresh tokens when they expire. If the automatic refresh fails, a "Log In" button appears next to the MCP in the agent/pipeline/chat interface. Clicking it re-opens the OAuth authorization flow. You don't need to manually manage token lifecycle.

### Question 5: Can you use multiple Remote MCPs in a single agent?

**Expected answer**: Yes, you can add multiple Remote MCPs to a single agent, pipeline, or chat. Each MCP operates independently with its own authentication and tools. This is useful for integrating multiple services (e.g., GitHub + Jira + Confluence) in a single workflow. The agent selects the appropriate tool from any attached MCP based on the user's request.

### Question 6: What should you check if no tools appear after clicking "Get / Sync tools"?

**Expected answer**: Check: (1) authentication — is the Bearer token correct or has the OAuth flow completed, (2) URL — is it the correct MCP endpoint, (3) network — can you reach the server from your network, (4) timeout — increase it if the server is slow, (5) permissions — does your account have access to the tools. Also check the browser popup blocker for OAuth flows.

### Question 7: Why does Remote MCP not require any local installation?

**Expected answer**: Remote MCP runs entirely through the Elitea web UI. The MCP server is a cloud service (like GitHub's or Atlassian's MCP endpoint), and Elitea connects to it over HTTP/HTTPS. All configuration — URL, credentials, tool selection — is done in the browser. Unlike Stdio MCP, there's no local process to install, no Python environment to set up, and no CLI tools to manage.

## Troubleshooting

### Problem: "Get / Sync tools" returns no tools

**Symptoms**: Clicking the button shows no tools or an empty list

**Solutions**:
1. Verify the URL is correct (check for typos, ensure `https://` prefix)
1. Check Bearer token is valid and has required permissions/scopes
1. For OAuth — ensure authorization modal appeared and you completed the flow
1. Increase timeout value in Advanced Settings (try 120 seconds)
1. Check network connectivity — can you reach the MCP server from your browser?
1. Verify the MCP server is actually running (check provider status page)

### Problem: Authentication fails (401/403 errors)

**Symptoms**: HTTP 401 (Unauthorized) or 403 (Forbidden) errors when discovering or using tools

**Solutions**:
1. **Bearer token**: Verify token is correct, hasn't expired, and has required scopes
1. **OAuth**: Click "Log In" to re-authorize — token may have expired
1. Check header format: must be exactly `{"Authorization": "Bearer your-token"}`
1. For GitHub: ensure token has `repo`, `read:org`, `workflow`, `read:user` scopes
1. Regenerate token if necessary and update MCP configuration

### Problem: OAuth authorization flow fails or gets stuck

**Symptoms**: Authorization modal doesn't appear, or browser window gets stuck

**Solutions**:
1. Allow popups for Elitea domain in your browser settings
1. Try authorizing in a different browser (Chrome, Firefox, Edge)
1. Complete the OAuth flow quickly before session expires
1. If stuck, close the authorization window and click "Get / Sync tools" again
1. For Atlassian: verify your organization admin has allowed the Elitea domain
   - Admin must add `https://next.elitea.ai/**` in Atlassian Administration → Apps → AI settings → Rovo MCP server

### Problem: Tools fail during execution

**Symptoms**: Tools are discovered but fail when used in agents, pipelines, or chat

**Solutions**:
1. Test tools individually in the TEST SETTINGS panel first
1. Check if required parameters are missing — review tool documentation
1. Verify OAuth scopes include permissions for the specific operation
1. Check rate limits — reduce frequency of API calls if needed
1. For server errors (5xx) — retry after a delay, check provider status page

### Problem: Stale data or cached results

**Symptoms**: Tools show outdated information or changes not reflected

**Solutions**:
1. Click "Get / Sync tools" to refresh tool schemas
1. Reduce Cache TTL value for more frequent updates (e.g., from 300 to 60 seconds)
1. Disable caching temporarily for testing
1. Save the MCP configuration after making changes
1. Refresh the agent/pipeline/chat session to pick up new configuration

### Problem: Atlassian domain authorization error

**Symptoms**: Error message "Your organization admin must authorize access from a domain to this app"

**Solutions**:
1. Contact your Atlassian organization admin
1. Ask them to add `https://next.elitea.ai/**` in: Atlassian Administration → Apps → AI settings → Rovo MCP server → Add domain
1. Alternatively, ask admin to enable "Allow Atlassian supported domains"
1. This is an organization-level setting — only admins can change it

## Next Steps

After completing this module, you should:

### Experiment with Remote MCP Configurations

1. **Try different MCP providers**: GitHub, Atlassian, Figma, or any service that exposes an MCP endpoint
1. **Compare authentication methods**: Try both Bearer token and OAuth flows
1. **Configure multi-MCP agents**: Attach GitHub + Atlassian to a single agent for cross-platform workflows

### Build Production Workflows

1. **Code review agent**: Create an agent with GitHub MCP that reviews PRs and creates issues
1. **Documentation agent**: Use Atlassian MCP to automatically create/update Confluence pages
1. **Sprint management agent**: Combine Jira MCP with GitHub MCP for automated sprint tracking

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
   - Never commit tokens to version control
   - Rotate tokens regularly (every 30-90 days)
   - Use separate tokens for different environments
   - Prefer OAuth over static tokens for team configurations
   - Revoke tokens immediately if compromised

1. **Scope Management**:
   - Request only the OAuth scopes your agents actually need (principle of least privilege)
   - Document which scopes are required and why
   - Review and audit scope usage periodically

1. **Tool Filtering**:
   - Disable write/delete tools if your agent only needs read access
   - Use tool filtering to reduce attack surface
   - Start with read-only tools and enable write operations only when needed

### Configuration Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Name | String | Yes | Descriptive name for this MCP |
| Description | String | No | What this MCP provides |
| URL | String | Yes | HTTP/HTTPS endpoint for MCP server |
| Headers | JSON | No | Authentication headers (Bearer token, custom) |
| Client ID | String | No | OAuth 2.0 client identifier |
| Client Secret | String | No | OAuth 2.0 client secret |
| Scopes | Array | No | OAuth 2.0 permission scopes |
| Timeout | Integer | No | Request timeout in seconds (default: 60) |
| Enable Caching | Boolean | No | Cache tool schemas (default: true) |
| Cache TTL | Integer | No | Cache duration in seconds (default: 300) |

---

**Note**: This module requires an active EPAM employee account with Elitea platform access. The GitHub example requires a GitHub account with a Personal Access Token. The Atlassian example requires access to an Atlassian Cloud site.
