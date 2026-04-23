"""
Download a Microsoft Teams meeting transcript via Microsoft Graph.

Yes — Graph exposes /me/onlineMeetings/{id}/transcripts/{tid}/content with
$format=text/vtt or $format=application/msword (docx). This script wraps it.

Usage (inside the container):
    docker compose run --rm app python download_transcript.py \
        --join-url "https://teams.microsoft.com/l/meetup-join/..." \
        --format docx \
        --out /data/transcript.docx

If --join-url is omitted the script lists your recent meetings with transcripts
and prints their IDs so you can re-run with --meeting-id.

Required Graph permissions (delegated, must be added to the app registration
AND consented on first run):
  - OnlineMeetings.Read
  - OnlineMeetingTranscript.Read.All

This script reuses the on-disk token cache from graph_auth.py but requests its
own scopes. The first run with these new scopes will trigger device-code flow
again to grant consent.
"""

import argparse
import json
import os
import sys
import urllib.parse

import requests
from dotenv import load_dotenv
from msal import PublicClientApplication, SerializableTokenCache

load_dotenv()

TENANT_ID = os.environ["AZURE_TENANT_ID"]
CLIENT_ID = os.environ["AZURE_CLIENT_ID"]
SCOPES = ["OnlineMeetings.Read", "OnlineMeetingTranscript.Read.All"]
CACHE_PATH = "/data/token_cache.bin"
GRAPH = "https://graph.microsoft.com/v1.0"


def get_token() -> str:
    cache = SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            cache.deserialize(f.read())
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
    if cache.has_state_changed:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            f.write(cache.serialize())
    if "access_token" not in result:
        print("Auth failed:", json.dumps(result, indent=2))
        sys.exit(1)
    return result["access_token"]


def find_meeting_id(token: str, join_url: str) -> str:
    # Graph requires the join URL exactly as Teams produced it.
    q = urllib.parse.quote(f"JoinWebUrl eq '{join_url}'", safe="")
    r = requests.get(
        f"{GRAPH}/me/onlineMeetings?$filter={q}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    r.raise_for_status()
    items = r.json().get("value", [])
    if not items:
        sys.exit(f"No online meeting matched join URL {join_url}")
    return items[0]["id"]


def list_transcripts(token: str, meeting_id: str) -> list:
    r = requests.get(
        f"{GRAPH}/me/onlineMeetings/{meeting_id}/transcripts",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("value", [])


def download(token: str, meeting_id: str, transcript_id: str, fmt: str, out_path: str) -> None:
    accept = {
        "vtt": "text/vtt",
        "docx": "application/msword",
    }[fmt]
    r = requests.get(
        f"{GRAPH}/me/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/content",
        headers={"Authorization": f"Bearer {token}", "Accept": accept},
        params={"$format": accept},
        timeout=120,
    )
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"Wrote {out_path} ({len(r.content)} bytes)")


def main() -> None:
    p = argparse.ArgumentParser(description="Download a Teams meeting transcript via Graph.")
    p.add_argument("--join-url", help="Teams meeting join URL (used to look up the meeting id)")
    p.add_argument("--meeting-id", help="Online meeting id (skip --join-url)")
    p.add_argument("--transcript-id", help="Specific transcript id (default: latest)")
    p.add_argument("--format", choices=["vtt", "docx"], default="docx")
    p.add_argument("--out", default="/data/transcript.docx")
    p.add_argument("--list", action="store_true", help="List transcripts for the meeting and exit")
    args = p.parse_args()

    token = get_token()

    meeting_id = args.meeting_id
    if not meeting_id:
        if not args.join_url:
            sys.exit("Provide --meeting-id or --join-url.")
        meeting_id = find_meeting_id(token, args.join_url)

    transcripts = list_transcripts(token, meeting_id)
    if not transcripts:
        sys.exit(f"No transcripts found for meeting {meeting_id}.")

    if args.list:
        for t in transcripts:
            print(f"{t['id']}\t{t.get('createdDateTime', '?')}")
        return

    transcript_id = args.transcript_id or transcripts[-1]["id"]
    download(token, meeting_id, transcript_id, args.format, args.out)


if __name__ == "__main__":
    main()
