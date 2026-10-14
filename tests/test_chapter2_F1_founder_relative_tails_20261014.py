"""Founder-relative +0.05 assurance / -0.05 investment source-only F1 tails."""
import numpy as np
import pytest

from scripts.model3_island import reproduction
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, original_context,
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    balanced_source, balanced_cocarriage,
    joint_pre_mutation_segregational_deviations,
)
from scripts.audit_chapter2_directional_cosegregation_20261014 import directional_f1
from scripts.audit_chapter2_F1_founder_relative_tails_20261014 import (
    source_mean_threshold_tails, technical_report,
)


def directly_enumerated_single_offspring_tails(state, ledger):
    """Independent full father/mother/4 A-copy/4 I-copy t0 source exact enumeration."""
    prob=ledger.outcross.copy()
    prob[np.diag_indices(len(state.ids))]+=ledger.self_viable
    prob/=prob.sum()
    Amean=float(state.alleles[:,2,:].mean())
    Imean=float(state.alleles[:,1,:].mean())
    A_threshold=Amean+.05
    I_threshold=Imean-.05
    result=np.zeros(6,dtype=float)
    for father in range(48):
        for mother in range(48):
            w=prob[father,mother]
            if not w:continue
            Achoices=[(state.alleles[father,2,f]+state.alleles[mother,2,m])/2
                      for f in range(2) for m in range(2)]
            Ichoices=[(state.alleles[father,1,f]+state.alleles[mother,1,m])/2
                      for f in range(2) for m in range(2)]
            pA=sum(a>=A_threshold for a in Achoices)/4
            pI=sum(i<=I_threshold for i in Ichoices)/4
            joint=w*pA*pI
            result[0]+=w*pA
            result[1]+=w*pI
            result[2]+=joint
            result[3 if father==mother else 4]+=joint
            parent_mid=(state.alleles[father,1,:].mean()+
                        state.alleles[mother,1,:].mean())/2
            if parent_mid<=I_threshold:
                result[5]+=joint
    return result


@pytest.mark.parametrize("pool,context,m",[(0,0,0),(0,0,12),(3,3,0),(5,3,3),(13,4,12)])
def test_original_48_pair_16_gamete_combinations_independently(pool,context,m):
    original=original_fixture()
    config,visitor=original_context(original,"main",context)
    state=balanced_cocarriage(balanced_source(pool),pool,m)
    ledger=reproduction.reproduce(state,visitor,config)
    actual=source_mean_threshold_tails(state,ledger)
    direct=directly_enumerated_single_offspring_tails(state,ledger)
    keys=("p_one_offspring_A_at_least_plus_0p05",
          "p_one_offspring_I_at_most_minus_0p05",
          "p_one_offspring_both_0p05_thresholds",
          "p_both_via_selfed_parent_pair",
          "p_both_via_outcross_parent_pair",
          "p_both_where_selected_parent_I_midpoint_already_below_threshold")
    for idx,key in enumerate(keys):
        assert abs(actual[key]-direct[idx])<2e-13,key


def test_founder_relative_A_threshold_requires_two_carriers_at_h_1_over_16():
    old=original_fixture()
    for context in (0,3,4):
        config,visitor=original_context(old,"main",context)
        for pool in (0,1,15):
            s=balanced_cocarriage(balanced_source(pool),pool,6)
            l=reproduction.reproduce(s,visitor,config)
            parent=l.outcross.copy()
            parent[np.diag_indices(48)]+=l.self_viable
            p=parent/parent.sum()
            a=(s.alleles[:,2,0]!=s.alleles[:,2,1])
            truth=0.25*float(np.sum(p*np.outer(a,a)))
            result=source_mean_threshold_tails(s,l)
            assert result["founder_mean_A"]==0.5
            assert result["one_offspring_A_target"]==0.55
            assert abs(result["p_one_offspring_A_at_least_plus_0p05"]-truth)<1e-14


def test_parental_midpoint_signed_event_is_not_founder_threshold_event():
    old=original_fixture()
    conf,vis=original_context(old,"main",0)
    cases=[]
    for pool in range(16):
        s=balanced_cocarriage(balanced_source(pool),pool,0)
        ledger=reproduction.reproduce(s,vis,conf)
        sig=directional_f1(s,ledger)
        founder=source_mean_threshold_tails(s,ledger)
        assert sig["p_A_up_and_I_down"]==0
        assert founder["p_both_via_outcross_parent_pair"]==0
        cases.append(founder["p_one_offspring_both_0p05_thresholds"])
    # Between-adult I differences can cross founder threshold despite
    # m=0 and no within-individual hidden I in any A carrier parent.
    assert max(cases)>0


def test_entire_192_t0_threshold_inventory_and_matched_marginals():
    r=technical_report()
    assert r["status"]=="NO_BIOLOGY_ORIGINAL_MODEL3_CONDITIONAL_F1_THRESHOLD_ANALYTIC"
    assert r["matched_F1_single_offspring_contrasts"]==192
    assert r["new_biological_futures_or_sustained_events"]==0
    assert len(r["rows"])==192
    for pool in range(16):
        for context in (0,3,4):
            g=[x for x in r["rows"] if x["synthetic_source_pool"]==pool
               and x["visitor_context"]==context]
            assert len(g)==4
            assert abs(max(x["p_one_offspring_A_at_least_plus_0p05"] for x in g)-
                       min(x["p_one_offspring_A_at_least_plus_0p05"] for x in g))<2e-14
            assert abs(max(x["p_one_offspring_I_at_most_minus_0p05"] for x in g)-
                       min(x["p_one_offspring_I_at_most_minus_0p05"] for x in g))<2e-14
            for x in g:
                assert abs(x["p_one_offspring_both_0p05_thresholds"]-
                           x["p_both_via_selfed_parent_pair"]-
                           x["p_both_via_outcross_parent_pair"])<1e-13
                assert abs(x["p_one_offspring_both_0p05_thresholds"]-
                           x["p_both_where_selected_parent_I_midpoint_already_below_threshold"]-
                           x["p_both_where_selected_parent_I_midpoint_above_threshold"])<1e-13


def test_unregistered_threshold_scope_rejected():
    fixture=original_fixture()
    config,visitor=original_context(fixture,"main",0)
    state=balanced_cocarriage(balanced_source(0),0,0)
    ledger=reproduction.reproduce(state,visitor,config)
    with pytest.raises(ValueError,match="original 48-founder"):
        source_mean_threshold_tails(state,ledger,threshold=.025)
