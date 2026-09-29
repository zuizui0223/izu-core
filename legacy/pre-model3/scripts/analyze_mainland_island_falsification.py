#!/usr/bin/env python3
"""Summarize the predeclared mainland/island falsification ledger.

This analysis is intentionally categorical. It tests whether broad novelty claims survive
mainland controls; it does not convert heterogeneous literature into a common effect size.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/results/mainland_island_falsification_ledger.json"
OUT = ROOT / "data/results/mainland_island_falsification_summary.json"


def build_summary(data: dict) -> dict:
    verdicts = {}
    for row in data["controls"]:
        verdicts.setdefault(row["test"], []).append(row["verdict"])

    return {
        "schema_version": "1.0",
        "n_controls": len(data["controls"]),
        "tests": verdicts,
        "hypothesis_assessment": data["hypothesis_assessment"],
        "overbroad_claims_falsified": [
            "functional_recurrence_is_island_specific",
            "architectural_contingency_is_island_specific",
        ],
        "surviving_island_specific_candidate": (
            "oceanic_insularity_changes_architectural_opportunity_space"
        ),
        "refined_repository_claim": data["refined_repository_claim"],
        "next_test": data["next_test"],
        "claim_boundary": data["claim_boundary"],
    }


def main() -> None:
    data = json.loads(LEDGER.read_text())
    summary = build_summary(data)
    OUT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
