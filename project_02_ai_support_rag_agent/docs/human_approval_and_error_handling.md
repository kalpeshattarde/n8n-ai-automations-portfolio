# Support Human Approval And Error Handling

Human approval is required for customer-facing replies. Sensitive or low-confidence tickets are escalated instead of drafted for send.

Escalate:

- refunds
- billing disputes
- complaints
- SSO/security issues
- legal concerns
- low confidence or missing KB match

Unhandled workflow failures route to `workflows/global_error_handler.json`.

