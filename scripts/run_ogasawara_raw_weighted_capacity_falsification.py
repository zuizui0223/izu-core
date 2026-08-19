from __future__ import annotations

import csv
import itertools
import json
import math
from bisect import bisect_right
from pathlib import Path

REFERENCE_GEO = Path("data/results/frozen_candidate_gift_geography_match.json")
OGASAWARA_GEO = Path("data/results/ogasawara_gift_capacity_match.json")
OGASAWARA_METRICS = Path("data/results/ogasawara/context_analysis/island_metrics.csv")
ABM_DIRECTION = Path("data/results/abm_v4_global_continuous_isolation_gradient.json")
OUT = Path("data/results/ogasawara_raw_weighted_capacity_falsification.json")

# PR #188 source-native structure filtering removed these four frozen Doré rows.
# PR #187 defined the small-area diagnostic on the remaining corrected rows.
CORRECTED_STRUCTURE_EXCLUSIONS = {"RP160", "RP163", "RP197", "RP222"}
EXPECTED_ISLANDS = {"A_Chichijima", "B_Hahajima", "C_Anijima", "D_Ototojima"}


def ranks(values: list[float]) -> list[float]:
    ordered = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(ordered):
        j = i + 1
        while j < len(ordered) and values[ordered[j]] == values[ordered[i]]:
            j += 1
        average_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            out[ordered[k]] = average_rank
        i = j
    return out


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("vectors must have the same length >= 2")
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    den = math.sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    if den == 0:
        return 0.0
    return sum(a * b for a, b in zip(dx, dy)) / den


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(ranks(x), ranks(y))


def exact_permutation_test(x: list[float], y: list[float], alternative: str) -> dict:
    observed = spearman(x, y)
    permutations = list(dict.fromkeys(itertools.permutations(y)))
    statistics = [spearman(x, list(permuted)) for permuted in permutations]
    eps = 1e-12
    if alternative == "less":
        extreme = sum(value <= observed + eps for value in statistics)
    elif alternative == "greater":
        extreme = sum(value >= observed - eps for value in statistics)
    elif alternative == "two-sided":
        extreme = sum(abs(value) >= abs(observed) - eps for value in statistics)
    else:
        raise ValueError(alternative)
    return {
        "rho": observed,
        "alternative": alternative,
        "exact_permutation_p": extreme / len(statistics),
        "permutation_count": len(statistics),
    }


def reference_unique_log_areas(payload: dict) -> list[float]:
    areas = []
    admitted_regions = set()
    for row in payload["matches"]:
        if row.get("kind") != "dore_network_location":
            continue
        region = row.get("region_pub")
        if region in CORRECTED_STRUCTURE_EXCLUSIONS:
            continue
        if not row.get("auto_lock"):
            raise RuntimeError(f"corrected reference geography is not locked for {region}")
        candidates = row.get("top_candidates") or []
        if not candidates or candidates[0].get("area_km2") is None:
            raise RuntimeError(f"corrected reference area missing for {region}")
        areas.append(math.log1p(float(candidates[0]["area_km2"])))
        admitted_regions.add(region)
    if len(admitted_regions) != 22:
        raise RuntimeError(f"expected 22 corrected reference regions, got {len(admitted_regions)}")
    unique = sorted(set(areas))
    if len(unique) < 2:
        raise RuntimeError("reference area distribution has fewer than two unique values")
    return unique


def frozen_capacity_index(area_km2: float, reference_log_areas: list[float]) -> float:
    """Extend PR #187 reverse rank by linear interpolation on its frozen unique log-area grid."""
    x = math.log1p(area_km2)
    n = len(reference_log_areas)
    if x <= reference_log_areas[0]:
        return 1.0
    if x >= reference_log_areas[-1]:
        return 0.0
    hi = bisect_right(reference_log_areas, x)
    lo = hi - 1
    x0, x1 = reference_log_areas[lo], reference_log_areas[hi]
    fraction = (x - x0) / (x1 - x0)
    position = (lo + fraction) / (n - 1)
    return 1.0 - position


def pairwise_concordance(rows: list[dict], outcome: str, expected: str) -> dict:
    concordant = 0
    discordant = 0
    ties = 0
    details = []
    for a, b in itertools.combinations(rows, 2):
        if a["capacity_index"] == b["capacity_index"]:
            ties += 1
            continue
        strong, weak = (a, b) if a["capacity_index"] > b["capacity_index"] else (b, a)
        observed_delta = strong[outcome] - weak[outcome]
        match = observed_delta < 0 if expected == "decrease" else observed_delta > 0
        if observed_delta == 0:
            ties += 1
            state = "tie"
        elif match:
            concordant += 1
            state = "concordant"
        else:
            discordant += 1
            state = "discordant"
        details.append({
            "stronger_constraint": strong["island"],
            "weaker_constraint": weak["island"],
            "observed_delta": observed_delta,
            "state": state,
        })
    return {
        "concordant_pairs": concordant,
        "discordant_pairs": discordant,
        "ties": ties,
        "details": details,
    }


