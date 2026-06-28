# Setup Guide

## Mock Mode

```powershell
python project_01_ai_revops_automation/scripts/simulate_lead_scoring.py
python project_01_ai_revops_automation/scripts/generate_daily_sales_report.py
```

Outputs are written to `project_01_ai_revops_automation/output_samples/`.

## Real Integration Mode

1. Copy `.env.example` to a private `.env` outside Git tracking and fill only local/private values.
2. Configure OpenRouter using `project_01_ai_revops_automation/integrations/openrouter_setup.md`.
3. Configure Google Forms and Sheets using `project_01_ai_revops_automation/integrations/google_workspace_setup.md`.
4. Start PostgreSQL and apply `project_01_ai_revops_automation/database/schema.sql`.
5. Create n8n credentials: Google Sheets, Gmail, Google Calendar, PostgreSQL, OpenRouter HTTP auth.
6. Import `project_01_ai_revops_automation/workflows/global_error_handler.json`.
7. Import `project_01_ai_revops_automation/workflows/n8n_project_workflow.json`.
8. Attach the global error handler in workflow settings.
9. Test with one sandbox Google Form response before activation.

## Required Private Credentials

- OpenRouter API key.
- Google OAuth credentials.
- PostgreSQL connection.
- Gmail sender/reviewer account.
- Google Calendar ID.

## Production Notes

Keep Gmail in approval mode until follow-up quality and consent handling are verified. Do not auto-send to leads from an unreviewed LLM draft.
