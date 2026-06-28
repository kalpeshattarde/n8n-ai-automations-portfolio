# Support MCP-Ready Architecture

This project is MCP-ready, not a deployed MCP server. A tool layer would keep support actions narrow and auditable.

Tools:

- `create_support_ticket`
- `search_knowledge_base`
- `create_approval_task`
- `log_workflow_error`

The LLM can request a route or draft, but tools enforce allowed actions and approval requirements.

