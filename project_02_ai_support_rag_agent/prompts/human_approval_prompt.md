# Human Approval Prompt

Review the drafted support response before it is sent.

Approve only if:

- the answer cites a relevant knowledge-base article
- confidence is high
- no refund, billing dispute, complaint, SSO incident, or security issue is present
- the reply does not make commitments outside the knowledge base

If rejected, provide one of these decisions:

- escalate_to_billing
- escalate_to_technical_support
- escalate_to_customer_success
- needs_more_information

