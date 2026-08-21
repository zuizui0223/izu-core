from __future__ import annotations

import io
import json
import math
from collections import Counter, defaultdict
from datetime import date, datetime, time
from pathlib import Path

from openpyxl import load_workbook

import acquire_audit_martinique_2025_v9_source as source_gate

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DESIGN = ROOT / "data/design/abm_v9_martinique_2025_source_gate_v1.json"
OUT = ROOT / "data/results/martinique_2025_reconstruction_structure.json"
INTERACTION_NAME = "Plant_insect_interactions_former_names.xlsx"
SAMPLING_NAME = "Sampling_data.xlsx"


def fetch_required_bytes() -> dict[str, bytes]:
    design = json.loads(SOURCE_DESIGN.read_text())
    recovered: dict[str, bytes] = {}
    for row in design["author_deposited_files"]:
        if row["name"] not in {INTERACTION_NAME, SAMPLING_NAME}:
            continue
        status, payload, error = source_gate.fetch(row["url"])
        if status != 200 or payload is None:
            raise RuntimeError(f"required Martinique source unavailable: {row['name']} {status} {error}")
        recovered[row["name"]] = payload
    if set(recovered) != {INTERACTION_NAME, SAMPLING_NAME}:
        raise RuntimeError("required Martinique workbooks were not both recovered")
    return recovered


def rows_from_sheet(payload: bytes, sheet_name: str) -> tuple[list[str], list[dict[str, object]]]:
    book = load_workbook(io.BytesIO(payload), read_only=True, data_only=True)
    if sheet_name not in book.sheetnames:
        raise RuntimeError(f"missing sheet {sheet_name}")
    sheet = book[sheet_name]
    iterator = sheet.iter_rows(values_only=True)
    header_row = next(iterator)
    headers = [str(value).strip() if value is not None else "" for value in header_row]
    rows = []
    for raw in iterator:
        if not any(value not in (None, "") for value in raw):
            continue
        row = {header: value for header, value in zip(headers, raw) if header}
        rows.append(row)
    book.close()
    return headers, rows


def clean(value: object) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().split())


def canonical_month(value: object) -> str | None:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m")
    if isinstance(value, date):
        return value.strftime("%Y-%m")
    text = clean(value)
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m")
        except ValueError:
            pass
    if len(text) >= 7 and text[4] in "-/" and text[:4].isdigit():
        return text[:7].replace("/", "-")
    return None


def canonical_date(value: object) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = clean(value)
    return text or None


def minutes_since_midnight(value: object) -> float | None:
    if isinstance(value, datetime):
        value = value.time()
    if isinstance(value, time):
        return value.hour * 60 + value.minute + value.second / 60
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        number = float(value)
        if 0 <= number < 1:
            return number * 24 * 60
    text = clean(value)
    if not text:
        return None
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.hour * 60 + parsed.minute + parsed.second / 60
        except ValueError:
            pass
    return None


