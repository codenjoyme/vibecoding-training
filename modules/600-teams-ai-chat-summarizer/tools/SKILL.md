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

- [ ] App Registration exists; `Allow public client flows = Yes`.
- [ ] Six Graph delegated permissions added; consent granted.
- [ ] `.env` populated with the four required variables.
- [ ] `docker compose run --rm smoke` prints user displayName.
- [ ] `docker compose run --rm list-chats` prints chats.
- [ ] `docker compose run --rm app python create_notification_chat.py` prints chat id; chat appears in Teams.
- [ ] `docker compose run --rm app python summarize_and_notify.py "<src>" --top 20` posts a message into the notification chat.

## Common Errors

- `AADSTS7000218` — public client flows not enabled (Step 2).
- `AADSTS65001` — consent not granted; sign in interactively and click Accept.
- `AADSTS70011` — invalid scope; do not include `openid`/`profile`/`offline_access` manually.
- `HTTP 403` from Graph — missing scope or revoked consent; delete token cache and re-auth.
- Docker `requirements.txt: not found` during build — `.dockerignore` excludes `*.txt`; add `!requirements.txt`.
