"""
Smoke test — verify Azure App Registration + Microsoft Graph access.

Calls GET /me and prints basic profile fields. If this works, the Azure side
is wired correctly and other scripts (list_chats.py, ...) will work too.
"""

import requests

from graph_auth import get_access_token

GRAPH = "https://graph.microsoft.com/v1.0"


def main() -> None:
    token = get_access_token()
    print("\n=== Authenticated! Calling GET /me ... ===\n", flush=True)

    resp = requests.get(
        f"{GRAPH}/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    me = resp.json()

    print(f"  displayName:       {me.get('displayName')}")
    print(f"  mail:              {me.get('mail')}")
    print(f"  userPrincipalName: {me.get('userPrincipalName')}")
    print(f"  id:                {me.get('id')}")
    print("\nAzure side is wired up correctly.")


if __name__ == "__main__":
    main()
