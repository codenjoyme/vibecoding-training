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


def list_recent_transcripts(token: str, days: int) -> list:
    """List ALL of the user's transcripts created in the last N days, newest first.

    Uses /me/onlineMeetings/getAllTranscripts which requires a $filter on
    meetingOrganizerUserId or meetingStartDateTime. We use the latter.
    """
    from datetime import datetime, timedelta, timezone

    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    flt = urllib.parse.quote(f"meetingStartDateTime ge {since}", safe="")
    url = f"{GRAPH}/me/onlineMeetings/getAllTranscripts?$filter={flt}"
    items: list = []
    while url:
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
        r.raise_for_status()
        body = r.json()
        items.extend(body.get("value", []))
        url = body.get("@odata.nextLink")
    items.sort(key=lambda t: t.get("createdDateTime", ""), reverse=True)
    return items


def get_meeting(token: str, meeting_id: str) -> dict:
    r = requests.get(
        f"{GRAPH}/me/onlineMeetings/{meeting_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def participant_names(meeting: dict) -> list:
    """Best-effort participant display names from an onlineMeeting payload."""
    p = meeting.get("participants", {})
    names = []
    org = p.get("organizer", {})
    if org:
        ident = (org.get("upn") or
                 (org.get("identity", {}).get("user") or {}).get("displayName"))
        if ident:
            names.append(f"organizer={ident}")
    for a in p.get("attendees", []) or []:
        ident = (a.get("upn") or
                 (a.get("identity", {}).get("user") or {}).get("displayName"))
        if ident:
            names.append(ident)
    return names


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
    p.add_argument("--list-recent", action="store_true",
                   help="List recent transcripts across ALL meetings (newest first) and exit")
    p.add_argument("--latest", action="store_true",
                   help="Auto-pick the most recent transcript across all meetings in the last --days window")
    p.add_argument("--days", type=int, default=14,
                   help="Window in days for --list-recent / --latest (default: 14)")
    args = p.parse_args()

    token = get_token()

    if args.list_recent or (args.latest and not (args.meeting_id or args.join_url)):
        recent = list_recent_transcripts(token, args.days)
        if not recent:
            sys.exit(f"No transcripts in the last {args.days} day(s).")
        if args.list_recent and not args.latest:
            for t in recent:
                mid = t.get("meetingId", "?")
                created = t.get("createdDateTime", "?")
                tid = t.get("id", "?")
                # Best-effort: enrich with subject + participants.
                try:
                    m = get_meeting(token, mid)
                    subj = m.get("subject", "(no subject)")
                    parts = ", ".join(participant_names(m)) or "(no participants)"
                except Exception as e:
                    subj = f"(meeting fetch failed: {e})"
                    parts = "?"
                print(f"{created}  meeting={mid}")
                print(f"  subject:      {subj}")
                print(f"  participants: {parts}")
                print(f"  transcript:   {tid}")
                print()
            return
        # --latest path: pick top
        latest = recent[0]
        meeting_id = latest["meetingId"]
        transcript_id = latest["id"]
        print(f"Latest transcript: meeting={meeting_id}  transcript={transcript_id}  created={latest.get('createdDateTime')}")
        try:
            m = get_meeting(token, meeting_id)
            print(f"  subject:      {m.get('subject', '(no subject)')}")
            print(f"  participants: {', '.join(participant_names(m)) or '(no participants)'}")
        except Exception as e:
            print(f"  (could not fetch meeting metadata: {e})")
        download(token, meeting_id, transcript_id, args.format, args.out)
        return

    meeting_id = args.meeting_id
    if not meeting_id:
        if not args.join_url:
            sys.exit("Provide --meeting-id, --join-url, --list-recent, or --latest.")
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
