"""The island-history pilot is isolated from the confirmed Chapter 2 evidence."""
from pathlib import Path
import hashlib
import json

import pytest

from scripts.run_chapter2_island_history_transplant import (
    case_id, census, declared_groups, load_design, snapshot_digest,
)
from scripts.summarize_chapter2_island_history_transplant import (
    investment, mean_or_none, paired_difference, summarize,
)
from scripts.model3_island.run import founders_from_spec

ROOT = Path(__file__).resolve().parents[1]


def test_pilot_design_is_preoutcome_and_separate_from_confirmation():
    d, source = load_design()
    assert d["status"] == "exploratory_pilot_protocol_locked_before_execution"
    assert set(d["settings"]) == set(source["settings"])
    assert set(d["modes"]) == {"fixed", "evolving"}
    assert set(d["pre_environments"]) == {"near", "far"}
    assert set(d["post_environments"]) == {"near", "far"}
    assert d["pre_mutation_probability"] == 0.01
    assert d["campaign"]["distinct_visitor_histories"] == 4
    assert len(declared_groups(d)) == 128
    assert len({case_id(g, post, rate)
                for g in declared_groups(d)
                for post in d["post_environments"]
                for rate in d["post_mutation_probabilities"]}) == 512


def test_census_preserves_trait_variances_and_empty_endpoints():
    state = founders_from_spec(
        dict(count=4, draw_count=4, means=[0.5, 0.5, 0.5],
             sd=0.1, birth_year=0), 20261008
    )
    row = census(state)
    assert row["count"] == 4
    assert len(row["traits"]) == 3
    assert len(row["trait_variances"]) == 3
    assert len(row["allele_variances"]) == 3
    assert snapshot_digest(state) == snapshot_digest(state)
    assert mean_or_none([None, 1., 3.]) == 2
    assert paired_difference(None, 4.) is None
    assert paired_difference(4., 1.) == 3.


def test_pilot_statistical_guard_preserves_history_level_units():
    d, _ = load_design()
    # Synthetic fixtures test only the readout contracts, never the science.
    records = {}
    for group in declared_groups(d):
        setting, h, rep, mode, pre = group
        for post in d["post_environments"]:
            for mu in d["post_mutation_probabilities"]:
                row = {
                    "setting": setting, "visitor_history_seed": h,
                    "demographic_repeat_seed": rep, "assurance_mode": mode,
                    "pre_environment": pre,
                    "switch_genetic_snapshot_sha256": f"{setting}:{h}:{rep}:{mode}:{pre}",
                    "switch": {"count": 48, "traits": [.5, .5, .5]},
                    "end": {"count": 48, "traits": [.5, .4 if pre == "far" else .5, .5]},
                    "immediate_post_switch_reproduction": {
                        "maternal_viable_per_plant": 2 if pre == "far" else 3
                    },
                }
                records[case_id(group, post, mu)] = row
    output = summarize(d, records)
    assert output["status"] == "completed_exploratory_screen_not_confirmatory"
    assert len(output["ecological_contrast"]) == 4 * 2 * 2 * 2
    for row in output["ecological_contrast"]:
        assert row["independent_histories"] == 4
        assert row["nested_pairs"] == 8
        assert row["end_investment_far_history_minus_near_history"] == pytest.approx(-.1)
        assert row["immediate_maternal_viable_far_history_minus_near_history"] == -1
    assert all(r["identical_switch_pairs"] == 8 for r in output["post_mutation_contrast"])
