# RevOps OpenRouter Setup

OpenRouter is used only in Real Integration Mode to score leads and return strict JSON.

Required environment values:

- `OPENROUTER_API_KEY`
- `OPENROUTER_BASE_URL`
- `OPENROUTER_MODEL`
- `OPENROUTER_SITE_URL`
- `OPENROUTER_APP_NAME`

n8n should use an HTTP Request node named `OpenRouter - Score Lead With Structured JSON`. The response must be validated by `Code - Validate OpenRouter JSON Output` before CRM writes.

Expected JSON fields:

```json
{
  "score": 82,
  "tier": "Hot",
  "reasons": ["clear pain", "budget confirmed"],
  "risk_flags": [],
  "recommended_next_action": "book discovery call",
  "follow_up_email_subject": "Automation discovery next step",
  "follow_up_email_body": "Draft body for approval"
}
```

Do not send unnecessary PII to the LLM. Keep Gmail in approval mode.

