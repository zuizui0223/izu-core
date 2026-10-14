"""Directional A-up/I-down source-only joint gamete transmission audit."""
import numpy as np
import pytest

from scripts.model3_island import reproduction
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, original_context,
)
from scripts.audit_chapter2_balanced_cocarriage_20261014 import (
    balanced_source, balanced_cocarriage, joint_pre_mutation_segregational_deviations,
)
from scripts.audit_chapter2_directional_cosegregation_20261014 import (
    directional_f1, technical_report,
)


def independent_copy_enumeration(source, ledger):
    """Brute force original source diploid copy combinations at BOTH loci.

    This does not sample offspring or call the biological update operator.
    """
    p=ledger.outcross.copy()
    np.fill_diagonal(p,np.diag(p)+ledger.self_viable)
    p/=p.sum()
    signed=selfsigned=outcrosssigned=otherquad=0.
    marginal_A=marginal_I=0.
    for father in range(48):
        for mother in range(48):
            weight=float(p[father,mother])
            if weight==0: continue
            a0=(source.alleles[father,2].mean()+
                source.alleles[mother,2].mean())/2
            i0=(source.alleles[father,1].mean()+
                source.alleles[mother,1].mean())/2
            pApos=pIneg=pIpos=0.
            for fcopy in (0,1):
                for mcopy in (0,1):
                    a_child=(source.alleles[father,2,fcopy]+
                             source.alleles[mother,2,mcopy])/2
                    i_child=(source.alleles[father,1,fcopy]+
                             source.alleles[mother,1,mcopy])/2
                    pApos+= (a_child>a0)/4
                    pIneg+= (i_child<i0)/4
                    pIpos+= (i_child>i0)/4
            w=weight*pApos*pIneg
            signed+=w
            otherquad+=weight*pApos*pIpos
            marginal_A+=weight*pApos
            marginal_I+=weight*pIneg
            if father==mother: selfsigned+=w
            else: outcrosssigned+=w
    return dict(signed=signed,selfed=selfsigned,outcross=outcrosssigned,
                A_up=marginal_A,I_down=marginal_I,
                A_up_I_up=otherquad)


@pytest.mark.parametrize("context,m",[(0,0),(0,12),(3,0),(3,3),(4,12)])
def test_sign_correct_against_full_meiosis_copy_enumeration(context,m):
    base=balanced_source(3)
    edit=balanced_cocarriage(base,3,m)
    fixture=original_fixture()
    cfg,vis=original_context(fixture,"main",context)
    ledger=reproduction.reproduce(edit,vis,cfg)
    target=directional_f1(edit,ledger)
    direct=independent_copy_enumeration(edit,ledger)
    comparisons={
        "p_A_up_and_I_down":"signed",
        "p_A_up_and_I_up":"A_up_I_up",
        "p_A_up_and_I_down_from_selfed_parent_pair":"selfed",
        "p_A_up_and_I_down_from_outcross_parent_pair":"outcross",
        "p_A_above_selected_parent_midpoint":"A_up",
        "p_I_below_selected_parent_midpoint":"I_down",
    }
    for key,checked in comparisons.items():
        assert abs(target[key]-direct[checked])<2e-13, key


def test_no_visitor_directional_signs_have_exact_m_over_768_law():
    fixture=original_fixture()
    cfg,vis=original_context(fixture,"main",0)
    assert len(vis.ids)==0
    for pool in range(16):
        base=balanced_source(pool)
        for m in (0,3,6,12):
            edited=balanced_cocarriage(base,pool,m)
            ledger=reproduction.reproduce(edited,vis,cfg)
            p=directional_f1(edited,ledger)
            carriers=((edited.alleles[:,1,0]!=edited.alleles[:,1,1]) &
                      (edited.alleles[:,2,0]!=edited.alleles[:,2,1]))
            true_weighted=float(ledger.self_viable[carriers].sum() /
                                ledger.self_viable.sum())/16
            assert abs(p["p_A_up_and_I_down"]-true_weighted)<1e-14
            if m==0:
                assert p["p_A_up_and_I_down"]==0
            if m==12:
                assert abs(p["p_A_up_and_I_down"]-1/64)<1e-14
            assert abs(p["p_A_above_selected_parent_midpoint"]-.0625)<1e-14
            assert abs(p["p_I_below_selected_parent_midpoint"]-.0625)<1e-14
            assert p["p_A_up_and_I_down_from_outcross_parent_pair"]==0
            assert abs(p["p_A_up_and_I_down_from_selfed_parent_pair"]-m/768)<1e-14


