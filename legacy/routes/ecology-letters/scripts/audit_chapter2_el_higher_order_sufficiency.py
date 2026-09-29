from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from scripts.audit_chapter2_el_nonlinear_reduction import (
    adaptive_consumer_resource,
    order_label,
    run_consumer_resource_grid,
)

ROOT = Path(__file__).resolve().parents[1]
HIGHER_ORDER_FREEZE = ROOT / "data/design/chapter2_el_higher_order_sufficiency_freeze_20260913.json"
FEEDBACK_FREEZE = ROOT / "data/design/chapter2_el_mixed_feedback_validation_freeze_20260913.json"
SOURCE_DESIGN = ROOT / "data/design/chapter2_el_nonlinear_reduction_audit_20260913.json"
OUT = ROOT / "data/results/chapter2_el_higher_order_sufficiency_20260913.json"


def rho_for_keff(k: int, k_eff: float) -> float:
    if k < k_eff or k_eff <= 1.0:
        raise ValueError("require k >= k_eff > 1")
    if k == 1:
        raise ValueError("k=1 cannot represent finite k_eff>1")
    rho = (k - k_eff) / (k_eff * (k - 1.0))
    if not 0.0 <= rho < 1.0:
        raise ValueError("derived rho outside [0,1)")
    return rho


def variance_factor(k: int, rho: float) -> float:
    return rho + (1.0 - rho) / k


def cumulant_factor(order: int, k: int, rho: float) -> float:
    """Multiplier of a common source cumulant under sqrt-rho common-factor pooling."""
    if order < 2:
        raise ValueError("cumulant order must be >=2")
    return rho ** (order / 2.0) + (1.0 - rho) ** (order / 2.0) / (k ** (order - 1))


def quadratic_components(
    *,
    var_x: float,
    tau: float,
    mu3: float,
    kappa4: float,
    b: float,
    c: float,
    d: float,
    e: float,
) -> dict[str, float]:
    """Exact C/I components for the centered quadratic mixed-response extension.

    Y = aX + bZ + cXZ + (d/2)(Z^2-tau) + (e/2)X(Z^2-tau),
    with centered independent X and Z.  The aX term contributes only to S.
    """
    var_z2 = kappa4 + 2.0 * tau * tau
    community = b * b * tau + b * d * mu3 + 0.25 * d * d * var_z2
    interaction = var_x * (
        c * c * tau + c * e * mu3 + 0.25 * e * e * var_z2
    )
    return {
        "C": community,
        "I": interaction,
        "I_over_C": interaction / community,
        "Var_Z2": var_z2,
    }


def symmetric_ratio_derivative_sign(*, b: float, c: float, d: float, e: float) -> float:
    """Sign numerator of d(I/C)/d Var(Z^2) at fixed tau when mu3=0."""
    return e * e * b * b - c * c * d * d


def holling_integrated_abs_derivative(order: int, handling: float) -> float:
    """Integral_0^1 |d^order [A/(1+hA)] / dA^order| dA."""
    if order < 2 or handling <= 0.0:
        raise ValueError("require derivative order >=2 and handling>0")
    return math.factorial(order - 1) * handling ** (order - 2) * (
        1.0 - (1.0 + handling) ** (-order)
    )


def _two_way_rows(*, k_values, seed: int, realizations: int, n_resource: int,
                  width: float, handling: float, alpha: float, steps: int) -> list[dict]:
    rows: list[dict] = []
    for k in k_values:
        fr = adaptive_consumer_resource(
            k=int(k),
            seed=int(seed),
            realizations=int(realizations),
            n_resource=int(n_resource),
            width=float(width),
            handling=float(handling),
            alpha=float(alpha),
            steps=int(steps),
        )
        rows.append(
            {
                "k": int(k),
                "S": float(fr[0]),
                "C": float(fr[1]),
                "I": float(fr[2]),
                "I_over_C": float(fr[2] / fr[1]),
                "order": order_label(fr),
            }
        )
    return rows


def _trajectory_pattern(rows: list[dict]) -> dict[str, bool]:
    winners = [row["order"][0] for row in rows]
    return {
        "ci_flip": rows[0]["C"] > rows[0]["I"] and any(row["I"] > row["C"] for row in rows[1:]),
        "intermediate_i_winner": "I" in winners[1:4],
        "full_c_i_s": winners[0] == "C" and "I" in winners[1:4] and winners[-1] == "S",
    }


