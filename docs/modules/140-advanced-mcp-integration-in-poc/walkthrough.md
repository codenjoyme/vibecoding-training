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
- Create boilerplate MCP server with 3 example tools
- Add MCP endpoint to your backend API
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
            │ MCP Protocol (HTTP or stdio)
            │
┌───────────┼─────────────────────────────────────┐
│  Your Web Application Backend                  │
│           │                                     │
│           ↓                                     │
│  ┌────────────────┐                            │
│  │  MCP Server    │                            │
│  │  Endpoint      │                            │
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
- MCP server runs as part of your backend application
- Exposes tools that wrap your existing API logic
- Agent calls tools through MCP protocol
- MCP server translates to your internal API calls

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

## Part 2: Create Boilerplate MCP Server

### What We'll Do

Create a reference MCP server implementation with 3 example tools. This serves as a template you can adapt for your actual application.

---

### Step 1: Create Tools Directory

Navigate to your project:

```bash
# Windows
cd c:/workspace/hello-genai/work/120-task

# macOS/Linux
cd ~/workspace/hello-genai/work/120-task
```

Create `tools/` directory for MCP server code:

```bash
mkdir tools
```

This directory will contain reference MCP server implementations.

---

### Step 2: Initialize TypeScript Project in Tools

```bash
cd tools
npm init -y
npm install --save-dev typescript @types/node
npm install @modelcontextprotocol/sdk
```

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

Create directory structure:

```bash
mkdir src
```

---

### Step 3: Create Boilerplate MCP Server

Create `src/example-mcp-server.ts`:

```typescript
#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

/**
 * Example MCP Server - Boilerplate Reference
 * 
 * This is a reference implementation showing 3 types of tools:
 * 1. Tool with no parameters, returns data (get_status)
 * 2. Tool with parameters, returns data (get_user)
 * 3. Tool with parameters, returns success (create_item)
 * 
 * Adapt this pattern to your actual application.
 */

// === Tool Definitions ===

const tools: Tool[] = [
  // Tool 1: No parameters, returns data
  {
    name: 'app_get_status',
    description: 'Get current application status and statistics',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },

  // Tool 2: With parameters, returns data
  {
    name: 'app_get_user',
    description: 'Get user details by ID',
    inputSchema: {
      type: 'object',
      properties: {
        userId: {
          type: 'string',
          description: 'User ID to retrieve',
        },
      },
      required: ['userId'],
    },
  },

  // Tool 3: With parameters, returns success/failure
  {
    name: 'app_create_item',
    description: 'Create a new item in the system',
    inputSchema: {
      type: 'object',
      properties: {
        title: {
          type: 'string',
          description: 'Item title',
        },
        description: {
          type: 'string',
          description: 'Item description (optional)',
        },
        priority: {
          type: 'string',
          enum: ['low', 'medium', 'high'],
          description: 'Item priority level',
        },
      },
      required: ['title', 'priority'],
    },
  },
];

// === Tool Implementations ===

async function handleGetStatus(): Promise<any> {
  // In real app: query your database, check services, etc.
  return {
    status: 'online',
    uptime: '24h 15m',
    users_online: 42,
    requests_today: 1337,
    database: 'connected',
    cache: 'healthy',
  };
}

async function handleGetUser(userId: string): Promise<any> {
  // In real app: query your database
  // Mock data for demonstration
  const mockUsers: Record<string, any> = {
    '1': { id: '1', name: 'Alice Johnson', email: 'alice@example.com', role: 'admin' },
    '2': { id: '2', name: 'Bob Smith', email: 'bob@example.com', role: 'user' },
    '3': { id: '3', name: 'Carol White', email: 'carol@example.com', role: 'user' },
  };

  const user = mockUsers[userId];
  if (!user) {
    throw new Error(`User with ID ${userId} not found`);
  }

  return user;
}

async function handleCreateItem(
  title: string,
  description: string | undefined,
  priority: 'low' | 'medium' | 'high'
): Promise<any> {
  // In real app: insert into database
  // Mock implementation for demonstration
  const newItem = {
    id: `item_${Date.now()}`,
    title,
    description: description || null,
    priority,
    created_at: new Date().toISOString(),
    status: 'active',
  };

  console.error(`[MCP] Created item: ${JSON.stringify(newItem)}`);

  return {
    success: true,
    item: newItem,
    message: `Item "${title}" created successfully`,
  };
}

// === MCP Server Setup ===

const server = new Server(
  {
    name: 'example-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handle tool listing
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: any;

    switch (name) {
      case 'app_get_status':
        result = await handleGetStatus();
        break;

      case 'app_get_user':
        result = await handleGetUser(args.userId);
        break;

      case 'app_create_item':
        result = await handleCreateItem(args.title, args.description, args.priority);
        break;

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error: any) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// === Start Server ===

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Example MCP server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
```

