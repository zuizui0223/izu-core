"""Original R2 low-I numerical allele expected transmission versus endpoint fixation."""
from __future__ import annotations

import json
from types import SimpleNamespace

import numpy as np
import pytest

from scripts.model3_island.types import PlantState
from scripts.audit_chapter2_r2_low_I_allele_transmission_20261024 import (
    STATUS, expected_alleles, replay
)


def _synthetic():
    n=48
    a=np.full((n,3,2),0.5,dtype=float)
    a[0,1,:]=[0.25,0.5]
    a[1,1,:]=[0.25,0.25]
    return PlantState(
        alleles=a,
        allele_origin=np.arange(n*6,dtype=np.int64).reshape(n,3,2),
        mutation_flags=np.zeros((n,3,2),dtype=bool),
        ids=np.arange(n,dtype=np.int64),
        birth_years=np.zeros(n,dtype=np.int64)
    )


def test_ordered_parentage_genome_expected_low_I_counts_and_selfing():
    s=_synthetic()
    O=np.zeros((48,48))
    O[0,2]=8.0
    selfed=np.zeros(48)
    ledger=SimpleNamespace(outcross=O,self_viable=selfed,ovules=np.full(48,2.0))
    x=expected_alleles(s,ledger)
    lo=x["numerical_I_allele_frequencies"]["0.25"]
    assert lo["count_at_original_census30"]==3
    assert lo["frequency_at_original_census30"]==pytest.approx(3/96)
    assert lo["expected_frequency_in_resident_offspring"]==pytest.approx(.25)
    assert x["expected_mean_offspring_I"]==pytest.approx(.25*.25+.5*.75)
    assert x["original_native_outcross_fraction"]==pytest.approx(8/96)
    selfed[1]=8
    y=expected_alleles(s,ledger)
    assert y["numerical_I_allele_frequencies"]["0.25"]["expected_frequency_in_resident_offspring"]==pytest.approx(.625)
    assert y["expected_mean_offspring_I"]==pytest.approx(.25*.625+.5*.375)
    assert json.loads(json.dumps(y,allow_nan=False))==y


def test_invalid_or_monomorphic_parentage_is_rejected():
    s=_synthetic()
    bad=SimpleNamespace(outcross=np.zeros((48,48)),self_viable=np.zeros(48),
                        ovules=np.ones(48))
    with pytest.raises(AssertionError,match="viable offspring total"):
        expected_alleles(s,bad)
    bad.outcross=np.ones((47,47))
    with pytest.raises(AssertionError,match="invalid frozen"):
        expected_alleles(s,bad)
    uniform=s.alleles.copy()
    uniform[:,1,:]=.5
    fixed=PlantState(
        alleles=uniform,allele_origin=s.allele_origin,
        mutation_flags=s.mutation_flags,ids=s.ids,birth_years=s.birth_years
    )
    bad.outcross=np.zeros((48,48))
    bad.self_viable[0]=1
    with pytest.raises(AssertionError,match="must segregate"):
        expected_alleles(fixed,bad)


@pytest.fixture(scope="module")
def original():
    return replay()


def test_original_22_cells_verify_both_chromosome_transmission_and_source_historical_fate(original):
    d=original
    assert d["status"]==STATUS
    assert d["source_shock_genomes_exactly_hash_verified"]==22
    assert d["source_terminal_genomes_also_hash_verified_in_parent_replay"]==44
    assert d["source_original_cases"]==384
    assert d["source_matched_original_future_pairs"]==192
    assert d["n_original_founders"]==11
    assert d["n_orig_t30_genomes_biallelic_I"]==20
    assert d["n_orig_t30_genomes_triallelic_I"]==2
    assert d["new_biological_population_futures"]==d["new_preregistered_experiments"]==0
    assert len(d["rows"])==22
    assert all(x["decline_minus_control_expected_mean_I_shift"]<0 for x in d["rows"])
    assert sum(x["original_decline_fixed_to_lowest_I"] for x in d["rows"])==20
    for row in d["rows"]:
        assert sum(y["count_at_original_census30"] for y in row["allelic_expected_outcomes"]["control"]["numerical_I_allele_frequencies"].values())==96
        assert row["original_census30_full_genome_sha256"]
        assert len(row["original_census30_full_genome_sha256"])==64
        assert json.loads(json.dumps(row,allow_nan=False))==row
        if len(row["original_I_numerical_allele_values"])==2:
            levels=row["original_I_numerical_allele_values"]
            assert row["decline_minus_control_expected_lowest_I_fraction"]==pytest.approx(
                -row["decline_minus_control_expected_mean_I_shift"]/(levels[1]-levels[0]),
                abs=2e-13
            )


def test_rare_low_allele_exceptions_had_positive_relative_expected_transmission(original):
    z=original["special_low_copy_exceptions"]
    assert len(z)==2
    expected={
        (0.3,810102,4):(6,0.00457748119739243,0.75),
        (0.5,810110,3):(4,0.003082477806781947,0.5)
    }
    for r in z:
        key=(r["initial_A"],r["original_founder_seed"],r["nested_demographic_repeat"])
        copies,delta,fixed=expected[key]
        assert r["lowest_I_count_at_shock"]==copies
        assert r["original_decline_terminal_fixed_I"]==fixed
        assert r["original_decline_fixed_to_lowest_I"] is False
        assert r["decline_minus_control_expected_lowest_I_fraction"]==pytest.approx(delta,abs=2e-13)
        assert r["decline_minus_control_expected_lowest_I_fraction"]>0
        assert r["decline_minus_control_expected_mean_I_shift"]<0


def test_do_not_promote_selection_drift_or_population_frequency_threshold(original):
    assert "NO_CAUSAL_FIXATION_PROBABILITY" in original["claim_rank"]
    assert "Independent selective allele frequency advantage" in original["not_identified"][0]
    assert original["new_biological_population_futures"]==0
    assert original["new_preregistered_experiments"]==0
