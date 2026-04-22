# 🚀 Quick Start

## Prerequisites

- **Model:** Use **Claude Sonnet 4.6** (or newer) as your AI model. Select it in the model picker of your AI Chat panel.
- **Mode:** Make sure you are in **Agent Mode** (not Edit or Ask mode). Agent Mode allows the AI to read files, run commands, and make changes autonomously.

## Starting from scratch (no IDE installed)

1. Complete **one** of the first two modules manually — they guide you through installation:
   - [Installing VSCode + GitHub Copilot](modules/010-installing-vscode-github-copilot/walkthrough.md) — recommended for most users
   - [Installing Cursor](modules/020-installing-cursor/walkthrough.md) — alternative AI-native IDE
2. At the end of the module, you'll find a link — paste it into the AI Chat in your IDE
3. From that point on, the AI agent conducts the entire training for you 🤖

## Already have an IDE with AI assistant?

If you already have VS Code + Copilot, Cursor, or another AI-enabled IDE installed, skip the installation modules.

Paste this link directly into your AI Chat (Copilot Chat, Cursor Chat, etc.):

```
https://github.com/codenjoyme/vibecoding-training/blob/main/modules/025-downloading-course-materials/walkthrough.md
```

The agent will download the course repository, set everything up, and start guiding you through the modules — fully automatically.

> ⚠️ **Note:** After downloading, the agent will try to reopen your IDE in the course folder (`c:/workspace/hello-genai/`). If it doesn't switch automatically, open the folder manually: **File → Open Folder** → navigate to `c:/workspace/hello-genai/`. Then open a new AI Chat and type "Let's start training" — the agent will detect that the course is already set up and continue from the right place.

## Already have an IDE with AI assistant and Git?

If you have Git installed and are comfortable with the command line, this is the fastest path:

1. Clone the repository to your preferred location:
   ```
   git clone https://github.com/codenjoyme/vibecoding-training.git c:/workspace/hello-genai
   ```
   > On macOS/Linux use `~/workspace/hello-genai` instead.
2. Open a **new empty workspace** in your IDE: **File → Open Folder** → select `c:/workspace/hello-genai`
3. Open AI Chat (Copilot Chat, Cursor Chat, etc.) and type:
   ```
   Let's start training
   ```
4. The agent will detect the course materials and start guiding you through the modules 🤖
