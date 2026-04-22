# Skill: Connect a Python App to Microsoft Teams

> **Audience:** LLM agent setting up Microsoft Teams access from a custom Python app on a clean machine.
> **Goal:** Enable a Dockerized Python app to authenticate against Microsoft Entra ID, read Teams chats / messages via Microsoft Graph, and post summaries back into a dedicated chat.

## Prerequisites

- Corporate Microsoft 365 / Entra ID account (single tenant is sufficient).
- Docker Desktop installed and running.
- A GitHub account with access to GitHub Models.

## Required Secrets (`.env`)

| Variable | Source | Required |
|---|---|---|
| `AZURE_TENANT_ID` | Entra ID → App registration → Overview → Directory (tenant) ID | ✅ |
| `AZURE_CLIENT_ID` | Entra ID → App registration → Overview → Application (client) ID | ✅ |
| `AZURE_CLIENT_SECRET` | Entra ID → Certificates & secrets → New client secret → Value | ❌ optional (not used by device-code flow) |
| `GITHUB_TOKEN` | github.com → Settings → Developer settings → PAT (classic, scope: `read:user`) | ✅ |
| `LLM_MODEL` | constant, default `gpt-4o` | ✅ |
| `LLM_ENDPOINT` | constant, default `https://models.inference.ai.azure.com` | ✅ |
| `NOTIFICATION_CHAT_ID` | output of `create_notification_chat.py` | ✅ for posting |

`.env` MUST be gitignored. The token cache (`./data/token_cache.bin`) MUST also be gitignored.

## ⚠️ This Folder Already Has Working Scripts — REUSE Them

**Before writing any new code, read what's already here.** The agent's job is to glue these together for new use cases, not reimplement them. Do NOT regenerate MSAL flow, Graph auth headers, HTML stripping, or chat creation from scratch — they exist and are tested.

### Folder layout

```
tools/
├── SKILL.md                      ← this file (LLM-targeted reference)
├── readme.md                     ← human-friendly walkthrough with screenshots
├── .env.example                  ← template for required secrets (copy → .env)
├── .env                          ← LOCAL ONLY, gitignored
├── .gitignore                    ← .env, data/, __pycache__/, *.pyc, .venv/
├── .dockerignore                 ← excludes .env, data/, screenshots; KEEPS requirements.txt
├── Dockerfile                    ← python:3.12-slim, COPY *.py, PYTHONUNBUFFERED=1
├── docker-compose.yml            ← 3 services: app (generic CLI), smoke, list-chats
├── requirements.txt              ← msal, requests, python-dotenv
├── data/                         ← LOCAL ONLY, gitignored — holds token_cache.bin
├── img/                          ← screenshots used by readme.md
│
├── graph_auth.py                 ← shared MSAL device-code auth + token cache (CLOSED — do not modify)
├── smoke_test.py                 ← GET /me, prints displayName / mail / id
├── list_chats.py                 ← lists top-20 chats with members and last activity
├── read_messages.py              ← argparse: CHAT_ID --top N, prints messages (HTML stripped)
├── create_notification_chat.py   ← argparse: --topic STR, idempotent, prints chat id
└── summarize_and_notify.py       ← argparse: SOURCE_CHAT_ID --top N, full E2E pipeline
```

### Architecture rule (OCP)

`graph_auth.py` is **closed for modification, open for import**. Every other script does:

```python
from graph_auth import get_access_token
token = get_access_token()
```

When extending, write a new `*.py` that imports `get_access_token`. Never re-implement MSAL.

### Per-script reference

| Script | What it does | Signature / args | Key implementation notes |
|---|---|---|---|
| `graph_auth.py` | Acquires a Microsoft Graph access token. Tries `acquire_token_silent` first, falls back to device-code flow. Persists the cache to `/data/token_cache.bin`. | `get_access_token() -> str` | Reads `AZURE_TENANT_ID` and `AZURE_CLIENT_ID` from env. `SCOPES = ["User.Read", "Chat.Read", "ChatMessage.Read", "Chat.ReadWrite", "ChatMessage.Send"]` — do NOT add `openid`/`profile`/`offline_access` (MSAL adds them). |
| `smoke_test.py` | Verifies the whole auth chain. | no args | Calls `GET /me`, prints `displayName`, `mail`, `userPrincipalName`, `id`. Run this first when something breaks. |
| `list_chats.py` | Discovers the chat IDs you have access to. | no args, hardcoded `TOP=20` | `GET /me/chats?$top=20&$expand=members&$orderby=lastMessagePreview/createdDateTime desc`. Prints index, chatType, lastUpdated, label (topic or member names), and id. Copy the id you want to use. |
| `read_messages.py` | Dumps recent messages from one chat. | `CHAT_ID [--top N]` (default N=20) | `GET /me/chats/{id}/messages?$top=N`. Strips HTML, resolves sender (user / application / system), prints timestamps in UTC. Skip messages with empty body — they are attachment-only / system events. |
| `create_notification_chat.py` | Creates the dedicated "AI inbox" group chat. | `[--topic "AI Teams Summaries"]` | **Idempotent** — first calls `find_existing()` which scans group chats by topic; only creates if missing. Posts `POST /chats` with `chatType: "group"` + single `aadUserConversationMember` (you). Prints `NOTIFICATION_CHAT_ID=...` line ready to paste into `.env`. |
| `summarize_and_notify.py` | Full read → summarize → post pipeline. | `SOURCE_CHAT_ID [--top N]` (default N=20) | Pipeline: `fetch_messages()` → `build_transcript()` (oldest first, HTML stripped, drops empty bodies) → `summarize()` (POST `{LLM_ENDPOINT}/chat/completions`, model `LLM_MODEL`, `temperature=0.3`) → `markdown_to_teams_html()` → `post_to_notification_chat()`. System prompt asks for "3-7 bullets" — change `SYSTEM_PROMPT` constant to retune. |

