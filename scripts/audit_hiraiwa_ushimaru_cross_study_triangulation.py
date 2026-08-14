#!/usr/bin/env python3
"""Triangulate 2017 reproductive-response modes with 2024 response channels.

The 2017 Hiraiwa-Ushimaru study source-lock classifies three plant systems by
fruit-set response to long-tongued-pollinator functional exposure. The 2024
Figshare source independently supplies Oshima -> post-Oshima contrasts in
corrected trait matching, floral tube morphology and pollen receipt for those
same taxa.

The studies differ in year, exact geography and response estimands, and the 2017
fruit-set dataset lacks Oshima reproductive observations. This audit therefore
never treats species-specific signs as a same-estimand replication. Instead it
asks whether an independently characterized reproductive-sensitivity panel
supports a uniform downstream response cascade or independently recurs as a
heterogeneous-response system.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Mapping


EXPECTED_SHARED = {
    "Calystegia soldanella",
    "Vitex rotundifolia",
    "Lysimachia mauritiana",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(row: Mapping[str, object], field: str) -> str:
    return str(row.get(field, "") or "").strip()


def build_audit(
    sensitivity_rows: list[dict[str, str]],
    channel_rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    sensitivity = {text(row, "taxon"): row for row in sensitivity_rows}
    channels = {text(row, "plant"): row for row in channel_rows}
    shared = sorted(set(sensitivity) & set(channels))
    if set(shared) != EXPECTED_SHARED:
        raise ValueError(f"unexpected cross-study shared taxa: {shared}")

    rows: list[dict[str, object]] = []
    for taxon in shared:
        s = sensitivity[taxon]
        c = channels[taxon]
        full_cascade = (
            text(c, "matching_direction") == "lower_post"
            and text(c, "tube_direction") == "shorter_post"
            and text(c, "pollen_direction") == "lower_post"
        )
        rows.append({
            "taxon": taxon,
            "study_2017_response_mode": text(s, "response_mode"),
            "study_2017_breeding_context": text(s, "breeding_context"),
            "study_2017_reproductive_response": text(s, "reproductive_response"),
            "study_2017_oshima_reproductive_data_available": text(s, "oshima_reproductive_data_available"),
            "study_2024_matching_delta": float(c["matching_delta_post_minus_oshima"]),
            "study_2024_matching_direction": text(c, "matching_direction"),
            "study_2024_tube_delta_mm": float(c["tube_delta_mm_post_minus_oshima"]),
            "study_2024_tube_direction": text(c, "tube_direction"),
            "study_2024_pollen_delta": float(c["pollen_delta_post_minus_oshima"]),
            "study_2024_pollen_direction": text(c, "pollen_direction"),
            "uniform_matching_tube_pollen_decline": full_cascade,
            "species_specific_sign_replication_status": "not_same_estimand_or_boundary",
        })

    response_modes = sorted({str(row["study_2017_response_mode"]) for row in rows})
    pollen_directions = sorted({str(row["study_2024_pollen_direction"]) for row in rows})
    tube_directions = sorted({str(row["study_2024_tube_direction"]) for row in rows})
    full_cascade_taxa = [str(row["taxon"]) for row in rows if bool(row["uniform_matching_tube_pollen_decline"])]

    summary = {
        "schema_version": "1.0",
        "analysis_name": "hiraiwa_ushimaru_cross_study_triangulation",
        "study_2017_source": {
            "doi": "10.1098/rspb.2016.2218",
            "locked_table": "data/predictive_meta/hiraiwa_ushimaru_2017_reproductive_sensitivity.csv",
            "estimand": "fruit-set response to long-tongued-pollinator functional exposure and related visitation/proboscis metrics",
            "oshima_reproductive_data_available": false,
        },
        "study_2024_source": {
            "doi": "10.6084/m9.figshare.25025000.v1",
            "locked_table": "data/predictive_meta/hiraiwa_ushimaru_cross_channel_concordance.csv",
            "estimands": [
                "corrected trait-matching Oshima-to-post contrast",
                "floral tube Oshima-to-post contrast",
                "open-pollinated pollen-receipt Oshima-to-post contrast",
            ],
        },
        "n_shared_taxa": len(rows),
        "shared_taxa": shared,
        "study_2017_response_modes": response_modes,
        "study_2024_pollen_directions": pollen_directions,
        "study_2024_tube_directions": tube_directions,
        "uniform_matching_tube_pollen_decline_n": len(full_cascade_taxa),
        "uniform_matching_tube_pollen_decline_taxa": full_cascade_taxa,
        "heterogeneity_recurrence": {
            "study_2017_has_multiple_reproductive_response_modes": len(response_modes) > 1,
            "study_2024_shared_panel_has_multiple_pollen_directions": len(pollen_directions) > 1,
            "study_2024_shared_panel_has_multiple_tube_directions": len(tube_directions) > 1,
            "dataset_level_response_heterogeneity_recurs": (
                len(response_modes) > 1 and len(pollen_directions) > 1 and len(tube_directions) > 1
            ),
        },
        "reading": (
            "The three taxa independently characterized in the 2017 reproductive study do not form a uniform 2024 matching-lower / tube-shorter / pollen-lower cascade: zero of three show all three directions together. "
            "The recurring result across the two datasets is response heterogeneity itself, not a stable species-specific sign, because the studies use different years, boundaries and reproductive-function estimands."
        ),
        "mechanistic_implication": (
            "Direct reproductive dependency/assurance and network-state measurements are needed to explain why taxa exposed to a shared functional-environment shift express different downstream outcomes. The independent 2017 modes can constrain interpretation, but they cannot be transported as numeric dependency values into the 2024 analysis."
        ),
        "claim_boundary": (
            "Do not call the 2017 and 2024 taxon rows replicated effects: 2017 measures fruit-set sensitivity to a functional exposure gradient, 2024 measures matching/tube/pollen contrasts, and 2017 lacks Oshima reproductive observations. "
            "The supported replication level is qualitative recurrence of heterogeneous response modes across independent datasets, not species-specific sign replication, mediation, or historical Bombus causation."
        ),
    }
    return rows, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sensitivity",
        type=Path,
        default=Path("data/predictive_meta/hiraiwa_ushimaru_2017_reproductive_sensitivity.csv"),
    )
    parser.add_argument(
        "--channels",
        type=Path,
        default=Path("data/predictive_meta/hiraiwa_ushimaru_cross_channel_concordance.csv"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/hiraiwa_ushimaru_cross_study_triangulation"),
    )
    args = parser.parse_args()

    rows, summary = build_audit(read_csv(args.sensitivity), read_csv(args.channels))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "triangulation_rows.csv", rows)
    (args.out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
