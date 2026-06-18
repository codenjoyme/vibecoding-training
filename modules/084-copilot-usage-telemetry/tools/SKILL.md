---
name: copilot-usage-telemetry
description: >-
  Pull GitHub Copilot usage statistics without UI or screenshots. Two Python
  CLIs: one reads live credit/quota numbers from GitHub's private Copilot API,
  the other runs fast, context-free queries over the plugin's per-session
  `main.jsonl` debug log (tokens, requests, tool calls). Use when the user wants
  to track AI credits, premium-request usage, token counts, or inspect what a
  chat session actually did.
---

# Copilot Usage Telemetry

Two standalone tools that turn the Copilot status-bar hover numbers and the
hidden session logs into scriptable data.

| Script | Source | What it gives |
|--------|--------|---------------|
| `scripts/copilot_stats.py` | live GitHub API `copilot_internal/user` | AI credits / quota, plan, feature flags |
| `scripts/session_log.py` | local `debug-logs/*/main.jsonl` | tokens, context window, requests, tool calls — by line number |

Dependencies: `requests`, `python-dotenv` (only `copilot_stats.py` needs them;
`session_log.py` is stdlib-only).

---

## 1. `copilot_stats.py` — credits & quota (needs a token)

Reads `COPILOT_GITHUB_TOKEN` from a `.env` (searched upward from the current
directory AND the script's directory). The token is **never printed**. See
`.env.example` for the template. Requires a token from a Copilot-enabled
account (a classic GitHub PAT works; fine-grained PATs are rejected).

```bash
# Quick summary — the status-bar number (used %, remaining/entitlement, overage)
python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py credits

# Same data as JSON (text and json carry identical fields)
python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py credits --format json

# Everything the endpoint exposes (plan, flags, orgs, regional endpoints, full quotas)
python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py info

# `info --format json` prints the RAW endpoint response
python ./modules/084-copilot-usage-telemetry/tools/scripts/copilot_stats.py info --format json
```

**Key field for tracking:** AI credits = `premium_interactions.remaining`
(out of `entitlement`). The status-bar "N% used" = `100 - percent_remaining`.
Measure `remaining` before and after a run; the delta is what the run cost.

---

## 2. `session_log.py` — query the session log (no token, stdlib only)

The Copilot Chat extension writes one `main.jsonl` per session. These get large
(several MB), so load nothing into context — query it. Every view returns
**line numbers (coordinates)** so you can jump straight to a block.

This tool is intentionally generic: it knows nothing about UPD blocks or the
iterative-prompt pattern. It only provides primitives.

```bash
S=./modules/084-copilot-usage-telemetry/tools/scripts/session_log.py

# Find the current (most recent) log; --all lists every log newest-first
python $S locate
python $S locate --all

# Count events by type (tool_call, llm_request, user_message, …)
python $S types

# All user requests, with line numbers (great for finding UPD boundaries)
python $S requests

# Every raw line containing a substring (case-insensitive)
python $S grep "UPD2"

# Every tool_call for a tool (exact or substring match)
python $S tool read_file

# Tiny JSONPath-ish query (dot path, [index], * wildcard) over each event
python $S jsonpath attrs.model
python $S jsonpath attrs.inputTokens

# Pretty-print one event by line number, with optional context
python $S view 209 --context 2
```

Any command accepts an explicit log path as the last positional arg (default:
the most recent log), and `--json` for structured output.

### Event schema (from the `troubleshoot` skill)

Each line is one JSON event with `ts`, `dur`, `type`, `name`, `spanId`,
`parentSpanId`, `status`, `attrs`. Useful types:

- `user_message` — `attrs.content` (the raw user turn)
- `llm_request` — `attrs.model`, `inputTokens`, `outputTokens`, `maxTokens`, `userRequest`
- `tool_call` — `name`, `attrs.args`, `attrs.result`, `status`, `dur`
- `turn_start` / `turn_end` — tool-loop iteration boundaries

### Typical workflow

1. `requests` → get the line numbers of each user turn (e.g. where `UPD2` starts).
2. `jsonpath attrs.inputTokens` / `attrs.outputTokens` → token counts per request.
3. `tool <name>` → see which tools ran and how long they took.
4. `view <line> --context N` → drill into one event when you need detail.

---

## Security

- The real `.env` is gitignored; only `.env.example` is committed.
- `copilot_stats.py` never prints the token (only a non-secret fingerprint on auth errors).
- Session logs may contain file contents, paths, and pasted secrets — treat exports like server logs.
