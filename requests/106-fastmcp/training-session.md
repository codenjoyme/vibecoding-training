# Training Session: Module 106 — Building Custom MCP Servers with FastMCP

**Date:** 2026-04-22  
**Mode:** Self-run (agent played both trainer and learner roles)  
**Purpose:** Validate module content, find inconsistencies, verify practical exercises work

---

## Session Log

---

**Trainer:** 🧠 **Reminder:** This training is a dialogue, not a slideshow. Ask about anything that's unclear right here in the chat. The more questions you ask, the more you'll learn.

We're starting **Module 106 — Building Custom MCP Servers with FastMCP**. This module emerged from a real question: "What's the best way to connect AI to self-hosted Jira?" There are 5 answers, and we'll go through all of them.

Let's start with Part 1 — the decision map.

---

## Part 1: Five Approaches — The Decision Map

**Trainer:** Before writing a single line of code, you should know all the options. Here is the full map:

1. **Community MCP** — someone else built it, plug and play (⚠️ risky)
2. **Official vendor MCP** — the tool vendor built it (✅ safe, but may not exist for your tool)
3. **Elitea platform** — managed cloud agents (✅ enterprise)
4. **Python/CLI skill** — you write it, you own it (✅ full control)
5. **FastMCP wrapper** — Python server wrapping any REST API (✅ best balance)

The key insight: the first question you should always ask is **"who wrote this code and who has access to my token?"**

Tell me — in your current team, do you use any MCP servers right now? And did anyone ask "is this safe?" before connecting them?

**Learner:** We connected a few from GitHub, nobody asked about security. Honestly we just copied commands from the README.

**Trainer:** That's completely typical, and it's exactly the problem. When you connect an MCP server, that server process runs on your machine and receives every request you make — including your authentication token. It's like handing your apartment keys to a stranger and saying "you seem friendly."

The README says nothing about whether the server phones home with your token. The only way to know is to read the source code — or have your security team do it.

What would make your team actually take that step? Is there a process for this, or is it ad-hoc?

**Learner:** It's ad-hoc. We'd need a policy.

**Trainer:** Exactly. And that's what Approach 1 in the module addresses: the recommendation isn't "never use community MCPs" — it's "route them through your Security team before connecting." The token exposure risk is real enough that it needs a formal gate.

OK, one more angle on this. If you were choosing between Approach 1 (community, risky) and Approach 2 (official vendor), and the vendor's MCP only works for cloud but you have self-hosted — what would you actually do?

**Learner:** I guess we'd have to build something ourselves. Or use Approach 4.

**Trainer:** Right. And that's the whole point of this module — showing you that "build it yourself" is not scary at all with FastMCP. You get exactly the control you need in about 50 lines of Python.

Ready to move to Part 2 where we get into what FastMCP actually is?

---

## Part 2: FastMCP — What It Is and Why It Matters

**Trainer:** FastMCP is the standard Python library for building MCP servers. It was incorporated into the official MCP Python SDK in 2024 and today powers about 70% of MCP servers across all languages. One decorator — `@mcp.tool` — and your Python function becomes an MCP tool with auto-generated JSON schema, input validation, and error handling.

Here's the minimal example:

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

That's the entire server. FastMCP handles the protocol details. You focus on your logic.

Here's an interesting contrast: the raw MCP Python SDK requires you to manually write JSON schema for every parameter. If your function has 5 parameters, you write 5 schema definitions by hand. With FastMCP, the schema is generated from your Python type hints automatically. Adding `name: str` is the schema.

What's your reaction to this? Does it remind you of anything else in Python?

**Learner:** It looks like FastAPI. The decorators, the type hints doing the heavy lifting.

**Trainer:** Exactly right! FastAPI does the same thing for HTTP routes — you annotate your function and FastAPI generates the OpenAPI schema. FastMCP applies the same pattern to MCP tools. The co-inventor of FastMCP was inspired by FastAPI. If you already know FastAPI, you'll feel at home in 10 minutes.

Which actually raises an interesting question: if someone on your team knows FastAPI, they could build an MCP server almost without learning anything new. Have you used FastAPI or similar?

**Learner:** I've used it for internal APIs, yes.

**Trainer:** Perfect. Then Part 4 (where we write the actual server) will feel very familiar. The mental model is identical: function + decorator + type hints = tool definition.

