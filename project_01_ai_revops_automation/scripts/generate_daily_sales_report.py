from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Dict, List

import simulate_lead_scoring


PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "output_samples"
RESULTS_FILE = OUTPUT_DIR / "lead_scoring_results.csv"
REPORT_FILE = OUTPUT_DIR / "daily_owner_report_sample.md"


def parse_number(value: str | None) -> float:
    cleaned = (value or "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def read_results() -> List[Dict[str, str]]:
    if not RESULTS_FILE.exists():
        simulate_lead_scoring.main()
    with RESULTS_FILE.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = read_results()
    processed = [row for row in rows if row["processing_status"] == "processed"]
    needs_review = [row for row in rows if row["processing_status"] == "needs_review"]
    sales_relevant = processed + needs_review
    hot = [row for row in sales_relevant if row["lead_tier"] == "Hot"]
    warm = [row for row in sales_relevant if row["lead_tier"] == "Warm"]
    cold = [row for row in sales_relevant if row["lead_tier"] == "Cold"]
    quarantined = [row for row in rows if row["processing_status"] == "quarantined"]
    missing_contact = [row for row in rows if "missing_work_email" in row["risk_flags"]]

    pipeline_revenue = sum(parse_number(row["monthly_revenue"]) for row in hot + warm)
    manual_minutes_saved = len(sales_relevant) * 12 + 35
    time_saved_hours = round(manual_minutes_saved / 60, 1)

    sorted_priority = sorted(sales_relevant, key=lambda row: int(row["lead_score"]), reverse=True)[:5]

    lines = [
        "# Daily Owner Report Sample",
        "",
        f"Report date: {date.today().isoformat()}",
        "",
        "## Executive Summary",
        "",
        f"- Leads reviewed: {len(rows)}",
        f"- Hot leads: {len(hot)}",
        f"- Warm leads: {len(warm)}",
        f"- Cold leads: {len(cold)}",
        f"- Needs owner review: {len(needs_review)}",
        f"- Quarantined or unqualified: {len(quarantined)}",
        f"- Estimated manual time saved: {time_saved_hours} hours",
        f"- Qualified pipeline monthly revenue represented: ${pipeline_revenue:,.0f}",
        "",
        "## Priority Follow-Up Queue",
        "",
        "| Rank | Lead | Company | Tier | Score | Recommended Action |",
        "| ---: | --- | --- | --- | ---: | --- |",
    ]

    for rank, row in enumerate(sorted_priority, start=1):
        lines.append(
            f"| {rank} | {row['full_name']} | {row['company_name']} | {row['lead_tier']} | "
            f"{row['lead_score']} | {row['next_action']} |"
        )

    lines.extend(
        [
            "",
            "## Manager Notes",
            "",
            "- Hot leads should receive same-day owner attention.",
            "- Warm leads should receive a consultative follow-up with scoping questions.",
            "- Missing contact data should be enriched before outreach.",
            "- Unqualified leads are retained in the log for auditability, not sales action.",
            "",
            "## Risk Flags",
            "",
            f"- Missing contact records: {len(missing_contact)}",
            f"- Consent/quarantine records: {len(quarantined)}",
        ]
    )

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Daily report written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
