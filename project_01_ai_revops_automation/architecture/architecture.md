# RevOps Architecture

## Mock Mode

CSV lead intake -> validation -> deterministic scoring -> follow-up draft -> processing log -> manager report.

## Real Integration Mode

Google Form -> Google Sheets Trigger -> consent/required-field validation -> OpenRouter structured scoring -> JSON validation -> PostgreSQL CRM storage -> Gmail human approval -> Calendar discovery hold -> daily manager report -> global error handler.

## Production Mapping

| Capability | Portfolio Artifact | Production Tool |
| --- | --- | --- |
| Lead intake | `sample_data/leads.csv` | Google Forms and Google Sheets |
| AI scoring | local scoring function | OpenRouter HTTP Request node |
| CRM storage | `lead_scoring_results.csv` | `crm_leads` and `lead_events` tables |
| Human approval | generated draft | Gmail `sendAndWait` plus `approval_tasks` |
| Scheduling | recommended action text | Google Calendar event hold |
| Error logging | `processing_log.csv` | `workflow_errors` and global error workflow |

## Reliability Notes

- Do not contact leads without consent.
- Validate OpenRouter JSON before writing to CRM.
- Keep follow-up generation separate from sending.
- Use source row ID or email as an idempotency key.
- Log scoring prompt version and model name for auditability.

