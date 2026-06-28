# RevOps MCP-Ready Architecture

This project is MCP-ready, not a deployed MCP server. The safe tool boundary would expose only approved CRM and logging actions.

Tools:

- `create_lead`
- `update_lead_status`
- `create_approval_task`
- `log_workflow_error`

n8n can call these tools instead of giving an LLM direct database access. The LLM proposes structured actions; tools validate and execute them.

