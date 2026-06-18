# Copilot Usage Telemetry — Hands-on Walkthrough

In this walkthrough you'll set up three small Python tools that pull your GitHub Copilot usage numbers without screenshots: live AI-credit balance from Copilot's internal API, per-session token counts from the plugin's debug logs, and a tracker that records one row of statistics for every iterative-prompt run. By the end you'll do a full end-to-end capture — `begin` a run, do some work, and `end` it — then export the collected table.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

## What We'll Build / Use

Three scripts live in [tools/scripts/](tools/scripts):

- **`copilot_stats.py`** — calls GitHub's private `copilot_internal/user` endpoint and prints your AI-credit / quota numbers (the status-bar hover figure). Needs a GitHub token. Depends on `requests` + `python-dotenv`.
- **`session_log.py`** — fast, context-free "select views" over a session's `main.jsonl` debug log: locate logs, list requests, count tokens. No token, stdlib only.
- **`usage_track.py`** — the orchestrator. Calls the other two and stores one telemetry row per run in a SQLite DB at `~/.copilot-telemetry/telemetry.db`. Stdlib only.

The behaviour and field reference for all three is documented in [tools/SKILL.md](tools/SKILL.md).

Use your real interpreter path where the examples say `python` (on Windows this training environment uses `C:/Java/python-3.13/python.exe`).

## Part 1: Set up a GitHub PAT token

The credit endpoint needs a token from a Copilot-enabled account. **A classic PAT works; fine-grained PATs are rejected** by the internal endpoint.

1. Go to https://github.com/settings/tokens → *Generate new token* → **Generate new token (classic)**.
2. Give it a note (e.g. `copilot-telemetry`) and the `read:user` scope. No other scopes are required for reading the quota.
3. Generate and copy the token (it starts with `ghp_`).
4. In the module's `tools/` folder, copy the template and fill in your token:
   - Copy [tools/.env.example](tools/.env.example) to a new file named `.env` (in the repo root or next to the scripts — it is searched upward).
   - Set `COPILOT_GITHUB_TOKEN=ghp_your_token_here`.
5. Confirm `.env` is gitignored (it already is in this repo). **Never commit the real token.**

What just happened: the scripts read `COPILOT_GITHUB_TOKEN` from `.env` and never print it. If the token is wrong you'll get a clear 401 with only a non-secret fingerprint (prefix + length), never the token itself.

## Part 2: Read your AI credits (`copilot_stats.py`)

1. Run the quick summary — the same number the status bar shows on hover:

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py credits
   ```

   You should see your plan, reset date, and a `premium_interactions` line with `used=…%  remaining=…/30000`. **AI credits = `premium_interactions.remaining`.**

2. Get the same data as JSON (text and json carry identical fields):

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py credits --format json
   ```

3. Dump everything the endpoint exposes (plan, feature flags, orgs, regional endpoints, full quotas):

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py info
   python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py info --format json
   ```

Verify that `credits` shows a `remaining` number. That single number, measured before and after a run, is what a run costs.

## Part 3: Explore a session log (`session_log.py`)

The Copilot Chat extension writes one `main.jsonl` per session. These get large (tens of MB), so never load one into context — query it.

1. List recent logs, grouped by workspace, with the resolved folder path:

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py locate
   ```

   Find your workspace by its folder path and **copy the session log path**.

