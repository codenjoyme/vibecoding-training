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
            body = json.loads(self.read_body())
            self.send_json({"result": f"Echo: {body.get('text', '')}"})

        elif self.path == "/calculate":
            body = json.loads(self.read_body())
            a = body.get("a", 0)
            b = body.get("b", 0)
            op = body.get("operation", "")
            ops = {
                "add":      a + b,
                "subtract": a - b,
                "multiply": a * b,
                "divide":   a / b if b != 0 else None,
            }
            if op not in ops or ops[op] is None:
                self.send_json({"error": f"Invalid operation or division by zero: {op}"}, 400)
            else:
                result = ops[op]
                self.send_json({"result": f"Result: {a} {op} {b} = {result}"})

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
