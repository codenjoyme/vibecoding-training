# Skills CLI — Quick Demo Journey (Node.js Edition)

A step-by-step walkthrough of the full workflow: from installation to proposing a skill change via Pull Request.

---

## Step 1 — Install the CLI

```bash
npm install -g --install-links git+https://github.com/codenjoyme/apm-lite.git
```

> Installs the `skills` command globally from a private Git repository.  
> After this, `skills` is available in any terminal session.

---

## Step 2 — Verify installation

```bash
skills help
```

> Lists all available commands. Use `skills <command> --help` for details on any command.

---

## Step 3 — Create a project folder

```bash
mkdir my-project
cd my-project
```

> This is the developer's project workspace where skills will be installed.

---

## Step 4 — Initialize the skills workspace

```bash
skills init --repo https://github.com/your-org/skills-repo --groups backend
```

> Clones the central skills repository into `instructions/`, resolves skills for the `backend` group  
> (combining `_global.json` + `backend.json` + any sub-configs), applies sparse checkout  
> so only relevant skills are checked out locally. Writes `skills.json` in the project root.

**Local path example (for testing):**

```bash
skills init --repo ../skills-repo --groups project-alpha
```

**Multiple groups:**

```bash
skills init --repo ../skills-repo --groups backend,security
```

---

## Step 5 — List available skills

```bash
skills list
```

> Shows all skills in the central repository.  
> Active skills (checked out for your groups) are marked ✅.  
> Skills not in your groups are marked ○.

**Example output:**
```
Skills repository: ../skills-repo
Groups:           project-alpha

  ✅ code-review-base
  ✅ creating-instructions
  ✅ iterative-prompting
  ✅ security-guidelines
  ✅ style-guidelines
  ○  test-writing

Active: 5  |  Total: 6
```

---

## Step 6 — Your AI agent reads the skills

```
instructions/code-review-base/SKILL.md
instructions/creating-instructions/SKILL.md
instructions/security-guidelines/SKILL.md
...
```

> No extra configuration needed. The agent scans `instructions/*/SKILL.md`  
> and loads them as context automatically.

---

## Step 7 — Update local skills

```bash
skills pull
```

> Runs `git pull` in `instructions/`. Always checks out the default branch first  
> to avoid tracking issues after a previous `push`.

---

## Step 8 — Edit a skill

```bash
# Open the skill file in your editor
code instructions/code-review-base/SKILL.md
```

> Make your improvements directly in the checked-out skill directory.  
> Changes stay local until you propose them via `skills push`.

---

## Step 9 — Propose a change via Pull Request

```bash
skills push code-review-base
```

> 1. Creates branch `feature/code-review-base-update` in `instructions/`  
> 2. Stages all changes in `instructions/code-review-base/`  
> 3. Commits with message `feat(code-review-base): update skill instructions`  
> 4. Pushes the branch to origin  
> 5. Prints a PR creation URL (GitHub/GitLab)  
> 6. Returns to the default branch automatically

**Example output:**
```
→ Creating branch feature/code-review-base-update ...
  ✓ Branch created
→ Staging and committing changes in code-review-base/ ...
  ✓ Changes committed
→ Pushing branch feature/code-review-base-update ...
  ✓ Branch pushed

✅ Skill "code-review-base" pushed for review
   Branch: feature/code-review-base-update
   Open PR: https://github.com/your-org/skills-repo/compare/feature/code-review-base-update?expand=1
```

---

## Step 10 — Pull after the PR is merged

```bash
skills pull
```

> Updates all skills with the latest merged changes from the central repository.

---

## Summary

| Command | What it does |
|---------|-------------|
| `skills help` | Show all commands |
| `skills init --repo <url> --groups <group>` | Clone repo, checkout only relevant skills |
| `skills list` | Show active ✅ and inactive ○ skills |
| `skills pull` | Get latest changes from the central repo |
| `skills push <skill-name>` | Propose a skill change via branch + PR |
