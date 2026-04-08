# MCP Image Viewer Tool in PowerShell

**Duration:** 15-20 minutes  
**Skill:** Build a PowerShell MCP server that returns local images as base64 content, so AI can load and analyze images from the filesystem without manual file attachment

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- MCP protocol image content type (`type: "image"`, `data`, `mimeType`)
- How `chrome-devtools-mcp` returns screenshots as base64 in MCP responses
- Building a PowerShell MCP server from scratch (extending the echo pattern)
- Implementing a `load_image` tool that reads a file and returns it as base64
- Registering the local MCP server in `.vscode/mcp.json`
- Testing: asking AI to load and describe an image by file path

## Learning Outcome

Build and register a local PowerShell MCP tool that lets the AI load any image from your filesystem on demand — no manual attachment required

## Prerequisites

### Required Modules

- [035 — Visual Context with Screenshots](../035-visual-context-screenshots/about.md)
- [105 — MCP GitHub Integration — Issues Management](../105-mcp-github-integration-issues/about.md)

### Required Skills & Tools

- PowerShell available in terminal
- `.vscode/mcp.json` already working in the workspace (from module 100/105)
- Understanding of base64 encoding (basic awareness is enough)
- VS Code with GitHub Copilot Agent Mode

## When to Use

- You have images saved on disk that you want AI to analyze repeatedly
- You're building automation pipelines that generate screenshots for AI review
- You want AI to access diagrams, mockups, or exported visuals without manual intervention
- You're experimenting with MCP protocol to understand image content types
