# CLI: Command Line Interface

**Duration:** 10-15 minutes  
**Skill:** Call REST APIs directly from terminal using curl — bypassing LLM for deterministic, token-efficient tool execution without hallucination risk

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- What CLI is and how it relates to REST API
- Why calling tools directly (without LLM in the middle) is deterministic and avoids hallucinations
- Running a local REST server with the same 3 tools from Module 100
- Calling `echo`, `get_time`, and `calculate` via curl
- Sending binary files — what MCP can't do natively
- When to use CLI vs MCP

## Learning Outcome

Understand the difference between MCP (LLM-mediated tool calls) and CLI (direct tool calls), and know when each approach is appropriate

## Prerequisites

### Required Modules

- [100 — Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)

### Required Skills & Tools

- Basic familiarity with terminal/PowerShell
- curl available (pre-installed on Windows 10+, macOS, Linux)
- Python 3 available (`python --version`)
