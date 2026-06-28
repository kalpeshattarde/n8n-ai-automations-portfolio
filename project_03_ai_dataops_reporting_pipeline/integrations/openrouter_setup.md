# DataOps OpenRouter Setup

OpenRouter turns calculated KPIs into executive-readable insights. It must not invent metrics; it only summarizes values calculated by the workflow.

Expected JSON:

```json
{
  "executive_summary": "Short summary from actual KPIs",
  "risk_notes": ["overdue invoices increased"],
  "recommended_actions": ["review delayed orders"]
}
```

Validate JSON before inserting into `kpi_reports`.

