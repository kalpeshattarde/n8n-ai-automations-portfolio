# Setup Guide

## Mock Mode

```powershell
python project_03_ai_dataops_reporting_pipeline/scripts/clean_data.py
python project_03_ai_dataops_reporting_pipeline/scripts/generate_kpi_report.py
python project_03_ai_dataops_reporting_pipeline/scripts/generate_html_dashboard.py
```

Open `project_03_ai_dataops_reporting_pipeline/output_samples/dashboard_preview.html` in a browser after running the dashboard script.

## Real Integration Mode

1. Start PostgreSQL and apply `project_03_ai_dataops_reporting_pipeline/database/schema.sql`.
2. Load cleaned sales-order records into `sales_orders_clean`.
3. Configure OpenRouter using `project_03_ai_dataops_reporting_pipeline/integrations/openrouter_setup.md`.
4. Configure Gmail reporting recipient.
5. Choose a Power BI integration strategy from `project_03_ai_dataops_reporting_pipeline/integrations/power_bi_setup.md`.
6. Import `project_03_ai_dataops_reporting_pipeline/workflows/global_error_handler.json`.
7. Import `project_03_ai_dataops_reporting_pipeline/workflows/n8n_project_workflow.json`.
8. Attach the global error handler in workflow settings.
9. Run once manually before enabling the schedule.

## Required Private Credentials

- PostgreSQL connection.
- OpenRouter API key.
- Gmail OAuth credential.
- Optional Power BI tenant/app/workspace/dataset credentials.

## Production Notes

Power BI should connect to database views or refresh an existing dataset. The public repo intentionally does not include tenant-specific Power BI assets.
