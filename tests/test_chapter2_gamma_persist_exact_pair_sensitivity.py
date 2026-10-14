"""Original source counts, conservative all-boundary exact CI, null retention."""
import json
import pytest

from scripts.audit_chapter2_gamma_persist_exact_pair_sensitivity import (
    STATUS,audit,cp_bernoulli,paired_exact_interval,classify,
)


def test_zero_discordance_is_not_exact_zero_effect():
    ci=paired_exact_interval(0,0,64)
    assert ci[0]<-.05
    assert ci[1]>.05
    assert ci[0]==pytest.approx(-ci[1])
    assert classify(ci)=="inconclusive"


def test_known_strong_year20_signal_and_no_resolved_year80_cells():
    r=audit()
    assert r["status"]==STATUS
    assert len(r["results"])==16
    assert r["by_horizon"]["80"]["resolved_positive"]==0
    assert r["by_horizon"]["80"]["resolved_negative"]==0
    assert r["by_horizon"]["80"]["practically_equivalent"]==0
    assert r["by_horizon"]["80"]["inconclusive"]==8
    assert r["by_horizon"]["20"]["resolved_positive"]==1
    target=[x for x in r["results"] if (
        x["K"]==48 and x["assurance"]==.35 and x["gate"]=="half_self"
        and x["horizon"]==20
    )]
    assert len(target)==1
    assert target[0]["delta_plus_minus"]==pytest.approx(22/64)
    assert target[0]["conservative_classification"]=="resolved_positive"
    assert target[0]["bonferroni_cp_simultaneous_95"][0]>.05
    assert sum(x["both_survived"]+x["both_extinct"]+x["plus_only"]+x["minus_only"]
               for x in r["results"])==16*64
    json.dumps(r,allow_nan=False)


@pytest.mark.parametrize("bad",[
    (-1,0,64),(0,65,64),(64,1,64),(0,0,0),
])
def test_fail_closed_invalid_discordance_counts(bad):
    with pytest.raises(ValueError):
        paired_exact_interval(*bad)


def test_exact_interval_contains_known_null_and_bounds():
    lo,hi=cp_bernoulli(0,64,.025)
    assert lo==0
    assert .05<hi<.08
    interval=paired_exact_interval(22,0,64)
    assert interval[0]>.05
    assert interval[1]<.60
