import json
from pathlib import Path

from scripts.run_chapter2_1005_confirmatory_replication import declared_tasks, load_design, seed_ranges

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/chapter2_1005_confirmatory_replication_20261006.json"


def test_confirmatory_design_is_frozen_and_independent():
    design = load_design(DESIGN)
    histories, repeats = seed_ranges(design)
    assert list(histories) == list(range(26100601, 26100665))
    assert list(repeats) == list(range(26101601, 26101609))
    assert set(histories).isdisjoint(range(76001, 76065))
    assert set(repeats).isdisjoint(range(7101, 7109))
    assert design["primary_cell"] == {
        "reproductive_setting": "assurance_cost",
        "assurance_timing": "delayed",
        "assurance_cost": 0.5,
        "mutation_probability": 0.01,
        "rationale": "This is the cell in which the 51/64 discovery was defined; it is frozen before confirmatory outcomes are generated.",
    }


def test_confirmatory_campaign_has_no_outcome_dependent_extension():
    design = load_design(DESIGN)
    tasks = declared_tasks(design)
    assert len(tasks) == 4096
    assert sum(task[0] == "sequence" for task in tasks) == 2048
    assert sum(task[0] == "fixed_assurance" for task in tasks) == 2048
    assert design["sequence_campaign"]["primary_threshold"] == 0.05
    assert design["sequence_campaign"]["thresholds"] == [0.025, 0.05, 0.1]
    assert design["sequence_campaign"]["sustained_periods"] == 20
    assert design["sequence_campaign"]["tie_tolerance_periods"] == 5
    assert design["reporting_rules"]["no_retuning"].startswith("No seed extension")


def test_primary_success_rules_are_predeclared():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert "proportion >0.50" in design["sequence_campaign"]["primary_success_rule"]
    assert "lower bound >0.50" in design["sequence_campaign"]["primary_success_rule"]
    assert "both investment estimands must be negative" in design["fixed_assurance_campaign"]["primary_success_rule"]
    assert "upper bounds must be <0" in design["fixed_assurance_campaign"]["primary_success_rule"]
    assert design["reporting_rules"]["independent_n"].startswith("64 visitor histories")
