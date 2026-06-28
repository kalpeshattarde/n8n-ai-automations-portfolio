# Project 01: AI RevOps Automation System

Lead intake, consent validation, OpenRouter scoring, PostgreSQL CRM storage, Gmail approval, Calendar scheduling, and daily manager reporting.

## Problem Statement

Inbound leads often arrive through forms and spreadsheets before a sales owner can review them. The risk is not only slow response time; it is also weak consent handling, missing contact fields, unclear buying intent, and no audit trail for why a lead was prioritized.

## Business Value

The workflow separates clean leads from review-only records, scores qualified leads, drafts a follow-up for human approval, creates a discovery-call hold for hot leads, and stores the lead decision in a CRM-style PostgreSQL table. Mock Mode proves the logic locally. Real Integration Mode shows how it maps to Google Workspace, OpenRouter, PostgreSQL, Gmail, and Calendar.

## Modes

| Mode | What Runs | Purpose |
| --- | --- | --- |
| Mock Mode | Python scripts over `sample_data/leads.csv` | Proves scoring, consent handling, logs, email draft text, and manager report without APIs. |
| Real Integration Mode | `workflows/n8n_project_workflow.json` | Shows the production-aware integration structure using private credentials in n8n. |

## Tech Stack

- Python 3 standard library for local simulation.
- n8n for production orchestration.
- Google Forms and Sheets for lead intake.
- OpenRouter HTTP API for structured lead scoring.
- PostgreSQL for CRM records, lead events, approval tasks, and errors.
- Gmail `sendAndWait` for human approval.
- Google Calendar for tentative discovery holds.

## Workflow Explanation

1. Google Form response lands in Google Sheets.
2. n8n validates consent and required lead fields.
3. Invalid records are logged for owner review and not contacted.
4. Valid records are scored through OpenRouter with strict JSON output.
5. A Code node validates the LLM response before database writes.
6. PostgreSQL stores the scored CRM lead.
7. Hot leads trigger Gmail human approval and a tentative Calendar hold.
8. A scheduled report queries PostgreSQL and emails the manager.
9. Unhandled failures route to the global error handler.

## Local Setup

```powershell
python project_01_ai_revops_automation/scripts/simulate_lead_scoring.py
python project_01_ai_revops_automation/scripts/generate_daily_sales_report.py
```

## Real Integration Setup

1. Configure `.env` values from `.env.example`.
2. Set up [OpenRouter](./integrations/openrouter_setup.md).
3. Set up [Google Workspace](./integrations/google_workspace_setup.md).
4. Start/apply [PostgreSQL](./database/README.md).
5. Configure [n8n credentials](./integrations/n8n_credentials.md).
6. Import the global error handler, then this workflow.

## Sample Output

- `output_samples/lead_scoring_results.csv`
- `output_samples/processing_log.csv`
- `output_samples/ai_lead_summary_sample.md`
- `output_samples/daily_owner_report_sample.md`

## Error Handling

- Missing consent: logged and blocked from outreach.
- Missing contact data: routed to owner review.
- Invalid OpenRouter JSON: downgraded to manual review.
- PostgreSQL/Gmail/Calendar failures: handled by node-level error output and global error workflow.

## Resume Bullets

- Designed a dual-mode RevOps automation that validates Google Form leads, uses OpenRouter structured scoring, stores CRM decisions in PostgreSQL, and routes hot-lead follow-ups through Gmail approval and Calendar scheduling.
- Built a local Python simulation that proves consent handling, lead prioritization, follow-up drafting, validation logs, and manager reporting without external APIs.
