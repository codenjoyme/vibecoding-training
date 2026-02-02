## Motivation and Use Cases

- IDE-agnostic architecture allows teams to use different IDE/Plugins while sharing same instruction base.
- Team alignment on LLM model choice is more critical than IDE choice - IDE switching is less disruptive.
- Instructions are pure markdown docs describing SDLC workflows without platform-specific adaptors like `alwaysApply: true` or `mode: agent`.
- Following Single Responsibility Principle (SRP) - one SDLC workflow piece per instruction file.
- `main.agent.md` serves as catalog of all instructions with brief descriptions - when asked about (what to do), follow this instruction (with file path).
- Platform-specific entry points (`.github/copilot-instructions.md` for Copilot, different for Cursor) reference `main.agent.md` to load with every prompt.
- Extract essence from completed chat sessions into new instructions to avoid repeating same troubleshooting in future.
  + After achieving desired outcome through multiple iterations with agent, capture workflow as instruction.
  + Prevents repeating same back-and-forth when similar task appears later.
  + Instructions can be iteratively refined through future usage, triggering on potential model hallucinations.
- Common usage patterns with this instruction:
  + "Following instruction for creating instructions, create instruction based on this chat"
  + "Following instruction for creating instructions, create shortcut-links for all my instructions for Cursor"
  + "Following instruction for creating instructions, update instruction (name) with new knowledge from this chat session"
- Once general idea described in one file, can follow it with light prompt adjustments for different contexts.

## General Concepts

- If you don't know exactly which IDE (with which Agent system) is used in the project, there are always the markers described below.
- Always can create missing components when asked:
  + Make all missing prompts/rules based on existing instructions and selected IDE.
  + Create `main.agent.md` file with proper structure and links
  + Complete any missing instruction ecosystem components
- Instructions are platform-agnostic markdown files that contain pure actionable statements.
- Prompt files are platform-specific wrappers that reference instruction files using appropriate syntax.
- Instruction files contain the core logic, prompt files contain platform-specific integration.

## Instructions 

- If you are asked to create another one - please add it in this folder `./mcp_server/instructions/` as new file.
- All instructions are placed in `./mcp_server/instructions/` folder with `[name].agent.md` extension.
- Here `[name]` should consist of several words separated by a `-` symbol, the first of which is a verb, the essence of the operation being performed. 
- Use bullet points format, avoid headers and sections - keep it simple and actionable.
- Write short, concise statements - minimize words, maximize usefulness.
- Each point should be specific and actionable, not explanatory.
- Add new instruction reference to `./mcp_server/instructions/main.agent.md` with one-line description of what it covers.
- Use backticks for code examples, file paths, and commands.
- Include practical examples when necessary, but keep them minimal.
- Structure: bullet points with sub-bullets using `+` when needed.
- Avoid long explanations - focus on what to do, not why
- Look at existing files like `create-tool.agent.md`, `create-instruction.agent.md` for style reference.
- Use English for instruction content, respond in user's language.
- Test practical examples before including them.
- Keep file focused on one topic or workflow.
- Apply Single Responsibility Principle to instructions to avoid duplication.
- Extract common workflows into separate reusable instruction files.
- Reference shared instructions using `./mcp_server/instructions/[shared-name].agent.md` format.
- When updating existing instruction files:
  + Read existing file first to understand current structure and content.
  + Check which statements from new requirements already exist in the file.
  + Add new statements without rewriting the entire file using targeted edits.
  + Preserve existing useful content and build upon it incrementally.
  + Use sub-bullets with `+` for detailed practices under main points.
  + Include lessons learned from practical implementation experience.
  + Add debug and maintenance guidance for future development work.
  + Focus on actionable insights that improve workflow efficiency.

## VSCode + GitHub Copilot

- You can identify this case by `.github` folder inside your workspace.
- Add new file to the `./.github/prompts/` with name `to-[name].prompt.md` and the line we added to `main.agent.md` as reference to instruction file using platform-specific syntax as in example bellow: 
```markdown
---
mode: agent
---
- When you are asked to _______________, please follow the instructions `./mcp_server/instructions/__________.agent.md`.
```
- The file `.github/copilot-instructions.md` should contain the following:
```markdown
- Important! Always follow the instructions in `./mcp_server/instructions/main.agent.md` file.
- It contains links to other files with instructions.
- You should reload it in **every prompt** to get the latest instructions - because of the dynamic nature of the project. 
```
- The settings file `.vscode/settings.json` should contain:
  + Enable instruction and MCP files usage:
  ```
    "github.copilot.chat.codeGeneration.useInstructionFiles": true,
    "chat.mcp.access": "all",
    "chat.agent.maxRequests": 250
  ```
  + [Optionally] Ask user to enable auto-save for better experience:
  ```
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 100,
  ```

## Cursor

- You can identify this case by `.cursor` folder inside your workspace.

- You can identify this case by `.cursor` folder inside your workspace.
- Add new file to the `./.cursor/rules/` with name `to-[name].mdc` and reference to instruction file using Cursor-specific syntax:
```markdown
---
description: Brief description of when to use this instruction
globs:
alwaysApply: true
---

Follow the instructions in `./mcp_server/instructions/to-[name].agent.md` when you are asked to _______________.
```
- The main rules file `.cursor/rules/mcpyrex.mdc` should contain the following:
```markdown
---
description: Main instruction orchestrator for the project
globs:
alwaysApply: true
---

- Important! Always follow the instructions in `./mcp_server/instructions/main.agent.md` file.
- It contains links to other files with instructions.
- You should reload it in **every prompt** to get the latest instructions - because of the dynamic nature of the project.
```