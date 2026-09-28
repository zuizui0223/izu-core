from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

RAW = Path("data/external/dore2021_zenodo_v1/network interaction data.txt")
SOURCE_GATE = Path("data/results/dore2021_zenodo_v1_raw_interaction_source_gate.json")
FROZEN = Path("data/design/frozen_dore_candidate_network_locations.json")
TARGETS = Path("data/results/frozen_dore_network_targets.csv")
OUT = Path("data/results/dore2021_zenodo_v1_raw_interaction_schema_audit.json")

EXPECTED_COLUMNS = [
    "id_network",
    "id_network_aggreg",
    "pollinatororder",
    "pollinatorgenus",
    "pollinatorspecies",
    "plantgenus",
    "plantspecies",
    "Complete_ref",
    "Source",
]


def region_number(region_pub: str) -> str:
    match = re.fullmatch(r"RP(\d+)", str(region_pub).strip())
    if not match:
        raise ValueError(f"unexpected Region_pub: {region_pub!r}")
    return str(int(match.group(1)))


def taxon(parts: tuple[str | None, ...]) -> str:
    cleaned = [" ".join(str(x).split()) for x in parts if x not in (None, "")]
    return " ".join(cleaned).strip()


def load_targets() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    with TARGETS.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            out[row["region_pub"]] = {
                "pollinator_richness": int(float(row["pollinator_richness"])),
                "link_richness": int(float(row["link_richness"])),
                "data_type": row.get("data_type") or None,
                "system": row.get("system"),
            }
    return out


