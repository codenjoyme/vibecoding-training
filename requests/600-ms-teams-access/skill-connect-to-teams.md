# Skill: Connect a Python App to Microsoft Teams (LLM Setup Guide)

> **Status:** Draft v0.1 — distilled from a knowledge-transfer call (`summary-2026-04-22.md`).
> **Purpose:** Give an LLM agent enough information to set up Microsoft Teams access from a custom Python app on a clean machine, with no prior Azure/Graph experience required from the user.
> **To be improved iteratively** as the user pastes additional inputs from the original chat (Azure registration link, exact permission scopes, MSAL snippet, etc.).

## Goal

Enable a Dockerized Python application to:

1. Authenticate the **current user** against Microsoft Entra ID (Azure AD) of their corporate tenant.
2. Read the user's Teams **1:1 chats, group chats, and meeting chats** via Microsoft Graph API.
3. (Optional) Post back into a dedicated Teams chat/channel created by the app on first run.

No admin ticket should be required for the typical case — the user does the Azure App Registration themselves, in their own corporate tenant.

## Required Secrets (`.env`)

The application reads four secrets at container build/start time:

| Variable             | Where it comes from                                              | Used for                                             |
| -------------------- | ---------------------------------------------------------------- | ---------------------------------------------------- |
| `AZURE_TENANT_ID`    | Azure Portal → Entra ID → Overview                                | Identifies the corporate directory                    |
| `AZURE_CLIENT_ID`    | Azure Portal → App registrations → your app → Overview            | Identifies the registered app                         |
| `AZURE_CLIENT_SECRET`| Azure Portal → App registrations → your app → Certificates & secrets | Lets the app authenticate to Entra ID                 |
| `GITHUB_TOKEN`       | github.com → Settings → Developer settings → Personal access tokens (or GitHub Models token) | Calls the LLM via the GitHub Models endpoint (no premium-request burn) |

All four must end up in a `.env` file at the project root, listed in `.gitignore`. Never commit the values.

## Step 1 — Register the Application in Azure (Entra ID)

> The original step-by-step link will be added here once the source chat message is recovered. Until then, the procedure below is the working path used by the reference implementation.

