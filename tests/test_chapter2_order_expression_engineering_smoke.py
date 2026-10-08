"""Two-year OLD-history smoke, not part of the 64 new visitor-history cohort."""
import numpy as np
import pytest

from scripts.plan_chapter2_order_expression_identification import load_protocol
from scripts.chapter2_order_expression_schedule import (
    assigned_offsets, validate_scheduled_interventions,
)
from scripts.chapter2_order_expression_payoff import (
    reproduce_with_order_expression,
)
from scripts.chapter2_order_genetic_realization import GeneticOrderRecorder
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.population import advance
from scripts.model3_island.randomness import stream, STREAM_IDS
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, founders, load_design,
)
from scripts.run_model3_persistent_isolation import exposure


def test_declared_order_schedule_has_identical_dose_and_common_release():
    d = load_protocol()
    full = validate_scheduled_interventions(d)
    assert set(full) == {
        "assurance_first", "investment_first", "synchronous_time_control"
    }
    for result in full.values():
        assert result == {
            "A_offset_years": 200, "I_offset_years": 200,
            "common_release_updates": 100,
        }
    assert assigned_offsets(d, "assurance_first", 0) == (0.45, 0)
    assert assigned_offsets(d, "investment_first", 0) == (0, -0.45)
    assert assigned_offsets(d, "synchronous_time_control", 0) == (0.45, -0.45)
    for a in full:
        assert assigned_offsets(d, a, 300) == (0, 0)
        assert assigned_offsets(d, a, 399) == (0, 0)
    with pytest.raises(ValueError):
        assigned_offsets(d, "assurance_first", 400)
    with pytest.raises(ValueError):
        assigned_offsets(d, "assurance_first", True)
    with pytest.raises(ValueError):
        assigned_offsets(d, "missing_arm", 12)


@pytest.mark.parametrize("setting", ["prior_selfing", "pollen_discount"])
@pytest.mark.parametrize("arm", [
    "assurance_first", "investment_first", "synchronous_time_control"
])
def test_legacy_two_year_payoff_to_mendelian_recruitment_is_opt_in(setting, arm):
    protocol = load_protocol()
    biology = load_design(DEFAULT_DESIGN)
    cfg = config(biology, setting, 0.01, "evolving")
    visitors = exposure(26110601, "near")  # OLD; never use 37110801-64.
    state = founders(biology)
    original_initial = state.alleles.tobytes()
    genetic_recorder = GeneticOrderRecorder(state)
    master = int(np.random.SeedSequence([26110601, 26111601]).generate_state(1)[0])
    streams = {name: stream(master, name, 0) for name in STREAM_IDS}
    assert state.alleles.shape == (48, 3, 2)
    for year in range(2):
        a_offset, i_offset = assigned_offsets(protocol, arm, year)
        before = state.alleles.tobytes()
        ledger = reproduce_with_order_expression(
            state, visitors.visitors[year], cfg,
            assurance_shift=a_offset, investment_shift=i_offset,
        )
        # Never write temporary imposed traits into inherited alleles.
        assert state.alleles.tobytes() == before
        state, info = advance(
            state, ledger, visitors.seed_candidates[year], cfg, streams,
            year=year, mutation_traits=(True, True, True)
        )
        assert len(state.ids) <= cfg.capacity
        assert state.alleles.shape[1:] == (3, 2)
        assert info["resident_recruits"] >= 0
        genetic_recorder.observe(year + 1, state)
    assert original_initial == founders(biology).alleles.tobytes()
    assert len(genetic_recorder.observations) == 3
    assert genetic_recorder.observations[0]["inherited_means"] == (
        founders(biology).alleles.mean(axis=(0, 2)).tolist()
    )
    assert genetic_recorder.observations[2]["n"] == len(state.ids)
    # All temporary perturbations must be absent on the shared release phase.
    a, i = assigned_offsets(protocol, arm, 300)
    reference = reproduce(state, visitors.visitors[2], cfg)
    released = reproduce_with_order_expression(
        state, visitors.visitors[2], cfg,
        assurance_shift=a, investment_shift=i,
    )
    np.testing.assert_array_equal(released.maternal, reference.maternal)
    np.testing.assert_array_equal(released.paternal, reference.paternal)