One more thing to understand about FastMCP before we move on: the `instructions` parameter. You pass a string describing what your server does, and the AI model uses it to understand when to call which tools. Think of it as a system prompt for your MCP server.

Ready to set up the project in Part 3?

---

## Part 3: Setting Up the Project

**Trainer:** Let's create the folder structure. Navigate to your workspace and create:

```
c:/workspace/jira-mcp/          (Windows)
~/workspace/jira-mcp/           (macOS/Linux)
```

We need four files before writing any server code:

```
jira-mcp/
├── server.py        ← we'll write this in Part 4
├── .env             ← your real token (NEVER committed)
├── .env.example     ← template with placeholder values (committed)
├── .gitignore       ← excludes .env
└── requirements.txt ← fastmcp, httpx, python-dotenv
```

**Why this structure before any code?**

Because the #1 way tokens get leaked is: someone writes the token directly in the script, tests it, and commits. The gitignore-first discipline prevents that. You set up the guard rails before you even have a token to protect.

Create `.gitignore` first:

```
.env
__pycache__/
*.pyc
.venv/
```

Then `.env.example`:

```env
JIRA_BASE_URL=https://jira.your-company.com
JIRA_TOKEN=your_personal_access_token_here
```

Then install dependencies:

```powershell
pip install fastmcp httpx python-dotenv
```

_[Practical note from self-run: `pip install fastmcp` works with the system Python. FastMCP 3.2.4 installed successfully. `python -c "import ast; ast.parse(open('server.py').read()); print('Syntax OK')"` confirmed the server.py syntax is valid.]_

The `.env.example` is important for a different reason than `.gitignore`. `.gitignore` protects the secret. `.env.example` **documents the interface** — a teammate cloning this project knows exactly what variables to set without reading the source code.

Does your team have a convention for documenting required environment variables, or is it usually "ask the person who set it up"?

**Learner:** Usually the second option, unfortunately.

**Trainer:** Common problem. `.env.example` in git is the minimal solution with zero overhead. Any newer team member can `cp .env.example .env` and be guided directly to what they need.

Ready to move to Part 4 and write the actual FastMCP server?

---

## Part 4: Building the FastMCP Server

**Trainer:** Now the fun part. We're going to write `server.py` — a complete FastMCP server wrapping Jira's REST API.

The server has 4 tools: `get_issue`, `search_issues`, `create_issue`, `add_comment`.

The structure of `server.py` is always the same:
1. Load credentials from `.env`
2. Create the `FastMCP` instance
3. Define a shared HTTP client factory
4. Decorate your functions with `@mcp.tool`
5. Call `mcp.run()` in `__main__`

Here's the credential loading section — note the early validation:

```python
load_dotenv()  # Must be called FIRST

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")

if not JIRA_BASE_URL or not JIRA_TOKEN:
    raise RuntimeError("JIRA_BASE_URL and JIRA_TOKEN must be set in .env")
```

The `if not` check is a "fail fast" pattern — it's better to get a clear error at startup than a cryptic `NoneType` error buried in an HTTP call later.

Here's the security checklist built into this implementation. Which of these feels most important to you?

| Risk | Mitigation |
|---|---|
| Token in source code | `os.environ.get()` reads from environment, never hardcoded |
| Token in git | `.env` excluded via `.gitignore` |
| Unbounded results | `max_results` capped at 50 |
| State leakage between calls | Fresh `httpx.Client` per call |
| Error detail leak | `raise_for_status()` gives clean HTTP errors |

**Learner:** The token in source code one feels most critical. I've seen that happen.

**Trainer:** It's the most common and most painful. Once a token gets committed, even if you rotate it, it lives in git history forever unless you do a destructive rewrite. The habit of "always use environment variables" is worth building even for toy projects.

Here's an interesting angle: the `max_results = min(max_results, 50)` line. Why do you think we hardcode this cap in the server rather than letting the AI client pass any number?

**Learner:** To prevent the AI from accidentally requesting thousands of results?

**Trainer:** Exactly. AI models don't self-limit their requests. If the AI decides to search for "all issues" and your Jira has 50,000 of them, without the cap you'd burn the model's context window and possibly rate-limit the API. The server is the right place to enforce this — it's a policy decision that shouldn't be controlled by the caller.

This is actually a general principle of MCP server design: **trust the caller's intent, but limit the blast radius**. The AI knows what it wants; the server knows what's safe.

