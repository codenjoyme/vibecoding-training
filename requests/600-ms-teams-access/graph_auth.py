"""
Shared MSAL device-code authentication for Microsoft Graph.

Usage:
    from graph_auth import get_access_token
    token = get_access_token()

The token is cached on disk (/data/token_cache.bin) and refreshed silently
on subsequent runs. Only the first run requires interactive device-code login.
"""

import json
import os
import sys

from dotenv import load_dotenv
from msal import PublicClientApplication, SerializableTokenCache

load_dotenv()

TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]

# Resource scopes only — MSAL adds openid / profile / offline_access automatically.
SCOPES = [
    "User.Read",
    "Chat.Read",
    "ChatMessage.Read",
    "Chat.ReadWrite",
    "ChatMessage.Send",
]

CACHE_PATH = "/data/token_cache.bin"


def _load_cache() -> SerializableTokenCache:
    cache = SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache.deserialize(f.read())
    return cache


def _save_cache(cache: SerializableTokenCache) -> None:
    if not cache.has_state_changed:
        return
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        f.write(cache.serialize())


def get_access_token() -> str:
    """Return a valid Microsoft Graph access token. Triggers device flow on first run."""
    cache = _load_cache()
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )

    result = None
    for account in app.get_accounts():
        result = app.acquire_token_silent(SCOPES, account=account)
        if result:
            break

    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            print("Failed to start device flow:")
            print(json.dumps(flow, indent=2))
            sys.exit(1)
        print(flow["message"], flush=True)
        result = app.acquire_token_by_device_flow(flow)

    _save_cache(cache)

    if "access_token" not in result:
        print("Authentication failed:")
        print(json.dumps(result, indent=2))
        sys.exit(1)

    return result["access_token"]
