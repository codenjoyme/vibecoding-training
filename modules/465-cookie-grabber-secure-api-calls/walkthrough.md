# Cookie Grabber — Secure API Calls - Hands-on Walkthrough

In this module you will build a complete pipeline that lets the AI agent call cookie-protected internal APIs **without ever seeing the cookies**. You'll deploy a Dockerized server, install a Chrome extension, and use a CLI to make authenticated requests.

## Prerequisites

See [module overview](about.md) for full prerequisites list.

---

## What We'll Build

| Component | Where it runs | Purpose |
|-----------|---------------|---------|
| Chrome extension | Browser | Grabs cookies, encrypts them locally with AES-256-GCM, sends to server |
| HTTP + WebSocket server | Docker container | Receives encrypted blob, stores it on disk — never decrypts |
| Python CLI | Host machine | Decrypts cookies with master password, makes API calls for the agent |

The AI agent only sees CLI output (HTTP responses) — never the cookies themselves.

---

## Part 1: Threat Model & Why Encryption Matters

### What we're protecting against

- **AI agent leakage:** if cookies are visible in chat context, they can leak via summarization, logging, or model training
- **Disk exposure:** plaintext cookies on disk can be read by other processes or backed up to cloud storage
- **Network sniffing:** unencrypted WebSocket traffic on local network is readable to anyone on the same LAN

### Why master-password encryption works here

- Cookies are encrypted in the **browser** before leaving — using AES-256-GCM with a key derived from your master password (PBKDF2, 600 000 iterations, SHA-256)
- The server stores the encrypted blob — it has no key, cannot decrypt
- Only the local CLI, with the master password, can decrypt
- The model never sees the master password — it's in your `.env` or typed at the prompt

### When this is appropriate

✅ Internal APIs that only support session cookies  
✅ One-off data extraction tasks  
✅ Local development where you control all components  

❌ Production deployments — use proper API tokens or OAuth instead  
❌ Shared corporate machines — anyone with shell access could read the master password  
❌ APIs where the cookie itself is a long-lived secret of high value — rotate it manually after testing

---

## Part 2: Set Up the Workspace

### What we'll do

Create a working directory under `./workspace/465-task/` and copy the scripts from the module.

1. From your project root, create the working directory:
   - Windows: `mkdir -p workspace/465-task` (or use File Explorer)
   - macOS/Linux: `mkdir -p ./workspace/465-task`

2. Copy the scripts folder into it:
   - Windows: `Copy-Item -Recurse modules/465-cookie-grabber-secure-api-calls/tools/scripts ./workspace/465-task/`
   - macOS/Linux: `cp -r modules/465-cookie-grabber-secure-api-calls/tools/scripts ./workspace/465-task/`

3. Change into the working directory:
   ```
   cd ./workspace/465-task/scripts
   ```

You should now see: `server.py`, `cli.py`, `Dockerfile`, `docker-compose.yml`, `extension/`, two `requirements-*.txt` files, and `.env.example`.

---

## Part 3: Start the Docker Server

### What we'll do

Build and start the HTTP + WebSocket server inside Docker on port 9011. No Python needs to be installed on the host for the server.

1. From `./workspace/465-task/scripts/`, build and start the container:
   ```
   docker compose up -d --build
   ```

2. Verify the server is running:
   ```
   docker compose ps
   ```
   You should see one container in state `running`.

3. Open the status page in your browser: `http://localhost:9011/`
   - You should see the **Cookie Grabber** page with: `❌ No cookies stored yet`
   - There's a download link for `extension.zip`

### Verify

✅ `docker compose ps` shows one running container  
✅ `http://localhost:9011/` loads the status page

---

## Part 4: Install the Chrome Extension

### What we'll do

Load the Chrome extension as an "unpacked" extension so it can read cookies and send them to your local server.

1. From the status page (`http://localhost:9011/`), click **`extension.zip`** to download
2. Unzip to a folder (any location, e.g. `./workspace/465-task/extension-installed/`)
3. In Chrome, open `chrome://extensions`
4. Enable **Developer mode** (top-right toggle)
5. Click **Load unpacked**
6. Select the unzipped folder
7. Pin the extension by clicking the puzzle icon → pin **Cookie Grabber**

### Verify

✅ Extension shows up in `chrome://extensions` as "Cookie Grabber 1.0"  
✅ Cookie Grabber icon is visible in the Chrome toolbar

---

## Part 5: Grab Your First Cookies

### What we'll do

Use the extension popup to grab cookies for a target domain, encrypt them with a master password, and send them to the server.

