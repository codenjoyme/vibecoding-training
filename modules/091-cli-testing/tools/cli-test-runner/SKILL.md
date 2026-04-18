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
├── run-scenarios.ps1     ← PowerShell wrapper for Windows users
└── demo/                 ← usage examples and demos
    ├── node-cli/         ← example: testing a Node.js CLI tool
    │   ├── setup.sh      ← custom setup script (installs Node CLI)
    │   ├── Dockerfile    ← custom Dockerfile
    │   └── scenarios/
    │       └── basic-commands.md
    └── python-cli/       ← example: testing a Python CLI tool
        ├── setup.sh
        ├── Dockerfile
        └── scenarios/
            └── basic-commands.md
```

## How to Use This Skill

### Step 1: Create Your Project Test Structure

In your project, create a test folder with this layout:

```
your-project/
├── test/
│   ├── setup.sh              ← your custom setup script
│   ├── Dockerfile             ← your custom Dockerfile
│   └── scenarios/
│       ├── smoke-test.md      ← scenario file 1
│       ├── edge-cases.md      ← scenario file 2
│       └── regression.md      ← scenario file 3
```

### Step 2: Write Your Dockerfile

The Dockerfile sets up the environment for your CLI tool. It must:
- Install your CLI tool and its dependencies
- Copy the runner script and scenario files
- Set the entrypoint to use the runner

**Template:**

```dockerfile
FROM ubuntu:22.04

# Install your CLI dependencies
RUN apt-get update && apt-get install -y <your-dependencies> && rm -rf /var/lib/apt/lists/*

# Copy setup script and run it
COPY setup.sh /app/setup.sh
RUN chmod +x /app/setup.sh && /app/setup.sh

# Copy the universal runner script
COPY run-scenarios.sh /app/run-scenarios.sh
RUN chmod +x /app/run-scenarios.sh

# Copy scenario files
COPY scenarios/ /app/scenarios/

# Prepare workspace
RUN mkdir -p /workspace

ENTRYPOINT ["bash", "-c", "sed 's/\\r$//' /app/run-scenarios.sh > /tmp/run.sh && bash /tmp/run.sh \"$@\"", "--"]
```

You can use any base image: `ubuntu:22.04`, `node:20-slim`, `python:3.12-slim`, `alpine:3.19`, etc.

### Step 3: Write a Setup Script

The `setup.sh` is where you install and configure your CLI tool:

```bash
#!/usr/bin/env bash
# setup.sh — Install and configure your CLI tool
set -e

# Example: install a Node.js CLI
npm install -g your-cli-tool

# Example: install a Python CLI
# pip install your-cli-tool

# Example: build from source
# cd /app/source && make install
```

### Step 4: Write Scenario Files

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

### Step 5: Run the Tests

**PowerShell (Windows):**

```powershell
# Run all scenarios
& path/to/run-scenarios.ps1 -TestDir ./test

# Run specific scenarios by glob pattern
& path/to/run-scenarios.ps1 -TestDir ./test -Pattern "smoke*"

# Use a custom Docker image name
& path/to/run-scenarios.ps1 -TestDir ./test -ImageName my-cli-test

# Use a different base OS (must match your Dockerfile FROM)
& path/to/run-scenarios.ps1 -TestDir ./test -ImageName my-cli-test
```

**Bash (Linux/macOS):**

```bash
# Run all scenarios
bash path/to/run-scenarios.sh --test-dir ./test

# Run specific scenarios by glob pattern
bash path/to/run-scenarios.sh --test-dir ./test --pattern "smoke*"

# Use a custom Docker image name
bash path/to/run-scenarios.sh --test-dir ./test --image-name my-cli-test
```

**Direct Docker (advanced):**

```bash
# Build the image
docker build -t my-cli-test -f test/Dockerfile test/

# Run all scenarios
docker run --rm -v ./test/scenarios:/app/scenarios my-cli-test

# Run specific scenarios
docker run --rm -v ./test/scenarios:/app/scenarios my-cli-test --pattern "smoke*"
```

### Step 6: Review and Commit

```bash
# Check what changed
git diff test/scenarios/

# If the output looks correct, commit as the new golden snapshot
git add test/scenarios/
git commit -m "test: update golden snapshots"
```

## Runner Flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--test-dir` | `-d` | `.` | Path to test directory containing `Dockerfile`, `setup.sh`, and `scenarios/` |
| `--pattern` | `-p` | `*.md` | Glob pattern for scenario files to run |
| `--image-name` | `-i` | `cli-snapshot-test` | Docker image name to use |
| `--no-build` | `-n` | (off) | Skip Docker build, use existing image |
| `--local` | `-l` | (off) | Run locally without Docker (requires bash) |

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
