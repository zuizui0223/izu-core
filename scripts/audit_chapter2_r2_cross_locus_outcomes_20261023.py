"""Cross-locus R2 response from the identical SHA-verified 384 original trajectories.

DESCRIPTIVE source readback only. This code does not run Model 3 population
updates or infer causal genetic mediation. The original Actions ZIP is external.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import zipfile

from scripts.audit_chapter2_r2_original_384_pair_convergence_20261023 import (
    ZIP_SHA, PROTOCOL_SHA, SOURCE_SHA, readback, classify_pair
)

OUTCOME = "PASS_ARCHIVED_384_PAIR_CROSS_LOCUS_DESCRIPTIVE_READBACK"
EXPECTED = {
    (0.3, "strong_baseline_limitation"): (45, 23, 19, 3, -0.0697337962962963, 14),
    (0.3, "weak_baseline_limitation"): (8, 2, 0, 6, 0.037109374999999986, 7),
    (0.5, "strong_baseline_limitation"): (42, 14, 27, 1, -0.033420138888888895, 11),
    (0.5, "weak_baseline_limitation"): (8, 1, 3, 4, 0.01790364583333333, 4),
}
STAGES = (
    "both_polymorphic", "only_control_fixed",
    "only_decline_fixed", "both_fixed_to_distinct_values",
)


def classify_cross_locus(c: dict, d: dict) -> dict:
    """One matched native source pair: distinguish zero A and zero I responses.

    Equal allele value or means does NOT prove identical copies by descent.
    """
    a = classify_pair(c, d)
    I1 = c["t_end"]["genetic_support"]["I"]
    I2 = d["t_end"]["genetic_support"]["I"]
    for support in (I1, I2):
        if (len(support["allele_values"]) != len(support["allele_counts"])
                or sum(support["allele_counts"]) != 96
                or any(not 0 <= x <= 1 for x in support["allele_values"])):
            raise AssertionError("source terminal I allele support invalid")
    i_difference = d["t_end"]["I"] - c["t_end"]["I"]
    prefix = c["t_prefix"]["genetic_support"]
    prefix_A_fixed = len(prefix["A"]["allele_values"]) == 1
    prefix_M_fixed = len(prefix["M"]["allele_values"]) == 1
    prefix_I_polymorphic = len(prefix["I"]["allele_values"]) > 1
    if prefix_A_fixed != a["prefix_fixed"]:
        raise AssertionError("A prefix fixation contradicts source parent audit")
    if prefix_M_fixed:
        m0 = prefix["M"]["allele_values"][0]
        if (c["t_end"]["M"] != m0 or d["t_end"]["M"] != m0
                or c["t_end"]["genetic_support"]["M"]["allele_values"] != [m0]
                or d["t_end"]["genetic_support"]["M"]["allele_values"] != [m0]):
            raise AssertionError("M numeric fixation not absorbed under no mutation")
    A1 = c["t_end"]["genetic_support"]["A"]["allele_values"]
    A2 = d["t_end"]["genetic_support"]["A"]["allele_values"]
    if a["zero"] and not a["same_fixed_A"]:
        raise AssertionError("this original source has a zero A contrast without joint same-A fixation")
    if a["zero"]:
        stage = "both_fixed_same_A_value"
    elif len(A1) > 1 and len(A2) > 1:
        stage = "both_polymorphic"
    elif len(A1) == 1 and len(A2) == 1:
        if A1 == A2:
            raise AssertionError("different A means but fixed to same numerical A value")
        stage = "both_fixed_to_distinct_values"
    elif len(A1) == 1:
        stage = "only_control_fixed"
    else:
        stage = "only_decline_fixed"
    return {
        "A_zero": a["zero"],
        "A_prefix_polymorphic": not a["prefix_fixed"],
        "A_terminal_stage": stage,
        "A_fixed_at_shock": prefix_A_fixed,
        "M_fixed_at_shock": prefix_M_fixed,
        "I_polymorphic_at_shock": prefix_I_polymorphic,
        "M_same_numeric_endpoint": c["t_end"]["M"] == d["t_end"]["M"],
        "I_diff": i_difference,
        "I_support_different": I1 != I2,
        "I_nonzero": i_difference != 0,
        "I_negative": i_difference < 0,
        "I_positive": i_difference > 0,
    }


def analyze(original_zip: Path) -> dict:
    # Whole-archive checksum, source code identity, every member checksum,
    # exact 192 paired A-genetic endpoints and earlier admitted totals.
    original = readback(original_zip)
    if (original["status"] != "PASS_ORIGINAL_384_SHA_VERIFIED_EXACT_PAIR_R2_CONVERGENCE"
            or original["total_zero"] != 103
            or original["total_zero_polymorphic_at_shock"] != 69
            or original["source_artifact_zip_sha256"] != ZIP_SHA
            or original["source_commit"] != SOURCE_SHA):
        raise AssertionError("prior source-exact R2 audit admission failed")
    pairs = defaultdict(dict)
    with zipfile.ZipFile(original_zip) as z:
        for shard in ("strong.json", "weak.json"):
            for row in json.loads(z.read(shard))["rows"]:
                key = (row["start_A"], row["baseline"],
                       row["founder_seed"], row["demography_repeat"])
                if row["arm"] in pairs[key]:
                    raise AssertionError("duplicate source path in new cross-locus study")
                pairs[key][row["arm"]] = row
    if len(pairs) != 192:
        raise AssertionError("missing original paired source state")
    groups = defaultdict(list)
    for key, arms in pairs.items():
        if set(arms) != {"control", "decline"}:
            raise AssertionError("unmatched native future arms")
        groups[key[:2]].append(classify_cross_locus(arms["control"], arms["decline"]))
    if set(groups) != set(EXPECTED):
        raise AssertionError("original four R2 strata incomplete")
    results = []
    for key in sorted(groups):
        rows = groups[key]
        if len(rows) != 48:
            raise AssertionError("original 48 paired futures per stratum required")
        zeros = [r for r in rows if r["A_zero"]]
        others = [r for r in rows if not r["A_zero"]]
        neg = sum(r["I_negative"] for r in zeros)
        izero = sum(not r["I_nonzero"] for r in zeros)
        pos = sum(r["I_positive"] for r in zeros)
        count_changed_support = sum(r["I_support_different"] for r in zeros)
        poly_and_investment = sum(r["A_prefix_polymorphic"] and r["I_nonzero"]
                                  for r in zeros)
        fixed_A_and_I = sum(r["A_fixed_at_shock"] and r["I_nonzero"] for r in zeros)
        strict_only_I_seg = [
            r for r in zeros
            if r["A_fixed_at_shock"] and r["M_fixed_at_shock"]
            and r["I_polymorphic_at_shock"] and r["I_nonzero"]
        ]
        if any(not r["M_same_numeric_endpoint"] for r in strict_only_I_seg):
            raise AssertionError("strict A/M-frozen source has M expression divergence")
        mean_zero = sum(r["I_diff"] for r in zeros) / len(zeros)
        expected = EXPECTED[key]
        if ((len(zeros), neg, izero, pos, poly_and_investment) !=
                (expected[0], expected[1], expected[2], expected[3], expected[5])
                or abs(mean_zero - expected[4]) > 1e-12):
            raise AssertionError("original cross-locus contrast counts/mean changed")
        if count_changed_support != neg + pos:
            raise AssertionError("I support and I-mean contrast mismatch in original A-zero pairs")
        phases = dict(sorted(Counter(r["A_terminal_stage"] for r in others).items()))
        results.append({
            "initial_A": key[0],
            "baseline": key[1],
            "n_matched_futures": 48,
            "n_A_treatment_contrast_exact_zero": len(zeros),
            "n_A_zero_but_I_negative": neg,
            "n_A_zero_but_I_exact_zero": izero,
            "n_A_zero_but_I_positive": pos,
            "n_A_zero_but_I_allele_support_differs": count_changed_support,
            "n_A_prefix_polymorphic_then_A_zero_and_I_nonzero": poly_and_investment,
            "n_A_already_fixed_at_shock_but_I_nonzero": fixed_A_and_I,
            "n_A_M_already_fixed_I_polymorphic_at_shock_but_I_nonzero": len(strict_only_I_seg),
            "strict_A_M_frozen_I_negative": sum(r["I_negative"] for r in strict_only_I_seg),
            "strict_A_M_frozen_I_positive": sum(r["I_positive"] for r in strict_only_I_seg),
            "mean_signed_I_contrast_within_A_zero": mean_zero,
            "n_A_treatment_contrast_nonzero": len(others),
            "A_nonzero_terminal_fixation_phases": phases,
        })
    totals = {
        "A_zero_I_nonzero": sum(r["n_A_zero_but_I_negative"] + r["n_A_zero_but_I_positive"]
                               for r in results),
        "A_zero_I_allele_support_differs": sum(r["n_A_zero_but_I_allele_support_differs"] for r in results),
        "A_zero_I_zero": sum(r["n_A_zero_but_I_exact_zero"] for r in results),
        "A_prefix_polymorphic_A_zero_I_nonzero": sum(r["n_A_prefix_polymorphic_then_A_zero_and_I_nonzero"] for r in results),
        "A_fixed_at_shock_A_zero_I_nonzero": sum(r["n_A_already_fixed_at_shock_but_I_nonzero"] for r in results),
        "A_and_M_fixed_I_polymorphic_at_shock_I_nonzero": sum(r["n_A_M_already_fixed_I_polymorphic_at_shock_but_I_nonzero"] for r in results),
        "strict_A_M_frozen_I_negative": sum(r["strict_A_M_frozen_I_negative"] for r in results),
        "strict_A_M_frozen_I_positive": sum(r["strict_A_M_frozen_I_positive"] for r in results),
        "A_nonzero_both_fixed_to_distinct_values": sum(
            r["A_nonzero_terminal_fixation_phases"].get("both_fixed_to_distinct_values", 0) for r in results),
        "A_nonzero_only_one_future_fixed": sum(
            r["A_nonzero_terminal_fixation_phases"].get("only_control_fixed", 0) +
            r["A_nonzero_terminal_fixation_phases"].get("only_decline_fixed", 0) for r in results),
        "A_nonzero_both_futures_polymorphic": sum(
            r["A_nonzero_terminal_fixation_phases"].get("both_polymorphic", 0) for r in results),
    }
    if totals != {
        "A_zero_I_nonzero": 54, "A_zero_I_allele_support_differs": 54,
        "A_zero_I_zero": 49, "A_prefix_polymorphic_A_zero_I_nonzero": 36,
        "A_fixed_at_shock_A_zero_I_nonzero": 18,
        "A_and_M_fixed_I_polymorphic_at_shock_I_nonzero": 14,
        "strict_A_M_frozen_I_negative": 13,
        "strict_A_M_frozen_I_positive": 1,
        "A_nonzero_both_fixed_to_distinct_values": 1,
        "A_nonzero_only_one_future_fixed": 44,
        "A_nonzero_both_futures_polymorphic": 44,
    }:
        raise AssertionError("whole-cohort source-only cross-trait accounting failed")
    return {
        "status": OUTCOME,
        "source_zip_sha256": ZIP_SHA,
        "source_commit": SOURCE_SHA,
        "protocol_sha256": PROTOCOL_SHA,
        "source_actions_run_id": 39233450099,
        "n_independent_founders": 12,
        "n_nested_demographic_repeats": 4,
        "n_original_paths": 384, "n_original_paired_futures": 192,
        "n_A_zero_pairs": 103, "n_A_nonzero_pairs": 89,
        "strict_criterion": "A and M monomorphic at census30; I polymorphic at census30; no mutation or immigration; terminal I treatment difference nonzero",
        "totals": totals, "strata": results,
        "evidence_grade": "POST_OUTCOME_SOURCE_DESCRIPTIVE_NO_NEW_EVOLUTION",
        "new_population_updates": 0, "new_statistical_tests": 0,
        "limitations": [
            "Conditioning on observed terminal A contrast is post-outcome, not an intervention fixing A",
            "12 founders rather than 192 independently sampled biological systems",
            "Equal A allele value is not demonstrated common identity by descent",
            "Does not prove that A and I evolve causally independently or that there is no A effect",
            "Does not establish population extinction, source-colonization histories or natural-island generality",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", required=True, type=Path,
                        help="external original Actions ZIP; not committed to repo")
    args = parser.parse_args()
    print(json.dumps(analyze(args.zip), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
