# Elitea Remote MCP — HTTP Integration

**Duration:** 5-7 minutes

**Skill:** Configure Remote MCP servers on Elitea platform to connect cloud services (GitHub, Atlassian) via HTTP without local installation

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Understanding Remote MCP vs Stdio MCP architecture
- Configuring Remote MCP servers in Elitea platform UI
- Connecting external services (GitHub, Atlassian) via HTTP/HTTPS
- Authentication methods: Bearer tokens, OAuth 2.0, custom headers
- Discovering and syncing tools from remote MCP endpoints
- Testing MCP tools directly in Elitea UI
- Using Remote MCP in agents, pipelines, and chat
- Advanced settings: timeout, caching, tool filtering

## Learning Outcome

You will be able to create and configure Remote MCP servers on Elitea platform that connect to cloud services via HTTP/HTTPS. You'll understand the difference between Remote and Stdio MCP approaches, configure authentication (Bearer tokens, OAuth 2.0), discover and test available tools, and attach Remote MCPs to agents, pipelines, and chat sessions — all without installing anything locally.

## Prerequisites

### Required Modules

- [100 — Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)
- [165 — Elitea Platform MCP Integration](../165-elitea-platform-mcp-integration/about.md)

### Required Skills & Tools

- Active EPAM account with access to Elitea platform (https://next.elitea.ai)
- GitHub account with Personal Access Token or OAuth credentials
- Basic understanding of HTTP/HTTPS and REST APIs
- Internet connection for remote MCP server access

## When to Use

- Need to connect cloud services (GitHub, Jira, Confluence) to Elitea agents without local installation
- Want team-wide shared access to external tools through a centralized MCP configuration
- Require OAuth-based authentication for enterprise SaaS integrations
- Need to add external tool capabilities to Elitea agents or pipelines
- Want to avoid managing local MCP processes and dependencies
- Building production workflows that integrate multiple cloud services

## Resources

- [Elitea Remote MCP Documentation](https://elitea.ai/docs/integrations/mcp/create-and-use-remote-mcp/)
- [Elitea Stdio MCP Documentation](https://elitea.ai/docs/integrations/mcp/create-and-use-client-stdio/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