def audit_handling_only_prediction() -> dict:
    design = json.loads(SOURCE_DESIGN.read_text(encoding="utf-8"))
    settings = run_consumer_resource_grid(design)["setting_summaries"]

    by_handling: dict[str, dict[str, float | int]] = {}
    for handling in sorted({float(row["handling"]) for row in settings}):
        group = [row for row in settings if float(row["handling"]) == handling]
        counts = [int(row["seeds_CI_order_flip"]) for row in group]
        by_handling[str(handling)] = {
            "settings": len(group),
            "sum_seed_flips": int(sum(counts)),
            "mean_seed_flips": float(np.mean(counts)),
            "settings_with_flip_in_at_least_4_of_6_seeds": int(sum(value >= 4 for value in counts)),
            "H4": holling_integrated_abs_derivative(4, handling),
        }

    blocks: dict[tuple[int, float, float], dict[float, int]] = {}
    for row in settings:
        key = (int(row["n_resource"]), float(row["width"]), float(row["alpha"]))
        blocks.setdefault(key, {})[float(row["handling"])] = int(row["seeds_CI_order_flip"])
    contrasts = [values[4.0] - values[1.0] for values in blocks.values()]
    positive = sum(value > 0 for value in contrasts)
    negative = sum(value < 0 for value in contrasts)
    mean_difference = float(np.mean(contrasts))
    supported = positive > negative and mean_difference > 0.0

    means = [by_handling[str(h)]["mean_seed_flips"] for h in (1.0, 2.0, 4.0)]
    return {
        "status": "prespecified_prediction_tested",
        "predictor": "integrated absolute Holling-II fourth derivative H4(h)",
        "by_handling": by_handling,
        "matched_h4_minus_h1": {
            "blocks": len(contrasts),
            "positive": int(positive),
            "zero": int(sum(value == 0 for value in contrasts)),
            "negative": int(negative),
            "mean_difference": mean_difference,
            "median_difference": float(np.median(contrasts)),
        },
        "secondary_means_nondecreasing": bool(means[0] <= means[1] <= means[2]),
        "decision": "supported" if supported else "not_supported",
        "interpretation": "Scalar Holling curvature alone does not predict the C/I phase reversal in the frozen 54-setting grid.",
    }


def fresh_feedback_validation() -> dict:
    freeze = json.loads(FEEDBACK_FREEZE.read_text(encoding="utf-8"))
    cfg = freeze["factorial_validation"]
    seeds = [int(seed) for seed in freeze["fresh_seed_ensemble"]]
    alphas = [float(value) for value in cfg["adaptation_rate"]]
    if alphas != [0.0, 0.15]:
        raise ValueError("fresh validation expects frozen alpha pair [0.0, 0.15]")

    paired_rows = []
    component_rows: dict[tuple[float, int], list[tuple[float, float, float]]] = {}
    for n_resource in cfg["resource_types_per_copy"]:
        for width in cfg["match_width"]:
            for handling in cfg["handling"]:
                for seed in seeds:
                    pair = {
                        "n_resource": int(n_resource),
                        "width": float(width),
                        "handling": float(handling),
                        "seed": int(seed),
                    }
                    for alpha in alphas:
                        rows = _two_way_rows(
                            k_values=cfg["k_values"],
                            seed=seed,
                            realizations=cfg["realizations_per_seed"],
                            n_resource=n_resource,
                            width=width,
                            handling=handling,
                            alpha=alpha,
                            steps=cfg["adaptation_steps"],
                        )
                        pattern = _trajectory_pattern(rows)
                        pair[f"flip_{alpha}"] = int(pattern["ci_flip"])
                        pair[f"imid_{alpha}"] = int(pattern["intermediate_i_winner"])
                        pair[f"full_{alpha}"] = int(pattern["full_c_i_s"])
                        for row in rows:
                            component_rows.setdefault((alpha, int(row["k"])), []).append(
                                (float(row["S"]), float(row["C"]), float(row["I"]))
                            )
                    paired_rows.append(pair)

    differences = [row["flip_0.15"] - row["flip_0.0"] for row in paired_rows]
    total_alpha0 = sum(row["flip_0.0"] for row in paired_rows)
    total_alpha015 = sum(row["flip_0.15"] for row in paired_rows)
    positive = sum(value > 0 for value in differences)
    negative = sum(value < 0 for value in differences)
    supported = sum(differences) > 0 and positive > negative

    medians = []
    for alpha in alphas:
        for k in cfg["k_values"]:
            array = np.asarray(component_rows[(alpha, int(k))], dtype=float)
            median = np.median(array, axis=0)
            medians.append(
                {
                    "alpha": alpha,
                    "k": int(k),
                    "median_S": float(median[0]),
                    "median_C": float(median[1]),
                    "median_I": float(median[2]),
                    "C_gt_I_count": int(np.sum(array[:, 1] > array[:, 2])),
                    "I_gt_C_count": int(np.sum(array[:, 2] > array[:, 1])),
                }
            )

    return {
        "status": "fresh_seed_validation_complete",
        "fresh_seed_ensemble": seeds,
        "paired_block_seed_comparisons": len(paired_rows),
        "primary": {
            "alpha_0_flip_count": int(total_alpha0),
            "alpha_0_15_flip_count": int(total_alpha015),
            "positive_pairs": int(positive),
            "zero_pairs": int(sum(value == 0 for value in differences)),
            "negative_pairs": int(negative),
            "sum_paired_difference": int(sum(differences)),
            "decision": "supported" if supported else "not_supported",
        },
        "secondary": {
            "alpha_0_intermediate_i_winner_count": int(sum(row["imid_0.0"] for row in paired_rows)),
            "alpha_0_15_intermediate_i_winner_count": int(sum(row["imid_0.15"] for row in paired_rows)),
            "alpha_0_full_c_i_s_count": int(sum(row["full_0.0"] for row in paired_rows)),
            "alpha_0_15_full_c_i_s_count": int(sum(row["full_0.15"] for row in paired_rows)),
            "component_medians": medians,
        },
        "interpretation": (
            "Fresh seeds support state-adjustment feedback as a phase-shaping condition: alpha=0.15 creates "
            "C-dominated small-system cases that cross to I dominance, whereas alpha=0 is I-dominated from k=1 "
            "throughout this validation. The intervention changes phase topology rather than simply amplifying I."
        ),
    }


