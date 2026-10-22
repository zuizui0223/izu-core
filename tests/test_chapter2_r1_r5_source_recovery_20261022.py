"""Read-only evidence integration guards for the five current Chapter 2 results.

Checks sourced numbers, negative/inconclusive outcomes, nested denominators
and the two manuscript copies. Does not import biological producers or
generate new simulations / inferential intervals.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AUDITS = DOCS / "audits"


def source(path: Path):
    return json.loads(path.read_text(encoding="utf8"))


def test_r1_original_fixed_A_founder_transport_and_genetic_bound():
    receipt = source(DOCS / "CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json")
    cohort = receipt["fresh_founder_q1"]
    assert cohort["independent_founder_draws"] == 8
    assert cohort["independent_exogenous_visitor_histories"] == 8
    assert cohort["crossed_cells_per_setting"] == 64
    rows = cohort["settings"]
    assert len(rows) == 4
    assert all(r["negative_fixed_founder_means"] == 8 for r in rows)
    assert all(r["fixed_far_change_from_actual_founder_mean"] < 0 for r in rows)
    assert all(r["fixed_far_change_bootstrap95"][1] < 0 for r in rows)
    bound = receipt["support_theorem"]
    assert "no new mutation" in bound["hypotheses"]
    assert "no immigration" in bound["hypotheses"]
    assert "subset" in bound["statement"]
    assert "not" in bound["scope_warning"].lower()


def test_r2_conditional_sign_reversal_and_inconclusive_fourth_setting():
    raw = source(AUDITS / "CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json")
    assert raw["raw_rows"] == 384 and raw["founders"] == 12
    for initial_A in (0.3, 0.5):
        strong = next(x for x in raw["summaries"] if x["start_A"] == initial_A
                      and x["baseline"].startswith("strong"))
        weak = next(x for x in raw["summaries"] if x["start_A"] == initial_A
                    and x["baseline"].startswith("weak"))
        assert strong["terminal_decline_minus_control_I"] < 0
        assert weak["terminal_decline_minus_control_I"] > 0
        assert weak["terminal_decline_minus_control_A"] > strong["terminal_decline_minus_control_A"]
        row = next(x for x in raw["interactions"] if x["start_A"] == initial_A)
        assert row["interaction_A"] > 0
        assert row["bootstrap_95_A"][0] > 0
    q1 = (DOCS / "CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md").read_text(encoding="utf8")
    assert "fresh_founder_4setting_inconclusive" in q1
    assert "**INCONCLUSIVE**" in q1
    assert "negative in two of four" in q1


def test_r3_repeatability_is_not_a_positive_A_response_or_drift_fraction():
    repeat = source(AUDITS / "CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json")
    central = repeat["settings"]["delayed_control"]["central"]
    assert central["paired_eligible_contexts"] == 128
    assert central["A"]["far_identical_endpoint_contexts"] == 107
    assert central["I"]["far_identical_endpoint_contexts"] == 17
    sign = central["A"]["contrast_labels"]["0.0"]
    assert sign["all_neutral_contexts"] == sign["unanimous_contexts"] == 103
    pred = source(AUDITS / "CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json")["results"]
    assert pred["evolving_I_change"]["loo_skill"]["founder"] < 0
    assert 0 < pred["evolving_I_change"]["loo_skill"]["history"] < 0.01
    assert pred["evolving_M_change"]["loo_skill"]["history"] > 0.40
    assert 0.97 < pred["evolving_I_change"]["ss_fraction"]["interaction_plus_stochastic"] < 0.98
    variation = source(AUDITS / "CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json")
    A = {x["policy"]: x for x in variation["results"]
         if x["budget"] == "B8" and x["trait"] == "A"}
    assert sum(y["count"] for y in A["fixed"]["fixed_value_counts"]) == 15664
    assert sum(y["count"] for y in A["evolving"]["fixed_value_counts"]) == 25582
    assert next(y["count"] for y in A["fixed"]["fixed_value_counts"] if y["value"] == .75) == 5145
    assert next(y["count"] for y in A["evolving"]["fixed_value_counts"] if y["value"] == .75) == 25307


def test_r4_registered_G_S_and_exploratory_three_state_are_kept_separate():
    c = source(AUDITS / "CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json")
    assert c["crossings"] == 25600 and c["independent_axes"] == [160, 160]
    arms = c["arms"]
    assert arms["evolving_B8"]["alive"] == arms["fixed_B8"]["alive"] == 25600
    assert (arms["evolving_B8"]["genetic_first"] - arms["fixed_B8"]["genetic_first"]) / 256 == 8.328125
    assert (arms["evolving_B4p5"]["alive"] - arms["fixed_B4p5"]["alive"]) / 256 == 92.70703125
    assert all(row["evolving"] > row["fixed"] for row in c["epsilon_descriptive"])
    assert (arms["evolving_B4p5"]["alive_accessible"] -
            arms["fixed_B4p5"]["alive_accessible"]) / 256 == 35.56640625
    assert (arms["evolving_B8"]["alive_accessible"] -
            arms["fixed_B8"]["alive_accessible"]) / 256 == -8.328125
    assert c["primary"]["marginal_confidence"] == 0.975
    assert c["actual_restoration_tested"] is False


def test_r5_transfer_ancestry_survival_and_support_are_distinct():
    t = source(AUDITS / "CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json")
    for policy in ("fixed", "evolving"):
        cohorts = [x for x in t["cohort_allele_counts"] if x["key"][2] == policy]
        assert len(cohorts) == 32
        assert sum(x["distinct_alleles_M_I_A"][1] > 1 for x in cohorts) == 4
        no_visitors = next(x for x in t["tables"] if x["policy"] == policy and x["destination"] == 0)
        assert no_visitors["allocated"] == 1024
        assert next(x["entry_I_supported_cohorts"] for x in no_visitors["support"] if x["epsilon"] == 0) == 24
        assert no_visitors["directions"]["I"]["positive"] == (27 if policy == "fixed" else 29)
        assert no_visitors["occupied"] == (704 if policy == "fixed" else 1024)
    pedigree = source(AUDITS / "CHAPTER2_SECONDARY_COLONIZATION_PEDIGREE_VERIFIED_20261020.json")
    assert pedigree["paths"] == 240
    assert pedigree["independent_crossed_blocks"] == 4
    target = {g["policy"]: g for g in pedigree["groups"]
              if g["epoch"] == 25 and g["destination"] == "mainland_like_resident"
              and g["distance"] == 1.5}
    assert target["fixed"]["pedigree"] == 4 and target["evolving"]["pedigree"] == 6
    assert target["fixed"]["selected"] == 2 and target["evolving"]["selected"] == 4
    assert target["fixed"]["resident_occupied"] == target["evolving"]["resident_occupied"] == 8


def test_recovered_five_results_remain_consistent_between_manuscripts():
    master = (DOCS / "CHAPTER2_NEE_SUPPORTED_RESULTS_ARTICLE_EXTRACT_20261019.md").read_text(encoding="utf8")
    working = (DOCS / "CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md").read_text(encoding="utf8")
    assert master.count("## Results\n") == 1
    assert working.count("## Results — existing source-admitted evidence\n") == 1
    a = master.split("## Results\n", 1)[1].split("## Discussion\n", 1)[0]
    b = working.split("## Results — existing source-admitted evidence\n", 1)[1].split(
        "## Planned new decisive Results — PENDING, not observations", 1)[0]
    assert a == b
    assert [x.split(" — ")[0] for x in a.splitlines() if x.startswith("### R")] == [
        "### R1", "### R2", "### R3", "### R4", "### R5"]
    for term in ("all eight founder-averaged", "far-side I was also negative in two",
                 "103/128 contexts had unanimous A far-minus-near",
                 "97.622% combined residual", "8.33–8.60 points",
                 "27/1,024 fixed-history and 29/1,024 evolving-history",
                 "genetic_access_target_placeholder_does_not_exist"):
        if term.startswith("genetic_access_target_placeholder"):
            assert term not in a
        else:
            assert term in a
    abstract = master.split("## Abstract\n", 1)[1].split("## Introduction\n", 1)[0]
    body = master.split("## Introduction\n", 1)[1].split("## Online Methods", 1)[0]
    assert len(abstract.split()) <= 200 and len(body.split()) <= 3500
