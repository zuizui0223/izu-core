"""Exact original two rare-low-I loss exception pathwise source guards.

The 24 original prefixes and 48 original final diploid states are verified
against archived SHAs, not novel stochastic populations. Tests preserve
the source post-outcome/11-founder inference ceiling.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.audit_chapter2_r2_rare_low_I_loss_chronology_20261024 import (
    STATUS, EXPECTED, annual_copy_accounting, audit_original
)

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"docs/audits/CHAPTER2_R2_RARE_LOW_I_LOSS_CHRONOLOGY_20261024.json"


def _fake(low=.5,high=.75,initial_copies=6,next_copies=8):
    n=48
    mean=high-(high-low)*initial_copies/(2*n)
    next_mean=high-(high-low)*next_copies/(2*n)
    expected=-.001
    return {
       "year_from_original_founding":30,
       "N_before_reproduction":n,"N_after_recruitment":n,
       "current_I_allele_values":[low,high],
       "current_I":mean,"next_I":next_mean,
       "expected_I_shift_from_parentage":expected,
       "realization_residual":next_mean-mean-expected,
       "realized_I_shift":next_mean-mean,
    }


def test_two_allele_diploid_frequency_reconstruction_is_exact():
    y=_fake()
    result=annual_copy_accounting(y,.5,.75)
    assert result["low_I_copies_before"]==6
    assert result["low_I_copies_after"]==8
    assert result["conditional_expected_low_I_fraction_shift"]==pytest.approx(.004)
    assert result["realized_low_I_fraction_shift"]==pytest.approx(2/96)
    assert result["realization_residual_low_I_fraction"]==pytest.approx(2/96-.004)
    assert result["source_I_allele_support"]==[.5,.75]


def test_corrupted_allele_count_or_expected_identity_fails_closed():
    y=_fake()
    wrong=copy.deepcopy(y)
    wrong["current_I"]+=.001
    with pytest.raises(AssertionError,match="exact integer"):
        annual_copy_accounting(wrong,.5,.75)
    wrong=copy.deepcopy(y)
    wrong["realization_residual"]+=.05
    with pytest.raises(AssertionError,match="does not telescope"):
        annual_copy_accounting(wrong,.5,.75)
    wrong=copy.deepcopy(y)
    wrong["current_I_allele_values"]=[.25,.5,.75]
    with pytest.raises(AssertionError,match="does not support"):
        annual_copy_accounting(wrong,.5,.75)


@pytest.fixture(scope="module")
def audit():
    return audit_original()


def test_original_two_source_exception_ids_and_phase_lengths(audit):
    receipt=json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert audit["status"]==STATUS==receipt["status"]
    assert audit["source_original_actions_run_id"]==39233450099
    assert audit["source_archived_pathwise_actions_run_id"]==40057254260
    assert audit["source_genomes_SHA_verified_original_paired_cells"]==24
    assert audit["new_independent_biological_futures"]==0
    assert audit["new_preregistered_statistical_tests"]==0
    assert "NO_CAUSAL_SELECTION_DRIFT_SHARE" in audit["claim_rank"]
    assert len(audit["episodes"])==2
    assert len(EXPECTED)==2
    assert {(
        r["initial_A"],r["original_founder_seed"],r["demographic_repeat"]
    ) for r in audit["episodes"]}==set(EXPECTED)
    for row in audit["episodes"]:
        key=(row["initial_A"],row["original_founder_seed"],row["demographic_repeat"])
        exp=EXPECTED[key]
        assert row["original_low_I_copies_at_shock"]==exp["initial_count"]
        assert row["lowest_I_numerical_allele"]==exp["low"]
        assert row["higher_I_numerical_allele"]==exp["high"]
        assert len(row["source_original_prefix_sha256"])==64
        for arm in ("control","decline"):
            z=row["arms"][arm]
            assert z["first_original_census_low_I_allele_lost"]==exp["fixed_census"][arm]
            assert z["n_censuses_I_segregating"]==exp["n_segregating_source_generations"][arm]
            assert z["n_segregating_years_expected_low_I_frequency_positive"]==z["n_censuses_I_segregating"]
            assert z["sum_original_path_expected_low_I_frequency_shift"]==pytest.approx(
                exp["cumulative_expected_low_frequency"][arm],abs=1e-12)
            assert z["sum_original_path_realization_low_I_fraction_residual"]==pytest.approx(
                exp["cumulative_realization_low_frequency"][arm],abs=1e-12)
            assert z["sum_original_path_expected_low_I_frequency_shift"]>0
            assert z["sum_original_path_realization_low_I_fraction_residual"]<0
            assert z["original_path_total_realized_low_I_fraction_shift"]==pytest.approx(
                -exp["initial_count"]/96,abs=1e-12)
            assert len(z["original_years_until_fixation"])==z["n_censuses_I_segregating"]
            assert all(t["conditional_expected_low_I_fraction_shift"]>0
                       for t in z["original_years_until_fixation"])
    assert receipt["original_full_pathwise_JSON_sha256"]=="794a23aca8e56f8e74f4d5497fa221cbba9432a20170917163fe117dd7fddccc"


def test_summary_matches_original_verified_archive_and_rare_allele_identities(audit):
    receipt=json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["evidence_rank"]=="RETROSPECTIVE_EXACT_ORIGINAL_GENOME_PATHWISE_NO_CAUSAL_SELECTION_DRIFT_SHARE"
    assert receipt["n_original_founder_ids_in_exceptions"]==2
    assert receipt["n_original_source_pairs_in_exceptions"]==2
    assert receipt["no_new_biological_futures"] is True
    assert receipt["new_independent_population_updates"]==0
    assert receipt["new_preregistered_tests"]==0
    for x in audit["episodes"]:
        key=(x["initial_A"],x["original_founder_seed"],x["demographic_repeat"])
        old=next(y for y in receipt["exceptions"]
            if (y["initial_A"],y["founder_seed"],y["demographic_repeat"])==key)
        assert x["source_original_prefix_sha256"]==old["source_census30_genotype_sha256"]
        assert x["original_low_I_copies_at_shock"]==old["starting_copies_out_of_96"]
        for arm in ("control","decline"):
            a=x["arms"][arm]
            b=old["arms"][arm]
            assert a["first_original_census_low_I_allele_lost"]==b["first_census_allele_absent"]
            assert a["n_censuses_I_segregating"]==b["n_source_generations_with_I_segregation"]
            assert a["sum_original_path_expected_low_I_frequency_shift"]==pytest.approx(
                b["cumulative_expected_low_I_frequency"],abs=1e-12)
            assert a["sum_original_path_realization_low_I_fraction_residual"]==pytest.approx(
                b["cumulative_realization_low_I_residual"],abs=1e-12)
            assert a["last_low_I_copy_count_before_loss"]==b["last_count_before_loss"]
