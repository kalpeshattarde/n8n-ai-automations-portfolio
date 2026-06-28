# Project 03: AI DataOps Reporting Pipeline

Data quality validation, KPI calculation, OpenRouter insight generation, PostgreSQL report storage, Power BI-ready reporting, and stakeholder delivery.

## Problem Statement

Business reporting gets unreliable when raw exports have inconsistent dates, missing prices, stale payment statuses, and delayed delivery records. A production reporting workflow needs validation, traceability, and a clear handoff to BI tools.

## Business Value

This project turns raw sales-order data into reproducible KPIs, logs data quality issues, generates executive-friendly insights, and documents realistic Power BI integration paths without claiming a private BI tenant exists in the public repo.

## Modes

| Mode | What Runs | Purpose |
| --- | --- | --- |
| Mock Mode | Python scripts over `sales_orders.csv` | Proves cleaning, KPI calculation, data quality logging, Markdown report, and HTML dashboard output. |
| Real Integration Mode | `workflows/n8n_project_workflow.json` | Shows scheduled PostgreSQL reporting, OpenRouter insight generation, KPI storage, Gmail delivery, and Power BI-ready tables. |

## Tech Stack

- Python 3 standard library for local simulation.
- n8n for scheduled orchestration.
- PostgreSQL for cleaned orders and KPI reports.
- OpenRouter for executive insight generation.
- Gmail for stakeholder delivery.
- Power BI integration options documented through PostgreSQL, CSV, or REST refresh.

## Workflow Explanation

1. Scheduled n8n workflow reads cleaned sales orders from PostgreSQL.
2. Code node validates data quality and calculates KPIs.
3. Quality warnings are logged in PostgreSQL.
4. OpenRouter generates an executive summary from actual metrics only.
5. A validation node checks insight JSON.
6. KPI report is stored in `kpi_reports`.
7. Gmail sends the weekly stakeholder report.
8. Power BI connects to reporting tables or refreshes a dataset separately.

## Local Setup

```powershell
python project_03_ai_dataops_reporting_pipeline/scripts/clean_data.py
python project_03_ai_dataops_reporting_pipeline/scripts/generate_kpi_report.py
python project_03_ai_dataops_reporting_pipeline/scripts/generate_html_dashboard.py
```

Open `output_samples/dashboard_preview.html` after running the dashboard script.

## Real Integration Setup

1. Configure `.env` values from `.env.example`.
2. Start/apply [PostgreSQL](./database/README.md).
3. Configure [OpenRouter](./integrations/openrouter_setup.md).
4. Configure [Power BI integration strategy](./integrations/power_bi_setup.md).
5. Configure [Gmail reporting](./integrations/gmail_reporting_setup.md).
6. Configure [n8n credentials](./integrations/n8n_credentials.md).
6. Import the global error handler, then this workflow.

## Sample Output

- `output_samples/cleaned_sales_orders.csv`
- `output_samples/data_quality_log.csv`
- `output_samples/kpi_summary.json`
- `output_samples/weekly_ai_insights_report.md`
- `output_samples/dashboard_preview.html`

## Error Handling

- Invalid or missing data is logged and excluded from revenue metrics when needed.
- Data quality warnings are stored for operations review.
- Invalid OpenRouter JSON falls back to manual insight review.
- Workflow failures route to the global error handler.

## Resume Bullets

- Designed a dual-mode DataOps pipeline that validates sales-order data, calculates KPIs, stores report outputs in PostgreSQL, generates OpenRouter executive insights, and documents Power BI integration options.
- Built a local reporting simulation that produces cleaned CSVs, data quality logs, KPI JSON, Markdown insights, and an HTML dashboard without external APIs.
