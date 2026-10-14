"""Audit the full source-replayed t20 transplant family, no new histories."""
import json
import pytest

from scripts.audit_chapter2_t20_transplant_familywise import (
    STATUS, audit, familywise_interval
)


def test_no_single_raw_sign_can_replace_full_family_uncertainty():
    r=audit()
    assert r["status"]==STATUS
    assert r["n_comparisons"]==12
    assert r["n_common_eligible_exposed_model_visitor_histories"]==50
    assert len(r["contrasts"])==12
    assert r["primary_K48_genome_effect_verdict"]=="inconclusive"
    assert r["posthoc_K8_genome_effect_verdict"]=="inconclusive"
    assert r["n_inconclusive_effects_familywise"]==10
    assert r["n_resolved_positive_effects_above_5pp_familywise"]==2
    json.dumps(r,allow_nan=False)


def test_K8_genomic_source_positive_sign_does_not_meet_5pp_familywise_ROPE():
    v=audit()
    selected=next(x for x in v["contrasts"] if x["effect"]=="genome_origin"
                  and x["K"]==8 and x["future"]=="selected")
    assert selected["difference"]==.42
    ci=selected["familywise_12_contrast_conservative95"]
    assert 0<ci[0]<.05<ci[1]
    assert selected["familywise_ROPE_5pp_verdict"]=="inconclusive"


def test_transplant_followup_capacity_effects_are_secondaries():
    v=audit()
    capacities=[c for c in v["contrasts"] if c["effect"]=="future_capacity"]
    assert len(capacities)==4
    passing=[c for c in capacities if c["familywise_ROPE_5pp_verdict"]=="resolved_positive"]
    assert len(passing)==2
    assert all(c["donor"]=="neutral_origin" for c in passing)
    assert all(c["difference"]>=.50 for c in passing)


def test_degenerate_same_outcome_pairs_cannot_prove_effect_absence():
    lo,hi=familywise_interval(0,0,50,12)
    assert lo<-.05
    assert hi>.05
    assert lo==-hi


@pytest.mark.parametrize("arguments",[
    (-1,0,50,12),(0,51,50,12),(50,1,50,12),
    (0,0,0,12),(0,0,50,0),
])
def test_reject_invalid_familywise_input(arguments):
    with pytest.raises(ValueError):
        familywise_interval(*arguments)
