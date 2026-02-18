# Advanced MCP Integration in POC - Hands-on Walkthrough

You've built a web application prototype in Module 120. Now you'll add **MCP interface** to your application, giving AI agents direct programmatic access to your backend API. This transforms your app from something the agent can only see (through Chrome DevTools) to something the agent can **directly control and manipulate**.

With MCP integration, the AI agent can:
- Query your application's data
- Trigger backend operations
- Modify application state
- Debug and test API endpoints
- All without leaving the IDE

## Prerequisites

Before starting, ensure you have:
- Completed [Module 120: Rapid POC Prototyping](../120-rapid-poc-prototyping/about.md)
- Working web application in `work/120-task/`
- Node.js backend (Express, Fastify, or similar)
- Understanding of REST APIs
- Familiarity with MCP from Module 100

## What We'll Build

In this walkthrough, you'll:
- Understand why MCP integration matters for applications
- Study reference MCP server implementation patterns
- Create custom MCP server integrated with your backend
- Configure IDE to connect to your MCP server
- Test MCP integration with AI agent
- See real-world patterns for MCP-enabled applications

**Key insight:** MCP gives your application an **AI-native API**. Instead of writing documentation for humans to read and manually call APIs, you expose tools that AI agents can discover and use autonomously.

**Time required:** 25-30 minutes

---

## Part 1: Understanding MCP Integration

### What We'll Learn

Before coding, understand what MCP integration means for your application and why it's powerful.

---

### The Problem: Limited Agent Access

**Without MCP integration:**

Your web application has:
- Frontend UI (HTML/CSS/JS)
- Backend API (REST endpoints)
- Database

**AI agent can:**
- ✅ See the frontend (Chrome DevTools MCP from Module 130)
- ✅ Read your code files (Filesystem MCP)
- ❌ **Cannot directly call your backend API**
- ❌ **Cannot query your database**
- ❌ **Cannot trigger backend operations**

**Agent workaround:** Make HTTP requests using tools like `curl` or `fetch`, but:
- Requires knowing exact API endpoints and parameters
- No type safety or validation
- No discovery of available operations
- Error-prone and requires detailed documentation

---

### The Solution: MCP Server for Your Application

**With MCP integration:**

You create an **MCP server** that wraps your backend API and exposes it as **MCP tools**.

**AI agent can:**
- ✅ **Discover all available operations** (list users, create post, delete comment, etc.)
- ✅ **See tool schemas** (required parameters, types, descriptions)
- ✅ **Call operations directly** through MCP protocol
- ✅ **Get typed responses** with proper error handling
- ✅ **No need for API documentation** - tools are self-describing

**Example comparison:**

**Without MCP:**
```
Human instruction: "To create a user, POST to /api/users with JSON body containing name, email, and role fields. Name is required and must be 2-50 characters..."

Agent: Makes HTTP request, might get format wrong, lots of trial and error
```

**With MCP:**
```
Agent sees tool: "app_create_user" with schema showing required fields

Agent: Calls tool correctly on first try, gets structured response
```

---

### MCP Server Architecture

```
┌─────────────────────────────────────────────────┐
│  Your IDE (VS Code / Cursor)                   │
│                                                 │
│  ┌────────────────┐                            │
│  │  AI Agent      │                            │
│  │  (Claude)      │                            │
│  └────────┬───────┘                            │
│           │                                     │
│           │ Discovers & calls MCP tools        │
│           ↓                                     │
│  ┌────────────────┐                            │
│  │  MCP Client    │                            │
│  └────────┬───────┘                            │
└───────────┼─────────────────────────────────────┘
            │
            │ HTTP: POST http://localhost:3001/api/mcp
            │
┌───────────┼─────────────────────────────────────┐
│  Your Web Application Backend (port 3001)      │
│           │                                     │
│           ↓                                     │
│  ┌────────────────┐                            │
│  │  MCP HTTP      │                            │
│  │  Endpoint      │  /api/mcp                  │
│  └────────┬───────┘                            │
│           │                                     │
│           │ Translates to internal API calls   │
│           ↓                                     │
│  ┌────────────────┐      ┌──────────────┐     │
│  │  Your API      │─────→│  Database    │     │
│  │  Endpoints     │      └──────────────┘     │
│  └────────────────┘                            │
└─────────────────────────────────────────────────┘
```