---

### Step 4: Add Build Script

Update `tools/package.json` to add build script:

```json
{
  "name": "mcp-tools",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "start": "node dist/example-mcp-server.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0"
  }
}
```

---

### Step 5: Build the MCP Server

```bash
npm run build
```

**Expected output:**
```
> mcp-tools@1.0.0 build
> tsc

[No errors means successful compilation]
```

Check that `dist/example-mcp-server.js` was created:

```bash
ls dist/
```

**Boilerplate MCP server is ready! ✅**

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
      "command": "node",
      "args": ["c:/workspace/hello-genai/work/120-task/tools/dist/example-mcp-server.js"]
    }
  }
}
```

**Adjust the path** for your OS:
- Windows: `c:/workspace/hello-genai/work/120-task/tools/dist/example-mcp-server.js`
- macOS/Linux: `~/workspace/hello-genai/work/120-task/tools/dist/example-mcp-server.js`

**If you have other MCP servers**, add to the list:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@latest", "c:/workspace/hello-genai"]
    },
    "my-app": {
      "command": "node",
      "args": ["c:/workspace/hello-genai/work/120-task/tools/dist/example-mcp-server.js"]
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
      "command": "node",
      "args": ["c:/workspace/hello-genai/work/120-task/tools/dist/example-mcp-server.js"]
    }
  }
}
```

Adjust path for your OS as shown above.

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

