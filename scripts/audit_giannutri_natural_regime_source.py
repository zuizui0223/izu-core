from __future__ import annotations

import csv
import importlib.util
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data/external/giannutri2025"
SOURCE_GATE = ROOT / "data/design/abm_v6_giannutri_source_gate_v1.json"
DAILY_DESIGN = ROOT / "data/design/abm_v6_giannutri_daily_validation_v1.json"
RECONSTRUCTION_SCRIPT = ROOT / "scripts/audit_giannutri2025_daily_reconstruction_structure.py"
OUT = ROOT / "data/results/chapter2_giannutri_natural_regime_source_audit_20260914.json"

FOCAL = ("Apis_mellifera", "Anthophora_dispar", "Bombus_terrestris")


def clean(value: object) -> str:
    text = str(value or "").strip()
    if text.endswith(".0") and text[:-2].isdigit():
        return text[:-2]
    return text


def norm_header(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", clean(value).lower()).strip("_")


def read_table(path: Path) -> tuple[list[str], list[dict[str, str]], str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    sample = text[:10000]
    delimiter = "\t"
    try:
        delimiter = csv.Sniffer().sniff(sample, delimiters="\t,;").delimiter
    except csv.Error:
        pass
    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    rows = list(reader)
    return list(reader.fieldnames or []), rows, delimiter


def load_reconstruction_module():
    spec = importlib.util.spec_from_file_location("giannutri_source_reconstruction", RECONSTRUCTION_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def pick_exact_column(headers: list[str], candidates: tuple[str, ...]) -> str | None:
    normalized = {norm_header(header): header for header in headers}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


def main() -> None:
    source_gate = json.loads(SOURCE_GATE.read_text(encoding="utf-8"))
    daily_design = json.loads(DAILY_DESIGN.read_text(encoding="utf-8"))
    locked_dates = [clean(value) for value in daily_design["source_native_reconstruction"]["locked_final_dates"]]

    overlap_path = RAW_DIR / "transect_data_for_overlap_analysis.txt"
    walking_path = RAW_DIR / "walking_transects_dataset.txt"
    missing = [str(path.relative_to(ROOT)) for path in (overlap_path, walking_path) if not path.is_file()]
    if missing:
        raise RuntimeError(f"checksum-locked Giannutri source files missing after acquisition: {missing}")

    reconstruction = load_reconstruction_module()
    raw_overlap = reconstruction.fetch_rows()
    prefiltered = reconstruction.source_prefilter(raw_overlap)
    after_pool = reconstruction.pool_rows(prefiltered, set())
    final_rows, low_observation_dates = reconstruction.minimum_observation_filter(after_pool)
    final_dates = sorted({clean(row["Date"]) for row in final_rows})
    exact_locked_dates = final_dates == locked_dates

    walking_headers, walking_rows, walking_delimiter = read_table(walking_path)
    date_col = pick_exact_column(walking_headers, ("date", "sampling_date", "event_date"))
    transect_col = pick_exact_column(
        walking_headers,
        ("transetto", "transect", "transect_id", "transectid", "number", "numero"),
    )

    walking_inventory = {
        "rows": len(walking_rows),
        "columns": walking_headers,
        "delimiter_repr": repr(walking_delimiter),
        "date_column": date_col,
        "transect_column": transect_col,
    }

    effort_by_date: dict[str, int] = {}
    walking_dates: set[str] = set()
    if date_col is not None and transect_col is not None:
        transects: dict[str, set[str]] = defaultdict(set)
        for row in walking_rows:
            date = clean(row.get(date_col))
            transect = clean(row.get(transect_col))
            if not date:
                continue
            walking_dates.add(date)
            if transect:
                transects[date].add(transect)
        effort_by_date = {date: len(transects.get(date, set())) for date in locked_dates}

    rows_by_date_species: dict[tuple[str, str], float] = defaultdict(float)
    for row in final_rows:
        date = clean(row.get("Date"))
        species = clean(row.get("species"))
        plant = clean(row.get("plant"))
        if species not in FOCAL or plant == "volo":
            continue
        value = float(row.get("total") or 0.0)
        if not math.isfinite(value) or value < 0:
            raise RuntimeError(f"invalid interaction total: {row}")
        rows_by_date_species[(date, species)] += value

    standardized_series: dict[str, list[float]] = {species: [] for species in FOCAL}
    effort_complete = bool(effort_by_date) and all(effort_by_date.get(date, 0) > 0 for date in locked_dates)
    if effort_complete:
        for date in locked_dates:
            effort = float(effort_by_date[date])
            for species in FOCAL:
                standardized_series[species].append(rows_by_date_species.get((date, species), 0.0) / effort)

    series_nonconstant = {
        species: len(values) == len(locked_dates) and len({round(value, 15) for value in values}) > 1
        for species, values in standardized_series.items()
    }

    admission = bool(
        exact_locked_dates
        and len(final_dates) == 29
        and date_col is not None
        and transect_col is not None
        and effort_complete
        and all(series_nonconstant.values())
    )

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_giannutri_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "article_doi": source_gate["candidate_system"]["article_doi"],
            "zenodo_doi": source_gate["candidate_system"]["zenodo_doi"],
            "network_scope": source_gate["candidate_system"]["published_network_scope"],
            "published_daily_network_count": source_gate["candidate_system"]["published_daily_network_count"],
        },
        "source_native_selection": {
            "locked_date_count": len(locked_dates),
            "reconstructed_final_date_count": len(final_dates),
            "exact_locked_date_match": exact_locked_dates,
            "low_observation_dates_removed_by_source_rule": sorted(clean(value) for value in low_observation_dates),
            "ascertainment_boundary": "The 29 days are the source-defined retained three-bee daily networks. Their inclusion rule was fixed in the published source and frozen in izu-core before any natural D1/phi computation. They are not treated as a random sample of all island days.",
        },
        "walking_transect_effort": walking_inventory,
        "effort_by_locked_date": effort_by_date,
        "walking_contains_all_locked_dates": bool(effort_by_date) and all(date in walking_dates for date in locked_dates),
        "all_locked_dates_have_positive_reconstructed_transect_effort": effort_complete,
        "focal_partner_series": {
            species: {
                "time_bins": len(standardized_series[species]),
                "nonconstant_after_transect_standardization": series_nonconstant[species],
            }
            for species in FOCAL
        },
        "gate_checks": {
            "stable_system_identity": True,
            "source_native_time_bins_at_least_6": len(final_dates) >= 6,
            "stable_partner_identity": True,
            "minimum_nonconstant_partner_series_at_least_3": all(series_nonconstant.values()),
            "sampling_effort_reconstructible_from_independent_walking_transect_file": effort_complete,
            "coordinates_opened": False,
        },
        "decision": "ADMIT_BEFORE_COORDINATES" if admission else "FAIL_OR_REQUIRES_SOURCE_STRUCTURE_DIAGNOSIS",
        "claim_boundary": "This audit does not compute D1, phi, rho_eq, route thresholds, or any prior ABM target. It tests only whether the frozen 29 source-native daily networks can be effort-standardized using the independent walking-transect source file.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
