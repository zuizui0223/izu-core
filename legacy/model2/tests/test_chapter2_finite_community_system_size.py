from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_finite_community_system_size_freeze_20260908.json"
SUMMARY = ROOT / "data/results/chapter2_finite_community_system_size_summary_20260908.json"


def test_system_size_design_was_fixed_before_execution():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "fixed_before_execution"
    assert design["parent_main_commit"] == "35d93436b8bd929b6767965c02c8f6c4cfb500dc"
    assert design["system_size_scaling"]["copy_counts"] == [1, 2, 4, 8, 16]
    assert design["seed_ensemble"]["values"] == [20260826, 20250101, 20260833, 20260827, 999983, 12345]
    assert design["baseline"]["trait_adjustment"] == 0.0
    assert design["decision_rules"]["no_retuning"] is True
    assert design["decision_rules"]["no_seed_selection"] is True


def test_ci_verified_system_size_summary_preserves_claim_boundary():
    result = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert result["status"] == "verified_against_ci_artifact_run_2429"
    by_k = {row["copies"]: row for row in result["scale_summary"]}
    assert by_k[1]["mixed_sign_count_range"] == [64, 75]
    assert by_k[16]["mixed_sign_count_range"] == [44, 60]
    assert by_k[1]["island_empty_fraction_range"] == [0.07291666666666667, 0.13541666666666666]
    assert by_k[16]["island_empty_fraction_range"] == [0.0, 0.0]
    assert by_k[16]["island_final_count_cv_range"][1] < by_k[1]["island_final_count_cv_range"][0]
    assert by_k[16]["community_realization_fraction_range"][1] < by_k[1]["community_realization_fraction_range"][0]
    assert by_k[16]["nonadditivity_fraction_range"][0] > 0.5
    boundary = result["claim_boundary"].lower()
    assert "not an exact mean-field limit" in boundary
    assert "not a pde/lna validation" in boundary