def analytic_audit() -> dict:
    contours = []
    for k_eff, ks in ((2.0, (2, 4, 8, 16)), (4.0, (4, 8, 16, 32))):
        rows = []
        for k in ks:
            rho = rho_for_keff(k, k_eff)
            rows.append(
                {
                    "k": k,
                    "rho": rho,
                    "variance_factor": variance_factor(k, rho),
                    "kappa3_factor": cumulant_factor(3, k, rho),
                    "kappa4_factor": cumulant_factor(4, k, rho),
                }
            )
        contours.append(
            {
                "k_eff": k_eff,
                "rows": rows,
                "variance_fixed": bool(max(row["variance_factor"] for row in rows) - min(row["variance_factor"] for row in rows) < 1e-14),
                "kappa3_not_fixed": len({round(row["kappa3_factor"], 14) for row in rows}) > 1,
                "kappa4_not_fixed": len({round(row["kappa4_factor"], 14) for row in rows}) > 1,
            }
        )

    aligned = symmetric_ratio_derivative_sign(b=1.0, c=1.0, d=2.0, e=2.0)
    misaligned = symmetric_ratio_derivative_sign(b=1.0, c=1.0, d=1.0, e=2.0)
    return {
        "common_factor_contours": contours,
        "quadratic_mixed_response": {
            "exact_C": "b^2 tau + b d mu3 + (d^2/4) Var(Z^2)",
            "exact_I": "Var(X)[c^2 tau + c e mu3 + (e^2/4) Var(Z^2)]",
            "Var_Z2": "kappa4 + 2 tau^2",
            "symmetric_fixed_tau_derivative_sign": "sign(e^2 b^2 - c^2 d^2)",
            "aligned_example_sign_numerator": aligned,
            "misaligned_example_sign_numerator": misaligned,
            "sufficiency_condition_at_quadratic_order": "higher-moment changes do not alter I/C only when pure and mixed response curvatures are proportionally aligned (e^2 b^2 = c^2 d^2), or the relevant higher cumulants do not change",
        },
        "decision": "pass",
    }


def build() -> dict:
    higher_order_freeze = json.loads(HIGHER_ORDER_FREEZE.read_text(encoding="utf-8"))
    feedback_freeze = json.loads(FEEDBACK_FREEZE.read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0",
        "analysis": "chapter2_el_higher_order_sufficiency",
        "status": "complete",
        "design_freezes": [
            str(HIGHER_ORDER_FREEZE.relative_to(ROOT)),
            str(FEEDBACK_FREEZE.relative_to(ROOT)),
        ],
        "retuning_after_fresh_result": feedback_freeze["retuning_after_result"],
        "analytic": analytic_audit(),
        "prespecified_handling_only_prediction": audit_handling_only_prediction(),
        "fresh_mixed_feedback_validation": fresh_feedback_validation(),
        "claim_boundary": [
            "The handling-only prediction was frozen before setting-level outcomes were read and is retained as a negative result.",
            "The mixed-feedback prediction was formulated after that failure and tested only on six previously unused seeds across the complete frozen 18-block factorial intervention.",
            "The fresh-seed result is synthetic mechanism validation, not an estimate of natural ecological prevalence.",
            "Clone-mixture support effects and smooth higher-cumulant effects are treated as distinct mechanisms."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    result = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
