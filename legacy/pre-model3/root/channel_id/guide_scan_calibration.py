"""Validation and descriptive summaries for the measured Campanula guide channel.

The source is a companion-repository table of island means from 300-DPI
flattened-corolla scans.  This module promotes that table only to focal
calibration evidence.  It does not estimate a causal pollinator effect or turn
individual corollas into independent evolutionary replicates.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

SOURCE_REPOSITORY = "zuizui0223/shimahotarubukuro"
SOURCE_COMMIT = "6343d152a743c240348c736baf5c65768c9b7020"
EXPECTED_VALUES = {
    "Oshima": ("ardens", 88, 28.39),
    "Toshima": ("no_bombus", 63, 5.27),
    "Niijima": ("no_bombus", 35, 12.15),
    "Shikinejima": ("no_bombus", 5, 2.00),
    "Kozushima": ("no_bombus", 18, 4.31),
}


@dataclass(frozen=True)
class GuideCalibrationSummary:
    ardens_island: str
    ardens_guide_cov_pct: float
    no_bombus_islands: tuple[str, ...]
    no_bombus_equal_island_mean_pct: float
    second_transition_delta_pct_points: float
    no_bombus_islands_below_ardens: int
    leave_one_island_out_deltas: tuple[float, ...]


def _read(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"empty guide table: {path}")
    return [{key: str(value or "").strip() for key, value in row.items()} for row in rows]


def load_guide_summary(path: str | Path) -> tuple[dict[str, object], ...]:
    rows = _read(path)
    required = {
        "source_repository", "source_commit", "source_path", "island",
        "pollinator_regime", "n_corolla", "guide_cov_pct_mean",
        "guide_present_frac", "degraded_frac", "evidence_status",
        "analysis_use", "boundary",
    }
    missing = sorted(required.difference(rows[0]))
    if missing:
        raise ValueError("guide summary missing columns: " + ", ".join(missing))
    if {row["island"] for row in rows} != set(EXPECTED_VALUES):
        raise ValueError("guide summary island set drifted")
    output: list[dict[str, object]] = []
    for row in rows:
        island = row["island"]
        expected_regime, expected_n, expected_value = EXPECTED_VALUES[island]
        if row["source_repository"] != SOURCE_REPOSITORY:
            raise ValueError(f"{island}: source repository drifted")
        if row["source_commit"] != SOURCE_COMMIT:
            raise ValueError(f"{island}: source commit drifted")
        if row["pollinator_regime"] != expected_regime:
            raise ValueError(f"{island}: pollinator regime drifted")
        n_corolla = int(row["n_corolla"])
        guide = float(row["guide_cov_pct_mean"])
        if n_corolla != expected_n or abs(guide - expected_value) > 1e-9:
            raise ValueError(f"{island}: source-locked n/value drifted")
        if row["evidence_status"] != "measured_scan_summary":
            raise ValueError(f"{island}: evidence status must remain measured_scan_summary")
        if row["analysis_use"] != "calibration":
            raise ValueError(f"{island}: scan summary cannot enter the holdout partition")
        if not row["boundary"]:
            raise ValueError(f"{island}: evidence boundary is required")
        output.append({
            **row,
            "n_corolla": n_corolla,
            "guide_cov_pct_mean": guide,
            "guide_present_frac": float(row["guide_present_frac"]),
            "degraded_frac": float(row["degraded_frac"]),
        })
    return tuple(sorted(output, key=lambda row: float(row["region_order"])))


def summarize_second_transition(rows: tuple[dict[str, object], ...]) -> GuideCalibrationSummary:
    ardens = [row for row in rows if row["pollinator_regime"] == "ardens"]
    no_bombus = [row for row in rows if row["pollinator_regime"] == "no_bombus"]
    if len(ardens) != 1 or len(no_bombus) < 3:
        raise ValueError("guide calibration requires one ardens and at least three no-Bombus islands")
    reference = float(ardens[0]["guide_cov_pct_mean"])
    values = [float(row["guide_cov_pct_mean"]) for row in no_bombus]
    focal_mean = mean(values)
    leave_one_out = tuple(
        mean(values[:index] + values[index + 1:]) - reference
        for index in range(len(values))
    )
    return GuideCalibrationSummary(
        ardens_island=str(ardens[0]["island"]),
        ardens_guide_cov_pct=reference,
        no_bombus_islands=tuple(str(row["island"]) for row in no_bombus),
        no_bombus_equal_island_mean_pct=focal_mean,
        second_transition_delta_pct_points=focal_mean - reference,
        no_bombus_islands_below_ardens=sum(value < reference for value in values),
        leave_one_island_out_deltas=leave_one_out,
    )


def validate_contract_v1_1(path: str | Path) -> None:
    rows = _read(path)
    visible = [
        row for row in rows
        if row.get("scope") == "campanula_calibration"
        and row.get("analysis_group") == "specialist"
        and row.get("trait_family") == "visible_signal"
    ]
    if len(visible) != 1:
        raise ValueError("v1.1 requires one focal visible-signal row")
    row = visible[0]
    expected = {
        "contract_version": "1.1.0",
        "evidence_status": "measured_scan_summary",
        "empirical_shape": "second_transition_decline",
        "large_to_ardens": "not_observed",
        "ardens_to_no_bombus": "decrease",
        "prospective_role": "calibration_informative",
    }
    for field, value in expected.items():
        if row.get(field) != value:
            raise ValueError(f"v1.1 visible-signal contract drifted: {field}")


def validate_observation_bridge(
    observation_path: str | Path,
    guide_rows: tuple[dict[str, object], ...],
) -> None:
    rows = _read(observation_path)
    guide_observations = [
        row for row in rows
        if row.get("analysis_partition") == "calibration"
        and row.get("lineage_id") == "campanula_microdonta"
        and row.get("trait_id") == "guide_cov_pct_mean"
        and row.get("trait_family") == "visible_signal"
    ]
    if len(guide_observations) != len(guide_rows):
        raise ValueError("calibration observation bridge must contain one row per guide island")
    by_locator = {row["source_locator"].rsplit(":", 1)[-1]: row for row in guide_observations}
    for source in guide_rows:
        island = str(source["island"])
        if island not in by_locator:
            raise ValueError(f"missing guide observation for {island}")
        observation = by_locator[island]
        if observation["pollinator_regime"] != source["pollinator_regime"]:
            raise ValueError(f"{island}: observation regime disagrees with guide summary")
        if abs(float(observation["value"]) - float(source["guide_cov_pct_mean"])) > 1e-9:
            raise ValueError(f"{island}: observation value disagrees with guide summary")
        if observation["evidence_tier"] != "measured_scan_summary":
            raise ValueError(f"{island}: observation evidence tier drifted")
