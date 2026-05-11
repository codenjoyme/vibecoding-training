# 🚀 Quick Start

> **Recommended starting point:** [base-course.md](base-course.md) — a curated list of modules for onboarding with AI-assisted development.

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
Please follow instruction `https://github.com/codenjoyme/vibecoding-training/blob/main/quickstart.md`
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
   Let's start training on `base-course.md`
   ```
4. The agent will detect the course materials and start guiding you through the modules 🤖 The agent talks to you directly in the chat window — one question, one answer, one module at a time.

### Iterative prompt mode (saves tokens, keeps full log)

Type in the AI Chat:

```
Let's start training in `iterative prompt` mode based on `base-course.md`
```

In this mode the agent creates a `main.prompt.md` file and all training happens inside that file — not in the chat. You write `## UPD` blocks, the agent writes `### RESULT` blocks. The file stays in git — your full training history.

**Why use this mode:**
- Saves premium requests (the agent sleeps between your updates at zero cost)
- Full conversation history preserved in version control
- You work at your own pace — write an update, append `go`, the agent picks it up
