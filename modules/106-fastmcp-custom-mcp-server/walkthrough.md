# Building Custom MCP Servers with FastMCP - Hands-on Walkthrough

In this module you will explore five real-world approaches to connecting AI to a self-hosted tool, understand the security trade-offs of each, and then build your own MCP server using FastMCP. By the end you will have a working server that wraps a REST API, loads credentials from a `.env` file, and is connected to your IDE.

The running example throughout this module is **self-hosted Jira** — a common enterprise scenario where the official Atlassian MCP only supports Jira Cloud.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## Part 1: Five Approaches — The Decision Map

Before writing any code, it helps to understand all your options. Each approach has a different risk profile, effort level, and maintenance cost.

### Approach 1 — Third-Party Community MCP (⚠️ Risky)

You find an open-source MCP server on GitHub or the [Docker Hub MCP catalog](https://hub.docker.com/mcp) that someone already built for Jira. You add it to your `mcp.json` and it works immediately.

**Why this is dangerous:**

Connecting an unreviewed MCP server is equivalent to installing an unknown program from the internet. Once running:

- The server has access to **your authentication token** — if it exfiltrates it, an attacker can act on behalf of your account.
- It can read files, make API calls, or do anything your token allows.
- No amount of "it looks fine on GitHub" replaces a professional security review.

**What to do instead:** If your team wants to use a community MCP, route it through your **Security team** for a code review first. The token exposure risk alone justifies this step.

> Covered in detail in module [108 — Token & API Key Management](../108-token-api-key-management/about.md).

---

### Approach 2 — Official Vendor MCP (✅ Safest when available)

Many tools now ship their own MCP server. These are reviewed by the vendor, use proper OAuth or scoped tokens, and are the safest option.

**Jira example:** Atlassian's Rovo MCP works great — but only for **Jira Cloud**. If your company runs its own Jira instance, this option is not available.

**The pattern to recognize:** For any tool you want to connect, first check whether the vendor provides an official HTTP-based MCP server. Many tools embed one directly into their product. If so, use it.

> We used this pattern when connecting to GitHub in module [105 — MCP GitHub Integration](../105-mcp-github-integration-issues/about.md). The GitHub MCP server is HTTP-based, uses your PAT, and is maintained by GitHub themselves.

---

### Approach 3 — Elitea Platform (✅ Enterprise option)

If your organization uses the Elitea platform (available to EPAM employees), you can create no-code agents on Elitea and connect them to your IDE via MCP. Elitea handles authentication, security, and infrastructure.

> Full details in module [165 — Elitea Platform MCP Integration](../165-elitea-platform-mcp-integration/about.md). This approach is out of scope for this module.

---

### Approach 4 — Python/CLI Tool as a Skill (✅ Fully controlled)

You write a Python script or CLI tool that calls the Jira REST API using your own token (injected via `.env`). You then package it as an AI Skill — a reusable function the AI can call directly.

**Key advantages:**
- Your token never leaves your machine.
- You control exactly what operations are allowed.
- You can use open-source MCP code as a **learning reference** rather than running it directly.

**How to use the Docker Hub MCP catalog as a reference:**

Visit [hub.docker.com/mcp](https://hub.docker.com/mcp) to browse open-source MCP implementations. Each entry links to the source repository. Find a Jira (or similar) MCP, read the source code to understand the API calls it makes, then implement only the operations you need — with security in mind.

When you give the source code to your AI agent, ask it to:
1. Identify all external API calls and what data they send.
2. Flag any security concerns (token handling, data logging, network calls).
3. Implement a minimal, KISS version with only the endpoints you need.

> See module [076 — Advanced Skills Management System](../076-skills-management-system/about.md) for the Skills packaging pattern.

---

### Approach 5 — FastMCP Wrapper (✅ Best balance of control and convenience)

This is the **main focus of this module**.

FastMCP lets you write a Python server that:
- Exposes any REST API as MCP tools.
- Reads credentials securely from environment variables.
- Integrates with VS Code and Cursor via `mcp.json`.
- Runs locally as a subprocess — no cloud, no third party, no token exposure.

The rest of this walkthrough builds this server step by step.

---

## Part 2: FastMCP — What It Is and Why It Matters

FastMCP is the standard Python framework for building MCP servers. It was created by the team at Prefect, incorporated into the official MCP Python SDK in 2024, and today powers approximately 70% of MCP servers across all languages.

**Why FastMCP instead of the raw MCP SDK?**

| Raw MCP SDK | FastMCP |
|---|---|
| Manual JSON schema definition | Auto-generated from Python type hints |
| Verbose boilerplate per tool | `@mcp.tool` decorator |
| Manual transport setup | One-liner `mcp.run()` |
| No validation | Pydantic validation built-in |

With FastMCP, the full lifecycle looks like this:

```python
from fastmcp import FastMCP

mcp = FastMCP("My Jira MCP")

@mcp.tool
def get_issue(issue_key: str) -> dict:
    """Fetch a Jira issue by its key (e.g. PROJ-123)."""
    # your API call here
    ...

if __name__ == "__main__":
    mcp.run()
```

The `@mcp.tool` decorator does three things automatically:
1. Generates the JSON schema for the tool from your Python type hints.
2. Registers the tool with the MCP server.
3. Validates inputs before calling your function.

---

## Part 3: Setting Up the Project

### Step 1 — Create the project folder

Create a new folder for your MCP server:

```
c:/workspace/jira-mcp/          (Windows)
~/workspace/jira-mcp/           (macOS/Linux)
```

Inside it, create these files (you will fill them in during the next steps):

```
jira-mcp/
├── server.py
├── .env
├── .env.example
├── .gitignore
└── requirements.txt
```

### Step 2 — Set up `.gitignore`

The `.env` file contains your API token and must **never** be committed to Git.

Create `.gitignore`:

```
.env
__pycache__/
*.pyc
.venv/
```

### Step 3 — Create `.env.example`

This file documents what variables are needed without containing real values. Commit this file.

```env
JIRA_BASE_URL=https://jira.your-company.com
JIRA_TOKEN=your_personal_access_token_here
```

### Step 4 — Create your real `.env`

Copy `.env.example` to `.env` and fill in your actual values:

```env
JIRA_BASE_URL=https://jira.your-company.com
JIRA_TOKEN=eyJ...your_real_token...
```

### Step 5 — Install dependencies

Create `requirements.txt`:

```
fastmcp
httpx
python-dotenv
```

Then install:

- **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

- **macOS/Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

**What we just installed:**

| Package | Purpose |
|---|---|
| `fastmcp` | MCP server framework |
| `httpx` | Async HTTP client for calling the Jira REST API |
| `python-dotenv` | Load `.env` file into environment variables |

---

## Part 4: Building the FastMCP Server

### Step 6 — Write `server.py`

Open `server.py` in your IDE and add the following code. Read each section carefully — the comments explain every decision.

```python
import os
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

# --- Load credentials from .env ---
# This MUST happen before reading any environment variables.
# python-dotenv reads the .env file and sets os.environ entries.
load_dotenv()

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")

if not JIRA_BASE_URL or not JIRA_TOKEN:
    raise RuntimeError(
        "JIRA_BASE_URL and JIRA_TOKEN must be set in your .env file."
    )

# --- Create the MCP server ---
mcp = FastMCP(
    "Jira MCP",
    instructions=(
        "Use this server to interact with the self-hosted Jira instance. "
        "Always use issue keys like PROJ-123 when referencing issues."
    ),
)

# --- Shared HTTP client factory ---
# We create a fresh client per call so the server stays stateless.
def _jira_client() -> httpx.Client:
    return httpx.Client(
        base_url=JIRA_BASE_URL,
        headers={
            "Authorization": f"Bearer {JIRA_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=10.0,
    )

# --- Tools ---

@mcp.tool
def get_issue(issue_key: str) -> dict:
    """
    Fetch a Jira issue by its key.

    Args:
        issue_key: The Jira issue key, e.g. PROJ-123.

    Returns:
        A dictionary with the issue summary, status, assignee, and description.
    """
    with _jira_client() as client:
        response = client.get(f"/rest/api/2/issue/{issue_key}")
        response.raise_for_status()
        data = response.json()
        fields = data.get("fields", {})
        return {
            "key": data["key"],
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name"),
            "assignee": (fields.get("assignee") or {}).get("displayName"),
            "description": fields.get("description"),
        }


@mcp.tool
def search_issues(jql: str, max_results: int = 20) -> list[dict]:
    """
    Search Jira issues using JQL (Jira Query Language).

    Args:
        jql: A JQL query string, e.g. 'project = PROJ AND status = Open'.
        max_results: Maximum number of results to return (default 20, max 50).

    Returns:
        A list of matching issues with key, summary, and status.
    """
    max_results = min(max_results, 50)  # Enforce a hard cap for safety
    with _jira_client() as client:
        response = client.post(
            "/rest/api/2/search",
            json={"jql": jql, "maxResults": max_results, "fields": ["summary", "status"]},
        )
        response.raise_for_status()
        issues = response.json().get("issues", [])
        return [
            {
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"],
            }
            for issue in issues
        ]


@mcp.tool
def create_issue(project_key: str, summary: str, description: str = "", issue_type: str = "Task") -> dict:
    """
    Create a new Jira issue.

    Args:
        project_key: The project key, e.g. PROJ.
        summary: Short title of the issue.
        description: Detailed description (optional).
        issue_type: Issue type name, e.g. Task, Bug, Story (default: Task).

    Returns:
        A dict with the key and URL of the created issue.
    """
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type},
        }
    }
    with _jira_client() as client:
        response = client.post("/rest/api/2/issue", json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "key": data["key"],
            "url": f"{JIRA_BASE_URL}/browse/{data['key']}",
        }


@mcp.tool
def add_comment(issue_key: str, comment: str) -> dict:
    """
    Add a comment to an existing Jira issue.

    Args:
        issue_key: The Jira issue key, e.g. PROJ-123.
        comment: The comment text to add.

    Returns:
        A dict with the comment ID and author.
    """
    with _jira_client() as client:
        response = client.post(
            f"/rest/api/2/issue/{issue_key}/comment",
            json={"body": comment},
        )
        response.raise_for_status()
        data = response.json()
        return {
            "id": data["id"],
            "author": data.get("author", {}).get("displayName"),
        }


# --- Entry point ---
if __name__ == "__main__":
    mcp.run()
```

**Security checkpoints — built into this implementation:**

| Risk | Mitigation |
|---|---|
| Token exposed in code | Token read from `os.environ`, never hardcoded |
| Token committed to Git | `.env` is in `.gitignore`; `.env.example` has no real values |
| Unbounded API results | `max_results` capped at 50 in `search_issues` |
| Error details leaked | `raise_for_status()` raises a clean `httpx.HTTPStatusError` |
| Stateful HTTP connections | Fresh `httpx.Client` per call — no state leakage between tool calls |

---

## Part 5: Connecting to VS Code

### Step 7 — Add to `mcp.json`

Open your VS Code MCP configuration file. Its location depends on your setup:

- **User-level** (applies to all workspaces): `%APPDATA%\Code\User\mcp.json` (Windows) or `~/.config/Code/User/mcp.json` (macOS/Linux)
- **Workspace-level** (this project only): `.vscode/mcp.json` in your workspace root

Add the following entry inside the `mcpServers` object:

```json
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["c:/workspace/jira-mcp/server.py"],
      "env": {
        "JIRA_BASE_URL": "${env:JIRA_BASE_URL}",
        "JIRA_TOKEN": "${env:JIRA_TOKEN}"
      }
    }
  }
}
```

> **Windows note:** Use forward slashes in the path, or escape backslashes: `c:\\workspace\\jira-mcp\\server.py`.

> **Alternative:** Instead of `${env:...}` variables, you can rely on `load_dotenv()` in `server.py` reading the `.env` file automatically. In that case, remove the `"env"` block from `mcp.json` and let your Python script handle it.

### Step 8 — Verify the connection

1. Restart VS Code (or reload the MCP configuration via the Command Palette: **MCP: Restart All Servers**).
2. Open a new GitHub Copilot chat in Agent Mode.
3. Type: `What MCP tools do you have available?`
4. You should see `get_issue`, `search_issues`, `create_issue`, and `add_comment` listed.
5. Test with: `Search for open issues in project PROJ using the Jira MCP`

---

## Part 6: Using Open-Source MCPs as a Reference

Before building a FastMCP server from scratch, it is worth checking whether someone has already solved your problem. The [Docker Hub MCP catalog](https://hub.docker.com/mcp) lists hundreds of open-source MCP servers with their source repositories.

**How to use it safely:**

1. **Find** a community MCP for your tool (e.g., search for "jira" on Docker Hub).
2. **Open the source repository** — do not run anything yet.
3. **Give the source code to your AI agent** with this prompt:

   ```
   Review this MCP server code and tell me:
   1. All external network calls it makes and what data is sent.
   2. How it handles authentication tokens (is there any logging or forwarding?).
   3. Any security concerns (OWASP Top 10 items, hardcoded secrets, eval, shell injection).
   4. The minimum set of API calls I need to implement to get the main functionality.
   
   After the review, implement a minimal FastMCP version with only the essential tools,
   following secure coding practices.
   ```

4. **Review the AI's findings** before proceeding.
5. **Implement your own version** based on what you learned — you control every line.

This gives you the knowledge embedded in the open-source project without taking on its dependencies or trusting its code blindly.

---

## Success Criteria

- ✅ FastMCP server created with at least 2 working tools
- ✅ Token loaded from `.env`, never present in `server.py`
- ✅ `.env` excluded from Git via `.gitignore`
- ✅ `.env.example` committed with placeholder values
- ✅ Server listed in `mcp.json` and visible in VS Code Agent Mode
- ✅ Able to call a tool from the AI chat (`search_issues` or `get_issue`)
- ✅ Able to explain the difference between all 5 integration approaches

---

## Understanding Check

1. **Why should you never copy an unreviewed community MCP directly into `mcp.json`?**  
   Because the MCP server process has full access to your authentication token. A malicious or misconfigured server can exfiltrate it, letting attackers act on your behalf.

2. **What does the `@mcp.tool` decorator do in FastMCP?**  
   It registers the function as an MCP tool, auto-generates its JSON schema from Python type hints, and enables input validation before your function is called.

3. **Why is `load_dotenv()` called at the top of `server.py`, before anything else?**  
   Because `os.environ.get()` reads environment variables at call time. If `load_dotenv()` runs after those calls, the `.env` values would not be loaded yet and the variables would be `None`.

4. **Why does `search_issues` cap `max_results` at 50?**  
   To prevent a prompt injection or accidental query from returning thousands of results, overloading the LLM context window or the Jira API.

5. **What is the difference between using `${env:JIRA_TOKEN}` in `mcp.json` and letting `load_dotenv()` read the `.env` file?**  
   `${env:...}` reads from shell environment variables that must be set before VS Code starts. `load_dotenv()` reads from a `.env` file in the project directory — more convenient for local development, but the `.env` file must be excluded from Git.

6. **When is FastMCP a better choice than packaging a Python script as a CLI skill?**  
   When you need multiple operations (tools) and want them discoverable by the AI through the MCP protocol. A CLI skill is better for a single operation called deterministically; FastMCP is better when you want the AI to choose which operation to call based on context.

7. **How does the Docker Hub MCP catalog help you build a custom FastMCP server without running third-party code?**  
   You use the source code as a reference to understand which API endpoints your target tool exposes, then implement only the operations you need — in your own code, with your own security controls.

---

## Troubleshooting

**Server does not appear in VS Code after adding to `mcp.json`:**
- Reload MCP configuration: open Command Palette and run **MCP: Restart All Servers**.
- Check that the Python path in `"command"` matches your virtual environment's Python.
- Use the absolute path to `server.py` in `"args"`.

**`RuntimeError: JIRA_BASE_URL and JIRA_TOKEN must be set`:**
- Make sure `.env` exists in the same folder as `server.py`.
- Verify the `.env` file has no extra spaces around `=`, e.g. `JIRA_TOKEN=abc` not `JIRA_TOKEN = abc`.

**`httpx.HTTPStatusError: 401 Unauthorized`:**
- Your token may have expired or have insufficient permissions. Generate a new Personal Access Token in Jira: **Profile → Personal Access Tokens → Create token**.
- Ensure the token has at least **read** permissions for the relevant projects.

**`httpx.ConnectError` or connection timeout:**
- Verify `JIRA_BASE_URL` is correct and reachable from your machine (try `curl $JIRA_BASE_URL/rest/api/2/serverInfo` in terminal).
- Check if your network requires a VPN to reach the Jira instance.

**Tool returns `None` for `description` or `assignee`:**
- This is expected — not all Jira issues have an assignee or a description. The server returns `None` rather than failing.

---

## Next Steps

Continue with:

- [108 — Token & API Key Management](../108-token-api-key-management/about.md) — go deeper on `.env` patterns, key rotation, and pre-commit checks
- [140 — Advanced MCP Integration in a PoC](../140-advanced-mcp-integration-in-poc/about.md) — add an MCP interface to a full application you build
- [165 — Elitea Platform MCP Integration](../165-elitea-platform-mcp-integration/about.md) — explore the enterprise cloud alternative to local FastMCP servers
