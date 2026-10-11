"""Founder-total-delivered-pollen controls for four-type functional mismatch."""
import json
import numpy as np
import pytest
from scripts.audit_chapter2_q3q4_founder_delivery_matched_20261011 import (
    NONZERO_FRACTIONS,SETTINGS,BUDGETS,ARMS,
    comparator_visitors,reference_effectiveness,source_ledger,
    kernel,occupied80,audit,STATUS,
)


def test_founder_source_pollen_is_matched_but_functional_types_remain_four():
    for fraction in NONZERO_FRACTIONS:
        factor=reference_effectiveness(fraction)
        assert 0 < factor < 1
        x=comparator_visitors(fraction,"shifted4")
        y=comparator_visitors(fraction,"matched4_source_delivery")
        assert len(x.ids)==len(y.ids)==4
        np.testing.assert_allclose(x.effectiveness,1.)
        np.testing.assert_allclose(y.effectiveness,factor)
        np.testing.assert_allclose(y.optima,[.15,.35,.55,.75])
        assert not np.array_equal(x.optima,y.optima)
        for setting in SETTINGS:
            for b in BUDGETS:
                s=source_ledger((0,8,0),setting,b,fraction,"shifted4","native")
                m=source_ledger((0,8,0),setting,b,fraction,"matched4_source_delivery","native")
                assert s[2]==pytest.approx(m[2],rel=0,abs=1e-12)
                assert s[0]==pytest.approx(m[0],rel=0,abs=1e-11)
                np.testing.assert_allclose(s[1],m[1],rtol=0,atol=1e-12)
                assert 0<s[2]<.5 and 0<s[3]
    assert reference_effectiveness(.25)==pytest.approx(.6646107664171188,abs=1e-13)
    assert reference_effectiveness(.5)==pytest.approx(.0820444355586523,abs=1e-13)
    assert reference_effectiveness(1.)==pytest.approx(3.70042270966795e-6,abs=1e-16)


def test_transition_stochasticity_and_absorbing_extinction():
    for arm in ARMS:
        for mode in ("native","fixed_expression"):
            T=kernel("delayed_control",6.,.25,arm,mode)
            assert T.shape==(165,165)
            assert T[0,0]==1
            assert np.all(T[0,1:]==0)
            np.testing.assert_allclose(T.sum(axis=1),1.,rtol=0,atol=1e-12)
            assert 0<occupied80(T)<1


def test_all_exploratory_pairs_and_quantitative_negative_control():
    d=audit()
    assert d["status"]==STATUS
    assert d["n_paired_source_settings"]==len(NONZERO_FRACTIONS)*len(SETTINGS)*len(BUDGETS)
    assert d["n_new_ecological_histories"]==0 and d["n_natural_islands"]==0
    assert d["n_visitor_types_in_both_arms"]==4
    assert d["founder_match_only"] is True
    lookup={(r["mismatch_fraction"],r["setting"],r["budget"]):r for r in d["results"]}
    assert len(lookup)==32
    for row in lookup.values():
        d2=row["P80_by_visitor_context_and_policy"]
        assert set(d2)==set(ARMS)
        for arm in ARMS:
            assert 0<=d2[arm]["native"]<=1
            assert 0<=d2[arm]["fixed_expression"]<=1
            assert d2[arm]["native_minus_fixed"]==pytest.approx(
                d2[arm]["native"]-d2[arm]["fixed_expression"],abs=1e-12
            )
    q=lookup[.25,"delayed_control",6.]
    assert q["P80_native_shifted_minus_delivery_matched_reference"]==pytest.approx(
        -9.012276336411301e-6,rel=0,abs=1e-8
    )
    assert q["incremental_expression_effect_shifted_minus_reference"]==pytest.approx(
        -6.622002933633769e-6,rel=0,abs=1e-8
    )
    q=lookup[.5,"delayed_control",6.]
    assert q["P80_native_shifted_minus_delivery_matched_reference"]==pytest.approx(
        -1.483125435942749e-5,rel=0,abs=1e-8
    )
    q=lookup[1.,"delayed_control",6.]
    assert abs(q["P80_native_shifted_minus_delivery_matched_reference"])<2e-8
    q=lookup[.25,"delayed_control",8.]
    assert q["P80_native_shifted_minus_delivery_matched_reference"]==pytest.approx(
        .00019886126129087245,rel=0,abs=1e-7
    )
    assert "NOT uniquely" in d["warning"]
    json.dumps(d,allow_nan=False)


def test_invalid_source_contexts_rejected():
    with pytest.raises(ValueError):
        reference_effectiveness(0.)
    with pytest.raises(ValueError):
        comparator_visitors(.33,"shifted4")
    with pytest.raises(ValueError):
        comparator_visitors(.25,"invented")
    with pytest.raises(ValueError):
        source_ledger((0,8,0),"invented",6.,.25,"shifted4","native")
