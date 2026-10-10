"""No new visitor samples. Smoke source only; production checks full 96-path SHA."""
import json
from scripts.audit_chapter2_actual_vs_fixed4_visitor_swap import (
    SOURCE_96_SHA,STATUS,contract
)
from scripts.audit_chapter2_investment_conflict_path_replay import replay_path
from scripts.audit_chapter2_investment_commons_pilot_power import (
    contract as source_contract,initial_genotypes,visitors,
)


def test_postoutcome_same_genotype_visitor_replacement_contract():
    d,h=contract()
    assert len(h)==64
    assert d["original_n_stochastic_states"]==1533
    assert d["source_exact_sha256"]==SOURCE_96_SHA
    assert "Changes richness and composition together" in d["visitor_replacement"]


def test_visitor_counterfactual_is_not_used_by_genetic_demography():
    d,_=source_contract()
    founder,_=initial_genotypes(d)
    h=visitors(d,9701291,"stochastic_matched4")
    original_four=visitors(d,9701291,"static_matched4").visitors[0]
    old=replay_path(
        d,founder,h,9701291,"stochastic_matched4",8,8.,"native",
        diagnose=True)
    new=replay_path(
        d,founder,h,9701291,"stochastic_matched4",8,8.,"native",
        diagnose=True,reference_visitor_state=original_four)
    assert old["original_pilot_result"]==new["original_pilot_result"]
    assert old["source_conflict_window_years"]==new["source_conflict_window_years"]
    for a,b in zip(old["complete_native_or_centered_80_annual_states"],
                   new["complete_native_or_centered_80_annual_states"]):
        assert a["N"]==b["N"]
        if a["actual_native_mixed_genotype_window"] is None:
            assert b["actual_native_mixed_genotype_window"] is None
        else:
            ca=a["actual_native_mixed_genotype_window"]
            cb=b["actual_native_mixed_genotype_window"]
            cf=cb["same_genotype_static_four_visitor_counterfactual"]
            for field in ("mixed_genotype_majority_conflict",
                          "gamma_collective_log_seed",
                          "focal_beta_negative_count"):
                assert ca[field]==cb[field]
            assert isinstance(cf["mixed_genotype_majority_conflict"],bool)
    json.dumps(new,allow_nan=False)
