from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FROZEN_LEDGER = ROOT / "data/design/chapter2_external_prediction_admission_ledger_20260828.csv"
EXTENSION_LEDGER = ROOT / "data/design/chapter2_world_breadth_extension_20260902.csv"
PROCESS_LEDGER = ROOT / "data/design/chapter2_world_process_deepening_20260904.csv"
DEFAULT_OUTPUT = ROOT / "data/results/chapter2_world_process_deepening_audit_20260904.json"


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_audit() -> dict:
    frozen = _read_rows(FROZEN_LEDGER)
    extension = _read_rows(EXTENSION_LEDGER)
    packages = _read_rows(PROCESS_LEDGER)

    if len(frozen) != 25:
        raise RuntimeError(f"frozen identifiability denominator changed: {len(frozen)}")
    if len(extension) != 14:
        raise RuntimeError(f"post-freeze exact-group denominator changed: {len(extension)}")
    if len(packages) != 3:
        raise RuntimeError(f"process-deepening package count changed: expected 3, got {len(packages)}")

    known_groups = {row["geographic_overlap_group"] for row in frozen} | {
        row["geographic_overlap_group"] for row in extension
    }
    package_ids = [row["package_id"] for row in packages]
    if len(package_ids) != len(set(package_ids)):
        raise RuntimeError("duplicate process-deepening package IDs")
    if any(row["geographic_group"] not in known_groups for row in packages):
        unknown = sorted(row["geographic_group"] for row in packages if row["geographic_group"] not in known_groups)
        raise RuntimeError(f"process deepening silently introduced new geographic groups: {unknown}")
    if any(row["matched_single_transition_contract"] != "fail" for row in packages):
        raise RuntimeError("process deepening must not silently create a full matched transition contract")
    if any(row["changes_research_entry_or_geographic_denominator"].lower() != "false" for row in packages):
        raise RuntimeError("process deepening must not change research-entry or geographic denominators")
    if any(not row["source_references"].strip() or not row["source_verification"].strip() for row in packages):
        raise RuntimeError("every process package requires source references and verification state")

    stage_depth = {
        "mauritius_honeybee_bird_competition": "interaction_to_effectiveness_and_reproductive_performance",
        "ogasawara_honeybee_network_to_psychotria": "community_restructuring_to_pollen_transfer_and_fruit_set",
        "fiji_recent_bee_arrival_to_interaction_network": "arrival_to_distribution_and_interaction_network",
    }

    return {
        "schema_version": "1.0",
        "status": "source_verified_process_deepening_without_denominator_inflation",
        "frozen_boundaries": {
            "formal_identifiability_research_entries": 25,
            "post_freeze_exact_group_research_entries": 14,
            "formal_external_prediction_reopened": False,
            "frozen_measurement_fractions_recomputed": False,
        },
        "process_packages": {
            "count": len(packages),
            "geographic_groups": sorted({row["geographic_group"] for row in packages}),
            "matched_single_transition_contract_passes": 0,
            "changes_research_entry_or_geographic_denominator": False,
            "stage_depth": stage_depth,
        },
        "strongest_new_resolution": {
            "mauritius": "introduced honeybee visitation and nectar depletion plus experimental comparative pollination efficiency",
            "ogasawara": "island-scale honeybee dominance/spread plus focal honeybee-mediated asymmetric pollen transfer and fruit set",
            "fiji": "recent bee-arrival chronology plus contemporary introduced-versus-native bee interaction structure",
        },
        "claim_boundary": (
            "These packages deepen mechanisms inside geographic systems already counted elsewhere. "
            "They are not new independent systems, do not alter the 39-entry/34-label descriptive breadth counts, "
            "and do not change the frozen 0/25 full-contract or not_evaluable external-prediction conclusions."
        ),
    }


def write_audit(output: Path = DEFAULT_OUTPUT) -> Path:
    payload = build_audit()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(write_audit())
