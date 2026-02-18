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
 * Copy this file to your project's tools/ directory and adapt to your needs.
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
