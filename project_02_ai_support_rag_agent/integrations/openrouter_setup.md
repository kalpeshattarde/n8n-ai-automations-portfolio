# Support OpenRouter Setup

OpenRouter classifies tickets, selects a route, and drafts replies as strict JSON. The workflow must validate route, confidence, and risk flags before approval.

Expected JSON:

```json
{
  "category": "Technical",
  "confidence": 0.78,
  "matched_article_title": "API Rate Limit",
  "drafted_reply": "Reply text for reviewer",
  "risk_flags": [],
  "route": "approval"
}
```

Escalate refunds, billing disputes, complaints, SSO/security issues, legal concerns, and low-confidence responses.

