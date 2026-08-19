from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from channel_id.external_archipelago_network import WeightedNetwork, network_metrics

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/design/canary_trojelsgaard2015_weighted_source_map.json"
GATE = ROOT / "data/results/canary_trojelsgaard2015_weighted_source_gate.json"
RAW_DIR = ROOT / "data/external/canary_trojelsgaard2015"
OUT = ROOT / "data/results/canary_trojelsgaard2015_weighted_tierb.json"


def number(value: str, *, cell: str) -> float:
    text = str(value or "").strip()
    if text == "":
        return 0.0
    try:
        out = float(text)
    except ValueError as exc:
        raise ValueError(f"nonnumeric matrix cell {cell}: {value!r}") from exc
    if out < 0:
        raise ValueError(f"negative matrix cell {cell}: {out}")
    return out


def read_site(path: Path) -> dict[tuple[str, str], float]:
    text = path.read_text(encoding="utf-8-sig", errors="strict")
    sample = text[:10000]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(text.splitlines(), dialect=dialect))
    if not rows:
        raise ValueError(f"empty CSV: {path}")

    # Expected Dryad layout: header row contains plant taxa from column 2 onward;
    # rows thereafter contain pollinator taxon in column 1 and visit counts.
    header_index = None
    for i, row in enumerate(rows[:20]):
        if len(row) < 3:
            continue
        nonempty_after_first = [str(x).strip() for x in row[1:] if str(x).strip()]
        if len(nonempty_after_first) >= 2:
            # Header taxa should not all be numeric.
            numeric = 0
            for x in nonempty_after_first:
                try:
                    float(x)
                    numeric += 1
                except ValueError:
                    pass
            if numeric < len(nonempty_after_first) / 2:
                header_index = i
                break
    if header_index is None:
        raise ValueError(f"cannot identify header in {path.name}")

    header = rows[header_index]
    plant_cols = [(j, " ".join(str(v).split())) for j, v in enumerate(header[1:], start=1) if str(v).strip()]
    if not plant_cols:
        raise ValueError(f"no plant columns in {path.name}")

    edges: dict[tuple[str, str], float] = defaultdict(float)
    used_rows = 0
    for row_no, row in enumerate(rows[header_index + 1 :], start=header_index + 2):
        if not row or not str(row[0]).strip():
            continue
        pollinator = " ".join(str(row[0]).split())
        values = []
        parse_failed = False
        for j, plant in plant_cols:
            raw = row[j] if j < len(row) else ""
            try:
                values.append((plant, number(raw, cell=f"{path.name}:R{row_no}C{j+1}")))
            except ValueError:
                parse_failed = True
                break
        if parse_failed:
            # Permit footer/metadata rows only if none of the matrix fields can be parsed as numeric.
            numeric_like = 0
            for j, _ in plant_cols:
                if j >= len(row) or str(row[j]).strip() == "":
                    continue
                try:
                    float(str(row[j]).strip())
                    numeric_like += 1
                except ValueError:
                    pass
            if numeric_like == 0:
                continue
            raise ValueError(f"mixed numeric/non-numeric data row in {path.name} row {row_no}")
        used_rows += 1
        for plant, weight in values:
            if weight > 0:
                edges[(plant, pollinator)] += weight
    if not edges or used_rows == 0:
        raise ValueError(f"no positive interaction edges recovered from {path.name}")
    return dict(edges)


def network_from_edges(edges: dict[tuple[str, str], float]) -> WeightedNetwork:
    plants = sorted({plant for plant, _ in edges})
    pollinators = sorted({pollinator for _, pollinator in edges})
    matrix = [
        [float(edges.get((plant, pollinator), 0.0)) for pollinator in pollinators]
        for plant in plants
    ]
    return WeightedNetwork.from_rows(plants, pollinators, matrix)


def main() -> None:
    config = json.loads(CONFIG.read_text())
    gate = json.loads(GATE.read_text()) if GATE.exists() else {}
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "analysis": "canary_trojelsgaard2015_preregistered_weighted_tierb",
        "source_doi": config["source_doi"],
        "source_semantics": config["source_semantics"],
        "aggregation_rule": config["aggregation_rule"],
        "source_gate_status": gate.get("status"),
        "rows": [],
    }
    recovered = set((gate.get("recovered") or {}).keys())
    for spec in config["frozen_island_aggregation"]:
        files = list(spec["site_files"])
        missing = [name for name in files if name not in recovered or not (RAW_DIR / name).exists()]
        row = {
            "region_pub": spec["region_pub"],
            "island": spec["island"],
            "site_files": files,
            "missing_site_files": missing,
            "dore_pollinator_richness": spec["dore_pollinator_richness"],
            "dore_link_richness": spec["dore_link_richness"],
        }
        if missing:
            row.update({"status": "blocked_missing_preregistered_site_files", "tier_b_role": "blocked"})
            payload["rows"].append(row)
            continue
        try:
            aggregate: dict[tuple[str, str], float] = defaultdict(float)
            site_summaries = []
            for name in files:
                edges = read_site(RAW_DIR / name)
                site_network = network_from_edges(edges)
                site_summaries.append({"file": name, **network_metrics(site_network)})
                for pair, value in edges.items():
                    aggregate[pair] += value
            network = network_from_edges(dict(aggregate))
            metrics = network_metrics(network)
            topology_exact = (
                metrics["n_pollinators"] == int(spec["dore_pollinator_richness"])
                and metrics["n_positive_links"] == int(spec["dore_link_richness"])
            )
            row.update(
                {
                    "status": "weighted_island_aggregation_analyzed",
                    "site_metrics": site_summaries,
                    "metrics": metrics,
                    "topology_reconciles_to_frozen_dore_row": topology_exact,
                    "tier_b_role": "exact_topology_weighted_anchor" if topology_exact else "source_native_weighted_requires_filter_reconciliation",
                }
            )
        except Exception as exc:
            row.update({"status": "analysis_failed", "error": repr(exc), "tier_b_role": "blocked"})
        payload["rows"].append(row)

    exact = [row["region_pub"] for row in payload["rows"] if row.get("tier_b_role") == "exact_topology_weighted_anchor"]
    payload.update(
        {
            "exact_topology_weighted_anchor_ids": exact,
            "n_exact_topology_weighted_anchors": len(exact),
            "decision": "canary_weighted_anchors_recovered" if exact else "no_canary_weighted_anchor_yet",
            "next_gate": "Only exact or transparently filter-reconciled frozen rows may join Tier-B cross-system validation. Do not alter the preregistered site grouping based on metric fit.",
            "claim_boundary": config["claim_boundary"],
        }
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