def load_rows() -> tuple[list[dict], dict]:
    reference = json.loads(REFERENCE_GEO.read_text())
    og_geo = json.loads(OGASAWARA_GEO.read_text())
    ref_areas = reference_unique_log_areas(reference)

    if not og_geo.get("all_locked"):
        return [], {
            "status": "blocked_ogasawara_gift_geography_not_fully_locked",
            "geography": og_geo,
        }
    area_by_island = {
        row["source_island"]: float(row["selected"]["area_km2"])
        for row in og_geo["matches"]
    }
    if set(area_by_island) != EXPECTED_ISLANDS:
        raise RuntimeError("Ogasawara geography target set drifted")

    rows = []
    with OGASAWARA_METRICS.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            island = row["island"]
            if island not in EXPECTED_ISLANDS:
                continue
            area = area_by_island[island]
            rows.append({
                "island": island,
                "area_km2": area,
                "capacity_index": frozen_capacity_index(area, ref_areas),
                "interaction_shannon": float(row["interaction_shannon"]),
                "plant_niche_overlap": float(row["mean_plant_niche_overlap_morisita_horn"]),
                "n_long_rows": float(row["n_long_rows"]),
                "total_visitation_rate": float(row["total_visitation_rate"]),
                "n_positive_links": float(row["n_positive_links"]),
            })
    if {row["island"] for row in rows} != EXPECTED_ISLANDS:
        raise RuntimeError("Ogasawara weighted outcome island set drifted")
    rows.sort(key=lambda row: row["capacity_index"], reverse=True)
    return rows, {
        "status": "ready",
        "reference_unique_log_area_count": len(ref_areas),
        "geography": og_geo,
    }


def build() -> dict:
    abm = json.loads(ABM_DIRECTION.read_text())
    if not abm["tests"]["interaction_diversity_declines"]:
        raise RuntimeError("pre-existing ABM interaction-diversity direction is not negative")
    if not abm["tests"]["plant_niche_overlap_increases"]:
        raise RuntimeError("pre-existing ABM plant-niche-overlap direction is not positive")

    rows, gate = load_rows()
    if not rows:
        return {
            "schema_version": "1.0",
            "analysis": "ogasawara_raw_weighted_capacity_falsification",
            "decision": gate["status"],
            "gate": gate,
            "claim_boundary": "No biological result is emitted until all four Ogasawara islands have outcome-blind GIFT area locks.",
        }

    capacity = [row["capacity_index"] for row in rows]
    shannon = [row["interaction_shannon"] for row in rows]
    overlap = [row["plant_niche_overlap"] for row in rows]
    shannon_test = exact_permutation_test(capacity, shannon, "less")
    overlap_test = exact_permutation_test(capacity, overlap, "greater")
    effort_rows = exact_permutation_test(capacity, [row["n_long_rows"] for row in rows], "two-sided")
    effort_visits = exact_permutation_test(capacity, [row["total_visitation_rate"] for row in rows], "two-sided")

    shannon_direction = shannon_test["rho"] < 0
    overlap_direction = overlap_test["rho"] > 0
    shannon_exact = shannon_test["exact_permutation_p"] <= 0.05
    overlap_exact = overlap_test["exact_permutation_p"] <= 0.05
    if shannon_exact and overlap_exact:
        decision = "ogasawara_raw_weighted_supports_both_capacity_directions_at_exact_rank_level"
    elif shannon_direction and overlap_direction:
        decision = "ogasawara_raw_weighted_matches_both_capacity_directions_without_joint_exact_support"
    elif shannon_direction or overlap_direction:
        decision = "ogasawara_raw_weighted_capacity_result_is_mixed"
    else:
        decision = "ogasawara_raw_weighted_falsifies_both_capacity_directions"

    return {
        "schema_version": "1.0",
        "analysis": "ogasawara_raw_weighted_capacity_falsification",
        "status": "held_out_archipelago_weighted_outcome_test_of_postresult_capacity_hypothesis",
        "hypothesis_origin": "PR #187 post-result topology diagnostic; Ogasawara weighted outcomes were not used to define the small-area axis or its predicted directions.",
        "capacity_mapping": "PR #187 reverse rank on the corrected 22-row unique log(area) grid, extended to new areas by piecewise-linear interpolation and clamped at the frozen endpoints.",
        "pre_existing_abm_direction_source": str(ABM_DIRECTION),
        "predeclared_directions": {
            "interaction_shannon": "decrease as capacity constraint strengthens",
            "plant_niche_overlap_morisita_horn": "increase as capacity constraint strengthens",
        },
        "n_islands": len(rows),
        "rows": rows,
        "tests": {
            "interaction_shannon": shannon_test,
            "plant_niche_overlap": overlap_test,
            "pairwise_interaction_shannon": pairwise_concordance(rows, "interaction_shannon", "decrease"),
            "pairwise_plant_niche_overlap": pairwise_concordance(rows, "plant_niche_overlap", "increase"),
        },
        "sampling_diagnostics": {
            "capacity_vs_network_row_count": effort_rows,
            "capacity_vs_total_visitation_rate": effort_visits,
            "rule": "Sampling diagnostics are reported as potential confounding checks and do not change the predeclared biological direction after results are seen.",
        },
        "geography_gate": gate,
        "decision": decision,
        "next_gate": "If both raw weighted directions survive, validate the capacity hypothesis in another independent multi-island quantitative network system before any global coefficient or universal capacity claim. If either direction fails, retain the failure and revise the capacity hypothesis rather than selecting islands or outcomes post hoc.",
        "claim_boundary": "Four Ogasawara islands are independent island units within one archipelago, not four independent archipelagos. The test is directional and rank-based; it does not estimate a global area coefficient, identify island area causally, erase invasion/forest/sampling differences, or convert legitimate interaction counts into pollinator effectiveness or reproductive success.",
    }


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "decision": payload["decision"],
        "n_islands": payload.get("n_islands"),
        "tests": payload.get("tests"),
        "sampling_diagnostics": payload.get("sampling_diagnostics"),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
