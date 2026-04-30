# Jira CLI Access via MCPyrex Python Script — Hands-on Walkthrough

In this module you will build a Python CLI that queries Jira via the REST API, secure an API token with minimum permissions and IP restriction, connect the CLI to an AI agent via a skill descriptor, and optionally port the solution to another language.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Location | Purpose |
|-----------|----------|---------|
| `jira_cli.py` | `work/470-task/` | CLI script for querying Jira |
| `.env` | **project root** | Credentials (never committed) — shared by all tools |
| `SKILL.md` | `tools/SKILL.md` | AI agent descriptor |
| `test/` | `modules/470-jira-cli-access/test/` | Snapshot tests (Docker) |

---

## Part 1 — Why CLI, Not MCP, for Jira

**Time: 5 min**

### The MCP Context Problem

When you attach a Jira MCP server to your AI agent, every tool definition, schema, and response flows through the **context window**. For a typical sprint with 40 issues:
- Each issue = ~500 tokens of JSON
- 40 issues = ~20,000 tokens consumed before you ask a single question
- The model gets slower and more expensive with every tool call

**CLI runs outside the context window.** The agent calls the script, the script queries Jira, and the agent receives only the formatted output it needs — nothing more.

### Binary File Limitation of MCP

MCP tools return JSON. JSON cannot encode binary data cleanly. If you want to download a PDF attachment, a screenshot, or a ZIP file from Jira:
- ❌ MCP tool: must base64-encode → bloats context → often hits size limits
- ✅ CLI tool: streams directly to disk, returns only the filename

### CLI Advantages Summary

| Capability | MCP Tool | CLI Tool |
|-----------|----------|----------|
| Context usage | High (schema + all responses) | Minimal (formatted output only) |
| Binary downloads | Problematic | Native |
| Scriptable in CI/CD | No | Yes |
| Language-portable | Requires MCP server rewrite | Copy and translate the script |
| Testable independently | Requires MCP infrastructure | `python jira_cli.py search --jql "..."` |
| Extend with custom logic | Modify MCP server | Add a function |

> **When would you still choose MCP?** When you need real-time tool invocation inside an agent loop without leaving the chat, or when binary files are not involved. Module [106 — FastMCP](../106-fastmcp-custom-mcp-server/about.md) covers that path.

### Knowledge Check

*Q: You need to download 15 PDF attachments from sprint issues for a stakeholder report. CLI or MCP?*

**A:** CLI — MCP cannot stream binary files to disk; CLI downloads them natively.

---

## Part 2 — Creating a Secure Jira API Token

**Time: 8 min**

### Step 1: Find Your Current IP

Before creating the token, know which IP you will whitelist:

```powershell
# Windows PowerShell
Invoke-RestMethod -Uri "https://ifconfig.me"
```

```bash
# macOS / Linux
curl -s ifconfig.me
```

> **Best practice:** Connect to your company VPN **first**, then check your IP. The IP you whitelist should be the VPN egress IP — not your home IP. This way, even if your token leaks, an attacker cannot use it without access to your VPN.

### Step 2: Create the Token

