# DataOps PostgreSQL Setup

The DataOps workflow reads `sales_orders_clean`, stores reports in `kpi_reports`, and exposes `power_bi_weekly_kpis` for reporting.

Local connection:

```text
postgresql://akcelerate_app:akcelerate_dataops_password@localhost:5435/akcelerate_dataops
```

Run:

```powershell
cd project_03_ai_dataops_reporting_pipeline/database
docker compose up -d
```

