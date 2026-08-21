#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from channel_id.joint_identifiability import joint_identifiability_matrix, moderation_test_state

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/joint_identifiability_matrix.json"


def main() -> None:
    rows = joint_identifiability_matrix()
    state = moderation_test_state(rows)
    exact_dep = [r["panel"] for r in rows if r["direct_total_reproductive_dependency"] == "exact"]
    exact_exposure = [r["panel"] for r in rows if r["functional_exposure"] == "exact"]
    report = {
        "schema_version": "1.0",
        "analysis": "joint_identifiability_matrix",
        "real_data_only": True,
        "rows": rows,
        "summary": {
            "n_panels": len(rows),
            "exact_functional_exposure_panels": exact_exposure,
            "exact_direct_total_dependency_panels": exact_dep,
            "exact_joint_exposure_dependency_panels": state["exact_joint_panels"],
            "dependency_x_functional_exposure_test": state,
        },
        "scientific_reading": (
            "The current repository contains strong source-native evidence for both functional-exposure variation "
            "and direct reproductive-dependency variation, but these channels occur in different panels. "
            "Therefore the hypothesis that plant reproductive dependency moderates downstream response to "
            "pollinator functional change is biologically plausible and motivated by real data, but is not yet "
            "empirically identified as a cross-system coefficient."
        ),
        "next_empirical_gate": (
            "Obtain same-population linked functional exposure and direct reproductive dependency for Campanula "
            "under Issue #91, then seek at least one additional independent lineage/system with the same joint design "
            "before estimating a cross-lineage moderation slope."
        ),
        "claim_boundary": (
            "Do not regress source-native dependency ratios against FDQ-like exposure values across panels unless both "
            "quantities are jointly observed under a declared harmonized estimand. Partial evidence is not promoted "
            "to exact overlap, and repeated plants within one archipelago are not independent archipelago replicates."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
