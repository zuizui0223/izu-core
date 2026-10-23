"""Read-only R1–R5 source bridge: no visitors and competing outcomes.

No biological simulation, population update, new inferential endpoint or statistical
test. An instantaneous analytical payoff identity is compared with previously
archived exploratory R5 sign counts; R4 is a first-event arithmetic readback.
"""
from __future__ import annotations

import json
from math import log
from pathlib import Path
from types import SimpleNamespace

import numpy as np

from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.selection import investment_invasion_terms
from scripts.model3_island.types import PlantState, VisitorState


ROOT = Path(__file__).resolve().parents[1]
TRANSFER = ROOT / "docs/audits/CHAPTER2_READAPTATION_DESCRIPTIVE_TABLES_20261019.json"
CROSSED = ROOT / "docs/audits/CHAPTER2_CROSSED_ACCESS_SIGN_REVERSAL_20261023.json"
ORIGINAL = ROOT / "data/results/chapter2_assurance_generality_20261006.json"
BASELINE = ROOT / "docs/audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json"
PREDICTION = ROOT / "docs/audits/CHAPTER2_FOUNDER_PREDICTABILITY_20261021.json"
FRESH = ROOT / "docs/CHAPTER2_TWO_PROPOSITION_EVIDENCE_RECEIPT_20261016.json"
FRESH_REPORT = ROOT / "docs/CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md"


def source_no_visitor_payoff(*, timing: str, mode: str, investment_cost: float = 0.4) -> dict:
    """Check an exact conditional payoff identity against BOTH original source kernels.

    This uses two artificial *states*, with no population advance. They have equal
    M/A and differ only in I, so no historical finite-response mechanism is tested.
    """
    if timing not in ("prior", "delayed") or mode not in ("fixed", "evolving"):
        raise ValueError("invalid timing or assurance mode")
    if not (investment_cost > 0):
        raise ValueError("this strict-negative test requires a positive I cost")

    a = 0.5
    i0, i1, center = 0.3, 0.7, 0.5
    alleles = np.array([
        [[0.5, 0.5], [i0, i0], [a, a]],
        [[0.5, 0.5], [i1, i1], [a, a]],
    ], dtype=float)
    state = PlantState(
        alleles=alleles,
        allele_origin=np.zeros((2, 3, 2), dtype=np.int64),
        mutation_flags=np.zeros((2, 3, 2), dtype=bool),
        ids=np.array([1, 2], dtype=np.int64),
        birth_years=np.zeros(2, dtype=np.int64),
    )
    visitors = VisitorState(
        ids=np.array([], dtype=np.int64),
        optima=np.array([], dtype=float),
        breadths=np.array([], dtype=float),
        effectiveness=np.array([], dtype=float),
    )
    config = SimpleNamespace(
        capacity=8,
        assurance_mode=mode,
        fixed_assurance=a,
        assurance_timing=timing,
        ovule_budget=8.0,
        investment_cost=investment_cost,
        assurance_cost=0.25,
        depression=0.5,
        activity=1.0,
    )
    ledger = reproduce(state, visitors, config)
    if (ledger.self_viable <= 0).any() or ledger.outcross.any() or ledger.exported.any():
        raise AssertionError("not a fertile zero-visitor comparison")
    log_fitness_ratio = log(float(ledger.self_viable[1] / ledger.self_viable[0]))
    analytic_log_ratio = -investment_cost * (i1 * i1 - i0 * i0)
    terms = investment_invasion_terms(np.array([0.5, center, a]), visitors, config)
    gradient = float(terms["gradient"])
    analytic_gradient = -2 * investment_cost * center
    if not np.isclose(log_fitness_ratio, analytic_log_ratio, rtol=0, atol=1e-12):
        raise AssertionError("source reproduction disagrees with exact zero-visitor ratio")
    if not np.isclose(gradient, analytic_gradient, rtol=0, atol=1e-12):
        raise AssertionError("rare-mutant gradient disagrees with zero-visitor identity")
    if not (log_fitness_ratio < 0 and gradient < 0):
        raise AssertionError("positive investment cost must disfavor increased I in this local state")
    return {
        "timing": timing,
        "assurance_expression": mode,
        "log_relative_fitness_high_minus_low_I": log_fitness_ratio,
        "source_gradient_at_I_0p5": gradient,
        "evidence": "exact conditional model-payoff check, NOT historical evolutionary response",
    }


