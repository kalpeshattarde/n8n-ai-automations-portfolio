from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import generate_kpi_report


PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "output_samples"
KPI_FILE = OUTPUT_DIR / "kpi_summary.json"
DASHBOARD_FILE = OUTPUT_DIR / "dashboard_preview.html"


def ensure_kpis() -> None:
    if not KPI_FILE.exists():
        generate_kpi_report.main()


def money(value: float) -> str:
    return f"${value:,.0f}"


def metric_card(label: str, value: str, note: str) -> str:
    return f"""
      <section class="card">
        <p class="label">{label}</p>
        <h2>{value}</h2>
        <p class="note">{note}</p>
      </section>
    """


def render_top_customers(customers: List[Dict[str, object]]) -> str:
    rows = "\n".join(
        f"<tr><td>{item['customer']}</td><td>{money(float(item['revenue']))}</td></tr>"
        for item in customers
    )
    return f"<table><thead><tr><th>Customer</th><th>Revenue</th></tr></thead><tbody>{rows}</tbody></table>"


def render_dashboard(kpis: Dict[str, object]) -> str:
    delayed = kpis.get("delayed_orders", [])
    delayed_text = ", ".join(item["order_id"] for item in delayed) if delayed else "None"
    monthly_rows = "\n".join(
        f"<tr><td>{month}</td><td>{money(float(revenue))}</td></tr>"
        for month, revenue in kpis.get("monthly_revenue", {}).items()
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AKcelerateHQ DataOps Dashboard</title>
  <style>
    :root {{
      --navy: #102040;
      --blue: #0458D6;
      --sky: #0880D8;
      --cyan: #21A9DD;
      --aqua: #35BAE0;
      --paper: #F1F0EE;
      --slate: #525D63;
      --plum: #602040;
      --white: #ffffff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: var(--paper);
      color: var(--navy);
    }}
    header {{
      background: var(--navy);
      color: var(--white);
      padding: 28px 40px;
      border-bottom: 6px solid var(--cyan);
    }}
    header p {{ margin: 8px 0 0; color: #d8edf6; }}
    main {{ padding: 28px 40px 44px; max-width: 1180px; margin: 0 auto; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .card {{
      background: var(--white);
      border: 1px solid #d9dde0;
      border-radius: 8px;
      padding: 18px;
      min-height: 140px;
    }}
    .label {{
      margin: 0 0 10px;
      color: var(--slate);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0;
      font-weight: 700;
    }}
    h1, h2, h3 {{ margin: 0; }}
    h2 {{ font-size: 30px; color: var(--blue); }}
    .note {{ color: var(--slate); line-height: 1.45; }}
    .panel {{
      background: var(--white);
      border: 1px solid #d9dde0;
      border-radius: 8px;
      padding: 20px;
      margin-top: 16px;
    }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ text-align: left; border-bottom: 1px solid #e5e7eb; padding: 10px 8px; }}
    th {{ color: var(--slate); font-size: 13px; }}
    .risk {{ color: var(--plum); font-weight: 700; }}
    .bar {{
      height: 12px;
      background: linear-gradient(90deg, var(--blue), var(--cyan), var(--aqua));
      border-radius: 999px;
      margin-top: 12px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>AKcelerateHQ DataOps Dashboard</h1>
    <p>Sales order KPI preview generated from the local reporting pipeline. Report date: {kpis['report_date']}.</p>
  </header>
  <main>
    <section class="grid">
      {metric_card("Total Revenue", money(float(kpis['total_revenue'])), "Valid revenue rows only")}
      {metric_card("Pending Payments", money(float(kpis['pending_payments'])), "Includes pending and overdue")}
      {metric_card("Overdue Amount", money(float(kpis['overdue_invoice_amount'])), str(kpis['overdue_invoice_count']) + " overdue invoices")}
      {metric_card("Average Order Value", money(float(kpis['average_order_value'])), "Based on valid revenue orders")}
    </section>
    <section class="panel">
      <h3>Top Customers</h3>
      {render_top_customers(kpis['top_customers'])}
    </section>
    <section class="panel">
      <h3>Monthly Revenue</h3>
      <div class="bar"></div>
      <table><thead><tr><th>Month</th><th>Revenue</th></tr></thead><tbody>{monthly_rows}</tbody></table>
    </section>
    <section class="panel">
      <h3>Data Quality And Operations Risk</h3>
      <p class="risk">Data quality issues logged: {kpis['data_quality_issue_count']}</p>
      <p>Delayed orders: {delayed_text}</p>
      <p class="note">Use this dashboard as a stakeholder preview. In production, the same metrics should be stored in a database or BI layer after validation.</p>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    ensure_kpis()
    kpis = json.loads(KPI_FILE.read_text(encoding="utf-8"))
    DASHBOARD_FILE.write_text(render_dashboard(kpis), encoding="utf-8")
    print(f"Dashboard written to {DASHBOARD_FILE}")


if __name__ == "__main__":
    main()

