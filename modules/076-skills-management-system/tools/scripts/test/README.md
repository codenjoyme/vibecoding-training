# Skills CLI (Go) — Smoke Test Framework

## Concept

The smoke test runs inside a Docker container (clean Linux),
executes **all** CLI commands from scratch, and writes the output
back into the same `commands.md` file — right under each command.

After the run you check `git diff test/commands.md`:
- **diff is empty** → nothing changed, behavior is stable.
- **diff exists** → inspect what changed, fix or commit.

The file is committed to the repository — it serves as a "golden snapshot" of CLI behavior.

---

## Quick Start

### 1. Build the image

```bash
cd modules/076-skills-management-system/tools
docker build -t skills-go-smoke -f scripts/test/Dockerfile .
```

### 2. Run the test

```bash
docker run --rm -v ./scripts/test:/app/test skills-go-smoke
```

Output is written directly into `scripts/test/commands.md`.

### 3. Check the result

```bash
git diff scripts/test/commands.md
```

If everything is fine:

```bash
git add scripts/test/commands.md
git commit -m "smoke: update golden snapshot (go)"
```
