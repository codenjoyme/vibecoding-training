<follow>
iterative-prompt.agent.md
</follow>

# Context

This prompt was created from a live chat session on 2026-04-30. The conversation explored Jira access options and led to a request to build a dedicated training module using the MCPyrex CLI approach.

## Chat Summary

**User:** Do we have a module about Jira access?

**Agent:** No standalone Jira module exists. Jira is partially covered in:
- `modules/168-elitea-remote-mcp-http-integration/walkthrough.md` — Atlassian OAuth 2.0 Remote MCP section with tools: `jira_create_issue`, `jira_search_issues`, `jira_get_board`, etc.
- `modules/proposed-mcpyrex-modules.md` — module 470 "mcpyrex: Jira Integration & PDF Processing" proposed but not yet created.

**User:** Let's create a new module using the iterative prompt approach. Based on a MCPyrex Python script, build a CLI for Jira access with an API token. Key points to cover in the module:
- When creating an API token — recommend limiting its permissions (e.g., read-only), setting a time limit, and restricting access by IP
- Show how to discover your own IP address
- Recommend using VPN to minimize the risk of token leakage
- Explain why CLI is more flexible than MCP: supports binary files, can be extended easily, saves context because work happens via CLI outside the AI context window
- Allow the user to port the solution to any language they prefer at the end
- Organize everything around a `skill.md` file at the module core
- Switch to polling mode after creating the request

---

## UPD1

Create training module **470 — Jira CLI Access via MCPyrex** in `modules/470-jira-cli-access/`.

**Module placement:** After module 445 (mcpyrex HTTP Client) and before 475 (mcpyrex JavaScript Engine).

**Dependencies:**
- `400-installing-mcpyrex-mcp-python-toolbox` — mcpyrex must be installed
- `440` (terminal execution) — CLI runs via terminal
- `445` (HTTP client) — Jira uses REST API over HTTP
- `108-token-api-key-management` — API token security concepts

**Module structure to create:**
1. `modules/470-jira-cli-access/about.md` — module overview (title, elevator pitch, prerequisites, outcomes)
2. `modules/470-jira-cli-access/skill.md` — the SKILL.md that the module is organized around; it should be the runnable AI agent skill for querying Jira via CLI
3. `modules/470-jira-cli-access/walkthrough.md` — full step-by-step training session with 4–6 parts:

**Walkthrough structure:**

**Part 1 — Why CLI over MCP for Jira**
- MCP tools load into context window → expensive
- CLI runs outside context → saves tokens
- CLI handles binary attachments (screenshots, PDFs, ZIPs) — MCP cannot
- CLI is easily scriptable, pipeable, testable independently
- CLI can be ported to any language; MCP requires server wrapper overhead
- Cross-link to module `106-fastmcp-custom-mcp-server` for MCP alternative

**Part 2 — Creating a Jira API Token Safely**
- Go to https://id.atlassian.com/manage-api-tokens
- Create token with **minimum permissions** — read-only scope if only querying
- Set an **expiration date** — never create tokens that don't expire
- **IP restriction** — limit the token to your office/VPN IP range
  - How to find your current IP: `curl ifconfig.me` or `curl icanhazip.com`
- **VPN best practice** — always work from behind a VPN so the allowed IP is the VPN egress, not your home IP; this way if token leaks, attacker can't use it without VPN
- Store token in `.env` file — never hardcode, never commit
- Cross-link to module `108-token-api-key-management`

**Part 3 — Building the MCPyrex Python CLI Script**
- Python script that reads `JIRA_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` from `.env`
- Uses `requests` library with Basic Auth (email + token)
- CLI commands (argparse or click):
  - `search` — JQL query, returns issue list as JSON or table
  - `get` — fetch single issue by key
  - `comment` — add comment to issue (optional, read-only mode can skip)
  - `attachments` — list attachments, download binary files
- Output formats: `--format json` | `--format table` | `--format plain`
- Show how binary attachments are downloaded to disk (this is impossible cleanly via MCP)

**Part 4 — Connecting the CLI as an AI Skill**
- The `skill.md` file teaches the AI agent how to invoke the CLI
- Format: describe available commands, expected input/output, when to use
- Show the AI using the CLI tool in a real workflow (search sprint issues, get details, download attachment)

**Part 5 — Security Checklist**
- Summarize all security practices as a checklist:
  - [ ] Token is read-only scoped
  - [ ] Token has expiration date set
  - [ ] IP restriction enabled (VPN IP)
  - [ ] `.env` is in `.gitignore`
  - [ ] No token in logs or output
  - [ ] Script validates `JIRA_URL` is HTTPS only

**Part 6 — Port to Any Language**
- Explain that the pattern (env vars + REST + argparse/CLI) is language-agnostic
- Show equivalents: Node.js (axios + dotenv + commander), Go (net/http + cobra), Java (OkHttp + picocli)
- Practical task: ask user to pick their preferred language and port the script using AI assistance

**skill.md requirements:**
- Must follow the SKILL.md format used in other modules (e.g., `modules/076-skills-management-system/` or `modules/090-ai-skills-tools-creation/`)
- Should define: what the skill does, when to invoke it, CLI usage examples, expected output format, error handling guidance

**Add module 470 to `modules/module-catalog.md` and `training-plan.md`.**

go

### RESULT

Created module **470 — Jira CLI Access via MCPyrex Python Script** placed between 400 (mcpyrex toolbox) and 500 (AI workflow guide).

- [modules/470-jira-cli-access/about.md](../../modules/470-jira-cli-access/about.md) — module overview with prerequisites (400, 108), topics, outcomes, and resource links
- [modules/470-jira-cli-access/skill.md](../../modules/470-jira-cli-access/skill.md) — AI agent skill descriptor: what the CLI does, when to invoke it, all commands with examples, error handling table, and language-porting guide
- [modules/470-jira-cli-access/walkthrough.md](../../modules/470-jira-cli-access/walkthrough.md) — 6-part hands-on walkthrough:
  - Part 1: CLI vs MCP comparison — context savings, binary files, portability
  - Part 2: Secure API token creation — expiry, IP restriction, VPN best practice, `curl ifconfig.me` IP discovery
  - Part 3: Full `jira_cli.py` with `search`, `get`, `attachments`, `download` commands
  - Part 4: Attaching `skill.md` as an AI agent skill, demo workflow
  - Part 5: Security checklist (8 items)
  - Part 6: Language porting table (Node.js, Go, Java, Bash) with AI-assisted porting prompt
- [modules/module-catalog.md](../../modules/module-catalog.md) — module 470 added
- [training-plan.md](../../training-plan.md) — module 470 added after 400