Ready to see the full `server.py` and then connect it to VS Code in Part 5?

---

## Part 5: Connecting to VS Code

**Trainer:** The server is ready. Now we connect it to VS Code via `mcp.json`.

```json
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["c:/workspace/jira-mcp/server.py"]
    }
  }
}
```

VS Code launches `server.py` as a subprocess on startup. The server communicates via stdio — no ports, no network, no firewall rules.

After adding this:
1. Reload MCP config (Command Palette → **MCP: Restart All Servers**)
2. Open Agent Mode chat
3. Ask: "What MCP tools do you have available?"
4. You should see `get_issue`, `search_issues`, `create_issue`, `add_comment`

**Verification test:**
```
Search for open issues in project PROJ using the Jira MCP
```

One thing to note: when VS Code starts your server, it inherits your shell's environment variables. If `JIRA_TOKEN` is set in your shell, the server picks it up even without a `.env` file. However, relying on the `.env` file is safer — it makes the setup reproducible and independent of shell configuration.

What's your initial reaction to the whole setup? Is it simpler or more complex than you expected?

**Learner:** Simpler than I expected, honestly. I thought MCP servers would be much harder to build.

**Trainer:** That's the FastMCP value proposition. The framework handles protocol complexity, transport, schema generation, and validation — you just write Python functions. The entire working Jira server is about 120 lines including comments.

Compare that to the raw MCP SDK: you'd need to write JSON schema for every parameter, wire up the transport manually, and handle protocol lifecycle events. FastMCP hides all of that.

Let's move to Part 6 — using open-source MCP code as a safe reference.

---

## Part 6: Using Open-Source MCPs as a Reference

**Trainer:** The [Docker Hub MCP catalog](https://hub.docker.com/mcp) lists hundreds of open-source MCP servers. You can use them as learning material without running any of their code.

The workflow:
1. Find a community MCP for your tool
2. Open the source code
3. Give it to your AI agent and ask for a security review
4. Ask the AI to implement a minimal FastMCP version based on what it found

The security review prompt to use:

```
Review this MCP server code and tell me:
1. All external network calls it makes and what data is sent.
2. How it handles authentication tokens (any logging or forwarding?).
3. Any security concerns (OWASP Top 10, hardcoded secrets, eval, shell injection).
4. The minimum set of API calls I need to reimplement the core functionality.

After the review, implement a minimal FastMCP version with only the essential
tools, following secure coding practices.
```

This gives you the knowledge from an experienced developer's implementation without inheriting their dependencies or trusting their code.

What do you think about this approach — using the community code as a research artifact rather than a runtime dependency?

**Learner:** It's clever. You get the benefit of someone else's API research without the security risk.

**Trainer:** Exactly. The community MCP developer has already figured out which Jira endpoints are worth calling, what the request/response shapes look like, and what edge cases exist. That research is valuable. The code itself (with unknown dependencies and unknown intent) is what you want to avoid running.

It's the same reason you'd read a library's source code to understand its patterns, then implement a minimal version yourself for a critical system. Knowledge is transferable; trust is not.

One last thing: pair this with module 134 (AI Code Security Review) if you want a more systematic approach to reviewing any code before trusting it.

---

## Issues Found During Self-Run

### Fix Applied
- **Missing "What We'll Build" section** — walkthrough.md lacked the required component table and time estimate. Added between Prerequisites and Part 1.

### Notes for Module Author
- The `requirements.txt` in the module example uses `fastmcp` (which installs as `fastmcp 3.2.4` — ✅ verified working, Apache-2.0 license)
- Python venv module may not be available in all Python 3.13 installations — consider adding a note: "If `python -m venv` fails, install via `pip install virtualenv` and use `virtualenv .venv` instead"
- The `mcp.json` section could clarify: VS Code MCP configuration lives in `.vscode/mcp.json` (workspace) or `%APPDATA%\Code\User\mcp.json` (user-level). Both work; workspace-level is generally preferred for project-specific servers.

---

## Session Summary

- ✅ All 6 Parts covered
- ✅ Practical files created: `work/106-task/server.py`, `.env.example`, `.gitignore`, `requirements.txt`
- ✅ FastMCP 3.2.4 installed and verified
- ✅ `server.py` syntax validated
- ✅ Inconsistency fixed: added "What We'll Build" section to walkthrough.md
- ✅ Module cross-links verified: 100, 105, 108, 076, 134, 165 all exist
