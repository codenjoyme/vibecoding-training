# CLI Snapshot Testing with Docker

**Duration:** 5-7 minutes  
**Skill:** Test any CLI tool by capturing its full output as a golden Markdown snapshot and reviewing changes via `git diff`

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Approval Tests concept and its origins (Llewellyn Falco)
- Snapshot-based testing vs traditional assertions
- Markdown-based scenario format: commands + descriptions + captured output
- OS-agnostic testing with Docker containers
- Using `git diff` + LLM for regression analysis
- Customizing the framework for any CLI tool

## Learning Outcome

Set up a complete CLI snapshot testing pipeline: write scenario files, configure Docker for your CLI, run tests, commit golden snapshots, and use `git diff` to detect regressions — all without writing a single assertion.

## Prerequisites

### Required Modules

- [060 — Version Control with Git](../060-version-control-git/about.md)
- [090 — AI Skills & Tools Creation](../090-ai-skills-tools-creation/about.md) *(optional, recommended)*

### Required Skills & Tools

- Docker Desktop installed and running
- Terminal access (PowerShell on Windows, bash on Linux/macOS)
- Basic understanding of CLI tools and command-line usage
- Git installed and configured

## When to Use

- You have a CLI tool (your own or third-party) and want to verify its behavior after changes
- You're refactoring a legacy CLI and need a safety net
- You want to document CLI behavior as living, verifiable Markdown
- You need OS-agnostic tests that run the same on any developer's machine
