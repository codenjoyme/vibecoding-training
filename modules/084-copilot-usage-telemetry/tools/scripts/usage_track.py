#!/usr/bin/env python3
"""Usage tracker — persist one row of telemetry per iterative-prompt UPD run.

This is the orchestrator that ties the other two scripts together so the AI
agent itself never has to parse a multi-megabyte log or talk to GitHub:

    copilot_stats.py  -> live AI-credit / quota numbers   (premium_interactions)
    session_log.py    -> token counts & metadata from the per-session main.jsonl

`usage_track.py` calls BOTH on the agent's behalf and writes the result into a
SQLite database under ~/.copilot-telemetry/telemetry.db. One row = one UPD run.

Two-phase workflow (driven by the iterative-prompt agent):

    # at the START of a UPD — prints a unique marker the agent echoes into chat
    python usage_track.py begin "UPD7"
        -> { "run_id": 12, "marker": "FG8FBJ7EV547HBJEH" }

    # at the END of the UPD, after RESULT is written and committed
    python usage_track.py end 12 --write-min 6 --read-min 20
        -> fills credits/tokens/model, resolves the log BY MARKER

The marker trick solves the "any keystroke in any chat updates mtime" problem
from UPD5: the agent prints the marker, the log that contains it is provably
THIS session's log — no guessing about which file is "most recent".

Stdlib only (sqlite3, json, …). The credit/token sub-scripts are imported
lazily and any failure degrades to NULL columns instead of crashing.
"""

import argparse
import json
import os
import random
import sqlite3
import string
import sys
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 stdout/stderr on Windows so Cyrillic / emoji don't crash printing.
# Use reconfigure (mutates the existing stream in place) rather than swapping in
# a new TextIOWrapper — a swapped-in wrapper would be orphaned and close the
# underlying buffer when the sibling scripts re-wrap stdout on import.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Make the sibling scripts importable as modules (they live next to this file).
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))


# ── Storage location ─────────────────────────────────────────────────────────

def _db_path():
    """Return the telemetry DB path (override with COPILOT_TELEMETRY_DIR)."""
    base = os.getenv("COPILOT_TELEMETRY_DIR")
    root = Path(base) if base else (Path.home() / ".copilot-telemetry")
    root.mkdir(parents=True, exist_ok=True)
    return root / "telemetry.db"


