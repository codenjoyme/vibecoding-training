#!/usr/bin/env python3
"""Copilot usage telemetry — pull AI-credit / quota statistics from GitHub's
private Copilot endpoints (no UI, no screenshots).

Experimental script for module 084. Right now it focuses on ONE goal:
fetch the credit/quota snapshot that the Copilot status bar shows on hover.

Data source discovered by reverse-engineering the Copilot extension bundle:
    GET https://api.github.com/copilot_internal/user
        Authorization: token <github_token>
        X-GitHub-Api-Version: 2025-04-01
    -> JSON containing `quota_snapshots` and `quota_reset_date`.

The token is read from COPILOT_GITHUB_TOKEN in a .env file (searched upward
from CWD, so the repo-root .env is found). The token is never printed.
"""

import argparse
import json
import os
import sys

import requests
from dotenv import find_dotenv, load_dotenv

# Search for .env from CWD upward (finds repo-root .env if no local one exists).
_env_file = os.getenv("COPILOT_ENV_FILE") or find_dotenv(usecwd=True) or ".env"
load_dotenv(_env_file)

TOKEN = os.getenv("COPILOT_GITHUB_TOKEN", "").strip()
API_BASE = os.getenv("COPILOT_API_BASE", "https://api.github.com").rstrip("/")
API_VERSION = "2025-04-01"


def _require_token():
    if not TOKEN:
        sys.exit(
            "ERROR: COPILOT_GITHUB_TOKEN is not set.\n"
            "Create a .env (repo root or next to this script) with:\n"
            "  COPILOT_GITHUB_TOKEN=ghp_xxx\n"
            "See .env.example for the template."
        )


def _headers():
    return {
        "Authorization": f"token {TOKEN}",
        "X-GitHub-Api-Version": API_VERSION,
        "Accept": "application/json",
        # The endpoint is internal to the editor integration; identify like the plugin.
        "Editor-Version": "vscode/1.120.0",
        "Editor-Plugin-Version": "copilot-chat/0.0.0",
        "User-Agent": "copilot-usage-telemetry/0.1",
    }


def _redact_token_hint():
    """Return a non-secret fingerprint of the token for debugging (prefix + length)."""
    if not TOKEN:
        return "<empty>"
    prefix = TOKEN[:4]
    return f"prefix='{prefix}…' length={len(TOKEN)}"


def api_get(path):
    url = f"{API_BASE}{path}"
    try:
        resp = requests.get(url, headers=_headers(), timeout=20)
    except requests.RequestException as e:
        sys.exit(f"ERROR: network failure calling {path}: {e}")

    if resp.status_code == 401:
        sys.exit(
            "ERROR: 401 Unauthorized — the token was rejected by GitHub.\n"
            f"  Token fingerprint: {_redact_token_hint()}\n"
            "  The Copilot quota endpoint needs a token from a Copilot-enabled account.\n"
            "  Try generating a classic GitHub PAT (no extra scopes required for read)\n"
            "  at https://github.com/settings/tokens and put it in COPILOT_GITHUB_TOKEN."
        )
    if resp.status_code == 403:
        sys.exit(
            "ERROR: 403 Forbidden — token authenticated but lacks access to this endpoint.\n"
            f"  Token fingerprint: {_redact_token_hint()}\n"
            "  This usually means the account has no active Copilot subscription,\n"
            "  or the token type is not accepted for copilot_internal.\n"
            f"  Raw response: {resp.text[:300]}"
        )
    if resp.status_code == 404:
        sys.exit(
            "ERROR: 404 Not Found — endpoint path rejected.\n"
            f"  Raw response: {resp.text[:300]}"
        )
    if not resp.ok:
        sys.exit(f"ERROR: {resp.status_code} — {resp.text[:300]}")

    try:
        return resp.json()
    except ValueError:
        sys.exit(f"ERROR: response was not JSON:\n{resp.text[:300]}")


def cmd_credits(args):
    """Fetch and display the credit/quota snapshot."""
    _require_token()
    data = api_get("/copilot_internal/user")

    snapshots = data.get("quota_snapshots")
    reset_date = data.get("quota_reset_date")
    plan = data.get("copilot_plan") or data.get("access_type_sku")

    out = {
        "copilot_plan": plan,
        "quota_reset_date": reset_date,
        "quota_snapshots": snapshots,
    }

    if args.format == "json":
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # table format
    print(f"Plan:        {plan}")
    print(f"Reset date:  {reset_date}")
    if not snapshots:
        print("\nNo quota_snapshots in response. Full keys returned:")
        print("  " + ", ".join(sorted(data.keys())))
        return
    print("\nQuota snapshots:")
    for name, snap in snapshots.items():
        if not isinstance(snap, dict):
            print(f"  {name}: {snap}")
            continue
        pct = snap.get("percent_remaining")
        entitled = snap.get("entitlement")
        remaining = snap.get("remaining")
        unlimited = snap.get("unlimited")
        used_pct = (100 - pct) if isinstance(pct, (int, float)) else "?"
        print(
            f"  {name:18} used={used_pct}%  remaining={remaining}  "
            f"entitlement={entitled}  unlimited={unlimited}"
        )


def cmd_raw(args):
    """Dump the full copilot_internal/user response (for exploration).

    The token itself is never part of this response, but review before sharing.
    """
    _require_token()
    data = api_get("/copilot_internal/user")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_token_info(args):
    """Exchange for a Copilot token; its body also carries quota fields."""
    _require_token()
    data = api_get("/copilot_internal/v2/token")
    # Strip the actual token value before printing — keep only metadata.
    safe = {k: v for k, v in data.items() if k != "token"}
    safe["token"] = "<redacted>" if data.get("token") else None
    print(json.dumps(safe, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description="Pull Copilot credit/quota statistics from GitHub's private endpoints."
    )
    parser.add_argument(
        "--format", choices=["table", "json"], default="table",
        help="output format (default: table)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("credits", help="show credit/quota snapshot (the status-bar number)")
    sub.add_parser("raw", help="dump full copilot_internal/user JSON")
    sub.add_parser("token-info", help="show copilot token metadata + quota (token redacted)")

    args = parser.parse_args()

    handlers = {
        "credits": cmd_credits,
        "raw": cmd_raw,
        "token-info": cmd_token_info,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
