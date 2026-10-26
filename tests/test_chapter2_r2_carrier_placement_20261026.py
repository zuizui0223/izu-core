"""Design-only R2 falsification: copies and expressed I do not determine allele return.

Reproductive-operator tests only. No stochastic biological populations,
new source founders/visitors, offspring draws or biological Actions dispatch.
"""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pytest

from scripts.review_chapter2_r2_carrier_placement_20261026 import (
    STATUS, LEDGER_FIELDS, RECODABLE, N, N_CARRIERS,
    artificial_source_state, recode_I_only, expected_gene_weight, review,
)
from scripts.review_chapter2_r2_independent_feasibility_20261025 import PROTOCOL
from scripts.chapter2_pollen_baseline_factorial_20261019 import admit, config, visitors
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import PlantState


@pytest.fixture(scope="module")
def report():
    return review()


def test_run_authorization_is_provably_off_and_source_provenance_is_pinned(report):
    gate=json.loads(Path(PROTOCOL).read_text(encoding="utf8"))
    assert gate["status"]=="DESIGN_ONLY_NOT_AUTHORIZED_NOT_PREREGISTERED"
    assert all(flag is False for flag in gate["run_gate"].values())
    assert report["status"]==STATUS
    assert report["source_provenance"]["old_22_selected_source_founder_count"]==11
    assert report["not_registered_not_authorized"] is True
    assert report["should_dispatch_actions"] is False
    assert report["natural_island_causal_claim"] is False
    assert report["prospective_founder_histories"]==0
    assert report["new_biological_population_updates"]==0
    assert report["new_offspring_draws"]==0
    assert report["new_random_seed_reservations"]==0
    assert report["population"]=="ARTIFICIAL_48_DIPLOID_LABELLED_TEMPLATE_NOT_AUTHENTIC_FOUNDER"
    assert json.loads(json.dumps(report,allow_nan=False))==report


def test_exact_same_current_expressed_M_I_A_and_same_allele_counts_in_both_carrier_placements():
    base=artificial_source_state()
    assert len(base.ids)==N==48
    assert np.all(base.alleles[:RECODABLE,1,:]==.5)
    assert np.all(base.alleles[RECODABLE:,1,:]==.75)
    a=recode_I_only(base,list(range(8)))
    b=recode_I_only(base,list(range(16,24)))
    for changed in (a,b):
        assert np.array_equal(base.alleles.mean(axis=2),changed.alleles.mean(axis=2))
        assert np.array_equal(base.alleles[:,0,:],changed.alleles[:,0,:])
        assert np.array_equal(base.alleles[:,2,:],changed.alleles[:,2,:])
        assert np.array_equal(base.ids,changed.ids)
        assert np.array_equal(base.birth_years,changed.birth_years)
        vals,count=np.unique(changed.alleles[:,1,:],return_counts=True)
        assert dict(zip(vals.tolist(),count.tolist()))=={.25:8,.5:32,.75:56}
        assert float(changed.alleles[:,1,:].mean())==.625
        assert float(np.var(changed.alleles[:,1,:].mean(axis=1)))==.015625
    assert not np.array_equal(a.alleles[:,1,:],b.alleles[:,1,:])
    for invalid in ([0]*8,list(range(7)),list(range(7))+[24],
                    list(range(7))+[-1],list(range(7))+[True]):
        with pytest.raises(ValueError,match="exactly eight"):
            recode_I_only(base,invalid)


def test_real_model3_expected_parental_genotype_transmission_differs_with_identical_fecundity(report):
    assert len(report["native_static_reproduction_settings_checked"])==4
    assert report["same_current_native_reproductive_ledger_in_each_source_environment"] is True
    assert report["same_low_I_copy_count_and_allelic_value_variance"] is True
    assert report["current_low_I_copy_count_per_96"]==8
    assert report["current_mean_I_phenotype"]==.625
    assert report["current_phenotypic_I_variance"]==.015625
    hi=report["carrier_indices_at_higher_native_genetic_return"]
    lo=report["carrier_indices_at_lower_native_genetic_return"]
    assert len(set(hi))==len(set(lo))==N_CARRIERS
    assert not set(hi)&set(lo)
    assert all(0<=v<24 for v in hi+lo)
    for setting in report["native_static_reproduction_settings_checked"]:
        assert setting["original_current_reproductive_ledger_exactly_identical_across_placements"]
        assert setting["original_model_external_activity"] in (.4,.04)
        assert setting["baseline"] in ("strong_baseline_limitation","weak_baseline_limitation")
        x=setting["recode_allocations"]
        assert set(x)=={"high_current_parental_return","low_current_parental_return"}
        for row in x.values():
            assert row["low_I_allele_copies"]==8
            assert row["starting_low_I_fraction"]==pytest.approx(8/96)
            assert row["current_parentage_ledger_equals_original_byte_for_byte"]
            assert 0<=row["expected_low_I_fraction_in_newborns"]<=1
            assert row["expected_low_I_fraction_in_newborns"]==pytest.approx(
                row["mathematically_expected_from_weighted_gene_return"],abs=2e-13)
        assert setting["difference_in_low_I_newborn_fraction_from_carrier_placement"]==pytest.approx(
            x["high_current_parental_return"]["expected_low_I_fraction_in_newborns"]
            -x["low_current_parental_return"]["expected_low_I_fraction_in_newborns"],abs=2e-13)
    reference=next(x for x in report["native_static_reproduction_settings_checked"]
                   if x["baseline"]=="strong_baseline_limitation"
                   and x["original_model_external_activity"]==.4)
    assert reference["difference_in_low_I_newborn_fraction_from_carrier_placement"]>1e-12


