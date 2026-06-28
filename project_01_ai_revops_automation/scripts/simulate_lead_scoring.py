from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_DIR / "sample_data" / "leads.csv"
OUTPUT_DIR = PROJECT_DIR / "output_samples"
RESULTS_FILE = OUTPUT_DIR / "lead_scoring_results.csv"
LOG_FILE = OUTPUT_DIR / "processing_log.csv"
SUMMARY_FILE = OUTPUT_DIR / "ai_lead_summary_sample.md"


ResultRow = Dict[str, str]


def normalize(value: str | None) -> str:
    return (value or "").strip()


def parse_number(value: str | None) -> float:
    cleaned = normalize(value).replace(",", "").replace("$", "").replace("USD", "")
    digits = "".join(ch for ch in cleaned if ch.isdigit() or ch == ".")
    if not digits:
        return 0.0
    try:
        return float(digits)
    except ValueError:
        return 0.0


def contains_any(value: str, keywords: Iterable[str]) -> bool:
    lower = value.lower()
    return any(keyword in lower for keyword in keywords)


def score_lead(row: Dict[str, str]) -> Tuple[int, str, List[str], List[str]]:
    consent = normalize(row.get("consent")).lower()
    if consent not in {"yes", "y", "true", "1"}:
        return 0, "Unqualified", ["Contact consent was not provided."], ["missing_consent"]

    score = 0
    reasons: List[str] = []
    risks: List[str] = []

    monthly_revenue = parse_number(row.get("monthly_revenue"))
    budget = parse_number(row.get("budget"))
    hours_lost = parse_number(row.get("hours_lost_per_week"))
    timeline = normalize(row.get("timeline"))
    authority = normalize(row.get("decision_authority"))
    desired_outcome = normalize(row.get("desired_outcome"))
    tools_used = normalize(row.get("tools_used"))

    if monthly_revenue >= 100000:
        score += 15
        reasons.append("High revenue account with meaningful automation upside.")
    elif monthly_revenue >= 50000:
        score += 10
        reasons.append("Mid-market revenue profile can justify workflow investment.")
    elif monthly_revenue >= 20000:
        score += 5

    if hours_lost >= 15:
        score += 20
        reasons.append("Manual work is costing more than 15 hours per week.")
    elif hours_lost >= 10:
        score += 15
        reasons.append("Manual work is costing at least 10 hours per week.")
    elif hours_lost >= 5:
        score += 8

    if budget >= 15000:
        score += 20
        reasons.append("Budget supports a production automation build.")
    elif budget >= 8000:
        score += 15
        reasons.append("Budget is strong enough for a scoped automation sprint.")
    elif budget >= 3000:
        score += 8
    else:
        risks.append("budget_may_be_too_low")

    if contains_any(timeline, ["immediate", "this month", "asap", "urgent", "next 30"]):
        score += 20
        reasons.append("Timeline indicates near-term buying intent.")
    elif contains_any(timeline, ["next 60", "60 days"]):
        score += 10
    elif contains_any(timeline, ["quarter"]):
        score += 5

    if contains_any(authority, ["founder", "owner", "ceo", "vp", "director", "partner", "sales head"]):
        score += 15
        reasons.append("Requester appears to have decision authority.")
    elif contains_any(authority, ["manager", "operations"]):
        score += 8
    else:
        risks.append("decision_authority_unclear")

    if len(desired_outcome) >= 45:
        score += 10
        reasons.append("Desired outcome is specific enough to scope a workflow.")

    if tools_used.count(";") >= 2:
        score += 5

    if not normalize(row.get("work_email")):
        score -= 12
        risks.append("missing_work_email")

    score = max(0, min(100, score))
    if score >= 75:
        tier = "Hot"
    elif score >= 50:
        tier = "Warm"
    elif score >= 25:
        tier = "Cold"
    else:
        tier = "Unqualified"

    if not reasons:
        reasons.append("Lead has limited urgency, budget, or operational detail.")

    return score, tier, reasons[:3], risks


def recommend_next_action(tier: str, risks: List[str]) -> str:
    if "missing_consent" in risks:
        return "Do not contact. Keep record only for audit trail."
    if "missing_work_email" in risks:
        return "Ask owner to enrich contact details before outreach."
    if tier == "Hot":
        return "Notify sales owner today and draft a same-day discovery call email."
    if tier == "Warm":
        return "Send consultative follow-up and ask two scoping questions."
    if tier == "Cold":
        return "Add to nurture list with educational automation examples."
    return "No sales action recommended."


def build_summary(row: Dict[str, str], score: int, tier: str, reasons: List[str], risks: List[str]) -> str:
    company = normalize(row.get("company_name")) or "Unknown company"
    pain = normalize(row.get("pain_points")) or "No pain point provided"
    outcome = normalize(row.get("desired_outcome")) or "No desired outcome provided"
    risk_text = ", ".join(risks) if risks else "none"
    reason_text = " ".join(reasons)
    return (
        f"{company} is a {tier} lead with score {score}. {reason_text} "
        f"Pain point: {pain}. Desired outcome: {outcome}. Risk flags: {risk_text}."
    )


