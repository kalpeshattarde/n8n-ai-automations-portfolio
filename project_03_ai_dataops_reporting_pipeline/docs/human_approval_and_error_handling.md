# DataOps Human Approval And Error Handling

DataOps does not send customer-facing messages, but stakeholder reports should be reviewed when data quality warnings exceed threshold.

Error handling:

- Invalid rows are logged and excluded when needed.
- OpenRouter insight JSON is validated before report storage.
- Workflow failures route to `workflows/global_error_handler.json`.
- Use report date and report type as idempotency keys.

