from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/analyze_chapter2_natural_regime_coordinates.py"
PLAN = ROOT / "data/design/chapter2_natural_regime_analysis_plan_20260913.json"

spec = importlib.util.spec_from_file_location("natural_regime", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_hill_d1_equal_partner_totals_is_partner_count() -> None:
    values = np.asarray([21.0, 21.0, 21.0])
    assert module._hill_d1(values) == pytest.approx(3.0, rel=1e-12)


def test_phi_matches_definition() -> None:
    matrix = np.asarray(
        [
            [1.0, 1.0, 6.0],
            [2.0, 2.0, 5.0],
            [3.0, 3.0, 4.0],
            [4.0, 4.0, 3.0],
            [5.0, 5.0, 2.0],
            [6.0, 6.0, 1.0],
        ]
    )
    observed, eligible = module._phi(matrix)
    sds = np.std(matrix, axis=0, ddof=1)
    expected = np.var(matrix.sum(axis=1), ddof=1) / np.sum(sds) ** 2
    assert eligible == [0, 1, 2]
    assert observed == pytest.approx(expected, rel=1e-12)


def _write_fixture_csv(path: Path) -> None:
    rows = []
    vectors = {
        "a": [1, 2, 3, 4, 5, 6],
        "b": [1, 2, 3, 4, 5, 6],
        "c": [6, 5, 4, 3, 2, 1],
    }
    for time_index in range(6):
        for partner, series in vectors.items():
            rows.append(
                {
                    "source_study_id": "source1",
                    "archipelago_id": "arch1",
                    "system_id": "system1",
                    "time_bin": f"t{time_index + 1}",
                    "partner_id": partner,
                    "value": series[time_index] * 2,
                    "effort": 2,
                }
            )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(module.REQUIRED_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def _small_plan(tmp_path: Path) -> Path:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    plan["bootstrap"]["replicates"] = 80
    plan["bootstrap"]["minimum_valid_phi_replicates"] = 50
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    return path


def test_run_recovers_effort_standardized_coordinates_deterministically(tmp_path: Path) -> None:
    csv_path = tmp_path / "input.csv"
    _write_fixture_csv(csv_path)
    plan_path = _small_plan(tmp_path)

    first = module.run(csv_path, plan_path)
    second = module.run(csv_path, plan_path)
    row = first["systems"][0]

    assert row["breadth_D1"] == pytest.approx(3.0, rel=1e-12)
    assert row["observed_partner_richness"] == 3
    assert row["time_bins"] == 6
    assert row["eligible_synchrony_partners"] == 3
    assert first["systems"] == second["systems"]
    assert first["route_decision"]["route"] == second["route_decision"]["route"] == "fallback_Oikos_plus_EL"
    assert first["route_decision"]["summary"]["D1_q90_q10_ratio"] == second["route_decision"]["summary"]["D1_q90_q10_ratio"]
    assert first["route_decision"]["summary"]["phi_q90_q10_span"] == second["route_decision"]["summary"]["phi_q90_q10_span"]


def test_route_requires_three_sources_for_nee() -> None:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    rows = []
    for i in range(12):
        rows.append(
            {
                "source_study_id": "source1" if i < 6 else "source2",
                "archipelago_id": "arch1" if i < 6 else "arch2",
                "system_id": f"s{i}",
                "breadth_D1": 1.0 + i,
                "phi": 0.05 + 0.04 * i,
            }
        )
    decision = module.classify_route(rows, plan)
    assert decision["route"] == "Ecology_Letters_combined"
    assert decision["nee_count_criteria_pass"] is False


def test_invalid_nonpositive_effort_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(module.REQUIRED_COLUMNS))
        writer.writeheader()
        writer.writerow(
            {
                "source_study_id": "s",
                "archipelago_id": "a",
                "system_id": "x",
                "time_bin": "t1",
                "partner_id": "p",
                "value": 1,
                "effort": 0,
            }
        )
    with pytest.raises(ValueError, match="invalid effort"):
        module.load_canonical_csv(path)
