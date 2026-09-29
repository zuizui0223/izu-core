from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
import urllib.request
from collections import defaultdict
from pathlib import Path

from scipy.stats import spearmanr

from channel_id.external_archipelago_network import canonical_label

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSIS = ROOT / "data/design/cabrera_v8_failure_diagnosis_v1.json"
VALIDATION = ROOT / "data/design/abm_v8_cabrera_validation_v1.json"
OUT = ROOT / "data/results/cabrera_v8_failure_layer_diagnosis.json"
CSV_URL = "https://digital.csic.es/bitstream/10261/420466/1/cabrera_22_23_habitat.csv"
CSV_SHA256 = "399ec11ae6ce18c8e9ebb050857ca7c1da4cb4a7858e24382750a92ae5e16a07"
USER_AGENT = "izu-core-cabrera-failure-diagnosis/1.0"


def fetch_rows() -> list[dict[str, str]]:
    request = urllib.request.Request(CSV_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != CSV_SHA256:
        raise RuntimeError(f"Cabrera source checksum drift: {actual}")
    text = None
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = payload.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise RuntimeError("Cabrera source could not be decoded")
    rows = list(csv.DictReader(io.StringIO(text), delimiter=";"))
    if len(rows) != 3874:
        raise RuntimeError(f"Cabrera source row count drifted: {len(rows)}")
    return [dict(row) for row in rows]


def numeric(value: object) -> float | None:
    text = str(value or "").strip().replace(",", ".")
    if not text or text.lower() in {"na", "nan", "null", "none", "-"}:
        return None
    try:
        result = float(text)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def shannon(weights) -> float:
    positive = [float(value) for value in weights if float(value) > 0.0]
    total = sum(positive)
    if total <= 0.0:
        return 0.0
    return -sum((value / total) * math.log(value / total) for value in positive)


def median(values: list[float]) -> float | None:
    return None if not values else float(statistics.median(values))


def context_pairs_and_pooled(rows: list[dict[str, str]], locked: list[tuple[str, str]]):
    locked_set = set(locked)
    obs = [row for row in rows if row.get("Method", "").strip() == "obs"]
    observed = {
        (row.get("COMMUNITY", "").strip(), row.get("visita", "").strip())
        for row in obs
        if row.get("COMMUNITY", "").strip() and row.get("visita", "").strip()
    }
    if observed != locked_set:
        raise RuntimeError("Cabrera obs context membership drifted")

    by_context: dict[tuple[str, str], list[dict[str, str]]] = {key: [] for key in locked}
    for row in obs:
        key = (row.get("COMMUNITY", "").strip(), row.get("visita", "").strip())
        if key not in locked_set:
            raise RuntimeError(f"unexpected Cabrera obs context: {key}")
        by_context[key].append(row)

    weights_by_context: dict[tuple[str, str], dict[tuple[str, str], float]] = {}
    pooled: dict[tuple[str, str], float] = {}
    for key, subset in by_context.items():
        weights: dict[tuple[str, str], float] = {}
        for row in subset:
            plant = row.get("Plant sp", "").strip()
            pollinator = row.get("Pollinator", "").strip()
            amount = numeric(row.get("N ind"))
            if not pollinator:
                if amount == 0.0:
                    continue
                raise RuntimeError("blank pollinator row is not explicit N ind=0")
            if not plant or amount is None or amount <= 0.0:
                raise RuntimeError("positive interaction row lacks frozen plant/pollinator/N ind structure")
            pair = (canonical_label(plant), canonical_label(pollinator))
            weights[pair] = weights.get(pair, 0.0) + amount
            pooled[pair] = pooled.get(pair, 0.0) + amount
        weights_by_context[key] = weights
    return by_context, weights_by_context, pooled


def unique_consistent_sum(
    subset: list[dict[str, str]],
    *,
    key_fields: tuple[str, ...],
    value_field: str,
) -> tuple[float | None, int]:
    values_by_key: dict[tuple[str, ...], set[float]] = defaultdict(set)
    missing_keys = 0
    for row in subset:
        key = tuple(row.get(field, "").strip() for field in key_fields)
        if not all(key):
            continue
        value = numeric(row.get(value_field))
        if value is None:
            missing_keys += 1
            continue
        values_by_key[key].add(value)
    inconsistent = sum(len(values) > 1 for values in values_by_key.values())
    if inconsistent or missing_keys:
        return None, inconsistent + missing_keys
    return sum(next(iter(values)) for values in values_by_key.values()), 0


def spearman_summary(contexts: list[dict], x_key: str, y_key: str) -> dict:
    valid = [
        row for row in contexts
        if row.get(x_key) is not None and row.get(y_key) is not None
    ]
    if len(valid) < 3:
        return {"n": len(valid), "rho": None, "leave_one_community_out_rho_range": None}
    xs = [float(row[x_key]) for row in valid]
    ys = [float(row[y_key]) for row in valid]
    rho = float(spearmanr(xs, ys).statistic)
    if not math.isfinite(rho):
        rho = None

    leave_one = []
    communities = sorted({row["community"] for row in valid})
    for community in communities:
        subset = [row for row in valid if row["community"] != community]
        if len(subset) < 3:
            continue
        sx = [float(row[x_key]) for row in subset]
        sy = [float(row[y_key]) for row in subset]
        value = float(spearmanr(sx, sy).statistic)
        if math.isfinite(value):
            leave_one.append({"excluded_community": community, "rho": value})
    return {
        "n": len(valid),
        "rho": rho,
        "leave_one_community_out": leave_one,
        "leave_one_community_out_rho_range": (
            [min(row["rho"] for row in leave_one), max(row["rho"] for row in leave_one)]
            if leave_one else None
        ),
    }


def main() -> None:
    diagnosis = json.loads(DIAGNOSIS.read_text())
    validation = json.loads(VALIDATION.read_text())
    if diagnosis["failure_source"]["decision"] != "v8_fails_cabrera_conditional_pair_support_predictive_adequacy":
        raise RuntimeError("diagnosis is not bound to the preserved v8 failure")
    if validation["source_native_reconstruction"]["primary_method_label"] != "obs":
        raise RuntimeError("Cabrera primary method drifted")
    if validation["source_native_reconstruction"]["primary_interaction_weight"] != "N ind":
        raise RuntimeError("Cabrera primary interaction weight drifted")

    locked = [tuple(key) for key in validation["source_native_reconstruction"]["locked_context_keys"]]
    rows = fetch_rows()
    by_context, weights_by_context, pooled = context_pairs_and_pooled(rows, locked)
    opportunity_pairs = {pair for pair, amount in pooled.items() if amount > 0.0}
    pooled_plants = {plant for plant, _ in opportunity_pairs}
    if len(opportunity_pairs) != 295 or len(pooled_plants) != 22:
        raise RuntimeError("Cabrera pooled opportunity drifted from preserved v8 failure")

    context_rows = []
    duration_inconsistency_contexts = []
    flower_inconsistency_contexts = []
    for key in locked:
        subset = by_context[key]
        weights = weights_by_context[key]
        active_pairs = {pair for pair, amount in weights.items() if amount > 0.0}
        sampled_plants = {
            canonical_label(row.get("Plant sp", ""))
            for row in subset
            if row.get("Plant sp", "").strip()
        }
        sampled_positive_plants = sampled_plants & pooled_plants
        plant_conditioned_pairs = {
            pair for pair in opportunity_pairs if pair[0] in sampled_positive_plants
        }

        census_keys = {
            row.get("censo", "").strip()
            for row in subset
            if row.get("censo", "").strip()
        }
        total_minutes, duration_issues = unique_consistent_sum(
            subset,
            key_fields=("censo",),
            value_field="Delta_T_minutes",
        )
        observed_flowers, flower_issues = unique_consistent_sum(
            subset,
            key_fields=("censo", "Plant sp"),
            value_field="N observed flowers",
        )
        if duration_issues:
            duration_inconsistency_contexts.append({"community": key[0], "visita": key[1], "issue_count": duration_issues})
        if flower_issues:
            flower_inconsistency_contexts.append({"community": key[0], "visita": key[1], "issue_count": flower_issues})

        h = shannon(weights.values())
        positive_pair_count = len(active_pairs)
        evenness = h / math.log(positive_pair_count) if positive_pair_count > 1 else 0.0
        total_n_ind = sum(weights.values())
        context_rows.append({
            "community": key[0],
            "visita": key[1],
            "global_pair_support_fraction": len(active_pairs) / len(opportunity_pairs),
            "sampled_positive_plant_fraction": len(sampled_positive_plants) / len(pooled_plants),
            "sampled_positive_plant_count": len(sampled_positive_plants),
            "plant_conditioned_pair_opportunity_fraction": len(plant_conditioned_pairs) / len(opportunity_pairs),
            "plant_conditioned_pair_opportunity_count": len(plant_conditioned_pairs),
            "pair_realization_given_sampled_plants": (
                len(active_pairs) / len(plant_conditioned_pairs) if plant_conditioned_pairs else None
            ),
            "unique_census_count": len(census_keys),
            "total_unique_census_minutes": total_minutes,
            "observed_flower_exposure": observed_flowers,
            "positive_pair_count": positive_pair_count,
            "total_n_ind": total_n_ind,
            "interaction_shannon": h,
            "interaction_evenness": evenness,
        })

    relationships = {
        "global_pair_support_vs_sampled_positive_plant_fraction": spearman_summary(
            context_rows, "sampled_positive_plant_fraction", "global_pair_support_fraction"
        ),
        "global_pair_support_vs_plant_conditioned_pair_opportunity_fraction": spearman_summary(
            context_rows, "plant_conditioned_pair_opportunity_fraction", "global_pair_support_fraction"
        ),
        "conditional_pair_realization_vs_unique_census_count": spearman_summary(
            context_rows, "unique_census_count", "pair_realization_given_sampled_plants"
        ),
        "conditional_pair_realization_vs_total_unique_census_minutes": spearman_summary(
            context_rows, "total_unique_census_minutes", "pair_realization_given_sampled_plants"
        ),
        "conditional_pair_realization_vs_observed_flower_exposure": spearman_summary(
            context_rows, "observed_flower_exposure", "pair_realization_given_sampled_plants"
        ),
        "shannon_vs_positive_pair_count": spearman_summary(
            context_rows, "positive_pair_count", "interaction_shannon"
        ),
        "shannon_vs_total_n_ind": spearman_summary(
            context_rows, "total_n_ind", "interaction_shannon"
        ),
        "shannon_vs_sampled_positive_plant_fraction": spearman_summary(
            context_rows, "sampled_positive_plant_fraction", "interaction_shannon"
        ),
        "evenness_vs_positive_pair_count": spearman_summary(
            context_rows, "positive_pair_count", "interaction_evenness"
        ),
    }

    global_fractions = [row["global_pair_support_fraction"] for row in context_rows]
    sampled_plant_fractions = [row["sampled_positive_plant_fraction"] for row in context_rows]
    plant_opportunity_fractions = [row["plant_conditioned_pair_opportunity_fraction"] for row in context_rows]
    conditional_realization = [
        row["pair_realization_given_sampled_plants"]
        for row in context_rows if row["pair_realization_given_sampled_plants"] is not None
    ]
    shannons = [row["interaction_shannon"] for row in context_rows]
    evenness = [row["interaction_evenness"] for row in context_rows]

    payload = {
        "schema_version": "1.0",
        "analysis": "cabrera_v8_failure_layer_diagnosis",
        "status": "post_falsification_diagnosis_not_model_rescue",
        "preserved_failure_decision": diagnosis["failure_source"]["decision"],
        "context_count": len(context_rows),
        "pooled_opportunity": {
            "positive_pair_count": len(opportunity_pairs),
            "positive_plant_count": len(pooled_plants),
        },
        "decomposition_summary": {
            "median_global_pair_support_fraction": median(global_fractions),
            "median_sampled_positive_plant_fraction": median(sampled_plant_fractions),
            "median_plant_conditioned_pair_opportunity_fraction": median(plant_opportunity_fractions),
            "median_pair_realization_given_sampled_plants": median(conditional_realization),
            "median_conditional_to_global_pair_fraction_ratio": (
                median(conditional_realization) / median(global_fractions)
                if median(conditional_realization) is not None and median(global_fractions) not in (None, 0.0)
                else None
            ),
            "interaction_shannon_range": max(shannons) - min(shannons),
            "interaction_evenness_range": max(evenness) - min(evenness),
            "interaction_shannon_median": median(shannons),
            "interaction_evenness_median": median(evenness),
        },
        "exposure_consistency": {
            "duration_inconsistency_contexts": duration_inconsistency_contexts,
            "observed_flower_inconsistency_contexts": flower_inconsistency_contexts,
            "duration_metric_available_for_all_contexts": not duration_inconsistency_contexts,
            "observed_flower_metric_available_for_all_contexts": not flower_inconsistency_contexts,
        },
        "descriptive_relationships": relationships,
        "contexts": context_rows,
        "v8_parameters_reestimated": False,
        "primary_v8_result_relabelled": False,
        "claim_boundary": diagnosis["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "preserved_failure_decision": payload["preserved_failure_decision"],
        "decomposition_summary": payload["decomposition_summary"],
        "exposure_consistency": payload["exposure_consistency"],
        "descriptive_relationships": payload["descriptive_relationships"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
