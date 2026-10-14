"""The island-history pilot is isolated from the confirmed Chapter 2 evidence."""
from pathlib import Path
import hashlib
import json

import pytest

from scripts.run_chapter2_island_history_transplant import (
    case_id, census, declared_groups, load_design, run_group, snapshot_digest,
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



def test_one_update_reciprocal_fork_smoke(tmp_path):
    """Real ABM/reproduction smoke; not a scientific result or full pilot."""
    d, source = load_design()
    mini = dict(d, pre_periods=1, post_periods=1)
    group = declared_groups(d)[0]
    run_group(mini, source, group, tmp_path)
    rows = [
        json.loads((tmp_path / (case_id(group, post, mu) + ".json")).read_text())
        for post in d["post_environments"]
        for mu in d["post_mutation_probabilities"]
    ]
    assert len(rows) == 4
    assert len({row["switch_genetic_snapshot_sha256"] for row in rows}) == 1
    assert len({tuple(row["switch"]["traits"]) for row in rows}) == 1
    assert all(row["pre_occupied_censuses"] <= 2 for row in rows)
    assert all(row["post_occupied_censuses"] <= 2 for row in rows)
    assert all(0 <= row["end"]["count"] <= 48 for row in rows)



def test_payoff_factorial_is_fixed_state_and_additive_by_identity():
    """A very short live model check; not an outcome from the full pilot."""
    from scripts.diagnose_chapter2_island_history_payoff import run_pair

    d, source = load_design()
    setting = "prior_selfing"
    seed = d["visitor_history_seeds"][0]
    rep = d["demographic_repeat_seeds"][0]
    for mode in ("fixed", "evolving"):
        result = run_pair(
            (setting, seed, rep, mode), source,
            pre_years=1, post_seed_offset=d["post_visitor_seed_offset"]
        )
        assert result["admissible"]
        assert len(result["factors"]) == 6
        for row in result["factors"]:
            assert row["clamped_total"] == pytest.approx(
                row["investment_mean_shift"] + row["assurance_mean_shift"]
            )
            if mode == "fixed":
                assert row["assurance_mean_shift"] == pytest.approx(0.0)
                assert row["interaction"] == pytest.approx(0.0)



def test_independent_payoff_confirmation_design_is_frozen_and_new():
    from scripts.run_chapter2_island_payoff_confirmation import (
        groups, load_frozen, case_key,
    )

    d, _ = load_frozen()
    tasks = groups(d)
    assert len(tasks) == 1024
    assert len(set(case_key(t) for t in tasks)) == 1024
    assert {t[1] for t in tasks} == set(range(28100801, 28100865))
    assert {t[2] for t in tasks} == {28101801, 28101802}
    assert {t[0] for t in tasks} == set(d["settings"])
    assert {t[3] for t in tasks} == {"fixed", "evolving"}
    assert not (set(range(28100801, 28100865)) &
                set(range(27120701, 27120705)))


def test_independent_payoff_joint_decision_requires_all_five():
    from scripts.summarize_chapter2_island_payoff_confirmation import decide

    d, _ = __import__(
        "scripts.run_chapter2_island_payoff_confirmation",
        fromlist=["load_frozen"]
    ).load_frozen()
    rows = [
        dict(setting=setting, mode="evolving", metric=metric,
             admissible=True, mean=sign*0.3,
             bootstrap95=[0.1, 0.5] if sign == 1 else [-0.5, -0.1])
        for setting, metric, sign in [
            ("prior_selfing", "viable_maternal", 1),
            ("pollen_discount", "viable_maternal", 1),
            ("assurance_cost", "viable_maternal", -1),
            ("prior_selfing", "female_outcross", -1),
            ("pollen_discount", "female_outcross", -1),
        ]
    ]
    yes = decide(d, rows)
    assert yes["status"] == "all_five_confirmed"
    assert yes["n_passed"] == 5
    rows[1]["bootstrap95"] = [-0.01, 0.5]
    no = decide(d, rows)
    assert no["status"] == "at_least_one_frozen_rule_failed"
    assert no["n_passed"] == 4