def test_pollen_enabled_crosses_can_combine_disjoint_carriers():
    fixture=original_fixture()
    for context in (3,4):
        cfg,vis=original_context(fixture,"main",context)
        for pool in range(16):
            base=balanced_source(pool)
            disjoint=balanced_cocarriage(base,pool,0)
            together=balanced_cocarriage(base,pool,12)
            l0=reproduction.reproduce(disjoint,vis,cfg)
            l1=reproduction.reproduce(together,vis,cfg)
            zero=directional_f1(disjoint,l0)
            overlap=directional_f1(together,l1)
            assert zero["p_A_up_and_I_down_from_selfed_parent_pair"]==0
            assert zero["p_A_up_and_I_down_from_outcross_parent_pair"]>0
            assert overlap["p_A_up_and_I_down"]>zero["p_A_up_and_I_down"]
            assert (overlap["p_A_up_and_I_down_from_selfed_parent_pair"]>0)


def test_symmetry_shows_joint_tail_difference_is_not_directional_selection():
    fixture=original_fixture()
    for context in (0,3,4):
        cfg,vis=original_context(fixture,"main",context)
        for pool in (0,5,15):
            base=balanced_source(pool)
            for m in (0,3,6,12):
                edited=balanced_cocarriage(base,pool,m)
                led=reproduction.reproduce(edited,vis,cfg)
                result=directional_f1(edited,led)
                for quadrant in ("p_A_up_and_I_up","p_A_down_and_I_down",
                                 "p_A_down_and_I_up"):
                    assert result[quadrant]==result["p_A_up_and_I_down"]
                assert result["covariance_of_signed_Mendelian_A_and_I_deviations"]==0
                nonsign=joint_pre_mutation_segregational_deviations(edited,led)
                assert abs(4*result["p_A_up_and_I_down"]-
                           nonsign["p_joint_nonzero_A_and_I_segregation"])<1e-14


def test_exact_full_source_grid_and_no_evolution_or_survival_claims():
    report=technical_report()
    assert report["status"]=="NO_BIOLOGY_NATIVE_REPRODUCTION_PREMUTATION_SIGNED_MEIOSIS"
    assert report["conditional_signed_first_offspring_cases"]==192
    assert report["new_biological_offspring_or_population_futures"]==0
    assert report["sustained_A_or_I_response_events_computed"] is False
    assert report["Q4_survival_or_persistence_computed"] is False
    assert report["independent_natural_island_sources_observed"]==0
    assert report["long_run_response_order_unidentified"] is True
    assert len(report["summary_by_visitor_context_and_m"])==12
    assert len(report["rows"])==192
    for row in report["rows"]:
        assert abs(row["p_A_up_and_I_down"] -
                   row["p_A_up_and_I_down_from_selfed_parent_pair"] -
                   row["p_A_up_and_I_down_from_outcross_parent_pair"])<1e-14
    assert report["direction_is_relative_to_selected_parent_midpoint_not_founder_mean"] is True


def test_source_guard_rejects_wrong_census_or_genotype_model():
    fixture=original_fixture()
    cfg,vis=original_context(fixture,"main",0)
    base=balanced_source(0)
    altered=balanced_cocarriage(base,0,3)
    ledger=reproduction.reproduce(altered,vis,cfg)
    from scripts.model3_island import population
    wrong=population.subset(altered, np.arange(2))
    with pytest.raises(ValueError,match="48-adult"):
        directional_f1(wrong,ledger)


def test_zero_signed_deviation_covariance_is_independently_enumerated():
    """Both directions can co-occur more often without signed covariance."""
    doc=original_fixture()
    c,vis=original_context(doc,"main",3)
    original=balanced_source(5)
    edited=balanced_cocarriage(original,5,12)
    led=reproduction.reproduce(edited,vis,c)
    p=led.outcross.copy()
    np.fill_diagonal(p,np.diag(p)+led.self_viable)
    p/=p.sum()
    product=meanA=meanI=0.
    for father in range(48):
        for mother in range(48):
            weight=float(p[father,mother])
            if weight==0: continue
            Amean=(edited.alleles[father,2].mean()+
                   edited.alleles[mother,2].mean())/2
            Imean=(edited.alleles[father,1].mean()+
                   edited.alleles[mother,1].mean())/2
            for aF in (0,1):
                for aM in (0,1):
                    deltaA=(edited.alleles[father,2,aF]+
                            edited.alleles[mother,2,aM])/2-Amean
                    for iF in (0,1):
                        for iM in (0,1):
                            deltaI=(edited.alleles[father,1,iF]+
                                    edited.alleles[mother,1,iM])/2-Imean
                            w=weight/16
                            meanA+=w*deltaA
                            meanI+=w*deltaI
                            product+=w*deltaA*deltaI
    assert abs(meanA)<1e-14
    assert abs(meanI)<1e-14
    assert abs(product-meanA*meanI)<1e-14
    # Quadrant tails are nevertheless nonzero.
    joint=directional_f1(edited,led)
    assert joint["p_A_up_and_I_down"]>0
    assert joint["p_A_up_and_I_up"]>0
