# MCP Quiz

## Question 1
What is the main problem that Model Context Protocol (MCP) solves?

A) It makes AI models run faster  
B) It standardizes how AI assistants connect to data sources and tools  
C) It improves AI's ability to write code  
D) It reduces the cost of API calls  

**Correct Answer:** B

**Explanation:** MCP provides a standardized protocol for connecting AI assistants to various data sources and tools, eliminating the need to write custom integrations for each data source.

---

## Question 2
What is the key difference between VS Code and Cursor MCP configuration files?

A) VS Code uses `.vscode/mcp.json` with `"servers"`, Cursor uses `.cursor/mcp.json` with `"mcpServers"`  
B) VS Code doesn't support MCP  
C) Cursor requires additional authentication  
D) There is no difference  

**Correct Answer:** A

**Explanation:** VS Code places MCP config in `.vscode/mcp.json` with root key `"servers"`, while Cursor uses `.cursor/mcp.json` with root key `"mcpServers"`. The internal structure is otherwise the same.

---

## Question 3
Why does each MCP tool call require user approval?

A) To slow down AI responses  
B) To collect usage statistics  
C) Security - tools can execute code, access files, and modify data  
D) To test user attention  

**Correct Answer:** C

**Explanation:** MCP tools can perform powerful operations like executing code, reading/writing files, and calling APIs. Approval dialogs ensure users review what the tool will do before execution, preventing malicious or unintended operations.

---

## Question 4
How do multiple MCP servers affect your AI assistant's performance?

A) They make it faster  
B) They consume more context space, leading to slower responses and higher costs  
C) They have no impact  
D) They only affect memory usage  

**Correct Answer:** B

**Explanation:** Each MCP tool's description is added to the AI's context window. More tools mean less space for conversation, slower response times, and higher costs (for paid APIs). Best practice: enable only the servers you're actively using.

---

## Question 5
Which three core methods does the MCP JSON-RPC protocol use?

A) connect, disconnect, execute  
B) start, stop, run  
C) initialize, tools/list, tools/call  
D) setup, query, respond  

**Correct Answer:** C

**Explanation:** The MCP protocol uses three core methods:
- `initialize` - Establishes connection and exchanges capabilities
- `tools/list` - Returns available tools with their schemas
- `tools/call` - Executes a specific tool with provided parameters

---

## Question 6
When should you create a custom MCP server instead of using an existing one?

A) Never - always use existing servers  
B) When integrating proprietary systems or needing specialized operations  
C) Only if you know Python or TypeScript  
D) When existing servers are too expensive  

**Correct Answer:** B

**Explanation:** Create custom MCP servers when:
- No existing server fits your specific needs
- Integrating proprietary business systems
- Need specialized operations with custom logic

Use existing servers for standard functionality that's already been tested and maintained by the community.

---

## Question 7
What information appears in an MCP tool approval dialog?

A) Only the tool name  
B) Tool name, input parameters with values, and security warning  
C) Just the AI's reasoning  
D) File paths only  

**Correct Answer:** B

**Explanation:** The approval dialog shows:
- Tool name (e.g., "echo", "calculate")
- Input parameters with their values (e.g., `{"text": "Hello"}`)
- Security warning about potential misuse

This allows you to verify the AI is calling the correct tool with expected data before execution.

---

## Scoring Guide

- **7 correct:** Excellent! You fully understand MCP fundamentals
- **5-6 correct:** Good! Review sections on configuration differences and security
- **3-4 correct:** Review the walkthrough, especially Parts 1-2 and tool approval workflow
- **0-2 correct:** Revisit the entire walkthrough and practice with the echo server
