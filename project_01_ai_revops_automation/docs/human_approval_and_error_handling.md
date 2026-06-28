# RevOps Human Approval And Error Handling

Human approval is required before any sales follow-up is sent. The workflow uses Gmail `sendAndWait` and logs approval context in `approval_tasks`.

Error handling:

- Missing consent or required fields are logged and blocked from outreach.
- Invalid OpenRouter JSON becomes manual review.
- PostgreSQL, Gmail, and Calendar failures route to `workflows/global_error_handler.json`.
- Use source row ID or work email as the idempotency key.

