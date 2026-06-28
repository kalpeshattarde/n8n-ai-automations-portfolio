CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS sales_orders_clean (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  order_id TEXT UNIQUE NOT NULL,
  order_date DATE,
  customer_name TEXT NOT NULL,
  country TEXT,
  product TEXT,
  quantity INTEGER,
  unit_price NUMERIC(14, 2),
  currency TEXT NOT NULL DEFAULT 'USD',
  amount NUMERIC(14, 2),
  payment_status TEXT,
  invoice_due_date DATE,
  order_status TEXT,
  ship_date DATE,
  delivery_date DATE,
  owner TEXT,
  is_overdue BOOLEAN NOT NULL DEFAULT FALSE,
  is_delayed BOOLEAN NOT NULL DEFAULT FALSE,
  is_valid_revenue BOOLEAN NOT NULL DEFAULT TRUE,
  data_quality_issues TEXT[],
  loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dataops_orders_date ON sales_orders_clean(order_date);
CREATE INDEX IF NOT EXISTS idx_dataops_orders_customer ON sales_orders_clean(customer_name);
CREATE INDEX IF NOT EXISTS idx_dataops_orders_payment ON sales_orders_clean(payment_status);

CREATE TABLE IF NOT EXISTS kpi_reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  report_date DATE NOT NULL,
  report_type TEXT NOT NULL,
  total_revenue NUMERIC(14, 2),
  pending_payments NUMERIC(14, 2),
  overdue_invoice_amount NUMERIC(14, 2),
  overdue_invoice_count INTEGER,
  average_order_value NUMERIC(14, 2),
  insight_summary TEXT,
  model_name TEXT,
  prompt_version TEXT,
  report_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dataops_reports_date_type ON kpi_reports(report_date, report_type);

CREATE OR REPLACE VIEW power_bi_weekly_kpis AS
SELECT
  report_date,
  report_type,
  total_revenue,
  pending_payments,
  overdue_invoice_amount,
  overdue_invoice_count,
  average_order_value,
  insight_summary,
  created_at
FROM kpi_reports;

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

CREATE INDEX IF NOT EXISTS idx_dataops_workflow_errors_status ON workflow_errors(remediation_status);

