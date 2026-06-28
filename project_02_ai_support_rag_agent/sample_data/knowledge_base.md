# Knowledge Base

## Account Invites

If a teammate does not receive an invite, ask the admin to confirm the email address, check spam, and resend the invite from Settings > Team > Pending Invites. If the domain uses strict filtering, ask IT to allow emails from `no-reply@example-saas.com`.

## Report Export

Workspace admins and managers can export activity reports from Analytics > Reports > Export CSV. Starter plans include weekly activity exports. Pro and Business plans also include custom date ranges.

## API Rate Limit

The API returns HTTP 429 when a workspace exceeds the allowed request rate. Retry with exponential backoff, reduce polling frequency, and contact support for higher limits on Business or Enterprise plans. Production incidents should be escalated to technical support.

## Password Reset

Password reset links expire after 30 minutes. Request a new link, open the most recent email, and complete the reset in the same browser session. If multiple reset emails were requested, only the newest link will work.

## Billing Contact

Billing admins can update the billing email from Settings > Billing > Billing Contact. If the user is not a billing admin, ask an account owner to make the change.

## Seat Count And Invoice Adjustments

Invoices are calculated from active paid seats at the time the billing period closes. Billing disputes, refunds, and seat count corrections must be reviewed by the billing team before any customer-facing commitment is made.

## Trial Cancellation And Refunds

Trial cancellation can be completed from Settings > Billing > Cancel Plan. Refund requests require human review. Do not promise a refund automatically.

## SSO Login

SSO access denied errors may be caused by missing identity provider group mapping, an inactive user, or a domain mismatch. Enterprise SSO issues should be escalated to technical support with workspace ID, user email, timestamp, and identity provider.

## Dashboard Data Missing

Dashboard data may be delayed by sync latency or failed integrations. Ask for affected dashboard name, date range, integration source, and screenshot. Repeated failures or high-value accounts should be escalated.

