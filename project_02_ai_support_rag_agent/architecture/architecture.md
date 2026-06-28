# Support RAG Architecture

## Mock Mode

Support ticket CSV -> category classification -> Markdown KB retrieval -> confidence score -> drafted reply -> approval/escalation report.

## Real Integration Mode

Gmail labeled ticket -> normalized ticket shape -> PostgreSQL ticket storage -> approved KB retrieval -> OpenRouter classification and reply draft -> JSON validation -> approval or escalation -> analytics report -> global error handler.

## Production Mapping

| Capability | Portfolio Artifact | Production Tool |
| --- | --- | --- |
| Ticket intake | `support_tickets.csv` | Gmail label trigger or helpdesk webhook |
| Knowledge source | `knowledge_base.md` | `knowledge_base_articles` table or vector store |
| AI classification | deterministic classifier | OpenRouter structured JSON |
| Approval queue | output report | Gmail `sendAndWait` plus `approval_tasks` |
| Escalation | escalation markdown | `workflow_errors`, Slack/Jira/helpdesk escalation |
| Analytics | support analytics report | PostgreSQL query and manager email |

## Reliability Notes

- Do not auto-send low-confidence replies.
- Escalate refunds, billing disputes, complaints, SSO/security issues, and high-value account risk.
- Keep retrieved content separate from system instructions.
- Store approval decisions for audit and prompt improvement.