1. Sign in to [https://portal.azure.com](https://portal.azure.com) with the corporate account.
2. Go to **Microsoft Entra ID** (formerly Azure Active Directory).
3. In the left menu pick **App registrations** → **+ New registration**.
4. Fill in:
   - **Name:** any human-readable name, e.g. `teams-ai-assistant-<your-username>`.
   - **Supported account types:** *Accounts in this organizational directory only* (single tenant) is enough.
   - **Redirect URI:** type **Public client/native (mobile & desktop)**, value `http://localhost` (used by the interactive sign-in flow on first launch).
5. Click **Register**.
6. From the **Overview** page copy:
   - **Application (client) ID** → `AZURE_CLIENT_ID`
   - **Directory (tenant) ID** → `AZURE_TENANT_ID`
7. Open **Certificates & secrets** → **+ New client secret**, give it a name and expiry, copy the **Value** (only shown once) → `AZURE_CLIENT_SECRET`.

## Step 2 — Grant Microsoft Graph Permissions

Open the registered app → **API permissions** → **+ Add a permission** → **Microsoft Graph** → **Delegated permissions** (the app acts on behalf of the signed-in user).

Minimum permission set for **read-only** chat summarization:

- `Chat.Read` — read the user's 1:1 and group chats.
- `ChatMessage.Read` — read chat messages.
- `User.Read` — required by default; identifies the signed-in user.
- `offline_access` — keeps the refresh token so re-auth is not needed every run.

Additional permissions for **posting back** into Teams (used by this PoC for notifications):

- `Chat.ReadWrite` — create and post into the dedicated app chat.
- `ChatMessage.Send` — send messages on the user's behalf.

> If the corporate tenant flags any of these as "admin consent required", the user must request admin consent. In the reference setup, all of the above were self-grantable for the individual user — no admin ticket was needed.

After adding, click **Grant admin consent for `<tenant>`** if available; otherwise consent will be requested interactively on first sign-in.

## Step 3 — First-Run Authentication Flow

The app uses **MSAL for Python** with the **interactive / device-code** flow:

- On `docker compose up` the container prints either a localhost URL or a device code + URL.
- The user opens it in a browser, signs in with the corporate account, approves the requested scopes once.
- MSAL caches the refresh token to a file mounted on a Docker volume → subsequent runs do not require re-auth until the token chain expires.

Pseudo-code for the auth client:

```python
import os
from msal import PublicClientApplication, SerializableTokenCache

SCOPES = [
    "Chat.Read", "ChatMessage.Read",
    "Chat.ReadWrite", "ChatMessage.Send",
    "User.Read", "offline_access",
]

cache = SerializableTokenCache()
if os.path.exists("/data/token_cache.bin"):
    cache.deserialize(open("/data/token_cache.bin").read())

app = PublicClientApplication(
    client_id=os.environ["AZURE_CLIENT_ID"],
    authority=f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}",
    token_cache=cache,
)

accounts = app.get_accounts()
result = (
    app.acquire_token_silent(SCOPES, account=accounts[0])
    if accounts else None
)
if not result:
    flow = app.initiate_device_flow(scopes=SCOPES)
    print(flow["message"])  # user opens URL, enters code
    result = app.acquire_token_by_device_flow(flow)

if cache.has_state_changed:
    open("/data/token_cache.bin", "w").write(cache.serialize())

access_token = result["access_token"]
```

> When using a confidential client (i.e. `AZURE_CLIENT_SECRET`) instead of a public one, switch to `ConfidentialClientApplication` and the on-behalf-of or client-credentials flow. The reference implementation uses the public/interactive flow and treats `AZURE_CLIENT_SECRET` as optional / future-use.

## Step 4 — Calling Microsoft Graph

All Graph calls are plain HTTPS with `Authorization: Bearer <access_token>`.

Useful endpoints for this scenario:

| Goal                                | Endpoint                                                          |
| ----------------------------------- | ----------------------------------------------------------------- |
| List the user's chats               | `GET https://graph.microsoft.com/v1.0/me/chats`                   |
| Get messages in a chat              | `GET https://graph.microsoft.com/v1.0/me/chats/{chat-id}/messages` |
| Send a message into a chat          | `POST https://graph.microsoft.com/v1.0/me/chats/{chat-id}/messages` |
| Create a 1:1 / group chat           | `POST https://graph.microsoft.com/v1.0/chats`                     |
| Get the signed-in user              | `GET https://graph.microsoft.com/v1.0/me`                         |

> **Channels** (Teams team channels) live under `/teams/{team-id}/channels/...` and require a different permission set (`ChannelMessage.Read.All` etc.). They are intentionally **out of scope** for the v1 of this skill — only chats and meetings are covered.

When in doubt about an endpoint or required scope, point the agent at **context7 MCP** to fetch the latest Microsoft Graph docs instead of relying on training-data knowledge.

## Step 5 — Containerization Notes

- Mount a named volume to `/data` so the MSAL token cache and any local DB survive restarts.
- Pass the four env vars via `env_file: .env` in `docker-compose.yml`.
- For the device-code flow, simply `docker compose up` in the foreground on the very first run so the user can copy the code; subsequent runs can be detached.

## Open Items (Iterate Here)

- [ ] Add the original Azure setup link from the source chat message.
- [ ] Confirm the exact minimum scope list against the live PoC.
- [ ] Decide whether to ship a public-client (interactive) or confidential-client variant by default.
- [ ] Add a `docker-compose.yml` reference snippet.
- [ ] Add a smoke-test script: `GET /me` → print display name, `GET /me/chats?$top=1` → print first chat topic.
- [ ] Document the "auto-create dedicated notification chat on first run" behavior with the exact Graph payload.
- [ ] Add troubleshooting section: AADSTS errors, consent loops, expired client secret, missing `offline_access`.

## Verification Checklist (Definition of Done for a Clean Machine)

- [ ] Azure App Registration exists in the user's tenant with the four required IDs/secret captured.
- [ ] Required Graph delegated permissions added and consented.
- [ ] `.env` populated with all four variables; `.env` is in `.gitignore`.
- [ ] `docker compose up` runs the container; on first run a sign-in URL/device code is printed.
- [ ] After sign-in the app calls `GET /me` successfully and prints the user's name.
- [ ] The app lists the user's chats and reads the latest messages from at least one.
- [ ] (If write scope granted) The app creates a dedicated chat and posts a "hello" notification.
