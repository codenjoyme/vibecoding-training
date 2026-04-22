"""
List your top Microsoft Teams chats.

Calls GET /me/chats?$top=20&$expand=members&$orderby=lastUpdatedDateTime desc
and prints a compact summary per chat:
  - id (Graph chat id)
  - chatType (oneOnOne / group / meeting)
  - topic or member names
  - lastUpdatedDateTime

Use the printed id later as a target for reading or sending messages.
"""

from datetime import datetime, timezone

import requests

from graph_auth import get_access_token

GRAPH = "https://graph.microsoft.com/v1.0"
TOP = 20


def fmt_when(iso: str | None) -> str:
    if not iso:
        return "—"
    # Trim trailing Z and fractional seconds to a stable width.
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return iso


def chat_label(chat: dict) -> str:
    topic = chat.get("topic")
    if topic:
        return topic
    members = chat.get("members", []) or []
    names = [m.get("displayName") or m.get("email") or "?" for m in members]
    return ", ".join(names) if names else "(no members)"


def main() -> None:
    token = get_access_token()

    url = f"{GRAPH}/me/chats?$top={TOP}&$expand=members&$orderby=lastMessagePreview/createdDateTime desc"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    if resp.status_code != 200:
        print(f"HTTP {resp.status_code}")
        print(resp.text)
        raise SystemExit(1)

    chats = resp.json().get("value", [])
    print(f"\n=== {len(chats)} chat(s) ===\n")

    for i, chat in enumerate(chats, 1):
        chat_id = chat.get("id", "")
        chat_type = chat.get("chatType", "?")
        when = fmt_when(chat.get("lastUpdatedDateTime"))
        label = chat_label(chat)
        print(f"[{i:>2}] {chat_type:<10} {when}")
        print(f"     {label}")
        print(f"     id: {chat_id}")
        print()


if __name__ == "__main__":
    main()
