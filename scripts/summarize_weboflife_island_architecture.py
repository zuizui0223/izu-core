from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

RAW = Path("data/external/weboflife_mauritius_seychelles")
GATE = Path("data/results/weboflife_mauritius_seychelles_matrix_gate.json")
OUT = Path("data/results/weboflife_mauritius_seychelles_architecture_summary.json")


def load_edges(path: Path, network_id: str):
    parsed = json.loads(path.read_text(encoding="utf-8"))
    rows = parsed.get("data") or parsed.get("rows") or [] if isinstance(parsed, dict) else parsed
    out = []
    for row in rows:
        if str(row.get("network_name")) != network_id:
            continue
        w = float(row.get("connection_strength") or 0)
        if w <= 0:
            continue
        out.append((str(row.get("species1") or ""), str(row.get("species2") or ""), w))
    return out


def mean_pairwise_jaccard(plant_partners):
    plants = sorted(plant_partners)
    vals = []
    for i in range(len(plants)):
        a = plant_partners[plants[i]]
        for j in range(i + 1, len(plants)):
            b = plant_partners[plants[j]]
            union = a | b
            vals.append(len(a & b) / len(union) if union else 1.0)
    return statistics.mean(vals) if vals else None


def mean_pairwise_weighted_overlap(plant_weights):
    plants = sorted(plant_weights)
    profiles = {}
    for plant in plants:
        total = sum(plant_weights[plant].values())
        profiles[plant] = {k: v / total for k, v in plant_weights[plant].items()} if total > 0 else {}
    vals = []
    for i in range(len(plants)):
        a = profiles[plants[i]]
        for j in range(i + 1, len(plants)):
            b = profiles[plants[j]]
            keys = set(a) | set(b)
            vals.append(sum(min(a.get(k, 0.0), b.get(k, 0.0)) for k in keys))
    return statistics.mean(vals) if vals else None


def network_metrics(edges):
    pollinators = {a for a, _, _ in edges}
    plants = {b for _, b, _ in edges}
    total = sum(w for _, _, w in edges)
    probs = [w / total for _, _, w in edges]
    shannon = -sum(p * math.log(p) for p in probs if p > 0)
    plant_partners = {p: set() for p in plants}
    plant_weights = {p: {} for p in plants}
    for poll, plant, w in edges:
        plant_partners[plant].add(poll)
        plant_weights[plant][poll] = plant_weights[plant].get(poll, 0.0) + w
    return {
        "pollinator_richness": len(pollinators),
        "plant_richness": len(plants),
        "link_richness": len(edges),
        "total_connection_strength": total,
        "interaction_shannon": shannon,
        "interaction_shannon_effective_number": math.exp(shannon),
        "plant_partner_jaccard_overlap": mean_pairwise_jaccard(plant_partners),
        "plant_weighted_profile_overlap": mean_pairwise_weighted_overlap(plant_weights),
    }


def summarize(values):
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    return {
        "n_networks": len(vals),
        "mean": statistics.mean(vals),
        "median": statistics.median(vals),
        "min": min(vals),
        "max": max(vals),
        "sd": statistics.stdev(vals) if len(vals) > 1 else 0.0,
    }


def main() -> None:
    gate = json.loads(GATE.read_text())
    if not gate["admission"]["all_requested_bytes_recovered"]:
        raise RuntimeError("matrix gate is not complete; architecture summary cannot run")
    systems = {}
    for system, source in gate["systems"].items():
        networks = []
        for entry in source["entries"]:
            network_id = entry["network_id"]
            edges = load_edges(Path(entry["path"]), network_id)
            if not edges:
                raise RuntimeError(f"no positive edges parsed for {network_id}")
            networks.append({"network_id": network_id, **network_metrics(edges)})
        metric_names = [k for k in networks[0] if k != "network_id"]
        systems[system] = {
            "independent_system_count": 1,
            "within_system_network_replicates": len(networks),
            "network_metrics": networks,
            "aggregate": {k: summarize([x[k] for x in networks]) for k in metric_names},
        }
    payload = {
        "analysis": "weboflife_mauritius_seychelles_within_system_architecture",
        "systems": systems,
        "metric_definitions": {
            "interaction_shannon": "Shannon entropy of normalized positive edge weights within each source-native network.",
            "interaction_shannon_effective_number": "exp(Shannon), an effective-number representation of weighted interaction diversity.",
            "plant_partner_jaccard_overlap": "Mean pairwise Jaccard overlap among plants' pollinator-partner sets; this matches the qualitative form of the current ABM plant-overlap proxy but is not silently equated to Traveset et al. niche-overlap estimands.",
            "plant_weighted_profile_overlap": "Mean pairwise sum of minima between plant-normalized pollinator-use profiles (0–1 proportional overlap)."
        },
        "independence_boundary": "The 24 Mauritius and 48 Seychelles networks are within-system repeated subnetworks/time slices. They estimate within-system variability but contribute two independent island-system clusters, not 72 independent systems.",
        "biological_boundary": "Web of Life connection strength is interaction/visitation weight. It is not single-visit pollen deposition, pollinator effectiveness or reproductive success.",
        "next_gate": "Use source-locked island geography and the frozen v4 saturation envelope to test whether matrix-level interaction diversity and plant-overlap organization are predicted better by the mechanistic ABM than by geography-only baselines, retaining system-level clustering.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