**Key points:**
- MCP server runs as HTTP endpoint in your backend application
- Backend typically runs on port 3001 (or your chosen port)
- MCP endpoint handles POST requests at `/api/mcp`
- Agent calls tools through HTTP requests
- MCP endpoint translates to your internal API calls

---

### When to Add MCP to Your Application

**Good use cases:**
- **Development & debugging:** Agent can query data, test operations, fix bugs
- **Admin operations:** Agent can perform bulk operations, data cleanup, reports
- **Prototyping:** Rapidly test ideas by letting agent manipulate application state
- **Testing:** Agent can set up test data, run scenarios, verify results
- **Data analysis:** Agent can query your data and provide insights

**Not recommended for:**
- **Production user-facing features:** Use traditional REST API
- **Security-sensitive operations:** MCP typically runs in development mode
- **High-performance requirements:** MCP has overhead for schema validation
- **Public access:** MCP is designed for trusted development environments

---

## Part 2: Create MCP Server for Your Backend

### What We'll Do

Study the reference MCP server implementation, then create a custom MCP server integrated into your application's backend. The reference code serves as a template - you'll adapt it for your actual application.

---

### Step 1: Review Reference Implementation

The reference MCP server is provided in this module's `tools/` directory for study.

**Ask your AI agent:**

```
Show me the reference MCP server implementation from:
modules/140-advanced-mcp-integration-in-poc/tools/example-mcp-server.ts

Explain how it's structured:
- Tool definitions with schemas
- Handler functions
- MCP server setup
- Error handling patterns
```

**What to understand:**

The reference shows 3 tool patterns:
1. **`app_get_status`** - No parameters, returns data
2. **`app_get_user`** - With parameter, returns data or error
3. **`app_create_item`** - Multiple parameters, creates resource

These patterns cover all common MCP tool use cases.

---

### Step 2: Create MCP Server for Your Backend

Now create a custom MCP server integrated into your backend application.

**Ask your AI agent:**

```
Based on the reference MCP server in Module 140, create a custom MCP server for my backend application.

My backend structure:
work/120-task/backend/src/

Create:
work/120-task/backend/src/mcp/server.ts

My application is: [describe your app from Module 120]

Create MCP tools for these operations:
[List 3-5 operations your app provides]

Requirements:
- Use the same MCP SDK patterns as the reference
- Adapt tool names to my domain (not app_*, use my_app_*)
- Use mock data initially (we'll connect real API later)
- Include proper TypeScript types
- Add error handling for each tool
```

**Example for TODO app:**
```
Create MCP tools for:
- todo_list - Get all todos
- todo_get - Get todo by ID
- todo_create - Create new todo
- todo_update - Update todo (mark complete, change text)
- todo_delete - Delete todo by ID
```

---

### Step 3: Install MCP SDK in Backend

The agent will need MCP SDK in your backend project.

Navigate to backend directory:

```bash
# Windows
cd c:/workspace/hello-genai/work/120-task/backend

# macOS/Linux
cd ~/workspace/hello-genai/work/120-task/backend
```

**Ask your AI agent:**

```
Add @modelcontextprotocol/sdk to my backend dependencies and install.
```

The agent should update `package.json` and run `npm install`.

---

### Step 4: Build Your MCP Server

If your backend uses TypeScript, ensure MCP code compiles:

```bash
npm run build
```

Check that your MCP server compiled successfully:

```bash
# Example location - adjust for your project structure
ls backend/dist/mcp/server.js
```

---

### Step 5: Start Your Backend Server

Your MCP endpoint is part of your backend server. Start your backend:

```bash
cd backend
npm start
# or npm run dev for development mode
```

**Expected output:**
```
Server running on http://localhost:3001
MCP endpoint available at /api/mcp
```

**Your custom MCP server is ready! ✅**

---

## Part 3: Configure MCP in IDE

### What We'll Do

Add your MCP server to IDE configuration so the AI agent can discover and use it.

---

### Step 1: Identify Your IDE

**Which IDE are you using?**
- **VS Code** → Follow "For VS Code" instructions
- **Cursor** → Follow "For Cursor" instructions

---

### Step 2: Add MCP Server Configuration

**For VS Code:**

1. Open Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type: **"MCP: Edit Config"**
3. This opens `cline_mcp_settings.json`

**Add your MCP server** to `mcpServers`:

