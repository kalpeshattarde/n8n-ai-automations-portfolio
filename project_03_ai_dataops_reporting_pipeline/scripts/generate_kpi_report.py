from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

import clean_data


PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "output_samples"
CLEAN_FILE = OUTPUT_DIR / "cleaned_sales_orders.csv"
LOG_FILE = OUTPUT_DIR / "data_quality_log.csv"
KPI_FILE = OUTPUT_DIR / "kpi_summary.json"
REPORT_FILE = OUTPUT_DIR / "weekly_ai_insights_report.md"


def parse_float(value: str | None) -> float:
    try:
        return float(value or 0)
    except ValueError:
        return 0.0


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def ensure_clean_data() -> None:
    if not CLEAN_FILE.exists():
        clean_data.main()


def calculate_kpis(rows: List[Dict[str, str]], issue_count: int) -> Dict[str, object]:
    valid_rows = [row for row in rows if row["is_valid_revenue"] == "yes"]
    total_revenue = sum(parse_float(row["amount"]) for row in valid_rows)
    pending_payments = sum(
        parse_float(row["amount"])
        for row in valid_rows
        if row["payment_status"] in {"Pending", "Overdue"}
    )
    overdue_invoices = [row for row in valid_rows if row["is_overdue"] == "yes"]
    delayed_orders = [row for row in rows if row["is_delayed"] == "yes"]
    average_order_value = total_revenue / len(valid_rows) if valid_rows else 0.0

    customer_revenue: Dict[str, float] = defaultdict(float)
    monthly_revenue: Dict[str, float] = defaultdict(float)
    for row in valid_rows:
        amount = parse_float(row["amount"])
        customer_revenue[row["customer_name"]] += amount
        month = row["order_date"][:7] if row["order_date"] else "unknown"
        monthly_revenue[month] += amount

    top_customers = sorted(customer_revenue.items(), key=lambda item: item[1], reverse=True)[:5]

    return {
        "report_date": clean_data.REPORT_DATE.isoformat(),
        "total_orders": len(rows),
        "valid_revenue_orders": len(valid_rows),
        "total_revenue": round(total_revenue, 2),
        "pending_payments": round(pending_payments, 2),
        "overdue_invoice_count": len(overdue_invoices),
        "overdue_invoice_amount": round(sum(parse_float(row["amount"]) for row in overdue_invoices), 2),
        "average_order_value": round(average_order_value, 2),
        "top_customers": [{"customer": name, "revenue": round(value, 2)} for name, value in top_customers],
        "delayed_orders": [{"order_id": row["order_id"], "customer": row["customer_name"]} for row in delayed_orders],
        "monthly_revenue": {month: round(value, 2) for month, value in sorted(monthly_revenue.items())},
        "data_quality_issue_count": issue_count,
    }


def write_report(kpis: Dict[str, object]) -> None:
    top_customer = kpis["top_customers"][0] if kpis["top_customers"] else {"customer": "n/a", "revenue": 0}
    lines = [
        "# Weekly AI Insights Report",
        "",
        f"Report date: {kpis['report_date']}",
        "",
        "## KPI Summary",
        "",
        f"- Total revenue: ${kpis['total_revenue']:,.2f}",
        f"- Pending payments: ${kpis['pending_payments']:,.2f}",
        f"- Overdue invoice amount: ${kpis['overdue_invoice_amount']:,.2f}",
        f"- Overdue invoice count: {kpis['overdue_invoice_count']}",
        f"- Average order value: ${kpis['average_order_value']:,.2f}",
        f"- Data quality issues logged: {kpis['data_quality_issue_count']}",
        "",
        "## AI-Style Insights",
        "",
        f"- {top_customer['customer']} is the largest customer in the current sample at ${top_customer['revenue']:,.2f}.",
        "- Collections follow-up should focus on overdue and pending accounts before the next reporting cycle.",
        "- Delayed or incomplete delivery rows should be reviewed because they can distort operations reporting.",
        "- Invalid revenue rows are excluded from KPI totals but retained in the data quality log for correction.",
        "",
        "## Monthly Revenue",
        "",
        "| Month | Revenue |",
        "| --- | ---: |",
    ]
    for month, revenue in kpis["monthly_revenue"].items():
        lines.append(f"| {month} | ${revenue:,.2f} |")

    lines.extend(["", "## Delayed Orders", "", "| Order | Customer |", "| --- | --- |"])
    for order in kpis["delayed_orders"]:
        lines.append(f"| {order['order_id']} | {order['customer']} |")

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ensure_clean_data()
    rows = read_csv(CLEAN_FILE)
    issue_count = len(read_csv(LOG_FILE)) if LOG_FILE.exists() else 0
    kpis = calculate_kpis(rows, issue_count)
    KPI_FILE.write_text(json.dumps(kpis, indent=2), encoding="utf-8")
    write_report(kpis)
    print(f"KPI report written to {REPORT_FILE}")


if __name__ == "__main__":
    main()

