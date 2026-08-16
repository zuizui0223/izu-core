#!/usr/bin/env python3
"""Verify the live Seychelles acquisition/analysis against the checked summary."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = ROOT / "artifacts" / "seychelles_pollination_effectiveness"
CHECKED = ROOT / "data" / "results" / "seychelles_pollination_effectiveness_summary.json"


def close(left: float, right: float, tol: float = 1e-12) -> None:
    if not math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=tol):
        raise AssertionError(f"numeric drift: {left!r} != {right!r}")


def main() -> None:
    acquisition = json.loads((ARTIFACT_ROOT / "summary.json").read_text(encoding="utf-8"))
    live = json.loads((ARTIFACT_ROOT / "analysis" / "summary.json").read_text(encoding="utf-8"))
    checked = json.loads(CHECKED.read_text(encoding="utf-8"))

    assert acquisition["dataset_doi"] == checked["dataset_doi"]
    live_hashes = {row["name"]: row["sha256"] for row in acquisition["files"]}
    assert live_hashes == checked["source_file_sha256"]
    assert live["scale"] == checked["scale"]

    for plant in checked["plants"]:
        live_plant = live["plants"][plant]
        fixed = checked["plants"][plant]
        assert live_plant["published_overall_effectiveness_headline"] == fixed["published_overall_effectiveness_headline"]
        assert live_plant["source_rows"]["census"] == fixed["census_rows"]
        assert live_plant["source_rows"]["flower_contact"] == fixed["flower_contact_rows"]
        assert live_plant["reproductive_experiments"]["single_visit_exclusion_n"] == fixed["single_visit_rows"]
        assert live_plant["reproductive_experiments"]["breeding_treatment_n"] == fixed["breeding_rows"]

    for plant in ("Polyscias crassa", "Syzygium wrightii"):
        close(
            live["plants"][plant]["census_quantity"]["ant_disturbance"]["disturbed_to_undisturbed_rate_ratio"],
            checked["plants"][plant]["ant_disturbed_to_undisturbed_non_ant_visit_rate_ratio"],
        )

    p_live = live["plants"]["Polyscias crassa"]["reproductive_experiments"]["single_visit_quality"]
    for guild, expected in checked["plants"]["Polyscias crassa"]["single_visit_mature_fruit"].items():
        got = p_live[guild]["mature_or_recorded_fruit"]
        assert got["successes"] == expected["successes"] and got["n_observed"] == expected["n"]
        close(got["proportion"], expected["proportion"])

    s_live = live["plants"]["Syzygium wrightii"]["reproductive_experiments"]
    for guild, expected in checked["plants"]["Syzygium wrightii"]["single_visit_seed_positive"].items():
        got = s_live["single_visit_quality"][guild]["seed_positive"]
        assert got["successes"] == expected["successes"] and got["n_observed"] == expected["n"]
        close(got["proportion"], expected["proportion"])
    s_auto = s_live["breeding_treatments"]["Auto"]
    s_expected = checked["plants"]["Syzygium wrightii"]["source_labeled_auto_treatment"]
    assert s_auto["n_rows"] == s_expected["n"]
    assert s_auto["green_fruit"]["successes"] == s_expected["green_fruit_successes"]
    close(s_auto["green_fruit"]["proportion"], s_expected["green_fruit_proportion"])
    assert s_auto["seed_positive"]["successes"] == s_expected["seed_positive_successes"]
    close(s_auto["seed_positive"]["proportion"], s_expected["seed_positive_proportion"])

    t_live = live["plants"]["Thespesia populnea"]["reproductive_experiments"]
    for guild, expected in checked["plants"]["Thespesia populnea"]["single_visit_recorded_fruit"].items():
        got = t_live["single_visit_quality"][guild]["mature_or_recorded_fruit"]
        assert got["successes"] == expected["successes"] and got["n_observed"] == expected["n"]
        close(got["proportion"], expected["proportion"])
    t_auto = t_live["breeding_treatments"]["Auto"]
    t_expected = checked["plants"]["Thespesia populnea"]["source_labeled_auto_treatment"]
    assert t_auto["n_rows"] == t_expected["n"]
    assert t_auto["mature_or_recorded_fruit"]["successes"] == t_expected["fruit_successes"]
    close(t_auto["mature_or_recorded_fruit"]["proportion"], t_expected["fruit_proportion"])
    assert t_auto["seed_positive"]["successes"] == t_expected["seed_positive_successes"]
    close(t_auto["seed_positive"]["proportion"], t_expected["seed_positive_proportion"])

    print("Seychelles checked real-data summary reproduced exactly.")


if __name__ == "__main__":
    main()