def test_phenotype_changing_recode_does_change_ovule_allocation_negative_control():
    base=artificial_source_state()
    d=admit()
    cfg=config(d,"strong_baseline_limitation",.4)
    vis=visitors(d,"strong_baseline_limitation")
    source=reproduce(base,vis,cfg)
    # A deliberately INVALID phenotype-changing replacement is not admissible
    # to the matched-expressed-I carrier placement experiment.
    bad=base.alleles.copy()
    bad[0,1,:]=[.25,.5]  # expression .375, not the original .500
    changed=PlantState(
        alleles=bad,allele_origin=base.allele_origin,
        mutation_flags=base.mutation_flags,ids=base.ids,
        birth_years=base.birth_years,
    )
    assert not np.array_equal(base.alleles.mean(axis=2),
                              changed.alleles.mean(axis=2))
    different=reproduce(changed,vis,cfg)
    assert not np.array_equal(source.ovules,different.ovules)
    # A valid phenotype-preserving recode instead leaves EVERY current
    # ledger quantity identical, not just the population total.
    valid=recode_I_only(base,list(range(8)))
    samen=reproduce(valid,vis,cfg)
    for key in LEDGER_FIELDS:
        assert np.array_equal(getattr(source,key),getattr(samen,key))
    weights=expected_gene_weight(source)
    assert weights.shape==(N,)
    assert float(weights.min())<float(weights.max())


def test_actions_verified_source_static_carrier_readback_is_bounded(report):
    receipt=json.loads((Path(__file__).resolve().parents[1]/
        "docs/audits/CHAPTER2_R2_STATIC_CARRIER_PLACEMENT_20261026.json").read_text(encoding="utf8"))
    assert receipt["status"]=="SOURCE_NATIVE_STATIC_MATCHED_LEDGER_ALLELE_PLACEMENT_COUNTEREXAMPLE_HOLD"
    assert receipt["verified_actions_run_id"]==40255080484
    assert receipt["verified_actions_artifact_id"]==12621963266
    assert receipt["verified_artifact_json_length_bytes"]==8573
    assert receipt["verified_artifact_json_sha256"]=="4fe0474778ef6bbcf6a0b47c3f208fea11778df2021621cb2132c4924cae8b35"
    assert receipt["new_biological_population_updates"]==0
    assert receipt["new_offspring_draws"]==0
    assert receipt["future_random_seeds_reserved"]==0
    assert receipt["should_dispatch_actions"] is False
    assert receipt["preregistration_approved"] is False
    assert receipt["author_signoff"] is False
    assert receipt["legacy_r2_fresh_founder_four_setting_overall"]=="INCONCLUSIVE"
    assert receipt["claim_rank"]=="CONSTRUCTED_IDENTIFIABILITY_COUNTEREXAMPLE_ONLY_NOT_INDEPENDENT_BIOLOGICAL_EVIDENCE"
    assert receipt["artificial_recode"]["all_nine_native_reproduction_ledger_components_exactly_identical"]
    assert receipt["artificial_recode"]["I_numeric_allele_counts"]=={"0.25":8,"0.5":32,"0.75":56}
    assert len(receipt["settings"])==len(report["native_static_reproduction_settings_checked"])==4
    by_key={(r["baseline"],r["original_model_external_activity"]):r
        for r in report["native_static_reproduction_settings_checked"]}
    for recorded in receipt["settings"]:
        current=by_key[(recorded["baseline"],recorded["activity"])]
        x=current["recode_allocations"]
        assert recorded["expected_lowest_I_frequency_newborn_high_return_carriers"]==pytest.approx(
            x["high_current_parental_return"]["expected_low_I_fraction_in_newborns"],abs=1e-12)
        assert recorded["expected_lowest_I_frequency_newborn_low_return_carriers"]==pytest.approx(
            x["low_current_parental_return"]["expected_low_I_fraction_in_newborns"],abs=1e-12)
        assert recorded["high_minus_low_expected_frequency"]==pytest.approx(
            current["difference_in_low_I_newborn_fraction_from_carrier_placement"],abs=1e-12)
