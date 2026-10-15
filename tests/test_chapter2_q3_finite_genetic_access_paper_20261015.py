"""Read-only paper admission of the verified Model 3 Q3 source evidence.

This checks original scientific readout/independent receipt identities and
manuscript denominators. It does not regenerate biological trajectories,
refit source models or infer a causal genetic-drift effect.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import math
import statistics
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "data/results/model3_ch2_bridge_prospective_frozen_20260927.json"
ACCESS = ROOT / "data/results/directional_access_20261013/READOUT.json"
ACCESS_REVIEW = ROOT / "data/results/directional_access_20261013/INDEPENDENT_REVIEW.json"
LOSS = ROOT / "data/results/low_allele_loss_20261014/extracted/READOUT.json"
LOSS_REVIEW = ROOT / "data/results/low_allele_loss_20261014/INDEPENDENT_REVIEW.json"
LOSS_CASES = ROOT / "data/results/low_allele_loss_20261014/extracted/ALL_CASES.csv"
PAPER = ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
SI = ROOT / "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
ROUTE = ROOT / "data/design/chapter2_one_paper_route_20261010.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _check_counts(access: dict, loss: dict) -> None:
    """These are overlapping source cases, NOT two independent populations."""
    assert access["cases"] == loss["cases"] == 2304
    assert access["ever_excluded"] == loss["eligible_loss"] == 1238
    assert access["excluded_before_fixation"] == 703
    assert access["excluded_with_expressed_variance"] == 703
    assert access["excluded_at_fixation"] == 535
    assert access["excluded_before_fixation"] + access["excluded_at_fixation"] == 1238
    assert access["missing_I_excluded_before_fixation"] == 702
    assert loss["statuses"] == {"no_exclusion": 1066, "eligible_loss": 1238}
    assert loss["direction_counts"] == {
        "favouring_needed": 315,
        "opposing_needed": 923,
        "screened_near_zero": 0,
    }
    assert sum(loss["direction_counts"].values()) == loss["eligible_loss"]
    assert access["cases_sha256"] == loss["input_cases_sha256"]
    assert access["new_biological_histories"] == loss["new_biological_histories"] == 0
    assert loss["reproduction_advances"] == 0


def test_source_rank_and_original_independent_receipts() -> None:
    access, loss = _load(ACCESS), _load(LOSS)
    _check_counts(access, loss)
    a_review, l_review = _load(ACCESS_REVIEW), _load(LOSS_REVIEW)
    assert a_review["status"] == "ALL2304_DIRECTIONAL_SUPPORT_AND_ANCESTRY_INDEPENDENTLY_VERIFIED"
    assert l_review["status"] == "ALL2304_LAST_LOSS_RECORDS_INDEPENDENTLY_VERIFIED"
    assert a_review["cases"] == l_review["cases"] == 2304
    assert l_review["eligible_loss"] == 1238
    assert l_review["gamete_enumerations"] == 10_994_304
    assert a_review["readout_sha256"] == hashlib.sha256(ACCESS.read_bytes()).hexdigest()
    assert l_review["readout_sha256"] == hashlib.sha256(LOSS.read_bytes()).hexdigest()
    assert a_review["cases_sha256"] == access["cases_sha256"]
    assert l_review["cases_sha256"] == loss["cases_sha256"]
    assert a_review["new_biological_histories"] == l_review["new_biological_histories"] == 0


@pytest.mark.parametrize("field,value", [
    ("excluded_before_fixation", 704),
    ("excluded_at_fixation", 534),
    ("missing_I_excluded_before_fixation", 703),
    ("ever_excluded", 1237),
])
def test_reject_altered_directional_source_counts(field: str, value: int) -> None:
    access, loss = _load(ACCESS), _load(LOSS)
    before = copy.deepcopy(access)
    before[field] = value
    with pytest.raises(AssertionError):
        _check_counts(before, loss)


def test_reject_false_independent_loss_denominator() -> None:
    access, loss = _load(ACCESS), _load(LOSS)
    altered = copy.deepcopy(loss)
    altered["eligible_loss"] = 703
    with pytest.raises(AssertionError):
        _check_counts(access, altered)
    altered = copy.deepcopy(loss)
    altered["direction_counts"]["favouring_needed"] += 1
    with pytest.raises(AssertionError):
        _check_counts(access, altered)


def test_source_selected_loss_probabilities_follow_actual_parental_lottery() -> None:
    """Loss-selected conditional probabilities: NOT all-trajectory failure rates."""
    source = _load(LOSS)
    raw = LOSS_CASES.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == source["cases_sha256"]
    records = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    assert len(records) == source["cases"] == 2304
    eligible = [r for r in records if r["transition_status"] == "eligible_loss"]
    assert len(eligible) == source["eligible_loss"] == 1238
    groups = {
        k: [r for r in eligible if r["loss_direction"] == k]
        for k in ("favouring_needed", "opposing_needed")
    }
    assert {k: len(v) for k, v in groups.items()} == {
        "favouring_needed": 315, "opposing_needed": 923
    }
    for r in eligible:
        n = int(r["retained_resident_count"])
        assert n == 48
        q0 = float(r["q0"])
        probability = float(r["conditional_loss_probability"])
        assert math.isclose(probability, q0**n, rel_tol=0, abs_tol=1e-13)
        frequency = float(r["expected_frequency"])
        current = float(r["current_frequency"])
        weighting = float(r["parent_weighting_response"])
        assert math.isclose(frequency-current, weighting, rel_tol=0, abs_tol=1e-13)
        assert math.isclose(
            float(r["sampling_transmission_residual"]), -frequency, rel_tol=0, abs_tol=1e-13
        )
        assert weighting > 0 if r["loss_direction"] == "favouring_needed" else weighting < 0
    fav, opp = groups["favouring_needed"], groups["opposing_needed"]
    assert statistics.median(int(r["needed_copies_before"]) for r in fav) == 2
    assert statistics.median(float(r["expected_frequency"]) for r in fav) == pytest.approx(
        0.021133482709469034, rel=0, abs=1e-13
    )
    assert statistics.median(float(r["conditional_loss_probability"]) for r in fav) == pytest.approx(
        0.3260053119547402, rel=0, abs=1e-13
    )
    assert statistics.median(float(r["conditional_loss_probability"]) for r in opp) == pytest.approx(
        0.38693881062178476, rel=0, abs=1e-13
    )


def test_original_prospective_bridge_remains_a_distinct_cohort() -> None:
    bridge = _load(BRIDGE)
    assert bridge["status"] == "frozen_complete_prospective_model3_ch2_bridge"
    assert bridge["provenance"]["histories_verified"] == 128
    assert bridge["provenance"]["cases_verified"] == 24576
    reports = {(r["intervention"], r["model"]): r for r in bridge["reports"]}
    assert reports["natural", "density"]["mean"] == pytest.approx(-0.4510, abs=0.00005)
    assert reports["natural", "individual"]["mean"] == pytest.approx(-0.1446, abs=0.00005)
    assert reports["natural", "density"]["mixed_counts"] == [0, 0, 0]
    assert reports["natural", "individual"]["mixed_counts"] == [12, 8, 1]
    assert reports["richness_matched", "density"]["mixed_counts"][0] == 16
    assert reports["richness_matched", "individual"]["mixed_counts"][0] == 68
    assert reports["visitor_pooled", "individual"]["mixed_counts"][0] == 0
    assert reports["visitor_pooled", "density"]["mixed_counts"][0] == 0
    assert reports["large_plant_capacity", "individual"]["mixed_counts"][0] == 1
    assert reports["natural", "individual"]["repeat_disagreements"][0] == 97


def test_manuscript_si_and_route_preserve_denominators_and_limitations() -> None:
    paper, si, route = PAPER.read_text(encoding="utf-8"), SI.read_text(encoding="utf-8"), _load(ROUTE)
    main = paper.split("# Introduction", 1)[1].split("# Primary figure assembly and captions", 1)[0]
    abstract = paper.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    q3 = paper.split("## Q3 —", 1)[1].split("## Q4 —", 1)[0]
    s14 = si.split("## S14.", 1)[1].split("## S15.", 1)[0]
    assert len(main.split()) == 4991
    assert route["journal_fit"]["current_main_text_words"] == len(main.split())
    assert route["journal_fit"]["current_integrated_main_words"] == len(main.split())
    assert len(main.split()) < route["journal_fit"]["ecology_letters_letter_main_max"] == 5000
    assert len(abstract.split()) == route["journal_fit"]["current_abstract_words"] == 148
    assert route["status"] == "active_unified_manuscript_not_submitted"
    for token in ("2,304", "1,238", "703", "535", "315", "923"):
        assert token in q3 and token in s14
    assert "not independent samples or a causal estimate of drift" in q3
    assert "Density is not the stochastic expectation of the ABM" in q3
    assert "Source-separated Q3 evidence map" in s14
    assert "before complete fixation" in s14
    assert "do not" in s14.lower() or "not" in s14.lower()
    assert "near–far" in main
    assert "not submitted" in paper
    assert "Three gates intervene" in paper
    assert "not one experimentally established Q1-to-Q4 mediation chain" in paper
    assert "not a natural mediation analysis" in paper
    assert "conditional expected frequency e" in q3
    assert "median of **two necessary low-I allele copies**" in q3
    assert "median **0.326 probability" in q3
    assert "strictly negative realized sampling/transmission residual (−e)" in q3
    assert "no-I-mutation and no-immigration law" in q3
    assert "The mechanism: from reproductive returns to irreversible loss of a response option" in s14
    assert "e-p>0" in s14
    assert "0.3260053" in s14 and "0.3869388" in s14
    assert "outcome-selected set of loss transitions" in s14
    assert "conditional parental weighting and realized inheritance point in opposite directions" in s14
    assert "not a continuous causal mediation estimated in a single synthetic cohort" in s14
    assert "genetically explicit plant–pollinator model" in abstract
    assert "Both regimes remained pollen-limited." in abstract
