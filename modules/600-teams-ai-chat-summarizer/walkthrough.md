# Microsoft Teams AI Chat Summarizer - Hands-on Walkthrough

In this module you will go end-to-end from a blank machine to a running Dockerized Python app that reads your Teams chats, summarizes them with an LLM, and posts the summary back into a dedicated Teams chat. Every part below mirrors a real iterative session — including the real errors and fixes — so you experience the same gotchas and learn how to recover.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Description |
|---|---|
| Azure App Registration | Identity for your custom app inside your Entra ID tenant |
| Microsoft Graph delegated permissions | `Chat.Read`, `ChatMessage.Read`, `Chat.ReadWrite`, `ChatMessage.Send`, `offline_access`, `User.Read` |
| `.env` file | Tenant ID, client ID, GitHub PAT, notification chat ID — all gitignored |
| MSAL device-code flow | Headless authentication; token cached on a Docker volume |
| 6 Python scripts | `graph_auth`, `smoke_test`, `list_chats`, `read_messages`, `create_notification_chat`, `summarize_and_notify` |
| Dockerfile + docker-compose | One generic `app` runner + named services for common scripts |
| A dedicated "AI Teams Summaries" chat | Created via Graph; receives the AI-generated summaries |

The starter scripts are already in [tools/](tools/) — you will follow the walkthrough to set up Azure, configure `.env`, and run the scripts in the right order.

**Time estimate:** 30-45 minutes end to end.

---

## Part 1: Register the Application in Azure

### What we'll do
Create a new App Registration in Microsoft Entra ID under your corporate tenant.

### Action

1. Open https://portal.azure.com and sign in with your corporate account.

   ![Azure portal home](tools/img/01-azure-portal-home.png)

2. Navigate to **Microsoft Entra ID → App registrations**.

   ![App registrations page](tools/img/02-app-registrations-page.png)

3. Click **+ New registration** and fill in:
   - **Name:** any human-readable label, e.g. `teams-ai-assistant-<your-username>`.
   - **Supported account types:** *Accounts in this organizational directory only* (single tenant). This is the most restrictive and safest option.

     ![Supported account types](tools/img/03-supported-account-types.png)

   - **Redirect URI:** type **Public client/native (mobile & desktop)**, value `http://localhost`.

     ![Registration form filled](tools/img/04-registration-form-filled.png)

4. Click **Register**.
5. On the **Overview** page note the two GUIDs you will need shortly:
   - `Application (client) ID` → future `AZURE_CLIENT_ID`
   - `Directory (tenant) ID` → future `AZURE_TENANT_ID`

   ![App overview page](tools/img/05-app-overview-page.png)

