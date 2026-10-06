import json
from pathlib import Path

from scripts.run_chapter2_assurance_generality import declared_tasks, load_design
from scripts.summarize_chapter2_assurance_generality import adjudicate

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_assurance_generality_20261006.json"


def test_generality_design_is_frozen_and_complete():
    design = load_design(DESIGN)
    assert design["status"] == "frozen_before_generality_execution"
    assert set(design["settings"]) == {
        "delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"
    }
    assert design["main_campaign"]["visitor_history_seeds"]["first"] == 26110601
    assert design["main_campaign"]["demographic_repeat_seeds"]["first"] == 26111601
    tasks = declared_tasks(design)
    assert len(tasks) == 8448
    assert sum(t[0] == "main" for t in tasks) == 8192
    assert sum(t[0] == "structural" for t in tasks) == 256


def test_generality_rule_requires_all_four_for_el_route():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    structural = {"status": "passed"}
    rows = [
        {"setting": name, "passes_frozen_rule": True}
        for name in design["settings"]
    ]
    result = adjudicate(design, rows, structural)
    assert result["status"] == "all_four_confirmed"
    assert result["n_passed"] == 4
    assert "Ecology Letters" in result["journal_route"]


def test_generality_rule_keeps_partial_result_at_je():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    structural = {"status": "passed"}
    rows = [
        {"setting": name, "passes_frozen_rule": name == "assurance_cost"}
        for name in design["settings"]
    ]
    result = adjudicate(design, rows, structural)
    assert result["status"] == "partial_generality"
    assert result["passed_settings"] == ["assurance_cost"]
    assert result["journal_route"].startswith("Journal of Ecology")


RESULT = ROOT / "data/results/chapter2_assurance_generality_20261006.json"


def test_recorded_generality_result_satisfies_the_frozen_rule():
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["status"] == "complete_generality_readout"
    assert result["declared_cases"] == 8448
    assert result["independent_visitor_histories"] == 64
    assert result["nested_demographic_repeats"] == 8
    assert result["structural_control"] == {
        "status": "passed",
        "matched_pairs_checked": 128,
        "mismatches": [],
    }

    expected = {"delayed_control", "prior_selfing", "pollen_discount", "assurance_cost"}
    rows = {row["setting"]: row for row in result["settings"]}
    assert set(rows) == expected
    for row in rows.values():
        assert row["admissible"] is True
        assert row["eligible_histories_fixed_pair"] == 64
        assert row["eligible_histories_four_cell"] == 64
        assert all(
            value == 1.0
            for mode in row["occupancy"].values()
            for value in mode.values()
        )
        fixed = row["fixed_far_minus_near"]
        attenuation = row["attenuation_evolving_minus_fixed"]
        assert fixed["mean"] < 0
        assert fixed["bootstrap95"][1] < 0
        assert attenuation["mean"] > 0
        assert attenuation["bootstrap95"][0] > 0
        assert row["passes_frozen_rule"] is True

    assert result["adjudication"]["status"] == "all_four_confirmed"
    assert result["adjudication"]["n_passed"] == 4
    assert set(result["adjudication"]["passed_settings"]) == expected
    assert result["workflow_provenance"]["artifact_sha256"] == (
        "34bedf03e6cde0b3d7f5140b7f352227b5dd1550c097e66e42022aa9830d3d8c"
    )
