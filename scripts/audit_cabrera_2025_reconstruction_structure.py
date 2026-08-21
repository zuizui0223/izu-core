from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/cabrera_2025_reconstruction_structure.json"
CSV_URL = "https://digital.csic.es/bitstream/10261/420466/1/cabrera_22_23_habitat.csv"
CSV_SHA256 = "399ec11ae6ce18c8e9ebb050857ca7c1da4cb4a7858e24382750a92ae5e16a07"
USER_AGENT = "izu-core-structural-audit/1.0"
EXPECTED_HEADERS = [
    "visita", "censo", "COMMUNITY", "habitat", "Start_T", "End_T",
    "Delta_T_minutes", "Plant sp", "N open flowers", "N observed flowers",
    "Pollinator", "Family", "Functional group", "N ind", "N visit flowers",
    "Method", "Island",
]


def fetch() -> bytes:
    req = urllib.request.Request(CSV_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as response:
        payload = response.read()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != CSV_SHA256:
        raise RuntimeError(f"Cabrera CSV checksum drift: {actual}")
    return payload


def decode(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError("Cabrera CSV cannot be decoded")


def parse_float(value: str) -> float | None:
    text = str(value or "").strip().replace(",", ".")
    if not text or text.lower() in {"na", "nan", "null", "none", "-"}:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def normalize_label(value: str) -> str:
    return " ".join(str(value or "").split()).casefold()


def label_collision_audit(values: list[str]) -> dict:
    variants: dict[str, set[str]] = defaultdict(set)
    for raw in values:
        text = " ".join(str(raw or "").split())
        if text:
            variants[normalize_label(text)].add(text)
    collisions = {key: sorted(raws) for key, raws in variants.items() if len(raws) > 1}
    return {
        "nonblank_raw_label_count": len({" ".join(str(v).split()) for v in values if str(v).strip()}),
        "canonical_label_count": len(variants),
        "variant_collision_count": len(collisions),
        "variant_collisions": collisions,
    }


def numeric_presence(rows: list[dict[str, str]], field: str) -> dict:
    parsed = [parse_float(row.get(field, "")) for row in rows]
    return {
        "row_count": len(rows),
        "numeric_count": sum(value is not None for value in parsed),
        "missing_or_nonnumeric_count": sum(value is None for value in parsed),
        "zero_count": sum(value == 0 for value in parsed if value is not None),
        "positive_count": sum(value > 0 for value in parsed if value is not None),
        "negative_count": sum(value < 0 for value in parsed if value is not None),
    }


def cardinality(rows: list[dict[str, str]], field: str) -> int:
    return len({row.get(field, "").strip() for row in rows if row.get(field, "").strip()})


def context_key(row: dict[str, str], fields: tuple[str, ...]) -> tuple[str, ...] | None:
    values = tuple(row.get(field, "").strip() for field in fields)
    return values if all(values) else None


def context_count(rows: list[dict[str, str]], fields: tuple[str, ...]) -> int:
    return len({key for row in rows if (key := context_key(row, fields)) is not None})


def sorted_context_keys(rows: list[dict[str, str]], fields: tuple[str, ...]) -> list[list[str]]:
    keys = {key for row in rows if (key := context_key(row, fields)) is not None}
    def sort_key(key: tuple[str, ...]):
        converted = []
        for value in key:
            converted.append((0, int(value)) if value.isdigit() else (1, value))
        return tuple(converted)
    return [list(key) for key in sorted(keys, key=sort_key)]


def main() -> None:
    payload = fetch()
    reader = csv.DictReader(io.StringIO(decode(payload)), delimiter=";")
    headers = reader.fieldnames or []
    if headers != EXPECTED_HEADERS:
        raise RuntimeError(f"Cabrera headers drifted: {headers}")
    rows = [dict(row) for row in reader]
    if len(rows) != 3874:
        raise RuntimeError(f"Cabrera source row count drifted: {len(rows)}")

    methods = sorted({row["Method"].strip() for row in rows if row["Method"].strip()})
    comunidades = sorted({row["COMMUNITY"].strip() for row in rows if row["COMMUNITY"].strip()})
    visitas = sorted({row["visita"].strip() for row in rows if row["visita"].strip()}, key=lambda x: int(x) if x.isdigit() else x)
    habitats = sorted({row["habitat"].strip() for row in rows if row["habitat"].strip()})
    islands = sorted({row["Island"].strip() for row in rows if row["Island"].strip()})

    method_rows: dict[str, dict] = {}
    for method in methods:
        subset = [row for row in rows if row["Method"].strip() == method]
        community_visit = {
            key for row in subset
            if (key := context_key(row, ("COMMUNITY", "visita"))) is not None
        }
        coverage_by_visit: dict[str, list[str]] = {}
        for visit in visitas:
            sites = sorted({
                row["COMMUNITY"].strip()
                for row in subset
                if row["visita"].strip() == visit and row["COMMUNITY"].strip()
            })
            if sites:
                coverage_by_visit[visit] = sites
        pollinator_values = [row["Pollinator"] for row in subset]
        method_rows[method] = {
            "rows": len(subset),
            "community_count": cardinality(subset, "COMMUNITY"),
            "visit_count": cardinality(subset, "visita"),
            "census_count": cardinality(subset, "censo"),
            "community_x_visit_context_count": len(community_visit),
            "community_x_visit_context_keys": sorted_context_keys(subset, ("COMMUNITY", "visita")),
            "community_x_visit_x_census_count": context_count(subset, ("COMMUNITY", "visita", "censo")),
            "community_coverage_by_visit": coverage_by_visit,
            "visits_with_all_six_communities": sum(len(sites) == 6 for sites in coverage_by_visit.values()),
            "blank_pollinator_rows": sum(not str(value).strip() for value in pollinator_values),
            "nonblank_pollinator_label_count": len({str(value).strip() for value in pollinator_values if str(value).strip()}),
            "n_ind_structure": numeric_presence(subset, "N ind"),
            "n_visit_flowers_structure": numeric_presence(subset, "N visit flowers"),
            "n_observed_flowers_structure": numeric_presence(subset, "N observed flowers"),
            "duration_structure": numeric_presence(subset, "Delta_T_minutes"),
        }

    methods_by_community_visit: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        key = context_key(row, ("COMMUNITY", "visita"))
        method = row["Method"].strip()
        if key is not None and method:
            methods_by_community_visit[key].add(method)
    method_pattern_counts = Counter(tuple(sorted(values)) for values in methods_by_community_visit.values())

    habitat_by_community: dict[str, list[str]] = {}
    community_habitat_pair_counts: dict[str, int] = {}
    for community in comunidades:
        habitat_by_community[community] = sorted({
            row["habitat"].strip()
            for row in rows
            if row["COMMUNITY"].strip() == community and row["habitat"].strip()
        })
        for habitat in habitat_by_community[community]:
            community_habitat_pair_counts[f"{community}|{habitat}"] = sum(
                row["COMMUNITY"].strip() == community and row["habitat"].strip() == habitat
                for row in rows
            )

    pollinator_raw = [row["Pollinator"] for row in rows]
    plant_raw = [row["Plant sp"] for row in rows]
    blank_pollinator_rows = [row for row in rows if not row["Pollinator"].strip()]
    nonblank_zero_ind_labels = Counter(
        row["Pollinator"].strip()
        for row in rows
        if row["Pollinator"].strip() and parse_float(row["N ind"]) == 0
    )

    payload_out = {
        "schema_version": "1.1",
        "analysis": "cabrera_2025_reconstruction_structure_audit",
        "source_sha256": CSV_SHA256,
        "source_rows": len(rows),
        "headers": headers,
        "structural_cardinalities": {
            "community": len(comunidades),
            "visita": len(visitas),
            "censo": cardinality(rows, "censo"),
            "method": len(methods),
            "habitat": cardinality(rows, "habitat"),
            "plant_raw_nonblank": cardinality(rows, "Plant sp"),
            "pollinator_raw_nonblank": cardinality(rows, "Pollinator"),
            "community_x_visita": context_count(rows, ("COMMUNITY", "visita")),
            "community_x_visita_x_method": context_count(rows, ("COMMUNITY", "visita", "Method")),
            "community_x_visita_x_censo": context_count(rows, ("COMMUNITY", "visita", "censo")),
        },
        "source_values": {
            "methods": methods,
            "communities": comunidades,
            "visitas": visitas,
            "habitats": habitats,
            "islands": islands,
            "habitat_by_community": habitat_by_community,
            "community_habitat_pair_row_counts": community_habitat_pair_counts,
            "method_pattern_counts_across_community_x_visita": {
                "|".join(pattern): count for pattern, count in sorted(method_pattern_counts.items())
            },
        },
        "method_structure": method_rows,
        "zero_and_blank_structure": {
            "blank_pollinator_row_count": len(blank_pollinator_rows),
            "blank_pollinator_rows_n_ind": numeric_presence(blank_pollinator_rows, "N ind"),
            "blank_pollinator_rows_n_visit_flowers": numeric_presence(blank_pollinator_rows, "N visit flowers"),
            "nonblank_pollinator_labels_with_zero_n_ind": dict(sorted(nonblank_zero_ind_labels.items())),
            "all_rows_n_ind": numeric_presence(rows, "N ind"),
            "all_rows_n_visit_flowers": numeric_presence(rows, "N visit flowers"),
        },
        "identity_audit": {
            "plant": label_collision_audit(plant_raw),
            "pollinator": label_collision_audit(pollinator_raw),
        },
        "target_metrics_calculated": False,
        "network_matrices_built": False,
        "claim_boundary": (
            "This is a source-structure audit only. Counts of rows, exact source-observed context keys, methods, missing/zero source fields, "
            "and identity spellings are inspected to freeze reconstruction rules before any v8 support or architecture target is calculated."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload_out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload_out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
