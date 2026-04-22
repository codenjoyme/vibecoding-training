"""
Create a dedicated Microsoft Teams notification chat for AI summaries.

Strategy:
  Microsoft Graph does not allow creating a 'oneOnOne' chat with only yourself.
  Workaround: create a 'group' chat with a single member (you), with a topic.
  This becomes a private "inbox" channel that only you see.

Usage:
    python create_notification_chat.py [--topic "AI Teams Summaries"]

Prints the new chat id. Copy it into .env as NOTIFICATION_CHAT_ID.
If a chat with this exact topic already exists, prints that one instead
(idempotent — safe to run multiple times).
"""

import argparse
import sys

import requests

from graph_auth import get_access_token

GRAPH = "https://graph.microsoft.com/v1.0"
DEFAULT_TOPIC = "AI Teams Summaries"


def get_my_user_id(token: str) -> str:
    resp = requests.get(
        f"{GRAPH}/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def find_existing(token: str, topic: str) -> str | None:
    """Return chat id if a group chat with this exact topic already exists."""
    resp = requests.get(
        f"{GRAPH}/me/chats?$filter=chatType eq 'group'&$top=50",
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    if resp.status_code != 200:
        return None
    for chat in resp.json().get("value", []):
        if chat.get("topic") == topic:
            return chat.get("id")
    return None


def create_chat(token: str, topic: str, my_user_id: str) -> str:
    payload = {
        "chatType": "group",
        "topic": topic,
        "members": [
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{my_user_id}')",
            }
        ],
    }
    resp = requests.post(
        f"{GRAPH}/chats",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )
    if resp.status_code not in (200, 201):
        print(f"HTTP {resp.status_code}")
        print(resp.text)
        sys.exit(1)
    return resp.json()["id"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a notification chat in Teams.")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help=f"Chat topic (default: '{DEFAULT_TOPIC}')")
    args = parser.parse_args()

    token = get_access_token()

    existing = find_existing(token, args.topic)
    if existing:
        print(f"\nChat with topic '{args.topic}' already exists.")
        print(f"  id: {existing}\n")
        print("Add to .env:")
        print(f"  NOTIFICATION_CHAT_ID={existing}")
        return

    my_id = get_my_user_id(token)
    chat_id = create_chat(token, args.topic, my_id)

    print(f"\nCreated chat '{args.topic}'.")
    print(f"  id: {chat_id}\n")
    print("Add to .env:")
    print(f"  NOTIFICATION_CHAT_ID={chat_id}")


if __name__ == "__main__":
    main()
