"""Validate the cross-lineage regime-transition response registry."""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY = HERE.parent / "data" / "predictive_meta" / "regime_transition_registry.csv"

REQUIRED = {
    "record_id",
    "lineage_id",
    "taxon",
    "analysis_role",
    "dependency_class",
    "response_domain",
    "response_family",
    "response_type",
    "observation_unit",
    "source_status",
    "regime_coverage",
    "eligible_for_shape_test",
    "allowed_shape_models",
    "boundary",
}
VALID_ROLES = {"calibration", "positive_holdout", "negative_control", "context", "pending"}
VALID_DEPENDENCY = {"specialist", "generalist", "alternative_guild", "unknown"}
VALID_DOMAINS = {"trait_state", "mating_system", "interaction", "occupancy"}
VALID_TYPES = {"continuous", "proportion", "binary", "ordinal", "multistate", "occupancy", "pending"}
VALID_MODELS = {"none", "cline", "first_step", "second_step", "two_step", "environment_history"}
ELIGIBLE_SOURCE = {"source_locked", "full_text_verified", "c_rank_blinded"}
THREE_REGIMES = {"large_bombus", "ardens", "no_bombus"}


def load_registry(path: Path = REGISTRY) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED.difference(reader.fieldnames or ())
        if missing:
            raise ValueError("registry missing columns: " + ", ".join(sorted(missing)))
        return list(reader)


def validate(path: Path = REGISTRY) -> dict[str, int]:
    rows = load_registry(path)
    if not rows:
        raise ValueError("regime-transition registry is empty")

    ids = [row["record_id"].strip() for row in rows]
    if not all(ids) or len(ids) != len(set(ids)):
        raise ValueError("record_id values must be non-empty and unique")

    for row in rows:
        record = row["record_id"]
        if row["analysis_role"] not in VALID_ROLES:
            raise ValueError(f"{record}: invalid analysis_role")
        if row["dependency_class"] not in VALID_DEPENDENCY:
            raise ValueError(f"{record}: invalid dependency_class")
        if row["response_domain"] not in VALID_DOMAINS:
            raise ValueError(f"{record}: invalid response_domain")
        if row["response_type"] not in VALID_TYPES:
            raise ValueError(f"{record}: invalid response_type")
        if row["eligible_for_shape_test"] not in {"yes", "no"}:
            raise ValueError(f"{record}: eligible_for_shape_test must be yes or no")

        models = {value for value in row["allowed_shape_models"].split("|") if value}
        unknown = models.difference(VALID_MODELS)
        if unknown:
            raise ValueError(f"{record}: unknown shape models {sorted(unknown)}")

        if row["eligible_for_shape_test"] == "yes":
            regimes = {value for value in row["regime_coverage"].split("|") if value}
            if not THREE_REGIMES.issubset(regimes):
                raise ValueError(f"{record}: eligible records require all three regimes")
            if row["source_status"] not in ELIGIBLE_SOURCE:
                raise ValueError(f"{record}: source status is not eligible for shape testing")
            if models != VALID_MODELS:
                raise ValueError(f"{record}: eligible records must allow the full competing-model set")
        elif models:
            raise ValueError(f"{record}: ineligible records must not preselect shape models")

        if row["response_domain"] == "occupancy" and row["response_type"] != "occupancy":
            raise ValueError(f"{record}: occupancy domain requires occupancy response_type")

        if (
            row["taxon"] == "Campanula microdonta"
            and row["response_family"] == "visible_signal"
        ):
            raise ValueError("unfinished Campanula visible-signal records must remain outside the registry")

    calibration = [row for row in rows if row["analysis_role"] == "calibration"]
    calibration_families = {row["response_family"] for row in calibration}
    expected = {"floral_size", "outcrossing", "autonomous_assurance"}
    if calibration_families != expected:
        raise ValueError(
            f"calibration must contain exactly the three adopted families: {sorted(expected)}"
        )

    return {
        "records": len(rows),
        "eligible": sum(row["eligible_for_shape_test"] == "yes" for row in rows),
        "calibration": len(calibration),
        "negative_controls": sum(row["analysis_role"] == "negative_control" for row in rows),
        "pending": sum(row["analysis_role"] == "pending" for row in rows),
    }


def main() -> None:
    summary = validate()
    print("OK: regime-transition registry", summary)


if __name__ == "__main__":
    main()