### Key reusable helpers (already implemented — don't rewrite)

| Helper | Where | Use |
|---|---|---|
| `get_access_token()` | `graph_auth.py` | Authenticated Graph calls in any new script |
| `strip_html(s)` | `read_messages.py`, `summarize_and_notify.py` | Convert Teams message HTML → plain text |
| `fmt_when(iso)` | same | ISO timestamp → "YYYY-MM-DD HH:MM UTC" |
| `sender_name(msg)` | `read_messages.py` | Resolve user / application / system sender |
| `find_existing(token, topic)` | `create_notification_chat.py` | Look up a group chat by topic (idempotency pattern) |
| `markdown_to_teams_html(md, src, count)` | `summarize_and_notify.py` | Minimal markdown → Teams-safe HTML (`<b>`, `<br>`, bullets) |
| `build_transcript(msgs)` | `summarize_and_notify.py` | Convert message list (newest first) → LLM-ready transcript (oldest first) |

### Standard run commands (from `tools/`)

```powershell
# Verify auth
docker compose run --rm smoke

# Discover chats
docker compose run --rm list-chats

# Read messages from one chat
docker compose run --rm app python read_messages.py "<CHAT_ID>" --top 20

# Create the AI-inbox chat (idempotent)
docker compose run --rm app python create_notification_chat.py

# Full pipeline (use --build once after adding new scripts)
docker compose run --rm --build app python summarize_and_notify.py "<SOURCE_CHAT_ID>" --top 20
```

The `app` service has `entrypoint: []` and accepts arbitrary `python <file>.py <args>`. Add new scripts to the folder, run with `--build` once, then drop `--build` for subsequent runs.

### Extending — recipe for a new script

1. Create `tools/new_thing.py` next to the existing scripts.
2. `from graph_auth import get_access_token` (and `strip_html` / `fmt_when` / etc. via `from read_messages import ...` if useful).
3. Use `requests` + `Authorization: Bearer {token}` against `https://graph.microsoft.com/v1.0/...`.
4. Add `import argparse` for CLI parameters; mirror the style of `read_messages.py`.
5. Run with `docker compose run --rm --build app python new_thing.py <args>` (the `--build` is needed once because `Dockerfile` does `COPY *.py`).
6. Optionally add a named compose service in `docker-compose.yml` if you'll run it often.

---

## Step 1 — Register the Application in Azure

1. Go to https://portal.azure.com → **Microsoft Entra ID → App registrations → + New registration**.
2. Name: `teams-ai-assistant-<username>`. Supported account types: **Single tenant**. Redirect URI: **Public client/native (mobile & desktop)** = `http://localhost`.
3. Register. Copy `Application (client) ID` and `Directory (tenant) ID` from Overview.

## Step 2 — Enable Public Client Flows

1. App registration → **Authentication (Preview)** → **Settings** → **Allow public client flows = Yes** → **Save**.

This is mandatory for the device-code flow even though the redirect URI is registered as `Public client/native`. Without it, Azure returns `AADSTS7000218`.

## Step 3 — Add Microsoft Graph Delegated Permissions

App registration → **API permissions → + Add a permission → Microsoft Graph → Delegated permissions**. Add:

- `User.Read` (default)
- `Chat.Read`
- `ChatMessage.Read`
- `Chat.ReadWrite`
- `ChatMessage.Send`
- `offline_access`

For all six, **Admin consent required = No** in the typical corporate tenant. Consent will be granted interactively on first sign-in.

## Step 4 — Authenticate with MSAL Device-Code Flow

Use `PublicClientApplication` + `SerializableTokenCache` persisted to `/data/token_cache.bin`:

```python
from msal import PublicClientApplication, SerializableTokenCache

SCOPES = ["User.Read", "Chat.Read", "ChatMessage.Read",
          "Chat.ReadWrite", "ChatMessage.Send"]
# Note: do NOT include openid/profile/offline_access — MSAL adds them.

cache = SerializableTokenCache()
if os.path.exists(CACHE_PATH):
    cache.deserialize(open(CACHE_PATH).read())

app = PublicClientApplication(
    client_id=CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    token_cache=cache,
)

# Try silent first.
result = None
for acc in app.get_accounts():
    result = app.acquire_token_silent(SCOPES, account=acc)
    if result: break

# Fall back to device flow.
if not result:
    flow = app.initiate_device_flow(scopes=SCOPES)
    print(flow["message"])  # user opens URL, types code
    result = app.acquire_token_by_device_flow(flow)

if cache.has_state_changed:
    open(CACHE_PATH, "w").write(cache.serialize())

token = result["access_token"]
```

