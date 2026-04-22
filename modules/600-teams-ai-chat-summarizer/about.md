# Microsoft Teams AI Chat Summarizer

**Duration:** 30-45 minutes
**Skill:** Build a Dockerized Python app that authenticates to Microsoft Entra ID, reads your Teams chats via Microsoft Graph, summarizes them with an LLM, and posts the summary back into a dedicated Teams chat.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Registering an application in Microsoft Entra ID (Azure AD) without admin tickets
- Choosing the right Microsoft Graph delegated permissions for chat read/write
- MSAL device-code authentication flow for headless / Dockerized apps
- Persisting an MSAL token cache across container restarts via Docker volumes
- Reading chats and messages with Microsoft Graph (`/me/chats`, `/me/chats/{id}/messages`)
- Creating a self-only "notification chat" as an AI assistant inbox
- Summarizing chat content with GitHub Models (`gpt-4o`) and posting HTML back into Teams
- Sanitizing PII / organizational identifiers before publishing artifacts

## Learning Outcome

You can wire any custom Python application to Microsoft Teams using Microsoft Graph, run it in Docker, and ship a real end-to-end automation: read a chat → summarize with an LLM → post the result back into Teams. You also know which secrets must never leave the machine and how to scrub PII from intermediate artifacts before sharing them.

## Prerequisites

### Required Modules

- [108 — Token & API Key Management](../108-token-api-key-management/about.md)
- [110 — Development Environment Setup](../110-development-environment-setup/about.md)
- [058 — Workspace Kickoff Prompt Files](../058-workspace-kickoff-prompt-files/about.md) *(optional, recommended)*

### Required Skills & Tools

- A corporate Microsoft 365 / Entra ID account that allows self-service App Registrations (no admin ticket required for `Chat.Read`, `ChatMessage.Read`, `Chat.ReadWrite`, `ChatMessage.Send`, `offline_access`)
- Docker Desktop running locally
- A GitHub account with access to GitHub Models (free tier is enough)
- Basic Python knowledge

## When to Use

- You want to build a personal AI assistant on top of your own Teams chats
- You need a working reference for any Microsoft Graph integration (mail, calendar, files — same auth pattern)
- You want a worked example of MSAL device-code flow inside Docker
- You want to compare the cost and ergonomics of GitHub Models vs Copilot premium requests for an automation use case

## Resources

- [Tools, scripts & screenshots](tools/readme.md) — drop-in starter kit produced by this module
- [SKILL.md](tools/SKILL.md) — concise LLM-targeted instruction to reproduce the setup
- [Microsoft Graph REST API reference](https://learn.microsoft.com/en-us/graph/api/overview)
- [MSAL Python documentation](https://learn.microsoft.com/en-us/entra/msal/python/)
- [GitHub Models endpoint](https://github.com/marketplace/models)