def numeric(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def identity_structure(rows: list[dict[str, object]], best: str, genus: str, species: str, family: str) -> dict:
    blank_best = sum(not clean(row.get(best)) for row in rows)
    fallback_genus_species = sum(
        not clean(row.get(best)) and bool(clean(row.get(genus))) and bool(clean(row.get(species)))
        for row in rows
    )
    fallback_genus = sum(
        not clean(row.get(best)) and bool(clean(row.get(genus))) and not clean(row.get(species))
        for row in rows
    )
    fallback_family = sum(
        not clean(row.get(best)) and not clean(row.get(genus)) and bool(clean(row.get(family)))
        for row in rows
    )
    unresolved = sum(
        not clean(row.get(best))
        and not clean(row.get(genus))
        and not clean(row.get(species))
        and not clean(row.get(family))
        for row in rows
    )
    best_values = {clean(row.get(best)) for row in rows if clean(row.get(best))}
    return {
        "row_count": len(rows),
        "nonblank_best_id_count": len(best_values),
        "blank_best_id_rows": blank_best,
        "blank_best_with_genus_species_rows": fallback_genus_species,
        "blank_best_with_genus_only_rows": fallback_genus,
        "blank_best_with_family_only_rows": fallback_family,
        "fully_unresolved_rows": unresolved,
    }


def context_keys(rows: list[dict[str, object]]) -> dict:
    sites = sorted({clean(row.get("Site")) for row in rows if clean(row.get("Site"))})
    periods = sorted({clean(row.get("Period")) for row in rows if clean(row.get("Period"))})
    dates = sorted({canonical_date(row.get("Date")) for row in rows if canonical_date(row.get("Date"))})
    months = sorted({canonical_month(row.get("Date")) for row in rows if canonical_month(row.get("Date"))})
    site_month = sorted({
        (clean(row.get("Site")), canonical_month(row.get("Date")))
        for row in rows
        if clean(row.get("Site")) and canonical_month(row.get("Date"))
    })
    site_period = sorted({
        (clean(row.get("Site")), clean(row.get("Period")))
        for row in rows
        if clean(row.get("Site")) and clean(row.get("Period"))
    })
    return {
        "sites": sites,
        "periods": periods,
        "dates": dates,
        "months": months,
        "site_month_keys": [list(key) for key in site_month],
        "site_period_keys": [list(key) for key in site_period],
        "site_count": len(sites),
        "period_count": len(periods),
        "date_count": len(dates),
        "month_count": len(months),
        "site_month_count": len(site_month),
        "site_period_count": len(site_period),
    }


def period_month_map(rows: list[dict[str, object]]) -> dict[str, list[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        period = clean(row.get("Period"))
        month = canonical_month(row.get("Date"))
        if period and month:
            mapping[period].add(month)
    return {key: sorted(values) for key, values in sorted(mapping.items())}


def site_month_coverage(rows: list[dict[str, object]]) -> dict[str, list[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        site = clean(row.get("Site"))
        month = canonical_month(row.get("Date"))
        if site and month:
            mapping[month].add(site)
    return {month: sorted(sites) for month, sites in sorted(mapping.items())}


def exposure_structure(rows: list[dict[str, object]]) -> dict:
    unique_windows = set()
    invalid_windows = 0
    for row in rows:
        site = clean(row.get("Site"))
        month = canonical_month(row.get("Date"))
        day = canonical_date(row.get("Date"))
        transect = clean(row.get("Transect"))
        start = minutes_since_midnight(row.get("H_start"))
        end = minutes_since_midnight(row.get("H_end"))
        if not site or not month or start is None or end is None:
            continue
        duration = end - start
        if duration < 0:
            duration += 24 * 60
        if duration <= 0:
            invalid_windows += 1
            continue
        unique_windows.add((site, month, day, transect, round(start, 6), round(end, 6), round(duration, 6)))

    minutes_by_context: dict[tuple[str, str], float] = defaultdict(float)
    windows_by_context: Counter[tuple[str, str]] = Counter()
    for site, month, _day, _transect, _start, _end, duration in unique_windows:
        minutes_by_context[(site, month)] += duration
        windows_by_context[(site, month)] += 1
    values = list(minutes_by_context.values())
    return {
        "unique_observation_window_count": len(unique_windows),
        "invalid_or_nonpositive_window_count": invalid_windows,
        "site_months_with_recoverable_windows": len(minutes_by_context),
        "total_unique_window_minutes_min": min(values) if values else None,
        "total_unique_window_minutes_max": max(values) if values else None,
        "total_unique_window_minutes_distinct": sorted({round(value, 6) for value in values}),
        "window_count_per_site_month_distinct": sorted(set(windows_by_context.values())),
    }


def floral_structure(rows: list[dict[str, object]]) -> dict:
    values = [numeric(row.get("Nb_Floral_unit")) for row in rows]
    finite = [value for value in values if value is not None]
    quadrat_by_context: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        site = clean(row.get("Site"))
        month = canonical_month(row.get("Date"))
        quadrat = clean(row.get("Quadrat"))
        transect = clean(row.get("Transect"))
        if site and month and quadrat:
            quadrat_by_context[(site, month)].add(f"{transect}|{quadrat}")
    quadrat_counts = [len(values) for values in quadrat_by_context.values()]
    return {
        "nb_floral_unit_numeric_rows": len(finite),
        "nb_floral_unit_missing_or_nonnumeric_rows": len(values) - len(finite),
        "nb_floral_unit_negative_rows": sum(value < 0 for value in finite),
        "nb_floral_unit_zero_rows": sum(value == 0 for value in finite),
        "nb_floral_unit_positive_rows": sum(value > 0 for value in finite),
        "site_months_with_quadrat_ids": len(quadrat_by_context),
        "quadrat_count_per_site_month_distinct": sorted(set(quadrat_counts)),
    }


def main() -> None:
    payloads = fetch_required_bytes()
    interaction_headers, interaction_rows = rows_from_sheet(payloads[INTERACTION_NAME], "Insects-Plants")
    _sampling_interaction_headers, sampling_interaction_rows = rows_from_sheet(payloads[SAMPLING_NAME], "Insects_Plants")
    floral_headers, floral_rows = rows_from_sheet(payloads[SAMPLING_NAME], "Floral_abundance")

    interaction_context = context_keys(interaction_rows)
    sampling_interaction_context = context_keys(sampling_interaction_rows)
    floral_context = context_keys(floral_rows)

    output = {
        "schema_version": "1.0",
        "analysis": "martinique_2025_reconstruction_structure_audit",
        "target_metrics_calculated": False,
        "network_matrices_built": False,
        "interaction_events_aggregated": False,
        "v9_predictive_fit_calculated": False,
        "source_hashes": {name: source_gate.sha256(payload) for name, payload in payloads.items()},
        "interaction": {
            "headers": interaction_headers,
            "row_count": len(interaction_rows),
            "context_structure": interaction_context,
            "period_to_months": period_month_map(interaction_rows),
            "site_coverage_by_month": site_month_coverage(interaction_rows),
            "plant_identity": identity_structure(interaction_rows, "Plant_Best_ID", "Plant_genus", "Plant_species", "Plant_family"),
            "insect_identity": identity_structure(interaction_rows, "Insect_Best_ID", "Insect_genus", "Insect_species", "Insect_family"),
            "exposure_structure": exposure_structure(interaction_rows),
        },
        "sampling_workbook_interaction_sheet": {
            "row_count": len(sampling_interaction_rows),
            "same_row_count_as_former_names_workbook": len(sampling_interaction_rows) == len(interaction_rows),
            "context_structure": sampling_interaction_context,
        },
        "floral_abundance": {
            "headers": floral_headers,
            "row_count": len(floral_rows),
            "context_structure": floral_context,
            "period_to_months": period_month_map(floral_rows),
            "site_coverage_by_month": site_month_coverage(floral_rows),
            "plant_identity": identity_structure(floral_rows, "Plant_Best_ID", "Plant_genus", "Plant_species", "Plant_family"),
            "floral_measure_structure": floral_structure(floral_rows),
        },
        "cross_source_structure": {
            "site_sets_match": set(interaction_context["sites"]) == set(floral_context["sites"]),
            "month_sets_match": set(interaction_context["months"]).issubset(set(floral_context["months"])),
            "period_sets_match": set(interaction_context["periods"]).issubset(set(floral_context["periods"])),
            "interaction_site_month_keys_subset_of_floral": {
                tuple(row) for row in interaction_context["site_month_keys"]
            }.issubset({tuple(row) for row in floral_context["site_month_keys"]}),
            "interaction_site_period_keys_subset_of_floral": {
                tuple(row) for row in interaction_context["site_period_keys"]
            }.issubset({tuple(row) for row in floral_context["site_period_keys"]}),
            "floral_site_month_keys_without_interaction_events": [
                list(key)
                for key in sorted(
                    {tuple(row) for row in floral_context["site_month_keys"]}
                    - {tuple(row) for row in interaction_context["site_month_keys"]}
                )
            ],
        },
        "claim_boundary": (
            "Source-structure audit only. Cardinalities, identity completeness, time/context keys, observation-window structure, "
            "and floral-unit field validity are inspected before selecting network units or calculating any ecological network target."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "interaction_rows": len(interaction_rows),
        "floral_rows": len(floral_rows),
        "interaction_context": interaction_context,
        "floral_context": floral_context,
        "interaction_period_to_months": output["interaction"]["period_to_months"],
        "floral_period_to_months": output["floral_abundance"]["period_to_months"],
        "plant_identity_interaction": output["interaction"]["plant_identity"],
        "insect_identity": output["interaction"]["insect_identity"],
        "plant_identity_floral": output["floral_abundance"]["plant_identity"],
        "exposure": output["interaction"]["exposure_structure"],
        "floral_measure": output["floral_abundance"]["floral_measure_structure"],
        "cross_source": output["cross_source_structure"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
