# CLI: Command Line Interface - Hands-on Walkthrough

In Module 100, you saw AI calling tools through the MCP protocol — AI acted as a middleman, reading tool schemas, constructing JSON-RPC calls, and routing results back to you. Now let's look at the alternative: calling the same tools **directly from the terminal using curl**, with no LLM in the middle at all.

You'll run the same three tools (`echo`, `get_time`, `calculate`) on a local REST server and feel the direct connection — then understand when this matters and why.

## Prerequisites

- Completed [Module 100: Model Context Protocol (MCP)](../100-mcp-model-context-protocol/about.md)
- Terminal (PowerShell on Windows, or any shell on macOS/Linux)
- curl — pre-installed on Windows 10+, macOS, and all Linux distros
- Python 3 — pre-installed on macOS/Linux; on Windows check with `python --version`

---

## What We'll Build

A minimal local REST server with the same 3 tools from Module 100:

| Tool | Module 100 (MCP) | Module 103 (REST + CLI) |
|---|---|---|
| echo | AI calls `echo` tool via JSON-RPC | `curl POST /echo` |
| get_time | AI calls `get_time` tool via JSON-RPC | `curl GET /time` |
| calculate | AI calls `calculate` tool via JSON-RPC | `curl POST /calculate` |
| **file upload** | ❌ not possible natively | ✅ `curl -F "file=@..."` |

This lets you compare both approaches side-by-side with identical functionality.

---

## Part 1: Start the REST Server

### 1.1 Windows (PowerShell)

Open a terminal and run:

```powershell
powershell -ExecutionPolicy Bypass -File ./modules/103-cli-command-line-interface/tools/rest-server.ps1
```

To **stop the server** at any time (run in a second terminal):

```powershell
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%rest-server%'" | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

You should see:
```
REST server running at http://localhost:8080
Available endpoints:
  POST /echo        - body: {"text": "hello"}
  GET  /time        - returns current timestamp
  POST /calculate   - body: {"a": 10, "b": 5, "operation": "add"}
  POST /upload      - multipart file upload (binary demo)
