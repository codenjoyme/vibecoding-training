# Creating Instructions — SKILL.md

## Purpose
This skill defines how to create, organize, and maintain AI instruction files.

## Core Principles
- IDE-agnostic: instructions are plain Markdown in a dedicated folder
- Single Responsibility: one SDLC workflow piece per instruction file
- Tools-agnostic: works with VSCode Copilot, Cursor, Claude Code, and any LLM agent
- Composable: instructions can reference each other; no monoliths

## How to Create an Instruction
1. Identify the SDLC workflow to capture
2. Create `<name>.agent.md` in `instructions/`
3. Register it in `main.agent.md` catalog with a short description and keywords
4. Add thin IDE adapter wrappers (`.github/prompts/`, `.cursor/rules/`) pointing to the file

## IDE Adapter Wrappers
- VSCode Copilot: `.github/prompts/<name>.prompt.md` referencing `../../instructions/<name>.agent.md`
- Cursor: `.cursor/rules/<name>.mdc` with `globs: ""` and content referencing the instruction file
- Claude Code: `.claude/commands/<name>.md` calling the instruction file

## When to Split a File
Split when a single file exceeds ~700 lines or covers more than one logical workflow.
