# Iterative Prompting — SKILL.md

## Purpose
This skill defines the iterative prompt workflow — maintaining a `main.prompt.md` file
as a living specification that grows with your project rather than losing context in chat.

## Core Workflow
- Keep a `main.prompt.md` file in your request folder (version-controlled)
- Add each new request as a new `## UPD[N]` block at the bottom
- After the AI acts, it appends a `### RESULT` block with a brief changelog
- Use `git diff` to give the AI precise context about what changed since last run

## Key Benefits
- No context drift — the file is the full history
- `git diff` replaces "here's what changed since last time"
- Works with any AI agent (Copilot, Cursor, Claude Code, CLI)
- Self-documenting: file is both spec and breadcrumb trail

## When to Use
Use iterative prompting for any multi-step task where you need to:
- Maintain context across multiple AI interactions
- Track what was done and what's still pending
- Reproduce the exact sequence of changes later
