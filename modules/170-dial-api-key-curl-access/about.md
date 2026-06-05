# DIAL API Key and cURL Access

**Duration:** 15–20 minutes

**Skill:** Obtain DIAL API key and test connection to AI models using simple cURL requests without programming.

**👉 [Start hands-on walkthrough](walkthrough.md)**

## Topics

- Requesting API key through DIAL support portal
- Understanding REST API basics for AI model access
- Testing DIAL connection with cURL commands
- Listing available models with `test-dial-models-list-windows.ps1` / `test-dial-models-list-linux.sh`
- Verifying API key validity and model availability
- Connecting GitHub Copilot Chat to DIAL via `dial-proxy.py` relay and `chatLanguageModels.json`
- Fixing `Unknown tokenizer` bug in Copilot BYOK integration (`patch_jn.py`)
- Rate limit errors and how to request higher limits via support portal
- Basic troubleshooting of API connection issues

## Learning Outcome

You will successfully request and receive your DIAL API key, then execute a cURL command to query an AI model and receive a response. This validates your access to corporate AI infrastructure without writing any code.

## Prerequisites

### Required Modules

- [080 — Learning from Hallucinations](../080-learning-from-hallucinations/about.md)

### Required Skills & Tools

- Access to DIAL chat interface: https://chat.lab.epam.com/
- Ability to create support tickets on support portal
- Basic command line skills (PowerShell on Windows or Terminal on macOS/Linux)
- VPN connection to company's internal network
- Python 3.11+ and `uv` (for Part 8 — GHCP integration via `dial-proxy.py`)
- No programming knowledge required

## When to Use

- First-time setup for accessing models
- Testing API connectivity before building applications
- Troubleshooting authentication issues
- Validating new API keys after rotation
- Quick ad-hoc queries to AI models without IDE

## Resources

- [DIAL Chat Interface](https://chat.lab.epam.com/)
- [DIAL REST API Documentation](https://epam-rail.com/dial-api)
- Example cURL scripts in `tools/` directory
- GHCP integration scripts in `tools/copilot/` directory (`dial-proxy.py`, `chatLanguageModels.js`)
