#!/usr/bin/env python3
# REST server in Python - same 3 tools as MCP echo server
# Endpoints: POST /echo, GET /time, POST /calculate, POST /upload
# Requires no external dependencies - uses built-in http.server and json modules

import json
import cgi
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8080

class RestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[{self.command}] {self.path}")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length)

    def do_GET(self):
        if self.path == "/time":
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.send_json({"result": f"Current time: {now}"})
        else:
            self.send_json({"error": f"Not found: {self.path}"}, 404)

    def do_POST(self):
        if self.path == "/echo":
            raw = self.read_body()
            try:
                body = json.loads(raw)
                if "text" not in body:
                    raise ValueError("Missing required field: text")
                self.send_json({"result": f"Echo: {body['text']}"})
            except Exception as e:
                print(f"  [ERROR] /echo: {e}")
                self.send_json({"error": f"Bad request: {e}", "received": raw.decode("utf-8", errors="replace")}, 400)

        elif self.path == "/calculate":
            raw = self.read_body()
            try:
                body = json.loads(raw)
                a = body.get("a")
                b = body.get("b")
                op = body.get("operation")
                if a is None or b is None or op is None:
                    raise ValueError("Missing required fields: a, b, operation")
                ops = {"add", "subtract", "multiply", "divide"}
                if op not in ops:
                    raise ValueError(f"Unknown operation: {op}. Use: add, subtract, multiply, divide")
                if op == "divide" and b == 0:
                    raise ValueError("Division by zero")
                result = {"add": a+b, "subtract": a-b, "multiply": a*b, "divide": a/b}[op]
                self.send_json({"result": f"Result: {a} {op} {b} = {result}"})
            except Exception as e:
                print(f"  [ERROR] /calculate: {e}")
                self.send_json({"error": f"Bad request: {e}", "received": raw.decode("utf-8", errors="replace")}, 400)

        elif self.path == "/upload":
            # Read raw bytes - works for any binary content
            content_type = self.headers.get("Content-Type", "")
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            self.send_json({
                "result": "File received successfully",
                "bytes": len(raw),
                "content_type": content_type,
                "note": "Binary data arrived intact - no encoding needed"
            })

        else:
            self.send_json({"error": f"Not found: {self.path}"}, 404)


if __name__ == "__main__":
    print(f"REST server running at http://localhost:{PORT}")
    print("Available endpoints:")
    print('  POST /echo        - body: {"text": "hello"}')
    print("  GET  /time        - returns current timestamp")
    print('  POST /calculate   - body: {"a": 10, "b": 5, "operation": "add"}')
    print("  POST /upload      - multipart file upload (binary demo)")
    print("Press Ctrl+C to stop\n")
    server = HTTPServer(("localhost", PORT), RestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
