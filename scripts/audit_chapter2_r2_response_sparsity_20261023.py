"""Read-only R2 baseline-384 zero-response/fixation decomposition.

Uses independently source-audited summaries. This is DESCRIPTIVE and post-outcome:
no simulation, no new significance, and no pure-memory or fixation mediation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEPENDENT = ROOT / "docs/audits/CHAPTER2_BASELINE_POLLEN_384_INDEPENDENT_REVIEW_20261019.json"
REGISTERED_SOURCE = ROOT / "docs/audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json"
SOURCE_SHA = "eb785dc6865ca1842ec9d6c7d511778c74e03478"
PROTOCOL_SHA = "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849"


def analyze() -> dict:
    review = json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    source = json.loads(REGISTERED_SOURCE.read_text(encoding="utf-8"))
    if (review["status"] != "INDEPENDENT_SAVED_DATA_RECOMPUTATION_PASS"
            or review["source_sha"] != SOURCE_SHA
            or review["protocol_sha256"] != PROTOCOL_SHA
            or review["rows"] != 384
            or not review["all_survive"]
            or review["independent_founders"] != 12
            or source["status"] != "EXPLORATORY_RAW_ENDPOINT_AUDIT_PASS"
            or source["source_contract_sha256"] != PROTOCOL_SHA
            or source["raw_rows"] != 384
            or source["founders"] != 12):
        raise AssertionError("R2 original independently audited source identity changed")
    if len(review["pair_contrasts"]) != len(source["summaries"]) != 4:
        raise AssertionError("four initial-A by baseline strata required")
    if len(review["strata"]) != 8:
        raise AssertionError("two arms for every source stratum required")
    summaries = {(row["start_A"], row["baseline"]): row for row in source["summaries"]}
    if len(summaries) != 4:
        raise AssertionError("duplicated 384-source baseline or initial-A strata")
    pair_contrasts = {(row["start_A"], row["baseline"]): row
                      for row in review["pair_contrasts"]}
    if set(pair_contrasts) != set(summaries):
        raise AssertionError("independent-reader/source stratum mismatch")
    strata = {(row["start_A"], row["baseline"], row["arm"]): row
              for row in review["strata"]}
    if len(strata) != 8:
        raise AssertionError("duplicate independently audited stratum")
    results = []
    for starting_a in (0.3, 0.5):
        for baseline in ("strong_baseline_limitation", "weak_baseline_limitation"):
            k = (starting_a, baseline)
            summary, readback = summaries[k], pair_contrasts[k]
            n = summary["allocated_pairs"]
            if n != summary["both_survived"] or n != 48:
                raise AssertionError("not the original 48 paired all-surviving contrasts")
            if not readback["prefix_fixed_pairs_all_remain_same_A"]:
                raise AssertionError("no-mutation absorbing fixation not verified")
            fixed = readback["prefix_fixed_A_pairs"]
            zero = readback["zero_A_contrast_pairs"]
            nonzero = n - zero
            polymorphic_at_shock = n - fixed
            if not (0 <= fixed <= zero < n and polymorphic_at_shock > 0):
                raise AssertionError("zero/nonzero counts violate prefix-fixation constraint")
            for arm in ("control", "decline"):
                row = strata[(starting_a, baseline, arm)]
                if row["n"] != n or row["A"]["t_prefix"]["fixed"] != fixed:
                    raise AssertionError("independent stratum contradicts paired prefix-fixed A")
            mean = summary["terminal_decline_minus_control_A"]
            if abs(mean - readback["A_decline_minus_control"]) >= 1e-12:
                raise AssertionError("source and independent reader mean A response disagree")
            nonzero_conditional_mean = mean * n / nonzero
            nonfixed_conditional_mean = mean * n / polymorphic_at_shock
            results.append({
                "initial_A": starting_a,
                "baseline": baseline,
                "paired_histories_n": n,
                "zero_exact_A_contrast_pairs": zero,
                "nonzero_exact_A_contrast_pairs": nonzero,
                "nonzero_fraction": nonzero / n,
                "prefix_fixed_A_pairs": fixed,
                "prefix_polymorphic_A_pairs": polymorphic_at_shock,
                "zero_among_prefix_polymorphic_pairs": zero - fixed,
                "unconditional_signed_mean_A_contrast": mean,
                "mean_signed_contrast_given_exact_nonzero": nonzero_conditional_mean,
                "mean_signed_contrast_given_prefix_polymorphic": nonfixed_conditional_mean,
                "nonzero_definition": "exact numeric inequality, not a biological change threshold",
            })
    by_key = {(row["initial_A"], row["baseline"]): row for row in results}
    comparisons = []
    for a in (0.3, 0.5):
        strong = by_key[(a, "strong_baseline_limitation")]
        weak = by_key[(a, "weak_baseline_limitation")]
        if not (weak["nonzero_fraction"] > strong["nonzero_fraction"]
                and weak["unconditional_signed_mean_A_contrast"] >
                    strong["unconditional_signed_mean_A_contrast"]
                and weak["mean_signed_contrast_given_prefix_polymorphic"] >
                    strong["mean_signed_contrast_given_prefix_polymorphic"]):
            raise AssertionError("observed R2 sparse-response direction changed")
        comparisons.append({
            "initial_A": a,
            "weak_minus_strong_nonzero_fraction": weak["nonzero_fraction"] - strong["nonzero_fraction"],
            "weak_minus_strong_unconditional_A": (
                weak["unconditional_signed_mean_A_contrast"] -
                strong["unconditional_signed_mean_A_contrast"]
            ),
            "weak_minus_strong_mean_among_prefix_polymorphic": (
                weak["mean_signed_contrast_given_prefix_polymorphic"] -
                strong["mean_signed_contrast_given_prefix_polymorphic"]
            ),
            "interpretation": "descriptive differences; no identified mediation",
        })
    return {
        "status": "SOURCE_BOUND_EXPLORATORY_R2_RESPONSE_SPARSITY_NO_NEW_BIOLOGY",
        "source_run_sha": SOURCE_SHA,
        "source_contract_sha256": PROTOCOL_SHA,
        "original_rows": 384,
        "independent_founders": 12,
        "nested_demographic_repeats_per_founder": 4,
        "all_trajectories_survived": True,
        "strata": results,
        "comparisons": comparisons,
        "interpretation": (
            "The much smaller unconditional additional-A response after strong baseline "
            "limitation reflects fewer exact nonzero paired responses. Prefix A fixation "
            "forces some zeros but cannot explain all zeros: many pairs still had A "
            "variation at shock yet ended with zero treatment difference."
        ),
        "not_identified": [
            "Pure causal contribution of prior A fixation",
            "Instantaneous pollen-delivery effect matched across baseline environments",
            "Genetic-history mediation independent of current state",
            "Distribution of signs/magnitudes within nonzero paths",
            "Predictive or inferential sampling uncertainty for conditional nonzero means",
            "Meaningful biological response incidence beyond exact numeric equality",
        ],
        "registered_R1_R2_R3_R4_R5_inference_unchanged": True,
        "new_biological_simulations": 0,
        "new_statistical_tests": 0,
    }


if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=2))
