# Jira CLI Access via MCPyrex Python Script

**Duration:** 25-35 minutes

**Skill:** Build a Python CLI tool that queries Jira via REST API, configure a secure API token, and teach the AI agent to drive it using a `skill.md` descriptor — then optionally port the solution to any language.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why CLI beats MCP for Jira: context savings, binary file support, language portability
- Creating a Jira API token with minimum permissions, expiration, and IP restriction
- Using VPN to protect your token even if it leaks
- Building a Python CLI with `argparse` and `requests` using `.env` for secrets
- Downloading binary attachments — something MCP tools cannot do cleanly
- Creating a `skill.md` so the AI agent knows how to invoke the CLI
- Porting the solution to Node.js, Go, or Java using AI assistance

## Learning Outcome

You will have a working Jira CLI tool that can search issues, fetch details, and download attachments — secured by a scoped API token behind a VPN. You will also have a `skill.md` that lets any AI agent use this CLI as a tool, and the knowledge to port the pattern to any language.

## Prerequisites

### Required Modules

- [400 — Installing mcpyrex — MCP Python Toolbox](../400-installing-mcpyrex-mcp-python-toolbox/about.md)
- [108 — Token & API Key Management](../108-token-api-key-management/about.md)

### Recommended Modules

- [106 — Building Custom MCP Servers with FastMCP](../106-fastmcp-custom-mcp-server/about.md) — MCP alternative approach
- [440 — mcpyrex: Terminal Execution](../400-installing-mcpyrex-mcp-python-toolbox/about.md) — terminal tool in context
- [445 — mcpyrex: HTTP Client & REST APIs](../400-installing-mcpyrex-mcp-python-toolbox/about.md) — HTTP layer details

### Required Skills & Tools

- Python 3.9+ installed
- Jira account with API token access (Atlassian Cloud or Server)
- VS Code with GitHub Copilot
- Git and terminal access
- VPN client (recommended)

## When to Use

- When you need to query or manage Jira issues from AI chat without loading an MCP server
- When you need to download binary attachments (PDFs, images, ZIPs) from Jira issues
- When your Jira is self-hosted and official MCP servers don't support it
- When you want a portable, scriptable integration that works without an IDE

## Resources

- Atlassian API token management: [id.atlassian.com/manage-api-tokens](https://id.atlassian.com/manage-api-tokens)
- Jira REST API v3 docs: [developer.atlassian.com/cloud/jira/platform/rest/v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- Python `requests` library: [docs.python-requests.org](https://docs.python-requests.org)
- python-dotenv: [pypi.org/project/python-dotenv](https://pypi.org/project/python-dotenv/)
