"""Source matched one-step engineering gate; never runs new ecological histories."""
from dataclasses import replace

import numpy as np
import pytest

from scripts.audit_chapter2_joint_one_step_genetics_occupancy import (
    GATES, STATUS, audit, exact_conditional_step, fixture,
)
from scripts.chapter2_kb_reproduction import reproduce_kb
from scripts.chapter2_postzygotic_viability_gate import (
    gate_postzygotic_seed_viability,
)
from scripts.model3_island.types import Ledger


def test_fixed_B_identical_founders_K_invariant_first_step_all_gates():
    result = audit()
    assert result["status"] == STATUS
    assert result["design"]["new_ecological_visitor_histories"] == 0
    assert result["design"]["exposed_confirmatory_histories_accessed"] is False
    assert result["design"]["future_generation_trajectories_run"] == 0
    assert set(result["gates"]) == set(GATES)
    for outcome in result["gates"].values():
        assert outcome["first_step_ledger_and_occupancy_K_invariant"] is True
        assert outcome["expected_recruits_K8"] <= 8 + 1e-12
        assert outcome["expected_recruits_K48"] <= 48 + 1e-12
        assert outcome["expected_recruits_K48"] >= outcome["expected_recruits_K8"]
        assert outcome["conditional_matching_mean_variance_K8"] >= (
            outcome["conditional_matching_mean_variance_K48"]
        )


def test_matching_outcross_parent_directions_reconstruct_exact_source_mean():
    state, visitors, cfg = fixture()
    original = reproduce_kb(
        state, visitors, cfg, background_denominator_capacity=48,
    )
    base = exact_conditional_step(state, original, cfg)
    for gate in GATES:
        s, o = GATES[gate]
        modified = gate_postzygotic_seed_viability(
            original, selfed_fraction=s, outcross_fraction=o,
        )
        obtained = exact_conditional_step(state, modified, cfg)
        transmission_sum = (
            np.asarray(obtained["self_transmission_contribution"])
            + np.asarray(obtained["outcross_father_transmission_contribution"])
            + np.asarray(obtained["outcross_mother_transmission_contribution"])
        )
        np.testing.assert_allclose(
            transmission_sum,
            obtained["offspring_mean_given_occupied"],
            atol=1e-12, rtol=0,
        )
        for untouched in ("exported", "delivered", "ovules", "self_raw"):
            np.testing.assert_array_equal(
                getattr(modified, untouched), getattr(original, untouched),
            )
        assert obtained["trait_mean_after_extinction"] is None
        assert obtained["continuous_sde_spde_validated"] is False
        assert 0 <= obtained["probability_extinct"] <= 1
        assert obtained["probability_extinct"] + obtained["probability_occupied"] == pytest.approx(1)
    assert base["recruitment_intensity"] > 0


def test_zero_seed_retention_has_no_conditional_genetic_trait():
    state, visitors, cfg = fixture()
    original = reproduce_kb(
        state, visitors, cfg, background_denominator_capacity=48,
    )
    zero = gate_postzygotic_seed_viability(
        original, selfed_fraction=0.0, outcross_fraction=0.0,
    )
    outcome = exact_conditional_step(state, zero, cfg)
    assert outcome["recruitment_intensity"] == 0
    assert outcome["probability_extinct"] == 1
    assert outcome["probability_occupied"] == 0
    assert outcome["offspring_mean_given_occupied"] is None
    assert outcome["conditional_mean_covariance"] is None
    assert outcome["trait_mean_after_extinction"] is None


@pytest.mark.parametrize("restriction", [
    {"survival": 0.1},
    {"mutation_rate": 0.01},
])
def test_reject_biology_not_supported_by_exact_restricted_moments(restriction):
    state, visitors, cfg = fixture()
    old = reproduce_kb(state, visitors, cfg, background_denominator_capacity=48)
    with pytest.raises(ValueError, match="no survival, mutation or immigration"):
        exact_conditional_step(state, old, replace(cfg, **restriction))


def test_reject_mismatched_ledger_population_and_immigration():
    state, visitors, cfg = fixture()
    led = reproduce_kb(state, visitors, cfg, background_denominator_capacity=48)
    with pytest.raises(ValueError, match="no survival, mutation or immigration"):
        exact_conditional_step(
            state, led, replace(cfg, seed_arrival=replace(cfg.seed_arrival, supply=1.0))
        )
    with pytest.raises(ValueError, match="nonempty founder"):
        exact_conditional_step(
            replace(
                state, alleles=state.alleles[:7],
                allele_origin=state.allele_origin[:7],
                mutation_flags=state.mutation_flags[:7],
                ids=state.ids[:7], birth_years=state.birth_years[:7],
            ), led, cfg
        )
