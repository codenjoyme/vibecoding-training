# MCP Server Boilerplate

This directory contains reference boilerplate code for creating custom MCP servers.

## Files

- **example-mcp-server.ts** - Complete MCP server implementation with 3 example tools
- **package.json** - Dependencies and build scripts
- **tsconfig.json** - TypeScript configuration

## Usage

Copy these files to your project:

```bash
# From your project directory
cp modules/140-advanced-mcp-integration-in-poc/tools/* ./tools/

# Or ask AI agent:
# "Copy the example MCP server from Module 140 to my project's tools/ directory"
```

Then install dependencies and build:

```bash
cd tools
npm install
npm run build
```

The compiled MCP server will be in `tools/dist/example-mcp-server.js`.

## Tool Examples

The boilerplate includes 3 types of tools:

1. **app_get_status** - Tool with no parameters, returns data
2. **app_get_user** - Tool with parameters, returns data
3. **app_create_item** - Tool with multiple parameters, returns success/failure

These cover all common MCP tool patterns.

## Adapting to Your Application

1. Change tool names to match your domain (e.g., `todo_list`, `blog_get_post`)
2. Update tool schemas with your actual parameters
3. Replace mock data with real API calls to your backend
4. Add error handling for your specific use cases
5. Update server name and version in `Server()` constructor

## Testing

After building, test the MCP server:

```bash
# Run directly
node dist/example-mcp-server.js

# Should output: "Example MCP server running on stdio"
```

Then configure in your IDE MCP settings and test with AI agent.

## Learn More

See [Module 140 Walkthrough](../walkthrough.md) for detailed instructions.
