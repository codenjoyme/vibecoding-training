# Token & API Key Management

**Duration:** 15 minutes

**Skill:** Set up a secure secrets workflow using `.env` files and environment variables so API keys never end up in Git.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why API keys leak and what the consequences are
- The `.env` + `dotenv` pattern for Python and Node.js projects
- Setting and reading environment variables in PowerShell and bash
- How to rotate a compromised key
- Pre-commit checklist: verify no secrets in staged files

## Learning Outcome

You have a working `.env` setup for your projects, `.env` is always in `.gitignore`, and you have a secrets checklist you run before every commit.

## Prerequisites

### Required Modules

- [060 — Version Control with Git](../060-version-control-git/about.md)
- [105 — MCP GitHub Integration](../105-mcp-github-integration-issues/about.md)

### Required Skills & Tools

- Git installed and configured
- At least one API key in use (DIAL, GitHub, or any MCP server key)
- Python or Node.js installed (for loading `.env` in code)
