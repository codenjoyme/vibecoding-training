# Kata — Building Calculation Skills - Hands-on Walkthrough

In this module you will run a focused kata: the same 5-step loop repeated across multiple calculation themes. Each round creates a deterministic Python CLI skill (stdlib only) plus `SKILL.md`, then verifies output with exact commands.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Description |
|---|---|
| `work/678-kata/round-1-fibonacci/scripts/calculate.py` | Deterministic Fibonacci CLI with `--count`, `--output`, `--format` |
| `work/678-kata/round-1-fibonacci/SKILL.md` | Skill metadata and runnable examples |
| `work/678-kata/round-2-*/` | Second skill built from a new theme menu |
| `work/678-kata/round-3-*/` | Stretch round with your own calculation theme |

---

## Part 1: Warm-up on a Deterministic Skill

### What We'll Do

Review a worked skill example and identify why it is deterministic.

1. Open `instructions/calculate-trig-table/SKILL.md` as the reference example.
2. Trace the relationship between:
   - CLI script
   - `SKILL.md` usage examples
   - verification commands and outputs
3. Answer out loud: **What makes this skill deterministic?**

### What Happened

You anchored on the key distinction:
- **Model work:** generating scaffolding and docs from your prompt.
- **Tool work:** running predictable computation in Python stdlib with the same output for the same input.

---

## Part 2: Round 1 (Concrete) — Fibonacci Sequence Table

### What We'll Do

Run the full 5-step kata loop with exact prompts and CLI commands.

Before you start, switch your IDE chat to **Agent Mode** and pick **Claude Sonnet 4.5** (or newer).

### Step 0: Prepare Workspace

Use one of these paths:
- Windows: `c:/workspace/hello-genai/work/678-kata/round-1-fibonacci/`
- macOS/Linux: `~/workspace/hello-genai/work/678-kata/round-1-fibonacci/`

```powershell
# Windows (PowerShell)
mkdir c:/workspace/hello-genai/work/678-kata/round-1-fibonacci/scripts -Force
mkdir c:/workspace/hello-genai/work/678-kata/round-1-fibonacci/output -Force
cd c:/workspace/hello-genai
```

```bash
# macOS/Linux
mkdir -p ~/workspace/hello-genai/work/678-kata/round-1-fibonacci/scripts
mkdir -p ~/workspace/hello-genai/work/678-kata/round-1-fibonacci/output
cd ~/workspace/hello-genai
```

### 5-Step Loop (Round 1)

1. **Describe**
   Ask the agent:
   > Create a deterministic Python CLI in `work/678-kata/round-1-fibonacci/scripts/calculate.py` that generates a Fibonacci sequence table. Use `argparse` with `--count`, `--output`, and `--format` (`md|json|csv`). Use only Python stdlib.

2. **Generate script**
   Ask the agent to include:
   - input validation (`--count` > 0)
   - deterministic calculation only
   - output to stdout when `--output` is omitted
   - write to file when `--output` is set

3. **Write `SKILL.md`**
   Ask the agent:
   > Draft `work/678-kata/round-1-fibonacci/SKILL.md` with sections: name, description, version, usage, example commands, notes.

4. **Run**
   Execute commands exactly:

   ```bash
   python work/678-kata/round-1-fibonacci/scripts/calculate.py --count 10 --format md
   python work/678-kata/round-1-fibonacci/scripts/calculate.py --count 10 --format json --output work/678-kata/round-1-fibonacci/output/fibonacci.json
   python work/678-kata/round-1-fibonacci/scripts/calculate.py --count 10 --format csv --output work/678-kata/round-1-fibonacci/output/fibonacci.csv
   ```

5. **Verify**
   Confirm file outputs:

   ```bash
   cat work/678-kata/round-1-fibonacci/output/fibonacci.json
   cat work/678-kata/round-1-fibonacci/output/fibonacci.csv
   ```

   Check that:
   - sequence starts `0, 1, 1, 2, 3, 5...`
   - `SKILL.md` example commands run without edits
   - repeated runs produce identical output

### What Happened

You completed one full deterministic skill-creation cycle end to end.

---

## Part 3: Round 2 — Pick a New Theme and Repeat the Same 5 Steps

### What We'll Do

Repeat the identical loop with a different calculation domain.

Pick one theme:
1. Unit conversion table
2. Statistics summary
3. Amortization schedule
4. Prime sieve

For Round 2, keep the same interface contract:
- `scripts/calculate.py`
- `--output`
- `--format md|json|csv`
- deterministic stdlib-only logic

### What Happened

You reinforced the reusable workflow while changing only domain logic.

---

## Part 4: Round 3 (Stretch) — Your Own Theme

### What We'll Do

Name any calculation you want (for example: compound interest ladder, pacing calculator, percentile bands) and run the same 5-step loop with minimal scaffolding.

### What Happened

You moved from guided execution to independent skill creation.

---

## Part 5: Debrief + Optional Git Commit

### What We'll Do

Compare all created skills side by side and lock in the pattern.

Debrief prompts:
1. What stayed the same across all rounds?
2. What changed each round?
3. When should you use an LLM vs. a deterministic script?

Optional commit:

```bash
git add work/678-kata/round-1-fibonacci work/678-kata/round-2-* work/678-kata/round-3-*
git commit -m "feat(kata): add deterministic calculation skills rounds 1-3"
```

### What Happened

You now have a repeatable kata loop that can produce new calculation skills quickly and reliably.

---

## Success Criteria

- ✅ At least two skills were created, each with `scripts/calculate.py` and a complete `SKILL.md`
- ✅ Example commands in each `SKILL.md` run without modification
- ✅ You can explain deterministic vs. generative computation in your own words
- ✅ You can start a new calculation skill from scratch without re-reading this module
- ✅ (Stretch) Three rounds are committed to Git with a clear commit message

## Understanding Check

1. **Why is this kata faster than creating one large "perfect" skill in a single pass?**  
   *Expected:* Short loops provide quick feedback, reduce rework, and build repeatable muscle memory.
2. **What makes a calculation script deterministic in this module?**  
   *Expected:* Same inputs always produce the same outputs, with no model calls inside the script.
3. **Why keep the CLI contract (`--output`, `--format`) stable across rounds?**  
   *Expected:* Consistent interfaces make skills easier to test, compare, and reuse.
4. **When should the model be used in this workflow?**  
   *Expected:* For scaffolding, documentation, and iteration support—not for runtime calculation.
5. **When is `statistics`/`decimal` preferable to plain float arithmetic?**  
   *Expected:* When precision or explicit statistical summaries are required.
6. **What is the minimum package of a reusable skill artifact in this kata?**  
   *Expected:* A deterministic `scripts/calculate.py` plus a runnable, complete `SKILL.md`.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `python: command not found` | Python not in PATH | Install Python 3.9+ and reopen terminal |
| Script runs but output file is missing | Parent folder not created | Create `output/` before using `--output` |
| JSON/CSV format mismatch | Inconsistent serializer logic | Keep one internal data model and serialize per format |
| `SKILL.md` examples fail | Docs and script drifted | Re-run each example command verbatim and update docs immediately |
| Different output on repeated runs | Hidden non-determinism | Remove random/time-based logic and ensure stdlib-only deterministic computation |

## Next Steps

- Apply this kata loop to a real team utility in your current project.
- Pair with [104 — Port Existing Code into Skills](../104-port-to-skills/about.md) to package an existing script as a reusable skill.
- Add CLI snapshot tests from [091 — CLI Snapshot Testing with Docker](../091-cli-testing/about.md) when your new skill becomes shared team tooling.