```json
{
  "mcpServers": {
    "my-app": {
      "type": "http",
      "url": "http://localhost:3001/api/mcp"
    }
  }
}
```

**Adjust the port and path** if your backend uses different settings:
- Default: `http://localhost:3001/api/mcp`
- Custom port: `http://localhost:YOUR_PORT/api/mcp`

**If you have other MCP servers**, add to the list:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@latest", "c:/workspace/hello-genai"]
    },
    "my-app": {
      "type": "http",
      "url": "http://localhost:3001/api/mcp"
    }
  }
}
```

---

**For Cursor:**

1. Open Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type: **"Cursor Settings: MCP"**
3. This opens MCP configuration

**Important:** Cursor uses **`servers`** instead of `mcpServers`.

```json
{
  "servers": {
    "my-app": {
      "type": "http",
      "url": "http://localhost:3001/api/mcp"
    }
  }
}
```

Adjust port and path if your backend uses different settings.

---

### Step 3: Restart IDE

Close and reopen your IDE for MCP configuration to take effect.

---

### Step 4: Verify MCP Server Connection

Open AI chat and ask:

```
Do you have access to "my-app" MCP server? List the available tools.
```

**Expected response:**
```
Yes, I have access to the my-app MCP server with these tools:

1. todo_list - Get all todos
2. todo_get - Get todo by ID (requires id parameter)
3. todo_create - Create new todo (requires title parameter)
4. todo_update - Update existing todo
5. todo_delete - Delete todo by ID
```

(Tool names will match what you created for your specific application)

**If tools are listed → MCP server configured successfully! ✅**

---

## Part 4: Test MCP Integration

### What We'll Do

Test the tools you created for your specific application to verify MCP integration works correctly.

---

### Test Your Custom Tools

The specific tests depend on what tools you created. Here's the general approach:

**Test 1: Tool with No Parameters (if you have one)**

Example for TODO app:

```
Use the todo_list tool to get all todos.
```

**Agent should:**
- Call your list tool
- Receive mock data

**✅ Test passed if agent shows your mock data.**

---

**Test 2: Tool with Parameters (Success Case)**

Example for TODO app:

```
Use todo_get tool to get details for todo ID "1".
```

**Agent should:**
- Call your get tool with parameter
- Receive todo data

**✅ Test passed if agent shows the todo.**

---

**Test 3: Tool with Parameters (Error Case)**

```
Try to get todo with ID "999" (should not exist).
```

**Agent should:**
- Call your get tool
- Receive error from your error handling

**✅ Test passed if agent reports error correctly.**

---

**Test 4: Tool that Creates/Modifies Data**

Example for TODO app:

```
Create a new todo with title "Test MCP Integration".
```

**Agent should:**
- Call your create tool
- Receive success response with created item

**✅ Test passed if item is created successfully.**

---

**Test 5: Tool Validation**

```
Try to create a todo without required parameters.
```

**Agent should:**
- Recognize missing required parameters from schema
- Ask you for the values or report that it cannot proceed

**✅ Test passed if agent handles validation correctly.**

---

**If all your custom tools work → MCP integration successful! ✅**

---

## Part 5: Connect to Real Backend API

### What We'll Do

Now that your MCP tools work with mock data, connect them to your actual backend API.

---

### Step 1: Understand Your Backend Architecture

**Ask yourself:**
- Where is my backend API logic? (controllers, services, routes?)
- Does my backend use a database? (in-memory, SQLite, PostgreSQL?)
- What functions already exist that I can reuse?

---

### Step 2: Connect MCP Tools to Backend Logic

**Ask your AI agent:**

```
Update my MCP server in backend/src/mcp/server.ts to call my real backend logic instead of mock data.

My backend structure:
- API routes: backend/src/routes/
- Business logic: backend/src/services/ (or controllers/)
- Database: [describe your setup]

For each MCP tool:
- Import the corresponding service/controller function
- Call it instead of returning mock data
- Handle errors from backend properly
- Return real data to MCP client

