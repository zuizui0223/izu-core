"""Regression guards for distinct Q3 finite-realization evidence families.

Only read previously frozen committed numerical receipts. These checks cannot
calculate causal genetic drift, rerun the plant model or establish island rates.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "data/results/model3_ch2_bridge_prospective_frozen_20260927.json"
ACCESS = ROOT / "data/results/directional_access_20261013/READOUT.json"
LOSS = ROOT / "data/results/low_allele_loss_20261014/extracted/READOUT.json"
PAPER = ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
NOTE = ROOT / "docs/CHAPTER2_Q3_FINITE_GENETIC_ACCESS_AND_REALIZATION_20261015.md"


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def test_bridge_effects_count_history_units_not_cases():
    d = read_json(BRIDGE)
    assert d["provenance"]["histories_verified"] == 128
    assert d["provenance"]["cases_verified"] == 24576
    reports = {(x["intervention"], x["model"]): x for x in d["reports"]}
    assert len(reports) == 8
    a = reports["natural", "individual"]
    b = reports["natural", "density"]
    assert round(a["mean"], 4) == -0.1446
    assert round(b["mean"], 4) == -0.4510
    assert a["mixed_counts"] == [12, 8, 1]
    assert b["mixed_counts"] == [0, 0, 0]
    assert reports["richness_matched", "individual"]["mixed_counts"] == [68, 59, 18]
    assert reports["richness_matched", "density"]["mixed_counts"] == [16, 1, 0]
    assert abs(reports["richness_matched", "individual"]["mean"] - .0333) < .0001
    assert abs(reports["richness_matched", "density"]["mean"] - .0338) < .0001
    assert reports["visitor_pooled", "individual"]["mixed_counts"] == [0, 0, 0]
    assert reports["visitor_pooled", "density"]["mixed_counts"] == [0, 0, 0]
    assert reports["large_plant_capacity", "individual"]["mixed_counts"] == [1, 1, 0]
    assert "not a visitor-community control" in d["prospective_answers"]["finite_plant_population"]["qualification"]
    assert "identity persistence" in d["prospective_answers"]["dynamic_realized_richness_matching"]["qualification"]


def test_low_allele_access_and_expected_transmission_are_different_denominators():
    a, b = read_json(ACCESS), read_json(LOSS)
    assert a["cases"] == b["cases"] == 2304
    assert len(a["cells"]) == len(b["cells"]) == 18
    assert a["ever_excluded"] == b["eligible_loss"] == 1238
    assert a["excluded_before_fixation"] == 703
    assert a["excluded_at_fixation"] == 535
    assert 703 + 535 == 1238
    assert a["excluded_with_expressed_variance"] == 703
    assert a["missing_I_excluded_before_fixation"] == 702
    assert b["statuses"] == {"no_exclusion": 1066, "eligible_loss": 1238}
    assert b["direction_counts"] == {
        "favouring_needed": 315, "opposing_needed": 923, "screened_near_zero": 0
    }
    assert sum(b["direction_counts"].values()) == 1238
    assert a["original_categories"] == b["original_categories"]
    assert a["outer_sha256"] == b["original_outer_sha256"]
    assert a["cases_sha256"] == b["input_cases_sha256"]
    assert a["new_biological_histories"] == b["new_biological_histories"] == 0
    assert b["reproduction_advances"] == 0
    assert "NOT_CAUSAL_LOSS_ATTRIBUTION" in a["status"]
    assert "NOT_HISTORICAL_CAUSAL_SHARES" in b["status"]


def test_unified_q3_makes_specific_positive_claim_without_drifts_or_survival_overreach():
    paper = PAPER.read_text(encoding="utf-8")
    note = NOTE.read_text(encoding="utf-8")
    q3 = paper.split("## Q3 — Realization", 1)[1].split("## Q4 — Persistence", 1)[0]
    q4 = paper.split("## Q4 — Persistence", 1)[1].split("# Discussion", 1)[0]
    discussion = paper.split("# Discussion", 1)[1].split("# Conclusion", 1)[0]
    for item in ("703 before investment-allele fixation", "1,238 first exclusions",
                 "315", "conditional parental weighting increased the expected frequency", "S14"):
        q3 = q3.replace("**", "")
        assert item in q3
    assert "overlapping, differently conditioned diagnostics" in q3
    assert "not independent samples or a causal estimate of drift" in q3
    assert "drift" in discussion and "Mendelian" in paper
    assert "not the stochastic expectation of the ABM" in q3
    assert "+0.007746" in q4
    assert "without demonstrating that naturally" in paper.split("# Conclusion", 1)[1] or "not" in q4.lower()
    for term in ("128 original visitor-history", "2,304 original histories",
                 "**703 histories**", "**315/1,238**", "not a new experiment"):
        assert term.lower() in note.lower()


def test_original_labels_not_reinterpreted_as_universal_island_experiments():
    note = NOTE.read_text(encoding="utf-8").replace("**", "")
    assert "not a pure independent causal" in note.lower() or "not pure independent causal" in note.lower() or "not pure independent causal contributions" in note.lower() or "not pure independent causal" in note.lower()
    assert "not" in note.lower() and "stochastic expectation" in note.lower()
    assert "different denominator" in note.lower() or "not a subset definition" in note.lower()
    assert "same run" in note.lower()
    assert "no new model 3 biological updates" in note.lower()