def transfer_source_signs() -> dict:
    """Read the frozen exploratory transfer *sign counts*, not raw effect sizes."""
    data = json.loads(TRANSFER.read_text(encoding="utf-8"))
    if data["schema"] != "readaptation_descriptive_paper_tables_v1":
        raise AssertionError("transfer table schema changed")
    rows = [row for row in data["tables"] if row["destination"] == 0]
    if len(rows) != 2 or {row["policy"] for row in rows} != {"fixed", "evolving"}:
        raise AssertionError("not exactly two original no-visitor history policies")
    result = {}
    for row in rows:
        i = row["directions"]["I"]
        if i["positive"] + i["negative"] + i["zero"] + i["extinct"] != row["allocated"]:
            raise AssertionError("R5 sign denominator mismatch")
        if row["occupied"] + i["extinct"] != row["allocated"]:
            raise AssertionError("R5 occupancy denominator mismatch")
        result[row["policy"]] = {
            "nested_futures_allocated": row["allocated"],
            "occupied_futures": row["occupied"],
            "positive_I_exact_signs": i["positive"],
            "negative_I_exact_signs": i["negative"],
            "zero_I_exact_signs": i["zero"],
            "extinct_futures_I_undefined": i["extinct"],
            "cohorts": row["cohorts"],
            "cohorts_with_any_I_change": row["cohorts_with_any_I_change"],
            "not_an_independent_founder_count": True,
            "signs_do_not_establish_biologically_large_changes": True,
        }
    return result


def crossed_competing_event_identity() -> dict:
    """Verify R4 source-sealed endpoint partition and sign reversal (post-outcome)."""
    data = json.loads(CROSSED.read_text(encoding="utf-8"))
    if data["status"] != "POST_OUTCOME_CROSSED_DESCRIPTIVE_NOT_REGISTERED":
        raise AssertionError("R4 endpoint has unexpectedly changed registration status")
    totals = data["original_provenance"]["complete_arm_totals"]
    n = data["original_provenance"]["original_cell_count"]
    for arm, row in totals.items():
        if row["genetic_first"] + row["extinction_first"] + row["alive_accessible"] != n:
            raise AssertionError(f"non-partitioning first events in {arm}")
        if row["alive_accessible"] > row["alive"]:
            raise AssertionError("target support cannot exceed occupancy")
    summary = {}
    for b in ("B8", "B4p5"):
        e, f = totals["evolving_" + b], totals["fixed_" + b]
        delta_g = e["genetic_first"] - f["genetic_first"]
        delta_e = e["extinction_first"] - f["extinction_first"]
        delta_x = e["alive_accessible"] - f["alive_accessible"]
        if delta_x != -(delta_g + delta_e):
            raise AssertionError("first-event identity failed")
        summary[b] = {
            "first_genetic_loss_diff_count": delta_g,
            "first_extinction_diff_count": delta_e,
            "alive_with_I_support_diff_count": delta_x,
            "alive_with_I_support_diff_pp": 100 * delta_x / n,
            "post_outcome_not_registered": True,
        }
    if not (summary["B8"]["alive_with_I_support_diff_count"] < 0 <
            summary["B4p5"]["alive_with_I_support_diff_count"]):
        raise AssertionError("stored contrast does not reproduce the sign reversal")
    return summary



def original_R1_R2_readback() -> dict:
    """R1/R2: preserve the registered original 4/4 and exploratory 384 contrast.

    Do not promote original shared-founder agreement to the later fresh-founder
    registered four-setting generality decision, which remains INCONCLUSIVE.
    """
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    if original["status"] != "complete_generality_readout":
        raise AssertionError("not the original completed R1/R2 result")
    if original["adjudication"]["status"] != "all_four_confirmed":
        raise AssertionError("original source's frozen four-setting decision changed")
    settings = original["settings"]
    if len(settings) != 4 or len({row["setting"] for row in settings}) != 4:
        raise AssertionError("expected all four original reproductive settings")
    fixed_and_attenuation = []
    for row in settings:
        fixed = row["fixed_far_change_from_founders"]
        contrast = row["fixed_far_minus_near"]
        interaction = row["attenuation_evolving_minus_fixed"]
        if not (row["admissible"] and row["passes_frozen_rule"] and
                fixed["mean"] < 0 and contrast["bootstrap95"][1] < 0 and
                interaction["bootstrap95"][0] > 0):
            raise AssertionError("one of the original R1/R2 frozen gates failed")
        fixed_and_attenuation.append({
            "setting": row["setting"],
            "fixed_A_far_I_change_from_founder": fixed["mean"],
            "A_evolution_attenuation_near_far": interaction["mean"],
        })
    fresh = json.loads(FRESH.read_text(encoding="utf-8"))["fresh_founder_q1"]
    if not (fresh["independent_founder_draws"] == 8 and
            fresh["independent_exogenous_visitor_histories"] == 8 and
            fresh["original_32_shard_case_count"] == 1088):
        raise AssertionError("not the originally admitted independent-fresh-founder cohort")
    if "fresh_founder_4setting_inconclusive" not in FRESH_REPORT.read_text(encoding="utf-8"):
        raise AssertionError("missing the original registered inconclusive decision")
    fresh_rows = fresh["settings"]
    if len(fresh_rows) != 4 or len({row["setting"] for row in fresh_rows}) != 4:
        raise AssertionError("fresh-founder four-setting scope changed")
    fresh_nonnecessity = []
    for row in fresh_rows:
        if not (row["negative_fixed_founder_means"] == 8 and
                row["fixed_far_change_from_actual_founder_mean"] < 0 and
                row["fixed_far_change_bootstrap95"][1] < 0):
            raise AssertionError("fresh-founder fixed-A R1 support was not preserved")
        fresh_nonnecessity.append({
            "setting": row["setting"],
            "fixed_A_far_I_change_from_actual_founder":
                row["fixed_far_change_from_actual_founder_mean"],
            "negative_fixed_founder_marginals": row["negative_fixed_founder_means"],
        })
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    if baseline["status"] != "EXPLORATORY_RAW_ENDPOINT_AUDIT_PASS":
        raise AssertionError("384-path source is not admitted")
    if baseline["raw_rows"] != 384 or baseline["founders"] != 12:
        raise AssertionError("not the archived 384-path experiment")
    grouped = {(float(row["start_A"]), row["baseline"]): row
               for row in baseline["summaries"]}
    if len(grouped) != 4:
        raise AssertionError("expected four archived baseline x initial A contrasts")
    reversals = []
    for starting_a in (0.3, 0.5):
        strong = grouped[starting_a, "strong_baseline_limitation"]
        weak = grouped[starting_a, "weak_baseline_limitation"]
        if not (strong["both_survived"] == weak["both_survived"] == 48
                and strong["terminal_decline_minus_control_I"] < 0
                and weak["terminal_decline_minus_control_I"] > 0):
            raise AssertionError("archived baseline-dependent I contrast changed")
        reversals.append({
            "starting_A": starting_a,
            "strong_baseline_I_decline_minus_control":
                strong["terminal_decline_minus_control_I"],
            "weak_baseline_I_decline_minus_control":
                weak["terminal_decline_minus_control_I"],
            "absolute_pollen_delivery_was_not_matched": True,
        })
    return {
        "original_registered_four_setting": fixed_and_attenuation,
        "independent_fresh_founder_fixed_A_readback": fresh_nonnecessity,
        "independent_fresh_founder_four_setting_overall": "INCONCLUSIVE",
        "exploratory_384_baseline_regime_sign_reversal": reversals,
        "not_identified": "A-only genetic mediation or history-only effect",
    }


