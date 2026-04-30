# Jira CLI Access via MCPyrex Python Script

> **Module 470** | Duration: 25-35 min | Python + Jira REST API + AI skill

---

## What We'll Build

| Component | Location | Purpose |
|-----------|----------|---------|
| `jira_cli.py` | `work/470-jira-cli/` | CLI script for querying Jira |
| `.env` | `work/470-jira-cli/` | Credentials (never committed) |
| `skill.md` | `modules/470-jira-cli-access/` | AI agent descriptor |

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

Before creating the token, know which IP you'll whitelist:

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

1. Go to: [https://id.atlassian.com/manage-api-tokens](https://id.atlassian.com/manage-api-tokens)
2. Click **Create API token**
3. Fill in:
   - **Label:** `jira-cli-dev` (descriptive name)
   - **Expiration:** set a date — **never leave it "no expiry"**; 90 days is reasonable for dev work
4. Click **Create** → copy the token immediately (shown only once)

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

*Q: Your token leaked in a public GitHub commit. What's the blast radius if you had IP restriction enabled with VPN IP?*

**A:** Very limited — the attacker has the token but cannot use it without access to your VPN. Revoke the token immediately at id.atlassian.com, then rotate. No VPN access = no Jira access.

---

## Part 3 — Building the Python CLI

**Time: 10 min**

### Project Setup

```powershell
# Windows
New-Item -ItemType Directory -Path work/470-jira-cli
cd work/470-jira-cli
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install requests python-dotenv
```

```bash
# macOS / Linux
mkdir -p work/470-jira-cli && cd work/470-jira-cli
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

### `.gitignore`

Create `work/470-jira-cli/.gitignore`:

```
.env
.venv/
__pycache__/
downloads/
*.pyc
```

### `.env`

Create `work/470-jira-cli/.env`:

```
JIRA_URL=https://your-org.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your_api_token_here
```

### `jira_cli.py`

Create `work/470-jira-cli/jira_cli.py`:

```python
#!/usr/bin/env python3
"""Jira CLI — query Jira issues, fetch details, download attachments."""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")


def validate_config():
    if not JIRA_URL.startswith("https://"):
        sys.exit("ERROR: JIRA_URL must start with https://")
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        sys.exit("ERROR: JIRA_EMAIL and JIRA_API_TOKEN must be set in .env")


def auth():
    return (JIRA_EMAIL, JIRA_API_TOKEN)


def api_get(path, params=None):
    url = f"{JIRA_URL}/rest/api/3{path}"
    resp = requests.get(url, auth=auth(), params=params, timeout=15)
    if resp.status_code == 401:
        sys.exit("ERROR: 401 Unauthorized — check JIRA_EMAIL and JIRA_API_TOKEN")
    if resp.status_code == 403:
        sys.exit("ERROR: 403 Forbidden — token lacks permission for this operation")
    resp.raise_for_status()
    return resp.json()


def format_table(rows, headers):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))


def cmd_search(args):
    data = api_get("/search", params={
        "jql": args.jql,
        "maxResults": args.max,
        "fields": "summary,status,assignee,priority"
    })
    issues = data.get("issues", [])
    if not issues:
        print("No issues found.")
        return
    if args.format == "json":
        print(json.dumps(issues, indent=2))
    elif args.format == "plain":
        for i in issues:
            print(f"{i['key']}: {i['fields']['summary']}")
    else:
        rows = []
        for i in issues:
            f = i["fields"]
            rows.append([
                i["key"],
                f["summary"][:60],
                f.get("status", {}).get("name", "-"),
                (f.get("assignee") or {}).get("displayName", "Unassigned"),
            ])
        format_table(rows, ["KEY", "SUMMARY", "STATUS", "ASSIGNEE"])


def cmd_get(args):
    data = api_get(f"/issue/{args.key}")
    f = data["fields"]
    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        fields = [
            ("Key", data["key"]),
            ("Summary", f.get("summary", "-")),
            ("Status", f.get("status", {}).get("name", "-")),
            ("Assignee", (f.get("assignee") or {}).get("displayName", "Unassigned")),
            ("Reporter", (f.get("reporter") or {}).get("displayName", "-")),
            ("Priority", (f.get("priority") or {}).get("name", "-")),
            ("Created", f.get("created", "-")[:10]),
            ("Updated", f.get("updated", "-")[:10]),
            ("Labels", ", ".join(f.get("labels", [])) or "-"),
            ("Comments", str(f.get("comment", {}).get("total", 0))),
        ]
        for label, value in fields:
            print(f"{label:<12}: {value}")
        desc = f.get("description")
        if desc and isinstance(desc, dict):
            # Atlassian Document Format — extract plain text
            content = desc.get("content", [])
            texts = []
            for block in content:
                for node in block.get("content", []):
                    if node.get("type") == "text":
                        texts.append(node.get("text", ""))
            if texts:
                print(f"\nDescription:\n{''.join(texts)}")


