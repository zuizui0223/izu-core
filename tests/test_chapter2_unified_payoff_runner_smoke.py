"""Engineering smoke tests use HISTORICAL seeds, never the new 64-history cohort.

Production task coverage and success criteria are tested separately by the
non-peeking design test. These 2-update smokes are NOT scientific outcomes.
"""
from dataclasses import replace
import hashlib
import json
import numpy as np
import pytest

from scripts.plan_chapter2_unified_payoff_evolution_persistence import (
    Prehistory, load_design, prehistory_tasks
)
from scripts.run_chapter2_assurance_generality import load_design as source_design
from scripts.run_chapter2_unified_payoff_prehistories import (
    SOURCE, run_one, persist_one, source_hashes
)
from scripts.run_chapter2_unified_payoff_postshock import (
    recover_state, shock_ancestors, one_future, common_streams
)
from scripts.summarize_chapter2_unified_payoff_evolution_persistence import (
    bootstrap_summary, evaluate
)
from scripts.model3_island.randomness import STREAM_IDS


def miniature(d):
    return {
        **d,
        "prehistory": {
            **d["prehistory"], "updates": 2,
            "occupancy_census_times": [0, 1, 2],
            "local_diagnostic_times": [0, 1, 2],
        },
        "postshock": {**d["postshock"], "updates": 2},
    }


def test_old_history_2_update_biology_and_selection_gradient_identity(tmp_path):
    d = miniature(load_design())
    biology = source_design(SOURCE)
    # This visitor history belongs to the OLD 2026-10-06 campaign.
    old_seed = 26110601
    modes = []
    for mode in ("fixed", "evolving"):
        t = Prehistory("delayed_control", mode, "near", old_seed, 26111601)
        state, recorded = run_one(t, d, biology)
        assert recorded["postshock_results_exposed"] is False
        assert [x["t"] for x in recorded["snapshots"]] == [0, 1, 2]
        assert recorded["snapshots"][-1]["n"] <= 48
        assert len(recorded["payoff_snapshots"]) >= 1
        gradients = [x["local_fixed_resident_gradient"]
                     for x in recorded["snapshots"]]
        for grad in gradients:
            assert grad is not None
            assert grad["gradient"] == pytest.approx(sum(
                grad[k] for k in (
                    "maternal_outcross_component",
                    "paternal_export_component",
                    "selfing_displacement_component",
                    "ovule_allocation_cost_component",
                )))
        if mode == "fixed":
            assert np.all(state.alleles[:, 2, :] == 0.5)
        modes.append((t, state))
    task, pre_state = modes[0]
    # Byte-audited round trip: postshock must recover EXACT diploid metadata.
    hashes = source_hashes()
    persist_one(tmp_path, task, d, biology, hashes)
    restored, sha = recover_state(tmp_path, task, d, hashes)
    assert len(sha) == 64
    for field in ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years"):
        assert np.array_equal(getattr(restored, field), getattr(pre_state, field))


def test_future_rules_equalize_a_evolution_and_preserve_the_bottleneck():
    d = miniature(load_design())
    biology = source_design(SOURCE)
    t = Prehistory("prior_selfing", "fixed", "far", 26110601, 26111601)
    state, _ = run_one(t, d, biology)
    bottled = shock_ancestors(t, state)
    assert len(bottled.ids) == min(8, len(state.ids))
    assert set(bottled.ids).issubset(set(state.ids))
    assert np.all(state.alleles[:, 2, :] == 0.5)
    # Even the historical FIXED-A population enters an EVOLVING-A future.
    near = one_future(t, state, d, biology,
                      "bottleneck_small_capacity", 3, "near", bottled)
    far = one_future(t, state, d, biology,
                     "founder_bottleneck", 3, "near", bottled)
    assert near["future_assurance_mode"] == "evolving"
    assert far["future_assurance_mode"] == "evolving"
    assert near["t0_population"] == far["t0_population"] == len(bottled.ids)
    assert near["end_population"] <= 8
    assert far["end_population"] <= 48
    assert near["t0_reproductive_output"] is not None
    assert near["t0_reproductive_output"]["maternal_viable_per_plant"] >= 0
    other_mode = replace(t, mode="evolving", environment="near")
    a = common_streams(t, 0, 2, 0, 3)
    b = common_streams(other_mode, 0, 2, 0, 3)
    assert a["recruitment"].random() == b["recruitment"].random()
    assert a["parents"].random() == b["parents"].random()
    # The founder bottleneck and maintained-small-capacity regimes use
    # the same eight ancestors AND matched future demographic streams.
    bottleneck_large = common_streams(t, 0, 1, 0, 3)
    bottleneck_small = common_streams(t, 0, 2, 0, 3)
    for stream_name in STREAM_IDS:
        assert bottleneck_large[stream_name].random() == (
            bottleneck_small[stream_name].random()
        )
    # Changing the historical treatment alone must also leave RNG matched.
    comparison = common_streams(other_mode, 0, 1, 0, 3)
    for stream_name in STREAM_IDS:
        assert comparison[stream_name].random() == (
            common_streams(t, 0, 2, 0, 3)[stream_name].random()
        )


