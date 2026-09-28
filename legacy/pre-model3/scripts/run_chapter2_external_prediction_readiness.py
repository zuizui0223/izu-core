from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_external_prediction_challenge_freeze_20260828.json"
LEDGER = ROOT / "data/design/chapter2_external_prediction_admission_ledger_20260828.csv"
SOURCE_AUDIT = ROOT / "docs/CHAPTER2_EXTERNAL_PREDICTION_SOURCE_AUDIT_20260828.md"
OUT = ROOT / "data/results/chapter2_external_prediction_readiness_frozen_20260828.json"

AVAILABILITY_COLUMNS = (
    "source_functional_state",
    "partner_loss",
    "partner_arrival_replacement",
    "community_functional_shift",
    "richness_fd_change",
    "local_filtering",
    "reproductive_assurance",
    "response_outcome",
)
REQUIRED_COLUMNS = (
    "layer",
    "system_id",
    "system_name",
    "geographic_overlap_group",
    "response_family",
    *AVAILABILITY_COLUMNS,
    "chapter2_target_contract",
    "prediction_chronology",
    "admission_class",
    "anchor_selection_chronology",
    "source_reference",
    "evidence_note",
)
AVAILABILITY = {
    "direct_measurement",
    "source_derived_proxy",
    "unavailable",
    "not_applicable",
}
ADMISSION_CLASSES = {
    "admissible_prospective_like_challenge",
    "retrospective_explanatory_test_only",
    "reality_boundary_only",
    "source_gated_unusable",
}
CHRONOLOGY = {
    "pre_target_exact_target_frozen",
    "published_outcome_known_or_mapping_post_outcome",
    "no_chapter2_target",
    "source_unresolved",
}
ANCHOR_CHRONOLOGY = {
    "post_outcome_not_prespecified",
    "not_applicable",
}


def canonical_text_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_ledger(path: Path = LEDGER) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("admission ledger has no header")
        missing = [name for name in REQUIRED_COLUMNS if name not in reader.fieldnames]
        if missing:
            raise ValueError(f"admission ledger missing columns: {missing}")
        rows = list(reader)
    return rows


def is_available(value: str) -> bool:
    return value in {"direct_measurement", "source_derived_proxy"}


