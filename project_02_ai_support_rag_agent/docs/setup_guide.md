# Setup Guide

## Mock Mode

```powershell
python project_02_ai_support_rag_agent/scripts/simple_rag_retriever.py
python project_02_ai_support_rag_agent/scripts/simulate_ticket_triage.py
```

Outputs are written to `project_02_ai_support_rag_agent/output_samples/`.

## Real Integration Mode

1. Configure Gmail label intake for support messages.
2. Load approved support articles into `knowledge_base_articles`.
3. Configure OpenRouter using `project_02_ai_support_rag_agent/integrations/openrouter_setup.md`.
4. Configure PostgreSQL using `project_02_ai_support_rag_agent/database/schema.sql`.
5. Create n8n credentials: Gmail, PostgreSQL, OpenRouter HTTP auth.
6. Import `project_02_ai_support_rag_agent/workflows/global_error_handler.json`.
7. Import `project_02_ai_support_rag_agent/workflows/n8n_project_workflow.json`.
8. Attach the global error handler in workflow settings.
9. Test with safe SaaS-style sandbox tickets.

## Required Private Credentials

- Gmail OAuth credential.
- OpenRouter API key.
- PostgreSQL connection.
- Support reviewer inbox.

## Production Notes

Do not auto-send replies until approval data proves the workflow is safe. Keep refunds, complaints, billing disputes, SSO/security issues, and low-confidence replies in escalation.