def R3_known_source_predictability_readback() -> dict:
    """Audit held-out score identity for known source IDs; do not infer drift."""
    d = json.loads(PREDICTION.read_text(encoding="utf-8"))
    if d["primary"] != "evolving_I_change founder-only leave-cell-out skill":
        raise AssertionError("primary predictive estimand changed")
    x = d["results"]
    out = {}
    for name in ("evolving_I_change", "evolving_M_change", "evolving_A_change"):
        r = x[name]
        if (r["n_founders"], r["n_histories"]) != (160, 160):
            raise AssertionError("not the archived 160x160 cross")
        for component in ("founder", "history", "additive"):
            expected = 1 - r["loo_sse"][component] / r["loo_sse"]["intercept"]
            if not np.isclose(expected, r["loo_skill"][component], atol=1e-12, rtol=0):
                raise AssertionError("R3 held-out PRESS score no longer agrees")
        out[name] = {
            "founder_only_loo_skill": r["loo_skill"]["founder"],
            "history_only_loo_skill": r["loo_skill"]["history"],
            "interaction_plus_realization_ss_fraction":
                r["ss_fraction"]["interaction_plus_stochastic"],
        }
    if not (out["evolving_M_change"]["history_only_loo_skill"] >
            out["evolving_I_change"]["history_only_loo_skill"]):
        raise AssertionError("archived M/I known-history prediction contrast changed")
    return {
        "known_source_prediction_not_unseen_founders": out,
        "interaction_plus_realization_not_pure_drift": True,
        "endpoint_repeatability_cohort_is_separate": True,
    }


def read_only_audit() -> dict:
    return {
        "status": "EXPLORATORY_READ_ONLY_NO_NEW_BIOLOGY",
        "R1_R2_original_and_baseline": original_R1_R2_readback(),
        "R3_known_source_predictability": R3_known_source_predictability_readback(),
        "source_payoffs": [
            source_no_visitor_payoff(timing=t, mode=m)
            for t in ("delayed", "prior") for m in ("fixed", "evolving")
        ],
        "R5_no_visitor_transfer": transfer_source_signs(),
        "R4_competing_event_arithmetic": crossed_competing_event_identity(),
        "inference_limits": [
            "Local directional selection does not determine finite inherited realizations.",
            "Exact sign counts may include near-zero numeric effects; no magnitude inference.",
            "R5 policies inherit different M/I/A and nested futures are not independent founders.",
            "R4 first-event differences are not cause-specific genetic hazards or causal mediation.",
            "R1–R5 registered findings, original cohorts, figure values and p-values are unchanged.",
        ],
        "new_biological_simulations": 0,
        "new_preregistered_endpoints": 0,
    }


if __name__ == "__main__":
    print(json.dumps(read_only_audit(), indent=2, ensure_ascii=False))
