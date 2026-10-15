"""Source-ranked Q3 claim gate; numerical tests use frozen readouts, not simulation."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
ROUTE = ROOT / "data/design/chapter2_one_paper_route_20261010.json"
NOTE = ROOT / "docs/CHAPTER2_Q3_SELECTION_REALIZATION_SOURCE_MAP_20261015.md"


def _json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_bridge_realization_numbers_are_frozen_and_two_axes_distinct() -> None:
    source = _json("data/results/model3_ch2_bridge_prospective_frozen_20260927.json")
    assert source["status"] == "frozen_complete_prospective_model3_ch2_bridge"
    assert source["provenance"]["histories_verified"] == 128
    by_key = {(x["intervention"], x["model"]): x for x in source["reports"]}
    natural_abm = by_key["natural", "individual"]
    natural_density = by_key["natural", "density"]
    matched_abm = by_key["richness_matched", "individual"]
    matched_density = by_key["richness_matched", "density"]
    pooled_abm = by_key["visitor_pooled", "individual"]
    large_abm = by_key["large_plant_capacity", "individual"]
    assert round(natural_abm["mean"], 4) == -0.1446
    assert round(natural_density["mean"], 4) == -0.4510
    assert natural_abm["mixed_counts"] == [12, 8, 1]
    assert natural_density["mixed_counts"] == [0, 0, 0]
    assert natural_abm["repeat_disagreements"][0] == 97
    assert round(matched_abm["mean"], 4) == 0.0333
    assert round(matched_density["mean"], 4) == 0.0338
    assert matched_abm["mixed_counts"][0] == 68
    assert matched_density["mixed_counts"][0] == 16
    assert pooled_abm["mixed_counts"] == [0, 0, 0]
    assert large_abm["mixed_counts"] == [1, 1, 0]
    assert large_abm["repeat_disagreements"][0] == 31


def test_first_exclusion_and_last_loss_keep_nonexchangeable_denominators() -> None:
    access = _json("data/results/directional_access_20261013/READOUT.json")
    loss = _json("data/results/low_allele_loss_20261014/extracted/READOUT.json")
    access_audit = _json("data/results/directional_access_20261013/INDEPENDENT_REVIEW.json")
    loss_audit = _json("data/results/low_allele_loss_20261014/INDEPENDENT_REVIEW.json")
    assert access["cases"] == loss["cases"] == 2304
    assert access["cases_sha256"] == loss["input_cases_sha256"]
    assert access["ever_excluded"] == 1238
    assert access["excluded_before_fixation"] == 703
    assert access["excluded_with_expressed_variance"] == 703
    assert access["excluded_at_fixation"] == 535
    assert access["missing_I_excluded_before_fixation"] == 702
    assert loss["eligible_loss"] == 1238
    assert loss["statuses"]["no_exclusion"] == 1066
    assert loss["direction_counts"] == {
        "favouring_needed": 315,
        "opposing_needed": 923,
        "screened_near_zero": 0,
    }
    assert loss["new_biological_histories"] == loss["reproduction_advances"] == 0
    assert access["new_biological_histories"] == 0
    assert access_audit["status"] == "ALL2304_DIRECTIONAL_SUPPORT_AND_ANCESTRY_INDEPENDENTLY_VERIFIED"
    assert access_audit["parent_homolog_checks"] == 44_236_800
    assert loss_audit["status"] == "ALL2304_LAST_LOSS_RECORDS_INDEPENDENTLY_VERIFIED"
    assert loss_audit["scalar_checks"] == 23_522
    assert loss_audit["gamete_enumerations"] == 10_994_304
    assert loss_audit["producer_imported"] is False


def test_q3_text_has_positive_but_model_bounded_mechanism() -> None:
    paper = PAPER.read_text(encoding="utf-8")
    q3 = paper.split("## Q3 — ", 1)[1].split("## Q4 — ", 1)[0]
    discussion = paper.split("# Discussion", 1)[1].split("# Conclusion", 1)[0]
    note = NOTE.read_text(encoding="utf-8")
    for marker in ("703", "1,238", "315", "923", "0.05", "48 to 192", "3/32", "2/32"):
        assert marker in q3, marker
    assert "before single-allele fixation" in q3
    assert "conditional expected" in q3
    assert "not" in q3.lower() and "drift" in q3.lower()
    assert "different 2,304-history" in q3
    assert "realization filter" in discussion
    assert "expected reproductive contribution to retained inherited alleles" in paper.split("# Conclusion", 1)[1]
    assert "315/1,238" in note and "703 histories" in note
    assert "same 2,304 original histories" in note
    assert "not a drift effect size" in note.lower()
    assert "density is **not** the ABM\'s stochastic expectation" in q3
    assert "do **not** identify pure drift" in q3


def test_paper_fit_and_four_question_route_unchanged() -> None:
    paper = PAPER.read_text(encoding="utf-8")
    route = _json("data/design/chapter2_one_paper_route_20261010.json")
    main = paper.split("# Introduction", 1)[1].split("# Primary figure assembly and captions", 1)[0]
    abstract = paper.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    fit = route["journal_fit"]
    assert len(main.split()) == fit["current_main_text_words"] == fit["current_integrated_main_words"] == 4923
    assert len(abstract.split()) == fit["current_abstract_words"] == fit["current_integrated_abstract_words"] == 143
    assert len(main.split()) <= fit["ecology_letters_letter_main_max"]
    assert len(abstract.split()) <= fit["ecology_letters_letter_abstract_max"]
    assert route["status"] == "active_unified_manuscript_not_submitted"
    assert route["active_manuscript_count"] == 1
    assert "S28" in fit["updated_submission_scope"] and "S29" in fit["updated_submission_scope"]
    assert "## Q1 —" in paper and "## Q2 —" in paper
    assert "## Q3 —" in paper and "## Q4 —" in paper
    assert "K8-versus-K48 moderator" in paper

def test_conditional_parent_sampling_explains_how_rare_alleles_can_disappear() -> None:
    """Only read the frozen *selected* first-loss transitions; not a hazard model."""
    fp = ROOT / "data/results/low_allele_loss_20261014/extracted/ALL_CASES.csv"
    raw = fp.read_bytes()
    loss = _json("data/results/low_allele_loss_20261014/extracted/READOUT.json")
    assert hashlib.sha256(raw).hexdigest() == loss["cases_sha256"]
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    assert len(rows) == 2304
    selected = [r for r in rows if r["transition_status"] == "eligible_loss"]
    assert len(selected) == 1238
    fav = [r for r in selected if r["loss_direction"] == "favouring_needed"]
    assert len(fav) == loss["direction_counts"]["favouring_needed"] == 315
    assert all(float(r["parent_weighting_response"]) > 0.0 for r in fav)
    assert all(float(r["expected_frequency"]) > float(r["current_frequency"]) for r in fav)
    assert all(int(r["retained_resident_count"]) == 48 for r in selected)
    assert all(float(r["observed_change"]) == -float(r["current_frequency"]) for r in fav)
    # In these pre-observed-loss states, the needed allele is often only a
    # handful of homolog copies (48 diploid adults => 96 homologs).
    assert median(int(r["needed_copies_before"]) for r in fav) == 2
    chances = [float(r["conditional_loss_probability"]) for r in fav]
    assert math.isclose(median(chances), 0.3260053119547402, abs_tol=1e-12)
    # This source-law calculation integrates over hypothetical parent and
    # Mendelian draws at the *selected previous state*, not prospective losses.
    assert max(
        abs(float(r["q0"]) ** int(r["retained_resident_count"]) -
            float(r["conditional_loss_probability"]))
        for r in selected
    ) < 1e-12
    q3 = PAPER.read_text(encoding="utf-8").split("## Q3 — ", 1)[1].split("## Q4 — ", 1)[0]
    note = NOTE.read_text(encoding="utf-8")
    assert "two needed allele copies among 96 parental copies" in q3
    assert "median was 0.326" in q3
    assert "loss-selected, one-transition" in q3
    assert "0.3260053119547402" in note
    assert "not a new simulation" in note
