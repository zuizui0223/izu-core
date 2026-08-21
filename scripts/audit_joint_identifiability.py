#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from channel_id.joint_identifiability import (
    joint_identifiability_matrix,
    moderation_test_state,
    panels_with_partial_or_exact_joint_context,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/joint_identifiability_matrix.json"


def main() -> None:
    rows = joint_identifiability_matrix()
    state = moderation_test_state(rows)
    exact_dep = [r["panel"] for r in rows if r["direct_total_reproductive_dependency"] == "exact"]
    exact_exposure = [r["panel"] for r in rows if r["functional_exposure"] == "exact"]
    joint_context = panels_with_partial_or_exact_joint_context(rows)
    report = {
        "schema_version": "1.1",
        "analysis": "joint_identifiability_matrix",
        "real_data_only": True,
        "rows": rows,
        "summary": {
            "n_panels": len(rows),
            "exact_functional_exposure_panels": exact_exposure,
            "exact_direct_total_dependency_panels": exact_dep,
            "partial_or_exact_same_population_joint_context_panels": joint_context,
            "exact_joint_exposure_dependency_panels": state["exact_joint_panels"],
            "dependency_x_functional_exposure_test": state,
        },
        "scientific_reading": (
            "The repository now contains several real systems where pollinator exposure and reproductive information "
            "coexist at a source-linked population or individual unit, including individual-level Thespesia linkage "
            "in Seychelles and a two-population Guaiacum assemblage/breeding design. Those systems remain partial "
            "for the cross-lineage target because their exposure metrics are not harmonized to the Izu functional "
            "exposure estimand and/or their total dependency estimands are incomplete. Real-data motivation has "
            "therefore strengthened without making the moderation coefficient identified."
        ),
        "next_empirical_gate": (
            "Obtain same-population linked functional exposure and direct reproductive dependency for Campanula "
            "under Issue #91. In parallel, preserve Seychelles and Guaiacum as external joint architectures while "
            "defining a prespecified cross-system functional-exposure estimand before any harmonized slope is fit."
        ),
        "claim_boundary": (
            "Do not regress source-native dependency ratios against richness, broad visitor-group diversity or other "
            "FDQ-like quantities across panels unless both quantities are jointly observed under a declared harmonized "
            "estimand. Partial joint context is not promoted to exact moderation evidence, and repeated plants within "
            "one archipelago are not independent archipelago replicates."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
