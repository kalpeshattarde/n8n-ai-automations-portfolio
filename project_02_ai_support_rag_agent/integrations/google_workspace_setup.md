# Support Gmail Setup

Purpose:

- Gmail label receives support tickets.
- Gmail `sendAndWait` handles reviewer approval.

Setup:

1. Create a Gmail label such as `AI-Support-Intake`.
2. Set `GOOGLE_SUPPORT_LABEL`.
3. Create a Gmail OAuth credential in n8n.
4. Test with safe SaaS-style support emails.

Keep approval emails internal. Do not auto-send customer replies until approval metrics are reviewed.

