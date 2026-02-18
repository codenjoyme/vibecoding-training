# Main Instruction Catalog

This file serves as a catalog of all project instructions. Each instruction covers a specific SDLC workflow or development practice.

## ⚠️ LANGUAGE RULES (CRITICAL)

- **Respond to the user in their language.** If they write in non-English — answer in the same language. If in English — answer in English.
- **All project content must be written in English only** — this includes:
  + Module files (`about.md`, `walkthrough.md`)
  + Instruction files (`*.agent.md`)
  + Code, scripts, comments in code
  + Commit messages
  + Any text that goes into project files
- **If the user provides input in a non-English language** (e.g. describes a feature in non-English, gives feedback in non-English) — **translate it to English** before writing into any project file.
- The chat conversation language ≠ the project content language. Keep them separate.

## ⚠️ CRITICAL: When User Wants Training

**If user requests to:**
- Start training / пройти тренинг / начать обучение
- Continue training / продолжить модуль
- Go through any module / пройти модуль

**YOU MUST:**
1. **IMMEDIATELY load** `training-mode.agent.md` file
2. Follow ALL instructions from that file
3. Do NOT proceed without reading training-mode.agent.md first

**Why:** The training-mode.agent.md contains complete step-by-step methodology for conducting training sessions, progress tracking, and skill verification.

## Available Instructions

- `training-mode.agent.md` - **[LOAD THIS FOR ANY TRAINING REQUEST]** Guide users through training modules step-by-step, track progress, ensure skill formation with laconic communication style.
- `creating-instructions.agent.md` - Guidelines for creating, organizing, and maintaining instruction files across different IDE platforms (VSCode/Cursor).
- `create-training-module.agent.md` - Instructions for creating new training modules with proper structure, numbering, and integration into the course plan.
- `connect-course-to-github.agent.md` - Connect local course folder (downloaded as ZIP) to GitHub repository for automatic updates while preserving work folder.
- `github-copilot-cli-installation.agent.md` - Step-by-step guide for installing and configuring GitHub Copilot CLI on Windows, including nvm-windows setup and troubleshooting common issues.
- `git-workflow.agent.md` - Comprehensive Git workflow guide for AI-assisted development with baby steps methodology, installation instructions, .gitignore setup, and best practices.
- `export-chat-session.agent.md` - Export, list, and search GitHub Copilot chat sessions from VS Code using standalone Python script with HTML/JSON/text output formats.
