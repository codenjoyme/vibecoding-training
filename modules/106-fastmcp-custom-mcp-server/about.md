# Building Custom MCP Servers with FastMCP

**Duration:** 15-20 minutes  
**Skill:** Build a secure, Python-based MCP server that wraps any REST API using the FastMCP framework

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Five approaches to integrating AI with self-hosted tools (Jira as a case study)
- Security risks of connecting unreviewed community MCP servers
- When to use official vendor-provided MCP servers
- Using open-source MCP code as a reference and learning tool
- Building a custom MCP server with FastMCP: tools, resources, and `.env`-based secrets
- Hands-on: wrapping a REST API in a FastMCP server and connecting it to VS Code

## Learning Outcome

You understand the full spectrum of MCP integration options and their trade-offs. You can build a production-ready FastMCP server that safely wraps any HTTP API, injects credentials via environment variables, and connects to your IDE — without exposing tokens or depending on third-party code you haven't reviewed.

## Prerequisites

### Required Modules

- [100 — Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)
- [105 — MCP GitHub Integration — Issues](../105-mcp-github-integration-issues/about.md)
- [108 — Token & API Key Management](../108-token-api-key-management/about.md)

### Required Skills & Tools

- Python 3.10+ installed
- Basic Python knowledge (functions, decorators, imports)
- Access to any REST API with a personal access token (Jira, GitHub, GitLab, etc.)
- VS Code with GitHub Copilot or Cursor IDE

## When to Use

- You need to connect AI to a self-hosted tool that has no official cloud MCP
- You want full control over what the AI can and cannot do with your API
- Your security team requires you to avoid unreviewed third-party MCP servers
- You want to wrap an existing HTTP API without rewriting it

## Resources

- [FastMCP GitHub](https://github.com/PrefectHQ/fastmcp)
- [FastMCP Documentation](https://gofastmcp.com/)
- [Docker Hub MCP Catalog](https://hub.docker.com/mcp) — open-source MCP reference implementations
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