Maintain the same MCP tool interface (names, parameters, schemas).
```

**The agent will:**
- Import your backend modules
- Replace mock data with real function calls
- Add database queries if needed
- Preserve error handling

---

### Step 3: Test with Real Data

Rebuild your backend:

```bash
cd backend
npm run build
```

Restart your IDE to reload MCP server.

Test your tools again - now they should work with real data from your backend!

**Example test:**

```
Create a new todo with title "Real MCP Test".
Then list all todos to verify it was created.
```

**Agent should:**
- Create real todo in your database
- List real todos including the one just created

**✅ Connected to real backend successfully!**

---

## Part 6: Advanced MCP Patterns

### What We Learned

You've successfully created an MCP server that:
- Exposes your application functionality as MCP tools
- Validates inputs with schemas
- Handles errors gracefully
- Allows AI agents to control your application

### Advanced Patterns

**Pattern 1: Bulk Operations**

```typescript
{
  name: 'app_bulk_create_users',
  description: 'Create multiple users at once',
  inputSchema: {
    type: 'object',
    properties: {
      users: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            email: { type: 'string' },
            role: { type: 'string' },
          },
          required: ['name', 'email'],
        },
      },
    },
    required: ['users'],
  },
}
```

Allows agent to seed test data efficiently.

---

**Pattern 2: Complex Queries**

```typescript
{
  name: 'app_search_items',
  description: 'Search items with filters',
  inputSchema: {
    type: 'object',
    properties: {
      query: { type: 'string', description: 'Search text' },
      filters: {
        type: 'object',
        properties: {
          priority: { type: 'string', enum: ['low', 'medium', 'high'] },
          status: { type: 'string', enum: ['active', 'completed', 'archived'] },
          createdAfter: { type: 'string', description: 'ISO date string' },
        },
      },
      limit: { type: 'number', default: 10 },
      offset: { type: 'number', default: 0 },
    },
  },
}
```

Enables agent to perform sophisticated queries.

---

**Pattern 3: Admin Operations**

```typescript
{
  name: 'app_generate_report',
  description: 'Generate analytics report',
  inputSchema: {
    type: 'object',
    properties: {
      reportType: {
        type: 'string',
        enum: ['daily', 'weekly', 'monthly'],
      },
      format: {
        type: 'string',
        enum: ['json', 'csv', 'pdf'],
      },
    },
    required: ['reportType'],
  },
}
```

Agent can generate reports on demand.

---

**Pattern 4: State Inspection**

```typescript
{
  name: 'app_debug_state',
  description: 'Get internal application state for debugging',
  inputSchema: {
    type: 'object',
    properties: {
      component: {
        type: 'string',
        description: 'Specific component to inspect (optional)',
      },
    },
  },
}
```

Helps agent debug issues by inspecting internal state.

---

**Pattern 5: Database Operations**

```typescript
{
  name: 'app_db_query',
  description: 'Execute safe read-only database query',
  inputSchema: {
    type: 'object',
    properties: {
      table: { type: 'string', description: 'Table name' },
      where: { type: 'object', description: 'WHERE conditions' },
      limit: { type: 'number', default: 100 },
    },
    required: ['table'],
  },
}
```

**Warning:** Be very careful with direct database access. Add strict validation and read-only enforcement.

---

## Part 7: Real-World Development Workflow

### What We'll Do

See how MCP integration transforms your development workflow.

---

### Scenario 1: Debugging Data Issue

**Without MCP:**
```
User reports bug → Open database client → Write SQL query → Find issue → 
Fix code → Deploy → Ask user to verify
```

**With MCP:**
```
User reports bug → 
Ask agent: "Query our database for user 123's orders from last week" →
Agent shows data immediately →
Ask agent: "I see the issue. Fix the order calculation logic in orders.js" →
Agent fixes and tests →
Done in minutes
```

---

### Scenario 2: Setting Up Test Data

**Without MCP:**
```
Need test data → Write seeding script → Run script → 
Verify data was created → Now can test feature
```

**With MCP:**
```
Ask agent: "Create 10 test users with different roles and 50 test posts" →
Agent uses MCP tools to create data →
Ready to test immediately
```

---

### Scenario 3: API Testing

**Without MCP:**
```
Build new API endpoint → 
Open Postman → Configure request → Send → Check response →
Repeat for edge cases
```

**With MCP:**
```
Build new API endpoint →
Add MCP tool for it →
Ask agent: "Test the new create_order endpoint with valid data, invalid data, and edge cases" →
Agent tests all scenarios autonomously
```

---

### Scenario 4: Data Migration

**Without MCP:**
```
Need to migrate data → Write migration script → Test on sample →
Run on production → Hope nothing breaks
```

**With MCP:**
```
Ask agent: "I need to migrate all user records to add a new field 'premium_status'. 
Show me sample of current data first." →
Agent queries via MCP →
"Now write migration logic and test on one record" →
Agent tests →
"Looks good, apply to all records" →
Agent migrates data with progress updates
```

---

## Success Criteria

You've successfully completed this module when you can check off:

✅ Created custom MCP server in backend structure (not copied boilerplate)  
✅ MCP server integrated with backend (backend/src/mcp/server.ts)  
✅ Successfully built TypeScript MCP server  
✅ Configured IDE to connect to MCP server  
✅ AI agent can discover and list MCP tools  
✅ Tested custom tools with mock data  
✅ Connected MCP tools to real backend logic  
✅ Tested tools with real data from backend  
✅ Understanding of MCP integration patterns  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **What's the difference between REST API and MCP tools for an application?**
   
   Expected answer: REST API is for human-readable HTTP endpoints with documentation that humans read and manually call. MCP tools are self-describing with schemas that AI agents can automatically discover and call. MCP provides type safety, validation, and discovery built-in, while REST requires detailed documentation. MCP is optimized for AI consumption, REST for human consumption.

2. **Why use HTTP transport for MCP server in this example?**
   
   Expected answer: HTTP transport means MCP server exposes an HTTP endpoint (e.g., `/api/mcp`) that handles MCP protocol requests. This is ideal for web applications because the backend already runs as HTTP server. IDE makes POST requests to the endpoint. Benefits: (1) Integrates naturally with existing backend, (2) No need to spawn separate process, (3) Can reuse backend's database connections and services, (4) Easy to test with curl/Postman. Alternative is stdio transport where IDE spawns subprocess.

3. **What information goes into a tool's inputSchema?**
   
   Expected answer: inputSchema defines the tool's parameters using JSON Schema format: parameter names, types (string, number, boolean, object, array), descriptions, whether required or optional, default values, enums for allowed values, nested objects for complex parameters. This allows MCP clients to validate inputs before calling and helps AI agents understand what parameters are needed.

4. **Why is it important to handle errors in tool implementations?**
   
   Expected answer: Proper error handling ensures AI agents receive clear error messages they can understand and act on. Without good errors, agents might retry invalid operations, get confused about what went wrong, or provide poor feedback to users. Structured errors help agents debug issues and correct their approach. Always include descriptive error messages.

5. **When would you use MCP integration vs. traditional REST API?**
   
   Expected answer: Use MCP for: development/debugging workflows, admin operations, AI agent interactions, rapid prototyping, internal tools. Use traditional REST API for: production user-facing features, public APIs, mobile apps, third-party integrations, when you need standard HTTP caching/security. Often you'll have both—REST for users, MCP for developers/agents.

6. **What's the purpose of the `tools` array in the MCP server?**
   
   Expected answer: The tools array defines all available operations the MCP server provides. When an MCP client connects and requests ListTools, the server returns this array. Each tool includes name, description, and input schema. This enables automatic discovery—agents can see what operations are available without needing separate documentation. It's like an automatically generated, machine-readable API specification.

7. **How would you secure an MCP server in a real application?**
   
   Expected answer: Security considerations: (1) Only expose MCP in development environments, not production, (2) Add authentication/authorization checks in tool handlers, (3) Validate all inputs rigorously, (4) Use read-only database connections where possible, (5) Rate limit operations, (6) Log all MCP tool calls for audit, (7) Run MCP server with minimal privileges, (8) Never expose MCP endpoints publicly. Remember: MCP is for trusted development use, not public access.

---

## Troubleshooting

### Problem: MCP server not appearing in IDE tool list

**Symptoms:** Agent says "I don't have access to my-app MCP server"

**Solutions:**
1. **Verify MCP config has correct URL:**
   - Default: `http://localhost:3001/api/mcp`
   - Check your backend's actual port number
   - Ensure URL includes `/api/mcp` path
