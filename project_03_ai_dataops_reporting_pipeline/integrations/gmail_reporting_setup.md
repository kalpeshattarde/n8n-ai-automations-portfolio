# DataOps Gmail Reporting Setup

Purpose:

- Send weekly KPI summaries to the stakeholder email configured in `.env`.
- Keep report delivery separate from Power BI refresh so reporting still works if BI refresh is delayed.

Required values:

- `GMAIL_SENDER`
- `DATAOPS_STAKEHOLDER_EMAIL`

n8n setup:

1. Create a Gmail OAuth credential named `Gmail - Portfolio`.
2. Use the workflow node `Gmail - Send Weekly KPI Report`.
3. Test with a sandbox recipient before using a stakeholder inbox.

Do not include sensitive raw order payloads in email. Send summary metrics and link to the report/dashboard instead.

