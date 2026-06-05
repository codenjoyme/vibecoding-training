# CodeMie CLI Setup & IDE Integration

**Duration:** 45–60 minutes

**Skill:** Install, authenticate, and configure CodeMie CLI to run AI coding agents (Claude Code, Gemini, OpenCode) through your company's enterprise proxy, and connect them to VS Code or Cursor.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- What CodeMie CLI is and why it exists (enterprise AI proxy layer)
- Installing Node.js and the `@codemieai/code` npm package
- Authenticating with `codemie setup` — SSO, JWT, and other providers
- Installing AI coding agents: Claude Code, Gemini CLI, OpenCode
- IDE integration: Claude Code extension for VS Code and Cursor (proxy configuration)
- GitHub Copilot (GHCP) integration via relay proxy and `chatLanguageModels.json`
- One-time Copilot extension patch (`patch_jn.py`) to fix tool call tokenizer bug
- Running `codemie doctor` to health-check the installation
- Cross-platform troubleshooting with `tools/SKILL.md` as the reference guide

## Learning Outcome

CodeMie CLI is installed, authenticated, and connected to your IDE. `codemie doctor` reports all required checks as green. You know how to hand the `tools/SKILL.md` reference to your AI agent to get context-aware troubleshooting help.

## Prerequisites

### Required Modules

- [103 — CLI (Command Line Interface)](../103-cli-command-line-interface/about.md)
- [040 — Agent Mode Under the Hood](../040-agent-mode-under-the-hood/about.md) *(optional, recommended)*

### Required Skills & Tools

- Terminal access outside of any IDE (PowerShell on Windows, Terminal on macOS)
- Access to a CodeMie instance (URL provided by your team) or another supported auth provider
- Node.js LTS — installed during the walkthrough

## When to Use

Apply this module when:

- You need to run Claude Code, Gemini CLI, or OpenCode through a corporate AI gateway
- Your direct Anthropic/Google API access is restricted and CodeMie is your organisation's approved proxy
- You want to set up Cursor with the Claude Code extension pointing at a company-managed model
- You hit a setup or auth issue and want a structured reference to diagnose it

## Resources

- [nodejs.org](https://nodejs.org) — LTS download
- [python.org/downloads](https://python.org/downloads) — optional Python 3.13.x
- `tools/SKILL.md` — complete CodeMie CLI FAQ and reference (load this into your AI agent during setup)
