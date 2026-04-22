"""
Read recent messages from a Microsoft Teams chat.

Usage:
    python read_messages.py CHAT_ID [--top N]

Example:
    python read_messages.py 19:meeting_xxx@thread.v2 --top 30

Calls GET /me/chats/{chatId}/messages?$top=N&$orderby=createdDateTime desc
and prints each message: timestamp, sender, content (HTML stripped).
"""

import argparse
import re
import sys
from datetime import datetime, timezone

import requests

from graph_auth import get_access_token

GRAPH = "https://graph.microsoft.com/v1.0"
DEFAULT_TOP = 20
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")


def fmt_when(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except ValueError:
        return iso


def strip_html(s: str | None) -> str:
    if not s:
        return ""
    text = TAG_RE.sub("", s)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    text = WS_RE.sub(" ", text).strip()
    return text


def sender_name(msg: dict) -> str:
    frm = msg.get("from") or {}
    user = frm.get("user") or {}
    name = user.get("displayName")
    if name:
        return name
    app = frm.get("application") or {}
    if app.get("displayName"):
        return f"[bot] {app['displayName']}"
    if msg.get("messageType") == "systemEventMessage":
        return "[system]"
    return "?"


def main() -> None:
    parser = argparse.ArgumentParser(description="Read recent messages from a Teams chat.")
    parser.add_argument("chat_id", help="Graph chat id (from list_chats.py)")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP, help=f"Number of messages (default {DEFAULT_TOP})")
    args = parser.parse_args()

    token = get_access_token()
    url = f"{GRAPH}/me/chats/{args.chat_id}/messages?$top={args.top}"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    if resp.status_code != 200:
        print(f"HTTP {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    msgs = resp.json().get("value", [])
    print(f"\n=== {len(msgs)} message(s) in {args.chat_id} (newest first) ===\n")

    for msg in msgs:
        when = fmt_when(msg.get("createdDateTime"))
        who = sender_name(msg)
        body = msg.get("body") or {}
        text = strip_html(body.get("content"))
        if not text and msg.get("messageType") != "message":
            text = f"({msg.get('messageType')})"
        print(f"[{when}] {who}:")
        for line in (text or "").splitlines() or [""]:
            print(f"    {line}")
        print()


if __name__ == "__main__":
    main()
