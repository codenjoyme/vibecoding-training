# Reverse Engineering Project Knowledge from Text

**Duration:** 15 minutes

**Skill:** Extract project conventions, architecture rules, and working instructions from pairs of existing artifacts (issues + diffs, specs + code, PRs + reviews) using the AI text-triangle principle — where any two related texts can generate the third.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- The text-triangle principle: if two related texts produce a third, any two can reconstruct the missing one
- Extracting meta-knowledge from issue + commit diff pairs
- Building project instructions incrementally, commit by commit
- Reverse engineering coding conventions, architecture decisions, and team workflow
- Creating reusable instruction files from reverse-engineered knowledge

## Learning Outcome

You can take a project with zero documentation, find completed issues and their commit diffs, and feed them to an AI model to extract project conventions, coding standards, architecture decisions, and workflow rules — producing usable instruction files that capture how the team actually works.

## Prerequisites

### Required Modules

- [070 — Custom Instructions](../070-custom-instructions/about.md)
- [060 — Version Control with Git](../060-version-control-git/about.md)
- [105 — MCP GitHub Integration](../105-mcp-github-integration-issues/about.md) *(optional, recommended)*
- [160 — Bulk File Processing with AI](../160-bulk-file-processing-with-ai/about.md)

### Required Skills & Tools

- VS Code with GitHub Copilot (Agent Mode enabled)
- Access to a Git repository with completed issues and commits
- Basic understanding of diffs and commit history
- Python 3.10+ installed (for bulk extraction script in Step 7)

## When to Use

- You joined a new project with no documentation or stale documentation
- You want to understand how the team actually works (not how they say they work)
- You need to create onboarding instructions but no one has time to write them
- You want to extract coding conventions from real code changes, not guess at them
- You are preparing an instruction file and need grounded evidence of actual practices
