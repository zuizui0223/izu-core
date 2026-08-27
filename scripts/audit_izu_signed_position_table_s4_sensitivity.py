#!/usr/bin/env python3
"""Post-target sensitivity using the site-specific numeric values explicitly reported in Table S4.

The frozen primary signed-position mapping used the single species-level proboscis value
reported in Table S2 together with site-specific visit counts. Table S4 reports exact
site means for five pollinator species whose functional-group assignment varies among
sites. This audit corrects only those source-reported cases and reruns the already-frozen
primary projection. It does not replace or retune the primary mapping.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_PATH = ROOT / "scripts" / "analyze_izu_signed_position_triangulation.py"
SPEC = importlib.util.spec_from_file_location("izu_signed_position", ANALYSIS_PATH)
assert SPEC is not None and SPEC.loader is not None
ANALYSIS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYSIS)

# Table S2 species-level value, site visit counts, and Table S4 site-specific value.
# Only non-zero-visit cells with a Table S4 numeric value need to be represented.
S4_ROWS: dict[str, dict[str, Any]] = {
    "Campsomeriella annulata": {
        "table_s2_mm": 5.2,
        "sites": {
            "hitachi": (37, 4.3), "hitachinaka": (20, 5.3), "tateyama": (12, 6.0),
            "oshima": (13, 5.4), "niijima": (57, 5.1), "kozu": (129, 5.3), "miyake": (4, 6.3),
        },
    },
    "Scolia histrionica": {
        "table_s2_mm": 3.8,
        "sites": {
            "hitachi": (36, 4.2), "hitachinaka": (12, 3.8), "tateyama": (42, 3.8),
            "oshima": (44, 3.7), "niijima": (17, 3.9), "kozu": (1, 4.8),
        },
    },
    "Coelioxys formosicola": {
        "table_s2_mm": 4.7,
        "sites": {"hitachinaka": (2, 5.4), "tateyama": (2, 4.0)},
    },
    "Eucera nipponensis": {
        "table_s2_mm": 10.3,
        "sites": {
            "hitachi": (1, 11.2), "hitachinaka": (1, 10.7), "tateyama": (16, 11.3),
            "oshima": (3, 8.7), "kozu": (7, 9.5),
        },
    },
    "Polygonia c-aureum c-aureum": {
        "table_s2_mm": 10.0,
        "sites": {"hitachi": (2, 8.1), "tateyama": (1, 12.0)},
    },
}


def corrected_centers(gate: dict[str, Any]) -> dict[str, float]:
    centers = ANALYSIS.centers_from_gate(gate)
    site_payload = gate["pollinator_community_centers"]["site_centers_mm"]
    for site in centers:
        total_visits = int(site_payload[site]["n_visits"])
        weighted_delta = 0.0
        for row in S4_ROWS.values():
            if site not in row["sites"]:
                continue
            visits, site_mm = row["sites"][site]
            weighted_delta += int(visits) * (float(site_mm) - float(row["table_s2_mm"]))
        centers[site] = float(centers[site] + weighted_delta / total_visits)
    return centers


def build(gate_path: Path, plant_csv: Path) -> dict[str, Any]:
    gate = ANALYSIS.load_gate(gate_path)
    plant_site = ANALYSIS.aggregate_plant_site(pd.read_csv(plant_csv))
    centers = corrected_centers(gate)

    primary_spec = gate["pollinator_community_centers"]["primary_source_regime"]
    source_sites = [str(value) for value in primary_spec["sites"]]
    site_payload = gate["pollinator_community_centers"]["site_centers_mm"]
    source_visits = sum(int(site_payload[site]["n_visits"]) for site in source_sites)
    corrected_source_center = sum(
        int(site_payload[site]["n_visits"]) * centers[site] for site in source_sites
    ) / source_visits
    target_sites = sorted(set(centers) - set(source_sites))

    rows = ANALYSIS.build_projection_rows(
        plant_site,
        source_sites=source_sites,
        source_center_mm=corrected_source_center,
        target_sites=target_sites,
        site_centers_mm=centers,
    )
    summary = ANALYSIS.summarize_projection(rows)
    return {
        "schema_version": "1.0",
        "analysis": "izu_signed_position_table_s4_site_value_sensitivity",
        "role": "post-target robustness only; frozen Table S2 primary is unchanged",
        "table_s4_corrected_taxa": len(S4_ROWS),
        "corrected_site_centers_mm": centers,
        "corrected_continental_center_mm": corrected_source_center,
        "result": summary,
        "reading": (
            "This sensitivity asks whether the frozen primary result is materially changed when the exact site-specific numeric values explicitly reported in Table S4 replace the Table S2 species-level value for the five affected taxa. It does not make the remaining taxa site-exact."
        ),
        "claim_boundary": (
            "The 2017 supplement does not expose complete site-specific numeric proboscis means for all taxa. This sensitivity reduces one known transfer approximation but does not turn the community center into a fully site-exact trait reconstruction."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate", type=Path, required=True)
    parser.add_argument("--plant-csv", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.gate, args.plant_csv)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
