# Cookie Grabber — Secure API Calls with Browser Cookies

**Duration:** 15-20 minutes  
**Skill:** Access cookie-protected internal APIs from the AI agent via an encrypted CLI pipeline — without exposing cookies to the model or storing them in plaintext.

**👉 [Start hands-on walkthrough](walkthrough.md)**

---

## Topics

- Why cookies matter for internal API access and why MCP-based approaches are risky
- Architecture: Chrome extension → encrypted WebSocket → Docker server → local CLI
- AES-256-GCM encryption: cookies never leave the browser unencrypted
- Master-password key derivation (PBKDF2) — same password, zero shared secrets on the wire
- Dockerizing the server: HTTP status page + WebSocket endpoint, no Python on the host
- CLI pattern: `status`, `info`, `get`, `post`, `clear` commands
- Security boundaries: what the server sees vs. what the CLI sees

---

## Learning Outcome

You will have a working system where:
1. A Chrome browser extension grabs cookies for any domain and encrypts them locally (AES-256-GCM, PBKDF2 key from master password)
2. The encrypted blob is sent over WebSocket to a Dockerized server — which stores it but **never decrypts it**
3. A local CLI script decrypts cookies with your master password and makes authenticated API calls on behalf of the AI agent
4. The model only sees API responses — never the cookies themselves

---

## Prerequisites

### Required Modules

- [445 — HTTP Client & REST APIs](../445-http-client-rest-apis/about.md) *(optional, recommended)*
- [470 — Jira CLI Access](../470-jira-cli-access/about.md) *(optional — demonstrates the CLI pattern)*

### Required Skills & Tools

- Docker Desktop installed and running
- Google Chrome browser
- Python 3.10+ on the host (for the CLI)
- Basic understanding of cookies and HTTP authentication

---

## When to Use

Use this pattern when:
- The target API requires browser session cookies (not an API token)
- The API has no public token-based auth (internal corporate tools, Telescope, etc.)
- You want the AI agent to query the API without ever seeing the cookies
- You need a reusable, secure pipeline for multiple internal services

Do **not** use this pattern when:
- The API supports API tokens or OAuth — use those instead (simpler, safer)
- You are on a corporate network with strict policies against local WebSocket servers
