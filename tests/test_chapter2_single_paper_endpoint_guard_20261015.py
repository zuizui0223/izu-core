"""Fail-closed review of the single-Ch2 manuscript's distinct frozen endpoints.

Checks source-bound numerical facts; it is not a new independent biological replay.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md"
SI = ROOT / "docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md"
ROUTE = ROOT / "data/design/chapter2_one_paper_route_20261010.json"


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_q1_64_history_nested_8_repeat_four_setting_primary():
    src = read("data/results/chapter2_assurance_generality_20261006.json")
    proto = read("data/design/chapter2_assurance_generality_20261006.json")
    assert src["declared_cases"] == 8448
    assert src["independent_visitor_histories"] == 64
    assert src["nested_demographic_repeats"] == 8
    assert proto["main_campaign"]["declared_cases"] == 8192
    assert proto["structural_control"]["declared_cases"] == 256
    assert src["structural_control"]["status"] == "passed"
    assert src["structural_control"]["matched_pairs_checked"] == 128
    assert src["adjudication"]["n_passed"] == 4
    for arm in src["settings"]:
        assert arm["fixed_far_minus_near"]["bootstrap95"][1] < 0
        assert arm["attenuation_evolving_minus_fixed"]["bootstrap95"][0] > 0
        assert arm["eligible_histories_four_cell"] == 64
        assert all(
            arm["occupancy"][mode][space] == 1.0
            for mode in ("fixed", "evolving")
            for space in ("near", "far")
        )


def test_q3_preserves_selected_loss_not_population_probability():
    access = read("data/results/directional_access_20261013/READOUT.json")
    selection = read("data/results/low_allele_loss_20261014/extracted/READOUT.json")
    assert access["cases"] == selection["cases"] == 2304
    assert access["ever_excluded"] == 1238
    assert access["excluded_before_fixation"] == 703
    assert access["excluded_at_fixation"] == 535
    assert access["terminal_extinct"] == 0
    assert selection["eligible_loss"] == 1238
    assert selection["direction_counts"]["favouring_needed"] == 315
    assert selection["direction_counts"]["opposing_needed"] == 923


def test_q4a_new_history_stress_and_continued_evolvability_scope():
    d = read("data/design/chapter2_island_demographic_independent32_20261008.json")
    o = read("data/results/chapter2_island_demographic_independent32_20261008.json")
    replay = read("data/results/chapter2_island_demographic_independent32_replay_receipt_20261013.json")
    code = (ROOT / "scripts/run_chapter2_island_demographic_independent32.py").read_text(
        encoding="utf-8"
    )
    assert d["independent_visitor_histories"]["count"] == 32
    assert d["demographic_repeat_seeds"] == [30101801]
    assert d["prehistories"] == 400
    assert d["post_updates"] == 80
    assert d["stress_ovule_budgets"] == [2, 3, 4, 5]
    assert o["post_switch_trajectories"] == 4096
    assert o["predeclared_pooled_primary"]["pass"] is True
    assert o["predeclared_pooled_primary"]["mean"] == 0.1083984375
    assert o["predeclared_pooled_primary"]["bootstrap95"] == [
        0.0654296875, 0.1513671875
    ]
    assert replay["validation"]["all_eight_biological_projection_hashes_exact"] is True
    assert replay["validation"]["pooled_primary_exact"] is True
    assert d["pre_mutation_rate"] == d["post_mutation_rate"] == 0.01
    assert 'cfg = config(source, setting, d["pre_mutation_rate"], mode)' in code
    assert 'post_cfg = replace(' in code
    assert 'mutation_traits=(True, True, mode == "evolving")' in code
    prior = next(x for x in o["per_setting"] if x["setting"] == "prior_selfing")
    assert prior["bootstrap95"][0] < 0 < prior["bootstrap95"][1]


def test_q4b_separate_assigned_expression_k_background_moderator():
    out = read("results/chapter2/k_fixedB48_independent_primary_20261009.json")
    assert out["n_independent_visitor_histories"] == 64
    assert out["original_predeclared_primary"] == "tau(K8,B48)-tau(K48,B48)"
    q = out["contrasts"]["primary_K_at_fixed_B48"]
    assert q["mean"] == 0.007745713876893593
    assert q["bootstrap95"] == [
        0.002497158065469939, 0.013015478808429596
    ]


def test_only_one_active_paper_and_q4_both_in_text_and_supplement():
    route = read("data/design/chapter2_one_paper_route_20261010.json")
    manuscript = PAPER.read_text(encoding="utf-8")
    si = SI.read_text(encoding="utf-8")
    main = manuscript.split("# Introduction", 1)[1].split(
        "# Primary figure assembly and captions", 1
    )[0]
    abstract = manuscript.split("## Abstract", 1)[1].split("## Keywords", 1)[0]
    fit = route["journal_fit"]
    assert route["status"] == "active_unified_manuscript_not_submitted"
    assert route["active_manuscript_count"] == 1
    assert len(main.split()) == fit["current_integrated_main_words"] == 4992
    assert len(abstract.split()) == fit["current_integrated_abstract_words"] == 143
    assert "Both regimes remained pollen-limited." in abstract
    assert fit["current_main_text_words"] == 4992
    assert fit["current_abstract_words"] == len(abstract.split()) == 143
    assert "+0.1084 [0.0654,0.1514]" in manuscript
    assert "A evolvability **continued during the future**" in manuscript
    assert "+0.0077457" in manuscript
    assert "no natural-order" in manuscript.lower() or "naturally evolved" in manuscript.lower()
    assert "## S33. Independent 32-history" in si
    assert "0.1083984375" in si
    assert "+0.007745713876893593" in si
    assert "pre_mutation_rate" in si and "post_mutation_rate" in si
    assert "cannot" in si or "not" in si
