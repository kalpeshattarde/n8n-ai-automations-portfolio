INSERT INTO sales_orders_clean (
  order_id,
  order_date,
  customer_name,
  product,
  quantity,
  unit_price,
  amount,
  payment_status,
  invoice_due_date,
  order_status,
  owner
)
VALUES (
  'SO-1001',
  '2026-05-02',
  'BrightPath SaaS',
  'Automation Audit Package',
  1,
  1200,
  1200,
  'Paid',
  '2026-05-16',
  'Delivered',
  'Asha'
)
ON CONFLICT (order_id) DO NOTHING;

