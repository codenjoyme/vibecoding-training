"""Quick client to test the WinAPI MCP server end-to-end via stdio.

Run with the venv python:
    .venv/Scripts/python.exe test_client.py
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYEXE = HERE / ".venv" / "Scripts" / "python.exe"
SERVER = HERE / "server.py"


def send(proc: subprocess.Popen, payload: dict) -> None:
    line = json.dumps(payload, ensure_ascii=False)
    proc.stdin.write(line + "\n")
    proc.stdin.flush()


def read_response(proc: subprocess.Popen) -> dict | None:
    line = proc.stdout.readline()
    if not line:
        return None
    return json.loads(line)


def main() -> int:
    proc = subprocess.Popen(
        [str(PYEXE), str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        bufsize=1,
    )
    try:
        send(proc, {
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test_client", "version": "0"},
            },
        })
        init = read_response(proc)
        print("[initialize] ->", json.dumps(init, indent=2)[:300], "...\n")

        send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})

        send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        listing = read_response(proc)
        names = [t["name"] for t in listing["result"]["tools"]]
        print(f"[tools/list] -> {len(names)} tools: {names}\n")

        # Try screenshot_area on a small region (top-left 200x200)
        send(proc, {
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {
                "name": "screenshot_area",
                "arguments": {"x1": 0, "y1": 0, "x2": 200, "y2": 200},
            },
        })
        sc = read_response(proc)
        result = sc.get("result", {})
        content = result.get("content", [])
        text_items = [c for c in content if c.get("type") == "text"]
        image_items = [c for c in content if c.get("type") == "image"]
        print(f"[screenshot_area] -> {len(text_items)} text item(s), {len(image_items)} image item(s)")
        if text_items:
            print(f"   caption: {text_items[0]['text'].splitlines()[0]}")
        if image_items:
            img = image_items[0]
            print(f"   image: mimeType={img.get('mimeType')} base64_len={len(img.get('data', ''))}")

        # list_processes (no filter)
        send(proc, {
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "list_processes", "arguments": {"filter": "python"}},
        })
        lp = read_response(proc)
        text = lp["result"]["content"][0]["text"]
        parsed = json.loads(text)
        print(f"\n[list_processes filter=python] -> {len(parsed)} matches")
        for p in parsed[:3]:
            print(f"   {p}")

        # clipboard_set + clipboard_get round-trip
        send(proc, {
            "jsonrpc": "2.0", "id": 5, "method": "tools/call",
            "params": {"name": "clipboard_set", "arguments": {"text": "winapi-mcp test"}},
        })
        _ = read_response(proc)
        send(proc, {
            "jsonrpc": "2.0", "id": 6, "method": "tools/call",
            "params": {"name": "clipboard_get", "arguments": {}},
        })
        cg = read_response(proc)
        cg_text = json.loads(cg["result"]["content"][0]["text"])
        print(f"\n[clipboard round-trip] -> {cg_text}")

        return 0
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