Press Ctrl+C to stop
```

### 1.2 macOS / Linux (Python)

Make the script executable and run it:

```bash
chmod +x ./modules/103-cli-command-line-interface/tools/rest-server.sh
python3 ./modules/103-cli-command-line-interface/tools/rest-server.sh
```

Same output as above. The Python script uses only built-in modules — nothing to install.

> **Keep this terminal open.** Open a second terminal for the curl commands below.

---

## Part 2: Call the Tools via curl

These commands mirror what MCP did in Module 100 — but now you're calling the server directly.

### echo

```powershell
# Windows PowerShell
(Invoke-WebRequest -Uri http://localhost:8080/echo -Method POST `
  -ContentType "application/json" `
  -Body '{"text": "Hello CLI!"}' -UseBasicParsing).Content
```

```bash
# macOS / Linux
curl -s -X POST http://localhost:8080/echo \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello CLI!"}'
```

Expected response:
```json
{"result": "Echo: Hello CLI!"}
```

### get_time

```powershell
# Windows PowerShell
(Invoke-WebRequest -Uri http://localhost:8080/time -UseBasicParsing).Content
```

```bash
# macOS / Linux
curl -s http://localhost:8080/time
```

Expected response:
```json
{"result": "Current time: 2026-02-23 14:30:00"}
```

### calculate

```powershell
# Windows PowerShell
(Invoke-WebRequest -Uri http://localhost:8080/calculate -Method POST `
  -ContentType "application/json" `
  -Body '{"a": 42, "b": 17, "operation": "multiply"}' -UseBasicParsing).Content
```

```bash
# macOS / Linux
curl -s -X POST http://localhost:8080/calculate \
  -H "Content-Type: application/json" \
  -d '{"a": 42, "b": 17, "operation": "multiply"}'
```

Expected response:
```json
{"result": "Result: 42 multiply 17 = 714"}
```

---

## Part 3: Send a Binary File

This is where CLI outperforms MCP. Create a test file and send it:

```powershell
# Windows - create a test file
"Hello binary world" | Out-File -Encoding utf8 ./work/test-upload.txt

# Upload it as raw bytes
$bytes = [System.IO.File]::ReadAllBytes("$PWD/work/test-upload.txt")
$r = Invoke-WebRequest -Uri http://localhost:8080/upload -Method POST `
  -ContentType "application/octet-stream" -Body $bytes -UseBasicParsing
$r.Content
```

```bash
# macOS / Linux
echo "Hello binary world" > /tmp/test-upload.txt
curl -s -X POST http://localhost:8080/upload \
  --data-binary @/tmp/test-upload.txt \
  -H "Content-Type: application/octet-stream"
```

Expected response:
```json
{
  "result": "File received successfully",
  "bytes": 45,
  "content_type": "application/octet-stream",
  "note": "Binary data arrived intact - no encoding needed"
}
```

Try uploading any real file — a PDF, an image, a `.zip` archive. The server will receive the raw bytes regardless of format.

---

## Part 4: When to Bypass the LLM — and Why It Matters

> **This is the core concept of this module.** Read it carefully.

### How MCP works (with LLM in the middle)

```
You → LLM reads your prompt
        ↓
      LLM writes a tool call (JSON-RPC)
        ↓
      MCP server executes the tool
        ↓
      Result goes back to LLM
        ↓
      LLM re-writes the result in its response
        ↓
You ← You read the LLM's version of the result
```

### How CLI works (LLM-free path)

```
You → curl command
        ↓
      REST server executes the tool
        ↓
You ← You read the raw result directly
```

### Why bypassing LLM matters

**1. Hallucination risk is eliminated**

LLM never "copies" text — it always **re-generates** it token by token. When a result passes through LLM, it can silently alter numbers, names, dates, or code snippets. Example:

- Server returns: `"Result: 42 multiply 17 = 714"`
- LLM might return: `"The result is 714"` ✅ — or — `"The answer is 741"` ❌ (digit swap)

With curl, what the server returns is exactly what you see. No rewriting, no risk.

**2. Token savings**

Every tool call through MCP costs tokens:
- Tool schema in context (input tokens)
- AI reasoning about which tool to use (input tokens)
- AI writing the tool call parameters (output tokens)
- AI re-phrasing the result (output tokens)

With curl, you pay 0 tokens. For automation scripts that run hundreds of calls, this is a significant cost and speed difference.

**3. Binary files don't need encoding**

To send a file through MCP today, you'd have to:
1. Read the file into memory
2. Base64-encode it (+33% size)
3. Pass it as a string parameter in JSON
4. Decode it on the server side

With curl `-F "file=@..."`:
- Raw bytes go directly over HTTP
- No encoding, no size penalty
- Works for any file type: images, PDFs, ZIPs, executables

**Summary table:**

| | MCP (via LLM) | CLI (curl) |
|---|---|---|
| Hallucination risk | ⚠️ LLM re-generates results | ✅ Zero — direct output |
| Token cost | 🔴 High — schema + reasoning + output | ✅ Zero |
| Binary files | ❌ Requires Base64 encoding | ✅ Native multipart |
| Human-readable | ✅ Natural language in/out | ⚠️ JSON in/out |
| AI chaining tools | ✅ AI decides what to call | ❌ You decide explicitly |

**Rule of thumb:**
- Use **MCP** when you want AI to reason, chain tools, or translate natural language to actions
- Use **CLI** when you need precision, speed, binary data, or zero hallucination risk

---

## Success Criteria

✅ REST server starts without errors on your OS  
✅ `curl` calls return correct responses for all three tools  
✅ Binary file upload returns `"bytes"` count in the response  
✅ You can explain why CLI bypasses LLM and why that matters  
✅ You can name two concrete situations where CLI is better than MCP  

---

## Understanding Check

1. **What is the difference between CLI and REST API?**

   Expected answer: CLI is a tool (program) you run on your machine. REST API is a protocol for communication over HTTP. CLI tools like curl use REST API internally — they are a client, REST is the transport.

2. **Why does sending data through LLM introduce hallucination risk?**

   Expected answer: LLM doesn't copy text — it regenerates it token by token. Any value that passes through LLM (numbers, names, JSON fields) can be subtly altered. Direct CLI calls return raw server output with no LLM rewriting.

3. **Why is sending a binary file through MCP considered overengineering?**

   Expected answer: MCP uses JSON, which is text-only. To include binary data in JSON, you must Base64-encode it, which adds ~33% size overhead and requires encode/decode logic on both sides. curl's multipart upload sends raw bytes with no conversion.

4. **When would you prefer MCP over CLI?**

   Expected answer: When you need AI to interpret natural language, reason about which tool to use, chain multiple tools together, or explain results in human-readable form. MCP is ideal for conversational, exploratory workflows.

5. **How many tokens does a curl call cost?**

   Expected answer: Zero. curl calls the server directly without involving the LLM at all.

---

## Troubleshooting

### Problem: "Address already in use" / port 8080 taken

```bash
# macOS / Linux - find and kill process on port 8080
lsof -ti:8080 | xargs kill
```

```powershell
# Windows PowerShell - kill by script name (safer than by port)
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%rest-server%'" | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

> **Note:** Killing by port on Windows may hit system processes (PID 4). Always stop by script name instead.

### Problem: curl not found on Windows

curl is bundled with Windows 10+ (since 2018). If missing, download from https://curl.se/windows/ or use:
```powershell
Invoke-WebRequest -Uri http://localhost:8080/time -Method GET
```

### Problem: PowerShell HttpListener access denied

Run PowerShell as Administrator, or use a port above 1024 (8080 should work without elevation on most systems).

### Problem: Python not found on Windows

Install Python from https://python.org/downloads — check "Add to PATH" during installation. Then restart the terminal.

---

## Next Steps

You now understand both sides of tool execution: through LLM (MCP) and directly (CLI).

Continue to [Module 105: MCP GitHub Integration](../105-mcp-github-integration-issues/about.md) to see MCP used for a real-world case where AI reasoning adds value — managing GitHub issues through natural language.
