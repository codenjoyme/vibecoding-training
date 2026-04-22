# Base Course Recommendations

A curated list of modules recommended for onboarding and skill formation with AI-assisted development.

## Recommended Modules

| Module | Level | Tags | Description |
|--------|-------|------|-------------|
| [030-model-selection](modules/030-model-selection/) | base | important | Choose the right model — results depend on this heavily. Short answer: Claude Sonnet 4.6 |
| [035-visual-context-screenshots](modules/035-visual-context-screenshots/) | base | | Not just text — images can also be part of your context |
| [040-agent-mode-under-the-hood](modules/040-agent-mode-under-the-hood/) | base | important | How the agent works under the hood — removes the magic |
| [050-effective-prompting-without-arguing](modules/050-effective-prompting-without-arguing/) | base | important | Don't argue with models — they hallucinate more under pressure. Explore alternatives to arguing |
| [055-clarifying-requirements-before-start](modules/055-clarifying-requirements-before-start/) | base | important | How to fill the context before starting — switching the agent into interview mode |
| [057-agent-memory-management](modules/057-agent-memory-management/) | base | | Offload any memory to markdown files — makes the model less forgetful |
| [058-workspace-kickoff-prompt-files](modules/058-workspace-kickoff-prompt-files/) | base | optional | How to run experiments on any text data: "here are the files, figure it out and tell me… do this for me…" |
| [060-version-control-git](modules/060-version-control-git/) | base | important | Baby steps approach — critical when working with models that can break what was just done well |
| [070-custom-instructions](modules/070-custom-instructions/) | base | important | **FOUNDATION:** Create instructions for any purpose. The base instruction for creating instructions — start every GenAI project here |
| [080-learning-from-hallucinations](modules/080-learning-from-hallucinations/) | base | important | **FOUNDATION:** Don't edit instructions manually. When a hallucination occurs, ask the agent to fix the instruction so it won't happen again. A good instruction takes 10–15–20 iterations |
| [090-ai-skills-tools-creation](modules/090-ai-skills-tools-creation/) | base | important | **FOUNDATION:** The model can't do everything well — move part of the logic into a deterministic script, add an instruction, and get a Skill. Code is written by the model itself |
| [100-mcp-model-context-protocol](modules/100-mcp-model-context-protocol/) | base | important | A way to connect to 3rd-party systems |
| [103-cli-command-line-interface](modules/103-cli-command-line-interface/) | base | important | Another way to connect to 3rd-party systems |
| [110-development-environment-setup](modules/110-development-environment-setup/) | advanced | | For building your own PoC on Node.js — SpecKit can be wired up to it for rapid prototyping |
| [120-rapid-poc-prototyping-with-speckit](modules/120-rapid-poc-prototyping-with-speckit/) | advanced | | Spec-driven development framework — features are built better and the agent works autonomously longer |
| [130-chrome-devtools-mcp-qa-emulation](modules/130-chrome-devtools-mcp-qa-emulation/) | advanced | | For web applications — how to automate QA in the browser |
| [160-bulk-file-processing-with-ai](modules/160-bulk-file-processing-with-ai/) | advanced | | When processing many files, write a script and work with the agent in CLI mode |
| [196-reverse-engineering-project-knowledge](modules/196-reverse-engineering-project-knowledge/) | advanced | | When you have a project and need to extract instructions from its commit history |

## Legend

| Tag | Meaning |
|-----|---------|
| `base` | Core content for the first 2-hour sessions to get everyone aligned |
| `important` | Essential — this is the essence of GenAI-assisted development |
| `advanced` | Additional content after the base; the repo also has dozens more modules on similar topics |
| `optional` | Useful but not required for the core path |
