# AKcelerateHQ AI Automation Portfolio

AI automation engineering portfolio for AI Automation Engineer, n8n Automation Engineer, AI Workflow Engineer, RevOps Automation Specialist, and Data Automation Analyst roles.

This repository has two clear modes:

- Mock Mode: local Python simulations with CSV/Markdown/HTML outputs. No APIs, paid tools, or external calls are required.
- Real Integration Mode: n8n-ready architecture using OpenRouter, Google Workspace, PostgreSQL, Gmail approval flows, Calendar scheduling, Power BI reporting options, and a global error handler. Real credentials are intentionally represented as placeholders.

The public repo does not claim to be a deployed production system. It shows production-aware design: realistic workflow boundaries, credential handling, database schemas, approval controls, logging, and recruiter-friendly business context.

## About AKcelerateHQ

AKcelerateHQ is Kalpesh Attarde's AI automation practice focused on turning manual business workflows into reliable operating systems: lead follow-up, customer support triage, reporting, CRM updates, email drafts, and human-in-the-loop review.

## Projects

| Project | Mock Mode Proof | Real Integration Mode Design |
| --- | --- | --- |
| [01. AI RevOps Automation](./project_01_ai_revops_automation/README.md) | Scores lead CSVs, drafts follow-ups, logs validation issues, and produces a manager report. | Google Form to Sheets intake, OpenRouter structured scoring, PostgreSQL CRM storage, Gmail draft approval, Calendar booking, daily reporting. |
| [02. AI Support RAG Agent](./project_02_ai_support_rag_agent/README.md) | Classifies support CSVs, retrieves KB answers, drafts replies, and routes approval vs escalation. | Gmail label trigger, PostgreSQL ticket tables, RAG-ready KB search, OpenRouter classification/drafting, human approval, escalation and analytics. |
| [03. AI DataOps Reporting Pipeline](./project_03_ai_dataops_reporting_pipeline/README.md) | Cleans sales orders, calculates KPIs, writes insight reports, and generates an HTML dashboard. | Scheduled ingestion from PostgreSQL/Sheets/CSV, data quality gates, OpenRouter insight generation, PostgreSQL report storage, Power BI options, Gmail delivery. |

## Skills Demonstrated

- n8n workflow architecture with trigger, processing, branching, approval, reporting, and error paths
- OpenRouter integration design with structured JSON outputs and fallback/error handling
- CSV-based Google Sheets style data handling
- Google Workspace setup planning for Forms, Sheets, Gmail, and Calendar
- PostgreSQL schema design for CRM, support, reporting, approvals, and workflow logs
- Power BI integration strategy without claiming a public repo can refresh a private dataset
- MCP-ready architecture that routes tool actions through safe interfaces instead of direct ad hoc access
- Human-in-the-loop approval and escalation workflows
- Error handling, validation logs, and operational status tracking
- Security checklist covering secrets, OAuth scopes, PII, prompt injection, and rate limiting
- HTML dashboard generation without frontend dependencies

## Run Locally

Python 3 is enough. No paid API, no n8n instance, and no external dependency is required for the simulation layer.

```powershell
python project_01_ai_revops_automation/scripts/simulate_lead_scoring.py
python project_01_ai_revops_automation/scripts/generate_daily_sales_report.py

python project_02_ai_support_rag_agent/scripts/simple_rag_retriever.py
python project_02_ai_support_rag_agent/scripts/simulate_ticket_triage.py

python project_03_ai_dataops_reporting_pipeline/scripts/clean_data.py
python project_03_ai_dataops_reporting_pipeline/scripts/generate_kpi_report.py
python project_03_ai_dataops_reporting_pipeline/scripts/generate_html_dashboard.py
```

Generated outputs are written into each project's `output_samples/` folder.

## Real Integration Mode

Real Integration Mode is documented but not auto-executed from this public repo because it requires private credentials and paid or tenant-specific services.

Each project owns its own integration setup, schema, MCP notes, security checklist, demo guide, and n8n workflows:

- [RevOps setup](./project_01_ai_revops_automation/docs/setup_guide.md)
- [Support RAG setup](./project_02_ai_support_rag_agent/docs/setup_guide.md)
- [DataOps setup](./project_03_ai_dataops_reporting_pipeline/docs/setup_guide.md)

## Recruiter Guide

Start with the root [portfolio overview](./portfolio_overview.md), then open each project README. The strongest signals are the dual-mode design, realistic sample data, local runnable scripts, project-owned n8n workflows, PostgreSQL schema, MCP-ready boundaries, security notes, and resume bullets in [resume_project_bullets.md](./resume_project_bullets.md).

For a 10-minute screen, review:

1. Project 01 output report to understand RevOps impact.
2. Project 02 escalation logic to see responsible AI support routing.
3. Project 03 dashboard preview to see DataOps/business reporting capability.

## Mock vs Real Comparison

| Area | Mock Mode | Real Integration Mode |
| --- | --- | --- |
| LLM | Deterministic local scoring/drafting | OpenRouter HTTP Request nodes with structured JSON prompts |
| Data store | CSV and Markdown outputs | Project-owned PostgreSQL schemas in each `database/` folder |
| Google Workspace | Represented by CSV/email drafts | Forms/Sheets/Gmail/Calendar OAuth setup docs |
| Approval | Output files show routes | Gmail `sendAndWait` approval steps and approval tables |
| Reporting | Markdown/HTML reports | PostgreSQL report tables plus Power BI connection options |
| Errors | CSV validation logs | Global n8n error workflow plus `workflow_errors` table |

## Reference n8n Exports

Earlier credentialed n8n examples were moved to [archive/legacy_n8n_exports/](./archive/legacy_n8n_exports/). They remain available as reference exports, while the main portfolio projects are designed to run locally without external APIs.

## Contact Placeholder

Kalpesh Attarde  
Founder, AKcelerateHQ  
LinkedIn: `PASTE_LINKEDIN_URL_HERE`  
GitHub: `PASTE_GITHUB_PROFILE_URL_HERE`  
Email: `PASTE_PUBLIC_EMAIL_HERE`
