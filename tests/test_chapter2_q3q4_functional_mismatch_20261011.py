"""Source-native fixed-richness matching-gradient, not a visitor-absence test."""
import json
import numpy as np
import pytest

from scripts.audit_chapter2_q3q4_functional_mismatch_20261011 import (
    STATUS,FRACTIONS,SETTINGS,BUDGETS,START,REPLACEMENT,
    visitors,mean_compatibility,reproductive_source,transition,audit,
)


def test_exact_four_functional_types_and_only_optima_change():
    for l in FRACTIONS:
        v=visitors(l)
        assert len(v.ids)==4
        np.testing.assert_allclose(v.breadths,.18)
        np.testing.assert_allclose(v.effectiveness,1.)
        np.testing.assert_allclose(
            v.optima,START+l*(REPLACEMENT-START),rtol=0,atol=1e-14
        )
    c=[mean_compatibility(x) for x in FRACTIONS]
    assert all(c[i]>c[i+1] for i in range(len(c)-1))
    assert c[0]==pytest.approx(.36199604641043487,abs=1e-12)
    assert c[-1]==pytest.approx(.0005052022266616112,abs=1e-14)

    # The complete functional replacement remains a nonzero-pollen FOUR-type
    # environment, although its pollen service becomes almost absent.
    source_matched=reproductive_source((0,8,0),"delayed_control",6.,0.,"native")
    source_replaced=reproductive_source((0,8,0),"delayed_control",6.,1.,"native")
    assert source_matched[2]==pytest.approx(.47675164271993675,abs=1e-11)
    assert source_replaced[2]==pytest.approx(1.7641826055923552e-6,abs=1e-11)
    assert 0 < source_replaced[2] < source_matched[2]/10000
    assert source_matched[3]==pytest.approx(1.3254356593125667,abs=1e-10)
    assert source_replaced[3]==pytest.approx(4.978107026798955e-6,abs=1e-10)
    with pytest.raises(ValueError):
        visitors(.33)


@pytest.mark.parametrize("setting",SETTINGS)
def test_original_founders_genetic_lottery_equal_in_native_and_clamped(setting):
    for l in FRACTIONS:
        a=reproductive_source((0,8,0),setting,6.,l,"native")
        b=reproductive_source((0,8,0),setting,6.,l,"fixed_expression")
        assert a[0]==pytest.approx(b[0],abs=1e-12)
        np.testing.assert_allclose(a[1],[.25,.5,.25],atol=1e-12)
        np.testing.assert_allclose(a[1],b[1],atol=1e-12)
        assert a[2]>0 and a[3]>0
        assert a[0]==pytest.approx(a[3]+a[4],abs=1e-12)


def test_original_source_transition_is_row_stochastic():
    for l in (0.,.5,1.):
        T=transition("delayed_control",6.,l,"native")
        assert T.shape==(165,165)
        assert T[0,0]==1 and np.all(T[0,1:]==0)
        assert np.isfinite(T).all() and (T>=0).all()
        np.testing.assert_allclose(T.sum(axis=1),1.,atol=1e-12,rtol=0)


def test_all_40_source_cells_and_explicit_relative_vs_absolute_survival():
    d=audit()
    assert d["status"]==STATUS
    assert d["n_synthetic_source_cells"]==40
    assert d["n_independent_island_systems"]==0
    assert d["n_new_visitor_histories"]==0
    assert d["visitor_richness"]==4
    q={(r["mismatch_fraction"],r["budget"],r["setting"]):r for r in d["results"]}
    assert len(q)==40
    for budget in BUDGETS:
        for setting in SETTINGS:
            # Both policies decline in ABSOLUTE occupancy as floral-visitor
            # trait compatibility declines, even if the contrast changes sign.
            native=[q[l,budget,setting]["P80_native"] for l in FRACTIONS]
            fixed=[q[l,budget,setting]["P80_fixed"] for l in FRACTIONS]
            assert all(native[i]>native[i+1] for i in range(4))
            assert all(fixed[i]>fixed[i+1] for i in range(4))
            mu=[q[l,budget,setting]["source_N8_total_viable"] for l in FRACTIONS]
            assert all(mu[i]>mu[i+1] for i in range(4))
    for setting in SETTINGS:
        assert q[0.,6.,setting]["P80_delta"]<0
        assert q[.25,6.,setting]["P80_delta"]>0
        assert q[1.,6.,setting]["P80_delta"]>0
    for setting in SETTINGS[:3]:
        assert q[1.,8.,setting]["P80_delta"]<0
    assert q[0.5,8.,"assurance_cost"]["P80_delta"]>0
    assert "ABSOLUTE survival" in d["caveat"]
    json.dumps(d,allow_nan=False)


def test_preserve_independent_original_model_numeric_references():
    r={(x["mismatch_fraction"],x["budget"],x["setting"]):x
       for x in audit()["results"]}
    expected={
      (0.,6.,"delayed_control"):(.0262718266055,.0302426464542),
      (.25,6.,"delayed_control"):(.01360000,.01336830),
      (.5,6.,"delayed_control"):(.00586,.00259),
      (1.,6.,"delayed_control"):(.005281,.002025),
      (0.,8.,"delayed_control"):(.89404723,.90274790),
      (1.,8.,"delayed_control"):(.68102,.69359),
    }
    for key,(n,f) in expected.items():
        row=r[key]
        tol=2e-8 if key[0]==0 else 8e-6
        assert row["P80_native"]==pytest.approx(n,abs=tol)
        assert row["P80_fixed"]==pytest.approx(f,abs=tol)
    assert r[1.,6.,"delayed_control"]["P80_delta"]==pytest.approx(
        +.003256506,abs=2e-8
    )
    assert r[1.,8.,"delayed_control"]["P80_delta"]==pytest.approx(
        -.012568896,abs=2e-8
    )


def test_reject_offgrid_mating_resource_and_policy():
    with pytest.raises(ValueError):
        reproductive_source((0,8,0),"invented",6.,0.,"native")
    with pytest.raises(ValueError):
        reproductive_source((0,8,0),"prior_selfing",5.,0.,"native")
    with pytest.raises(ValueError):
        reproductive_source((0,8,0),"prior_selfing",6.,0.,"unknown")
