"""Source-native original R2 I allelic opportunity versus observed fixation.

Native CI replays only the ORIGINAL 22 pre-existing census30 and postshock
source trajectories from SHA-locked RNG+genotypes. Archive ZIP replay is an
optional second independent input, not a source of new biological experiments.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from scripts.audit_chapter2_r2_original_I_accessibility_20261024 import (
    STATUS, _finalize, analyze_original_zip, replay_original_native
)
from scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 import replay

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"docs/audits/CHAPTER2_R2_STANDING_I_ALLELE_ACCESS_20261024.json"
PRIOR=ROOT/"docs/audits/CHAPTER2_R2_FROZEN_AM_I_SORTING_20261023.json"


@pytest.fixture(scope="module")
def source_native():
    return replay_original_native()


def test_original_model_genomes_and_paired_fixed_I_are_reproduced(source_native):
    x=source_native
    r=json.loads(RECEIPT.read_text(encoding="utf-8"))
    p=json.loads(PRIOR.read_text(encoding="utf-8"))
    assert x["status"]==STATUS==r["status"]
    assert x["original_actions_run_id"]==r["source_actions_run_id"]==39233450099
    assert x["original_zip_sha256"]==r["source_zip_sha256"]
    assert x["original_protocol_sha256"]==r["source_protocol_sha256"]
    assert x["original_source_commit"]==r["source_commit"]
    assert x["n_original_paths"]==r["original_384_biological_trajectories"]==384
    assert x["n_original_paired_futures"]==r["original_matched_futures"]==192
    assert x["n_strict_AM_fixed_I_polymorphic_strong_history_source_cells"]==22
    assert p["totals"]["strong_pairs"]==22
    assert x["n_distinct_founder_seeds"]==r["founders_in_this_retro_selected_subset"]==11
    assert x["n_decline_fixed_to_lowest_I_allele_present_at_shock"]==20
    assert x["n_decline_fixed_to_other_higher_I_allele"]==2
    assert x["decline_fixed_I_value_counts"]==r["strata"]["strong_prior_pollen_limitation_AM_fixed_I_polymorphic_at_t30"]["decline_fixed_numerical_I_value_counts"]
    assert x["by_initial_A"]==[
        {"initial_A":0.3,"n_source_cells":16,"n_decline_fixed_to_lowest_accessible_I":15,"n_fixed_above_lowest_accessible_I":1},
        {"initial_A":0.5,"n_source_cells":6,"n_decline_fixed_to_lowest_accessible_I":5,"n_fixed_above_lowest_accessible_I":1},
    ]
    assert sum(row["decline_fixed_to_lowest_accessible_I_value"] for row in x["rows"])==20
    assert all(len(row["original_prefix_state_sha256"])==64 for row in x["rows"])
    assert all(sum(row["I_allele_counts_at_shock"])==96 for row in x["rows"])
    assert all(row["lowest_I_allele_count_out_of_96"] / 96 == row["lowest_I_allele_fraction"] for row in x["rows"])
    assert x["new_biological_population_updates"]==x["new_statistical_tests"]==0
    assert r["new_population_updates"]==r["new_independent_biological_experiments"]==0


def test_both_exceptions_reconcile_original_source_and_per_parent_expected_selection(source_native):
    x=source_native
    r=json.loads(RECEIPT.read_text(encoding="utf-8"))
    expected={
        (0.3,810102,4):(6,0.75,"2286da6eb42e60831cc61c790a191af67f082a3a3f99a9c50a2af025bf811b17",-0.0011443702993481075),
        (0.5,810110,3):(4,0.5,"3f5a9895a8c11772783c76fa6ecfd024a7e4f888f8df23f90246e7d72b6f9e96",-0.0007706194516954867),
    }
    assert len(x["exceptions"])==len(r["exceptions"])==2
    for source in x["exceptions"]:
        k=(source["initial_A"],source["original_founder_seed"],source["nested_demographic_repeat"])
        copies,fixed,sha,first_expected=expected[k]
        assert source["lowest_I_allele_count_out_of_96"]==copies
        assert source["decline_terminal_fixed_I_value"]==fixed
        assert source["original_prefix_state_sha256"]==sha
        assert source["terminal_I_treatment_contrast_exact_zero"] is True
        assert source["decline_fixed_to_lowest_accessible_I_value"] is False
        match=next(a for a in r["exceptions"] if (a["initial_A"],a["original_founder_seed"],a["nested_demographic_repeat"])==k)
        assert match["lowest_I_allele_fraction_at_shock"]==pytest.approx(copies/96,abs=1e-15)
        assert match["first_generation_expected_I_decline_minus_control"]==pytest.approx(first_expected,abs=1e-14)
    # Verify negative expected sorting from the full reconstructed ORIGINAL t30
    # genomes, including the TWO exceptions that ended at higher I alleles.
    static=replay()
    static_rows={(row["initial_A"],row["founder_seed"],row["demographic_repeat"]):row
                 for row in static["rows"] if row["baseline"]=="strong_baseline_limitation"}
    assert len(static_rows)==22
    for k,(_,_,_,expected) in expected.items():
        assert static_rows[k]["decline_minus_control_expected_I_sorting"]==pytest.approx(expected,abs=1e-14)
        assert static_rows[k]["decline_minus_control_expected_I_sorting"]<0
    assert all(row["decline_minus_control_expected_I_sorting"]<0 for row in static_rows.values())


def test_observed_count_gap_is_not_a_preregistered_population_threshold(source_native):
    x=source_native
    r=json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert x["min_lowest_allele_count_among_lower_fixations"]==16
    assert x["max_lowest_allele_count_among_higher_fixations"]==6
    assert r["source_sample_selected_after_original_outcomes"] is True
    assert r["new_significance_tests"]==0
    assert "NOT_A_VALIDATED_THRESHOLD" in r["evidence_rank"]
    assert any("No universal or prospectively" in s for s in r["limitations"])
    winners=[row for row in x["rows"] if row["decline_fixed_to_lowest_accessible_I_value"]]
    losers=x["exceptions"]
    assert min(row["lowest_I_allele_fraction"] for row in winners)==pytest.approx(16/96,abs=1e-15)
    assert max(row["lowest_I_allele_fraction"] for row in losers)==pytest.approx(6/96,abs=1e-15)
    # These are descriptive original-source values, NOT a derived 10% rule.


def test_corrupt_source_access_copy_count_fails_closed(source_native):
    rows=copy.deepcopy(source_native["rows"])
    bad=next(r for r in rows if not r["decline_fixed_to_lowest_accessible_I_value"])
    bad["lowest_I_allele_count_out_of_96"]=12
    with pytest.raises(AssertionError,match="two original high-I fixed exceptions changed"):
        _finalize(rows)


def test_optional_full_original_actions_ZIP_is_independent_grounding(source_native):
    path=os.environ.get("CHAPTER2_R2_384_ORIGINAL_ZIP")
    if not path:
        pytest.skip("Authentic source 1.86MB ZIP remains external; native hashes always tested")
    raw=analyze_original_zip(Path(path))
    assert raw.keys()==source_native.keys()
    assert raw["n_decline_fixed_to_lowest_I_allele_present_at_shock"]==20
    assert len(raw["rows"])==len(source_native["rows"])==22
    for a,b in zip(raw["rows"],source_native["rows"]):
        assert a.keys()==b.keys()
        for key in a:
            if isinstance(a[key],float):
                assert a[key]==pytest.approx(b[key],abs=1e-12)
            else:
                assert a[key]==b[key]
