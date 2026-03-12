# CI/CD Pipeline with AI Agents

**Duration:** 15 minutes

**Skill:** Set up a GitHub Actions pipeline that runs tests, enforces quality gates, and integrates AI review — automating the entire delegation-to-merge loop.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- GitHub Actions fundamentals: triggers, jobs, steps
- Running snapshot tests and unit tests automatically on every push
- Adding AI-assisted code review as a pipeline step
- Receiving notifications when a pipeline fails
- Walking through the complete loop: create issue → agent codes PR → CI runs → tests pass → merge

## Learning Outcome

You have a working CI/CD pipeline that runs your tests on every push, fails when output changes unexpectedly, and integrates with the AI agent delegation workflow from module 150.

## Prerequisites

### Required Modules

- [132 — AI-Assisted Test Generation & Snapshot Testing](../132-ai-assisted-test-generation/about.md)
- [150 — GitHub Coding Agent Delegation](../150-github-coding-agent-delegation/about.md)
- [152 — AI-Assisted Code Review](../152-ai-assisted-code-review/about.md)

### Required Skills & Tools

- GitHub repository with Actions enabled (free for public repos; limited free minutes for private)
- Tests from module 132 committed and passing locally
- A GitHub account with permission to create workflows in the repository
