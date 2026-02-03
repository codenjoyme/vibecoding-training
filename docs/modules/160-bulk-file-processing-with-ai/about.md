# Bulk File Processing with AI Agents

**Duration:** 5-7 minutes

**Skill:** Learn three approaches for processing multiple files with AI agents, understanding trade-offs between context drift, token efficiency, and automation.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Context drift and hallucinations in long-running AI sessions
- Single-session bulk processing vs. iterative approaches
- Script-based deterministic AI agent invocation
- GitHub Copilot CLI for automated file processing
- Token efficiency in bulk operations

## Learning Outcome

You will understand three evolutionary approaches to bulk file processing with AI: direct IDE agent requests, iterative prompting with instruction re-reading, and script-based automation. You'll implement the most efficient approach using GitHub Copilot CLI and Python to validate 20+ files with consistent quality.

## Prerequisites

- Completed Module 150: GitHub Coding Agent Delegation
- GitHub Copilot extension installed in VS Code
- Basic understanding of command line and Python scripts
- Familiarity with prompt engineering concepts

## When to Use

- Processing 20+ files with same transformation or validation
- Ensuring consistent quality across multiple code reviews
- Automating repetitive AI-assisted tasks
- Reducing token costs in bulk operations
- Avoiding context drift in large-scale refactoring

## Resources

- [GitHub Copilot CLI Installation Guide](../../instructions/github-copilot-cli-installation.agent.md)
- Example script: [validate_walkthroughs.py](tools/validate_walkthroughs.py)
- Example instruction: [validate-walkthrough.instruction.md](tools/validate-walkthrough.instruction.md)
