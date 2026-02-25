# Port Existing Code into Skills

**Duration:** 15-20 minutes  
**Skill:** Port an existing backend service into a portable CLI tool and package it as a reusable AI Skill — using the original code as the specification, with no prompt engineering required

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Using existing code as a specification (better than text descriptions)
- Why LLMs read code better than natural language requirements
- Porting familiar Java service logic (`echo`, `get_time`, `calculate`) to a cross-platform Python CLI
- Writing the instruction file — the "manual for your LLM"
- Packaging instruction + tool as a reusable Skill following AgentSkills.io principles
- Comparing MCP vs REST vs CLI Skill — three forms of the same three tools
- When porting is faster than building from scratch

## Learning Outcome

Port a Java Spring service (the same `echo`, `get_time`, `calculate` tools from modules 100 and 103) into a standalone Python CLI tool packaged as an AI Skill — without running or compiling the original code. Understand why three forms of the same tools (MCP, REST, CLI Skill) exist and when to choose each.

## Prerequisites

### Required Modules

- [090 — AI Skills & Tools Creation](../090-ai-skills-tools-creation/about.md)
- [103 — CLI: Command Line Interface](../103-cli-command-line-interface/about.md)

### Required Skills & Tools

- Basic familiarity with running Python scripts from terminal

## When to Use

- You have existing backend code and need a standalone CLI version
- Building automation or reporting scripts based on production service logic
- Turning internal team tools into AI-accessible, shareable Skills
- Creating audit-friendly, deterministic alternatives to LLM calculations
- Any time you want to avoid re-explaining requirements to AI — let the code speak
