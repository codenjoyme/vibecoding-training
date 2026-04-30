#!/usr/bin/env python3
"""Jira CLI — read and write Jira issues, comments, attachments."""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")
# JIRA_AUTH_TYPE: 'basic' (Atlassian Cloud) or 'bearer' (Jira Server/Data Center PAT)
JIRA_AUTH_TYPE = os.getenv("JIRA_AUTH_TYPE", "basic").lower()
# JIRA_API_VERSION: '2' (Jira Server/DC default) or '3' (Atlassian Cloud default)
JIRA_API_VERSION = os.getenv("JIRA_API_VERSION", "2" if JIRA_AUTH_TYPE == "bearer" else "3")


def validate_config():
    if not JIRA_URL.startswith("https://"):
        sys.exit("ERROR: JIRA_URL must start with https://")
    if not JIRA_API_TOKEN:
        sys.exit("ERROR: JIRA_API_TOKEN must be set in .env")
    if JIRA_AUTH_TYPE == "basic" and not JIRA_EMAIL:
        sys.exit("ERROR: JIRA_EMAIL must be set for basic auth mode")


def _headers(extra=None):
    h = {"Accept": "application/json"}
    if JIRA_AUTH_TYPE == "bearer":
        h["Authorization"] = f"Bearer {JIRA_API_TOKEN}"
    if extra:
        h.update(extra)
    return h


def _auth():
    if JIRA_AUTH_TYPE == "bearer":
        return None
    return (JIRA_EMAIL, JIRA_API_TOKEN)


def _handle_error(resp, context=""):
    if resp.status_code == 401:
        hint = "check JIRA_API_TOKEN" if JIRA_AUTH_TYPE == "bearer" else "check JIRA_EMAIL and JIRA_API_TOKEN"
        sys.exit(f"ERROR: 401 Unauthorized — {hint} (JIRA_AUTH_TYPE={JIRA_AUTH_TYPE})")
    if resp.status_code == 403:
        sys.exit(f"ERROR: 403 Forbidden — token lacks permission for this operation{' (' + context + ')' if context else ''}")
    if not resp.ok:
        try:
            detail = resp.json()
            msgs = detail.get("errorMessages", []) + list(detail.get("errors", {}).values())
            sys.exit(f"ERROR: {resp.status_code} — {'; '.join(msgs) if msgs else resp.text[:200]}")
        except Exception:
            sys.exit(f"ERROR: {resp.status_code} — {resp.text[:200]}")


def api_get(path, params=None):
    url = f"{JIRA_URL}/rest/api/{JIRA_API_VERSION}{path}"
    resp = requests.get(url, auth=_auth(), headers=_headers(), params=params, timeout=15)
    _handle_error(resp)
    return resp.json()


def api_post(path, body):
    url = f"{JIRA_URL}/rest/api/{JIRA_API_VERSION}{path}"
    resp = requests.post(url, auth=_auth(), headers=_headers({"Content-Type": "application/json"}),
                         data=json.dumps(body), timeout=15)
    _handle_error(resp, path)
    return resp.json() if resp.content else {}


def api_put(path, body):
    url = f"{JIRA_URL}/rest/api/{JIRA_API_VERSION}{path}"
    resp = requests.put(url, auth=_auth(), headers=_headers({"Content-Type": "application/json"}),
                        data=json.dumps(body), timeout=15)
    _handle_error(resp, path)
    return resp.json() if resp.content else {}


def format_table(rows, headers):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    fmt = "  ".join(f"{{:<{w}}}" for w in widths)
    print(fmt.format(*headers))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))


# ── READ commands ──────────────────────────────────────────────────────────────

def cmd_search(args):
    data = api_get("/search", params={
        "jql": args.jql,
        "maxResults": args.max,
        "fields": "summary,status,assignee,priority"
    })
    issues = data.get("issues", [])
    if not issues:
        print("No issues found.")
        return
    if args.format == "json":
        print(json.dumps(issues, indent=2))
    elif args.format == "plain":
        for i in issues:
            print(f"{i['key']}: {i['fields']['summary']}")
    else:
        rows = []
        for i in issues:
            f = i["fields"]
            rows.append([
                i["key"],
                f["summary"][:60],
                f.get("status", {}).get("name", "-"),
                (f.get("assignee") or {}).get("displayName", "Unassigned"),
            ])
        format_table(rows, ["KEY", "SUMMARY", "STATUS", "ASSIGNEE"])