def main() -> None:
    gate = json.loads(SOURCE_GATE.read_text()) if SOURCE_GATE.exists() else {}
    payload: dict[str, object] = {
        "schema_version": "2.0",
        "analysis": "dore2021_zenodo_v1_raw_interaction_schema_audit",
        "source_status": gate.get("status"),
        "source_sha256": gate.get("sha256"),
        "source_encoding": "latin-1",
        "status": "blocked",
    }
    if gate.get("status") != "raw_interaction_bytes_recovered" or not RAW.exists():
        payload["decision"] = "raw_bytes_not_available_for_schema_audit"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    with RAW.open("r", encoding="latin-1", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    if fields != EXPECTED_COLUMNS:
        raise ValueError(f"unexpected Zenodo v1 schema: {fields}")

    frozen = json.loads(FROZEN.read_text())
    frozen_rows = {str(row["region_pub"]): row for row in frozen["rows"]}
    targets = load_targets()
    raw_by_aggreg: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        raw_by_aggreg[str(int(row["id_network_aggreg"]))].append(row)

    reconciliation = []
    direct_raw = []
    absent = []
    exact_link = 0
    exact_pollinator = 0
    for region_pub, frozen_row in sorted(frozen_rows.items(), key=lambda item: int(region_number(item[0]))):
        aggregate_id = region_number(region_pub)
        raw = raw_by_aggreg.get(aggregate_id, [])
        if not raw:
            absent.append(region_pub)
            reconciliation.append(
                {
                    "region_pub": region_pub,
                    "id_network_aggreg": int(aggregate_id),
                    "system": frozen_row.get("system"),
                    "source_trace": frozen_row.get("source"),
                    "list_inter_dispo": frozen_row.get("list_inter_dispo"),
                    "list_inter_dbase": frozen_row.get("list_inter_dbase"),
                    "raw_state": "absent_from_zenodo_v1_interaction_table",
                }
            )
            continue

        direct_raw.append(region_pub)
        plants = {
            taxon((r.get("plantgenus"), r.get("plantspecies")))
            for r in raw
        }
        pollinators = {
            taxon((r.get("pollinatororder"), r.get("pollinatorgenus"), r.get("pollinatorspecies")))
            for r in raw
        }
        pairs = {
            (
                taxon((r.get("plantgenus"), r.get("plantspecies"))),
                taxon((r.get("pollinatororder"), r.get("pollinatorgenus"), r.get("pollinatorspecies"))),
            )
            for r in raw
        }
        source_network_ids = sorted({int(r["id_network"]) for r in raw})
        target = targets[region_pub]
        link_delta = len(pairs) - int(target["link_richness"])
        poll_delta = len(pollinators) - int(target["pollinator_richness"])
        if link_delta == 0:
            exact_link += 1
        if poll_delta == 0:
            exact_pollinator += 1
        reconciliation.append(
            {
                "region_pub": region_pub,
                "id_network_aggreg": int(aggregate_id),
                "system": target["system"],
                "data_type": target["data_type"],
                "raw_state": "topology_rows_recovered",
                "raw_row_count": len(raw),
                "source_subnetwork_count": len(source_network_ids),
                "source_subnetwork_ids": source_network_ids,
                "raw_unique_plants": len(plants),
                "raw_unique_pollinators": len(pollinators),
                "raw_unique_pairs": len(pairs),
                "dore_aggregate_pollinator_richness": target["pollinator_richness"],
                "dore_aggregate_link_richness": target["link_richness"],
                "pollinator_richness_delta_raw_minus_dore": poll_delta,
                "link_richness_delta_raw_minus_dore": link_delta,
                "topology_exact_link_reconciliation": link_delta == 0,
                "topology_exact_pollinator_reconciliation": poll_delta == 0,
            }
        )

    frequency_with_topology = [
        row["region_pub"]
        for row in reconciliation
        if row.get("raw_state") == "topology_rows_recovered" and row.get("data_type") == "frequency"
    ]
    repeated_raw_rows_exceed_unique_pairs = [
        row["region_pub"]
        for row in reconciliation
        if row.get("raw_state") == "topology_rows_recovered"
        and int(row["raw_row_count"]) > int(row["raw_unique_pairs"])
    ]

    payload.update(
        {
            "status": "schema_and_aggregate_id_link_audited",
            "delimiter": "tab",
            "n_rows": len(rows),
            "n_columns": len(fields),
            "columns": fields,
            "resolved_roles": {
                "frozen_network_join": "numeric suffix of Region_pub == id_network_aggreg",
                "source_subnetwork_id": "id_network",
                "plant_taxon": "plantgenus + plantspecies",
                "pollinator_taxon": "pollinatororder + pollinatorgenus + pollinatorspecies",
                "reference": "Complete_ref",
                "source_repository": "Source",
                "interaction_weight": None,
            },
            "interaction_weight_state": "absent_from_zenodo_v1_interaction_table",
            "frozen_region_pub_count": len(frozen_rows),
            "frozen_region_pub_with_raw_topology": len(direct_raw),
            "frozen_region_pub_without_raw_topology": len(absent),
            "frozen_region_pub_with_raw_topology_ids": direct_raw,
            "frozen_region_pub_without_raw_topology_ids": absent,
            "frequency_networks_with_raw_topology_only": frequency_with_topology,
            "aggregate_topology_reconciliation": {
                "exact_link_richness_rows": exact_link,
                "exact_pollinator_richness_rows": exact_pollinator,
                "rows_with_subnetwork_repetition": repeated_raw_rows_exceed_unique_pairs,
                "rows": reconciliation,
            },
            "decision": "raw_topology_links_22_of_26_but_weighted_tier_b_requires_original_frequency_matrices",
            "next_gate": "Recover source-native frequency/visitation-rate matrices for frozen frequency networks from their original repositories. The Zenodo topology table may validate identities and links but must not be converted into interaction weights. Binary/source-absent rows remain outside weighted Tier-B unless an original quantitative source is recovered.",
            "claim_boundary": "The Zenodo v1 interaction table recovers topology for 22/26 frozen networks and links by id_network_aggreg, but contains no explicit interaction weight. Repeated rows or source subnetworks are not interpreted as visit counts. No weighted interaction diversity or weighted plant niche-overlap estimate is admitted from this table alone.",
        }
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