def cmd_attachments(args):
    data = api_get(f"/issue/{args.key}", params={"fields": "attachment"})
    attachments = data["fields"].get("attachment", [])
    if not attachments:
        print("No attachments found.")
        return
    rows = [[a["filename"], a["mimeType"], f"{a['size']:,} bytes"] for a in attachments]
    format_table(rows, ["FILENAME", "TYPE", "SIZE"])


def cmd_download(args):
    data = api_get(f"/issue/{args.key}", params={"fields": "attachment"})
    attachments = data["fields"].get("attachment", [])
    target = next((a for a in attachments if a["filename"] == args.filename), None)
    if not target:
        sys.exit(f"ERROR: Attachment '{args.filename}' not found on {args.key}")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / args.filename
    resp = requests.get(target["content"], auth=auth(), stream=True, timeout=30)
    resp.raise_for_status()
    with open(dest, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    print(f"Downloaded: {dest} ({dest.stat().st_size:,} bytes)")


def main():
    validate_config()
    parser = argparse.ArgumentParser(description="Jira CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search issues with JQL")
    p_search.add_argument("--jql", required=True)
    p_search.add_argument("--format", choices=["table", "json", "plain"], default="table")
    p_search.add_argument("--max", type=int, default=20)

    p_get = sub.add_parser("get", help="Get issue details")
    p_get.add_argument("--key", required=True)
    p_get.add_argument("--format", choices=["table", "json", "plain"], default="table")

    p_att = sub.add_parser("attachments", help="List attachments on an issue")
    p_att.add_argument("--key", required=True)

    p_dl = sub.add_parser("download", help="Download an attachment")
    p_dl.add_argument("--key", required=True)
    p_dl.add_argument("--filename", required=True)
    p_dl.add_argument("--output", default="./downloads")

    args = parser.parse_args()
    dispatch = {"search": cmd_search, "get": cmd_get, "attachments": cmd_attachments, "download": cmd_download}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
```

### Verify the Setup

```bash
python jira_cli.py search --jql "project=YOUR_PROJECT AND status=Open" --max 5
```

Expected: a table of issues. If you see `401 Unauthorized`, your token is wrong or the email doesn't match the Atlassian account.

### Knowledge Check

*Q: What does `resp.raise_for_status()` do and why is it important?*

**A:** It raises an exception for any HTTP 4xx/5xx response, preventing the script from silently treating an error response as valid data.

---

## Part 4 — Connecting the CLI as an AI Skill

**Time: 5 min**

The `skill.md` file (at `modules/470-jira-cli-access/skill.md`) is a descriptor that teaches the AI agent how to use the CLI. You don't need to write prompts every time — you attach the skill once and the agent reads it.

### How to attach the skill in VS Code

In your agent chat, reference the skill file:

```
@workspace /path/to/modules/470-jira-cli-access/skill.md
```

Or add it to your workspace's `.github/copilot-instructions.md`:

```markdown
## Jira CLI Skill
Read and follow: modules/470-jira-cli-access/skill.md
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

*Q: Why does the skill.md list error codes like 401 and 403?*

**A:** So the agent can self-diagnose failures and guide the user to the right fix without asking the trainer — it's embedded troubleshooting knowledge.

---

## Part 5 — Security Checklist

**Time: 3 min**

Review before going to production:

- [ ] **Token scope:** uses minimum required permissions (read-only if possible)
- [ ] **Token expiry:** expiration date set in Atlassian token settings
- [ ] **IP restriction:** VPN egress IP is in Jira's allowlist
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

Ask your AI agent:

```
I have this Python Jira CLI script (paste jira_cli.py).
Port it to [your language of choice] keeping the same command structure:
  search, get, attachments, download
Use the same environment variable names for credentials.
```

The agent will produce a functionally equivalent CLI. Review that:
- Credentials come from env vars (not hardcoded)
- HTTPS-only check is preserved
- Token is never printed

### Knowledge Check

*Q: You ported to Node.js. Your colleague asks why you didn't just use the official Jira MCP for VS Code. What's your answer?*

**A:** The official Jira MCP (Rovo) only supports Atlassian Cloud, not self-hosted instances. The CLI approach works with any Jira version, handles binary downloads, runs outside the context window to save tokens, and can be called from CI/CD pipelines without an IDE.

---

## Module Summary

| What you built | Why it matters |
|----------------|---------------|
| Python Jira CLI with 4 commands | Reusable tool, no MCP server needed |
| Scoped API token with expiry + IP restriction | Minimal blast radius if token leaks |
| VPN-first workflow | Token useless without VPN access |
| `skill.md` descriptor | AI agent uses CLI without manual prompting |
| Language-portable pattern | Team can replicate in any stack |

**Next modules:**
- [475 — mcpyrex: JavaScript Execution Engine](../400-installing-mcpyrex-mcp-python-toolbox/about.md)
- [106 — FastMCP: Custom MCP Server](../106-fastmcp-custom-mcp-server/about.md) — when you do need a proper MCP tool
