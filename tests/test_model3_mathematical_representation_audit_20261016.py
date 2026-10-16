"""Read-only mathematical-representation gates for the archived Model 3 work.

These tests independently check a few model identities and archive arithmetic.
They DO NOT numerically certify a full nonlinear PDE, SDE, or SPDE. Source
readouts are historical engineering diagnostics, not independent island cohorts.
"""
from __future__ import annotations

import ast
import json
from math import exp, isclose, pi
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data/results"
SOURCE = ROOT / "scripts/model3_island"


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_the_deterministic_genotype_engine_is_an_annual_map_not_a_pde_solver():
    tree = ast.parse((SOURCE / "density.py").read_text(encoding="utf-8"))
    funcs = {
        node.name: node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    assert "density_step" in funcs
    node = funcs["density_step"]
    # This is a one-step genotype-count transform and its reproductive ledger.
    returns = [
        n for n in ast.walk(node) if isinstance(n, ast.Return)
    ]
    assert returns
    assert any(isinstance(r.value, ast.Tuple) and len(r.value.elts) == 2
               for r in returns)
    record = _read(RESULTS / "model3_mutation_limit_closeout_20261004.json")
    assert record["full_model_status"] == "nonlinear_nonlocal_integro_difference_not_pure_pde"
    assert record["status"] == "mutation_component_has_reflected_diffusion_limit"


def test_replicator_ode_is_accurate_only_at_its_declared_fixed_support_scope():
    record = _read(RESULTS / "model3_pde_closeout_20261004.json")
    rows = record["rows"]
    assert len(rows) == 75
    summaries = {r["periods"]: r for r in record["summaries"]}
    assert set(summaries) == {60, 200, 800}
    for period, summary in summaries.items():
        subset = [r for r in rows if r["periods"] == period]
        assert len(subset) == summary["n"] == summary["sign_matches"] == 25
        assert all(r["sign_match"] for r in subset)
        errors = np.array([
            r["ode_mean"] - r["exact_mean"] for r in subset
        ])
        np.testing.assert_allclose(
            errors,
            [r["ode_vs_exact_mean_error"] for r in subset],
            rtol=0, atol=1e-14,
        )
        assert isclose(
            float(np.mean(np.abs(errors))), summary["ode_mean_absolute_error"],
            abs_tol=1e-12, rel_tol=0,
        )
        assert isclose(
            float(np.max(np.abs(errors))), summary["ode_max_absolute_error"],
            abs_tol=1e-12, rel_tol=0,
        )
    states = {
        r["genotype"]: r for r in record["closure_counterexample"]
    }
    assert states["homozygous"]["initial_mean"] == .5
    assert states["heterozygous"]["initial_mean"] == .5
    assert states["homozygous"]["next_variance"] == 0.
    # Two independently Mendelian-distributed 0.4/0.6 homolog copies.
    expected_heterozygote_child_variance = (.6 - .4) ** 2 / 8
    assert isclose(states["heterozygous"]["next_variance"],
                   expected_heterozygote_child_variance, abs_tol=1e-14)


def test_exact_birth_jump_mutation_and_heat_pde_component_are_not_identical():
    record = _read(RESULTS / "model3_mutation_limit_closeout_20261004.json")
    assert "Neumann" in record["boundary_condition"]
    assert "mutation kernel" in record["claim_boundary"][0]
    item = next(r for r in record["weak_mutation"]
                if r["mode"] == 2 and isclose(r["mutation_sd"], .1)
                and isclose(r["mutation_rate"], .05))
    k = item["mode"]
    u = item["mutation_rate"]
    sigma = item["mutation_sd"]
    lambda_ = (k * pi) ** 2 * sigma ** 2 / 2
    jump_multiplier = (1 - u) + u * exp(-lambda_)
    heat_multiplier = exp(-u * lambda_)
    assert abs(jump_multiplier - heat_multiplier) > 1e-5
    assert isclose(item["exact_semigroup_multiplier"], jump_multiplier,
                   rel_tol=0, abs_tol=1e-12)
    assert isclose(item["diffusion_multiplier"], heat_multiplier,
                   rel_tol=0, abs_tol=1e-12)


def test_fast_time_itô_sde_obstruction_is_specific_not_universal():
    d = _read(RESULTS / "model3_fast_time_scaling_20261009.json")
    r = d["results"]["rigorous_structural_case"]
    ks = (8, 16, 32, 64, 128)
    b = r["one_step_drift_l2"]
    scaled = r["K_times_drift_l2"]
    assert len(b) == len(ks) == len(scaled)
    assert max(b) - min(b) < 1e-12
    np.testing.assert_allclose(
        scaled, [k * v for k, v in zip(ks, b)],
        rtol=0, atol=1e-12,
    )
    assert scaled[0] < scaled[-1]
    assert d["research_boundary"]["continuous_time_SPDE_constructed"] is False
    assert d["research_boundary"]["complete_3trait_genetic_drift_examined"] is False
    assert "cannot cover this family" in r["conclusion"]
    assert "Not a proof" in r["scope"]


def test_clt_for_one_mean_does_not_preserve_discrete_class_extinction():
    clt = _read(RESULTS / "model3_discrete_offspring_linear_noise_20261009.json")
    cases = clt["results"]
    assert [r["N"] for r in cases] == [8, 16, 32, 64, 128]
    distances = [r["kolmogorov_distance"] for r in cases]
    assert all(a > b for a, b in zip(distances, distances[1:]))
    assert isclose(distances[0], .09010413417480584, abs_tol=1e-12)
    assert isclose(distances[-1], .022407, abs_tol=2e-6)
    q, n = .02, 8
    actual_loss = (1 - q) ** n
    assert isclose(actual_loss, .8507630225817854, abs_tol=1e-12)
    # Any Dirichlet simplex whose q>0 class has positive concentration
    # gives strictly positive frequency almost surely, hence zero loss.
    dirichlet_loss = 0.
    assert actual_loss > .85 > dirichlet_loss
    assert clt["admissibility"]["autonomous_continuous_time_SDE_validated"] is False
    assert clt["admissibility"]["autonomous_trait_space_SPDE_validated"] is False


def test_gaussian_projection_can_err_in_both_directions_about_genetic_richness():
    projection = _read(RESULTS / "model3_gaussian_presence_bias_20261009.json")
    rounding = _read(RESULTS / "model3_stochastic_rounding_ablation_20261009.json")
    assert projection["method"]["genotype_classes"] == 27
    assert projection["method"]["fixed_conditioned_child_census_equal_to_K"]
    by_k = {r["K"]: r for r in rounding["one_step"]}
    assert set(by_k) == {8, 32, 128}
    for row in projection["cases"]:
        k = row["K"]
        exact = row["exact_expected_genotype_classes"]
        gaussian = row["projected_gaussian_mean_classes"]
        other = by_k[k]
        assert gaussian > exact
        assert other["largest_remainder"] > exact
        assert other["stochastic_resampling_conditional_expected_richness"] < exact
        assert isclose(exact, other["exact_expected_class_richness"],
                       abs_tol=1e-12, rel_tol=0)
        assert isclose(gaussian - exact, row["projected_minus_exact_bias"],
                       abs_tol=1e-12, rel_tol=0)
