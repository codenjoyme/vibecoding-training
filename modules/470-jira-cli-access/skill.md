# Jira CLI — AI Agent Skill

> **This file is both a human guide and an AI skill.** When an AI agent reads this file, it gains full context on how to query Jira using the `jira_cli.py` script. Share this file with your AI agent and ask it to use the CLI for any Jira-related task.

---

## What This Skill Does

This skill gives the AI agent access to a Jira instance via a local Python CLI script (`jira_cli.py`). The agent can search for issues using JQL, fetch issue details, list attachments, and download binary files — all without loading an MCP server into the context window.

**Key advantages over MCP tools:**
- Works outside the AI context window — saves tokens
- Handles binary file downloads (PDFs, images, ZIPs) cleanly
- No MCP server startup required — runs on demand
- Portable pattern: same CLI interface works from terminal, CI/CD, or scripts

---

## When to Invoke This Skill

Use this skill when the user asks to:
- Find Jira issues matching certain criteria
- Get details of a specific issue (summary, status, assignee, description, comments)
- List or download attachments from an issue
- Check sprint status or board contents
- Summarize or analyze Jira data

Do **not** use this skill if:
- The user wants to create or modify issues at scale (prefer Jira UI or dedicated scripts)
- The Jira instance is not configured in `.env`

---

## Prerequisites

Before invoking any CLI command, confirm:
1. `work/470-jira-cli/jira_cli.py` exists in the workspace
2. `work/470-jira-cli/.env` exists with `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
3. Python environment has `requests` and `python-dotenv` installed

---

## CLI Usage Reference

All commands run from the `work/470-jira-cli/` directory:

```
python jira_cli.py <command> [options]
```

### `search` — Search issues with JQL

```
python jira_cli.py search --jql "project=ABC AND status=Open" [--format table|json|plain] [--max 20]
```

**Options:**
- `--jql` (required): JQL query string
- `--format`: output format — `table` (default), `json`, or `plain`
- `--max`: maximum number of results (default: 20, max: 100)

**Example output (table):**
```
KEY         SUMMARY                        STATUS      ASSIGNEE
ABC-123     Fix login bug on mobile        In Progress Alice
ABC-124     Update API documentation       Open        Bob
```

### `get` — Fetch a single issue

```
python jira_cli.py get --key ABC-123 [--format table|json|plain]
```

**Output includes:** key, summary, status, assignee, reporter, priority, created, updated, description, labels, components, comments count.

### `attachments` — List attachments on an issue

```
python jira_cli.py attachments --key ABC-123
```

**Output:** filename, MIME type, size, download URL.

### `download` — Download a binary attachment

```
python jira_cli.py download --key ABC-123 --filename "screenshot.png" --output ./downloads/
```

Downloads the named attachment to the `--output` directory. Works for any file type including PDFs, images, and ZIP archives.

---

## Environment Variables

The CLI reads credentials from `work/470-jira-cli/.env`:

```
JIRA_URL=https://your-org.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_api_token_here
```

**Security rules enforced by the CLI:**
- `JIRA_URL` must start with `https://` — plain HTTP is rejected
- Token is never printed in output or logs
- `.env` must not be committed (enforced by `.gitignore`)

---

## Invocation Workflow for the AI Agent

When the user asks about Jira issues, follow this workflow:

1. **Confirm environment** — check that `.env` exists and is populated (ask the user if not)
2. **Build the JQL query** — translate the user's request to JQL
3. **Run `search`** — get matching issues in table format for quick scan
4. **Run `get`** if the user wants full details on a specific issue
5. **Run `attachments`** if the user needs to inspect or download files
6. **Summarize results** in plain language — do not dump raw JSON to the user

**Example agent workflow:**
```
User: "Show me all open P1 bugs in the PAYMENT project assigned to me"

Agent steps:
1. Run: python jira_cli.py search --jql "project=PAYMENT AND priority=Highest AND status=Open AND assignee=currentUser()"
2. Present results as a table
3. Offer to get details on any specific issue
```

---

## Error Handling

| Error | Likely cause | Agent action |
|-------|-------------|--------------|
| `401 Unauthorized` | Token invalid or expired | Ask user to regenerate token at https://id.atlassian.com/manage-api-tokens |
| `403 Forbidden` | Token lacks permissions for this operation | Ask user to check token scope |
| `400 Bad Request` | Invalid JQL syntax | Fix the JQL query and retry |
| `Connection refused` | Wrong `JIRA_URL` or network issue | Verify URL and VPN connection |
| `.env not found` | Setup not completed | Guide user through setup (see walkthrough Part 2) |

---

## Porting to Other Languages

This CLI pattern is language-agnostic. The core logic is:
1. Read credentials from environment variables
2. Make HTTP Basic Auth requests to Jira REST API v3
3. Parse JSON response
4. Format output to stdout

**Equivalent patterns:**
- **Node.js:** `axios` + `dotenv` + `commander`
- **Go:** `net/http` + `godotenv` + `cobra`
- **Java:** `OkHttp` + `dotenv-java` + `picocli`
- **Bash:** `curl` + `.env` file sourced manually

Ask your AI agent: *"Port `jira_cli.py` to [language] keeping the same command structure"*
