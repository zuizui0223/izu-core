from __future__ import annotations

import csv
import io
import json
import math
import re
import tempfile
from pathlib import Path

import acquire_audit_thousand_island_lake_2022 as source_gate

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data/design/abm_v9_thousand_island_lake_reconstruction_gate_v1.json"
SOURCE_AUDIT = ROOT / "data/results/thousand_island_lake_2022_source_audit.json"
RAW_DIR = ROOT / "data/external/thousand_island_lake_2022"
OUT = ROOT / "data/results/thousand_island_lake_2022_reconstruction_structure.json"
SPATIAL_REL = "3_span_1CV/all_ints_spatial.csv"
TEMPORAL_REL = "3_span_1CV/all_ints_temporal.csv"
PAIR_CODE = re.compile(r"^(PO[^_]+)_(PL[^_]+)$", re.IGNORECASE)
SPATIAL_ID = re.compile(r"^(?:B\d+|S\d+)$", re.IGNORECASE)
TEMPORAL_ID = re.compile(r"^t(?:19|20)\d{2}$", re.IGNORECASE)
PLANT_CODE = re.compile(r"^PL[^_\s]+$", re.IGNORECASE)
POLLINATOR_CODE = re.compile(r"^PO[^_\s]+$", re.IGNORECASE)


