from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

BASE = "https://mangal.io/api/v2"
OUT = Path("data/results/chapter2_mangal_repeated_network_candidate_screen_20260914.json")
USER_AGENT = "izu-core-source-audit/1.0"


def get_json(url: str, timeout: int = 90):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_all(endpoint: str, *, count: int = 1000) -> list[dict]:
    rows: list[dict] = []
    page = 0
    while True:
        query = urllib.parse.urlencode({"count": count, "page": page, "sort": "id"})
        payload = get_json(f"{BASE}/{endpoint}?{query}")
        if not isinstance(payload, list):
            raise RuntimeError(f"unexpected {endpoint} response: {type(payload)}")
        part = [row for row in payload if isinstance(row, dict)]
        rows.extend(part)
        if len(part) < count:
            break
        page += 1
        if page > 20:
            raise RuntimeError(f"pagination guard exceeded for {endpoint}")
    return rows


def query_rows(endpoint: str, **params) -> list[dict]:
    params = {**params, "count": 1000, "page": 0, "sort": "id"}
    payload = get_json(f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}")
    if not isinstance(payload, list):
        return []
    return [row for row in payload if isinstance(row, dict)]


def date_key(value: object) -> str:
    text = str(value or "").strip()
    return text[:10] if text else ""


def geom_key(value: object) -> str:
    if not isinstance(value, dict):
        return ""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def stable_geom_groups(nets: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for net in nets:
        key = geom_key(net.get("geom"))
        if key:
            groups[key].append(net)
    output = []
    for key, members in groups.items():
        dates = sorted({date_key(net.get("date")) for net in members if date_key(net.get("date"))})
        if len(dates) < 6:
            continue
        ordered = sorted(members, key=lambda row: (date_key(row.get("date")), int(row.get("id") or 0)))
        output.append({
            "geom": ordered[0].get("geom"),
            "network_count": len(members),
            "distinct_dates": len(dates),
            "date_min": dates[0],
            "date_max": dates[-1],
            "network_ids": [row.get("id") for row in ordered],
            "names_preview": [row.get("name") for row in ordered[:12]],
            "descriptions_preview": sorted({str(row.get("description") or "") for row in ordered})[:12],
        })
    return sorted(output, key=lambda row: (-int(row["distinct_dates"]), -int(row["network_count"]), json.dumps(row["geom"], sort_keys=True)))


def main() -> None:
    datasets = fetch_all("dataset")
    networks = fetch_all("network")
    references = fetch_all("reference")
    refs = {row.get("id"): row for row in references}
    by_dataset: dict[int, list[dict]] = defaultdict(list)
    for network in networks:
        try:
            dataset_id = int(network.get("dataset_id"))
        except (TypeError, ValueError):
            continue
        by_dataset[dataset_id].append(network)

    candidates = []
    for dataset in datasets:
        try:
            dataset_id = int(dataset.get("id"))
        except (TypeError, ValueError):
            continue
        nets = by_dataset.get(dataset_id, [])
        if len(nets) < 6:
            continue
        distinct_dates = sorted({date_key(net.get("date")) for net in nets if date_key(net.get("date"))})
        if len(distinct_dates) < 6:
            continue

        probes = []
        quantitative_probe = False
        presence_only_probe = True
        attribute_names = set()
        for network in sorted(nets, key=lambda row: int(row.get("id") or 0))[:3]:
            interactions = query_rows("interaction", network_id=network.get("id"))
            names = sorted({
                str((row.get("attribute") or {}).get("name") or "").strip()
                for row in interactions
                if isinstance(row.get("attribute"), dict)
            } - {""})
            attribute_names.update(names)
            values = [row.get("value") for row in interactions if row.get("value") is not None]
            numeric_values = []
            for value in values:
                try:
                    numeric_values.append(float(value))
                except (TypeError, ValueError):
                    pass
            is_presence = bool(names) and all(
                any(token in name.casefold() for token in ("presence", "binary", "absence"))
                for name in names
            )
            has_nonbinary_value = any(value not in {0.0, 1.0} for value in numeric_values)
            if numeric_values and (has_nonbinary_value or not is_presence):
                quantitative_probe = True
            if not is_presence:
                presence_only_probe = False
            probes.append({
                "network_id": network.get("id"),
                "date": date_key(network.get("date")),
                "interaction_rows": len(interactions),
                "attribute_names": names,
                "numeric_values_present": bool(numeric_values),
                "has_nonbinary_value": has_nonbinary_value,
            })

        ref = refs.get(dataset.get("ref_id"), {})
        candidates.append({
            "dataset_id": dataset_id,
            "dataset_name": dataset.get("name"),
            "dataset_date": date_key(dataset.get("date")),
            "dataset_description": dataset.get("description"),
            "network_count": len(nets),
            "distinct_network_dates": len(distinct_dates),
            "date_min": distinct_dates[0] if distinct_dates else None,
            "date_max": distinct_dates[-1] if distinct_dates else None,
            "stable_geom_groups_with_ge6_dates": stable_geom_groups(nets),
            "network_locations_preview": [
                {"id": net.get("id"), "name": net.get("name"), "date": date_key(net.get("date")), "geom": net.get("geom"), "description": net.get("description")}
                for net in sorted(nets, key=lambda row: int(row.get("id") or 0))[:12]
            ],
            "reference": {
                "doi": ref.get("doi"),
                "first_author": ref.get("first_author") or ref.get("author"),
                "year": ref.get("year"),
                "paper_url": ref.get("paper_url"),
                "data_url": ref.get("data_url"),
                "bibtex": ref.get("bibtex"),
            },
            "interaction_probe": probes,
            "attribute_names_probe": sorted(attribute_names),
            "quantitative_probe_pass": quantitative_probe,
            "presence_only_probe": presence_only_probe,
            "island_status": "unreviewed_after_result_blind_repetition_screen",
        })

    result = {
        "schema_version": "1.1",
        "analysis": "chapter2_mangal_repeated_network_candidate_screen",
        "status": "result_blind_source_structure_screen_coordinates_not_opened",
        "database_counts": {
            "datasets": len(datasets),
            "networks": len(networks),
            "references": len(references),
        },
        "screen_rule": {
            "minimum_networks_per_dataset": 6,
            "minimum_distinct_network_dates": 6,
            "stable_unit_second_pass": "exact source-native network geometry; retain groups with >=6 distinct dates without island filtering",
            "interaction_probe": "first three network IDs only; inspect attribute semantics and whether quantitative nonbinary values exist",
            "island_filter_applied": False,
            "coordinates_or_ecological_metrics_calculated": False,
        },
        "candidate_count": len(candidates),
        "quantitative_candidate_count": sum(bool(row["quantitative_probe_pass"]) for row in candidates),
        "candidates": candidates,
        "claim_boundary": "This screen precedes island-status review and uses no D1, phi, determinant, response, diversity or journal-route values. Dataset inclusion is based only on repeated dated networks and interaction measurement semantics; stable-unit grouping uses exact source geometry only."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "datasets": len(datasets),
        "networks": len(networks),
        "candidate_count": len(candidates),
        "quantitative_candidate_count": result["quantitative_candidate_count"],
        "candidate_names": [row["dataset_name"] for row in candidates],
        "stable_geom_group_counts": {row["dataset_name"]: len(row["stable_geom_groups_with_ge6_dates"]) for row in candidates},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
