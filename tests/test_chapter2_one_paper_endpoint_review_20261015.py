"""Single-paper source/endpoint admission guard (no new biological trajectories)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def data(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_q1_original_primary_does_not_turn_all_paths_into_independent_islands():
    result = data("data/results/chapter2_assurance_generality_20261006.json")
    protocol = data("data/design/chapter2_assurance_generality_20261006.json")
    assert result["declared_cases"] == 8448
    assert protocol["main_campaign"]["declared_cases"] == 8192
    assert protocol["structural_control"]["declared_cases"] == 256
    assert result["independent_visitor_histories"] == 64
    assert result["nested_demographic_repeats"] == 8
    assert result["structural_control"]["status"] == "passed"
    assert result["structural_control"]["matched_pairs_checked"] == 128
    assert result["adjudication"]["n_passed"] == 4
    assert len(result["settings"]) == 4
    for row in result["settings"]:
        a = row["fixed_far_minus_near"]
        b = row["attenuation_evolving_minus_fixed"]
        assert a["mean"] < 0 and a["bootstrap95"][1] < 0
        assert b["mean"] > 0 and b["bootstrap95"][0] > 0
        assert row["eligible_histories_four_cell"] == 64
        for mode in ("fixed", "evolving"):
            for arm in ("near", "far"):
                assert row["occupancy"][mode][arm] == 1.0


def test_q3_selected_allele_loss_is_not_invented_prospective_probability():
    access = data("data/results/directional_access_20261013/READOUT.json")
    loss = data("data/results/low_allele_loss_20261014/extracted/READOUT.json")
    assert access["cases"] == loss["cases"] == 2304
    assert access["ever_excluded"] == loss["eligible_loss"] == 1238
    assert access["excluded_before_fixation"] == 703
    assert access["excluded_at_fixation"] == 535
    assert access["excluded_with_expressed_variance"] == 703
    assert access["terminal_extinct"] == 0
    assert loss["direction_counts"]["favouring_needed"] == 315
    assert loss["direction_counts"]["opposing_needed"] == 923
    assert 315 + 923 == 1238


def test_q4_a_continued_evolvability_and_stress_gate_are_explicit():
    protocol = data("data/design/chapter2_island_demographic_independent32_20261008.json")
    output = data("data/results/chapter2_island_demographic_independent32_20261008.json")
    source = (ROOT / "scripts/run_chapter2_island_demographic_independent32.py").read_text(
        encoding="utf-8"
    )
    assert protocol["independent_visitor_histories"]["count"] == 32
    assert protocol["demographic_repeat_seeds"] == [30101801]
    assert protocol["post_updates"] == 80
    assert protocol["stress_ovule_budgets"] == [2, 3, 4, 5]
    assert output["post_switch_trajectories"] == protocol["total_post_trajectories"] == 4096
    assert output["predeclared_pooled_primary"]["pass"] is True
    assert output["predeclared_pooled_primary"]["mean"] == 0.1083984375
    assert output["predeclared_pooled_primary"]["bootstrap95"] == [
        0.0654296875, 0.1513671875
    ]
    assert protocol["pre_mutation_rate"] == protocol["post_mutation_rate"] == 0.01
    assert 'cfg = config(source, setting, d["pre_mutation_rate"], mode)' in source
    assert 'mutation_traits=(True, True, mode == "evolving")' in source
    assert 'post_cfg = replace(' in source
    # The archived runner preserves the *same* assurance mode through postshock.
    # Future unequal pre/post mutation designs would need a separately versioned
    # guard, not a quiet reclassification of this frozen original endpoint.


def test_q4_b_distinct_fixed_pollen_background_endpoint():
    fixed = data("results/chapter2/k_fixedB48_independent_primary_20261009.json")
    assert fixed["n_independent_visitor_histories"] == 64
    assert fixed["original_predeclared_primary"] == "tau(K8,B48)-tau(K48,B48)"
    contrast = fixed["contrasts"]["primary_K_at_fixed_B48"]
    assert abs(contrast["mean"] - 0.007745713876893593) < 1e-14
    assert contrast["bootstrap95"] == [
        0.002497158065469939, 0.013015478808429596
    ]


def test_review_is_about_one_active_manuscript_and_q4_is_retained():
    route = data("data/design/chapter2_one_paper_route_20261010.json")
    text = (ROOT / "docs/CHAPTER2_ONE_PAPER_CODE_ENDPOINT_STORY_REVIEW_20261015.md"
            ).read_text(encoding="utf-8")
    assert route["active_manuscript_count"] == 1
    assert route["status"] == "active_unified_manuscript_not_submitted"
    assert "ONE unified manuscript" in text
    assert "Q1" in text and "Q2" in text and "Q3" in text
    assert "Q4A" in text and "Q4B" in text
    assert "0.108398" in text and "0.0077457" in text
    assert "no claimed Q1→Q4 natural mediation" in text
    paper = (ROOT / route["active_manuscript"]).read_text(encoding="utf-8")
    si = (ROOT / "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
          ).read_text(encoding="utf-8")
    main = paper.split("# Introduction", 1)[1].split(
        "# Primary figure assembly and captions", 1
    )[0]
    abstract = paper.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    assert len(main.split()) == 4991
    assert len(abstract.split()) == 148
    assert "0.1084 [0.0654,0.1514]" in paper
    assert "A evolvability **continued during the future**" in paper
    assert "+0.007746" in paper
    assert "## S33. Conditional assurance-evolvability-by-history persistence" in si
    assert "0.1083984375" in si and "+0.007745713876893593" in si
