# Kata — Building Calculation Skills

**Duration:** 20-30 minutes

**Skill:** Practice the full skill-creation loop — describe a calculation, let the agent generate a deterministic Python CLI script, write a SKILL.md, run and verify output, then repeat with a new calculation theme.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- The kata mindset for AI-assisted development: short loops, repetition, and fast feedback
- Full skill-creation loop: describe → generate script → write SKILL.md → run → verify
- Deterministic vs. generative computation and when to use each
- Python stdlib for calculations: `math`, `statistics`, `decimal`, `fractions`, `itertools`
- CLI interface conventions: `argparse`, `--output`, `--format md|json|csv`
- Packaging scripts and `SKILL.md` together as reusable AI skills

## Learning Outcome

You can complete at least two full kata rounds in one session, each producing a reusable skill folder with a working deterministic Python CLI script and a complete `SKILL.md`, and you can start a new calculation skill from scratch in under 10 minutes.

## Prerequisites

### Required Modules

- [090 — AI Skills - Context, Tools & Memory](../090-ai-skills-tools-creation/about.md)
- [104 — Port Existing Code into Skills](../104-port-to-skills/about.md)
- [091 — CLI Snapshot Testing with Docker](../091-cli-testing/about.md) *(optional — not required to start; recommended after completing at least one round)*

### Required Skills & Tools

- Python 3.9+ available on PATH
- Terminal access (PowerShell on Windows or Bash/Zsh on macOS/Linux)
- VS Code, Cursor, or another IDE with Agent Mode
- Git configured locally (optional, for commit step after each round)

## When to Use

- You already understand what a skill is and now want speed and consistency creating new ones
- You need deterministic helpers for repeated calculations in delivery, QA, or analysis workflows
- You want a repeatable "prompt → script → docs → verify" routine your team can reuse
