#!/usr/bin/env python3
"""Jira CLI — query Jira issues, fetch details, download attachments."""

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


def validate_config():
    if not JIRA_URL.startswith("https://"):
        sys.exit("ERROR: JIRA_URL must start with https://")
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        sys.exit("ERROR: JIRA_EMAIL and JIRA_API_TOKEN must be set in .env")


def auth():
    return (JIRA_EMAIL, JIRA_API_TOKEN)


def api_get(path, params=None):
    url = f"{JIRA_URL}/rest/api/3{path}"
    resp = requests.get(url, auth=auth(), params=params, timeout=15)
    if resp.status_code == 401:
        sys.exit("ERROR: 401 Unauthorized — check JIRA_EMAIL and JIRA_API_TOKEN")
    if resp.status_code == 403:
        sys.exit("ERROR: 403 Forbidden — token lacks permission for this operation")
    resp.raise_for_status()
    return resp.json()


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
        fields = [
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
        for label, value in fields:
            print(f"{label:<12}: {value}")
        desc = f.get("description")
        if desc and isinstance(desc, dict):
            # Atlassian Document Format — extract plain text
            content = desc.get("content", [])
            texts = []
            for block in content:
                for node in block.get("content", []):
                    if node.get("type") == "text":
                        texts.append(node.get("text", ""))
            if texts:
                print(f"\nDescription:\n{''.join(texts)}")


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
    resp = requests.get(target["content"], auth=auth(), stream=True, timeout=30)
    resp.raise_for_status()
    with open(dest, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    print(f"Downloaded: {dest} ({dest.stat().st_size:,} bytes)")


def main():
    validate_config()
    parser = argparse.ArgumentParser(description="Jira CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", help="Search issues with JQL")
    p_search.add_argument("--jql", required=True)
    p_search.add_argument("--format", choices=["table", "json", "plain"], default="table")
    p_search.add_argument("--max", type=int, default=20)

    p_get = sub.add_parser("get", help="Get issue details")
    p_get.add_argument("--key", required=True)
    p_get.add_argument("--format", choices=["table", "json", "plain"], default="table")

    p_att = sub.add_parser("attachments", help="List attachments on an issue")
    p_att.add_argument("--key", required=True)

    p_dl = sub.add_parser("download", help="Download an attachment")
    p_dl.add_argument("--key", required=True)
    p_dl.add_argument("--filename", required=True)
    p_dl.add_argument("--output", default="./downloads")

    args = parser.parse_args()
    dispatch = {"search": cmd_search, "get": cmd_get, "attachments": cmd_attachments, "download": cmd_download}
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
