# Demo Skills Repository

This folder contains **pre-built skill files** for the walkthrough — it is a **read-only reference**. Do not modify or work directly in this folder.

The setup script copies the content to `work/076-task/skills-repo/` and initializes it as a real Git repository. All interactive work (Parts 1–6 of the walkthrough) happens in `work/076-task/`.

## Contents

- `skills-repo/` — skill content ready to be copied (no `.git` folder)
  - `.manifest/` — group and sub-config JSON files
  - `code-review-base/`, `security-guidelines/`, `style-guidelines/`, `test-writing/` — project-specific skills
  - `creating-instructions/`, `iterative-prompting/` — global skills

## Quick Start

Run from the **workspace root** (`vibecoding-for-managers/`):

```powershell
# Windows
.\modules\076-skills-management-system\demo\setup.ps1
```

```bash
# macOS/Linux
bash modules/076-skills-management-system/demo/setup.sh
```

The script creates `work/076-task/skills-repo/` as a git-initialized repository, then prints next steps for running `skills init`.
