"""Semantic lock for the Campanula channel-shape and holdout contracts.

The lock is intentionally semantic rather than a bare file checksum.  A changed
wording is allowed, but the versioned empirical shapes, evidence status and
scenario-facing directions cannot drift without changing this module and its
tests in the same reviewed commit.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

CONTRACT_VERSION = "1.0.0"
TRANSITIONS = ("large_to_ardens", "ardens_to_no_bombus")

SHAPE_FIELDS = (
    "contract_version",
    "scope",
    "analysis_group",
    "trait_family",
    "evidence_status",
    "empirical_shape",
    "large_to_ardens",
    "ardens_to_no_bombus",
    "prospective_role",
    "boundary",
)

EXPECTED_SHAPES = {
    ("campanula_calibration", "specialist", "floral_size"): {
        "evidence_status": "source_locked",
        "empirical_shape": "continuous_erosion",
        "large_to_ardens": "decrease",
        "ardens_to_no_bombus": "decrease|flat",
        "prospective_role": "calibration_nonunique",
    },
    ("campanula_calibration", "specialist", "outcrossing"): {
        "evidence_status": "source_locked",
        "empirical_shape": "continuous_erosion",
        "large_to_ardens": "flat|decrease",
        "ardens_to_no_bombus": "decrease",
        "prospective_role": "calibration_informative",
    },
    ("campanula_calibration", "specialist", "autonomous_assurance"): {
        "evidence_status": "source_locked",
        "empirical_shape": "second_transition_step",
        "large_to_ardens": "flat",
        "ardens_to_no_bombus": "increase",
        "prospective_role": "calibration_informative",
    },
    ("campanula_calibration", "specialist", "visible_signal"): {
        "evidence_status": "blocked_unmeasured",
        "empirical_shape": "not_estimated",
        "large_to_ardens": "not_scored",
        "ardens_to_no_bombus": "not_scored",
        "prospective_role": "prospective_only",
    },
    ("cross_lineage_prediction", "specialist", "visible_signal"): {
        "evidence_status": "theory_locked",
        "empirical_shape": "late_decline_prediction",
        "large_to_ardens": "flat|decrease",
        "ardens_to_no_bombus": "decrease",
        "prospective_role": "positive_holdout",
    },
    ("negative_control", "generalist", "visible_signal"): {
        "evidence_status": "c_rank_one_lineage",
        "empirical_shape": "flat_control",
        "large_to_ardens": "flat",
        "ardens_to_no_bombus": "flat",
        "prospective_role": "negative_control_holdout",
    },
}


@dataclass(frozen=True)
class ContractValidation:
    version: str
    shape_rows: int
    scenario_rows_checked: int
    image_rows_checked: int


def _read_csv(path: str | Path, required: Iterable[str]) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"contract file is empty: {path}")
    missing = sorted(set(required).difference(rows[0]))
    if missing:
        raise ValueError(f"{path}: missing columns: {', '.join(missing)}")
    return [{key: str(value or '').strip() for key, value in row.items()} for row in rows]


def _directions(value: str) -> frozenset[str]:
    return frozenset(item.strip() for item in value.split("|") if item.strip())


def load_and_validate_shapes(path: str | Path) -> dict[tuple[str, str, str], dict[str, str]]:
    rows = _read_csv(path, SHAPE_FIELDS)
    keyed: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        if row["contract_version"] != CONTRACT_VERSION:
            raise ValueError(
                f"{path}: expected contract_version {CONTRACT_VERSION}, "
                f"found {row['contract_version']}"
            )
        key = (row["scope"], row["analysis_group"], row["trait_family"])
        if key in keyed:
            raise ValueError(f"{path}: duplicate shape row {key}")
        keyed[key] = row
    if set(keyed) != set(EXPECTED_SHAPES):
        missing = sorted(set(EXPECTED_SHAPES).difference(keyed))
        extra = sorted(set(keyed).difference(EXPECTED_SHAPES))
        raise ValueError(f"{path}: shape-key drift; missing={missing}, extra={extra}")
    for key, expected in EXPECTED_SHAPES.items():
        row = keyed[key]
        for field, value in expected.items():
            if row[field] != value:
                raise ValueError(
                    f"{path}: locked value drift for {key} {field}: "
                    f"expected {value!r}, found {row[field]!r}"
                )
        if not row["boundary"]:
            raise ValueError(f"{path}: boundary is required for {key}")
    return keyed


def _scenario_index(path: str | Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    rows = _read_csv(
        path,
        (
            "scenario",
            "analysis_group",
            "trait_family",
            "transition",
            "allowed_directions",
            "minimum_abs_delta",
            "rule_status",
            "interpretation",
            "boundary",
        ),
    )
    return {
        (row["scenario"], row["analysis_group"], row["trait_family"], row["transition"]): row
        for row in rows
    }


def _image_index(path: str | Path) -> dict[tuple[str, str, str], dict[str, str]]:
    rows = _read_csv(
        path,
        (
            "scenario",
            "analysis_group",
            "feature_id",
            "transition",
            "allowed_directions",
            "minimum_abs_delta",
            "rule_status",
            "interpretation",
            "boundary",
        ),
    )
    return {
        (row["scenario"], row["analysis_group"], row["transition"]): row
        for row in rows
        if row["feature_id"] == "visual_salience_v1"
    }


def validate_contract_bundle(
    shape_path: str | Path,
    scenario_path: str | Path,
    image_path: str | Path,
) -> ContractValidation:
    shapes = load_and_validate_shapes(shape_path)
    scenarios = _scenario_index(scenario_path)
    images = _image_index(image_path)

    scenario_checks = 0
    for trait in ("floral_size", "outcrossing", "autonomous_assurance"):
        shape = shapes[("campanula_calibration", "specialist", trait)]
        for transition in TRANSITIONS:
            key = ("ardens_replacement_loss", "specialist", trait, transition)
            if key not in scenarios:
                raise ValueError(f"{scenario_path}: missing locked scenario row {key}")
            row = scenarios[key]
            if row["rule_status"] != "active":
                raise ValueError(f"{scenario_path}: locked scenario row is not active: {key}")
            if _directions(row["allowed_directions"]) != _directions(shape[transition]):
                raise ValueError(
                    f"{scenario_path}: directions disagree with channel-shape v1 for {key}"
                )
            scenario_checks += 1

    image_checks = 0
    for group, scope in (
        ("specialist", "cross_lineage_prediction"),
        ("generalist", "negative_control"),
    ):
        shape = shapes[(scope, group, "visible_signal")]
        for transition in TRANSITIONS:
            scenario_key = ("ardens_replacement_loss", group, "visible_signal", transition)
            image_key = ("ardens_replacement_loss", group, transition)
            if scenario_key not in scenarios or image_key not in images:
                raise ValueError(f"missing visible-signal contract row: {scenario_key}")
            expected = _directions(shape[transition])
            if _directions(scenarios[scenario_key]["allowed_directions"]) != expected:
                raise ValueError(f"scenario visible-signal directions drifted: {scenario_key}")
            if _directions(images[image_key]["allowed_directions"]) != expected:
                raise ValueError(f"image-proxy directions drifted: {image_key}")
            image_checks += 1

    environment_rows = [
        row for key, row in scenarios.items() if key[0] == "environment_only"
    ]
    if not environment_rows or any(row["rule_status"] != "not_identified" for row in environment_rows):
        raise ValueError("environment_only must remain unranked until its explicit likelihood exists")

    return ContractValidation(
        version=CONTRACT_VERSION,
        shape_rows=len(shapes),
        scenario_rows_checked=scenario_checks,
        image_rows_checked=image_checks,
    )
