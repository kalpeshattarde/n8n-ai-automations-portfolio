# DataOps MCP-Ready Architecture

This project is MCP-ready, not a deployed MCP server. Tools would expose reporting operations without direct LLM database access.

Tools:

- `generate_kpi_summary`
- `store_kpi_report`
- `log_workflow_error`

The LLM summarizes calculated KPIs only. It should not query arbitrary tables or invent metrics.

