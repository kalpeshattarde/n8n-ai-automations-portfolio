from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Tuple


PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_DIR / "sample_data" / "sales_orders.csv"
OUTPUT_DIR = PROJECT_DIR / "output_samples"
CLEAN_FILE = OUTPUT_DIR / "cleaned_sales_orders.csv"
LOG_FILE = OUTPUT_DIR / "data_quality_log.csv"
REPORT_DATE = date(2026, 6, 28)


def normalize(value: str | None) -> str:
    return (value or "").strip()


def parse_date(value: str | None) -> Tuple[str, str]:
    raw = normalize(value)
    if not raw:
        return "", "missing_date"
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw, fmt).date().isoformat(), ""
        except ValueError:
            continue
    return "", f"invalid_date:{raw}"


def parse_float(value: str | None) -> Tuple[float, str]:
    raw = normalize(value).replace(",", "").replace("$", "")
    if not raw:
        return 0.0, "missing_number"
    try:
        return float(raw), ""
    except ValueError:
        return 0.0, f"invalid_number:{raw}"


def parse_int(value: str | None) -> Tuple[int, str]:
    number, error = parse_float(value)
    return int(number), error


def standardize_status(value: str, allowed: List[str], default: str) -> Tuple[str, str]:
    cleaned = normalize(value).title()
    mapping = {item.lower(): item for item in allowed}
    if cleaned.lower() in mapping:
        return mapping[cleaned.lower()], ""
    return default, f"invalid_status:{value}"


def read_orders() -> List[Dict[str, str]]:
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean_orders() -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_rows: List[Dict[str, str]] = []
    logs: List[Dict[str, str]] = []

    for index, row in enumerate(read_orders(), start=1):
        order_id = normalize(row.get("order_id")) or f"row_{index}"
        issues: List[str] = []

        order_date, order_date_error = parse_date(row.get("order_date"))
        due_date, due_date_error = parse_date(row.get("invoice_due_date"))
        ship_date, ship_date_error = parse_date(row.get("ship_date"))
        delivery_date, delivery_date_error = parse_date(row.get("delivery_date"))
        quantity, quantity_error = parse_int(row.get("quantity"))
        unit_price, price_error = parse_float(row.get("unit_price"))
        payment_status, payment_error = standardize_status(
            normalize(row.get("payment_status")), ["Paid", "Pending", "Overdue"], "Pending"
        )
        order_status, order_error = standardize_status(
            normalize(row.get("order_status")), ["New", "In Progress", "Delivered", "Delayed"], "New"
        )

        for error in [
            order_date_error,
            due_date_error,
            ship_date_error if normalize(row.get("ship_date")) else "",
            delivery_date_error if normalize(row.get("delivery_date")) else "",
            quantity_error,
            price_error,
            payment_error,
            order_error,
        ]:
            if error:
                issues.append(error)

        amount = quantity * unit_price if quantity > 0 and unit_price > 0 else 0.0
        valid_revenue = "yes" if amount > 0 and order_date else "no"
        overdue = "no"
        if due_date and payment_status in {"Pending", "Overdue"}:
            overdue = "yes" if datetime.fromisoformat(due_date).date() < REPORT_DATE else "no"

        delayed = "yes" if order_status == "Delayed" else "no"
        if order_status in {"Delivered", "Delayed"} and not delivery_date:
            delayed = "yes"
            issues.append("missing_delivery_date_for_closed_or_delayed_order")

        cleaned_rows.append(
            {
                "order_id": order_id,
                "order_date": order_date,
                "customer_name": normalize(row.get("customer_name")),
                "country": normalize(row.get("country")),
                "product": normalize(row.get("product")),
                "quantity": str(quantity),
                "unit_price": f"{unit_price:.2f}",
                "currency": normalize(row.get("currency")) or "USD",
                "amount": f"{amount:.2f}",
                "payment_status": payment_status,
                "invoice_due_date": due_date,
                "order_status": order_status,
                "ship_date": ship_date,
                "delivery_date": delivery_date,
                "owner": normalize(row.get("owner")),
                "is_overdue": overdue,
                "is_delayed": delayed,
                "is_valid_revenue": valid_revenue,
                "data_quality_issues": " | ".join(sorted(set(issues))) if issues else "none",
            }
        )

        if issues:
            logs.append(
                {
                    "order_id": order_id,
                    "row_number": str(index),
                    "severity": "high" if valid_revenue == "no" else "medium",
                    "issues": " | ".join(sorted(set(issues))),
                }
            )

    return cleaned_rows, logs


def main() -> None:
    rows, logs = clean_orders()
    fields = [
        "order_id",
        "order_date",
        "customer_name",
        "country",
        "product",
        "quantity",
        "unit_price",
        "currency",
        "amount",
        "payment_status",
        "invoice_due_date",
        "order_status",
        "ship_date",
        "delivery_date",
        "owner",
        "is_overdue",
        "is_delayed",
        "is_valid_revenue",
        "data_quality_issues",
    ]
    write_csv(CLEAN_FILE, rows, fields)
    write_csv(LOG_FILE, logs, ["order_id", "row_number", "severity", "issues"])
    print(f"Cleaned {len(rows)} orders. Clean file written to {CLEAN_FILE}")


if __name__ == "__main__":
    main()