def draft_follow_up(row: Dict[str, str], tier: str) -> str:
    first_name = (normalize(row.get("full_name")).split() or ["there"])[0]
    company = normalize(row.get("company_name")) or "your team"
    pain = normalize(row.get("pain_points")) or "the manual workflow you described"
    outcome = normalize(row.get("desired_outcome")) or "reduce manual work and improve follow-up speed"

    if tier == "Unqualified":
        return "No outreach drafted because this lead is unqualified or missing consent."

    return (
        f"Hi {first_name},\n\n"
        f"Thanks for sharing the workflow details for {company}. Based on your note about {pain}, "
        f"the strongest starting point is a focused automation sprint around {outcome}.\n\n"
        "I can map the current process, identify the handoff points, and show what should be automated "
        "first versus kept for human review. Would you be open to a 20-minute discovery call this week?\n\n"
        "Regards,\nKalpesh"
    )


def read_leads() -> List[Dict[str, str]]:
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: List[ResultRow]) -> None:
    hot_or_warm = [row for row in rows if row["lead_tier"] in {"Hot", "Warm"}]
    hot_or_warm.sort(key=lambda row: int(row["lead_score"]), reverse=True)
    top_rows = hot_or_warm[:5]

    lines = [
        "# AI Lead Summary Sample",
        "",
        f"Generated at: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Priority Leads",
        "",
    ]

    if not top_rows:
        lines.append("No Hot or Warm leads found in this batch.")
    else:
        lines.append("| Lead | Company | Tier | Score | Next Action |")
        lines.append("| --- | --- | --- | ---: | --- |")
        for row in top_rows:
            lines.append(
                f"| {row['full_name']} | {row['company_name']} | {row['lead_tier']} | "
                f"{row['lead_score']} | {row['next_action']} |"
            )

    if top_rows:
        sample = top_rows[0]
        lines.extend(
            [
                "",
                "## Sample Follow-Up Draft",
                "",
                f"Lead: {sample['full_name']} at {sample['company_name']}",
                "",
                "```text",
                sample["follow_up_email"],
                "```",
            ]
        )

    SUMMARY_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def process_leads() -> Tuple[List[ResultRow], List[Dict[str, str]]]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results: List[ResultRow] = []
    logs: List[Dict[str, str]] = []

    for index, row in enumerate(read_leads(), start=1):
        lead_name = normalize(row.get("full_name")) or f"Row {index}"
        try:
            score, tier, reasons, risks = score_lead(row)
            next_action = recommend_next_action(tier, risks)
            summary = build_summary(row, score, tier, reasons, risks)
            follow_up = draft_follow_up(row, tier)

            if tier == "Unqualified":
                processing_status = "quarantined"
            elif risks:
                processing_status = "needs_review"
            else:
                processing_status = "processed"

            results.append(
                {
                    "full_name": lead_name,
                    "work_email": normalize(row.get("work_email")),
                    "company_name": normalize(row.get("company_name")),
                    "industry": normalize(row.get("industry")),
                    "monthly_revenue": normalize(row.get("monthly_revenue")),
                    "hours_lost_per_week": normalize(row.get("hours_lost_per_week")),
                    "budget": normalize(row.get("budget")),
                    "timeline": normalize(row.get("timeline")),
                    "decision_authority": normalize(row.get("decision_authority")),
                    "lead_score": str(score),
                    "lead_tier": tier,
                    "top_reasons": " | ".join(reasons),
                    "risk_flags": " | ".join(risks) if risks else "none",
                    "next_action": next_action,
                    "ai_summary": summary,
                    "follow_up_email": follow_up,
                    "processing_status": processing_status,
                }
            )
            logs.append(
                {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "row_number": str(index),
                    "lead": lead_name,
                    "status": "success" if processing_status == "processed" else processing_status,
                    "message": next_action,
                }
            )
        except Exception as exc:  # Defensive row-level logging for portfolio review.
            logs.append(
                {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "row_number": str(index),
                    "lead": lead_name,
                    "status": "error",
                    "message": str(exc),
                }
            )

    return results, logs


def main() -> None:
    results, logs = process_leads()
    result_fields = [
        "full_name",
        "work_email",
        "company_name",
        "industry",
        "monthly_revenue",
        "hours_lost_per_week",
        "budget",
        "timeline",
        "decision_authority",
        "lead_score",
        "lead_tier",
        "top_reasons",
        "risk_flags",
        "next_action",
        "ai_summary",
        "follow_up_email",
        "processing_status",
    ]
    log_fields = ["timestamp_utc", "row_number", "lead", "status", "message"]
    write_csv(RESULTS_FILE, results, result_fields)
    write_csv(LOG_FILE, logs, log_fields)
    write_summary(results)
    print(f"Processed {len(results)} leads. Results written to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
