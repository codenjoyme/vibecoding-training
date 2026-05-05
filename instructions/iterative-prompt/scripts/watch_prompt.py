"""Resilient main.prompt.md watcher.

Wakes only when the file changes AND the last unprocessed ## UPD block ends
with a 'go' marker.  Survives transient errors (file lock by editor, encoding
hiccups, etc.) by catching every exception inside the loop and continuing.

Usage:
    python .github/dark-factory/scripts/watch_prompt.py [path-to-main.prompt.md]

Exits 0 with `NEW UPD ready` on stdout when the trigger fires.
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from pathlib import Path

DEFAULT_PATH = Path('.github/work/main.prompt.md')
SLEEP_IDLE = 4       # seconds between polls when nothing changed
SLEEP_BUSY = 1       # faster polling when file changed but no `go` yet

# Regex: split on ## UPD headers (keep the header in the block)
_UPD_RE = re.compile(r'^(?=## UPD)', re.MULTILINE)


def read_file(p: Path) -> str:
    """Read the full file with retries to dodge editor save locks on Windows."""
    for attempt in range(5):
        try:
            return p.read_text(encoding='utf-8', errors='replace')
        except (PermissionError, OSError) as exc:
            if attempt == 4:
                raise
            time.sleep(0.2)
    raise RuntimeError('unreachable')


def file_hash(p: Path) -> str:
    for attempt in range(5):
        try:
            data = p.read_bytes()
            return hashlib.sha256(data).hexdigest()
        except (PermissionError, OSError) as exc:
            if attempt == 4:
                raise
            time.sleep(0.2)
    raise RuntimeError('unreachable')


def has_ready_upd(content: str) -> bool:
    """Return True if the last ## UPD block without ### RESULT ends with 'go'.

    Logic:
    1. Split the file into ## UPD blocks.
    2. Walk backwards to find the last block that has NO '### RESULT'.
    3. Check if that block's text (stripped) ends with 'go'.
    """
    blocks = _UPD_RE.split(content)
    # blocks[0] is everything before the first ## UPD (preamble) — skip it.
    upd_blocks = [b for b in blocks[1:] if b.startswith('## UPD') or b.startswith('UPD')]

    if not upd_blocks:
        return False

    # Walk from the end — find the last block without ### RESULT
    for block in reversed(upd_blocks):
        if '### RESULT' in block:
            # This UPD already processed — skip and stop searching.
            # All earlier UPDs are also done (they're in order).
            return False
        # Found an unprocessed UPD block — check for 'go'
        stripped = block.rstrip()
        # 'go' must be the very last word on the last line of the block
        if stripped.endswith('\ngo') or stripped.endswith(' go') or stripped == 'go':
            return True
        # Still being written (no 'go' yet)
        return False

    return False


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    if not path.exists():
        print(f'[watcher] file not found: {path}', flush=True)
        return 2

    try:
        baseline = file_hash(path)
    except Exception as exc:
        print(f'[watcher] initial hash error: {exc!r}; starting with empty baseline', flush=True)
        baseline = ''
    print(f'[watcher] watching {path} baseline={baseline[:12]}', flush=True)

    pending_change = False
    while True:
        try:
            time.sleep(SLEEP_BUSY if pending_change else SLEEP_IDLE)
            current = file_hash(path)
            if current != baseline:
                content = read_file(path)
                if has_ready_upd(content):
                    print(f'[watcher] NEW UPD ready: hash={current[:12]}', flush=True)
                    print('[watcher] >>> AGENT ACTION REQUIRED: read the prompt file NOW,', flush=True)
                    print('[watcher] >>> implement the new ## UPD block, write ### RESULT,', flush=True)
                    print('[watcher] >>> commit, then RESTART this watcher. Do NOT stop.', flush=True)
                    return 0
                if not pending_change:
                    print('[watcher] file changed but no `go` yet — polling faster', flush=True)
                else:
                    print('[watcher] still no `go`; waiting...', flush=True)
                pending_change = True
                baseline = current
            # else: no change, keep waiting
        except KeyboardInterrupt:
            print('[watcher] interrupted by user — exiting cleanly', flush=True)
            return 130
        except Exception as exc:
            # Never die on transient errors — log and keep looping.
            print(f'[watcher] caught {type(exc).__name__}: {exc} — continuing', flush=True)
            time.sleep(SLEEP_IDLE)


if __name__ == '__main__':
    sys.exit(main())
