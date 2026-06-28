# DataOps Architecture

## Mock Mode

Raw sales CSV -> cleaning -> data quality log -> KPI JSON -> Markdown insight report -> HTML dashboard.

## Real Integration Mode

Scheduled n8n trigger -> PostgreSQL cleaned-order query -> data quality validation -> KPI calculation -> OpenRouter executive insight generation -> KPI report storage -> Gmail delivery -> Power BI connection to reporting tables -> global error handler.

## Production Mapping

| Capability | Portfolio Artifact | Production Tool |
| --- | --- | --- |
| Raw input | `sales_orders.csv` | scheduled export, Sheets, API, or database table |
| Cleaning | `clean_data.py` | n8n Code node or warehouse transform |
| KPI storage | `kpi_summary.json` | `kpi_reports` table |
| BI reporting | HTML dashboard | Power BI connected to PostgreSQL views |
| Data quality | `data_quality_log.csv` | `workflow_errors` and quality monitoring table |
| Delivery | Markdown output | Gmail report or BI refresh notification |

## Reliability Notes

- Separate raw and cleaned records.
- Exclude invalid revenue rows from KPI totals.
- Log data quality warnings before sending reports.
- Do not let the LLM invent metrics; it should summarize calculated numbers only.
- Use report date and report type as idempotency keys.