def cmd_get(args):
    data = api_get(f"/issue/{args.key}")
    f = data["fields"]
    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        fields_out = [
            ("Key", data["key"]),
            ("Summary", f.get("summary", "-")),
            ("Status", f.get("status", {}).get("name", "-")),
            ("Assignee", (f.get("assignee") or {}).get("displayName", "Unassigned")),
            ("Reporter", (f.get("reporter") or {}).get("displayName", "-")),
            ("Priority", (f.get("priority") or {}).get("name", "-")),
            ("Created", f.get("created", "-")[:10]),
            ("Updated", f.get("updated", "-")[:10]),
            ("Labels", ", ".join(f.get("labels", [])) or "-"),
            ("Comments", str(f.get("comment", {}).get("total", 0))),
        ]
        for label, value in fields_out:
            print(f"{label:<12}: {value}")
        desc = f.get("description")
        if desc and isinstance(desc, dict):
            content = desc.get("content", [])
            texts = []
            for block in content:
                for node in block.get("content", []):
                    if node.get("type") == "text":
                        texts.append(node.get("text", ""))
            if texts:
                print(f"\nDescription:\n{''.join(texts)}")
        elif desc and isinstance(desc, str):
            print(f"\nDescription:\n{desc}")


def cmd_attachments(args):
    data = api_get(f"/issue/{args.key}", params={"fields": "attachment"})
    attachments = data["fields"].get("attachment", [])
    if not attachments:
        print("No attachments found.")
        return
    rows = [[a["filename"], a["mimeType"], f"{a['size']:,} bytes"] for a in attachments]
    format_table(rows, ["FILENAME", "TYPE", "SIZE"])


