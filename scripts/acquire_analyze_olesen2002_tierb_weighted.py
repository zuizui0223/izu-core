from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/design/olesen2002_tierb_weighted_source_map.json"
OUT = ROOT / "data/results/olesen2002_tierb_weighted_anchor.json"
RAW_DIR = ROOT / "data/external/olesen2002_iwdb"


def get_bytes(url: str, timeout: int = 90) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "text/plain,*/*"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_flat_integers(data: bytes) -> list[int]:
    text = data.decode("ascii", errors="strict")
    values = [int(token) for token in text.split()]
    if not values or any(value < 0 for value in values):
        raise ValueError("IWDB matrix must contain non-negative integer frequencies")
    return values


def make_network(flat: list[int], pollinator_rows: int, plant_columns: int) -> WeightedNetwork:
    if len(flat) != pollinator_rows * plant_columns:
        raise ValueError(
            f"cell count {len(flat)} != {pollinator_rows} x {plant_columns}"
        )
    source_rows = [
        flat[index * plant_columns : (index + 1) * plant_columns]
        for index in range(pollinator_rows)
    ]
    # IWDB text source is pollinator rows x plant columns. WeightedNetwork uses plants x pollinators.
    plant_rows = [
        [source_rows[pollinator][plant] for pollinator in range(pollinator_rows)]
        for plant in range(plant_columns)
    ]
    return WeightedNetwork.from_rows(
        [f"plant_{index + 1}" for index in range(plant_columns)],
        [f"pollinator_{index + 1}" for index in range(pollinator_rows)],
        plant_rows,
    )


def main() -> None:
    config = json.loads(CONFIG.read_text())
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for entry in config["networks"]:
        state = {k: entry[k] for k in entry}
        try:
            data = get_bytes(entry["url"])
            raw_path = RAW_DIR / f"{entry['region_pub']}.txt"
            raw_path.write_bytes(data)
            flat = parse_flat_integers(data)
            network = make_network(
                flat,
                int(entry["source_pollinator_rows"]),
                int(entry["source_plant_columns"]),
            )
            metrics = network_metrics(network)
            source_topology_ok = (
                metrics["n_pollinators"] == int(entry["source_pollinator_rows"])
                and metrics["n_plants"] == int(entry["source_plant_columns"])
                and metrics["n_positive_links"] == int(entry["source_topology_positive_links"])
            )
            dore_exact = (
                metrics["n_pollinators"] == int(entry["dore_frozen_pollinator_richness"])
                and metrics["n_positive_links"] == int(entry["dore_frozen_link_richness"])
                and abs(float(metrics["total_visitation_rate"]) - float(entry["dore_frozen_full_visits"])) < 1e-9
            )
            state.update(
                {
                    "status": "weighted_source_recovered_and_analyzed",
                    "source_bytes": len(data),
                    "source_sha256": sha256(data),
                    "source_cell_count": len(flat),
                    "source_frequency_sum": sum(flat),
                    "source_positive_cell_count": sum(value > 0 for value in flat),
                    "source_topology_reconciles": source_topology_ok,
                    "dore_frozen_counts_and_visits_reconcile_exactly": dore_exact,
                    "metrics": metrics,
                    "tier_b_role": (
                        "exact_frozen_weighted_anchor"
                        if dore_exact
                        else "source_native_weighted_method_validation_only"
                    ),
                }
            )
        except Exception as exc:
            state.update(
                {
                    "status": "weighted_source_recovery_or_analysis_failed",
                    "error": repr(exc),
                    "tier_b_role": "blocked",
                }
            )
        results.append(state)

    exact = [x["region_pub"] for x in results if x.get("tier_b_role") == "exact_frozen_weighted_anchor"]
    payload = {
        "schema_version": "1.0",
        "analysis": "olesen2002_iwdb_weighted_tier_b_source_validation",
        "source_page": config["source_page"],
        "source_data_statement": config["source_data_statement"],
        "metric_implementation": "channel_id.external_archipelago_network.network_metrics",
        "metrics_admitted_as_source_compatible_analogues": [
            "interaction_shannon",
            "mean_plant_niche_overlap_morisita_horn"
        ],
        "networks": results,
        "exact_frozen_weighted_anchor_ids": exact,
        "decision": (
            "at_least_one_exact_weighted_tier_b_anchor_recovered"
            if exact
            else "no_exact_weighted_tier_b_anchor_recovered"
        ),
        "next_gate": "Use exact anchors to validate the weighted metric pipeline, then recover additional frozen quantitative matrices from Canary, Seychelles/Mauritius and other source repositories. Do not run a global Tier-B LOSO until enough independent systems have exact/source-compatible weighted matrices.",
        "claim_boundary": config["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
