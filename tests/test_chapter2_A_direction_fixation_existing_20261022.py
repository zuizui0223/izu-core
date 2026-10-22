"""Read-only, source-bound checks of A direction and fixation synthesis."""
import copy
import json
from pathlib import Path

import pytest

from scripts.summarize_chapter2_A_direction_fixation_existing_20261022 import (
    ROOT, SOURCES, STATUS, run, main
)


def test_reconcile_160x160_fixation_and_neutral_direction():
    d = run(ROOT)
    assert d["status"] == STATUS
    assert d["new_biological_updates"] == 0
    assert d["new_statistical_tests"] == 0
    assert d["independent_source_cohorts_are_not_pooled"]
    x = d["main_B8_160x160"]
    assert x["fixed_expression"]["fixed_values"] == {
        "0.25": 5332, "0.5": 5187, "0.75": 5145}
    assert x["evolving_expression"]["fixed_values"] == {
        "0.5": 275, "0.75": 25307}
    assert x["fixed_expression"]["unfixed_at_census80"] == 9936
    assert x["evolving_expression"]["unfixed_at_census80"] == 18
    assert x["high_A_fixation_policy_difference_percentage_points"] == 78.7578125
    assert x["fixation_any_policy_difference_percentage_points"] == 38.7421875
    k = d["K32_one_history"]
    assert k["historical_visitor_histories"] == 1
    assert k["source_minus_neutral_A_frequency"] == pytest.approx(.47607421875)
    assert k["source_end_high_A_allele_frequency"] > .97
    assert k["neutral_same_N_end_high_A_allele_frequency"] == pytest.approx(.501190185546875)
    s = k["separate_pathwise_run"]
    assert s["expected_reproductive_filtering"] + s["finite_inheritance_sampling_residual"] == pytest.approx(s["realized_change"])
    m = k["separate_mean_and_census_matched_comparator"]
    assert m["source_end_variance"] > m["synthetic_control_end_variance"]
    assert d["distinct_128_by_four_repeat_cohort"]["unanimous_A_contrasts_equal_to_zero"] == 103


def test_analytical_no_visitors_pays_direct_maternal_A_benefit():
    x = run(ROOT)["analytical_no_visitor_case"]
    p = x["viable_self_production_by_A"]
    assert p["0.25"] < p["0.5"] < p["0.75"]
    assert p["0.75"] / p["0.5"] == pytest.approx(1.283017990961134)
    assert "1/A - A" in x["derivative_of_log_payoff"]


def test_reject_changed_evidence_before_synthesis(tmp_path):
    for path in SOURCES.values():
        dst = tmp_path / path
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ROOT / path).read_bytes())
    bad = tmp_path / SOURCES["variation"]
    source = json.loads(bad.read_text())
    row = next(r for r in source["results"] if r["budget"] == "B8"
               and r["policy"] == "evolving" and r["trait"] == "A")
    row["fixed_value_counts"][0]["count"] += 1
    bad.write_text(json.dumps(source))
    with pytest.raises(ValueError, match="fixation outcome categories"):
        run(tmp_path)


def test_output_is_read_only_and_never_overwrites(tmp_path, monkeypatch):
    from scripts import summarize_chapter2_A_direction_fixation_existing_20261022 as m
    out = tmp_path / "SUMMARY.json"
    monkeypatch.setattr("sys.argv", ["audit", "--root", str(ROOT), "--output", str(out)])
    m.main()
    result = json.loads(out.read_text())
    assert result["status"] == STATUS
    with pytest.raises(FileExistsError):
        m.main()
