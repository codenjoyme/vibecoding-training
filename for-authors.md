# 🎓 For Authors: Creating Training Content

## Prerequisites

- **Model:** Use **Claude Sonnet 4.6** (or newer) as your AI model. Select it in the model picker of your AI Chat panel.
- **Mode:** Make sure you are in **Agent Mode** (not Edit or Ask mode). Agent Mode allows the AI to read files, run commands, and make changes autonomously.

## Getting Started with Content Creation

This guide is for authors and contributors who want to create or modify training modules and instructions for this course.

## Essential Resources

### 1. **Example Requests**
Browse the [`requests/`](./requests) folder — it contains real examples of how modules and other content are created using the iterative prompt approach. This is your best learning resource for understanding the practical workflow.

### 2. **Iterative Prompt Approach**
The [`instructions/iterative-prompt.agent.md`](./instructions/iterative-prompt.agent.md) instruction explains how the iterative prompt workflow works. This is the recommended approach for creating content in this repository.

### 3. **Creating Training Modules**
When you ask the AI to create a new training module, it uses the [`instructions/create-training-module.agent.md`](./instructions/create-training-module.agent.md) instruction. Review this file to understand the module structure, naming conventions, and content requirements.

### 4. **Conducting Training**
When you ask the AI to conduct training or walk through a module, it uses the [`instructions/training-mode.agent.md`](./instructions/training-mode.agent.md) instruction.
- **Optional:** If you want to save tokens during training, use [`instructions/training-mode-iterative-prompt.agent.md`](./instructions/training-mode-iterative-prompt.agent.md) which enables training in iterative prompt mode.

### 5. **Instruction Architecture**
The [`instructions/creating-instructions.agent.md`](./instructions/creating-instructions.agent.md) file describes the architecture through which agents discover and access instructions across different IDEs:
- **GitHub Copilot** → [`.github/copilot-instructions.md`](./.github/copilot-instructions.md)
- **Claude Code** → [`CLAUDE.md`](./CLAUDE.md)
- **Cursor** → [`.cursor/rules/core-instructions.mdc`](./.cursor/rules/core-instructions.mdc)
- **Other IDEs** → [`AGENT.md`](./AGENT.md)

All paths lead to [`instructions/main.agent.md`](./instructions/main.agent.md), which serves as the central catalog linking to all instruction files in the [`instructions/`](./instructions) folder.

## Workflow Tips

1. **Start small:** Begin by exploring existing modules in the `modules/` folder to understand the structure and style.
2. **Use examples:** Reference the `requests/` folder for concrete examples of module creation workflows.
3. **Follow conventions:** Stick to established naming patterns, file structures, and writing style.
4. **Test your content:** Always walk through your modules as if you were a student to ensure clarity and completeness.
5. **Iterate:** Use the iterative prompt approach to refine content based on feedback and testing.

## Common Tasks

- **To create a new module:** Ask the AI to "create a training module about [topic]" — it will follow the structure defined in `create-training-module.agent.md`.
- **To update an existing module:** Use the iterative prompt approach documented in the `requests/` folder examples.
- **To test a module:** Ask the AI to "start training" or "walk through module [number]" — it will use `training-mode.agent.md`.
- **To create a new instruction:** Follow the guidelines in `creating-instructions.agent.md` for proper file placement and naming.

## Questions or Issues?

If you encounter issues or have questions about the authoring workflow, check the relevant instruction files or review similar examples in the `requests/` folder.
