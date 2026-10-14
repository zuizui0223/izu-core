"""Exact old I-homolog-collapsed population support; no evolutionary histories."""
from fractions import Fraction
from itertools import combinations
from collections import Counter
import json
import pytest

from scripts.audit_chapter2_founder_I_support_exact_20261014 import (
    ORIGINAL_BLOB, FOUNDERS, EXPECTED, RESULT, i_mean_profile,
    exact_mutation_free_I_support, audit, check_committed_result,
)


def test_original_t0_class_frequencies_are_from_authenticated_diploid_genomes():
    assert ORIGINAL_BLOB == "4b529cce12bc44e06d43a22b10c325a52bbd967b"
    assert dict(i_mean_profile("main")) == {6:12,7:6,8:6,9:12,10:12}
    assert dict(i_mean_profile("confirmation")) == {7:6,8:30,9:6,10:6}
    with pytest.raises(ValueError,match="historical"):
        i_mean_profile("unregistered")


def test_replayed_summary_matches_committed_exact_eight_rows():
    r=check_committed_result()
    assert r["genetic_futures_or_simulation_histories_run"]==0
    assert len(r["rows"])==8
    assert {x["n_founders"] for x in r["rows"]}==set(FOUNDERS)
    assert set(x["original_founder_block"] for x in r["rows"])==set(EXPECTED)
    assert sum(x["enumerated_phenotype_count_combinations"] for x in r["rows"])>6000


def test_exact_hypergeom_coverage_and_response_bound_not_mutation_or_selfing():
    d=audit()
    for row in d["rows"]:
        assert 0 <= row["mutation_free_necessary_support_count"] <= row["total_combinations"]
        assert Fraction(row["exact_support_probability"]) == Fraction(
            row["mutation_free_necessary_support_count"],row["total_combinations"])
        if row["n_founders"]==48:
            assert row["exact_support_probability"]=="1"
        else:
            assert float(row["exact_support_probability"].split("/")[0])>0


def test_n2_independent_pairwise_enumeration():
    for block in EXPECTED:
        profile=i_mean_profile(block)
        values=[v for v,k in profile for _ in range(k)]
        assert len(values)==48
        favorable=0
        for a,b in combinations(values,2):
            # First-generation mutation-free target support, not an event.
            avg=a+b
            vmin=min(a,b)
            favorable += 5*(avg - 2*vmin) >= 8
        exact=exact_mutation_free_I_support(profile,2)
        assert exact["mutation_free_necessary_support_count"]==favorable
        assert exact["total_combinations"]==1128


def test_zero_within_plant_I_heterozygosity_does_not_imply_no_I_allele_support():
    main=exact_mutation_free_I_support(i_mean_profile("main"),8)
    other=exact_mutation_free_I_support(i_mean_profile("confirmation"),8)
    assert Fraction(main["exact_support_probability"]) > Fraction(99,100)
    assert Fraction(other["exact_support_probability"]) > Fraction(1,2)
    assert main["mutation_free_necessary_support_count"] > 0
    assert other["mutation_free_necessary_support_count"] > 0


@pytest.mark.parametrize("count",[-1,0,49,2.5,True])
def test_out_of_domain_original_founder_sample_is_rejected(count):
    with pytest.raises(ValueError,match="Invalid finite source|Impossible founder count"):
        exact_mutation_free_I_support(i_mean_profile("main"),count)


def test_receipt_is_explicitly_combinatorial_not_empirical_response():
    doc=json.loads(RESULT.read_text())
    assert doc["status"]=="ORIGINAL_SOURCE_COMBINATORIAL_DIAGNOSTIC_NO_BIOLOGY"
    assert doc["genetic_futures_or_simulation_histories_run"]==0
    assert "NOT sustained 20-census event" in doc["outcome_definition"]
    assert "no" in " ".join(doc["limits"]).lower()