1. Open the website you want to access (e.g. `https://telescope.example.com/`) and **log in**
2. Click the Cookie Grabber extension icon
3. Fill in the popup:
   - **Target domain:** the domain (e.g. `telescope.example.com`)
   - **WebSocket server URL:** `ws://localhost:9011/ws` (default)
   - **Master password:** any strong password (you'll need it again in the CLI — remember it!)
4. Click **Grab & Send Cookies**

You should see: `✅ Sent N cookies for <domain>` in green.

5. Refresh `http://localhost:9011/` — the page now shows: `✅ Cookies stored — domain: ...`

### What just happened

- The extension read all cookies for the domain via `chrome.cookies.getAll`
- It generated a random salt (32 bytes) and IV (12 bytes)
- It derived a 256-bit AES key from your master password using PBKDF2 (600 000 iterations)
- It encrypted the cookie JSON with AES-256-GCM
- It sent `{domain, salt, iv, encrypted}` (all base64) to the server over WebSocket
- The server saved it to `data/cookies.enc` — **without decrypting**

---

## Part 6: Use the CLI to Make Authenticated Requests

### What we'll do

Install CLI dependencies on the host, then call the protected API.

1. Install CLI dependencies (one-time):
   ```
   pip install -r requirements-cli.txt
   ```

2. Set up your local environment:
   ```
   cp .env.example .env
   ```
   Then open `.env` and set `MASTER_PASSWORD=` to the same password you used in the extension.

3. Check status:
   ```
   python cli.py status
   ```
   Expected: `✅ Cookies stored — Domain: telescope.example.com`

4. Show metadata (no plaintext shown — values stay encrypted):
   ```
   python cli.py info
   ```

5. Make an authenticated GET request:
   ```
   python cli.py get --url https://telescope.example.com/api/v1/me
   ```
   The CLI will:
   - Load `data/cookies.enc`
   - Read `MASTER_PASSWORD` from `.env`
   - Derive the AES key with PBKDF2 (same parameters as the extension)
   - Decrypt cookies in memory
   - Make the HTTP request with cookies attached
   - Print HTTP status + response body

6. Try a POST:
   ```
   python cli.py post --url https://telescope.example.com/api/search --data '{"query": "test"}'
   ```

### Verify

✅ `cli.py status` confirms cookies are stored  
✅ `cli.py get` returns a valid JSON response (not a login redirect)  
✅ The model never saw the cookie values — only the API response

---

## Part 7: Use the Skill from the AI Agent

### What we'll do

Connect the SKILL.md to your AI agent so it can make authenticated requests on your behalf.

1. Open `tools/SKILL.md` in your IDE
2. In Copilot Chat, attach the SKILL.md file as context
3. Ask the agent:

> Using the Cookie Grabber skill, fetch my profile from https://telescope.example.com/api/v1/me and summarize what's in it.

The agent will:
- Run `python cli.py status` to confirm cookies are available
- Run `python cli.py get --url ...`
- Parse the JSON response and present a summary
- Never see or quote the cookie values themselves

---

## Success Criteria

- ✅ Docker container running on port 9011
- ✅ Status page accessible at `http://localhost:9011/`
- ✅ Chrome extension loaded and visible in toolbar
- ✅ Cookies grabbed and encrypted blob stored in `data/cookies.enc`
- ✅ `cli.py status` confirms storage
- ✅ `cli.py get` returns authenticated API response
- ✅ Master password never appears in chat or logs

---

## Understanding Check

Answer these to verify you understood the security model:

1. **Where exactly are cookies decrypted?**  
   Only on the host machine, inside the `cli.py` process — never in the browser (after grab), never on the server, never in chat.

2. **What does the Docker server actually store?**  
   A JSON file with `{salt, iv, ciphertext}` — base64-encoded encrypted blob. It has no key.

3. **Why PBKDF2 with 600 000 iterations?**  
   To make brute-forcing the master password computationally expensive. OWASP 2023 recommendation for SHA-256.

4. **What happens if you lose the master password?**  
   The encrypted file is unrecoverable. Run `cli.py clear` and grab cookies again with a new password.

5. **Why is this safer than putting cookies in `.env`?**  
   `.env` is plaintext on disk. The encrypted blob requires the password (which lives only in your head or in a separate secret store) to be useful.

6. **What stops an attacker who steals `cookies.enc` from getting in?**  
   The master password — without it, AES-256-GCM is computationally infeasible to break.

7. **Could the AI agent ever see the master password?**  
   Only if you put it in chat context (`.env` is fine; pasting plaintext is not). Treat the password the same way you would treat the cookies themselves.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Extension popup shows "WebSocket connection failed" | Server not running. Run `docker compose up -d`. Check firewall isn't blocking port 9011. |
| `cli.py` says "Decryption failed" | Wrong master password. Re-enter, or grab cookies again with a new password. |
| `cli.py get` returns HTML login page | Cookies expired. Re-grab via extension. |
| Extension shows "No cookies found for domain" | You're not logged in to the site, or the domain string is wrong (try with/without `www.`). |
| Server logs show `Invalid JSON from extension` | Extension version mismatch — reload the extension in `chrome://extensions`. |
| `data/cookies.enc` doesn't appear on host | Check Docker volume mount — `docker compose ps` should show port 9011 bound. |

---

## When to Use

- **Internal corporate APIs** that only support session cookies (Telescope, internal Jira/Confluence, dashboards)
- **Quick research tasks** where building a proper OAuth integration is overkill
- **Demos** where you want to show "AI agent uses real authenticated data" without exposing credentials in chat

Avoid for production automation — use proper service accounts and API tokens instead.

---

## Next Steps

- Module **470 — Jira CLI Access** shows the simpler API-token pattern for services that support it
- Module **108 — Token & API Key Management** covers how to store and rotate the master password
- Module **103 — CLI: Command-Line Interface** has the general CLI design principles used here