2. Set that path into a variable and run the views against it explicitly (omitting the path picks the most-recent log across *all* workspaces — often not yours, because any keystroke in any chat bumps a different log's mtime):

   ```bash
   LOG="C:/Users/<you>/AppData/Roaming/Code - Insiders/User/workspaceStorage/<wsId>/GitHub.copilot-chat/debug-logs/<sid>/main.jsonl"

   python ./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py types "$LOG"
   python ./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py requests "$LOG"
   python ./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py jsonpath attrs.inputTokens "$LOG"
   python ./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py tool read_file "$LOG"
   python ./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py view 209 --context 2 "$LOG"
   ```

You should see `requests` print line numbers (coordinates) for each user turn — these mark where each `UPD` block begins.

## Part 4: Track a full run (`usage_track.py`)

Now tie it all together. This is the two-phase workflow an agent runs automatically, but you can do it by hand to see the whole loop.

1. **Begin** a run. It captures the start time and start credits, and prints a unique **marker**:

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py begin "UPD-demo"
   ```

   Note the `run_id` and `marker` (e.g. `FG8FBJ7EV547HBJEH`).

2. **Echo the marker** somewhere it lands in the session log — paste it into the chat. This is what lets `end` find the exact log for this run (no guessing about "most recent").

3. Do some work (ask the agent anything), then **end** the run with the human minutes you spent writing the prompt and reading the result:

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py end <run_id> --write-min 5 --read-min 10
   ```

   It captures end credits, resolves the log by the marker, and extracts model, token sums, context start/finish, and a compaction heuristic.

4. If the final response hadn't flushed to the log yet, top it up later:

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py refresh <run_id>
   ```

5. Inspect what was stored and export the tracking table:

   ```bash
   python ./modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py list
   python ./modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py show <run_id>
   python ./modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py export --format md
   ```

The `export` output is the original tracking table — date, times, credits start/end/spent, context window, model, thinking effort, vendor, request/response text — ready to paste into a report.

## Part 5: Wire it into an agent (optional)

To have an agent run `begin`/`end` for you on every iteration, add a short optional pointer to its instruction file. The canonical procedure lives in the **Agent integration block** of [tools/SKILL.md](tools/SKILL.md) so you don't copy steps around:

```markdown
## Usage telemetry (optional)

If `modules/084-copilot-usage-telemetry/tools/scripts/usage_track.py` exists,
follow the **Agent integration block** in
`modules/084-copilot-usage-telemetry/tools/SKILL.md` to record one telemetry
row per run (`begin` + echo marker at the start, `end` after the commit).
```

This repo already wires it into [.github/agents/iterative-prompt.agent.md](../../.github/agents/iterative-prompt.agent.md).

## Success Criteria

- ✅ A classic PAT is stored in a gitignored `.env` as `COPILOT_GITHUB_TOKEN`.
- ✅ `copilot_stats.py credits` prints your `premium_interactions.remaining`.
- ✅ `session_log.py locate` shows your workspace by its folder path.
- ✅ `session_log.py requests "$LOG"` lists user turns with line numbers.
- ✅ A full `begin` → echo marker → `end` cycle stored a row in the SQLite DB.
- ✅ `usage_track.py export --format md` produces the tracking table.

## Understanding Check

1. Where does the "AI credits" number come from, and which exact field is it? *(GitHub's `copilot_internal/user` endpoint; `premium_interactions.remaining`.)*
2. Why must you pass an explicit log path to `session_log.py` instead of relying on the default? *(The default is the most-recent log across all workspaces; any keystroke in any chat updates a different log's mtime, so it's often not yours.)*
3. Why does `usage_track.py` print a marker, and what does the agent do with it? *(The marker is echoed into the chat so it lands in the session log; `end` finds the log that contains it — that's provably this run's log.)*
4. Which token type is rejected by the internal endpoint? *(Fine-grained PATs; use a classic `ghp_` PAT.)*
5. What does `context_max` represent, and why isn't it the model's full window? *(It's the per-request response budget `maxTokens`; the log doesn't expose the full context window like the 264K status-bar figure.)*
6. Where do the human "minutes writing / reading" values come from? *(They aren't in the logs — the agent asks the user and passes `--write-min` / `--read-min`.)*
7. What is the difference between `debug-logs` and `chatSessions`, and which has token counts? *(`chatSessions` is the rendered UI conversation, no tokens; `debug-logs/main.jsonl` is telemetry with `inputTokens`/`outputTokens`.)*

## Troubleshooting

- **401 Unauthorized on `credits`** — the token was rejected. Use a classic PAT (`ghp_…`), not a fine-grained one; make sure `.env` has the current value.
- **`credits` shows nothing but the token is valid** — the account may not have an active Copilot subscription, or `quota_snapshots` is empty.
- **`locate` shows the wrong workspace** — that's expected; it's mtime-sorted across all workspaces. Find your folder path in the grouped output and copy that session's path.
- **`end` didn't capture tokens / response text** — the log hadn't flushed yet. Run `usage_track.py refresh <run_id>` on the next turn.
- **Unicode/Cyrillic crash on Windows** — already handled; the scripts force UTF-8 stdout. If you see it, ensure you're on the current script versions.

## Next Steps

You now collect Copilot usage automatically around each run. Continue with the rest of the cost-optimization track, and use `usage_track.py export` to analyse which prompts cost the most credits and tokens — then optimise them.
