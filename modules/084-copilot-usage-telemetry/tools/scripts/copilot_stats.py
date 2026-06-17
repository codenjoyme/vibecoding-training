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
from pathlib import Path

import requests
from dotenv import load_dotenv


def _find_env_file():
    """Locate a .env by walking UP from two anchors: the current working
    directory and this script's directory. First match wins.

    This makes the script work no matter where you run it from — a local
    .env next to the script, or the repo-root .env several levels up.
    """
    override = os.getenv("COPILOT_ENV_FILE")
    if override:
        return override
    anchors = [Path.cwd(), Path(__file__).resolve().parent]
    for anchor in anchors:
        for folder in [anchor, *anchor.parents]:
            candidate = folder / ".env"
            if candidate.is_file():
                return str(candidate)
    return None


_env_file = _find_env_file()
if _env_file:
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
        "quota_reset_date_utc": data.get("quota_reset_date_utc"),
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
        overage = snap.get("overage_count")
        overage_ok = snap.get("overage_permitted")
        used_pct = round(100 - pct, 1) if isinstance(pct, (int, float)) else "?"
        print(
            f"  {name:22} used={used_pct}%  remaining={remaining}/{entitled}  "
            f"unlimited={unlimited}  overage={overage} (permitted={overage_ok})"
        )


def cmd_info(args):
    """Maximum info: everything useful the copilot_internal/user endpoint exposes."""
    _require_token()
    data = api_get("/copilot_internal/user")

    if args.format == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    def line(label, value):
        print(f"  {label:26} {value}")

    print("== Account / plan ==")
    for k in ("login", "copilot_plan", "access_type_sku", "token_based_billing",
              "assigned_date", "quota_reset_date", "quota_reset_date_utc",
              "can_upgrade_plan", "is_staff"):
        if k in data:
            line(k, data[k])

    print("\n== Feature flags ==")
    for k in sorted(data):
        if k.endswith("_enabled") or k in ("copilotignore_enabled", "is_mcp_enabled"):
            line(k, data[k])

    orgs = data.get("organization_list") or []
    if orgs:
        print("\n== Organizations ==")
        for o in orgs:
            line(o.get("login", "?"), o.get("name"))

    eps = data.get("endpoints") or {}
    if eps:
        print("\n== Regional endpoints ==")
        for name, url in eps.items():
            line(name, url)

    snapshots = data.get("quota_snapshots") or {}
    if snapshots:
        print("\n== Quota snapshots (full) ==")
        for name, snap in snapshots.items():
            print(f"  [{name}]")
            if isinstance(snap, dict):
                for sk in sorted(snap):
                    print(f"      {sk:22} {snap[sk]}")
            else:
                print(f"      {snap}")


def cmd_raw(args):
    """Dump the full copilot_internal/user response (for exploration).

    The token itself is never part of this response, but review before sharing.
    """
    _require_token()
    data = api_get("/copilot_internal/user")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _add_format_arg(p):
    p.add_argument(
        "--format", choices=["table", "json"], default=None,
        help="output format (default: table)",
    )


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
    # Global --format so it works either before or after the subcommand.
    parser.add_argument(
        "--format", choices=["table", "json"], default="table",
        help="output format (default: table)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("credits", "show credit/quota snapshot (the status-bar number)"),
        ("info", "show MAX info the endpoint exposes (plan, flags, orgs, endpoints, quotas)"),
        ("raw", "dump full copilot_internal/user JSON"),
        ("token-info", "show copilot token metadata + quota (token redacted)"),
    ):
        p = sub.add_parser(name, help=help_text)
        _add_format_arg(p)

    args = parser.parse_args()
    # A subcommand-level --format overrides the global default when provided.
    if getattr(args, "format", None) is None:
        args.format = "table"

    handlers = {
        "credits": cmd_credits,
        "info": cmd_info,
        "raw": cmd_raw,
        "token-info": cmd_token_info,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
