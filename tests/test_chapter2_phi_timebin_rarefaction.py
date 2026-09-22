from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_chapter2_phi_timebin_rarefaction.py"
PLAN = ROOT / "data/design/chapter2_natural_regime_analysis_plan_20260913.json"

spec = importlib.util.spec_from_file_location("phi_rarefaction", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _write_fixture(path: Path) -> None:
    sources = [
        ("s1", "a1", "x1"),
        ("s2", "a2", "x2"),
        ("s3", "a3", "x3"),
    ]
    rows = []
    for s_index, (source, arch, system) in enumerate(sources):
        for t in range(8):
            values = {
                "p1": 1 + t + s_index,
                "p2": 8 - t + s_index,
                "p3": 2 + ((t + s_index) % 3),
                "p4": 1 + ((2 * t + s_index) % 5),
            }
            for partner, value in values.items():
                rows.append({
                    "source_study_id": source,
                    "archipelago_id": arch,
                    "system_id": system,
                    "time_bin": f"t{t}",
                    "partner_id": partner,
                    "value": value,
                    "effort": 1.0,
                })
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "source_study_id", "archipelago_id", "system_id",
            "time_bin", "partner_id", "value", "effort",
        ])
        writer.writeheader()
        writer.writerows(rows)


def _freeze(tmp_path: Path) -> Path:
    payload = {
        "status": "frozen_before_execution",
        "target_time_bins": 6,
        "rarefaction_replicates": 30,
        "seed": 20260922,
        "expected_systems": 3,
        "admitted_sources": ["s1", "s2", "s3"],
        "interpretation_boundary": "fixture",
    }
    path = tmp_path / "freeze.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_phi_rarefaction_is_deterministic_and_uses_six_bins(tmp_path: Path) -> None:
    input_path = tmp_path / "canonical.csv"
    _write_fixture(input_path)
    freeze = _freeze(tmp_path)

    first = module.run([input_path], freeze_path=freeze, plan_path=PLAN)
    second = module.run([input_path], freeze_path=freeze, plan_path=PLAN)

    assert first == second
    assert first["target_time_bins"] == 6
    assert first["valid_iterations"] == 30
    assert first["invalid_iterations"] == 0
    assert len(first["per_system"]) == 3
    assert all(row["original_time_bins"] == 8 for row in first["per_system"])


def test_phi_only_keeps_full_breadth_definition(tmp_path: Path) -> None:
    input_path = tmp_path / "canonical.csv"
    _write_fixture(input_path)
    freeze = _freeze(tmp_path)
    result = module.run([input_path], freeze_path=freeze, plan_path=PLAN)

    assert "dispersion_criteria_pass_fraction" in result["phi_only_primary"]
    assert "dispersion_criteria_pass_fraction" in result["joint_coordinate_secondary"]
    assert set(result["phi_only_primary"]["leave_one_source_out_pass_fraction"]) == {
        "s1", "s2", "s3"
    }
