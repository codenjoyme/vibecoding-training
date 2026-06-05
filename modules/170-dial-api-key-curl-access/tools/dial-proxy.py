# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "urllib3",
# ]
# ///
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from http.server import HTTPServer
import requests
import json
import urllib3
import os
import sys
import re
import uuid
import io

# Ensure UTF-8 output on Windows (cp1252 can't encode emoji)
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

urllib3.disable_warnings()

DIAL_BASE = "https://ai-proxy.lab.epam.com"
PORT = 4000
API_KEY = os.environ.get("DIAL_API_KEY", "")
STRIP_PARAMS = ["temperature", "top_p", "presence_penalty", "frequency_penalty", "stream_options"]
# Must match the 'id' field in chatLanguageModels.json for this entry
SPOOF_MODEL = "gpt-4o-2024-11-20"

if not API_KEY:
    print("❌ $env:DIAL_API_KEY = 'your-key'")
    sys.exit(1)

SESSION = requests.Session()
SESSION.verify = False
SESSION.headers.update({"Content-Type": "application/json", "api-key": API_KEY})

# Маппинг Anthropic tool IDs → OpenAI tool IDs (сохраняем в рамках запроса)
tool_id_map = {}


def rewrite_tool_call_id(original_id):
    """Конвертирует toolu_bdrk_... в call_... формат"""
    if not original_id:
        return original_id
    if original_id.startswith("call_"):
        return original_id
    if original_id not in tool_id_map:
        tool_id_map[original_id] = f"call_{uuid.uuid4().hex[:24]}"
    return tool_id_map[original_id]


def patch_response_obj(obj):
    """Патчит объект ответа: model + tool call IDs"""
    if not isinstance(obj, dict):
        return obj

    # Подменяем model
    if "model" in obj:
        obj["model"] = SPOOF_MODEL

    # Патчим choices
    choices = obj.get("choices", [])
    for choice in choices:
        delta = choice.get("delta", {})
        message = choice.get("message", {})

        # Патчим tool_calls в delta (streaming)
        for tool_call in delta.get("tool_calls", []):
            if "id" in tool_call and tool_call["id"]:
                tool_call["id"] = rewrite_tool_call_id(tool_call["id"])

        # Патчим tool_calls в message (non-streaming)
        for tool_call in message.get("tool_calls", []):
            if "id" in tool_call and tool_call["id"]:
                tool_call["id"] = rewrite_tool_call_id(tool_call["id"])

    return obj


def patch_request_data(data):
    """Патчит запрос: убирает лишние параметры, фиксит tool_call_id в messages"""
    # Убираем неподдерживаемые параметры
    removed = [p for p in STRIP_PARAMS if p in data]
    for p in STRIP_PARAMS:
        data.pop(p, None)

    # Фиксим tool_call_id в messages (если Copilot вернул наш переписанный ID)
    messages = data.get("messages", [])
    for msg in messages:
        # tool role messages имеют tool_call_id
        if msg.get("role") == "tool" and "tool_call_id" in msg:
            tc_id = msg["tool_call_id"]
            # Ищем оригинальный ID по нашему маппингу
            for orig, rewritten in tool_id_map.items():
                if rewritten == tc_id:
                    msg["tool_call_id"] = orig
                    break

        # assistant messages могут иметь tool_calls
        if msg.get("role") == "assistant" and "tool_calls" in msg:
            for tc in msg["tool_calls"]:
                if "id" in tc:
                    for orig, rewritten in tool_id_map.items():
                        if rewritten == tc["id"]:
                            tc["id"] = orig
                            break

    return data, removed


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class ProxyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        is_stream = False
        try:
            data = json.loads(body)
            data, removed = patch_request_data(data)
            is_stream = data.get("stream", False)
            if removed:
                print(f"  🧹 Stripped: {', '.join(removed)}")
            body = json.dumps(data).encode()
        except json.JSONDecodeError:
            pass

        url = f"{DIAL_BASE}{self.path}"
        print(f"📤 POST {self.path} (stream={is_stream})")

        try:
            resp = SESSION.post(url, data=body, timeout=180, stream=is_stream)

            if not resp.ok:
                print(f"  ❌ {resp.status_code}: {resp.text[:200]}")
                self._send(resp.status_code, resp.content)
                return

            if is_stream:
                print(f"  ✅ Streaming...")
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.end_headers()

                try:
                    for chunk in resp.iter_lines():
                        if chunk:
                            line = chunk.decode("utf-8")
                            if line.startswith("data: ") and line.strip() != "data: [DONE]":
                                try:
                                    obj = json.loads(line[6:])
                                    obj = patch_response_obj(obj)
                                    line = "data: " + json.dumps(obj)
                                except (json.JSONDecodeError, ValueError):
                                    pass
                            self.wfile.write(f"{line}\n\n".encode())
                            self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError, OSError):
                    print(f"  ⚠️  Client disconnected")
                finally:
                    resp.close()
                print(f"  ✅ Done")
            else:
                content = resp.content
                try:
                    obj = json.loads(content)
                    obj = patch_response_obj(obj)
                    content = json.dumps(obj).encode()
                except:
                    pass
                print(f"  ✅ {resp.status_code}")
                self._send(resp.status_code, content)

        except Exception as e:
            print(f"  💥 {e}")
            self._send(502, json.dumps({"error": {"message": str(e)}}).encode())

    def do_GET(self):
        url = f"{DIAL_BASE}{self.path}"
        try:
            resp = SESSION.get(url, timeout=30)
            self._send(resp.status_code, resp.content)
        except Exception as e:
            self._send(502, json.dumps({"error": {"message": str(e)}}).encode())

    def _send(self, status, content):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, *args):
        pass


print(f"🚀 DIAL proxy on http://localhost:{PORT}")
print(f"🔑 Key: {API_KEY[:8]}...")
print(f"🎭 Spoof model: {SPOOF_MODEL}")
print(f"🧹 Strip: {STRIP_PARAMS}")
print(f"🔄 Tool ID rewrite: toolu_bdrk_* → call_*")
print(f"🧵 Threading: enabled")
print()
ThreadingHTTPServer(("localhost", PORT), ProxyHandler).serve_forever()