# CI/CD Pipeline with AI Agents - Hands-on Walkthrough

In this walkthrough, you'll build a GitHub Actions pipeline from scratch. It will run your tests automatically on every push, fail when snapshot output changes, and connect the full cycle: AI agent creates a PR, CI validates it, and you merge with confidence.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build

By the end of this walkthrough you will have:

- **A working CI workflow** — `.github/workflows/ci.yml` that runs on every push and pull request
- **Automated test execution** — both unit tests (pytest/jest) and snapshot comparison running in CI
- **Pipeline failure notifications** — you get notified when something breaks
- **A tested full loop** — create issue → AI agent opens PR → CI runs → tests pass → merge

---

## Part 1: Understand what CI/CD does

Before writing any YAML, ask AI:

```
Explain what a CI/CD pipeline is to a non-programmer manager.
Specifically: what problem does it solve that "just running tests locally" doesn't solve?

Then explain these specific GitHub Actions concepts in plain language:
- workflow file
- trigger (on: push, pull_request)
- job
- step
- matrix strategy (for running tests on multiple environments)

Use an analogy from management or manufacturing if helpful.
```

The key insight: CI is not optional for AI-assisted development. When AI agents push code, no human ran the code locally first. CI is the first safety check.

---

## Part 2: Create your first workflow file

**What we're about to do:** Create a workflow file that runs on every push and executes your tests.

Ask AI to generate the workflow:

```
Create a GitHub Actions workflow file for a [Python/Node.js] project.
The file should:

1. Trigger on: push to main, and on any pull_request to main
2. Run on: ubuntu-latest
3. Steps:
   a. Check out the code
   b. Set up [Python 3.11 / Node.js 20]
   c. Install dependencies from [requirements.txt / package.json]
   d. Run pytest / npm test
4. If any step fails, the workflow should fail and stop

Generate the complete .github/workflows/ci.yml file.
```

Review the generated YAML. It will look something like:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
```

Create the file at `.github/workflows/ci.yml` in your repository.

---

## Part 3: Add snapshot testing to the pipeline

**What we're about to do:** Extend the workflow to run your snapshot runner and compare the output to the committed baseline.

The key insight: the snapshot test in CI works differently from local. Locally you compare files manually. In CI, a script compares them and exits with a non-zero status if they differ — which causes the pipeline to fail.

Ask AI to help:

```
I have a snapshot testing setup from module 132:
- snapshot_runner.py — outputs to snapshot_current.txt
- snapshot_baseline.txt — committed to the repo, the expected state

Create a compare_snapshots.py script that:
1. Runs snapshot_runner.py (subprocess call)
2. Reads snapshot_baseline.txt and snapshot_current.txt
3. If they are identical: prints "PASS: snapshots match" and exits with code 0
4. If they differ: prints a clear diff showing what changed, and exits with code 1

Exit code 1 causes GitHub Actions to fail the step.
```

Add a new step to your workflow after the test step:

```yaml
      - name: Snapshot regression check
        run: python compare_snapshots.py
