# CLI Snapshot Testing Skill

A universal, OS-agnostic CLI snapshot testing framework inspired by the [Approval Tests](https://approvaltests.com/) approach. Instead of writing individual unit tests with assertions, you capture the full CLI output as a "golden snapshot" — a Markdown document that serves as both the test script and the expected result.

## Concept: Approval-Style Snapshot Testing

The original [Approval Tests](https://approvaltests.com/) idea by Llewellyn Falco: instead of writing assertions one by one, you run the system, capture its full output, and approve it as the "truth." On re-run, any difference from the approved output signals a potential regression.

**This skill extends the concept with three innovations:**

1. **No automated assertion** — the output is saved as a Markdown snapshot file. You (or an LLM reviewing `git diff`) decide whether the diff is acceptable. In the LLM era, the model can look at the snapshot + recent `git diff` and diagnose what went wrong — far more effectively than reading assertion failures.

2. **Markdown-based scenario format** — the test scenario is a readable Markdown document. It contains descriptions of *why* each command matters, interleaved with the commands themselves and their captured output. First run fills in the output blocks; subsequent runs update them. You commit the file as the golden truth.

3. **OS-agnostic via Docker** — everything runs inside a Docker container, so the test environment is identical regardless of whether you're on Windows, macOS, or Linux. Output is normalized (Windows `\r\n` → Unix `\n`).

## File Structure

```
cli-test-runner/
├── SKILL.md              ← this file (instructions)
├── run-scenarios.sh      ← universal bash runner (read-only, do not modify)
├── run-scenarios.ps1     ← PowerShell port for Windows (same features)
└── demo/                 ← usage examples
    ├── node-cli/         ← example: testing a Node.js CLI tool
    │   ├── setup.sh      ← custom setup script (installs cowsay)
    │   └── scenarios/
    │       └── basic-commands.md
    └── python-cli/       ← example: testing a Python CLI tool
        ├── setup.sh
        └── scenarios/
            └── basic-commands.md
```

No per-demo Dockerfiles needed — the runner generates one on the fly using `--base-image`.

## How to Use This Skill

### Step 1: Create Your Project Test Structure

In your project, create a test folder with this layout:

```
your-project/
├── test/
│   ├── setup.sh              ← your custom setup script
│   └── scenarios/
│       ├── smoke-test.md      ← scenario file 1
│       ├── edge-cases.md      ← scenario file 2
│       └── regression.md      ← scenario file 3
```

No Dockerfile needed — the runner generates one automatically. If you need full control, place a custom `Dockerfile` in the test dir and it will be used instead.

### Step 2: Write a Setup Script

The `setup.sh` is where you install and configure your CLI tool. This runs during `docker build`:

```bash
#!/usr/bin/env bash
# setup.sh — Install and configure your CLI tool
set -e

# Example: install a Node.js CLI (use --base-image node:20-slim)
npm install -g your-cli-tool

# Example: install a Python CLI (use --base-image python:3.12-slim)
# pip install your-cli-tool

# Example: build from source
# cd /app/source && make install
```

Choose a `--base-image` that matches your tool's runtime (e.g., `node:20-slim` for npm-based CLIs, `python:3.12-slim` for pip-based CLIs, `ubuntu:22.04` as a general default).

### Step 3: Write Scenario Files

Scenario files are Markdown documents. The format:

```markdown
# My CLI — Smoke Test

## Phase 1: Basic Commands

This tests the basic help output.

> `my-cli --help`

This verifies version display.

> `my-cli --version`

## Phase 2: Core Functionality

Create a new project and list contents.

> `cd /workspace`
> `my-cli init my-project`
> `ls -la my-project/`
```

**Rules:**
- Lines matching `` > `command` `` are extracted and executed
- Everything else (headings, descriptions, blank lines) is passed through unchanged
- `cd` commands update the working directory for subsequent commands
- Output is inserted as a fenced code block (`` ``` ``) after each command
- On re-run, old output blocks are replaced — descriptions stay intact
- Backticks in output are replaced with single quotes to avoid breaking fences

### Step 4: Run the Tests

Everything is driven by one script. Choose your shell:

**Bash (Linux / macOS / Git Bash on Windows):**

```bash
# Run all scenarios (default base: ubuntu:22.04)
bash path/to/run-scenarios.sh --test-dir ./test

# Specify a base image for your CLI
bash path/to/run-scenarios.sh --test-dir ./test --base-image node:20-slim

# Run specific scenarios by glob pattern
bash path/to/run-scenarios.sh --test-dir ./test --base-image python:3.12-slim --pattern "smoke*"

# Custom Docker image name
bash path/to/run-scenarios.sh --test-dir ./test --base-image node:20-slim --image-name my-cli-test
```

**PowerShell (Windows):**

```powershell
# Run all scenarios (default base: ubuntu:22.04)
& path/to/run-scenarios.ps1 -TestDir ./test

# Specify a base image for your CLI
& path/to/run-scenarios.ps1 -TestDir ./test -BaseImage node:20-slim

# Run specific scenarios by glob pattern
& path/to/run-scenarios.ps1 -TestDir ./test -BaseImage python:3.12-slim -Pattern "smoke*"

# Custom Docker image name
& path/to/run-scenarios.ps1 -TestDir ./test -BaseImage node:20-slim -ImageName my-cli-test
```

Both scripts do the same thing. Docker Desktop is required on all platforms.

**What happens under the hood:**
1. A temporary build context is created with your `setup.sh` + the runner script
2. A Dockerfile is generated on the fly using `--base-image` / `-BaseImage` (or your custom `Dockerfile` if one exists in the test dir)
3. Docker builds the image and installs your CLI via `setup.sh`
4. Container runs with `scenarios/` mounted as a volume — output writes back to host
5. Temporary build context is cleaned up

### Step 5: Review and Commit

```bash
# Check what changed
git diff test/scenarios/

# If the output looks correct, commit as the new golden snapshot
git add test/scenarios/
git commit -m "test: update golden snapshots"
```

## Runner Flags

**Bash (`run-scenarios.sh`):**

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--test-dir` | `-d` | `.` | Path to test directory containing `setup.sh` and `scenarios/` |
| `--base-image` | `-b` | `ubuntu:22.04` | Docker base image (e.g., `node:20-slim`, `python:3.12-slim`) |
| `--pattern` | `-p` | `*.md` | Glob pattern for scenario files to run |
| `--image-name` | `-i` | `cli-snapshot-test` | Docker image name to use |
| `--no-build` | `-n` | (off) | Skip Docker build, use existing image |
| `--local` | `-l` | (off) | Run locally without Docker (requires bash) |

**PowerShell (`run-scenarios.ps1`):**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-TestDir` | `.` | Path to test directory containing `setup.sh` and `scenarios/` |
| `-BaseImage` | `ubuntu:22.04` | Docker base image (e.g., `node:20-slim`, `python:3.12-slim`) |
| `-Pattern` | `*.md` | Glob pattern for scenario files to run |
| `-ImageName` | `cli-snapshot-test` | Docker image name to use |
| `-NoBuild` | (off) | Skip Docker build, use existing image |
| `-Local` | (off) | Run locally without Docker (requires bash) |

## Workflow with LLM Review

The killer feature: after running snapshots, use `git diff` + an LLM to automatically diagnose regressions.

```
1. You make code changes to your CLI
2. Run snapshot tests → scenarios get updated output
3. git diff test/scenarios/ shows exactly what changed
4. Feed the diff to an LLM: "Here's what changed in my CLI output after my recent code changes. Is this expected?"
5. The LLM can cross-reference the diff against your code changes and tell you if it's a regression or expected behavior change
```

This is dramatically more effective than reading assertion failure messages, because the LLM sees the *full context* of before/after output.

## Tips

- **Keep scenario files focused** — one file per feature area or test phase
- **Use descriptive text** between commands to document *why* each test matters
- **Commit after every green run** — the snapshot file *is* your test record
- **Git hashes and timestamps will change** every run — that's expected, verify structure and behavior
- **Use `cd` commands** to manage working directory within a scenario
- **Multiple scenario files** — organize into `scenarios/` folder, use `--pattern` to run subsets
- **Commands get `/dev/null` as stdin** — the runner redirects stdin to prevent commands from consuming the scenario file. If your CLI reads from stdin, pipe data explicitly: ``echo '{"key":"val"}' | my-cli parse``