## Step 5 — Microsoft Graph Endpoints

All calls: `Authorization: Bearer <access_token>`, base `https://graph.microsoft.com/v1.0`.

| Use case | Method + URL |
|---|---|
| Verify auth | `GET /me` |
| List user's chats | `GET /me/chats?$top=20&$expand=members&$orderby=lastMessagePreview/createdDateTime desc` |
| Read messages from a chat | `GET /me/chats/{chat_id}/messages?$top=N` |
| Send a message into a chat | `POST /me/chats/{chat_id}/messages` body: `{"body": {"contentType": "html", "content": "..."}}` |
| Create a new chat (group, with self) | `POST /chats` — see below |
| Get my user id | `GET /me` then `.id` |

**Channels** (`/teams/{team-id}/channels/...`) are out of scope — they require `ChannelMessage.Read.All` and admin consent.

## Step 6 — Create a Self-Only Notification Chat

Graph forbids `oneOnOne` with self. Workaround: create a `group` chat with one member (you):

```json
POST /chats
{
  "chatType": "group",
  "topic": "AI Teams Summaries",
  "members": [
    {
      "@odata.type": "#microsoft.graph.aadUserConversationMember",
      "roles": ["owner"],
      "user@odata.bind": "https://graph.microsoft.com/v1.0/users('<my_user_id>')"
    }
  ]
}
```

Make this idempotent: first `GET /me/chats?$filter=chatType eq 'group'` and check for existing topic match.

## Step 7 — Summarization via GitHub Models

LLM endpoint: `POST {LLM_ENDPOINT}/chat/completions` with `Authorization: Bearer {GITHUB_TOKEN}`. Body:

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "<concise summarization instructions>"},
    {"role": "user",   "content": "Сообщения чата (oldest first):\n\n<transcript>"}
  ],
  "temperature": 0.3
}
```

Parse `response.choices[0].message.content`.

## Step 8 — Post HTML Back into Teams

Convert the LLM markdown to minimal Teams HTML (`<b>`, `<br>`, `•`) before posting. Teams accepts `contentType: "html"` with a small whitelist of tags.

## Step 9 — Containerization Notes

- `python:3.12-slim` base.
- Mount a volume to `/data` so MSAL token cache survives `--rm` runs.
- `env_file: .env` in compose; `stdin_open: true` + `tty: true` for the device-code flow.
- `.dockerignore` MUST include `.env`, `data/`, screenshots — but exempt `requirements.txt` if you exclude `*.txt`.

## Step 10 — PII / Secret Hygiene

- `.gitignore`: `.env`, `data/`, original transcripts, screenshots, any chat-content markdown.
- Before sharing any markdown log: regex-replace personal names → `Stiven Pupkin`; emails → `stiven_pupkin@example.com`; org → `ACME`; GUIDs → `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`; chat ids → `19:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@thread.v2`; device codes → `XXXXXXXXX`.
- PNG screenshots cannot be auto-redacted — delete or manually obscure.

## Verification Checklist

- [ ] App Registration exists; `Allow public client flows = Yes` (and **Saved**).
- [ ] Six Graph delegated permissions added; consent granted (interactively on first sign-in).
- [ ] `tools/.env` populated: `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `GITHUB_TOKEN`, later `NOTIFICATION_CHAT_ID`.
- [ ] `docker compose run --rm smoke` prints user `displayName` from `GET /me`.
- [ ] `tools/data/token_cache.bin` was created (silent refresh works for next runs).
- [ ] `docker compose run --rm list-chats` prints 20 chats with their ids.
- [ ] `docker compose run --rm app python create_notification_chat.py` prints chat id; "AI Teams Summaries" appears in Teams; the printed line is pasted into `.env`.
- [ ] `docker compose run --rm app python read_messages.py "<chat_id>" --top 20` prints messages.
- [ ] `docker compose run --rm --build app python summarize_and_notify.py "<src>" --top 20` posts a summary into the notification chat.

## Common Errors

- `AADSTS7000218` — public client flows not enabled (Step 2). Fix: Authentication (Preview) → **Allow public client flows = Yes** → **Save**.
- `AADSTS65001` — consent not granted; sign in interactively and click **Accept** on the permissions screen.
- `AADSTS70011` — invalid scope; do not include `openid`/`profile`/`offline_access` manually — MSAL adds them.
- `HTTP 403` from Graph — missing scope or revoked consent; delete `tools/data/token_cache.bin` and re-authenticate.
- Docker build: `requirements.txt: not found` — `.dockerignore` excludes `*.txt`; add `!requirements.txt` exception.
- `python: can't open file '/app/<new>.py'` — image was not rebuilt after adding the script. Use `docker compose run --rm --build app ...` once.
- `KeyError: 'NOTIFICATION_CHAT_ID'` — `.env` not loaded or variable missing. Confirm `.env` exists in `tools/` and `docker-compose.yml` has `env_file: .env`.
