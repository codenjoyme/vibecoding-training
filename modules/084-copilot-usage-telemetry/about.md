# Copilot Usage Telemetry — Credit & Token Tracking

**Duration:** 6-8 minutes

**Skill:** Pull GitHub Copilot credit/quota and token-usage statistics programmatically — directly from Copilot's internal API and the plugin's per-session debug logs — instead of reading the status bar and taking screenshots by hand.

**👉 Hands-on walkthrough — *coming soon* (module under construction).**

## Topics

- Where Copilot exposes usage data: the status-bar quota indicator vs. the per-session `debug-logs/*.jsonl`
- The private `copilot_internal/user` endpoint that backs the credit indicator (`quota_snapshots`, `quota_reset_date`)
- Reading token counts and context-window usage from `llm_request` events in the session logs
- Authenticating safely with a GitHub token kept in a gitignored `.env` (`COPILOT_GITHUB_TOKEN`)
- Why token *type* matters (classic PAT vs. fine-grained PAT vs. editor OAuth token) for internal endpoints
- Building a small Python CLI that the AI agent can later call as a skill

## Learning Outcome

You can run a Python CLI that fetches your current Copilot credit balance and quota reset date from GitHub's internal API, and you understand how to mine per-session token usage from the plugin's debug logs — all without screenshots or manual hovering.

## Prerequisites

### Required Modules

- [083 — AI Cost Optimization & Token Economics](../083-ai-cost-optimization/about.md)
- [108 — Token & API Key Management](../108-token-api-key-management/about.md)
- [103 — CLI: Command Line Interface](../103-cli-command-line-interface/about.md) *(optional, recommended)*

### Required Skills & Tools

- Python 3.10+ with `requests` and `python-dotenv`
- A GitHub account with an active Copilot subscription
- A GitHub token stored in a gitignored `.env` as `COPILOT_GITHUB_TOKEN`
