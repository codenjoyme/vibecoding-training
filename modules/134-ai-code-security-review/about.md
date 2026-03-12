# AI Code Security Review

**Duration:** 15 minutes

**Skill:** Use AI as a security reviewer to find and fix the most common vulnerabilities in AI-generated code — from hardcoded secrets to injection risks and insecure defaults.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- The OWASP Top 10 vulnerabilities that AI commonly generates
- Using AI to do a structured security review of existing code
- Building a reusable security review instruction file
- Detecting and removing secrets from code and Git history
- Setting up `.env` + `.gitignore` as the first line of security defence

## Learning Outcome

You can apply an AI-assisted security review to any codebase, identify the most common vulnerability classes in AI-generated code, and set up a repeatable security review process using a custom instruction.

## Prerequisites

### Required Modules

- [070 — Custom Instructions](../070-custom-instructions/about.md)
- [110 — Development Environment Setup](../110-development-environment-setup/about.md)
- [132 — AI-Assisted Test Generation & Snapshot Testing](../132-ai-assisted-test-generation/about.md)

### Required Skills & Tools

- A working PoC or project with AI-generated code to review
- Git repository (for secret scanning and history inspection)
- Basic understanding of what an API key is and how it's used
