# RevOps Google Workspace Setup

Purpose:

- Google Forms collects inbound leads.
- Google Sheets receives form responses.
- Gmail sends approval requests.
- Google Calendar creates tentative discovery holds for hot leads.

Required setup:

1. Create a Google Form with fields matching `sample_data/leads.csv`.
2. Link the form to a Google Sheet tab named `Leads`.
3. Configure OAuth credentials for Google Sheets, Gmail, and Calendar in n8n.
4. Set `GOOGLE_FORMS_RESPONSE_SHEET_ID`, `GOOGLE_LEADS_SHEET_NAME`, and `GOOGLE_CALENDAR_ID`.

Use least-privilege scopes. Do not enable direct customer-facing sends until approval quality is verified.

