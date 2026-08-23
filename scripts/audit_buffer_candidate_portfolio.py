#!/usr/bin/env python3
"""Audit all registered buffer candidates with the frozen common interface."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.audit_buffer_mechanism_abm_admission import assess_candidate

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORTFOLIO = ROOT / "data/design/buffer_candidate_portfolio.json"


def load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def build(portfolio_path: Path = DEFAULT_PORTFOLIO) -> dict[str, Any]:
    portfolio = load(portfolio_path)
    interface_path = ROOT / str(portfolio["interface"])
    interface = load(interface_path)
    rows = []
    for relative in portfolio["candidates"]:
        candidate_path = ROOT / str(relative)
        candidate = load(candidate_path)
        audit = assess_candidate(candidate, interface)
        audit["candidate_path"] = str(relative)
        rows.append(audit)

    state_counts = Counter(row["state"] for row in rows)
    missing_counts = Counter()
    for row in rows:
        for reason in row["reasons"]:
            if reason.startswith("missing prerequisite: "):
                missing_counts[reason.removeprefix("missing prerequisite: ")] += 1

    return {
        "schema_version": "1.0",
        "analysis": "buffer_candidate_portfolio_admission",
        "interface": str(portfolio["interface"]),
        "candidates": rows,
        "summary": {
            "candidate_count": len(rows),
            "state_counts": dict(sorted(state_counts.items())),
            "mapping_ready_count": sum(bool(row["mapping_ready"]) for row in rows),
            "empirically_admitted_count": sum(bool(row["empirically_admitted"]) for row in rows),
            "missing_prerequisite_counts": dict(sorted(missing_counts.items())),
        },
        "decision": "no_current_registered_buffer_candidate_is_mapping_ready_or_empirically_admitted",
        "next_gate": (
            "Close source-identified missing prerequisites in existing candidates or register a genuinely new candidate. "
            "Do not add a generic buffer parameter and do not use known target outcomes to choose mappings."
        ),
        "claim_boundary": (
            "This portfolio compares admission readiness, not biological effect sizes. Different candidates may lack different links and are not quantitatively pooled."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--portfolio", type=Path, default=DEFAULT_PORTFOLIO)
    parser.add_argument("--output", type=Path, default=ROOT / "data/results/buffer_candidate_portfolio_admission_frozen.json")
    args = parser.parse_args()
    try:
        result = build(args.portfolio)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(str(error)) from error
    print(args.output)


if __name__ == "__main__":
    main()
