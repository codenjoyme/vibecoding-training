# Module 06 Completion Report

## Token Generation
An AI model generates text one token at a time by predicting the most likely next word based on all the text it has seen so far. Each new token is appended and the process repeats until the response is complete.

## Temperature Effect
Temperature is a randomness parameter that causes the model to select slightly different tokens each time, even for the same prompt. This is why two identical prompts produce responses that convey the same meaning but use different wording.

## Four Players in Agent Mode
1. User: The person who types prompts, reviews responses, and makes decisions.
2. AI Model: The language model (e.g. Claude Sonnet) that generates text token by token on the shared context.
3. Agent System: The orchestrator built into the IDE that coordinates the model, tools, and user interaction.
4. Tools: Functions that can read files, edit code, run terminal commands, and search the codebase on behalf of the agent.

## Context Window
The context window is the total text the AI model can see at any moment — it includes not just the visible chat messages but also hidden system prompts, agent behavioral rules, tool descriptions, and previous tool call results. This means the model operates on much more information than what appears in the user-facing chat panel.

## Tool Example
- Tool: read_file
- What it does: Reads the contents of a file in the workspace so the AI can understand existing code or documents before making changes.