```

Push this change to your repository. GitHub Actions will run automatically.

---

## Part 4: Watch CI run on a Pull Request

Use the GitHub UI to create a test pull request:

1. Create a new branch: `git checkout -b test/ci-validation`
2. Make a small change (add a comment to any file)
3. Push the branch: `git push origin test/ci-validation`
4. Open a Pull Request on GitHub

Open the PR. Under the "Checks" section, you'll see your CI workflow running. Watch it:
- Green checkmarks = each step passed
- If one fails, click it to see the log

**What just happened:** This is the automated quality gate. Before any code merges, CI validates it. When an AI agent opens a PR (module 150), this same pipeline runs — automatically, before any human review.

Merge or close the test PR.

---

## Part 5: Trigger a deliberate failure

**What we're about to do:** Change your code to make a snapshot fail in CI — so you see exactly what the failure looks like and how to read the failure log.

Make a small change to your application that changes the output (e.g., change a string, a number, a default value). Commit and push:

```
git add .
git commit -m "test: trigger CI snapshot failure"
git push origin main
```

Open GitHub Actions. The snapshot step will fail. Click on it. The log will show the diff — what changed.

This is the workflow for the rest of your project's life:
1. Change breaks snapshot → CI fails → you see the diff → decide: revert or update baseline
2. If the change is intentional: update `snapshot_baseline.txt`, push again → CI passes

Revert the change now: `git revert HEAD`. Push. CI should go green again.

---

## Part 6: Set up failure notifications

By default, GitHub emails you when a workflow fails — but only if you set it up.

Go to your GitHub repository → Settings → Notifications (or check your personal GitHub notification settings). Make sure:
- Email notifications are enabled for "Actions"
- Or install the [GitHub mobile app](https://github.com/mobile) for push notifications

Ask AI:

```
How do I add a step to my GitHub Actions workflow that posts a message 
to a Slack channel (or sends a webhook) when the CI pipeline fails?
Show me the simplest possible implementation using GitHub's built-in 
notification actions or a free webhook service.
```

Add the notification step to your workflow if you have a Slack workspace or webhook endpoint available.

---

## Part 7: Run the full delegation loop

**What we're about to do:** Run the complete workflow end-to-end — from issue to merged code — with CI as the automated quality gate.

1. **Create a GitHub Issue** — describe a small enhancement to your PoC (from module 150)
2. **Delegate to AI agent** — use the GitHub Coding Agent to address the issue
3. **AI opens a PR** — the agent commits code and opens a pull request
4. **CI runs automatically** — tests and snapshot comparison execute without any human trigger
5. **Review the CI results** — if green, review the code (module 152 workflow), then merge
6. **Merge** — the code is in main, CI runs one final time on main

Observe: you never ran the code locally. CI was your safety net. The AI agent wrote the code. You reviewed, CI validated, you merged.

---

## Success Criteria

- ✅ `.github/workflows/ci.yml` exists and triggers on push and pull_request
- ✅ Unit tests run in CI and all pass
- ✅ Snapshot comparison runs in CI and passes against committed baseline
- ✅ You deliberately broke a snapshot and watched CI fail with the diff visible in the log
- ✅ You reverted the change and CI went green again
- ✅ Failure notifications are configured (email or Slack)
- ✅ You ran the full loop: issue → agent PR → CI → review → merge

---

## Understanding Check

1. **Why does CI need to run on pull_request, not just on push to main?**
   > The goal is to catch problems before merging, not after. If CI only runs on main, broken code is already in the main branch by the time the failure is detected. Running on pull_request means the pipeline validates the code before it's merged — when it can still be rejected.

2. **What is the significance of "exit code 1" in a shell script used in CI?**
   > Unix-based systems signal success with exit code 0 and failure with any non-zero code (typically 1). GitHub Actions treats a non-zero exit as step failure, which marks the job as failed and blocks the pull request from being merged (if branch protection is configured).

3. **If the snapshot comparison fails on CI but passes locally, what are the most likely causes?**
   > (1) The application depends on environment variables not set in CI. (2) The application calls an external API that behaves differently or is rate-limited in CI. (3) The output contains timestamps or random values that weren't normalised. (4) A dependency version is different between local and CI. Check the CI logs carefully — they show the exact diff.

4. **What is the purpose of `actions/checkout@v4` as the first step in every workflow?**
   > GitHub Actions runs in a fresh virtual machine that has no code. `actions/checkout` clones your repository into the CI workspace. Without it, every subsequent step would fail because there are no files to work with.

5. **You delegate a feature to the GitHub AI agent. It opens a PR, CI passes, and the code looks fine in the diff. Is it safe to merge?**
   > CI passing means the tests and snapshots pass — it doesn't mean the feature is correct by requirements. You still need to verify that the agent implemented what you intended: does the feature work as described in the issue? Are edge cases handled? Code review (module 152) is the human verification step that CI cannot replace.

6. **What is "branch protection" and how does it relate to CI?**
   > Branch protection rules on GitHub can require CI to pass before any PR can be merged. Without it, CI is advisory — someone can merge even if tests fail. With branch protection, failed CI physically blocks the merge button. This turns CI from a recommendation into an enforcement mechanism.

---

## Troubleshooting

**CI fails with "command not found: pytest" even though requirements.txt includes pytest**
> The CI step may be running before the install step, or there's a Python path issue. Check the workflow step order — install must come before test. Also verify the run command matches exactly what works locally: `python -m pytest tests/` instead of just `pytest` sometimes resolves PATH issues.

**Snapshot comparison fails on CI but baseline was committed**
> Check whether `snapshot_baseline.txt` was committed with Windows line endings (CRLF) while CI runs on Linux (LF). Add `.gitattributes` to normalise: `*.txt text eol=lf`. Or update your compare script to normalise line endings before comparison.

**GitHub Actions is not triggering on my push**
> Verify the workflow file is committed to the correct branch (`main` or `master`). Check the file is in `.github/workflows/`. Check the `on:` trigger in the YAML matches your branch name exactly. GitHub Actions only picks up workflows from the default branch.

**CI minutes are running out on my private repository**
> GitHub gives 2,000 free CI minutes per month for private repositories. Optimise by: (1) Running CI only on pull_request, not on every push to main. (2) Using `paths:` filter to skip CI if only documentation changed. (3) Using `ubuntu-latest` (cheapest runner) rather than Windows or macOS runners.

---

## Next Steps

You now have a fully automated validation pipeline. The next logical step is to expand your integration capabilities:

**→ [Module 160 — Bulk File Processing with AI](../160-bulk-file-processing-with-ai/about.md)**

With CI handling quality, you can focus on building more advanced AI-powered features for your team.
