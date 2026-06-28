CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS crm_leads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  external_source TEXT NOT NULL DEFAULT 'google_sheets',
  source_record_id TEXT,
  full_name TEXT NOT NULL,
  work_email TEXT,
  company_name TEXT NOT NULL,
  website TEXT,
  industry TEXT,
  company_size TEXT,
  monthly_revenue NUMERIC(14, 2),
  country TEXT,
  pain_points TEXT,
  hours_lost_per_week NUMERIC(8, 2),
  tools_used TEXT,
  budget NUMERIC(14, 2),
  timeline TEXT,
  decision_authority TEXT,
  desired_outcome TEXT,
  consent BOOLEAN NOT NULL DEFAULT FALSE,
  lead_score INTEGER,
  lead_tier TEXT CHECK (lead_tier IN ('Hot', 'Warm', 'Cold', 'Unqualified')),
  ai_summary TEXT,
  recommended_next_action TEXT,
  status TEXT NOT NULL DEFAULT 'new',
  prompt_version TEXT,
  model_name TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_crm_leads_email ON crm_leads(work_email);
CREATE INDEX IF NOT EXISTS idx_crm_leads_status ON crm_leads(status);
CREATE INDEX IF NOT EXISTS idx_crm_leads_tier ON crm_leads(lead_tier);

CREATE TABLE IF NOT EXISTS lead_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lead_id UUID REFERENCES crm_leads(id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  event_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_lead_events_lead_id ON lead_events(lead_id);

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

CREATE INDEX IF NOT EXISTS idx_revops_approval_status ON approval_tasks(approval_status);

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

CREATE INDEX IF NOT EXISTS idx_revops_workflow_errors_status ON workflow_errors(remediation_status);