2. **Check backend server is running:**
   ```bash
   curl http://localhost:3001/api/mcp
   ```
   Should return MCP protocol response (not 404)
3. **Test MCP endpoint manually:**
   ```bash
   curl -X POST http://localhost:3001/api/mcp \
     -H "Content-Type: application/json" \
     -d '{"method": "tools/list"}'
   ```
   Should return list of tools
4. **Check for TypeScript compilation errors:**
   ```bash
   cd backend
   npm run build
   ```
5. **Restart IDE completely** (not just reload window)
6. **Check backend logs for errors** when IDE tries to connect

---

### Problem: "Module not found" error when running MCP server

**Symptoms:** Error mentions `@modelcontextprotocol/sdk` not found

**Solutions:**
1. **Install dependencies in backend directory:**
   ```bash
   cd backend
   npm install
   ```
2. **Verify package.json has the SDK:**
   ```json
   "dependencies": {
     "@modelcontextprotocol/sdk": "^0.5.0"
   }
   ```
3. **Try reinstalling:**
   ```bash
   rm -rf node_modules
   npm install
   ```

---

### Problem: MCP server connects but tools fail with errors

**Symptoms:** Agent can see tools but calling them produces errors

**Solutions:**
1. **Check MCP server console for errors:**
   - Errors are logged to stderr
   - Look in IDE output panel for MCP server logs