def cmd_download(args):
    data = api_get(f"/issue/{args.key}", params={"fields": "attachment"})
    attachments = data["fields"].get("attachment", [])
    target = next((a for a in attachments if a["filename"] == args.filename), None)
    if not target:
        sys.exit(f"ERROR: Attachment '{args.filename}' not found on {args.key}")
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / args.filename
    resp = requests.get(target["content"], auth=_auth(), headers=_headers(), stream=True, timeout=30)
    _handle_error(resp, "download")
    with open(dest, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    print(f"Downloaded: {dest} ({dest.stat().st_size:,} bytes)")


def cmd_comments(args):
    data = api_get(f"/issue/{args.key}/comment")
    comments = data.get("comments", [])
    if not comments:
        print("No comments.")
        return
    for c in comments:
        author = (c.get("author") or {}).get("displayName", "?")
        created = c.get("created", "")[:10]
        body = c.get("body", "")
        if isinstance(body, dict):
            # ADF format
            texts = []
            for block in body.get("content", []):
                for node in block.get("content", []):
                    if node.get("type") == "text":
                        texts.append(node.get("text", ""))
            body = "".join(texts)
        print(f"[{created}] {author}:")
        print(f"  {body[:300]}")
        print()


def cmd_transitions(args):
    data = api_get(f"/issue/{args.key}/transitions")
    rows = [[t["id"], t["name"]] for t in data.get("transitions", [])]
    if not rows:
        print("No transitions available.")
        return
    format_table(rows, ["ID", "NAME"])


# ── WRITE commands ─────────────────────────────────────────────────────────────

def cmd_create(args):
    body = {
        "fields": {
            "project": {"key": args.project},
            "issuetype": {"name": args.type},
            "summary": args.summary,
        }
    }
    if args.description:
        # Plain text description works for both API v2 and v3
        body["fields"]["description"] = args.description
    if args.priority:
        body["fields"]["priority"] = {"name": args.priority}
    if args.labels:
        body["fields"]["labels"] = [l.strip() for l in args.labels.split(",")]
    result = api_post("/issue", body)
    key = result.get("key", "?")
    print(f"Created: {key}")
    print(f"Link: {JIRA_URL}/browse/{key}")


def cmd_comment(args):
    body = {"body": args.text}
    result = api_post(f"/issue/{args.key}/comment", body)
    cid = result.get("id", "?")
    print(f"Comment added (id={cid}) to {args.key}")


def cmd_upload(args):
    filepath = Path(args.file)
    if not filepath.exists():
        sys.exit(f"ERROR: File not found: {filepath}")
    url = f"{JIRA_URL}/rest/api/{JIRA_API_VERSION}/issue/{args.key}/attachments"
    # Attachments use multipart/form-data and require X-Atlassian-Token header
    h = _headers({"X-Atlassian-Token": "no-check"})
    # Remove Content-Type so requests sets it with boundary
    h.pop("Content-Type", None)
    with open(filepath, "rb") as fh:
        resp = requests.post(url, auth=_auth(), headers=h,
                             files={"file": (filepath.name, fh, "application/octet-stream")},
                             timeout=60)
    _handle_error(resp, "upload")
    result = resp.json()
    if isinstance(result, list) and result:
        print(f"Uploaded: {result[0]['filename']} ({result[0]['size']:,} bytes) to {args.key}")
    else:
        print(f"Uploaded to {args.key}")


def cmd_transition(args):
    body = {"transition": {"id": args.id}}
    api_post(f"/issue/{args.key}/transitions", body)
    print(f"Transitioned {args.key} to transition id={args.id}")


def cmd_update(args):
    fields = {}
    if args.summary:
        fields["summary"] = args.summary
    if args.priority:
        fields["priority"] = {"name": args.priority}
    if args.labels:
        fields["labels"] = [l.strip() for l in args.labels.split(",")]
    if not fields:
        sys.exit("ERROR: provide at least one field to update (--summary, --priority, --labels)")
    url = f"{JIRA_URL}/rest/api/{JIRA_API_VERSION}/issue/{args.key}"
    resp = requests.put(url, auth=_auth(), headers=_headers({"Content-Type": "application/json"}),
                        data=json.dumps({"fields": fields}), timeout=15)
    _handle_error(resp, "update")
    print(f"Updated {args.key}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    validate_config()
    parser = argparse.ArgumentParser(
        description="Jira CLI — read and write issues, comments, attachments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
READ commands:
  search       Search issues with JQL
  get          Get full issue details
  attachments  List attachments on an issue
  download     Download an attachment to disk
  comments     List comments on an issue
  transitions  List available status transitions

WRITE commands (require write-scoped token):
  create       Create a new issue
  comment      Add a comment to an issue
  upload       Upload a file as an attachment
  transition   Move issue to a new status (use transitions to find IDs)
  update       Update summary, priority, or labels
"""
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # READ
    p = sub.add_parser("search", help="Search issues with JQL")
    p.add_argument("--jql", required=True)
    p.add_argument("--format", choices=["table", "json", "plain"], default="table")
    p.add_argument("--max", type=int, default=20)

    p = sub.add_parser("get", help="Get issue details")
    p.add_argument("--key", required=True)
    p.add_argument("--format", choices=["table", "json", "plain"], default="table")

    p = sub.add_parser("attachments", help="List attachments on an issue")
    p.add_argument("--key", required=True)

    p = sub.add_parser("download", help="Download an attachment")
    p.add_argument("--key", required=True)
    p.add_argument("--filename", required=True)
    p.add_argument("--output", default="./downloads")

    p = sub.add_parser("comments", help="List comments on an issue")
    p.add_argument("--key", required=True)

    p = sub.add_parser("transitions", help="List available status transitions")
    p.add_argument("--key", required=True)

    # WRITE
    p = sub.add_parser("create", help="Create a new issue")
    p.add_argument("--project", required=True, help="Project key (e.g. ABC)")
    p.add_argument("--summary", required=True)
    p.add_argument("--type", default="Task", help="Issue type (default: Task)")
    p.add_argument("--description", default="")
    p.add_argument("--priority", default="", help="e.g. Major, Minor, Critical")
    p.add_argument("--labels", default="", help="Comma-separated labels")

    p = sub.add_parser("comment", help="Add a comment to an issue")
    p.add_argument("--key", required=True)
    p.add_argument("--text", required=True)

    p = sub.add_parser("upload", help="Upload a file as attachment")
    p.add_argument("--key", required=True)
    p.add_argument("--file", required=True, help="Path to file to upload")

    p = sub.add_parser("transition", help="Move issue to a new status")
    p.add_argument("--key", required=True)
    p.add_argument("--id", required=True, help="Transition ID (use 'transitions' command to list)")

    p = sub.add_parser("update", help="Update issue fields")
    p.add_argument("--key", required=True)
    p.add_argument("--summary", default="")
    p.add_argument("--priority", default="")
    p.add_argument("--labels", default="", help="Comma-separated labels (replaces existing)")

    args = parser.parse_args()
    dispatch = {
        "search": cmd_search, "get": cmd_get, "attachments": cmd_attachments,
        "download": cmd_download, "comments": cmd_comments, "transitions": cmd_transitions,
        "create": cmd_create, "comment": cmd_comment, "upload": cmd_upload,
        "transition": cmd_transition, "update": cmd_update,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
