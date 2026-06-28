# Portfolio Overview

This portfolio is built to answer one hiring question: can Kalpesh design realistic AI automation systems that are runnable locally and credible as production integrations?

## Positioning

The repository now uses a dual-mode structure:

- Mock Mode proves the logic locally with Python, CSV, Markdown, JSON, and HTML outputs.
- Real Integration Mode documents and models how the same systems connect to n8n, OpenRouter, Google Workspace, PostgreSQL, Gmail approvals, Calendar scheduling, Power BI, and MCP-style tools.

This is not presented as a live SaaS deployment. It is a production-aware portfolio that shows architecture, workflow boundaries, credential handling, data persistence, safety controls, and business value.

## Project Value Summary

| Project | Business Value | Production Signals |
| --- | --- | --- |
| RevOps Automation | Faster lead prioritization and safer follow-up handling | Consent validation, OpenRouter structured scoring, PostgreSQL CRM storage, Gmail approval, Calendar hold, daily manager report |
| Support RAG Agent | Faster response drafting without unsafe auto-send | Gmail intake, KB retrieval, confidence thresholds, escalation rules, approval queue, analytics |
| DataOps Pipeline | Reproducible reporting from messy sales data | Data quality logging, KPI storage, OpenRouter insight generation, Power BI-ready tables |

## Reference Patterns Used

The design was shaped against the local `n8n-templates-organized` reference library, especially Lead Generation, Customer Support, Data Integration and APIs, and Analytics and Reporting. The final workflows are not copied template dumps; they are recruiter-facing systems built around those production patterns.

## What To Review First

1. Root `README.md` for Mock Mode vs Real Integration Mode.
2. Each project's `workflows/n8n_project_workflow.json` for the n8n workflow map.
3. Each project's `database/schema.sql` for production persistence design.
4. Each project's `mcp/architecture.md` for tool-boundary thinking.
5. Each project's `docs/security_checklist.md` for production safeguards.
6. Each project's `docs/demo_guide.md` for walkthrough structure.

## Why This Is Job-Ready

The repository avoids claiming that public placeholder workflows are live production deployments. It instead proves engineering maturity through realistic data, runnable simulations, importable workflow skeletons, integration setup guides, a unified database schema, MCP-ready tool definitions, security controls, and resume-ready impact language.