2. **Verify tool handler switch statement includes all tool names:**
   ```typescript
   case 'todo_get':  // Must match tool name exactly
   ```
3. **Test tool logic independently:**
   ```typescript
   // Add debugging
   console.error(`[MCP] Calling tool: ${name} with args:`, args);
   ```
4. **Validate parameter types match schema:**
   ```typescript
   // If schema says id is string, don't pass number
   ```

---

### Problem: MCP server can't connect to backend logic

**Symptoms:** Tools work with mock data but fail when calling real backend

**Solutions:**
1. **Verify backend modules are properly imported:**
   ```typescript
   import { TodoService } from '../services/TodoService.js';
   ```
2. **Check if backend is running (if MCP calls HTTP endpoints):**
   ```bash
   curl http://localhost:3000/api/status
   ```
3. **Add logging in MCP tool handlers:**
   ```typescript
   console.error(`[MCP] Calling backend function:`, functionName);
   const result = await backendFunction(args);
   console.error(`[MCP] Backend response:`, result);
   ```
4. **Handle backend errors:**
   ```typescript
   try {
     const result = await todoService.create(args);
     return result;
   } catch (error) {
     console.error('[MCP] Backend error:', error);
     throw new Error(`Backend error: ${error.message}`);
   }
   ```

---

### Problem: TypeScript compilation errors

**Symptoms:** `npm run build` fails with type errors

**Solutions:**
1. **Check imports use `.js` extension:**
   ```typescript
   // Correct
   import { Server } from '@modelcontextprotocol/sdk/server/index.js';
   
   // Wrong
   import { Server } from '@modelcontextprotocol/sdk/server/index';
   ```
2. **Verify tsconfig.json module settings:**
   ```json
   {
     "compilerOptions": {
       "module": "commonjs",  // or "ESNext"
       "esModuleInterop": true
     }
   }
   ```
3. **Update SDK version if outdated:**
   ```bash
   npm install @modelcontextprotocol/sdk@latest
   ```

---

## Next Steps

**Congratulations!** You've mastered MCP integration for your applications. Here's what comes next:

1. **Expand your MCP tools**
   
   Add more operations:
   - Analytics and reporting tools
   - Data export/import tools
   - Database maintenance tools
   - Testing utilities

2. **Integrate with multiple applications**
   
   Create MCP servers for:
   - Frontend application
   - Backend services
   - Database management
   - Third-party integrations

3. **Build development workflows**
   
   Combine MCP with:
   - Automated testing (Module 130 Chrome DevTools)
   - Version control (Module 060 Git)
   - Deployment automation
   - Monitoring and debugging

4. **Explore MCP protocol features**
   
   Advanced capabilities:
   - Resources (expose application data as resources)
   - Prompts (define reusable prompt templates)
   - Sampling (let MCP server request AI completions)
   - Progress notifications for long operations

5. **Continue to Module 150: GitHub Coding Agent Delegation**
   
   Learn how to delegate complete development tasks to GitHub Copilot Agent.

---

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/specification)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [Example MCP Servers](https://github.com/modelcontextprotocol/servers)
- [JSON Schema Guide](https://json-schema.org/learn/getting-started-step-by-step)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)

---

**Ready to continue your training?** Head to [Module 150: GitHub Coding Agent Delegation](../150-github-coding-agent-delegation/about.md)