def normalize(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")


def read_delimited(path: Path) -> tuple[list[str], list[list[str]], str]:
    payload = path.read_bytes()
    text, encoding = source_gate.decode_text(payload)
    lines = text.splitlines()
    sample = "\n".join(lines[:50])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        delimiter = dialect.delimiter
    except csv.Error:
        first = lines[0] if lines else ""
        delimiter = "\t" if "\t" in first else (";" if first.count(";") > first.count(",") else ",")
    rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
    if not rows:
        return [], [], encoding
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    return [str(x).strip() for x in rows[0]], rows[1:], encoding


def find_pair_column(headers: list[str], rows: list[list[str]]) -> int | None:
    for column in range(len(headers)):
        values = [str(row[column]).strip() for row in rows if str(row[column]).strip()]
        if not values:
            continue
        fraction = sum(bool(PAIR_CODE.fullmatch(value)) for value in values) / len(values)
        if fraction >= 0.8:
            return column
    return None


def numeric_column_properties(rows: list[list[str]], column: int) -> dict:
    values: list[float] = []
    for row in rows:
        text = str(row[column]).strip()
        if text == "":
            return {"all_numeric": False, "all_nonnegative": False, "all_integer": False}
        try:
            value = float(text)
        except ValueError:
            return {"all_numeric": False, "all_nonnegative": False, "all_integer": False}
        if not math.isfinite(value):
            return {"all_numeric": False, "all_nonnegative": False, "all_integer": False}
        values.append(value)
    return {
        "all_numeric": bool(values),
        "all_nonnegative": bool(values) and all(value >= 0.0 for value in values),
        "all_integer": bool(values) and all(float(value).is_integer() for value in values),
    }


def matrix_structure(path: Path, expected_kind: str) -> dict:
    headers, rows, encoding = read_delimited(path)
    pair_column = find_pair_column(headers, rows)
    if pair_column is None:
        raise RuntimeError(f"pair identity column not found in {path}")
    pair_codes = [str(row[pair_column]).strip() for row in rows if str(row[pair_column]).strip()]
    if expected_kind == "spatial":
        network_columns = [index for index, header in enumerate(headers) if SPATIAL_ID.fullmatch(str(header).strip())]
    elif expected_kind == "temporal":
        network_columns = [index for index, header in enumerate(headers) if TEMPORAL_ID.fullmatch(str(header).strip())]
    else:
        raise ValueError(expected_kind)
    properties = {headers[index]: numeric_column_properties(rows, index) for index in network_columns}
    decoded_pairs = []
    for code in pair_codes:
        match = PAIR_CODE.fullmatch(code)
        if match:
            decoded_pairs.append({"pair": code, "pollinator_code": match.group(1), "plant_code": match.group(2)})
    return {
        "path": str(path),
        "encoding": encoding,
        "data_row_count": len(rows),
        "pair_column_index": pair_column,
        "pair_column_header": headers[pair_column] or "<row_names>",
        "pair_code_count": len(pair_codes),
        "unique_pair_code_count": len(set(pair_codes)),
        "all_pair_codes_decode_as_PO_then_PL": len(decoded_pairs) == len(pair_codes),
        "unique_pollinator_code_count": len({row["pollinator_code"] for row in decoded_pairs}),
        "unique_plant_code_count": len({row["plant_code"] for row in decoded_pairs}),
        "network_columns": [headers[index] for index in network_columns],
        "network_column_count": len(network_columns),
        "all_network_columns_nonnegative_integer_counts": bool(network_columns) and all(
            row["all_numeric"] and row["all_nonnegative"] and row["all_integer"]
            for row in properties.values()
        ),
        "network_column_properties": properties,
        "pair_codes": pair_codes,
    }


def table_values_by_column(headers: list[str], rows: list[list[str]], limit: int = 12000) -> list[list[str]]:
    selected = rows[:limit]
    return [[str(row[column]).strip() for row in selected if str(row[column]).strip()] for column in range(len(headers))]


def structural_candidates(path: Path) -> dict:
    try:
        headers, rows, _ = read_delimited(path)
    except Exception:
        return {}
    if not headers or not rows:
        return {}
    normalized = [normalize(header) for header in headers]
    values = table_values_by_column(headers, rows)

    pair_columns = [
        index for index, column_values in enumerate(values)
        if column_values and sum(bool(PAIR_CODE.fullmatch(value)) for value in column_values) / len(column_values) >= 0.8
    ]
    plant_code_columns = [
        index for index, column_values in enumerate(values)
        if column_values and sum(bool(PLANT_CODE.fullmatch(value)) for value in column_values) / len(column_values) >= 0.8
    ]
    pollinator_code_columns = [
        index for index, column_values in enumerate(values)
        if column_values and sum(bool(POLLINATOR_CODE.fullmatch(value)) for value in column_values) / len(column_values) >= 0.8
    ]
    spatial_header_columns = [index for index, header in enumerate(headers) if SPATIAL_ID.fullmatch(str(header).strip())]
    temporal_header_columns = [index for index, header in enumerate(headers) if TEMPORAL_ID.fullmatch(str(header).strip())]
    network_header_columns = [
        index for index, key in enumerate(normalized)
        if any(token in key for token in ("island", "site", "network", "plot", "location"))
    ]
    time_header_columns = [
        index for index, key in enumerate(normalized)
        if any(token in key for token in ("year", "date", "month", "season", "time", "round", "survey"))
    ]
    availability_columns = [
        index for index, key in enumerate(normalized)
        if any(token in key for token in ("flower", "floral", "resource", "plant_abundance", "plant_density", "phenolog", "bloom"))
    ]
    exposure_columns = [
        index for index, key in enumerate(normalized)
        if any(token in key for token in ("effort", "duration", "minute", "hour", "census", "transect", "sampling_time", "observation_time"))
    ]

    wide_plant_network = False
    if plant_code_columns and spatial_header_columns:
        numeric_network = [numeric_column_properties(rows, index) for index in spatial_header_columns]
        wide_plant_network = all(row["all_numeric"] and row["all_nonnegative"] for row in numeric_network)

    long_independent_plant = bool(
        (plant_code_columns or any("plant" in key for key in normalized))
        and availability_columns
        and (network_header_columns or spatial_header_columns)
        and not pair_columns
        and not pollinator_code_columns
    )
    joint_site_year_pair = bool(
        pair_columns
        and ((network_header_columns and time_header_columns) or (spatial_header_columns and temporal_header_columns))
    )
    exposure_by_network = bool(exposure_columns and (network_header_columns or spatial_header_columns))

    if not any((wide_plant_network, long_independent_plant, joint_site_year_pair, exposure_by_network)):
        return {}
    return {
        "path": str(path),
        "headers": headers,
        "pair_columns": [headers[index] for index in pair_columns],
        "plant_code_columns": [headers[index] for index in plant_code_columns],
        "pollinator_code_columns": [headers[index] for index in pollinator_code_columns],
        "spatial_network_columns": [headers[index] for index in spatial_header_columns],
        "temporal_network_columns": [headers[index] for index in temporal_header_columns],
        "availability_columns": [headers[index] for index in availability_columns],
        "exposure_columns": [headers[index] for index in exposure_columns],
        "wide_plant_by_network_opportunity_candidate": wide_plant_network,
        "long_independent_plant_opportunity_candidate": long_independent_plant,
        "joint_site_year_pair_candidate": joint_site_year_pair,
        "sampling_exposure_by_network_candidate": exposure_by_network,
    }


def r_code_structure(path: Path) -> list[dict]:
    try:
        text, _ = source_gate.decode_text(path.read_bytes())
    except Exception:
        return []
    needles = (
        "all_ints_spatial", "all_ints_temporal", "ints_s_1cv", "flower", "floral",
        "effort", "duration", "year", "site", "island", "network", "interaction",
    )
    matches = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        lower = line.lower()
        if any(token in lower for token in needles):
            matches.append({"line": line_number, "text": line[:600]})
    return matches[:300]


def main() -> None:
    design = json.loads(DESIGN.read_text())
    source = json.loads(SOURCE_AUDIT.read_text())
    if source.get("status") != "source_admitted_til_raw_network_structure_before_v9_targets":
        raise RuntimeError("PR #209 source admission is not present")
    archives = sorted(RAW_DIR.glob("*.rar"))
    if len(archives) != 3:
        raise RuntimeError(f"expected three source RAR archives, found {len(archives)}")

    extracted_files: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="til_reconstruction_") as temporary:
        temp_root = Path(temporary)
        for archive in archives:
            destination = temp_root / archive.stem
            source_gate.extract_rar(archive, destination)
            extracted_files.extend(path for path in destination.rglob("*") if path.is_file())

        def find_suffix(relative_suffix: str) -> Path:
            matches = [path for path in extracted_files if str(path.relative_to(temp_root)).replace("\\", "/").endswith(relative_suffix)]
            if len(matches) != 1:
                raise RuntimeError(f"expected one {relative_suffix}, found {len(matches)}")
            return matches[0]

        spatial_path = find_suffix(SPATIAL_REL)
        temporal_path = find_suffix(TEMPORAL_REL)
        spatial = matrix_structure(spatial_path, "spatial")
        temporal = matrix_structure(temporal_path, "temporal")
        pair_identity_matches = set(spatial["pair_codes"]) == set(temporal["pair_codes"])

        candidates = []
        r_code_matches = []
        for path in extracted_files:
            suffix = path.suffix.lower()
            if suffix in {".csv", ".tsv", ".txt"}:
                candidate = structural_candidates(path)
                if candidate:
                    candidate["path"] = str(path.relative_to(temp_root)).replace("\\", "/")
                    candidates.append(candidate)
            elif suffix in {".r", ".rmd"}:
                rows = r_code_structure(path)
                if rows:
                    r_code_matches.append({
                        "path": str(path.relative_to(temp_root)).replace("\\", "/"),
                        "matches": rows,
                    })

    site_year_candidates = [row for row in candidates if row["joint_site_year_pair_candidate"]]
    plant_candidates = [
        row for row in candidates
        if row["wide_plant_by_network_opportunity_candidate"] or row["long_independent_plant_opportunity_candidate"]
    ]
    exposure_candidates = [row for row in candidates if row["sampling_exposure_by_network_candidate"]]

    raw_spatial_ok = (
        spatial["network_column_count"] == 42
        and spatial["unique_pair_code_count"] == spatial["pair_code_count"]
        and spatial["all_pair_codes_decode_as_PO_then_PL"]
        and spatial["all_network_columns_nonnegative_integer_counts"]
    )
    temporal_marginal_ok = (
        temporal["network_column_count"] == 3
        and temporal["unique_pair_code_count"] == temporal["pair_code_count"]
        and temporal["all_pair_codes_decode_as_PO_then_PL"]
        and temporal["all_network_columns_nonnegative_integer_counts"]
        and pair_identity_matches
    )
    independent_plant_opportunity_visible = bool(plant_candidates)
    sampling_exposure_visible = bool(exposure_candidates)
    joint_site_year_visible = bool(site_year_candidates)

    if not raw_spatial_ok:
        status = "blocked_til_reconstruction_spatial_pair_counts_not_auditable"
        admissible_claim = "blocked"
    elif independent_plant_opportunity_visible and sampling_exposure_visible:
        status = "til_reconstruction_supports_full_v9_design_freeze"
        admissible_claim = "full_v9"
    else:
        status = "til_reconstruction_supports_pair_support_only_not_full_v9"
        admissible_claim = "pair_support_only"

    output = {
        "schema_version": "1.0",
        "analysis": "thousand_island_lake_2022_reconstruction_structure_gate",
        "status": status,
        "admissible_claim": admissible_claim,
        "source_gate_pr": 209,
        "source_gate_status": source["status"],
        "spatial_matrix": {key: value for key, value in spatial.items() if key != "pair_codes"},
        "temporal_matrix": {key: value for key, value in temporal.items() if key != "pair_codes"},
        "pair_identity_set_matches_between_spatial_and_temporal_marginals": pair_identity_matches,
        "raw_42_spatial_pair_count_networks_auditable": raw_spatial_ok,
        "three_year_temporal_marginal_auditable": temporal_marginal_ok,
        "joint_site_year_pair_structure_visible": joint_site_year_visible,
        "joint_site_year_candidates": site_year_candidates,
        "independent_local_plant_resource_opportunity_visible": independent_plant_opportunity_visible,
        "plant_opportunity_candidates": plant_candidates,
        "sampling_exposure_visible_at_network_scale": sampling_exposure_visible,
        "sampling_exposure_candidates": exposure_candidates,
        "r_code_structural_matches": r_code_matches,
        "frozen_reconstruction_rule": (
            "Never form 42x3 site-year networks unless joint_site_year_pair_structure_visible is true. "
            "Use all_ints_spatial.csv as the only candidate repeated spatial pair-count matrix. "
            "Use all_ints_temporal.csv only as a separate whole-landscape temporal marginal."
        ),
        "target_metrics_calculated": False,
        "network_outcome_metrics_calculated": False,
        "v9_predictive_fit_calculated": False,
        "claim_boundary": design["claim_ladder"][admissible_claim],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": status,
        "admissible_claim": admissible_claim,
        "spatial_networks": spatial["network_column_count"],
        "temporal_networks": temporal["network_column_count"],
        "pair_rows_spatial": spatial["pair_code_count"],
        "pair_rows_temporal": temporal["pair_code_count"],
        "pair_identity_matches": pair_identity_matches,
        "joint_site_year_visible": joint_site_year_visible,
        "independent_plant_opportunity_visible": independent_plant_opportunity_visible,
        "sampling_exposure_visible": sampling_exposure_visible,
        "plant_candidate_count": len(plant_candidates),
        "exposure_candidate_count": len(exposure_candidates),
    }, indent=2))


if __name__ == "__main__":
    main()