# Columns map 1:1 onto the original UPD1 tracking table. Anything the logs
# cannot supply (human prompt-writing / reading minutes) is nullable and filled
# from the agent's --write-min / --read-min flags.
_SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    status          TEXT,           -- pending | done
    marker          TEXT,           -- random anchor printed into chat at begin
    label           TEXT,           -- e.g. "UPD7"
    workspace       TEXT,           -- repo / folder the run happened in
    date            TEXT,           -- YYYY-MM-DD
    started_at      TEXT,           -- ISO ts captured at begin
    ended_at        TEXT,           -- ISO ts captured at end
    write_minutes   INTEGER,        -- human: minutes spent writing the prompt
    read_minutes    INTEGER,        -- human: minutes spent reading the result
    credits_start   REAL,           -- premium_interactions.remaining at begin
    credits_end     REAL,           -- premium_interactions.remaining at end
    credits_spent   REAL,           -- start - end
    context_start   INTEGER,        -- first llm_request inputTokens in range
    context_finish  INTEGER,        -- last llm_request inputTokens in range
    context_max     INTEGER,        -- max maxTokens seen (response budget)
    compact         TEXT,           -- yes | no  (heuristic)
    input_tokens    INTEGER,        -- sum inputTokens over the run
    output_tokens   INTEGER,        -- sum outputTokens over the run
    log_file        TEXT,           -- resolved main.jsonl
    model           TEXT,
    thinking_effort TEXT,
    vendor          TEXT,
    request_text    TEXT,
    response_text   TEXT
);
"""


def _connect():
    conn = sqlite3.connect(str(_db_path()))
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    return conn


# ── Helpers that delegate to the sibling scripts ─────────────────────────────

def _now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def fetch_credits_remaining():
    """Return premium_interactions.remaining via copilot_stats, or None.

    Any failure (no token, network, missing deps) degrades to None so begin/end
    never crash on the credit side.
    """
    try:
        import copilot_stats as cs
    except Exception:
        return None
    try:
        cs._require_token()
        data = cs.api_get("/copilot_internal/user")
    except SystemExit:
        return None
    except Exception:
        return None
    snap = (data.get("quota_snapshots") or {}).get("premium_interactions") or {}
    val = snap.get("remaining")
    if val is None:
        val = snap.get("quota_remaining")
    return val


def _resolve_log_by_marker(marker, explicit=None, scan_limit=25):
    """Pick the main.jsonl for THIS run.

    Priority: explicit path > the most-recent log that CONTAINS the marker >
    the most-recent log overall. Returns a path string or None.
    """
    if explicit:
        return explicit if os.path.isfile(explicit) else None
    try:
        import session_log as sl
    except Exception:
        return None
    logs = sl.find_logs()[:scan_limit]
    if marker:
        for info in logs:
            try:
                with open(info["path"], "r", encoding="utf-8", errors="replace") as f:
                    if marker in f.read():
                        return info["path"]
            except OSError:
                continue
    return logs[0]["path"] if logs else None


def _detect_compact(series):
    """Heuristic: a sharp drop in inputTokens mid-run == a compaction happened."""
    peak = 0
    for v in series:
        if peak > 0 and v < peak * 0.6:
            return "yes"
        peak = max(peak, v)
    return "no"


def _vendor_for(model):
    if not model:
        return "GHCP"
    m = model.lower()
    if "claude" in m:
        return "Anthropic/GHCP"
    if "gpt" in m or "o1" in m or "o3" in m:
        return "OpenAI/GHCP"
    if "gemini" in m:
        return "Google/GHCP"
    return "GHCP"


def extract_from_log(path, marker=None):
    """Pull token/model metadata from the log, scanning from the marker line
    (the start of this UPD run) to EOF. Everything is best-effort."""
    try:
        import session_log as sl
    except Exception:
        return {}

    start_line = 1
    if marker:
        for ln, raw, _ in sl.iter_events(path):
            if marker in raw:
                start_line = ln
                break

    model = thinking = req_text = resp_text = None
    in_sum = out_sum = 0
    ctx_first = ctx_last = None
    ctx_max = 0
    input_series = []

    for ln, _, obj in sl.iter_events(path):
        if ln < start_line or not obj:
            continue
        t = obj.get("type")
        attrs = obj.get("attrs") or {}
        if t == "llm_request":
            model = attrs.get("model") or model
            it, ot, mx = attrs.get("inputTokens"), attrs.get("outputTokens"), attrs.get("maxTokens")
            if isinstance(it, (int, float)):
                in_sum += it
                if ctx_first is None:
                    ctx_first = it
                ctx_last = it
                input_series.append(it)
            if isinstance(ot, (int, float)):
                out_sum += ot
            if isinstance(mx, (int, float)):
                ctx_max = max(ctx_max, mx)
            if not req_text:
                req_text = attrs.get("userRequest")
            te = attrs.get("thinkingEffort") or attrs.get("thinking") or attrs.get("reasoningEffort")
            if te:
                thinking = te
        elif t == "user_message" and not req_text:
            req_text = attrs.get("content")
        elif t == "agent_response":
            resp_text = attrs.get("content") or resp_text

    return {
        "model": model,
        "input_tokens": in_sum or None,
        "output_tokens": out_sum or None,
        "context_start": ctx_first,
        "context_finish": ctx_last,
        "context_max": ctx_max or None,
        "compact": _detect_compact(input_series),
        "thinking_effort": thinking,
        "vendor": _vendor_for(model),
        "request_text": req_text,
        "response_text": resp_text,
    }


def _gen_marker(n=17):
    alphabet = string.ascii_uppercase + string.digits
    return "".join(random.choices(alphabet, k=n))


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_begin(args):
    """Open a pending run: capture start time + start credits, print a marker."""
    marker = args.marker or _gen_marker()
    workspace = args.workspace or os.getcwd()
    started = _now_iso()
    credits_start = fetch_credits_remaining()

    conn = _connect()
    cur = conn.execute(
        "INSERT INTO runs (status, marker, label, workspace, date, started_at, credits_start) "
        "VALUES ('pending', ?, ?, ?, ?, ?, ?)",
        (marker, args.label, workspace, started[:10], started, credits_start),
    )
    conn.commit()
    run_id = cur.lastrowid
    conn.close()

    out = {"run_id": run_id, "marker": marker, "started_at": started,
           "credits_start": credits_start, "label": args.label}
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    print(f"run_id: {run_id}")
    print(f"marker: {marker}")
    print(f"started_at: {started}")
    print(f"credits_start: {credits_start}")
    print("\n>>> Echo this marker into the chat so it lands in the session log:")
    print(f">>> {marker}")


def _load_run(conn, run_id):
    row = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
    if row is None:
        sys.exit(f"ERROR: run_id {run_id} not found.")
    return row


def cmd_end(args):
    """Close a run: capture end time + credits, resolve log by marker, extract."""
    conn = _connect()
    row = _load_run(conn, args.run_id)

    ended = _now_iso()
    credits_end = fetch_credits_remaining()
    credits_start = row["credits_start"]
    spent = None
    if isinstance(credits_start, (int, float)) and isinstance(credits_end, (int, float)):
        spent = round(credits_start - credits_end, 3)

    log_path = _resolve_log_by_marker(row["marker"], explicit=args.file)
    extracted = extract_from_log(log_path, marker=row["marker"]) if log_path else {}

    conn.execute(
        """UPDATE runs SET
            status='done', ended_at=?, write_minutes=?, read_minutes=?,
            credits_end=?, credits_spent=?, log_file=?,
            model=?, input_tokens=?, output_tokens=?,
            context_start=?, context_finish=?, context_max=?, compact=?,
            thinking_effort=?, vendor=?, request_text=?, response_text=?
           WHERE run_id=?""",
        (
            ended, args.write_min, args.read_min,
            credits_end, spent, log_path,
            extracted.get("model"), extracted.get("input_tokens"), extracted.get("output_tokens"),
            extracted.get("context_start"), extracted.get("context_finish"),
            extracted.get("context_max"), extracted.get("compact"),
            extracted.get("thinking_effort"), extracted.get("vendor"),
            extracted.get("request_text"), extracted.get("response_text"),
            args.run_id,
        ),
    )
    conn.commit()
    out = dict(_load_run(conn, args.run_id))
    conn.close()

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    print(f"run {args.run_id} closed ({out['label']})")
    print(f"  credits: {out['credits_start']} -> {out['credits_end']}  spent={out['credits_spent']}")
    print(f"  tokens:  in={out['input_tokens']} out={out['output_tokens']}")
    print(f"  context: {out['context_start']} -> {out['context_finish']} (max {out['context_max']}, compact={out['compact']})")
    print(f"  model:   {out['model']}  thinking={out['thinking_effort']}  vendor={out['vendor']}")
    print(f"  log:     {out['log_file']}")
    if not log_path:
        print("  NOTE: no log resolved — run `refresh` later once the session log has flushed.")


def cmd_refresh(args):
    """Re-extract log-derived fields for an existing run (post-flush top-up)."""
    conn = _connect()
    row = _load_run(conn, args.run_id)
    log_path = _resolve_log_by_marker(row["marker"], explicit=args.file)
    if not log_path:
        conn.close()
        sys.exit("ERROR: could not resolve a log (marker not found, pass --file).")
    extracted = extract_from_log(log_path, marker=row["marker"])
    conn.execute(
        """UPDATE runs SET log_file=?, model=?, input_tokens=?, output_tokens=?,
            context_start=?, context_finish=?, context_max=?, compact=?,
            thinking_effort=?, vendor=?, request_text=?, response_text=?
           WHERE run_id=?""",
        (
            log_path, extracted.get("model"), extracted.get("input_tokens"),
            extracted.get("output_tokens"), extracted.get("context_start"),
            extracted.get("context_finish"), extracted.get("context_max"),
            extracted.get("compact"), extracted.get("thinking_effort"),
            extracted.get("vendor"), extracted.get("request_text"),
            extracted.get("response_text"), args.run_id,
        ),
    )
    conn.commit()
    out = dict(_load_run(conn, args.run_id))
    conn.close()
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return
    print(f"run {args.run_id} refreshed from {log_path}")
    print(f"  tokens in={out['input_tokens']} out={out['output_tokens']}  model={out['model']}")


def cmd_list(args):
    """Show recent runs, newest first."""
    conn = _connect()
    where, params = "", []
    if args.workspace:
        where = "WHERE workspace = ?"
        params.append(args.workspace)
    rows = conn.execute(
        f"SELECT * FROM runs {where} ORDER BY run_id DESC LIMIT ?",
        (*params, args.limit),
    ).fetchall()
    conn.close()
    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False))
        return
    print(f"{'id':>4}  {'status':8} {'label':10} {'date':10}  {'spent':>7}  {'in':>8} {'out':>7}  model")
    for r in rows:
        print(f"{r['run_id']:>4}  {r['status']:8} {str(r['label'] or ''):10} "
              f"{str(r['date'] or ''):10}  {str(r['credits_spent'] or ''):>7}  "
              f"{str(r['input_tokens'] or ''):>8} {str(r['output_tokens'] or ''):>7}  "
              f"{r['model'] or ''}")


def cmd_show(args):
    """Dump one run as JSON (full record)."""
    conn = _connect()
    row = _load_run(conn, args.run_id)
    conn.close()
    print(json.dumps(dict(row), indent=2, ensure_ascii=False))


# Export column order mirrors the original UPD1 tracking table.
_EXPORT_COLUMNS = [
    ("date", "date"),
    ("started_at", "started_at"),
    ("ended_at", "ended_at"),
    ("write_minutes", "write_minutes"),
    ("read_minutes", "read_minutes"),
    ("credits_start", "credits_start"),
    ("credits_end", "credits_end"),
    ("credits_spent", "credits_spent"),
    ("context_start", "context_start"),
    ("compact", "compact"),
    ("context_finish", "context_finish"),
    ("chat_credits", "credits_spent"),
    ("log_file", "log_file"),
    ("label", "label"),
    ("request_text", "request_text"),
    ("response_text", "response_text"),
    ("model", "model"),
    ("context_max", "context_max"),
    ("thinking_effort", "thinking_effort"),
    ("vendor", "vendor"),
]


def cmd_export(args):
    """Emit the tracking table (csv or md) for pasting into a report."""
    conn = _connect()
    where, params = "", []
    if args.workspace:
        where = "WHERE workspace = ?"
        params.append(args.workspace)
    rows = conn.execute(
        f"SELECT * FROM runs {where} ORDER BY run_id ASC", params
    ).fetchall()
    conn.close()

    headers = [h for h, _ in _EXPORT_COLUMNS]

    def cell(r, field):
        v = r[field]
        return "" if v is None else str(v)

    if args.format == "md":
        print("| " + " | ".join(headers) + " |")
        print("|" + "|".join(["---"] * len(headers)) + "|")
        for r in rows:
            vals = [cell(r, f).replace("|", "\\|").replace("\n", " ") for _, f in _EXPORT_COLUMNS]
            print("| " + " | ".join(vals) + " |")
        return

    # csv
    import csv
    w = csv.writer(sys.stdout)
    w.writerow(headers)
    for r in rows:
        w.writerow([cell(r, f) for _, f in _EXPORT_COLUMNS])


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Persist one telemetry row per iterative-prompt UPD run "
                    "(orchestrates copilot_stats.py + session_log.py)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("begin", help="open a run; print a marker to echo into chat")
    p.add_argument("label", help="run label, e.g. UPD7")
    p.add_argument("--workspace", default=None, help="workspace/repo (default: cwd)")
    p.add_argument("--marker", default=None, help="explicit marker (default: random)")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("end", help="close a run; resolve log by marker, extract")
    p.add_argument("run_id", type=int)
    p.add_argument("--write-min", type=int, default=None, dest="write_min",
                   help="minutes spent writing the prompt (asked from the user)")
    p.add_argument("--read-min", type=int, default=None, dest="read_min",
                   help="minutes spent reading the result (asked from the user)")
    p.add_argument("--file", default=None, help="explicit main.jsonl (overrides marker)")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("refresh", help="re-extract log fields for a run (post-flush)")
    p.add_argument("run_id", type=int)
    p.add_argument("--file", default=None, help="explicit main.jsonl")
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("list", help="list recent runs")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--workspace", default=None)
    p.add_argument("--json", action="store_true")

    p = sub.add_parser("show", help="dump one run as JSON")
    p.add_argument("run_id", type=int)

    p = sub.add_parser("export", help="emit the tracking table (csv|md)")
    p.add_argument("--format", choices=["csv", "md"], default="csv")
    p.add_argument("--workspace", default=None)

    args = parser.parse_args()
    handlers = {
        "begin": cmd_begin, "end": cmd_end, "refresh": cmd_refresh,
        "list": cmd_list, "show": cmd_show, "export": cmd_export,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