def test_60_history_admission_uses_independent_visitor_not_nested_repeats():
    rng = np.random.default_rng(3611082026)
    indices = rng.integers(0, 64, size=(9999, 64))
    baseline = np.full((64, 2), -0.4)
    baseline[60:, 0] = np.nan
    result = bootstrap_summary(baseline, indices)
    assert result[0]["n_complete_histories"] == 60
    assert result[0]["conditional_on_endpoint_survival"] is True
    assert result[0]["mean"] == pytest.approx(-0.4)
    assert result[0]["bootstrap95"] == pytest.approx([-0.4, -0.4])
    assert result[1]["n_complete_histories"] == 64
    assert result[1]["conditional_on_endpoint_survival"] is False
    baseline[:2, 0] = np.nan
    result2 = bootstrap_summary(baseline, indices)
    assert result2[0]["n_complete_histories"] == 58
    assert result2[0]["bootstrap95"] is None

def test_synthetic_joint_gate_cannot_substitute_a_favourable_other_regime():
    """Algebraic unit fixture ONLY: no new-history biological simulation."""
    d = load_design()
    pre, post = {}, {}
    regimes = [r["id"] for r in d["postshock"]["regimes"]]
    futures = d["postshock"]["visitor_environments"]
    budgets = d["postshock"]["budgets"]
    for task in prehistory_tasks(d):
        far = task.environment == "far"
        evolved = task.mode == "evolving"
        investment = 0.7 - 0.3 * far + 0.1 * (far and evolved)
        pre[task] = {"snapshots": [{"n": 48, "means": [0.5, investment, 0.5]}]}
        # Matched hypothetical occupancies are deliberately constructed,
        # not sampled or measured; all four settings have identical signs.
        occupied = int(far and evolved)
        post[task] = {
            (regime, future, float(budget)): {"occupied": occupied}
            for regime in regimes for future in futures for budget in budgets
        }
    positive = evaluate(d, pre, post)
    assert positive["stage1"]["all_four_pass"] is True
    assert positive["stage2"]["primary_gate"]["passes_frozen_rule"] is True
    assert positive["joint_pass"] is True
    assert positive["stage2"]["primary_gate"]["mean"] == pytest.approx(1.0)

    # Remove effects ONLY in the preregistered primary small-capacity arm.
    # Positive results in the other two regimes MUST NOT rescue this gate.
    for cells in post.values():
        for future in futures:
            for budget in budgets:
                cells[("bottleneck_small_capacity", future, float(budget))][
                    "occupied"
                ] = 0
    negative = evaluate(d, pre, post)
    assert negative["stage1"]["all_four_pass"] is True
    assert negative["stage2"]["primary_gate"]["passes_frozen_rule"] is False
    assert negative["joint_pass"] is False
    others = [
        x for x in negative["stage2"]["all_regimes"]
        if x["regime"] != "bottleneck_small_capacity"
    ]
    assert all(x["all_setting_equal_weight_pooled"]["passes_frozen_rule"]
               for x in others)
