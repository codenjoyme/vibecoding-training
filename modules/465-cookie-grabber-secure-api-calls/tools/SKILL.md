# Cookie Grabber — AI Agent Skill

> **This file is both a human guide and an AI skill.** When an AI agent reads this file, it gains full context on how to make authenticated API calls using browser cookies captured via the Cookie Grabber pipeline.

---

## What This Skill Does

This skill enables the AI agent to call cookie-protected internal APIs (Telescope, internal dashboards, corporate portals, etc.) without ever seeing the cookies themselves.

**How it works:**
1. A Chrome extension grabs cookies for a target domain
2. The extension encrypts them with AES-256-GCM (key from master password) and sends to a local Docker server
3. The server stores only the encrypted blob — it never decrypts
4. The local CLI (`cli.py`) decrypts with the master password and makes HTTP requests using the cookies

**Key security property:** The AI agent only sees API responses — never the cookie values.

---

## When to Invoke This Skill

Use this skill when the user asks to:
- Fetch data from an internal API that requires browser session cookies
- Access a protected corporate portal via AI automation
- Make authenticated REST calls to services that don't support API tokens

Do **not** use this skill if:
- The API supports API tokens, OAuth, or Basic Auth — use those instead
- `cookies.enc` does not exist (user needs to run the extension first)
- The server is not running (`docker compose up`)

---

## Prerequisites

1. Docker server is running: `docker compose up -d` (from `tools/scripts/`)
2. `tools/scripts/data/cookies.enc` exists (extension was used to grab cookies)
3. CLI dependencies installed: `pip install -r tools/scripts/requirements-cli.txt`
4. `MASTER_PASSWORD` env var set, or ready to type it interactively

---

## CLI Usage Reference

Run `cli.py` from any directory — `.env` is searched upward automatically if `python-dotenv` is used, or set `COOKIE_FILE` explicitly.

```
python tools/scripts/cli.py <command> [options]
```

### `status` — Check if cookies are stored

```
python tools/scripts/cli.py status
```

### `info` — Show metadata (no plaintext cookie values)

```
python tools/scripts/cli.py info
```

### `get` — HTTP GET with cookies

```
python tools/scripts/cli.py get --url https://internal-api.example.com/api/v1/users
python tools/scripts/cli.py get --url https://internal-api.example.com/api/v1/me \
  --header Accept=application/json
```

### `post` — HTTP POST with cookies

```
python tools/scripts/cli.py post \
  --url https://internal-api.example.com/api/search \
  --data '{"query": "active users", "limit": 10}'
```

### `clear` — Delete stored cookies

```
python tools/scripts/cli.py clear
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MASTER_PASSWORD` | (prompt) | Password used to decrypt cookies |
| `COOKIE_FILE` | `./data/cookies.enc` | Path to encrypted cookie file |

---

## Invocation Workflow for the AI Agent

When the user asks to query a cookie-protected API:

1. **Check status** — run `cli.py status` to confirm cookies are available
2. **Run the query** — use `cli.py get --url ...` or `cli.py post --url ...`
3. **Present results** in plain language — do not dump raw JSON unless asked
4. If status shows no cookies → ask user to open Chrome, click extension, grab cookies for the target domain

**Example agent workflow:**
```
User: "Show me my active sprint tasks from the Telescope portal"

Agent steps:
1. Run: python tools/scripts/cli.py status  →  ✅ Cookies stored for telescope.example.com
2. Run: python tools/scripts/cli.py get --url https://telescope.example.com/api/sprint/active
3. Parse JSON, present task list in a readable table
```

---

## Error Handling

| Error | Likely cause | Action |
|-------|-------------|--------|
| `No cookies stored` | Extension not run yet | Ask user to open Chrome, click extension, enter domain + password |
| `Decryption failed` | Wrong master password | Ask user to re-enter password or check `MASTER_PASSWORD` env var |
| `Connection refused` when running extension | Server not started | `docker compose up -d` from `tools/scripts/` |
| `403 Forbidden` | Cookies expired | Re-grab cookies via extension |
| `SSLError` | Self-signed cert on target API | Add `--header Verify=false` or configure `requests` to skip verification |

---

## Files in This Skill

| Path | Purpose |
|------|---------|
| `tools/scripts/cli.py` | CLI for authenticated API calls (runs on host) |
| `tools/scripts/server.py` | HTTP + WebSocket server (runs in Docker) |
| `tools/scripts/extension/` | Chrome extension source (load unpacked in Chrome) |
| `tools/scripts/Dockerfile` | Docker image for server |
| `tools/scripts/docker-compose.yml` | One-command server startup |
| `tools/scripts/requirements-cli.txt` | Host CLI dependencies |
| `tools/scripts/requirements-server.txt` | Docker server dependencies |
| `tools/scripts/.env.example` | Config template |
| `tools/scripts/data/cookies.enc` | Encrypted cookie storage (gitignored) |