**Atlassian Cloud (jira.atlassian.net):**
1. Go to: [https://id.atlassian.com/manage-api-tokens](https://id.atlassian.com/manage-api-tokens)
2. Click **Create API token**
3. Set a **label** (`jira-cli-dev`) and an **expiration date** (90 days is reasonable)
4. Click **Create** → copy the token immediately (shown only once)
5. In `.env`: set `JIRA_AUTH_TYPE=basic` and fill in `JIRA_EMAIL`

**Jira Server / Data Center (self-hosted, e.g. your-company.jira.internal):**
1. Log in to Jira → click your avatar → **Profile**
2. In the left sidebar: **Personal Access Tokens** → **Create token**
3. Set a **name** and **expiration date**
4. Click **Create** → copy the token (shown only once)
5. In `.env`: set `JIRA_AUTH_TYPE=bearer` — no email required

### Step 3: Apply Minimum Permissions

Jira Cloud API tokens inherit the permissions of the user account. To minimize blast radius:
- Create a **dedicated service account** with read-only project permissions (preferred for teams)
- Or: use your personal account token but treat it as read-only — do not build write operations unless explicitly needed

### Step 4: IP Restriction (Jira Cloud Admins)

Jira Cloud admins can restrict API token usage by IP in **Organization Settings → Security → IP allowlists**. Ask your Jira admin to add the VPN egress IP to the allowlist.

For self-hosted Jira: configure IP restrictions at the reverse proxy level (nginx/Apache).

### Security Checklist

- [ ] Token has an expiration date
- [ ] Token label identifies its purpose
- [ ] You are connected to VPN — the whitelisted IP is the VPN egress
- [ ] Token is stored in `.env`, not hardcoded
- [ ] `.env` is in `.gitignore`

> See module [108 — Token & API Key Management](../108-token-api-key-management/about.md) for the full secret hygiene framework.

### Knowledge Check

*Q: Your token leaked in a public GitHub commit. What is the blast radius if you had IP restriction enabled with VPN IP?*

**A:** Very limited — the attacker has the token but cannot use it without access to your VPN. Revoke the token immediately at id.atlassian.com, then rotate. No VPN access = no Jira access.

---

## Part 3 — Building the Python CLI

**Time: 10 min**

### What We Will Build

We will set up a working directory at `work/470-task/`, fill in credentials, and run the CLI against a real Jira ticket.

### Step 1: Open the Work Folder

The directory `work/470-task/` is already prepared. Open it in your terminal:

```powershell
# Windows
cd work/470-task
```

```bash
# macOS / Linux
cd work/470-task
```

### Step 2: Install Dependencies

```powershell
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install requests python-dotenv
```

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

### Step 3: Fill In Your Credentials

Add your Jira credentials to the **project root `.env`** (the file at the root of this repository). The CLI uses `find_dotenv()` which searches from the current directory upward, so it will find the root `.env` whether you run from `work/470-task/` or from the module directory.

```dotenv
# ── Jira Server / Data Center (Bearer PAT) ────────────────────────────────────
JIRA_URL=https://your-company.jira.example.com
JIRA_API_TOKEN=your_personal_access_token_here
JIRA_AUTH_TYPE=bearer

# ── Atlassian Cloud (Basic Auth) ─────────────────────────────────────────────
# JIRA_URL=https://your-org.atlassian.net
# JIRA_EMAIL=your.email@company.com
# JIRA_API_TOKEN=your_atlassian_api_token_here
# JIRA_AUTH_TYPE=basic

# ── Test helpers (used by snapshot tests) ────────────────────────────────────
JIRA_TEST_KEY=PROJECT-1000
JIRA_SEARCH_JQL=assignee = currentUser() ORDER BY updated DESC
JIRA_WRITE_PROJECT=PROJECT
```

The root `.env` is already in `.gitignore` — it will never be committed. You can still keep a local `work/470-task/.env` for overrides; if it exists, it takes priority over the root file.

> **Why root `.env`?** A single credentials file is used by the CLI, the snapshot tests (mounted via `--env-file` in Docker), and any other tools in this workspace — no copying or syncing required.

### Step 4: Copy the CLI Script

Copy the script from the module tools folder:

```powershell
# Windows
Copy-Item ..\..\modules\470-jira-cli-access\tools\scripts\jira_cli.py .
```

```bash
# macOS / Linux
cp ../../modules/470-jira-cli-access/tools/scripts/jira_cli.py .
```

The full script source is at [tools/scripts/jira_cli.py](tools/scripts/jira_cli.py).

### Step 5: Verify the Setup

```bash
python jira_cli.py search --jql "project=YOUR_PROJECT AND status=Open" --max 5
```

Expected: a table of issues. If you see `401 Unauthorized`, your token is wrong or the email does not match the Atlassian account.

To test against the sample ticket, open `work/470-task/ticket.md`, find the issue key, then run:

```bash
python jira_cli.py get --key <ISSUE-KEY>
```

### Knowledge Check

*Q: What does `resp.raise_for_status()` do and why is it important?*

**A:** It raises an exception for any HTTP 4xx/5xx response, preventing the script from silently treating an error response as valid data.

---

## Part 4 — Connecting the CLI as an AI Skill

**Time: 5 min**

The AI agent skill descriptor lives at [tools/SKILL.md](tools/SKILL.md). It teaches the AI agent how to use the CLI — you do not need to repeat instructions every session. Attach it once and the agent reads it.

### How to attach the skill in VS Code

In your agent chat, reference the skill file:

```
@workspace modules/470-jira-cli-access/tools/SKILL.md
```

Or add it to your workspace's `.github/copilot-instructions.md`:

```markdown
## Jira CLI Skill
Read and follow: modules/470-jira-cli-access/tools/SKILL.md
```

### Demo workflow with the AI agent

Try this prompt after attaching the skill:

```
Show me all open P1 bugs in project PAYMENT assigned to me.
Download the first attachment from PAYMENT-42.
Summarize the description of PAYMENT-55 in 3 bullet points.
```

The agent will:
1. Run `jira_cli.py search` with the right JQL
2. Run `jira_cli.py attachments` then `download`
3. Run `jira_cli.py get --key PAYMENT-55` and summarize the output

**Context used:** only the formatted text output — not the full Jira API schema.

### Knowledge Check

*Q: Why does the SKILL.md list error codes like 401 and 403?*

**A:** So the agent can self-diagnose failures and guide the user to the right fix without asking the trainer — it is embedded troubleshooting knowledge.

---

## Part 5 — Security Checklist

**Time: 3 min**

Review before going to production:

- [ ] **Token scope:** uses minimum required permissions (read-only if possible)
- [ ] **Token expiry:** expiration date set in Atlassian token settings
- [ ] **IP restriction:** VPN egress IP is in Jira allowlist
- [ ] **VPN active:** always connect to VPN before running the CLI
- [ ] **`.env` protected:** listed in `.gitignore`, never committed
- [ ] **HTTPS enforced:** `validate_config()` rejects plain HTTP URLs
- [ ] **No token in logs:** script never prints `JIRA_API_TOKEN`
- [ ] **Token rotation:** scheduled reminder to rotate before expiry

> Run `git status` and confirm `.env` does not appear in untracked files. If it does, add it to `.gitignore` immediately and run `git rm --cached .env`.

---

## Part 6 — Port to Any Language

**Time: 5 min**

The pattern is always the same:
1. Read `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` from environment
2. HTTP GET to `{JIRA_URL}/rest/api/3/...` with Basic Auth
3. Parse JSON, format output

### Porting Equivalents

| Language | HTTP | Env vars | CLI args |
|----------|------|----------|----------|
| **Python** | `requests` | `python-dotenv` | `argparse` |
| **Node.js** | `axios` | `dotenv` | `commander` |
| **Go** | `net/http` | `godotenv` | `cobra` |
| **Java** | `OkHttp` | `dotenv-java` | `picocli` |
| **Bash** | `curl` | `source .env` | `getopts` / `$1` |

### Practical Task — Port with AI Assistance

Attach [tools/scripts/jira_cli.py](tools/scripts/jira_cli.py) to your AI agent and ask:

```
Port this Python Jira CLI to [your language of choice] keeping the same command structure:
  search, get, attachments, download
Use the same environment variable names for credentials.
```

Review that:
- Credentials come from env vars (not hardcoded)
- HTTPS-only check is preserved
- Token is never printed

### Knowledge Check

*Q: You ported to Node.js. Your colleague asks why you did not just use the official Jira MCP for VS Code. What is your answer?*

**A:** The official Jira MCP (Rovo) only supports Atlassian Cloud, not self-hosted instances. The CLI approach works with any Jira version, handles binary downloads, runs outside the context window to save tokens, and can be called from CI/CD pipelines without an IDE.

---

## Success Criteria

- ✅ `jira_cli.py search` returns a table of issues from your Jira project
- ✅ `jira_cli.py get --key <KEY>` shows issue details without errors
- ✅ `.env` is listed in `.gitignore` and does not appear in `git status`
- ✅ Token has an expiration date and you know the VPN IP it is restricted to
- ✅ AI agent uses the CLI via `tools/SKILL.md` without manual prompting
- ✅ You can explain the difference between CLI and MCP for binary file handling

## Understanding Check

1. **Why does CLI save tokens compared to MCP?** — CLI output is plain text; MCP loads full tool schemas and all responses into the context window.
2. **What happens if you do not set a token expiry?** — The token stays valid indefinitely; if it leaks, it can be used forever without rotation.
3. **Why whitelist the VPN IP instead of your home IP?** — The VPN egress is a stable, shared IP you control; whitelisting it means a leaked token is unusable without VPN access.
4. **What is the SKILL.md file for?** — It teaches the AI agent how to invoke the CLI, what commands are available, and how to handle errors — without manual prompting each session.
5. **Why must `JIRA_URL` start with `https://`?** — Plain HTTP transmits credentials in cleartext; the CLI rejects it to prevent accidental token exposure.
6. **How does the CLI handle binary attachments differently from MCP?** — The CLI streams bytes directly to disk via chunked download; MCP would need to base64-encode the binary into JSON.
7. **What is the first thing to do if your token leaks?** — Revoke it immediately at id.atlassian.com, then generate a new one and update `.env`.

## Troubleshooting

| Problem | Likely cause | Solution |
|---------|-------------|----------|
| `401 Unauthorized` | Token invalid or email mismatch | Re-check `.env`; regenerate token at id.atlassian.com |
| `403 Forbidden` | Token lacks permissions | Use account with at least Browse Projects permission |
| `400 Bad Request` | Invalid JQL | Fix the query; test JQL in Jira UI first |
| `Connection refused` | Wrong `JIRA_URL` | Verify URL; check VPN is connected |
| `ModuleNotFoundError: requests` | venv not activated | Activate the virtual environment first |
| `.env` not found | Missing file | Copy from `tools/.env.example` and fill in values |

## Part 7 — Snapshot Testing the CLI

**Time: 10 min**

Module [091 — CLI Testing](../091-cli-testing/about.md) introduced snapshot testing. Here we apply it to the Jira CLI.

### How It Works

1. Scenario files (`test/scenarios/*.md`) describe commands to run
2. `run-tests.ps1` builds a Docker image, mounts the scenarios, and runs them
3. Output is written back into the `.md` files — you review and commit the snapshot

Credentials come from the **root `.env`** via Docker `--env-file` — never baked into the image.

### Step 1: Add Test Env Vars to Root `.env`

Make sure these exist in your root `.env`:

```dotenv
JIRA_TEST_KEY=YOUR-PROJECT-123      # a real issue key for read tests
JIRA_SEARCH_JQL=project = YOUR-PROJECT AND status = Open
JIRA_WRITE_PROJECT=YOUR-PROJECT     # for create test (needs write token)
```

### Step 2: Run the Tests

From the project root:

```powershell
& modules/470-jira-cli-access/test/run-tests.ps1
```

First run builds the Docker image (`jira-cli-test`) — takes ~1-2 minutes. Subsequent runs with `-NoBuild` are fast:

```powershell
& modules/470-jira-cli-access/test/run-tests.ps1 -NoBuild
```

### Step 3: Review and Commit

```powershell
git diff modules/470-jira-cli-access/test/scenarios/
```

If the output looks correct, commit as the new golden snapshot. ⚠️ **Review carefully** — output may contain issue keys or Jira data. Redact or omit sensitive lines before committing.

### How the Reuse Works

| Component reused | From module | What it does |
|-----------------|-------------|-------------|
| `run-scenarios.sh` | 091-cli-testing | Engine that processes `.md` scenario files inside Docker |
| Dockerfile pattern | 091-cli-testing | Generated on the fly from `python:3.12-slim` base |
| Scenario format | 091-cli-testing | `` > `command` `` lines → captured output |
| `run-tests.ps1` | 470 (new) | Wrapper that adds `--env-file` for secrets + copies `jira_cli.py` |

---

## Next Steps

- [091 — CLI Snapshot Testing](../091-cli-testing/about.md) — full snapshot testing framework
- [106 — FastMCP: Custom MCP Server](../106-fastmcp-custom-mcp-server/about.md) — when you need a full MCP tool with real-time agent integration
- [108 — Token & API Key Management](../108-token-api-key-management/about.md) — deeper dive into secrets hygiene
