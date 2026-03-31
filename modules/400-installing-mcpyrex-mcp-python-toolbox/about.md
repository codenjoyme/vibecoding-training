# Installing mcpyrex — MCP Python Toolbox

**Duration:** 15-20 minutes

**Skill:** Install mcpyrex — an open-source MCP server with 30+ Python/Langchain tools — into a dedicated workspace, verify the MCP connection with GitHub Copilot, and run your first deterministic tool from both terminal and chat.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- What mcpyrex is and why deterministic MCP tools matter
- Cloning the repository into a separate workspace
- Running the interactive installer (Python, virtualenv, pip dependencies)
- IDE configuration: `.vscode/mcp.json` and workspace settings
- Verifying MCP server connectivity with GitHub Copilot
- Running tools from terminal (`python -m mcp_server.run`)
- Running tools from AI chat (asking Copilot to use a tool)
- Exploring the tool catalog with `lng_get_tools_info`

## Learning Outcome

You will have a fully working mcpyrex installation with 30+ MCP tools accessible from both terminal and GitHub Copilot chat. You will understand the project architecture (tools, projects, pipelines) and be able to verify that any tool responds correctly.

## Prerequisites

### Required Modules

- [010 — Installing VSCode + GitHub Copilot](../010-installing-vscode-github-copilot/about.md)
- [100 — Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)

### Required Skills & Tools

- VS Code with GitHub Copilot installed and working
- Git installed and available in terminal
- Internet connection (for cloning repository and installing dependencies)
- Basic terminal familiarity (running commands, navigating directories)

## When to Use

- When you want to extend GitHub Copilot with deterministic Python tools
- When you need precise operations (math, word counting, file processing) that LLMs hallucinate on
- When starting the mcpyrex training module series (400+)
- When you want a reference MCP server implementation to study

## Resources

- mcpyrex repository: [github.com/codenjoyme/mcpyrex-python](https://github.com/codenjoyme/mcpyrex-python)
- MCP Protocol docs: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- Security disclaimer: review `mcp_server/security-disclaimer.md` in the cloned project
