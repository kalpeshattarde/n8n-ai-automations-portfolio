# DataOps Power BI Setup

This project documents three realistic Power BI options:

1. Direct PostgreSQL connection to the `power_bi_weekly_kpis` view.
2. CSV import from `output_samples/cleaned_sales_orders.csv` or generated KPI files.
3. REST API refresh of an existing dataset using tenant-specific credentials.

Required private values for REST refresh:

- `POWER_BI_TENANT_ID`
- `POWER_BI_CLIENT_ID`
- `POWER_BI_CLIENT_SECRET`
- `POWER_BI_WORKSPACE_ID`
- `POWER_BI_DATASET_ID`

The public repo does not include a live Power BI workspace.