1. app_get_status - Get current application status and statistics
2. app_get_user - Get user details by ID (requires userId parameter)
3. app_create_item - Create a new item (requires title and priority)
```

**If tools are listed → MCP server configured successfully! ✅**

---

## Part 4: Test MCP Integration

### What We'll Do

Test each of the 3 example tools to verify MCP integration works correctly.

---

### Test 1: Tool with No Parameters

**Ask your AI agent:**

```
Use the app_get_status tool to get application status.
```

**Agent should:**
- Call `app_get_status` tool
- Receive mock status data

**Expected output:**
```json
{
  "status": "online",
  "uptime": "24h 15m",
  "users_online": 42,
  "requests_today": 1337,
  "database": "connected",
  "cache": "healthy"
}
```

**✅ Test 1 passed if agent shows this data.**

---

### Test 2: Tool with Parameters (Success Case)

**Ask your AI agent:**

```
Use app_get_user tool to get details for user ID "1".
```

**Agent should:**
- Call `app_get_user` with parameter `userId: "1"`
- Receive user data

**Expected output:**
```json
{
  "id": "1",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "role": "admin"
}
```

**✅ Test 2 passed if agent shows Alice's data.**

---

### Test 3: Tool with Parameters (Error Case)

**Ask your AI agent:**

```
Try to get user with ID "999" (should not exist).
```

**Agent should:**
- Call `app_get_user` with parameter `userId: "999"`
- Receive error

**Expected output:**
```
Error: User with ID 999 not found
```

**✅ Test 3 passed if agent reports error correctly.**

---

### Test 4: Tool with Multiple Parameters

**Ask your AI agent:**

```
Create a new item with title "Test Task", priority "high", and description "Testing MCP integration".
```

**Agent should:**
- Call `app_create_item` with all parameters
- Receive success response with created item

**Expected output:**
```json
{
  "success": true,
  "item": {
    "id": "item_1234567890",
    "title": "Test Task",
    "description": "Testing MCP integration",
    "priority": "high",
    "created_at": "2026-02-12T10:30:00.000Z",
    "status": "active"
  },
  "message": "Item \"Test Task\" created successfully"
}
```

**✅ Test 4 passed if item is created with correct data.**

---

### Test 5: Tool Validation (Missing Required Parameter)

**Ask your AI agent:**

```
Try to create an item without specifying priority (it's required).
```

**Agent should:**
- Recognize that `priority` is required (from schema)
- Either ask you for the value, or report that it cannot proceed without it

**The MCP schema prevents invalid calls, so agent should handle this gracefully.**

**✅ Test 5 passed if agent correctly handles the missing required parameter.**

---

## Part 5: Adapt to Your Real Application

### What We'll Do

Now that you have a working MCP server boilerplate, adapt it to your actual application from Module 120.

---

### Step 1: Identify Your Application's Operations

Think about what operations your application provides:

**Example for a TODO app:**
- Get all todos
- Get todo by ID
- Create new todo
- Update todo (mark complete, change text)
- Delete todo

**Example for a blog app:**
- List posts
- Get post by ID
- Create post
- Update post
- Delete post
- List comments for post

**Example for a contact form app:**
- List submitted contacts
- Get contact by ID
- Delete contact
- Export contacts to CSV

---

### Step 2: Define Tools for Your Application

**Ask your AI agent:**

```
My application is [describe your app from Module 120].

Based on the example MCP server in tools/src/example-mcp-server.ts, create a new MCP server file tools/src/my-app-mcp-server.ts with tools for:

[List 3-5 operations your app should support]

Follow the same pattern as example-mcp-server.ts:
- Define tools array with proper schemas
- Implement handler functions
- Use the same MCP server setup code

For now, use mock data like in the example. We'll connect to real API later.
```

---

### Step 3: Build and Test Your Application MCP Server

```bash
cd tools
npm run build
```

Update IDE MCP configuration to use your new server:

```json
{
  "mcpServers": {
    "my-app": {
      "command": "node",
      "args": ["c:/workspace/hello-genai/work/120-task/tools/dist/my-app-mcp-server.js"]
    }
  }
}
```

Restart IDE and test your tools with AI agent.

---

### Step 4: Connect to Real Backend API

Once tools work with mock data, connect to your actual backend:

**Ask your AI agent:**

```
Update my-app-mcp-server.ts to call my real backend API instead of mock data.

My backend runs at: http://localhost:3000
API endpoints:
- GET /api/todos - list all todos
- GET /api/todos/:id - get todo by ID
- POST /api/todos - create todo
- PUT /api/todos/:id - update todo
- DELETE /api/todos/:id - delete todo

Use fetch() to make HTTP requests to these endpoints.
Handle errors properly.
```

**Agent will:**
- Replace mock data with real HTTP calls
- Add error handling
- Preserve the same MCP tool interface

Rebuild, restart IDE, and test again—now with real data!

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

✅ Understand why MCP integration makes applications AI-controllable  
✅ Created boilerplate MCP server with 3 example tools  
✅ Successfully built TypeScript MCP server  
✅ Configured IDE to connect to MCP server  
✅ AI agent can discover and list MCP tools  
✅ Tested tool with no parameters (get_status)  
✅ Tested tool with parameters (get_user)  
✅ Tested error handling (user not found)  
✅ Tested tool with multiple parameters (create_item)  
✅ Adapted MCP server for your actual application  
✅ Connected MCP server to real backend API  
✅ Understanding of MCP integration patterns  

---

## Understanding Check

Answer these questions to verify comprehension:

1. **What's the difference between REST API and MCP tools for an application?**
   
   Expected answer: REST API is for human-readable HTTP endpoints with documentation that humans read and manually call. MCP tools are self-describing with schemas that AI agents can automatically discover and call. MCP provides type safety, validation, and discovery built-in, while REST requires detailed documentation. MCP is optimized for AI consumption, REST for human consumption.

2. **Why use stdio transport for MCP server in this example?**
   
   Expected answer: Stdio (standard input/output) transport means MCP server communicates through stdin/stdout pipes. This is simple, doesn't require network configuration, and works well for local development. The IDE spawns the MCP server process and communicates directly through pipes. For production or remote access, HTTP transport would be more appropriate.

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
1. **Verify MCP config file path is correct:**
   - Windows: Use forward slashes: `c:/workspace/...`
   - macOS/Linux: Use `~/workspace/...`
2. **Check file exists:**
   ```bash
   ls tools/dist/example-mcp-server.js
   ```
3. **Test MCP server manually:**
   ```bash
   node tools/dist/example-mcp-server.js
   ```
   Should show: "Example MCP server running on stdio"
4. **Check for TypeScript compilation errors:**
   ```bash
   cd tools
   npm run build
   ```
5. **Restart IDE completely** (not just reload window)

---

### Problem: "Module not found" error when running MCP server

**Symptoms:** Error mentions `@modelcontextprotocol/sdk` not found

**Solutions:**
1. **Install dependencies in tools directory:**
   ```bash
   cd tools
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
   case 'app_get_status':  // Must match tool name exactly
   ```
3. **Test tool logic independently:**
   ```typescript
   // Add debugging
   console.error(`[MCP] Calling tool: ${name} with args:`, args);
   ```
4. **Validate parameter types match schema:**
   ```typescript
   // If schema says userId is string, don't pass number
   ```

---

### Problem: MCP server can't connect to backend API

**Symptoms:** Tools work with mock data but fail when calling real API

**Solutions:**
1. **Verify backend is running:**
   ```bash
   curl http://localhost:3000/api/status
   ```
2. **Check CORS if making browser requests:**
   - Backend needs CORS headers for cross-origin requests
   - Or run MCP server on same domain
3. **Add request logging:**
   ```typescript
   console.error(`[MCP] Calling API: ${url}`);
   const response = await fetch(url);
   console.error(`[MCP] Response status: ${response.status}`);
   ```
4. **Handle network errors:**
   ```typescript
   try {
     const response = await fetch(url);
     if (!response.ok) {
       throw new Error(`API error: ${response.status}`);
     }
   } catch (error) {
     console.error('[MCP] Network error:', error);
     throw error;
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
