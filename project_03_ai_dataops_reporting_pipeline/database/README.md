# DataOps Database

Local PostgreSQL setup for the DataOps Real Integration Mode.

```powershell
cd project_03_ai_dataops_reporting_pipeline/database
docker compose up -d
```

This starts PostgreSQL on host port `5435` with cleaned orders, KPI reports, a Power BI-friendly view, and workflow error logging.

