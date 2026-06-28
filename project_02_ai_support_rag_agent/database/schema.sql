CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS support_tickets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  external_ticket_id TEXT UNIQUE,
  customer_name TEXT,
  customer_email TEXT,
  account_plan TEXT,
  channel TEXT NOT NULL DEFAULT 'gmail',
  priority TEXT,
  subject TEXT NOT NULL,
  message TEXT NOT NULL,
  category TEXT,
  confidence NUMERIC(5, 2),
  route TEXT CHECK (route IN ('approval', 'escalation', 'closed')),
  risk_flags TEXT[],
  status TEXT NOT NULL DEFAULT 'new',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_support_tickets_external ON support_tickets(external_ticket_id);
CREATE INDEX IF NOT EXISTS idx_support_tickets_route ON support_tickets(route);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);

CREATE TABLE IF NOT EXISTS knowledge_base_articles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  article_key TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  tags TEXT[] NOT NULL DEFAULT '{}',
  active BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_support_kb_active ON knowledge_base_articles(active);

CREATE TABLE IF NOT EXISTS support_responses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  ticket_id UUID REFERENCES support_tickets(id) ON DELETE CASCADE,
  kb_article_id UUID REFERENCES knowledge_base_articles(id),
  drafted_reply TEXT NOT NULL,
  model_name TEXT,
  prompt_version TEXT,
  approval_status TEXT NOT NULL DEFAULT 'pending',
  approved_by TEXT,
  approved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_support_responses_ticket ON support_responses(ticket_id);
CREATE INDEX IF NOT EXISTS idx_support_responses_approval ON support_responses(approval_status);

CREATE TABLE IF NOT EXISTS approval_tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_type TEXT NOT NULL,
  source_id UUID,
  approver_email TEXT NOT NULL,
  approval_status TEXT NOT NULL DEFAULT 'pending',
  approval_channel TEXT NOT NULL DEFAULT 'gmail_send_and_wait',
  approval_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  decision_notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  decided_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS workflow_errors (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  n8n_execution_id TEXT,
  workflow_name TEXT NOT NULL,
  node_name TEXT,
  severity TEXT NOT NULL DEFAULT 'error',
  error_message TEXT NOT NULL,
  payload_reference TEXT,
  remediation_status TEXT NOT NULL DEFAULT 'open',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_support_workflow_errors_status ON workflow_errors(remediation_status);

