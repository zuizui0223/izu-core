#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from channel_id.functional_exposure_harmonization import current_exposure_audits, harmonization_state

OUT = ROOT / "data/results/functional_exposure_harmonization_gate.json"


def main() -> None:
    audits = current_exposure_audits()
    report = {
        "schema_version": "1.0",
        "analysis": "functional_exposure_harmonization_gate",
        "source_locked_reference": {
            "paper_doi": "10.1111/1365-2435.14527",
            "dataset_doi": "10.6084/m9.figshare.25025000.v1",
            "metric": "abundance-weighted Rao's quadratic entropy of pollinator proboscis length",
            "formula": "FDQ = sum_i sum_j p_i p_j abs(L_i - L_j)",
            "interpretation": "higher values indicate a wider abundance-weighted distribution of proboscis-length function"
        },
        "required_for_izu_compatible_fdq": [
            "visitor relative abundance within a declared exposure unit",
            "quantitative pollination-relevant trait for every admitted visitor taxon/group",
            "source-native or prospectively prespecified trait mapping independent of reproductive outcome",
            "Rao-Q calculation under the same formula/direction",
            "repeated exposure units rather than one pooled population total"
        ],
        "prohibited_substitutions": [
            "species richness",
            "Shannon diversity",
            "Gini-Simpson diversity",
            "visitor identity alone",
            "binary Bombus/Apis presence",
            "coarse guild count without a quantitative trait distance",
            "a trait chosen after inspecting dependency or reproductive outcomes"
        ],
        "panels": [
            {
                "panel": row.panel,
                "relative_abundance_available": row.relative_abundance_available,
                "quantitative_pollination_trait_available": row.quantitative_pollination_trait_available,
                "source_or_prespecified_trait_map": row.source_or_prespecified_trait_map,
                "rao_q_estimable": row.rao_q_estimable,
                "repeated_exposure_units": row.repeated_exposure_units,
                "direct_dependency_same_source_unit": row.direct_dependency_same_source_unit,
                "izu_compatible_fdq_ready": row.izu_compatible_fdq_ready,
                "exact_joint_ready": row.exact_joint_ready,
                "note": row.note,
            }
            for row in audits
        ],
        "state": harmonization_state(),
        "scientific_reading": (
            "The apparent joint-data gap has narrowed: Seychelles Thespesia and Guaiacum contain useful source-linked "
            "exposure plus breeding information. The remaining cross-system blocker is construct harmonization, not "
            "mere row count. Izu FDQ is a quantitative trait-distance metric, so richness or generic visitor diversity "
            "cannot be used as an FDQ substitute."
        ),
        "next_gate": (
            "For Issue #91, preserve visitor taxon identity and attach a prospectively frozen proboscis-length/functional-trait "
            "lookup so the Campanula pilot can calculate the same Rao-Q exposure metric. For external systems, reopen "
            "harmonization only when visitor abundances and quantitative pollination traits are both recoverable."
        ),
        "claim_boundary": (
            "This gate defines comparability requirements; it does not assert that proboscis length is a universal functional "
            "trait for vertebrate-pollinated systems. Systems lacking a biologically homologous quantitative trait remain "
            "outside the Izu-compatible FDQ analysis rather than being forced onto the scale."
        )
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["state"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
