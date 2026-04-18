# CLI Snapshot Testing with Docker — Hands-on Walkthrough

In this module you will learn a powerful approach to testing CLI tools without writing conventional unit tests. Instead, you capture the full output of your CLI as a Markdown "golden snapshot" and use `git diff` to detect regressions. The approach is inspired by [Approval Tests](https://approvaltests.com/) by Llewellyn Falco, with three key innovations: no automated assertions (you or an LLM review the diff), Markdown-based scenario format (readable documentation that doubles as tests), and Docker-based execution (OS-agnostic, clean environment every run).

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough, you will have:

- **A scenario file** — a Markdown document listing CLI commands with descriptions of why each matters
- **A Docker setup** — a clean container that installs your CLI and runs the scenarios
- **A golden snapshot** — the scenario file with captured output committed to Git
- **A regression workflow** — run, diff, review, commit (or fix)

Components:
| Component | Purpose | Location |
|-----------|---------|----------|
| `run-scenarios.sh` | Universal bash runner (read-only) | Skill tool |
| `run-scenarios.ps1` | PowerShell wrapper for Windows | Skill tool |
| `Dockerfile` | Your custom container setup | Your test dir |
| `setup.sh` | CLI installation script | Your test dir |
| `scenarios/*.md` | Test scenario files | Your test dir |

## Part 1: Understand the Concept

### What is Approval Testing?

Traditional testing: you write assertions — `expect(output).toBe("hello")`. You define the expected result manually for every case.

**Approval testing** (by Llewellyn Falco): you run the system, capture its full output, and _approve_ it as the "truth." On the next run, any difference from the approved output is a potential regression.

### Three Innovations in This Skill

1. **No automated assertion.** The output is saved as a Markdown snapshot. You (or an LLM reviewing `git diff`) decide whether the diff is acceptable. In the LLM era, the model can look at the snapshot + your recent code changes and diagnose what went wrong — far more effectively than reading assertion failure messages.

2. **Markdown-based scenario format.** The test is a readable document with descriptions of _why_ each command matters, interleaved with commands and their output. It's documentation + test + evidence in one file.

3. **OS-agnostic via Docker.** Everything runs inside a container. Windows, macOS, Linux — same results. Line endings are normalized automatically.

### Why This Matters for Legacy Projects

A legacy project is one that works but has no tests. You can't add unit tests without understanding the code. But you _can_ capture what the CLI does today, approve that as truth, and detect when future changes alter that behavior. This is your safety net.

## Part 2: Explore the Demo

Let's start by looking at a working example.

1. Open your terminal and navigate to your workspace:

   **Windows (PowerShell):**
   ```powershell
   cd c:/workspace/hello-genai/
   ```

   **macOS/Linux:**
   ```bash
   cd ~/workspace/hello-genai/
   ```

2. Copy the skill's demo folder to your workspace. The demo includes a Node.js example (cowsay) and a Python example (httpie):

   ```
   # Copy the entire demo folder from the skill
   ```

   Or create a link / reference to the demo directory in the module's tools folder.

3. Look at the Node.js demo structure:

   ```
   demo/node-cli/
   ├── Dockerfile          ← Container with Node.js + cowsay
   ├── setup.sh            ← Installs cowsay globally
   ├── run-demo.ps1        ← One-click runner
   └── scenarios/
       └── basic-commands.md  ← Scenario file
   ```

4. Open `demo/node-cli/scenarios/basic-commands.md` and examine the format:

   ```markdown
   # Cowsay CLI — Snapshot Test

   ## Phase 1: Basic Commands

   Verify cowsay is installed and accessible.

   > `command -v cowsay`

   Check that it runs with default cow.

   > `cowsay "Hello from snapshot testing!"`
   ```

   Notice: commands are written as `` > `command` ``. Everything else is descriptive text that the runner passes through unchanged.

## Part 3: Run the Node.js Demo

1. Navigate to the skill's demo directory:

   **Windows (PowerShell):**
   ```powershell
   cd modules/091-cli-testing/tools/cli-test-runner/demo/node-cli
   ```

2. Run the demo:

   **Windows (PowerShell):**
   ```powershell
   & .\run-demo.ps1
   ```

   **What happens:**
   - Docker builds an image with Node.js and cowsay installed
   - The runner reads `scenarios/basic-commands.md`
   - Each `` > `command` `` line is executed inside the container
   - Output is captured and inserted as a fenced code block after each command
   - The result is written back to the same file

3. Open `scenarios/basic-commands.md` again. It now contains the output:

   ```markdown
   > `cowsay "Hello from snapshot testing!"`
   ```
    ______________________________
   < Hello from snapshot testing! >
    ------------------------------
           \   ^__^
            \  (oo)\_______
               (__)\       )\/\
                   ||----w |
                   ||     ||
   ```

4. Check what changed using Git:

   ```bash
   git diff scenarios/basic-commands.md
   ```

   You'll see the commands are unchanged but output blocks were added.

5. **This is your golden snapshot.** If you commit it, the next run will either produce identical output (no diff = stable) or show exactly what changed (diff = investigate).

## Part 4: Run the Python Demo

1. Navigate to the Python demo:

   ```powershell
   cd ../python-cli
   ```

2. Run the demo:

   ```powershell
   & .\run-demo.ps1
   ```

3. Check the result:

   ```bash
   git diff scenarios/basic-commands.md
   ```

   You'll see HTTPie's help output, version string, and offline HTTP request formatting — all captured automatically.

**Key observation:** The same runner script (`run-scenarios.sh`) works for both Node.js and Python CLIs. Only the `Dockerfile` and `setup.sh` change.

## Part 5: Create Your Own Test

Now let's set up snapshot testing for a CLI of your choice. We'll use a simple example: testing bash built-in commands.

1. Create a test directory in your workspace:

   ```bash
   mkdir -p my-cli-test/scenarios
   ```

2. Create `my-cli-test/setup.sh`:

   ```bash
   #!/usr/bin/env bash
   # No additional setup needed — we're testing bash builtins
   echo "Setup complete."
   ```

3. Create `my-cli-test/Dockerfile`:

   ```dockerfile
   FROM ubuntu:22.04

   RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

   COPY setup.sh /app/setup.sh
   RUN chmod +x /app/setup.sh && /app/setup.sh

   COPY run-scenarios.sh /app/run-scenarios.sh
   RUN chmod +x /app/run-scenarios.sh

   COPY scenarios/ /app/scenarios/
   RUN mkdir -p /workspace

   ENTRYPOINT ["bash", "-c", "sed 's/\\r$//' /app/run-scenarios.sh > /tmp/run.sh && bash /tmp/run.sh \"$@\"", "--"]
   ```

4. Create `my-cli-test/scenarios/bash-builtins.md`:

   ```markdown
   # Bash Builtins — Snapshot Test

   ## Phase 1: Environment

   Check the current user.

   > `whoami`

   Show the current working directory.

   > `pwd`

   ## Phase 2: File Operations

   Create a temporary file and verify.

   > `cd /workspace`
   > `echo "hello world" > test.txt`
   > `cat test.txt`
   > `wc -c test.txt`
   ```

5. Copy the runner script and run:

   **Windows (PowerShell):**
   ```powershell
   # From the skill directory
   & path/to/run-scenarios.ps1 -TestDir ./my-cli-test -ImageName my-cli-test
   ```

6. Check the output:

   ```bash
   cat my-cli-test/scenarios/bash-builtins.md
   ```

   You should see output blocks filled in after each command:
   - `whoami` → `root`
   - `pwd` → `/workspace`
   - `cat test.txt` → `hello world`
   - `wc -c test.txt` → `12 test.txt`

7. Commit as golden snapshot:

   ```bash
   git add my-cli-test/
   git commit -m "test: add bash builtins golden snapshot"
   ```

## Part 6: The Regression Workflow

This is where snapshot testing shines.

1. **Make a change** to your scenario. For example, modify the echo command:

   Edit `my-cli-test/scenarios/bash-builtins.md` — change `"hello world"` to `"hello snapshot testing"`.

2. **Re-run** the tests:

   ```powershell
   & path/to/run-scenarios.ps1 -TestDir ./my-cli-test -ImageName my-cli-test
   ```

3. **Check the diff:**

   ```bash
   git diff my-cli-test/scenarios/bash-builtins.md
   ```

   You'll see:
   - The `echo` command changed (expected — you changed it)
   - The `cat` output changed from `hello world` to `hello snapshot testing` (expected)
   - The `wc -c` value changed to `23 test.txt` (expected — different string length)

4. **Feed this to an LLM** — paste the `git diff` output into your AI assistant and ask:

   > "I changed the echo message in my CLI test. Does the diff look correct?"

   The LLM will confirm all changes are consistent with your modification. This is dramatically more effective than reading assertion failures.

5. **Commit or fix:**

   ```bash
   git add my-cli-test/scenarios/bash-builtins.md
   git commit -m "test: update snapshot after echo message change"
   ```

## Part 7: Customization Tips

### Changing the Base OS

Change the `FROM` line in your Dockerfile:

```dockerfile
FROM alpine:3.19        # Minimal Linux
FROM ubuntu:22.04       # Full-featured Linux
FROM node:20-slim       # Node.js pre-installed
FROM python:3.12-slim   # Python pre-installed
FROM golang:1.22        # Go pre-installed
```

### Running Specific Scenarios

Use the `--pattern` flag to run only matching files:

```powershell
& run-scenarios.ps1 -TestDir ./my-cli-test -Pattern "smoke*"
```

### Multiple Scenario Files

Organize by feature:

```
scenarios/
├── auth-commands.md
├── data-import.md
├── error-handling.md
└── smoke-test.md
```

Run all at once (default) or selectively with `--pattern`.

### Important: Commands Get `/dev/null` as stdin

The runner redirects stdin to `/dev/null` to prevent commands from accidentally consuming the scenario file. If your CLI reads from stdin, pipe data explicitly:

```markdown
> `echo '{"key":"val"}' | my-cli parse`
```

## Success Criteria

- ✅ You understand the difference between approval/snapshot testing and assertion-based testing
- ✅ You ran at least one demo (Node.js or Python) successfully
- ✅ You created your own scenario file and Dockerfile for a CLI
- ✅ You executed the scenarios and saw output captured in the Markdown file
- ✅ You used `git diff` to review changes after a modification
- ✅ You committed a golden snapshot to Git
- ✅ You understand the regression workflow: change → run → diff → review → commit/fix

## Understanding Check

1. **What is the core idea behind Approval Tests, and who created it?**
   Llewellyn Falco created Approval Tests. The core idea: instead of writing individual assertions, you capture the full system output, approve it as truth, and detect regressions by comparing future output against the approved snapshot.

2. **Why is the Markdown format beneficial for snapshot tests?**
   It combines documentation (why each test matters), the test itself (the commands), and the evidence (the output) in one readable file. It's human-readable, version-controllable, and reviewable in pull requests.

3. **Why does this framework run inside Docker?**
   Docker provides a clean, reproducible environment. Every run starts from scratch — no leftover artifacts, no OS-specific differences. The same test produces the same output on Windows, macOS, and Linux.

4. **How do you detect a regression with this approach?**
   Run the scenarios, then check `git diff` on the scenario files. If the diff is empty, behavior is stable. If something changed, review the diff (yourself or with an LLM) to decide if it's expected or a regression.

5. **What happens when commands read from stdin in the scenario runner?**
   The runner redirects stdin to `/dev/null` to prevent commands from consuming the scenario file. If your CLI needs stdin data, pipe it explicitly: ``echo 'data' | my-cli``.

6. **How does the LLM-assisted review workflow improve over traditional test failures?**
   Instead of reading cryptic assertion failures, you show the LLM the full before/after context via `git diff`. The LLM can cross-reference the output changes against your code changes and explain whether the differences are expected. It sees the full picture, not just one failing check.

7. **What's the difference between the first run and subsequent runs of a scenario?**
   The first run fills in empty output blocks (or creates them if absent). Subsequent runs replace the existing output. The committed file serves as the golden truth. Any difference on re-run is a signal to investigate.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker build fails | Verify Docker Desktop is running. Check `setup.sh` for syntax errors. |
| "No scenario files matching..." | Verify `scenarios/` directory exists and contains `.md` files. Check `--pattern` value. |
| Output blocks are empty | The command might have failed silently. Try running the command directly inside the container: `docker run -it <image> bash` |
| Line endings differ on Windows | The runner normalizes `\r\n` to `\n`. If you still see line ending diffs, configure Git: `git config core.autocrlf input` |
| Command consumes scenario file | Add `--ignore-stdin` to your CLI command, or the runner handles this via `/dev/null` stdin redirection |
| Git diff shows timestamp/hash changes | Expected — these change every run. Focus on structural and behavioral differences. |
| PowerShell script execution blocked | Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` |

## Next Steps

- Try snapshot-testing a CLI you use at work
- Integrate snapshot tests into your CI/CD pipeline: run on every PR, fail if diff is non-empty (unless explicitly approved)
- Explore [module 132 — AI-Assisted Test Generation](../132-ai-assisted-test-generation/about.md) for complementary testing approaches
- Use the LLM review workflow to automate regression analysis in your development process
