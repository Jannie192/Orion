# ORION MCP capability discovery

ORION discovers MCP capabilities through the standard `tools/list` operation. The discovery service should read the connected MCP server's advertised tools, including names, descriptions, input schemas, and output schemas, then upsert them into `tool_actions`. Pagination must be followed until `nextCursor` is absent, with a finite page cap.

## Security requirements

- Require an authenticated ORION user.
- Resolve the MCP endpoint only from a registered connected `tool_connections` record.
- Require HTTPS and reject localhost/private/link-local destinations.
- Never expose connection secrets to the browser.
- Preserve the advertised tool name as `path_template` for later `tools/call`.
- Default discovered actions to medium risk and approval required.
- Store the advertised input/output schemas so the reasoning layer can plan against real capabilities.

## Protocol

Use JSON-RPC 2.0 `tools/list`. MCP's current 2026-07-28 line supports paginated tool discovery; the TypeScript SDK's `listTools()` aggregates pages and caps the walk at 64 pages by default.
