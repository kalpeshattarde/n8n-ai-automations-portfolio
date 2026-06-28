# Project 02: AI Support RAG Agent

Support ticket ingestion, RAG-ready knowledge retrieval, OpenRouter classification/drafting, human approval, escalation, and daily analytics.

## Problem Statement

Support automation is useful only when it can distinguish routine questions from risky cases. Refunds, billing disputes, complaints, account access issues, and low-confidence answers need human review rather than direct auto-send.

## Business Value

The project shows a safe support automation pattern: draft helpful replies for routine tickets, escalate sensitive tickets, store decisions in PostgreSQL, and preserve human approval for customer-facing responses.

## Modes

| Mode | What Runs | Purpose |
| --- | --- | --- |
| Mock Mode | Python scripts over `support_tickets.csv` and `knowledge_base.md` | Proves classification, retrieval, confidence scoring, approval routing, and escalation reports. |
| Real Integration Mode | `workflows/n8n_project_workflow.json` | Shows Gmail-triggered ticket intake, PostgreSQL ticket storage, KB retrieval, OpenRouter drafting, and Gmail approval. |

## Tech Stack

- Python 3 standard library for local simulation.
- n8n for orchestration.
- Gmail trigger for ticket intake.
- PostgreSQL for tickets, KB articles, responses, approvals, and errors.
- OpenRouter for classification and reply drafting.
- Gmail `sendAndWait` for human approval.

## Workflow Explanation

1. Gmail trigger watches a support intake label.
2. n8n normalizes the email into a ticket shape.
3. PostgreSQL stores or updates the support ticket.
4. Approved KB articles are retrieved from PostgreSQL.
5. OpenRouter classifies the ticket, drafts a reply, and returns strict JSON.
6. A Code node validates confidence, risk flags, and route.
7. High-confidence safe replies go to human approval.
8. Risky or low-confidence tickets are logged as escalations.
9. Daily analytics summarize ticket volume, route mix, and confidence.

## Local Setup

```powershell
python project_02_ai_support_rag_agent/scripts/simple_rag_retriever.py
python project_02_ai_support_rag_agent/scripts/simulate_ticket_triage.py
```

## Real Integration Setup

1. Configure `.env` values from `.env.example`.
2. Set up Gmail label intake in [Google Workspace](./integrations/google_workspace_setup.md).
3. Load KB articles into [PostgreSQL](./database/README.md).
4. Configure [OpenRouter](./integrations/openrouter_setup.md).
5. Configure [n8n credentials](./integrations/n8n_credentials.md).
6. Import the global error handler, then this workflow.

## Sample Output

- `output_samples/retrieval_demo.md`
- `output_samples/ticket_triage_results.csv`
- `output_samples/drafted_reply_sample.md`
- `output_samples/escalation_report_sample.md`
- `output_samples/support_analytics_report.md`

## Error Handling

- Missing KB match: escalated.
- Low confidence: escalated.
- Refunds, billing disputes, complaints, SSO/security issues: escalated.
- Invalid OpenRouter JSON: escalated.
- Workflow failures: logged through the global error handler.

## Resume Bullets

- Designed a dual-mode support RAG workflow with Gmail ticket intake, PostgreSQL ticket/KB storage, OpenRouter classification and drafting, confidence-based approval routing, and escalation controls.
- Built a local simulation that proves retrieval, risk routing, drafted replies, escalation reports, and support analytics without external APIs.
