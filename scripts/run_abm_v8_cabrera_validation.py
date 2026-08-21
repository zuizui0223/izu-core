from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import math
import random
import statistics
import sys
import urllib.request
from itertools import combinations
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, canonical_label

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v8_cabrera_validation_v1.json"
V8_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v8_pair_support.py"
V6_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v6_local_support.py"
V5_SCRIPT = ROOT / "scripts/run_constraint_mechanism_abm_v5_hierarchical_context.py"
OUT = ROOT / "data/results/abm_v8_cabrera_validation.json"
CSV_URL = "https://digital.csic.es/bitstream/10261/420466/1/cabrera_22_23_habitat.csv"
CSV_SHA256 = "399ec11ae6ce18c8e9ebb050857ca7c1da4cb4a7858e24382750a92ae5e16a07"
USER_AGENT = "izu-core-cabrera-v8-validation/1.0"
SEED = 20260821
EPS = 1e-12


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def fetch_source() -> list[dict[str, str]]:
    request = urllib.request.Request(CSV_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response:
        payload = response.read()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != CSV_SHA256:
        raise RuntimeError(f"Cabrera CSV checksum drift: {actual}")
    text = None
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            text = payload.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        raise RuntimeError("Cabrera CSV cannot be decoded")
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


def percentile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("percentile requires values")
    ordered = sorted(float(value) for value in values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def envelope(values: list[float]) -> dict[str, float]:
    return {
        "p2.5": percentile(values, 0.025),
        "median": percentile(values, 0.5),
        "p97.5": percentile(values, 0.975),
    }


def inside(value: float, interval: dict[str, float]) -> bool:
    return interval["p2.5"] <= value <= interval["p97.5"]


def pair_set_from_network(network: WeightedNetwork | None) -> set[tuple[str, str]]:
    if network is None:
        return set()
    pairs: set[tuple[str, str]] = set()
    for plant_index, plant in enumerate(network.plant_names):
        for pollinator_index, pollinator in enumerate(network.pollinator_names):
            if network.matrix[plant_index][pollinator_index] > 0.0:
                pairs.add((canonical_label(plant), canonical_label(pollinator)))
    return pairs


def context_stats(
    pair_sets: list[set[tuple[str, str]]],
    shannons: list[float],
    *,
    opportunity_pairs: set[tuple[str, str]],
    pooled_shannon: float,
    pooled_plants: set[str],
    pooled_pollinators: set[str],
) -> dict[str, float | int | dict]:
    if not pair_sets or len(pair_sets) != len(shannons):
        raise ValueError("context statistics require aligned context data")
    if not opportunity_pairs:
        raise ValueError("pooled opportunity pair set is empty")
    if pooled_shannon <= 0.0:
        raise ValueError("pooled Shannon must be positive")

    pair_fractions = [len(pairs) / len(opportunity_pairs) for pairs in pair_sets]
    turnovers = []
    for left, right in combinations(pair_sets, 2):
        union = left | right
        turnovers.append(0.0 if not union else 1.0 - len(left & right) / len(union))

    plant_fractions = []
    pollinator_fractions = []
    positive_pair_counts = []
    for pairs in pair_sets:
        plants = {plant for plant, _ in pairs}
        pollinators = {pollinator for _, pollinator in pairs}
        plant_fractions.append(len(plants) / len(pooled_plants) if pooled_plants else 0.0)
        pollinator_fractions.append(len(pollinators) / len(pooled_pollinators) if pooled_pollinators else 0.0)
        positive_pair_counts.append(len(pairs))

    return {
        "median_pair_support_fraction": float(statistics.median(pair_fractions)),
        "mean_pair_support_jaccard_turnover": float(statistics.mean(turnovers)) if turnovers else 0.0,
        "interaction_shannon_relative_context_range": (max(shannons) - min(shannons)) / pooled_shannon,
        "secondary": {
            "pair_support_fraction_min": min(pair_fractions),
            "pair_support_fraction_max": max(pair_fractions),
            "active_plant_fraction_median": float(statistics.median(plant_fractions)),
            "active_plant_fraction_range": max(plant_fractions) - min(plant_fractions),
            "active_pollinator_fraction_median": float(statistics.median(pollinator_fractions)),
            "active_pollinator_fraction_range": max(pollinator_fractions) - min(pollinator_fractions),
            "empty_context_count": sum(not pairs for pairs in pair_sets),
            "positive_pair_count_min": min(positive_pair_counts),
            "positive_pair_count_max": max(positive_pair_counts),
            "shannon_min": min(shannons),
            "shannon_max": max(shannons),
        },
    }


def empirical_summary(design: dict) -> tuple[dict, WeightedNetwork]:
    rows = fetch_source()
    rule = design["source_native_reconstruction"]
    locked = [tuple(key) for key in rule["locked_context_keys"]]
    locked_set = set(locked)
    obs_rows = [row for row in rows if row.get("Method", "").strip() == rule["primary_method_label"]]
    observed_keys = {
        (row.get("COMMUNITY", "").strip(), row.get("visita", "").strip())
        for row in obs_rows
        if row.get("COMMUNITY", "").strip() and row.get("visita", "").strip()
    }
    if observed_keys != locked_set or len(locked) != 55:
        raise RuntimeError("Cabrera obs context membership drifted before target reconstruction")

    context_pair_weights: dict[tuple[str, str], dict[tuple[str, str], float]] = {key: {} for key in locked}
    sampled_plants_by_context: dict[tuple[str, str], set[str]] = {key: set() for key in locked}
    source_zero_rows = 0
    for row in obs_rows:
        context = (row.get("COMMUNITY", "").strip(), row.get("visita", "").strip())
        if context not in locked_set:
            raise RuntimeError(f"unlocked obs context encountered: {context}")
        plant_raw = row.get("Plant sp", "")
        if plant_raw.strip():
            sampled_plants_by_context[context].add(canonical_label(plant_raw))
        pollinator_raw = row.get("Pollinator", "")
        amount = numeric(row.get("N ind"))
        if not pollinator_raw.strip():
            if amount == 0.0:
                source_zero_rows += 1
                continue
            raise RuntimeError("blank Pollinator row is not an explicit N ind=0 absence record")
        if amount is None or amount <= 0.0:
            raise RuntimeError("nonblank Pollinator row lacks positive numeric N ind")
        if not plant_raw.strip():
            raise RuntimeError("positive pollinator interaction lacks Plant sp")
        pair = (canonical_label(plant_raw), canonical_label(pollinator_raw))
        context_pair_weights[context][pair] = context_pair_weights[context].get(pair, 0.0) + amount

    pooled: dict[tuple[str, str], float] = {}
    for weights in context_pair_weights.values():
        for pair, amount in weights.items():
            pooled[pair] = pooled.get(pair, 0.0) + amount
    opportunity_pairs = {pair for pair, amount in pooled.items() if amount > 0.0}
    if not opportunity_pairs:
        raise RuntimeError("Cabrera pooled opportunity contains no positive pair")

    plants = sorted({plant for plant, _ in opportunity_pairs})
    pollinators = sorted({pollinator for _, pollinator in opportunity_pairs})
    plant_index = {plant: i for i, plant in enumerate(plants)}
    pollinator_index = {pollinator: i for i, pollinator in enumerate(pollinators)}
    matrix = [[0.0 for _ in pollinators] for _ in plants]
    for (plant, pollinator), amount in pooled.items():
        matrix[plant_index[plant]][pollinator_index[pollinator]] += amount
    baseline = WeightedNetwork.from_rows(plants, pollinators, matrix)
    pooled_shannon = shannon(pooled.values())

    pair_sets: list[set[tuple[str, str]]] = []
    context_shannons: list[float] = []
    contexts = []
    for context in locked:
        weights = context_pair_weights[context]
        pairs = {pair for pair, amount in weights.items() if amount > 0.0}
        pair_sets.append(pairs)
        context_shannons.append(shannon(weights.values()))
        contexts.append({
            "community": context[0],
            "visita": context[1],
            "source_sampled_plant_count_including_zero_interaction_rows": len(sampled_plants_by_context[context]),
            "positive_pair_count": len(pairs),
            "positive_interaction_weight": sum(weights.values()),
        })

    stats = context_stats(
        pair_sets,
        context_shannons,
        opportunity_pairs=opportunity_pairs,
        pooled_shannon=pooled_shannon,
        pooled_plants=set(plants),
        pooled_pollinators=set(pollinators),
    )
    return {
        "context_count": len(locked),
        "primary_method_label": rule["primary_method_label"],
        "primary_interaction_weight": rule["primary_interaction_weight"],
        "explicit_blank_pollinator_zero_rows_retained_as_sampling_absence": source_zero_rows,
        "pooled_opportunity": {
            "positive_pair_count": len(opportunity_pairs),
            "positive_plant_count": len(plants),
            "positive_pollinator_count": len(pollinators),
            "total_N_ind": sum(pooled.values()),
            "interaction_shannon": pooled_shannon,
        },
        "primary_estimands": {
            key: stats[key]
            for key in (
                "median_pair_support_fraction",
                "mean_pair_support_jaccard_turnover",
                "interaction_shannon_relative_context_range",
            )
        },
        "secondary": stats["secondary"],
        "contexts": contexts,
    }, baseline


def fast_v8_pair_mask(v8, v6, network: WeightedNetwork, *, support_seed: int, support_strength: float):
    active = v6.active_pollinator_indices(
        len(network.pollinator_names),
        rng=random.Random(support_seed),
        support_strength=support_strength,
    )
    active_set = set(active)
    pair_rng = random.Random(support_seed + v8.PAIR_SEED_OFFSET)
    keep_probability = 1.0 - support_strength
    mask = tuple(
        tuple(
            (column in active_set)
            and (value > 0.0)
            and (pair_rng.random() < keep_probability)
            for column, value in enumerate(row)
        )
        for row in network.matrix
    )
    return mask, tuple(active)


def verify_fast_mask_identity(v8, v6, baseline: WeightedNetwork) -> None:
    for strength in (0.25, 0.5, 0.75):
        for seed in (20260821, 20260822, 20260823):
            expected_mask, expected_active = v8.draw_hierarchical_pair_support_mask(
                baseline, support_seed=seed, support_strength=strength
            )
            actual_mask, actual_active = fast_v8_pair_mask(
                v8, v6, baseline, support_seed=seed, support_strength=strength
            )
            if expected_mask != actual_mask or expected_active != actual_active:
                raise RuntimeError("optimized Cabrera support draw diverged from frozen v8 implementation")


def predictive_summary(design: dict, baseline: WeightedNetwork) -> dict:
    v8 = load(V8_SCRIPT, "cabrera_v8_core")
    v6 = load(V6_SCRIPT, "cabrera_v8_v6_source")
    v5 = load(V5_SCRIPT, "cabrera_v8_v5_source")
    verify_fast_mask_identity(v8, v6, baseline)

    predictive = design["v8_predictive_distribution"]
    support_strengths = [float(value) for value in predictive["support_strengths"]]
    weight_strengths = [float(value) for value in predictive["weight_strengths"]]
    replicates = int(predictive["replicates_per_support_x_weight_setting"])
    contexts_per_draw = int(predictive["contexts_per_replicate"])

    opportunity_pairs = pair_set_from_network(baseline)
    pooled_plants = {plant for plant, _ in opportunity_pairs}
    pooled_pollinators = {pollinator for _, pollinator in opportunity_pairs}
    pooled_shannon = shannon(value for row in baseline.matrix for value in row)

    distributions = {
        "median_pair_support_fraction": [],
        "mean_pair_support_jaccard_turnover": [],
        "interaction_shannon_relative_context_range": [],
    }
    secondary_distributions: dict[str, list[float]] = {
        "active_plant_fraction_median": [],
        "active_plant_fraction_range": [],
        "active_pollinator_fraction_median": [],
        "active_pollinator_fraction_range": [],
        "empty_context_count": [],
    }
    setting_summary = {}
    structural_failures = []
    completed = 0

    for support_index, support_strength in enumerate(support_strengths):
        for weight_index, weight_strength in enumerate(weight_strengths):
            local = {key: [] for key in distributions}
            for replicate in range(replicates):
                pair_sets = []
                shannons = []
                for context_index in range(contexts_per_draw):
                    support_seed = SEED + support_index * 10_000_000 + replicate * 10_000 + context_index
                    weight_seed = SEED + 500_000_000 + weight_index * 10_000_000 + replicate * 10_000 + context_index
                    mask, globally_active = fast_v8_pair_mask(
                        v8,
                        v6,
                        baseline,
                        support_seed=support_seed,
                        support_strength=support_strength,
                    )
                    supported, audit = v8.apply_pair_support_mask(baseline, mask)
                    if audit.get("new_taxa_created") or audit.get("new_links_created") or audit.get("max_retained_row_budget_error", 0.0) > 1e-10:
                        structural_failures.append({
                            "support_strength": support_strength,
                            "weight_strength": weight_strength,
                            "replicate": replicate,
                            "context_index": context_index,
                            "audit": audit,
                        })
                        return {
                            "structural_gate_passed": False,
                            "decision": "v8_fails_cabrera_model_structural_gate",
                            "failure": structural_failures[0],
                            "predictive_draws_completed_before_failure": completed,
                        }
                    if supported is None:
                        realized = None
                    else:
                        realized = v5.realize_local_context(
                            supported,
                            context_seed=weight_seed,
                            context_strength=weight_strength,
                        )
                    pairs = pair_set_from_network(realized)
                    pair_sets.append(pairs)
                    shannons.append(
                        0.0 if realized is None else shannon(value for row in realized.matrix for value in row)
                    )

                stats = context_stats(
                    pair_sets,
                    shannons,
                    opportunity_pairs=opportunity_pairs,
                    pooled_shannon=pooled_shannon,
                    pooled_plants=pooled_plants,
                    pooled_pollinators=pooled_pollinators,
                )
                for key in distributions:
                    value = float(stats[key])
                    distributions[key].append(value)
                    local[key].append(value)
                secondary = stats["secondary"]
                for key in secondary_distributions:
                    secondary_distributions[key].append(float(secondary[key]))
                completed += 1

            setting_summary[f"support={support_strength}|weight={weight_strength}"] = {
                key: {
                    "median": percentile(values, 0.5),
                    "p2.5": percentile(values, 0.025),
                    "p97.5": percentile(values, 0.975),
                }
                for key, values in local.items()
            }

    expected = int(predictive["predictive_draw_count"])
    if completed != expected:
        raise RuntimeError(f"predictive draw count drifted: {completed} != {expected}")
    return {
        "structural_gate_passed": True,
        "predictive_draw_count": completed,
        "contexts_per_draw": contexts_per_draw,
        "equal_support_and_weight_strength_weights": True,
        "primary_envelopes": {key: envelope(values) for key, values in distributions.items()},
        "secondary_envelopes": {key: envelope(values) for key, values in secondary_distributions.items()},
        "setting_summary": setting_summary,
        "fast_mask_identity_with_frozen_v8_verified": True,
    }


def write(payload: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    design = json.loads(DESIGN.read_text())
    if design["chronology"]["cabrera_target_metrics_calculated_before_freeze"] is not False:
        raise RuntimeError("Cabrera target chronology is not prospectively frozen")
    empirical, baseline = empirical_summary(design)
    predictive = predictive_summary(design, baseline)

    payload = {
        "schema_version": "1.0",
        "analysis": "abm_v8_cabrera_conditional_repeated_local_validation",
        "status": "held_out_conditional_pair_support_validation",
        "design_source": str(DESIGN),
        "target_metrics_inspected": True,
        "empirical": empirical,
        "predictive": predictive,
        "claim_boundary": design["claim_boundary"],
    }

    if not predictive.get("structural_gate_passed"):
        payload["tests"] = {
            "model_structural_gate": False,
            "median_pair_support_fraction_adequacy": None,
            "mean_pair_support_jaccard_turnover_adequacy": None,
            "interaction_shannon_relative_context_range_adequacy": None,
        }
        payload["decision"] = predictive["decision"]
        write(payload)
        return

    tests = {"model_structural_gate": True}
    for key, empirical_value in empirical["primary_estimands"].items():
        tests[f"{key}_adequacy"] = inside(float(empirical_value), predictive["primary_envelopes"][key])
    payload["tests"] = tests
    payload["decision"] = (
        "v8_survives_cabrera_conditional_pair_support_test"
        if all(value is True for value in tests.values())
        else "v8_fails_cabrera_conditional_pair_support_predictive_adequacy"
    )
    write(payload)


if __name__ == "__main__":
    main()
