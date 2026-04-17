# Skills CLI — Smoke Test Framework

## Concept

The smoke test runs inside a Docker container (clean Linux),
executes **all** CLI commands from scratch, and writes the output
back into the same `commands.md` file — right under each command.

After the run you check `git diff test/commands.md`:
- **diff is empty** → nothing changed, behavior is stable.
- **diff exists** → inspect what changed, fix or commit.

The file is committed to the repository — it serves as a "golden snapshot" of CLI behavior.

---

## Structure

```
test/
├── README.md          ← you are here
├── commands.md        ← commands + output (source AND result)
├── run-tests.sh       ← bash runner: executes commands, writes output back
└── Dockerfile         ← clean Linux container with Node.js + git
```

---

## Quick Start

### 1. Build the image

```bash
cd apm-lite
docker build -t skills-smoke -f test/Dockerfile .
```

### 2. Run the test

```bash
docker run --rm -v ./test:/app/test skills-smoke
```

Output is written directly into `test/commands.md`.

### 3. Check the result

```bash
git diff test/commands.md
```

If everything is fine:

```bash
git add test/commands.md
git commit -m "smoke: update golden snapshot"
```

---

## How It Works

`commands.md` is a Markdown file with this format:

```markdown
Some description of what we're doing

> `skills init --repo ../project-repo --groups group-1`
\```
output appears here after running
\```

> `skills list`
\```
output appears here
\```

More description text (ignored by the runner)
```

The runner (`run-tests.sh`):
1. Reads `commands.md` line by line
2. Lines matching `` > `command` `` are extracted and executed
3. Output (stdout + stderr) is inserted as a fenced code block after each command
4. Old output blocks are replaced on re-run
5. All other text (headings, descriptions) is passed through unchanged
6. `cd` commands update the working directory for subsequent commands

---

## Adding a New Test

Just add a command line to `commands.md`:

```markdown
> `skills create my-new-skill`
> `skills list`
```

Run the container, check the diff, commit.

---

## Shortcuts

Build + run in one line:

```bash
docker build -t skills-smoke -f test/Dockerfile . && docker run --rm -v ./test:/app/test skills-smoke
```

Build + run + diff:

```bash
docker build -t skills-smoke -f test/Dockerfile . && docker run --rm -v ./test:/app/test skills-smoke && git diff test/commands.md
```

Build + run + commit if OK:

```bash
docker build -t skills-smoke -f test/Dockerfile . && docker run --rm -v ./test:/app/test skills-smoke && git add test/commands.md && git commit -m "smoke: update golden snapshot"
```

PowerShell (Windows):

```powershell
docker build -t skills-smoke -f test/Dockerfile .
docker run --rm -v "${PWD}/test:/app/test" skills-smoke
git diff test/commands.md
```

---

## FAQ

**Q: Why Docker?**
A: Clean environment. No artifacts from previous runs,
no dependencies on the host OS.

**Q: Can I run without Docker?**
A: Yes, but on Linux. Just run `bash test/run-tests.sh`.
Make sure `node`, `npm`, and `git` are installed and the CLI is built.

**Q: How do I validate results?**
A: `git diff test/commands.md`. You (or an LLM) review the diff.
If it looks correct, commit. If not, investigate and fix.

**Q: Output has git hashes and timestamps — won't the diff always change?**
A: Yes, git hashes and timing values change every run.
That's expected — just verify the structure and behavior are correct, then commit the new snapshot.

**Q: How does re-run work?**
A: The runner replaces old `` ``` `` output blocks in-place. Descriptions,
headings, and command lines stay untouched. Only the content between
fences gets overwritten.
