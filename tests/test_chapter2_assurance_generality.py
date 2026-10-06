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
