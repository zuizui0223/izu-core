"""Read-only Q3→Q4 bridge feasibility audit from already exposed source receipts.

No plant genotypes, visitor histories, genetic paths or demographic trajectories
are generated. The source budget grid is post-discovery: all results are
descriptive, not fresh registration or independent confirmation.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/results/chapter2_original_evolved_budget_capacity_gate_receipt_20261010.json"
SHAPLEY = ROOT / "data/results/chapter2_original_evolved_resource_receipt_shapley_receipt_20261010.json"
CEILING = ROOT / "data/results/chapter2_original_evolved_K48_ceiling_receipt_20261010.json"
ORIGINAL = ROOT / "data/results/chapter2_original_evolved_pollen_service_receipt_20261010.json"
SETTINGS = ("delayed_control", "prior_selfing", "pollen_discount", "assurance_cost")
SCALES = (0.025, 0.05, 0.125, 0.25, 0.5, 1.0)
STATUS = "POSTDISCOVERY_READ_ONLY_BRIDGE_FEASIBILITY_NOT_PERSISTENCE"


def poisson_capped_mean(mu: float, capacity: int) -> float:
    """Exact E[min(Poisson(mu),K)] for finite mu and integer K>=1.

    Uses finite K-term deficit; large mu underflow gives the correct saturated K.
    No stochastic draw or external simulation library is involved.
    """
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
        raise ValueError("capacity must be a positive integer")
    if not math.isfinite(mu) or mu < 0:
        raise ValueError("expected viable seeds must be finite and nonnegative")
    term = math.exp(-mu)
    deficit = 0.0
    for i in range(capacity):
        deficit += (capacity - i) * term
        term *= mu / (i + 1)
    return min(float(capacity), max(0.0, capacity - deficit))


def one_step_occupancy(mu: float) -> float:
    """P(min(Poisson(mu), K)>0) = 1-exp(-mu), for K>=1.

    This identity depends on adult survival=0 and immigrant seed supply=0.
    Conditional one-year occupancy cannot identify a direct K effect at fixed mu.
    """
    if not math.isfinite(mu) or mu < 0:
        raise ValueError("invalid expected viable seed count")
    return -math.expm1(-mu)


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def audit(source: Path = SOURCE, shapley: Path = SHAPLEY, ceiling: Path = CEILING, original: Path = ORIGINAL) -> dict:
    b = _read(source)
    s = _read(shapley)
    c = _read(ceiling)
    o = _read(original)

    if (b.get("schema") != "chapter2_original_evolved_budget_capacity_gate_v1"
            or s.get("schema") != "chapter2_original_evolved_resource_receipt_shapley_v1"
            or c.get("schema") != "chapter2_native_one_step_K48_capacity_ceiling_result_v1"
            or o.get("schema") != "chapter2_original_evolved_pollen_service_source_result_v1"):
        raise ValueError("unknown historical source receipt schema")
    # Two distinct original result objects must NOT have equal SHA hashes.
    # Budget receipt comes from the Shapley source raw file; K48 ceiling
    # receipt comes from the earlier paired-genome source audit. Join both
    # through the parent original archived experiment/biological code.
    if (b["input_sha256"] != s["original_raw_full_json_sha256"]
            or c["parent_sha256"] != o["raw_output_sha256"]["paired"]
            or s["source_biology_sha256"] != o["source_reproduction_sha256"]):
        raise ValueError("cross-receipt SHA256 provenance mismatch")
    if (b["n_source_history_clusters"] != 64 or b["n_old_nested_repeats_used"] != 1
            or b["n_new_independent_histories"] != 0 or b["n_derived_one_year_cells"] != 1536
            or b["n_original_source_rows"] != 256 or b["n_mating_settings"] != 4
            or b["n_scales"] != 6 or b["fixed_K"] != 48 or b["fixed_B"] != 48
            or c["n_history_blocks"] != 64 or c["n_nested_repeats"] != 1
            or c["n_new_histories"] != 0 or s["independent_histories_new"] != 0
            or o["n_visitor_histories"] != 64 or o["n_nested_demographic_repeats"] != 1):
        raise ValueError("historical source unit or cohort contract changed")
    if not ("POST_DISCOVERY" in b["status"] and "POST_OUTCOME" in s["status"]
            and "NO_LONGRUN" in c["status"]):
        raise ValueError("receipt evidence ranks are not post-outcome one-step")
    rows = b["summary"]
    if len(rows) != 24 or len(c["near_t400"]) != 4 or len(s["rows"]) != 4:
        raise ValueError("incomplete original source matrix")
    indexed = {(r["setting"], float(r["budget_multiplier"])): r for r in rows}
    if len(indexed) != 24 or set(indexed) != {(name, b) for name in SETTINGS for b in SCALES}:
        raise ValueError("source settings or scales have changed")
    sh = {r["setting"]: r for r in s["rows"]}
    cp = {r["setting"]: r for r in c["near_t400"]}
    if set(sh) != set(SETTINGS) or set(cp) != set(SETTINGS):
        raise ValueError("misaligned source mating settings")

    for name in SETTINGS:
        q = sh[name]
        if not math.isclose(q["resource"] + q["receipt"], q["seed"], abs_tol=1e-9, rel_tol=0):
            raise ValueError("resource + pollen receipt no longer equals source maternal seed")
        if not q["delivered"] < 0:
            raise ValueError("source pollen transfer sign changed")
        full = indexed[(name, 1.0)]
        if not math.isclose(
            full["delta_next_N_mean"], cp[name]["mean_expected_census_delta"],
            abs_tol=1e-6, rel_tol=0
        ):
            raise ValueError("one-year K48 exact source census and fixed-budget receipt disagree")

    def scale_rows(multiplier: float) -> dict:
        entries = [indexed[(name, multiplier)] for name in SETTINGS]
        return {
            "budget_multiplier": multiplier,
            "min_occupancy_across_settings": min(r["mean_E_one_step_occupancy"] for r in entries),
            "intermediate_expected_N_both_arms_per_setting": {
                r["setting"]: r["n_both_N_in_0p1K_0p9K"] for r in entries
            },
            "E_histories_with_one_year_occupancy_0p1_to_0p9": {
                r["setting"]: r["n_E_occupancy_in_0p1_0p9"] for r in entries
            },
            "E_minus_clamp_expected_next_N_mean": {
                r["setting"]: r["delta_next_N_mean"] for r in entries
            },
            "E_minus_clamp_history_bootstrap95_posthoc": {
                r["setting"]: r["delta_next_N_history_bootstrap95_descriptive"] for r in entries
            },
        }

    # A deterministic, source-wide upper bound: both original viable-seed
    # intensities (evolved and investment-restored) are >= the frozen minimum.
    # Scaling by b preserves that inequality. Since P(occupied)=1-exp(-mu),
    # their absolute one-step occupancy difference cannot exceed exp(-b*min_mu).
    # This is NOT a confidence interval, realized effect or long-run bound.
    original_min_viable_seed = min(
        float(q["min_viable_mu_either_branch"]) for q in cp.values()
    )
    if not original_min_viable_seed > 0:
        raise ValueError("invalid archived minimum source viable seed mean")
    maximal_absolute_one_step_occupancy_change_by_scale = {
        str(factor): math.exp(-factor * original_min_viable_seed) for factor in SCALES
    }

    by_scale = [scale_rows(factor) for factor in SCALES]
    intermediate_E_total = sum(r["n_E_occupancy_in_0p1_0p9"] for r in rows)
    max_intermediate_E_in_any_64_history_setting = max(
        r["n_E_occupancy_in_0p1_0p9"] for r in rows
    )
    min_setting_mean_one_year_E_occupancy = min(r["mean_E_one_step_occupancy"] for r in rows)
    number_positive_seed = sum(q["seed"] > 0 for q in sh.values())
    if number_positive_seed != 3:
        raise ValueError("post-outcome group-seed compensation result changed")

    # Independent exact numeric illustration cited from separate, UNMERGED #452
    # source, with parameters held at the reported original monomorphic fixture.
    # Do not pass this fixture off as a validated new natural source system.
    source_mu = 8.99442
    example = {
        "provenance": "unmerged_PR_452_source_monorphic_N8_B48_budget6_NOT_IN_MAIN",
        "source_viable_mu": source_mu,
        "census_K8_expected_next_N": poisson_capped_mean(source_mu, 8),
        "census_K48_expected_next_N": poisson_capped_mean(source_mu, 48),
        "one_year_occupancy_both_K_given_same_mu": one_step_occupancy(source_mu),
        "note": "Expected N can be below K8 despite mu>N8. P(N'>0) is K-invariant at fixed mu, NOT an 80-update result."
    }

    return {
        "schema": "chapter2_four_question_q3q4_source_feasibility_v1",
        "status": STATUS,
        "n_new_independent_histories": 0,
        "n_new_stochastic_trajectories": 0,
        "n_original_reused_histories": 64,
        "n_old_nested_repeats_per_history": 1,
        "n_exposed_one_year_cells": b["n_derived_one_year_cells"],
        "source_original_shapley_raw_sha256": b["input_sha256"],
        "source_original_paired_raw_sha256": c["parent_sha256"],
        "source_original_reproductive_biology_sha256": o["source_reproduction_sha256"],
        "original_min_viable_seed_mean_across_original_source_arms": original_min_viable_seed,
        "rigorous_max_absolute_conditional_one_step_occupancy_change_by_scale": (
            maximal_absolute_one_step_occupancy_change_by_scale
        ),
        "bound_note": (
            "For the previously observed source states only, at the same original "
            "genotypes, visitor states and scaled b, all compared original viable-seed "
            "means are >= b*min_mu. Any one-generation occupancy probability "
            "difference is <= exp(-b*min_mu). This is a deterministic upper bound "
            "on expected conditional occupancy, not a CI or multi-generation result."
        ),
        "fixed_K": 48,
        "fixed_B": 48,
        "tested_scale_grid_post_outcome": list(SCALES),
        "by_scale": by_scale,
        "n_source_E_history_scale_cells_with_intermediate_one_year_occupancy": intermediate_E_total,
        "n_total_E_history_scale_cells": 64 * 4 * 6,
        "max_intermediate_E_per_64_history_setting": max_intermediate_E_in_any_64_history_setting,
        "minimum_setting_mean_E_one_year_occupancy": min_setting_mean_one_year_E_occupancy,
        "n_settings_with_mean_seed_increase_despite_delivered_pollen_loss": number_positive_seed,
        "census_example_unmerged_source": example,
        "decision": "NO_GO_FOR_CURRENT_SOURCE_GRID_AS_Q3_TO_Q4_LONGITUDINAL_CONFIRMATION",
        "scientific_interpretation": (
            "One-step expected census can be unsaturated while one-step binary occupancy "
            "remains close to one; mean group-seed contrasts are heterogeneous. An "
            "independently registered source-genotype to 80-update survival causal "
            "contrast cannot be identified by recycling these observed budget cells."
        ),
        "limits": [
            "Descriptive after-outcome combination of original #457 one-year source receipts; no new experiment or preregistration.",
            "The K8 example is a separately sourced unmerged exploratory #452 monomorphic fixture, not a natural island model.",
            "Within a fixed viable seed mean and zero adult survival/immigration, one-year occupancy does not directly depend on K.",
            "Neither conditional one-generation seed nor expected recruitment identifies inherited evolution or unconditional 80-update survival.",
            "No favorable resource multiplier, source history or visitor composition may be selected here for a fresh confirmatory claim.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "status", "n_source_E_history_scale_cells_with_intermediate_one_year_occupancy",
        "n_total_E_history_scale_cells", "minimum_setting_mean_E_one_year_occupancy",
        "decision",
    )}, sort_keys=True))


if __name__ == "__main__":
    main()
