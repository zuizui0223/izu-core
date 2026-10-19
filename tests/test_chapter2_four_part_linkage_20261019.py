"""Readout-level re-audit of original Q1–Q4 and the completed new evidence.

Source-locked documentary arithmetic only. It does not open original simulation ZIPs,
estimate causal mediation or promote exploratory studies to confirmations.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def close(a, b):
    assert abs(float(a) - float(b)) < 1e-11


def test_q1_original_and_fresh_are_not_four_independent_confirmations():
    q = read("data/results/chapter2_assurance_generality_20261006.json")
    f = read("docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json")
    assert q["independent_visitor_histories"] == 64
    assert q["adjudication"]["n_passed"] == 4 and len(q["settings"]) == 4
    for setting in q["settings"]:
        assert setting["passes_frozen_rule"] is True
        assert setting["fixed_far_change_from_founders"]["mean"] < 0
        assert setting["attenuation_evolving_minus_fixed"]["mean"] > 0
    assert f["fresh_founder_q1"]["independent_founder_draws"] == 8
    assert f["fresh_founder_q1"]["independent_exogenous_visitor_histories"] == 8
    for setting in f["fresh_founder_q1"]["settings"]:
        assert setting["fixed_far_minus_near_mean"] < 0
        assert setting["original_D"] > 0
    # The 8x8 four-setting joint verdict remains inconclusive because
    # the direct-cost confidence interval includes zero.
    paper = (ROOT/"docs/CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md").read_text(encoding="utf-8")
    assert "3/4" in paper and "INCONCLUSIVE" in paper
    assert f["fresh_founder_q1"]["original_32_shard_case_count"] == 1088


def test_q2_order_frequency_does_not_override_registered_ROPE_or_null():
    s = read("data/results/chapter2_1005_confirmatory_replication_20261006.json")
    assigned = read("results/chapter2/order_expression_full_cohort_20261009.json")
    carrier = read("docs/audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json")
    assert s["primary_sequence"]["counts"]["assurance_first"] == 51
    ps = next(x for x in s["threshold_sensitivity"]
              if x["setting"] == "prior_selfing" and x["mutation_rate"] == .01
              and x["threshold"] == .05)
    assert ps["counts"]["assurance_first"] == 30
    point = assigned["main_order_history_DID"]
    assert point["decision"] == "equivalent_within_predeclared_ROPE"
    assert -.05 < point["history_bootstrap95"][0] < point["history_bootstrap95"][1] < .05
    close(point["pooled_mean"], -.013589137072344082)
    assert assigned["n_independent_visitor_histories"] == 64
    assert carrier["original_run"]["original_cases"] == 384
    assert carrier["registered_inference"]["result"] == "both_inconclusive"
    for ep in carrier["coprimary"].values():
        assert ep["excludes_zero"] is False
        assert ep["simultaneous_familywise_CI"][0] < 0 < ep["simultaneous_familywise_CI"][1]


def test_q3_structural_access_is_distinct_from_stochastic_order_gap():
    source = read("data/results/directional_access_20261013/READOUT.json")
    assert source["cases"] == 2304 and source["terminal_extinct"] == 0
    assert sum(source["original_categories"].values()) == source["cases"]
    assert source["excluded_before_fixation"] == 703
    assert source["excluded_at_fixation"] == 535
    assert source["ever_excluded"] == 703 + 535
    atom = (ROOT/"docs/atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md").read_text(encoding="utf-8")
    assert "3/32" in atom and "2/32" in atom
    assert "15/32" in atom and "7/32" in atom
    assert "not" in atom.lower() and "mean" in atom.lower()
    # These are two *different* original cohorts and cannot be used
    # for a newly identified allele-loss-mediated density/ABM explanation.


def test_q4_original_interaction_and_new_G_S_have_different_estimands():
    old = read("data/results/chapter2_island_demographic_independent32_20261008.json")
    new = read("docs/audits/CHAPTER2_CONFIRM160_COMPACT_RESULTS_20261019.json")
    assert old["independent_histories"] == 32
    assert len(old["per_setting"]) == 4
    close(sum(x["interaction"] for x in old["per_setting"])/4,
          old["predeclared_pooled_primary"]["mean"])
    assert old["per_setting"][1]["setting"] == "prior_selfing"
    assert old["per_setting"][1]["bootstrap95"][0] < 0
    assert new["independent_axes"] == [160,160] and new["crossings"] == 25600
    assert new["actual_restoration_tested"] is False
    a = new["arms"]; n = new["crossings"]
    G = (a["evolving_B8"]["genetic_first"] - a["fixed_B8"]["genetic_first"])/n
    S = ((a["evolving_B4p5"]["alive"]-a["fixed_B4p5"]["alive"])
        -(a["evolving_B8"]["alive"]-a["fixed_B8"]["alive"]))/n
    eps = {v["name"]:v for v in new["primary"]["endpoints"]}
    close(G,eps["genetic_loss"]["estimate"])
    close(S,eps["survival_interaction"]["estimate"])
    close(G,.08328125)
    close(S,.9270703125)
    assert a["fixed_B8"]["alive"] == a["evolving_B8"]["alive"] == n
    assert all(v["interval"][0]>0 for v in eps.values())
    # The two effects are different outcomes in *different* resource regimes.
    # Their co-occurrence does not identify G as a mediator for S.


def test_context_changes_sign_and_occupied_time_is_competing_risk():
    pollen = read("docs/audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json")
    variation = read("docs/audits/CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.json")
    assert pollen["raw_rows"] == 384 and pollen["founders"] == 12
    for start in (.3,.5):
        strong = next(x for x in pollen["summaries"] if x["start_A"] == start
                      and x["baseline"].startswith("strong"))
        weak = next(x for x in pollen["summaries"] if x["start_A"] == start
                    and x["baseline"].startswith("weak"))
        inter = next(x for x in pollen["interactions"] if x["start_A"] == start)
        close(weak["terminal_decline_minus_control_A"]
              - strong["terminal_decline_minus_control_A"], inter["interaction_A"])
        assert strong["terminal_decline_minus_control_I"]<0
        assert weak["terminal_decline_minus_control_I"]>0
    assert variation["crossings"] == 25600
    duration = {x["budget"]:x for x in variation["contrasts"] if
                x["trait"]=="I" and x["endpoint"]=="occupied_polymorphic_duration"}
    assert duration["B8"]["estimate"]<0 and duration["B4p5"]["estimate"]>0
    for policy in ("fixed","evolving"):
        v = next(x for x in variation["results"] if x["budget"]=="B4p5"
                 and x["policy"]==policy and x["trait"]=="I")
        assert len(v["curves"]["extinct"])==80
    # Duration at B4.5 ends when population goes extinct; not pure fixation time.


def test_transfer_allocation_and_no_unconditional_recovery_claim():
    tables = read("docs/audits/CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json")
    assert len(tables["tables"]) == 10 and len(tables["cohort_allele_counts"]) == 64
    assert sum(t["allocated"] for t in tables["tables"]) == 10240
    for policy in ("fixed","evolving"):
        rows = [t for t in tables["tables"] if t["policy"]==policy]
        assert len(rows)==5 and all(t["cohorts"] == 32 for t in rows)
        cohort = [x for x in tables["cohort_allele_counts"] if x["key"][2]==policy]
        assert len(cohort)==32
        assert sum(x["distinct_alleles_M_I_A"][1]>1 for x in cohort)==4
        assert next(s for s in rows[0]["support"] if s["epsilon"]==0)["entry_I_supported_cohorts"]==24
    assert sum(x["occupied"] for x in tables["tables"] if x["policy"]=="evolving")==5120


def test_current_paper_names_all_four_parts_and_retains_negative_inference():
    path=ROOT/"docs/CHAPTER2_UNIFIED_NEE_ARTICLE_WORKING_20261017.md"
    article=path.read_text(encoding="utf-8")
    assert all(v in article for v in ("Q1: selection", "Q2: sequence",
                                      "Q3: realization", "Q4: persistence"))
    assert "equivalent_within_predeclared_ROPE" in article
    assert "3/32" in article and "2/32" in article
    assert "+8.33" in article and "+92.71" in article
    assert "not identified" in article.lower() or "not establish" in article.lower()
    assert "CHAPTER2_FOUR_PART_EVIDENCE_LINKAGE_REVIEW_20261019.md" in article
