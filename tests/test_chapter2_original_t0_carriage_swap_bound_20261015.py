"""Read-only checks of original fixed-genome overlap feasibility."""
import json
from copy import deepcopy
import pytest
from scripts.audit_chapter2_original_t0_carriage_swap_bound_20261015 import OUTPUT, load_original, one_block, report

def test_recompute_and_match_frozen_source():
    observed = report(load_original())
    frozen = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert observed == frozen
    assert observed["full_genome_model3_future_updates"] == 0
    assert observed["new_independent_source_genomes"] == 0

def test_original_phenotypes_and_overlap_cap():
    outcomes = report(load_original())["blocks"]
    for name, expected in {"main": (8,24,24,0), "confirmation": (5,30,18,6)}.items():
        x=outcomes[name]
        assert (x["distinct_expressed_M_I_A_strata"], x["original_I_heterozygote_adults"], x["original_I_homozygote_adults"], x["exact_matched_A_carrier_swap_capacity_with_I_original"]) == expected
        assert x["m0_to_m12_without_rewriting_I_is_feasible_under_this_control"] is False
        assert sorted(i for group in x["strata"] for i in group["individual_ids"]) == list(range(48))
        assert sum(g["phenotype_stratified_A_carrier_swap_capacity"] for g in x["strata"]) == expected[-1]
        for g in x["strata"]:
            assert g["individuals"] == g["I_heterozygote_adults"] + g["I_homozygote_adults"]
            assert g["phenotype_stratified_A_carrier_swap_capacity"] == min(g["I_heterozygote_adults"],g["I_homozygote_adults"])
    assert all(g["phenotype_stratified_A_carrier_swap_capacity"] == 0 for g in outcomes["main"]["strata"])
    mixed=[g for g in outcomes["confirmation"]["strata"] if g["phenotype_stratified_A_carrier_swap_capacity"]]
    assert len(mixed) == 1 and (mixed[0]["individuals"],mixed[0]["I_heterozygote_adults"],mixed[0]["I_homozygote_adults"]) == (24,18,6)

def test_source_validation_fails_closed():
    fields=load_original()["original_founders"]["main"]["source_state_arrays"]
    changed=deepcopy(fields)
    changed["alleles"]["dtype"]="<f4"
    with pytest.raises(ValueError,match="shape/dtype"):
        one_block("main",changed)
    changed=deepcopy(fields)
    changed["ids"]["data_b64"]=fields["alleles"]["data_b64"]
    with pytest.raises(ValueError,match="content/SHA"):
        one_block("main",changed)

def test_scope_is_not_natural_island_claim():
    claims=" ".join(report(load_original())["interpretation_limits"])
    assert "not a proof" in claims
    assert "not a measured mainland" in claims
