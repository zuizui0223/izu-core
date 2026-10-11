"""Native source selection sign clock with matched cumulative pollination dose."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_sequence_tempo_focal_sign_clock_20261011 import (
    STATUS, PROFILE_SEEDS, TIMINGS, COSTS, local_beta,sign_clock,audit,
)


def test_genuine_native_source_focal_A_and_I_gradients_precede_genetic_evolution():
    for timing in TIMINGS:
        for cost in COSTS:
            a=local_beta(48271001,timing,cost,0.,"assurance")
            i0=local_beta(48271001,timing,cost,0.,"investment")
            i1=local_beta(48271001,timing,cost,1.,"investment")
            assert a>.02
            assert i0>.02
            assert i1<-.02
            assert local_beta(48271001,timing,cost,.3,"assurance")>0


def test_two_declared_schedules_have_different_beta_I_sign_onset_at_equal_dose():
    delayed=sign_clock(48271001,"delayed",.5)
    assert delayed["dose_matched_break_index"]==29
    assert delayed["focal_beta_I_matched"]==pytest.approx(.4655,abs=.0002)
    assert delayed["focal_beta_I_shifted"]<-.4
    assert delayed["lambda_for_beta_I_below_negative_deadband"]==pytest.approx(
        .4532,abs=.0002
    )
    assert delayed["by_schedule"]["abrupt"]["first_update_with_negative_focal_beta_I"]==30
    assert delayed["by_schedule"]["gradual"]["first_update_with_negative_focal_beta_I"]==45
    assert delayed["sudden_minus_gradual_negative_selection_onset"]==-15

    prior=sign_clock(48271001,"prior",.5)
    assert prior["dose_matched_break_index"]==29
    assert prior["by_schedule"]["abrupt"]["first_update_with_negative_focal_beta_I"]==30
    assert prior["by_schedule"]["gradual"]["first_update_with_negative_focal_beta_I"]==33
    assert prior["sudden_minus_gradual_negative_selection_onset"]==-3


def test_all_16_profiles_by_4_mating_treatments_and_no_natural_history():
    d=audit()
    assert d["status"]==STATUS
    assert d["n_synthetic_visitor_profiles"]==16
    assert d["n_cost_timing_source_conditions"]==4
    assert d["n_source_cells"]==64
    assert d["n_new_evolutionary_outcomes"]==0
    assert d["n_natural_ecological_systems"]==0
    for row in d["results"]:
        assert row["focal_beta_I_matched"]>.02
        assert row["focal_beta_I_shifted"]<-.02
        assert row["positive_assurance_beta_range"][0]>.02
        assert (row["by_schedule"]["abrupt"]["first_update_with_negative_focal_beta_I"]
                <row["by_schedule"]["gradual"]["first_update_with_negative_focal_beta_I"])
        assert -20<=row["sudden_minus_gradual_negative_selection_onset"]<=-2
    # Assured resource COST affects A local W returns, but independently
    # does not alter the timing of βI sign crossing in this fixed reference.
    indexed={(x["source_profile_seed"],x["assurance_timing"],
              x["direct_assurance_cost"]):x for x in d["results"]}
    for seed in PROFILE_SEEDS:
        for timing in TIMINGS:
            low=indexed[seed,timing,0.]
            high=indexed[seed,timing,.5]
            # Source fitness signs and timing are identical, but the native
            # F/P/S floating-point arithmetic can vary in its last bits when
            # direct assurance cost is changed. Do not require exact float
            # equality for separately evaluated log W derivatives.
            for schedule in ("abrupt","gradual"):
                a,b=low["by_schedule"][schedule],high["by_schedule"][schedule]
                assert a["first_update_with_negative_focal_beta_I"]==b[
                    "first_update_with_negative_focal_beta_I"]
                assert a["lambda_at_first_negative"]==pytest.approx(
                    b["lambda_at_first_negative"],abs=1e-14
                )
                assert a["beta_I_at_first_negative"]==pytest.approx(
                    b["beta_I_at_first_negative"],rel=0,abs=1e-12
                )
            assert low["focal_beta_I_matched"]==pytest.approx(
                high["focal_beta_I_matched"],rel=0,abs=1e-12
            )
    json.dumps(d,allow_nan=False)


def test_unknown_fitness_clock_context_rejected():
    with pytest.raises(ValueError):
        sign_clock(48270000,"delayed",.5)
    with pytest.raises(ValueError):
        sign_clock(48271001,"unknown",.5)
    with pytest.raises(ValueError):
        sign_clock(48271001,"delayed",.2)
