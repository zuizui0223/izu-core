from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from scripts.audit_finite_n_gaussian_mean_field import pmf_moments, pooled_count_summary, terminal_count_pmf
from scripts.run_response_geometry_parameter_robustness import BASE

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/results/finite_n_gaussian_mean_field_summary_20260908.json"


def test_exact_count_process_matches_ci_verified_summary():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    mainland = pmf_moments(terminal_count_pmf(BASE.mainland, steps=BASE.steps))
    island = pmf_moments(terminal_count_pmf(BASE.island, steps=BASE.steps))
    assert mainland["mean"] == pytest.approx(summary["exact_single_copy_count_process"]["mainland_like"]["mean"])
    assert mainland["cv"] == pytest.approx(summary["exact_single_copy_count_process"]["mainland_like"]["cv"])
    assert island["mean"] == pytest.approx(summary["exact_single_copy_count_process"]["island_like"]["mean"])
    assert island["empty_probability"] == pytest.approx(
        summary["exact_single_copy_count_process"]["island_like"]["empty_probability"]
    )


def test_pooled_count_cv_has_exact_inverse_sqrt_k_scaling():
    island_pmf = terminal_count_pmf(BASE.island, steps=BASE.steps)
    one = pmf_moments(island_pmf)
    for k in (2, 4, 8, 16, 64):
        pooled = pooled_count_summary(island_pmf, k)
        assert pooled["cv"] == pytest.approx(one["cv"] / math.sqrt(k), rel=1e-12, abs=1e-12)
        assert pooled["empty_probability"] == pytest.approx(one["empty_probability"] ** k)


def test_mean_field_limit_is_single_signed_and_gaussian_converges_to_abm():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    mean_field = summary["mean_field"]
    assert mean_field["classification"] == "all_positive"
    assert mean_field["minimum_kernel_contrast"] > 0
    errors = [row["absolute_error"] for row in summary["gaussian_vs_abm_mixed_probability"]]
    assert errors == sorted(errors, reverse=True)
    assert errors[-1] < 0.01
    k16 = summary["gaussian_vs_abm_mixed_probability"][-1]
    assert k16["k"] == 16
    assert abs(k16["gaussian"] - k16["abm"]) < 0.01


def test_gaussian_extrapolation_is_bounded_as_approximation():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    rows = {row["k"]: row for row in summary["gaussian_extrapolation"]}
    assert rows[512]["mixed"] < 0.01
    assert rows[1024]["all_positive"] > 0.999
    boundary = summary["claim_boundary"].lower()
    assert "not an exact fokker-planck" in boundary
    assert "not a natural abundance estimate" in boundary
