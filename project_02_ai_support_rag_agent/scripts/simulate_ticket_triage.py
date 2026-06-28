from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import simple_rag_retriever


PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_DIR / "sample_data" / "support_tickets.csv"
OUTPUT_DIR = PROJECT_DIR / "output_samples"
RESULTS_FILE = OUTPUT_DIR / "ticket_triage_results.csv"
DRAFT_FILE = OUTPUT_DIR / "drafted_reply_sample.md"
ESCALATION_FILE = OUTPUT_DIR / "escalation_report_sample.md"
ANALYTICS_FILE = OUTPUT_DIR / "support_analytics_report.md"


def normalize(value: str | None) -> str:
    return (value or "").strip()


def contains_any(text: str, keywords: List[str]) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in keywords)


def classify_ticket(ticket: Dict[str, str]) -> str:
    text = f"{ticket.get('subject', '')} {ticket.get('message', '')}".lower()
    if contains_any(text, ["refund", "cancel trial", "charged after the trial"]):
        return "Refund"
    if contains_any(text, ["invoice", "billing", "charged", "seat", "payment"]):
        return "Billing"
    if contains_any(text, ["api", "sync", "429", "sso", "login", "password", "access denied"]):
        return "Technical"
    if contains_any(text, ["invite", "teammate", "workspace", "onboard"]):
        return "Onboarding"
    if contains_any(text, ["unhappy", "third time", "move to another vendor", "complaint"]):
        return "Complaint"
    return "Other"


def needs_escalation(ticket: Dict[str, str], category: str, confidence: float) -> Tuple[bool, str]:
    priority = normalize(ticket.get("priority")).lower()
    safe_to_auto_reply = normalize(ticket.get("safe_to_auto_reply")).lower() == "yes"
    arr_impact = float(normalize(ticket.get("arr_impact")) or 0)
    text = f"{ticket.get('subject', '')} {ticket.get('message', '')}".lower()

    if category in {"Refund", "Complaint"}:
        return True, f"{category.lower()} tickets require human decisioning"
    if category == "Billing" and contains_any(text, ["invoice", "charged", "refund", "extra seat", "correct it", "dispute"]):
        return True, "billing dispute requires human decisioning"
    if "sso" in text:
        return True, "SSO access issue requires technical support review"
    if confidence < 0.45:
        return True, "retrieval confidence below approval threshold"
    if priority in {"urgent", "high"} and arr_impact >= 10000:
        return True, "high-value or urgent account risk"
    if not safe_to_auto_reply:
        return True, "source data marked unsafe for direct auto-reply"
    return False, "safe for human approval queue"


def draft_reply(ticket: Dict[str, str], article_title: str, article_body: str, category: str) -> str:
    first_name = (normalize(ticket.get("customer_name")).split() or ["there"])[0]
    body_sentence = article_body.split(".")[0].strip()
    return (
        f"Hi {first_name},\n\n"
        f"Thanks for reaching out. Based on our {article_title} guidance, {body_sentence.lower()}.\n\n"
        "I have included the next step below for review. If anything looks different in your workspace, "
        "reply with a screenshot or the affected workspace details and our team will check it.\n\n"
        "Regards,\nSupport Team"
    )


def read_tickets() -> List[Dict[str, str]]:
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def process_tickets() -> List[Dict[str, str]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results: List[Dict[str, str]] = []

    for ticket in read_tickets():
        query = f"{ticket.get('subject', '')} {ticket.get('message', '')}"
        category = classify_ticket(ticket)
        article, confidence = simple_rag_retriever.retrieve(query)[0]
        escalate, escalation_reason = needs_escalation(ticket, category, confidence)
        route = "Escalate" if escalate else "Human Approval"
        reply = draft_reply(ticket, article["title"], article["body"], category)

        results.append(
            {
                "ticket_id": normalize(ticket.get("ticket_id")),
                "customer_name": normalize(ticket.get("customer_name")),
                "account_plan": normalize(ticket.get("account_plan")),
                "priority": normalize(ticket.get("priority")),
                "category": category,
                "matched_article": article["title"],
                "confidence": f"{confidence:.2f}",
                "route": route,
                "escalation_reason": escalation_reason,
                "drafted_reply": reply,
                "processed_at_utc": datetime.now(timezone.utc).isoformat(),
            }
        )

    return results


def write_reports(rows: List[Dict[str, str]]) -> None:
    approval_rows = [row for row in rows if row["route"] == "Human Approval"]
    escalation_rows = [row for row in rows if row["route"] == "Escalate"]

    if approval_rows:
        sample = approval_rows[0]
        DRAFT_FILE.write_text(
            "\n".join(
                [
                    "# Drafted Reply Sample",
                    "",
                    f"Ticket: {sample['ticket_id']}",
                    f"Category: {sample['category']}",
                    f"Matched article: {sample['matched_article']}",
                    f"Confidence: {sample['confidence']}",
                    f"Route: {sample['route']}",
                    "",
                    "```text",
                    sample["drafted_reply"],
                    "```",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    escalation_lines = [
        "# Escalation Report Sample",
        "",
        "| Ticket | Customer | Category | Priority | Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in escalation_rows:
        escalation_lines.append(
            f"| {row['ticket_id']} | {row['customer_name']} | {row['category']} | "
            f"{row['priority']} | {row['escalation_reason']} |"
        )
    ESCALATION_FILE.write_text("\n".join(escalation_lines) + "\n", encoding="utf-8")

    category_counts = Counter(row["category"] for row in rows)
    estimated_minutes_saved = len(approval_rows) * 8 + len(escalation_rows) * 3
    analytics_lines = [
        "# Support Analytics Report",
        "",
        f"Tickets processed: {len(rows)}",
        f"Human approval queue: {len(approval_rows)}",
        f"Escalations: {len(escalation_rows)}",
        f"Estimated handling time saved: {round(estimated_minutes_saved / 60, 1)} hours",
        "",
        "## Category Mix",
        "",
    ]
    for category, count in sorted(category_counts.items()):
        analytics_lines.append(f"- {category}: {count}")
    analytics_lines.extend(
        [
            "",
            "## Operating Notes",
            "",
            "- Approval queue items are routine enough for a human reviewer to send quickly.",
            "- Escalated tickets are intentionally conservative because billing, refunds, complaints, SSO, and high-value incidents need human judgment.",
            "- The next production step is storing approval decisions to improve retrieval and prompt coverage.",
        ]
    )
    ANALYTICS_FILE.write_text("\n".join(analytics_lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = process_tickets()
    fields = [
        "ticket_id",
        "customer_name",
        "account_plan",
        "priority",
        "category",
        "matched_article",
        "confidence",
        "route",
        "escalation_reason",
        "drafted_reply",
        "processed_at_utc",
    ]
    write_csv(RESULTS_FILE, rows, fields)
    write_reports(rows)
    print(f"Processed {len(rows)} tickets. Results written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