### What happened
You created an identity for your custom app. The redirect URI must be registered as **Public client / native** (not Web) — otherwise Azure will treat the app as a confidential client and refuse the device-code flow we use later. We will tighten this further in [Part 5](#part-4-fix-public-client-flow).

---

## Part 2: Add Microsoft Graph Permissions

### What we'll do
Grant your app the minimum delegated permissions needed to read and write Teams chats on behalf of the signed-in user.

### Action

1. In the App Registration, go to **API permissions**.
2. The default `User.Read` (Delegated) is fine — leave it.

   ![API permissions default](tools/img/09-api-permissions-default.png)

3. Click **+ Add a permission → Microsoft Graph → Delegated permissions**.

   ![Choose Microsoft Graph](tools/img/10-choose-microsoft-graph.png)

   ![Delegated permissions](tools/img/11-delegated-permissions.png)

4. Add the following five permissions (search by name, tick the checkbox, click **Add permissions**):
   - `ChatMessage.Read` — read chat messages

     ![Add ChatMessage.Read](tools/img/12-add-chatmessage-read.png)

   - `Chat.Read` — read user's 1:1 and group chats

     ![Add Chat.Read](tools/img/13-add-chat-read.png)

   - `offline_access` (under *OpenId permissions*) — keep refresh tokens

     ![Add offline_access](tools/img/14-add-offline-access.png)

   - `Chat.ReadWrite` — create chats and modify chat content

     ![Add Chat.ReadWrite](tools/img/15-add-chat-readwrite.png)

   - `ChatMessage.Send` — send messages on the user's behalf

     ![Add ChatMessage.Send](tools/img/16-add-chatmessage-send.png)

5. Verify the final list — all six permissions present:

   ![Permissions final list](tools/img/17-permissions-final-list.png)

### What happened

You should now see six permissions in the list. The **Admin consent required = No** column for each one means you do **not** need an IT ticket — the consent will be granted interactively by you on first sign-in.

If your tenant flags any as "admin consent required", click **Grant admin consent for `<tenant>`** (button at the top). If it is greyed out, you must request admin consent through your normal IT channel — this varies by company.

---

## Part 3: Issue Secrets

### What we'll do
Capture the three Azure values into a local `.env` file, plus a GitHub Personal Access Token for the LLM call.

### Action

1. **Optional:** Create an `AZURE_CLIENT_SECRET` — App Registration → **Certificates & secrets → + New client secret**. The secret is shown only once; copy it immediately. **For the device-code flow used in this module, the secret is NOT required.** Generate it only if your future code paths might switch to a confidential client.

   ![Certificates & secrets menu](tools/img/06-certificates-secrets-menu.png)

   ![Client secret added](tools/img/07-client-secret-added.png)

   ![Client secret value (copy now — shown only once!)](tools/img/08-client-secret-value.png)

2. Create a GitHub PAT for GitHub Models:
   - Open https://github.com/settings/tokens → **Generate new token (classic)**.

     ![GitHub PAT page](tools/img/18-github-pat-page.png)

   - Pick a sensible expiration (30-90 days for personal automation):

     ![GitHub PAT expiration](tools/img/19-github-pat-expiration.png)

   - **Scopes:** only `read:user` is needed for GitHub Models access.

     ![GitHub PAT read:user scope](tools/img/20-github-pat-readuser-scope.png)

   - Copy the token immediately (shown once).

     ![GitHub PAT created](tools/img/21-github-pat-created.png)
3. In the cloned repository, copy [tools/.env.example](tools/.env.example) to `tools/.env` and fill in:
   - `AZURE_TENANT_ID` ← Directory (tenant) ID
   - `AZURE_CLIENT_ID` ← Application (client) ID
   - `GITHUB_TOKEN` ← the GitHub PAT
   - Leave `NOTIFICATION_CHAT_ID` empty for now — we will populate it in [Part 7](#part-7-create-the-notification-chat).
4. Verify `.env` is gitignored (`.gitignore` in the tools folder already lists it).

### What happened
You now have all secrets for the Azure side and the LLM side stored locally and outside of Git. Never commit `.env`.

---

## Part 4: Run the Smoke Test in Docker

### What we'll do
Build the Docker image and run the smoke test, which calls `GET /me` via Microsoft Graph using MSAL device-code authentication.

### Action

From the `tools/` folder:

```powershell
docker compose run --rm smoke
```

Docker will build the image (~30 seconds first time) and then print a device-code prompt:

![Device code request in terminal](tools/img/22-device-code-request.png)

```
To sign in, use a web browser to open the page https://login.microsoftonline.com/device
and enter the code XXXXXXXXX to authenticate.
```

1. Open the URL, enter the code:

   ![Enter device code in browser](tools/img/24-device-code-entered.png)

2. Sign in with your corporate account. On the **Permissions requested** screen, click **Accept**.
3. The browser confirms a successful sign-in:

   ![Signed in successfully](tools/img/23-signed-in-successfully.png)

4. Return to the terminal — the script will print your `displayName`, `mail`, and `id`.

### What happened
You completed the first end-to-end auth round-trip. MSAL also persisted the token to `/data/token_cache.bin` (mounted from `./data` on your host). All future runs will refresh silently — no more device codes — until the refresh token chain expires.

---

## Part 5: Fix Public Client Flow

### What we'll do
If the smoke test fails with `AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'`, fix the App Registration so the device-code flow is allowed.

### Why this happens
Even though you registered the app as `Public client/native`, Azure has an explicit toggle called **Allow public client flows** that must be turned on separately. Without it, Azure treats the app as confidential and refuses device-code authentication.

### Action

1. App Registration → **Authentication (Preview)**.
2. Scroll to **Settings** tab → **Allow public client flows** → switch to **Yes**.
3. Click **Save** at the top — this is easy to forget; the change does nothing until you save.

   ![Allow public client flows = Yes](tools/img/25-allow-public-client-flows.png)

4. Re-run `docker compose run --rm smoke`.

### What happened
Your app is now correctly configured as a public client and can complete device-code authentication.

---

## Part 6: List Your Chats

### What we'll do
Use the cached token (no device code needed!) to list your top 20 Teams chats.

### Action

```powershell
docker compose run --rm list-chats
```

### What happened
You should see a numbered list of chats with `chatType` (`oneOnOne`, `group`, `meeting`), `lastUpdatedDateTime`, topic / participant names, and the Graph `id`. Save the `id` of one chat — you will read messages from it in [Part 8](#part-8-read-messages).

The script ([list_chats.py](tools/list_chats.py)) calls `GET /me/chats?$top=20&$expand=members&$orderby=lastMessagePreview/createdDateTime desc`.

---

## Part 7: Create the Notification Chat

### What we'll do
Create a private Teams chat that will receive AI-generated summaries — your "AI assistant inbox".

### Why a `group` chat with one participant
Microsoft Graph does not allow you to create a `oneOnOne` chat with yourself. The well-known workaround is to create a `group` chat with a single member (you) and a custom `topic`. Only you see it.

### Action

```powershell
docker compose run --rm app python create_notification_chat.py
```

The script is **idempotent** — if a chat with the same topic already exists, it returns that one. The output ends with:

```
Add to .env:
  NOTIFICATION_CHAT_ID=19:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@thread.v2
```

1. Copy that line into your `tools/.env`.
2. Open Teams — the new chat **AI Teams Summaries** appears in your chat list:

   ![Notification chat in Teams](tools/img/26-notification-chat-in-teams.png)

---

## Part 8: Read Messages

### What we'll do
Fetch the latest N messages from any chat by its Graph id.

### Action

```powershell
docker compose run --rm app python read_messages.py "<CHAT_ID>" --top 20
```

Replace `<CHAT_ID>` with one of the ids printed in Part 6. The script ([read_messages.py](tools/read_messages.py)) handles HTML stripping, sender resolution, and timestamps.

### What happened
You have proven that the Graph chat-message endpoint works with your token. You may also notice some messages with empty bodies or `messageType = unknownFutureValue` — those are attachments (files, images), system events, or message types newer than the SDK enumeration. They are safe to ignore for the summary use case.

---

## Part 9: Summarize a Chat and Post Back to Teams

### What we'll do
Run the full pipeline: read messages → call GitHub Models (`gpt-4o`) → post the summary into the notification chat.

### Action

```powershell
docker compose run --rm --build app python summarize_and_notify.py "<SOURCE_CHAT_ID>" --top 20
```

The `--build` flag rebuilds the image so any new `.py` script is included. Use it once after adding new scripts; subsequent runs do not need it.

### What happened

1. The script ([summarize_and_notify.py](tools/summarize_and_notify.py)) fetched 20 messages and built a plain transcript (oldest first, HTML stripped).
2. It called `POST $LLM_ENDPOINT/chat/completions` with a system prompt asking for a 3-7 bullet summary in your language.
3. It converted the markdown bullets to small Teams HTML and called `POST /me/chats/{NOTIFICATION_CHAT_ID}/messages`.

Open Teams → **AI Teams Summaries** — you should see a new message titled `AI summary (20 messages from <chat id>)` with the bullets:

![Summary received in Teams](tools/img/27-summary-received-in-teams.png)

This is your first complete read → summarize → write loop. From here you can extend in many directions — see [Next Steps](#next-steps).

---

## Part 10: Sanitize Artifacts Before Sharing

### What we'll do
Audit every tracked file for personally identifiable information (PII) and organizational identifiers before pushing the work to a shared repository.

### Why
The `data/token_cache.bin`, `.env`, the original transcript file, and screenshots all contain identifying information that must never end up in version control. Even your iterative-prompt log will contain real chat ids, names, and possibly URLs.

### Action

1. Verify `.gitignore` includes `.env`, `data/`, and any local transcript / screenshot files you do not intend to publish.
2. Run a regex scan for common PII / org markers:
   ```powershell
   Select-String -Path tools/* -Pattern '<your-name>|<your-org>|<your-domain>|<known-coworker-names>'
   ```
3. For markdown logs you do want to publish (e.g. a `main.prompt.md` style trail), batch-replace:
   - Personal names → `Stiven Pupkin`
   - Email → `stiven_pupkin@example.com`
   - Org → `ACME`
   - GUIDs → `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - Chat ids → `19:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@thread.v2`
   - Device codes → `XXXXXXXXX`
4. **PNG screenshots cannot be auto-redacted.** Either delete them before publishing or manually obscure (Snipping Tool → Highlight) any tokens, ids, names, and tenant-specific URLs.

### What happened
Your tracked artifacts are safe to share. The local `.env`, token cache, and original transcript stay on your machine, gitignored.

---

## Part 11: Download a Meeting Transcript via Graph (optional)

### What we'll do
Skip the manual "Download transcript" click in the Teams UI — pull the `.docx` (or `.vtt`) straight from the Graph API.

### Why
If you want to automate transcript ingestion, scheduled summaries, or pipe the file into [620 — Microsoft Teams Meeting Transcription](../620-meeting-transcription/about.md) without a human download step, the API gives you a stable handle.

### Action

1. Add two more delegated permissions to the App Registration (Part 2 pattern):
   - `OnlineMeetings.Read`
   - `OnlineMeetingTranscript.Read.All`

   Grant consent (admin consent may be required by tenant policy).
2. Run [download_transcript.py](tools/download_transcript.py):
   ```powershell
   docker compose run --rm app python download_transcript.py `
     --join-url "<paste teams meeting join URL>" `
     --format docx `
     --out /data/meeting.docx
   ```
   First run triggers a **new** device-code flow because the scopes differ from `graph_auth.py` — the script uses its own MSAL client.
3. To list available transcripts on a meeting first (helpful when there are several recordings):
   ```powershell
   docker compose run --rm app python download_transcript.py --join-url "<URL>" --list
   ```
4. Use `--format vtt` if you want the WebVTT subtitle file instead of `.docx`.

### What happened
You have a `meeting.docx` produced by the API, byte-equivalent to the one you'd get from the Teams UI. Hand it off to module 620 to extract anonymized text and feed it to the summarizer from Part 9.

> ℹ️ Both transcript scopes are **separate** from the chat scopes used elsewhere in this module. Adding them does not invalidate the existing token cache; you simply get a second cached account entry.

---

## Success Criteria

- ✅ App Registration exists in your Entra ID tenant with `Allow public client flows = Yes`
- ✅ Six Microsoft Graph delegated permissions added; consent granted (interactively or by admin)
- ✅ `tools/.env` populated with `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `GITHUB_TOKEN`, `NOTIFICATION_CHAT_ID`
- ✅ `docker compose run --rm smoke` prints your `displayName` from `GET /me`
- ✅ MSAL token cache exists at `tools/data/token_cache.bin` and is **not** committed to Git
- ✅ `docker compose run --rm list-chats` prints your top 20 chats
- ✅ `docker compose run --rm app python read_messages.py "<id>" --top 20` reads messages from a chosen chat
- ✅ A new chat **AI Teams Summaries** appears in your Teams client
- ✅ A summary message is posted into that chat by `summarize_and_notify.py`
- ✅ A regex scan of tracked files finds no PII / org identifiers

## Understanding Check

1. **Why must `Allow public client flows` be enabled even though we picked "Public client/native" at registration?**
   *Expected:* The platform type sets the redirect URI category, but Azure has a separate runtime toggle that controls whether device-code (and other public flows) are allowed. Both are required.
2. **Why do we cache the MSAL token on a Docker volume rather than inside the container?**
   *Expected:* So that the token survives container restarts and `--rm` runs. Without persistence the user would have to re-authenticate every run.
3. **What is the difference between `chatType = group` and `chatType = oneOnOne`, and why do we use `group` for the notification chat?**
   *Expected:* Graph forbids creating a `oneOnOne` with only yourself. A `group` with a single member is the documented workaround.
4. **Why use GitHub Models (`gpt-4o`) instead of GitHub Copilot for the summarization step?**
   *Expected:* GitHub Models bills per token without burning Copilot premium-request quota; for a background batch job this is far cheaper, and quality is comparable for short summaries.
5. **What categories of secrets/PII must never be committed in this module?**
   *Expected:* `AZURE_CLIENT_SECRET`, `GITHUB_TOKEN`, MSAL token cache, original transcript files, screenshots with personal data, real chat ids, real GUIDs.
6. **Which scope alone would let you only **read** chats and not post anything?**
   *Expected:* `Chat.Read` + `ChatMessage.Read` (plus `User.Read` and `offline_access`). Drop `Chat.ReadWrite` and `ChatMessage.Send`.
7. **Why is the `AZURE_CLIENT_SECRET` optional in this setup?**
   *Expected:* The device-code flow uses the public client model and does not send a client secret. The secret is only useful if you later switch to a confidential client variant.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `AADSTS7000218: client_assertion or client_secret` | Public client flows not enabled | Part 5: Authentication → Allow public client flows = Yes → **Save** |
| `AADSTS65001: user or admin has not consented` | Consent not granted | Sign in interactively and click **Accept** on the permissions screen, or have an admin grant consent |
| `AADSTS70011: invalid scope` | Typo or unsupported scope | Verify scopes match the exact strings; do not include `openid`/`profile`/`offline_access` manually — MSAL adds them |
| `failed to compute cache key: ".../requirements.txt": not found` | `.dockerignore` excludes `*.txt` | Add `!requirements.txt` exception |
| `python: can't open file '/app/<new>.py'` | Image was not rebuilt after adding the script | Use `docker compose run --rm --build app ...` once |
| `KeyError: 'NOTIFICATION_CHAT_ID'` | `.env` not loaded or variable missing | Confirm `.env` exists in `tools/` and `env_file: .env` is set in compose |
| `HTTP 403 Forbidden` from Graph | Missing scope or consent revoked | Re-check API permissions; delete `data/token_cache.bin` and re-authenticate |
| Empty message bodies in `read_messages` output | Attachment-only / system messages | Skip messages where `body.content` is empty; inspect `attachments[]` if needed |

## When to Use

- You want a personal AI assistant that summarizes high-volume Teams chats while you focus on deep work
- You want a reference implementation for any other Microsoft Graph integration (mail, calendar, files, OneDrive)
- You are evaluating GitHub Models vs Copilot premium requests for an automation use case

## Next Steps

After completing this module:

- Extend `summarize_and_notify.py` to remember the last seen message id per chat (incremental summaries instead of full re-read every run)
- Add a polling loop (cron or `time.sleep` inside the container) for hands-free operation
- Aggregate multiple chats into a single daily digest
- Move on to [185 — Prompt Templates for Dynamic Queries](../185-prompt-templates-dynamic-queries/about.md) to refine the LLM prompt with structured templates
- Or to [196 — Reverse Engineering Project Knowledge](../196-reverse-engineering-project-knowledge/about.md) to extract conventions from the chats you now have programmatic access to
