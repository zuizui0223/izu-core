"""Adversarial no-biology tests for hypothetical colonisation genetic-access algebra."""
from __future__ import annotations

import copy
import json
from fractions import Fraction
from math import comb

import pytest

from scripts.audit_chapter2_colonisation_genetic_access_feasibility_20261014 import (
    SPEC, ideal_segregation_variance, no_heterozygote_probability, report, validate
)


def declared():
    return json.loads(SPEC.read_text(encoding="utf-8"))


def test_exact_source_sample_heterozygote_loss():
    r = report(declared())
    assert r["biology_histories_run"] == 0
    assert [x["founders"] for x in r["p_original_A_heterozygote_total_loss"]] == [2,8,24,48]
    expected = [Fraction(comb(36,n),comb(48,n)) if n <= 36 else Fraction(0)
                for n in (2,8,24,48)]
    assert [Fraction(x["exact"]) for x in r["p_original_A_heterozygote_total_loss"]] == expected
    assert expected[0] == Fraction(105,188)
    assert expected[-1] == 0


def test_matched_variance_does_not_match_allele_support():
    q_small = ideal_segregation_variance(Fraction(1,8), Fraction(1,4))
    q_full = ideal_segregation_variance(Fraction(1,16), Fraction(1))
    assert q_small == q_full == Fraction(1,512)
    assert ideal_segregation_variance(Fraction(1,8),Fraction(1)) == 4*q_full
    assert ideal_segregation_variance(Fraction(1,16),Fraction(1,4)) == q_full/4
    cells = report(declared())["A_support_vs_ideal_variance_cells"]
    assert len(cells) == 4
    assert all(x["mutation_free_0p05_individual_support"] for x in cells)


@pytest.mark.parametrize("name,value,pattern", [
    ("status", "SUCCESS_CONFIRMED", "design-only"),
    ("candidate_founder_samples", [8,48], "founding sample counts"),
])
def test_no_silent_promotions_or_changed_founder_grid(name,value,pattern):
    d=declared()
    d[name]=value
    with pytest.raises(ValueError,match=pattern):
        validate(d)


def test_fake_mainland_measurement_is_rejected():
    d=declared()
    d["illustrative_mainland_source"]["real_observed_mainland_data"]=True
    with pytest.raises(ValueError,match="falsely claimed"):
        validate(d)


def test_genetically_homogeneous_source_not_allowed():
    d=declared()
    d["naturalistic_founder_sample"]["source_pool_heterogeneity_mandatory"]=False
    with pytest.raises(ValueError,match="homogeneous A"):
        validate(d)


def test_biological_run_or_author_approval_not_inferred():
    for key,value in [("author_approval_for_new_biology",True),
                      ("new_biological_histories",1),
                      ("source_genotypes_and_rng_frozen",True)]:
        d=declared()
        d["approval"][key]=value
        with pytest.raises(ValueError,match="No biological execution"):
            validate(d)


def test_original_six_classes_or_census_capacity_change_rejected():
    d=declared()
    d["outcome"]["classes"][0]="investment_first"
    with pytest.raises(ValueError,match="Six-class"):
        validate(d)
    d=declared()
    d["controlled_genetic_only"]["initial_plant_census"]=96
    with pytest.raises(ValueError,match="fixed-census"):
        validate(d)


def test_ideal_formula_refuses_invalid_parameters():
    with pytest.raises(ValueError,match="Invalid"):
        ideal_segregation_variance(Fraction(1,16),Fraction(2))
    with pytest.raises(ValueError,match="Impossible"):
        no_heterozygote_probability(48,12,49)
