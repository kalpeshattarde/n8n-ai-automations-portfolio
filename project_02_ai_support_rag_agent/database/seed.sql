INSERT INTO knowledge_base_articles (article_key, title, body, tags)
VALUES
  ('account_invites', 'Account Invites', 'Admins can resend invites from Settings > Team > Pending Invites. Confirm email spelling and spam filtering.', ARRAY['onboarding', 'team']),
  ('api_rate_limit', 'API Rate Limit', 'HTTP 429 means the workspace is exceeding request limits. Use exponential backoff and reduce polling frequency. Escalate production incidents.', ARRAY['technical', 'api']),
  ('billing_contact', 'Billing Contact', 'Billing admins can update billing email from Settings > Billing > Billing Contact. Non-admins need an account owner.', ARRAY['billing'])
ON CONFLICT (article_key) DO NOTHING;

