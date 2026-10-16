"""Read-only cross-layer logic gates for the active izu-core Model 3 manuscript.

Scientific rank: software/interpretation regression tests, NOT new biological
histories, new independent ecological units, or validation of natural islands.
Do not rewrite frozen source data or redesign an original treatment to pass.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

import numpy as np
import pytest

from scripts.model3_island.density import density_step, make_grid, project_state
from scripts.model3_island.population import subset
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import Config, PlantState, VisitorState
from scripts.run_chapter2_assurance_generality import founders, load_design

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_assurance_generality_20261006.json"
BRIDGE = ROOT / "data/design/model3_ch2_bridge_20260927.json"
GENERALITY = ROOT / "data/results/chapter2_assurance_generality_20261006.json"
ARMS = ROOT / "data/results/chapter2_assurance_attenuation_decomposition_20261006.json"
GRADIENT = ROOT / "data/results/chapter2_assurance_gradient_components_20261006.json"
Q4_DESIGN = ROOT / "data/design/chapter2_island_demographic_independent32_20261008.json"
Q4_RUNNER = ROOT / "scripts/run_chapter2_island_demographic_independent32.py"
MODEL = ROOT / "scripts/model3_island"


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _small_state():
    """Three plants, one diploid individual per genotype; 0.5 is expressed A."""
    return PlantState(
        alleles=np.array([
            [[.45, .55], [.35, .65], [.5, .5]],
            [[.55, .65], [.45, .55], [.5, .5]],
            [[.35, .45], [.55, .65], [.5, .5]],
        ], dtype=float),
        allele_origin=np.arange(18, dtype=np.int64).reshape(3, 3, 2),
        mutation_flags=np.zeros((3, 3, 2), dtype=bool),
        ids=np.arange(3, dtype=np.int64),
        birth_years=np.zeros(3, dtype=np.int64),
    )


def _visitors():
    return VisitorState(
        ids=np.array([71, 72], dtype=np.int64),
        optima=np.array([.4, .6]),
        breadths=np.array([.2, .2]),
        effectiveness=np.array([1., 1.]),
    )


@pytest.mark.parametrize("setting", ("delayed_control", "prior_selfing",
                                     "pollen_discount", "assurance_cost"))
def test_source_reproductive_ledger_separates_male_female_self_and_cost(setting):
    from scripts.run_chapter2_assurance_generality import config
    design = load_design(DESIGN)
    cfg = config(design, setting, .01, "fixed")
    ledger = reproduce(_small_state(), _visitors(), cfg)
    assert np.count_nonzero(np.diag(ledger.outcross)) == 0
    assert np.count_nonzero(np.diag(ledger.delivered)) == 0
    np.testing.assert_allclose(
        ledger.outcross.sum(axis=0) + ledger.self_viable,
        ledger.maternal, atol=1e-12, rtol=0,
    )
    np.testing.assert_allclose(
        ledger.outcross.sum(axis=1) + ledger.self_viable,
        ledger.paternal, atol=1e-12, rtol=0,
    )
    np.testing.assert_allclose(ledger.maternal.sum(), ledger.paternal.sum(),
                               atol=1e-12, rtol=0)
    np.testing.assert_allclose(
        ledger.delivered.sum(axis=1) + ledger.lost,
        ledger.exported, atol=1e-12, rtol=0,
    )
    assert np.all(ledger.outcross.sum(axis=0) + ledger.self_raw
                  <= ledger.ovules + 1e-12)
    assert np.all(ledger.self_viable <= ledger.self_raw)


def test_single_plant_finite_outcross_zero_but_density_is_not_same_operator():
    """A source-acknowledged closure difference; it must not be called drift."""
    cfg = Config.from_dict(_json(BRIDGE)["base_config"])
    state = subset(_small_state(), np.array([0], dtype=np.int64))
    # A visitor may export pollen, but the one individual cannot outcross with
    # itself. Its autonomous selfing is deliberately a separate seed route.
    finite = reproduce(state, _visitors(), cfg)
    assert finite.exported.sum() > 0
    assert finite.delivered.sum() == 0
    assert finite.outcross.sum() == 0
    assert finite.self_viable.sum() > 0
    nodes = (np.array([0., .5, 1.]),) * 3
    grid = make_grid(nodes)
    # Snap the state to the grid so population state and density representation
    # have the same genotype support. This is not an evolutionary trajectory.
    snapped, counts = project_state(state, grid)
    finite_snapped = reproduce(snapped, _visitors(), cfg)
    assert finite_snapped.outcross.sum() == 0
    empty = PlantState(
        alleles=np.empty((0, 3, 2)),
        allele_origin=np.empty((0, 3, 2), dtype=np.int64),
        mutation_flags=np.empty((0, 3, 2), dtype=bool),
        ids=np.empty(0, dtype=np.int64),
        birth_years=np.empty(0, dtype=np.int64),
    )
    _, density = density_step(
        counts, grid, _visitors(), empty, cfg,
        mutation_traits=(False, False, False),
    )
    assert density.outcross.sum() > 0, (
        "This expected operator difference is intentionally documented; "
        "density closure does not remove individual self pollen."
    )


def test_q1_interaction_recomputed_from_unpooled_original_four_arm_mean():
    experiment = _json(GENERALITY)
    decomposition = _json(ARMS)
    fixed = _json(DESIGN)
    assert experiment["design_sha256"] == decomposition["source_design_sha256"]
    assert experiment["independent_visitor_histories"] == 64
    assert fixed["main_campaign"]["founder_seed"] == 74001
    assert fixed["main_campaign"]["declared_cases"] == 8192
    assert experiment["structural_control"]["matched_pairs_checked"] == 128
    assert experiment["structural_control"]["mismatches"] == []
    arms = {row["setting"]: row for row in decomposition["settings"]}
    for row in experiment["settings"]:
        name = row["setting"]
        estimate = arms[name]["estimates"]
        near = estimate["evolution_effect_near"]["mean"]
        far = estimate["evolution_effect_far"]["mean"]
        registered = row["attenuation_evolving_minus_fixed"]["mean"]
        assert near < 0 < far
        assert np.isclose(far - near, registered, atol=1e-12, rtol=0)
        assert np.isclose(estimate["attenuation"]["mean"], registered,
                          atol=1e-12, rtol=0)
        assert row["eligible_histories_four_cell"] == 64
        assert all(v == 1.0 for arms in row["occupancy"].values()
                   for v in arms.values())
        assert row["passes_frozen_rule"]
        # Crucially, the far arm does not grow in investment from founders.
        assert estimate["fixed_far_investment_change"]["mean"] < 0
        assert estimate["evolving_far_investment_change"]["mean"] < 0


def test_fixed_resident_gradients_do_not_identify_long_run_far_contrast():
    arms = {row["setting"]: row for row in _json(ARMS)["settings"]}
    rows = [r for r in _json(GRADIENT)["rows"] if r["snapshot"] == 400]
    assert len(rows) == 4
    for row in rows:
        setting = row["setting"]
        near = row["assurance_effect_high_minus_low"]["near"]["gradient"]["mean"]
        far = row["assurance_effect_high_minus_low"]["far"]["gradient"]["mean"]
        final_far = arms[setting]["estimates"]["evolution_effect_far"]["mean"]
        assert near < far < 0 < final_far  # different estimands, not a sign bug


def test_q4_original_design_and_runner_retain_future_a_mode_and_k_pollen_coupling():
    design = _json(Q4_DESIGN)
    src = Q4_RUNNER.read_text(encoding="utf-8")
    assert design["pre_mutation_rate"] == design["post_mutation_rate"] == .01
    assert 'cfg = config(source, setting, d["pre_mutation_rate"], mode)' in src
    assert 'post_cfg = replace(' in src
    assert 'capacity=d["post_capacity"]' in src
    # The post-update inherits the SAME mode and cfg, not a historical-only
    # allele intervention. Lock this caveat, not the misleading old gloss.
    assert src.count('mutation_traits=(True, True, mode == "evolving")') == 2
    finite = (MODEL / "reproduction.py").read_text(encoding="utf-8")
    kb = (ROOT / "scripts/chapter2_kb_reproduction.py").read_text(encoding="utf-8")
    assert "+config.capacity*config.background_ratio" in finite
    assert "+background_denominator_capacity*config.background_ratio" in kb


def test_module_level_import_graph_is_acyclic():
    """Top-level Python import cycles, not time-lag ecological feedback."""
    files = list(MODEL.glob("*.py"))
    names = {p.stem for p in files}
    graph = {name: set() for name in names}
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.level == 1:
                if node.module in names:
                    graph[path.stem].add(node.module)
    visited, current = set(), set()

    def walk(name):
        assert name not in current, f"import-time cycle through {name}"
        if name in visited:
            return
        current.add(name)
        for dependency in graph[name]:
            walk(dependency)
        current.remove(name)
        visited.add(name)

    for name in graph:
        walk(name)
    assert len(visited) == len(names)


def test_q1_exposure_is_external_and_initial_a_identical():
    """No feedback from plant phenotype into the next visitor population."""
    from scripts.run_model3_persistent_isolation import exposure
    from scripts.run_chapter2_assurance_generality import config
    design = load_design(DESIGN)
    plants = founders(design)
    assert np.array_equal(plants.alleles[:, 2, :],
                          np.full((48, 2), .5))
    visitors = exposure(26110601, "far")
    v0 = visitors.visitors[0]
    for setting in design["settings"]:
        f = config(design, setting, .01, "fixed")
        e = config(design, setting, .01, "evolving")
        f_ledger = reproduce(plants, v0, f)
        e_ledger = reproduce(plants, v0, e)
        for name in ("outcross", "self_raw", "self_viable", "ovules"):
            np.testing.assert_array_equal(getattr(f_ledger, name),
                                          getattr(e_ledger, name))
        # Cross-population feedback is within plants, not visitor arrivals;
        # the visitor history object itself remains unchanged.
        assert visitors.visitors[0] is v0