def validate_ledger(rows: list[dict[str, str]]) -> None:
    if len(rows) != 25:
        raise ValueError(f"expected 25 source-audited research entries, observed {len(rows)}")
    ids = [row["system_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("system_id values must be unique")
    layer_counts = Counter(row["layer"] for row in rows)
    if layer_counts != {
        "strict": 13,
        "additional": 6,
        "model_development": 6,
    }:
        raise ValueError(f"unexpected layer counts: {dict(layer_counts)}")

    for row in rows:
        for column in AVAILABILITY_COLUMNS:
            if row[column] not in AVAILABILITY:
                raise ValueError(
                    f"{row['system_id']} has invalid {column}: {row[column]}"
                )
        if row["admission_class"] not in ADMISSION_CLASSES:
            raise ValueError(
                f"{row['system_id']} has invalid admission_class: {row['admission_class']}"
            )
        if row["prediction_chronology"] not in CHRONOLOGY:
            raise ValueError(
                f"{row['system_id']} has invalid prediction_chronology: "
                f"{row['prediction_chronology']}"
            )
        if row["anchor_selection_chronology"] not in ANCHOR_CHRONOLOGY:
            raise ValueError(
                f"{row['system_id']} has invalid anchor_selection_chronology: "
                f"{row['anchor_selection_chronology']}"
            )
        if row["chapter2_target_contract"] not in {"pass", "fail"}:
            raise ValueError(
                f"{row['system_id']} has invalid chapter2_target_contract: "
                f"{row['chapter2_target_contract']}"
            )
        if row["chapter2_target_contract"] == "pass" and not is_available(
            row["response_outcome"]
        ):
            raise ValueError(
                f"{row['system_id']} passes target contract without a response outcome"
            )
        if row["admission_class"] == "admissible_prospective_like_challenge":
            if row["prediction_chronology"] != "pre_target_exact_target_frozen":
                raise ValueError(
                    f"{row['system_id']} is prospective-like without pre-target chronology"
                )
            if row["chapter2_target_contract"] != "pass":
                raise ValueError(
                    f"{row['system_id']} is prospective-like but fails the target contract"
                )


def hypothesis_flags(row: dict[str, str]) -> dict[str, bool]:
    target = row["chapter2_target_contract"] == "pass" and is_available(
        row["response_outcome"]
    )
    h1 = target and is_available(row["source_functional_state"])
    h2 = (
        target
        and is_available(row["partner_loss"])
        and is_available(row["partner_arrival_replacement"])
    )
    h3 = (
        target
        and is_available(row["source_functional_state"])
        and is_available(row["community_functional_shift"])
    )
    h4 = h3 and is_available(row["local_filtering"])
    return {"H0": target, "H1": h1, "H2": h2, "H3": h3, "H4": h4}


def build() -> dict:
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    if design["status"] != "fixed_before_new_readiness_evaluation":
        raise ValueError("external-prediction design is not in its frozen pre-evaluation state")
    rows = load_ledger()
    validate_ledger(rows)

    flags = {row["system_id"]: hypothesis_flags(row) for row in rows}
    predictor_counts = {
        column: dict(Counter(row[column] for row in rows))
        for column in AVAILABILITY_COLUMNS
    }
    hypothesis_counts = {
        hypothesis: sum(system_flags[hypothesis] for system_flags in flags.values())
        for hypothesis in ("H0", "H1", "H2", "H3", "H4")
    }

    prospective_complete = []
    retrospective_complete = []
    for row in rows:
        complete_h0_h3 = all(flags[row["system_id"]][name] for name in ("H0", "H1", "H2", "H3"))
        if not complete_h0_h3:
            continue
        if row["admission_class"] == "admissible_prospective_like_challenge":
            prospective_complete.append(row)
        elif row["admission_class"] == "retrospective_explanatory_test_only":
            retrospective_complete.append(row)

    by_family: dict[str, set[str]] = defaultdict(set)
    for row in prospective_complete:
        by_family[row["response_family"]].add(row["geographic_overlap_group"])
    family_cluster_counts = {
        family: len(clusters) for family, clusters in sorted(by_family.items())
    }
    maximum_family_clusters = max(family_cluster_counts.values(), default=0)
    minimum_clusters = design["formal_evaluation_gate"][
        "minimum_independent_system_clusters"
    ]
    formal_gate_passed = maximum_family_clusters >= minimum_clusters

    if formal_gate_passed:
        decision = "pending_formal_model_evaluation"
        maximum_level = "Level 2 pending Level 3 evaluation"
        route = "do_not_claim_upgrade_until_frozen_holdout_evaluation_is_complete"
    else:
        decision = "C_formal_external_prediction_not_supported_by_current_world_data"
        maximum_level = "Level 2"
        route = "retain_current_Journal_of_Ecology_or_Oikos_conditional_geometry_route"

    anchor_rows = [
        row for row in rows if row["anchor_selection_chronology"] != "not_applicable"
    ]
    if len(anchor_rows) != 1 or anchor_rows[0]["system_id"] != "izu_hiraiwa_ushimaru":
        raise ValueError("Izu anchor-selection chronology must be recorded exactly once")

    return {
        "schema_version": "1.0",
        "analysis": "chapter2_external_prediction_readiness",
        "status": "frozen_complete_20260828",
        "input_identity": {
            str(DESIGN.relative_to(ROOT)).replace("\\", "/"): {
                "canonical_text_sha256": canonical_text_sha256(DESIGN)
            },
            str(LEDGER.relative_to(ROOT)).replace("\\", "/"): {
                "canonical_text_sha256": canonical_text_sha256(LEDGER)
            },
            str(SOURCE_AUDIT.relative_to(ROOT)).replace("\\", "/"): {
                "canonical_text_sha256": canonical_text_sha256(SOURCE_AUDIT)
            },
        },
        "universe": {
            "research_entries": len(rows),
            "layer_counts": dict(Counter(row["layer"] for row in rows)),
            "geographic_overlap_groups": len(
                {row["geographic_overlap_group"] for row in rows}
            ),
            "independence_boundary": "Geographic overlap groups are de-duplication labels, not an estimate of exchangeable archipelago n.",
        },
        "admission": {
            "class_counts": dict(Counter(row["admission_class"] for row in rows)),
            "target_contract_pass_count": sum(
                row["chapter2_target_contract"] == "pass" for row in rows
            ),
            "predictor_availability_counts": predictor_counts,
            "hypothesis_evaluable_entry_counts": hypothesis_counts,
            "prospective_like_complete_H0_to_H3_entry_count": len(
                prospective_complete
            ),
            "retrospective_complete_H0_to_H3_entry_count": len(
                retrospective_complete
            ),
            "prospective_like_complete_response_family_cluster_counts": family_cluster_counts,
        },
        "formal_evaluation_gate": {
            "minimum_independent_system_clusters": minimum_clusters,
            "maximum_same_response_family_prospective_like_clusters": maximum_family_clusters,
            "passed": formal_gate_passed,
            "H0_to_H4_model_comparison": (
                "not_evaluable" if not formal_gate_passed else "pending"
            ),
            "leave_one_system_out": (
                "not_evaluable" if not formal_gate_passed else "pending"
            ),
            "leave_one_archipelago_out": (
                "not_evaluable" if not formal_gate_passed else "pending"
            ),
            "permutation_test": (
                "not_evaluable" if not formal_gate_passed else "pending"
            ),
            "reason": (
                "No response family has the frozen minimum of four geographically de-duplicated, prospective-like entries with a common Chapter 2 target and complete H0-H3 inputs."
                if not formal_gate_passed
                else "The source-admission floor is met; performance evaluation is still required before any Level 3 claim."
            ),
        },
        "control_axis_decision": {
            "synthetic_axes_defined": ["T", "D0", "C", "F"],
            "assurance_role": "downstream magnitude modifier, excluded from sign-regime rescue",
            "empirical_projection_ready": formal_gate_passed,
            "boundary": "The four axes are model-derived coordinates. Defining them does not make an empirical system projectable when source-native measurements or mappings are absent.",
        },
        "izu_anchor_selection": {
            "formal_preoutcome_selection_score_available": False,
            "chronology": anchor_rows[0]["anchor_selection_chronology"],
            "allowed_role": "data-depth focal triangulation selected transparently after the comparative programme, not an outcome-independent winner of a global score",
            "chapter3_data_used_for_chapter2_validation": False,
        },
        "decision": decision,
        "maximum_supported_claim_level": maximum_level,
        "journal_route": route,
        "figure_concept": {
            "panel_A": "General response phase diagram on model-derived turnover imbalance T and source/community matching displacement, with local filtering shown as branch-transition arrows rather than an empirical threshold.",
            "panel_B": "External-system projection matrix showing measured, proxy and missing inputs; non-projectable systems remain outside the phase plane rather than being assigned from their outcomes.",
            "status": "design_only_because_formal_external_projection_gate_failed",
        },
        "claim_boundary": "This is a frozen data-readiness and identifiability result, not a failed fitted model. No response classifier was fitted, no system was removed or replaced by fit, and no synthetic frequency is interpreted as natural prevalence.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "research_entries": payload["universe"]["research_entries"],
                "formal_gate_passed": payload["formal_evaluation_gate"]["passed"],
                "decision": payload["decision"],
                "maximum_supported_claim_level": payload[
                    "maximum_supported_claim_level"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
