# Demo Skills Repository

This folder contains a pre-built skills repository for the walkthrough.

Use it to skip hand-writing all SKILL.md content and jump straight to CLI practice.

## Contents

- `skills-repo/` — Central skills Git repository (ready to initialize)
  - `.manifest/` — Group and sub-config JSON files
  - `code-review-base/`, `security-guidelines/`, `style-guidelines/`, `test-writing/` — Project-specific skills
  - `creating-instructions/`, `iterative-prompting/` — Global skills

## Quick Start

1. Run the setup script to initialize `skills-repo` as a Git repository:

   ```powershell
   # Windows
   .\setup.ps1
   ```

   ```bash
   # macOS/Linux
   chmod +x ./setup.sh && ./setup.sh
   ```

2. Create project workspaces pointing to the demo repo:

   ```bash
   # From this demo/ folder
   mkdir project-alpha
   cd project-alpha
   skills init --repo ../demo/skills-repo --groups project-alpha
   ```

The setup script only needs to be run once. After that, use `skills pull`, `skills push`, and `skills list` as shown in the walkthrough.
