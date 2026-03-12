# AI-Assisted Test Generation & Snapshot Testing

**Duration:** 15 minutes

**Skill:** Generate tests with AI and implement snapshot testing — record your application's output, commit it to Git, and use `git diff` to detect regressions automatically.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Why testing AI-generated code matters and what types of tests exist
- Asking AI to generate unit tests for existing functions
- Snapshot testing: run → record output → commit → diff
- Using `git diff` as your assertion engine
- Accepting or rejecting changes via Git commit workflow

## Learning Outcome

You can protect your PoC from regressions using snapshot testing — a zero-assertion, black-box approach where Git tracks what changed — and supplement it with AI-generated unit tests for critical functions.

## Prerequisites

### Required Modules

- [060 — Version Control with Git](../060-version-control-git/about.md)
- [110 — Development Environment Setup](../110-development-environment-setup/about.md)
- [130 — QA with Chrome DevTools MCP](../130-chrome-devtools-mcp-qa-emulation/about.md)

### Required Skills & Tools

- A working PoC application (from module 120 or later) with at least one function or endpoint
- Basic terminal usage (running Python or Node.js scripts)
- Git repository with committed code baseline
