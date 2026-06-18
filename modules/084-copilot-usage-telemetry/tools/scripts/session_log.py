#!/usr/bin/env python3
"""Session-log explorer — fast, context-free queries over a Copilot Chat
`main.jsonl` debug log.

These logs can be several megabytes. Loading one into an AI context window is
wasteful, so this tool gives you cheap "select views": locate the current log,
list event types, pull out every user request, grep raw lines, filter by tool,
or run a tiny JSONPath-ish expression — all returning LINE NUMBERS (coordinates)
so you can jump straight to the block you need.

This script deliberately knows NOTHING about UPD blocks or the iterative-prompt
pattern. It only provides generic primitives; higher-level logic is layered on
top later.

Log location (written by the Copilot Chat extension, one folder per session):
    <userdata>/User/workspaceStorage/<wsId>/GitHub.copilot-chat/debug-logs/<sid>/main.jsonl

Each line is one JSON event. Common fields: ts, dur, sid, type, name, spanId,
parentSpanId, status, attrs. See the `troubleshoot` skill for the full schema.
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows so Cyrillic / emoji in logs don't crash.
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ── Locating logs ────────────────────────────────────────────────────────────

def _userdata_roots():
    """Return candidate VS Code user-data roots across OSes and variants."""
    roots = []
    home = Path.home()
    variants = ["Code", "Code - Insiders"]
    if sys.platform == "win32":
        appdata = os.getenv("APPDATA", str(home / "AppData" / "Roaming"))
        for v in variants:
            roots.append(Path(appdata) / v)
    elif sys.platform == "darwin":
        for v in variants:
            roots.append(home / "Library" / "Application Support" / v)
    else:
        for v in variants:
            roots.append(home / ".config" / v)
    return roots


def find_logs():
    """Return all `main.jsonl` debug logs, newest first (by mtime)."""
    logs = []
    for root in _userdata_roots():
        pattern = str(root / "User" / "workspaceStorage" / "*" /
                      "GitHub.copilot-chat" / "debug-logs" / "*" / "main.jsonl")
        logs.extend(glob.glob(pattern))
    logs = [p for p in logs if os.path.isfile(p)]
    logs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return logs


def resolve_log(arg_file):
    """Resolve the target log: explicit path, or the most-recent one."""
    if arg_file:
        if not os.path.isfile(arg_file):
            sys.exit(f"ERROR: file not found: {arg_file}")
        return arg_file
    logs = find_logs()
    if not logs:
        sys.exit("ERROR: no main.jsonl debug logs found. Is Copilot Chat logging enabled?")
    return logs[0]


# ── Reading ──────────────────────────────────────────────────────────────────

def iter_events(path):
    """Yield (line_number, raw_text, parsed_or_None) for each line (1-based)."""
    with open(path, "r", encoding="utf-8") as f:
        for i, raw in enumerate(f, start=1):
            raw = raw.rstrip("\n")
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                obj = None
            yield i, raw, obj


def _preview(text, width=140):
    text = " ".join(str(text).split())
    return text if len(text) <= width else text[: width - 1] + "…"


# ── Tiny JSONPath-ish resolver ───────────────────────────────────────────────

def get_path(obj, path):
    """Resolve a minimal dotted path with [index] and '*' wildcard.

    Supports: 'attrs.model', 'attrs.inputTokens', 'foo[0].bar', 'items.*.id'.
    Returns a list of matched values (empty if nothing matched).
    """
    tokens = []
    for part in path.split("."):
        while "[" in part:
            key, _, rest = part.partition("[")
            if key:
                tokens.append(key)
            idx, _, part = rest.partition("]")
            tokens.append(int(idx) if idx.lstrip("-").isdigit() else idx)
        if part:
            tokens.append(part)

    current = [obj]
    for tok in tokens:
        nxt = []
        for cur in current:
            if tok == "*":
                if isinstance(cur, dict):
                    nxt.extend(cur.values())
                elif isinstance(cur, list):
                    nxt.extend(cur)
            elif isinstance(tok, int):
                if isinstance(cur, list) and -len(cur) <= tok < len(cur):
                    nxt.append(cur[tok])
            else:
                if isinstance(cur, dict) and tok in cur:
                    nxt.append(cur[tok])
        current = nxt
        if not current:
            return []
    return current


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_locate(args):
    logs = find_logs()
    if not logs:
        sys.exit("No main.jsonl debug logs found.")
    if args.all:
        for p in logs:
            size_kb = os.path.getsize(p) / 1024
            mtime = __import__("datetime").datetime.fromtimestamp(os.path.getmtime(p))
            print(f"{mtime:%Y-%m-%d %H:%M}  {size_kb:8.0f} KB  {p}")
    else:
        print(logs[0])


def cmd_types(args):
    path = resolve_log(args.file)
    counts = {}
    for _, _, obj in iter_events(path):
        t = (obj or {}).get("type", "<unparsed>") if obj is not None else "<unparsed>"
        counts[t] = counts.get(t, 0) + 1
    if args.json:
        print(json.dumps({"file": path, "counts": counts}, indent=2, ensure_ascii=False))
        return
    print(f"# {path}")
    for t, n in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
        print(f"  {n:6}  {t}")


def cmd_requests(args):
    """All user requests, with line numbers (coordinates)."""
    path = resolve_log(args.file)
    rows = []
    for ln, _, obj in iter_events(path):
        if not obj:
            continue
        t = obj.get("type")
        text = None
        if t == "user_message":
            text = (obj.get("attrs") or {}).get("content")
        elif t == "llm_request":
            text = (obj.get("attrs") or {}).get("userRequest")
        if text:
            rows.append({"line": ln, "type": t, "text": text})
    if args.json:
        print(json.dumps({"file": path, "requests": rows}, indent=2, ensure_ascii=False))
        return
    print(f"# {path}")
    for r in rows:
        print(f"  L{r['line']:<6} [{r['type']}] {_preview(r['text'])}")


def cmd_grep(args):
    """Every line whose raw text contains <text> (case-insensitive)."""
    path = resolve_log(args.file)
    needle = args.text.lower()
    rows = []
    for ln, raw, obj in iter_events(path):
        if needle in raw.lower():
            rows.append({"line": ln, "type": (obj or {}).get("type"), "text": raw})
    if args.json:
        print(json.dumps({"file": path, "needle": args.text, "matches": rows},
                         indent=2, ensure_ascii=False))
        return
    print(f"# {path}  ({len(rows)} match(es) for '{args.text}')")
    for r in rows:
        print(f"  L{r['line']:<6} [{r['type']}] {_preview(r['text'])}")


def cmd_tool(args):
    """Every tool_call event for a given tool name, with line numbers."""
    path = resolve_log(args.file)
    rows = []
    for ln, _, obj in iter_events(path):
        if not obj or obj.get("type") != "tool_call":
            continue
        if obj.get("name") == args.name or args.name.lower() in str(obj.get("name", "")).lower():
            attrs = obj.get("attrs") or {}
            rows.append({
                "line": ln,
                "name": obj.get("name"),
                "status": obj.get("status"),
                "dur": obj.get("dur"),
                "args": attrs.get("args"),
            })
    if args.json:
        print(json.dumps({"file": path, "tool": args.name, "calls": rows},
                         indent=2, ensure_ascii=False))
        return
    print(f"# {path}  ({len(rows)} call(s) of '{args.name}')")
    for r in rows:
        print(f"  L{r['line']:<6} {r['status']:5} {str(r['dur']):>7}ms  {_preview(r['args'], 100)}")


def cmd_jsonpath(args):
    """Run a tiny JSONPath-ish expression against each event; report matches."""
    path = resolve_log(args.file)
    rows = []
    for ln, _, obj in iter_events(path):
        if not obj:
            continue
        values = get_path(obj, args.expr)
        for v in values:
            rows.append({"line": ln, "value": v})
    if args.json:
        print(json.dumps({"file": path, "expr": args.expr, "matches": rows},
                         indent=2, ensure_ascii=False))
        return
    print(f"# {path}  ({len(rows)} match(es) for '{args.expr}')")
    for r in rows:
        print(f"  L{r['line']:<6} {_preview(json.dumps(r['value'], ensure_ascii=False))}")


def cmd_view(args):
    """Pretty-print a single event by line number, with optional context."""
    path = resolve_log(args.file)
    lo = max(1, args.line - args.context)
    hi = args.line + args.context
    for ln, raw, obj in iter_events(path):
        if ln < lo or ln > hi:
            continue
        marker = ">>" if ln == args.line else "  "
        if ln == args.line and obj is not None:
            print(f"{marker} L{ln}:")
            print(json.dumps(obj, indent=2, ensure_ascii=False))
        else:
            print(f"{marker} L{ln}: {_preview(raw)}")


# ── CLI ──────────────────────────────────────────────────────────────────────

def _add_common(p, with_file=True):
    if with_file:
        p.add_argument("file", nargs="?", default=None,
                       help="path to main.jsonl (default: most recent log)")
    p.add_argument("--json", action="store_true", help="output structured JSON")


def main():
    parser = argparse.ArgumentParser(
        description="Fast, context-free select views over a Copilot Chat main.jsonl log."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("locate", help="print the current (most recent) log path")
    p.add_argument("--all", action="store_true", help="list all logs newest-first")

    p = sub.add_parser("types", help="count events by type")
    _add_common(p)

    p = sub.add_parser("requests", help="list all user requests with line numbers")
    _add_common(p)

    p = sub.add_parser("grep", help="lines whose raw text contains TEXT")
    p.add_argument("text", help="substring to search for (case-insensitive)")
    _add_common(p)

    p = sub.add_parser("tool", help="tool_call events for tool NAME")
    p.add_argument("name", help="tool name (exact or substring)")
    _add_common(p)

    p = sub.add_parser("jsonpath", help="tiny JSONPath-ish query, e.g. attrs.model")
    p.add_argument("expr", help="dotted path with [idx] and * wildcard")
    _add_common(p)

    p = sub.add_parser("view", help="pretty-print one event by line number")
    p.add_argument("line", type=int, help="line number to show")
    p.add_argument("--context", type=int, default=0, help="N lines of context around it")
    _add_common(p)

    args = parser.parse_args()
    handlers = {
        "locate": cmd_locate,
        "types": cmd_types,
        "requests": cmd_requests,
        "grep": cmd_grep,
        "tool": cmd_tool,
        "jsonpath": cmd_jsonpath,
        "view": cmd_view,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
