"""
Read recent messages from a Teams chat, summarize them via GitHub Models,
and post the summary into the dedicated notification chat.

Usage:
    python summarize_and_notify.py SOURCE_CHAT_ID [--top N]

Required env (in .env):
    AZURE_TENANT_ID, AZURE_CLIENT_ID  - for Microsoft Graph (auto via graph_auth)
    GITHUB_TOKEN                      - for GitHub Models LLM
    LLM_MODEL                         - e.g. "gpt-4o" (default)
    LLM_ENDPOINT                      - e.g. "https://models.inference.ai.azure.com"
    NOTIFICATION_CHAT_ID              - target chat for summaries (from create_notification_chat.py)
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from graph_auth import get_access_token

load_dotenv()

GRAPH = "https://graph.microsoft.com/v1.0"
DEFAULT_TOP = 20
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"[ \t]+")

NOTIFICATION_CHAT_ID = os.environ["NOTIFICATION_CHAT_ID"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "https://models.inference.ai.azure.com").rstrip("/")

SYSTEM_PROMPT = (
    "Ты помогаешь быстро читать переписку из корпоративного чата. "
    "На входе — последние сообщения чата (newest first). "
    "Сделай краткое summary в 3-7 буллетов на русском языке: "
    "о чём говорили, какие решения приняты, какие открытые вопросы, какие важные ссылки/имена упомянуты. "
    "Сохраняй контекст разговора (кто кому что отвечал), не выдумывай. "
    "Будь кратким и по делу."
)


def strip_html(s: str | None) -> str:
    if not s:
        return ""
    text = TAG_RE.sub("", s)
    for esc, ch in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"')):
        text = text.replace(esc, ch)
    return WS_RE.sub(" ", text).strip()


def fmt_when(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return iso


def sender_name(msg: dict) -> str:
    frm = msg.get("from") or {}
    user = frm.get("user") or {}
    return user.get("displayName") or "?"


def fetch_messages(token: str, chat_id: str, top: int) -> list[dict]:
    resp = requests.get(
        f"{GRAPH}/me/chats/{chat_id}/messages?$top={top}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    if resp.status_code != 200:
        print(f"Graph HTTP {resp.status_code}: {resp.text}")
        sys.exit(1)
    return resp.json().get("value", [])


def build_transcript(msgs: list[dict]) -> str:
    """Plain-text transcript, oldest first, suitable for the LLM."""
    lines = []
    for msg in reversed(msgs):  # oldest first reads better for LLM
        text = strip_html((msg.get("body") or {}).get("content"))
        if not text:
            continue  # skip attachment-only / system events
        when = fmt_when(msg.get("createdDateTime"))
        who = sender_name(msg)
        lines.append(f"[{when}] {who}: {text}")
    return "\n".join(lines)


def summarize(transcript: str) -> str:
    if not transcript.strip():
        return "(в чате нет текстовых сообщений за этот период)"
    resp = requests.post(
        f"{LLM_ENDPOINT}/chat/completions",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Сообщения чата (oldest first):\n\n{transcript}"},
            ],
            "temperature": 0.3,
        },
        timeout=60,
    )
    if resp.status_code != 200:
        print(f"LLM HTTP {resp.status_code}: {resp.text}")
        sys.exit(1)
    return resp.json()["choices"][0]["message"]["content"].strip()


def post_to_notification_chat(token: str, html_content: str) -> None:
    resp = requests.post(
        f"{GRAPH}/me/chats/{NOTIFICATION_CHAT_ID}/messages",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "body": {
                "contentType": "html",
                "content": html_content,
            }
        },
        timeout=20,
    )
    if resp.status_code not in (200, 201):
        print(f"Graph POST HTTP {resp.status_code}: {resp.text}")
        sys.exit(1)


def markdown_to_teams_html(md: str, source_chat_id: str, count: int) -> str:
    """Very small markdown → Teams HTML conversion (bullets + line breaks)."""
    lines = []
    lines.append(f"<b>AI summary</b> ({count} messages from <code>{source_chat_id}</code>)<br><br>")
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            lines.append("<br>")
        elif line.startswith(("- ", "* ", "• ")):
            lines.append(f"• {line[2:]}<br>")
        elif re.match(r"^\d+\.\s", line):
            lines.append(f"{line}<br>")
        else:
            lines.append(f"{line}<br>")
    return "".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a Teams chat and post the summary to the notification chat.")
    parser.add_argument("source_chat_id", help="Graph chat id to read from")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP, help=f"Number of messages (default {DEFAULT_TOP})")
    args = parser.parse_args()

    token = get_access_token()
    print(f"Fetching {args.top} messages from {args.source_chat_id} ...", flush=True)
    msgs = fetch_messages(token, args.source_chat_id, args.top)
    transcript = build_transcript(msgs)
    print(f"Got {len(msgs)} messages, {len(transcript)} chars of text. Summarizing via {LLM_MODEL} ...", flush=True)

    summary = summarize(transcript)
    print("\n--- Summary ---\n")
    print(summary)
    print("\n--- Posting to notification chat ---\n")

    html = markdown_to_teams_html(summary, args.source_chat_id, len(msgs))
    post_to_notification_chat(token, html)
    print("Done. Check your 'AI Teams Summaries' chat in Teams.")


if __name__ == "__main__":
    main()
