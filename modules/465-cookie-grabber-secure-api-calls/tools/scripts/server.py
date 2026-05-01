#!/usr/bin/env python3
"""
Cookie Grabber Server
─────────────────────
Combined HTTP + WebSocket server. Run inside Docker (single port: 8080).

Endpoints:
  GET  /               HTML status page + extension install guide
  GET  /api/status     JSON {"has_cookies": bool, "domain": str, "stored_at": str}
  GET  /extension.zip  Download Chrome extension as zip
  GET  /ws             WebSocket — receives encrypted cookie blobs from the extension

Security model:
  • The server NEVER decrypts cookies.
  • It only stores the encrypted blob (salt + IV + ciphertext) to /data/cookies.enc.
  • Only the local CLI (with the master password) can decrypt.
"""

import io
import json
import logging
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from aiohttp import WSMsgType, web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
EXTENSION_DIR = Path(__file__).parent / "extension"
PORT = int(os.getenv("PORT", "9011"))
COOKIE_FILE = DATA_DIR / "cookies.enc"
META_FILE = DATA_DIR / "meta.json"

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Cookie Grabber — Server Status</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 700px; margin: 3rem auto; padding: 0 1rem; }}
    h1   {{ color: #2563eb; }}
    .ok  {{ color: #16a34a; font-weight: bold; }}
    .no  {{ color: #dc2626; font-weight: bold; }}
    pre  {{ background: #f1f5f9; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }}
    a    {{ color: #2563eb; }}
    ol   {{ line-height: 2; }}
  </style>
</head>
<body>
  <h1>🍪 Cookie Grabber Server</h1>
  <p>Status: <span id="status">loading…</span></p>
  <h2>Install the Extension</h2>
  <ol>
    <li>Download: <a href="/extension.zip">extension.zip</a></li>
    <li>Unzip to a local folder</li>
    <li>Open Chrome → <code>chrome://extensions</code> → Enable <em>Developer mode</em></li>
    <li>Click <strong>Load unpacked</strong> → select the unzipped folder</li>
    <li>Pin the extension and click it to open the popup</li>
  </ol>
  <h2>WebSocket endpoint</h2>
  <pre>ws://localhost:{port}/ws</pre>
  <h2>CLI usage (host machine)</h2>
  <pre>python cli.py status
python cli.py get --url https://your-api.example.com/data</pre>
  <script>
    fetch('/api/status')
      .then(r => r.json())
      .then(d => {{
        const el = document.getElementById('status');
        if (d.has_cookies) {{
          el.className = 'ok';
          el.textContent = '✅ Cookies stored — domain: ' + d.domain + '  captured: ' + d.stored_at;
        }} else {{
          el.className = 'no';
          el.textContent = '❌ No cookies stored yet — use the extension';
        }}
      }});
  </script>
</body>
</html>"""


async def handle_index(request: web.Request) -> web.Response:
    return web.Response(
        text=INDEX_HTML.format(port=PORT),
        content_type="text/html",
    )


async def handle_status(request: web.Request) -> web.Response:
    if META_FILE.exists() and COOKIE_FILE.exists():
        meta = json.loads(META_FILE.read_text(encoding="utf-8"))
        return web.json_response({"has_cookies": True, **meta})
    return web.json_response({"has_cookies": False})


async def handle_extension_zip(request: web.Request) -> web.Response:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in EXTENSION_DIR.rglob("*"):
            if f.is_file():
                zf.write(f, f.relative_to(EXTENSION_DIR))
    buf.seek(0)
    return web.Response(
        body=buf.read(),
        content_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="cookie-grabber-extension.zip"'},
    )


async def handle_ws(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    log.info("Extension connected from %s", request.remote)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                payload = json.loads(msg.data)
                domain = payload.get("domain", "unknown")
                encrypted = payload.get("encrypted")
                salt = payload.get("salt")
                iv = payload.get("iv")

                if not all([encrypted, salt, iv]):
                    await ws.send_str(json.dumps({"ok": False, "error": "Missing fields: encrypted, salt, iv"}))
                    continue

                DATA_DIR.mkdir(parents=True, exist_ok=True)
                # Store encrypted blob — server never decrypts
                COOKIE_FILE.write_text(
                    json.dumps({"version": 1, "domain": domain, "salt": salt, "iv": iv, "ciphertext": encrypted}),
                    encoding="utf-8",
                )
                META_FILE.write_text(
                    json.dumps({"domain": domain, "stored_at": datetime.now(timezone.utc).isoformat()}),
                    encoding="utf-8",
                )
                log.info("Stored encrypted cookies for domain: %s", domain)
                await ws.send_str(json.dumps({"ok": True, "domain": domain}))

            except json.JSONDecodeError as exc:
                log.warning("Invalid JSON from extension: %s", exc)
                await ws.send_str(json.dumps({"ok": False, "error": str(exc)}))

        elif msg.type == WSMsgType.ERROR:
            log.error("WebSocket error: %s", ws.exception())

    log.info("Extension disconnected")
    return ws


def main() -> None:
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/status", handle_status)
    app.router.add_get("/extension.zip", handle_extension_zip)
    app.router.add_get("/ws", handle_ws)
    log.info("Starting Cookie Grabber Server on port %d", PORT)
    web.run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
