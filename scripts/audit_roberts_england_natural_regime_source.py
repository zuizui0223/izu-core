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
OUT = ROOT / "data/results/chapter2_roberts_england_natural_regime_source_audit_20260915.json"
SOURCE_REPO = "JoseBSL/EuPPollNet"
TAG = "v1.3.0"
INTERACTION_BLOB_SHA = "32604e7aac1b704112eae1afbb9b7de1849a1a27"
FLOWER_BLOB_SHA = "c9225e56b6e20441ba92fad442dc6ce8e3cd3af2"
PROCESSING_SCRIPT_BLOB_SHA = "f30479d6fb8dfdfc5af61676bed21f3d43ba9573"
INTERACTION_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/29_30_31_STEP/Interaction_data.csv"
FLOWER_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/29_30_31_STEP/Flower_count.csv"


def get_bytes(url: str, timeout: int = 180) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "text/csv,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def decode(payload: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return payload.decode(encoding, errors="strict"), encoding
        except UnicodeDecodeError:
            continue
    raise RuntimeError("STEP source could not be decoded losslessly")


def clean(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def pick(fields: list[str], *candidates: str) -> str | None:
    mapping = {clean(x).casefold(): x for x in fields}
    for candidate in candidates:
        if candidate.casefold() in mapping:
            return mapping[candidate.casefold()]
    return None


def number(value: object) -> float | None:
    try:
        x = float(clean(value))
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def date_key(row: dict[str, str], day_col: str, month_col: str, year_col: str) -> str:
    day, month, year = clean(row.get(day_col)), clean(row.get(month_col)), clean(row.get(year_col))
    if not all((day, month, year)):
        return ""
    try:
        return f"{int(float(year)):04d}-{int(float(month)):02d}-{int(float(day)):02d}"
    except ValueError:
        return ""


def main() -> None:
    interaction_bytes = get_bytes(INTERACTION_URL)
    flower_bytes = get_bytes(FLOWER_URL)
    interaction_text, interaction_encoding = decode(interaction_bytes)
    flower_text, flower_encoding = decode(flower_bytes)
    interactions_all = list(csv.DictReader(io.StringIO(interaction_text)))
    flowers_all = list(csv.DictReader(io.StringIO(flower_text)))
    if not interactions_all or not flowers_all:
        raise RuntimeError("STEP raw CSVs are empty")

    ifields = list(interactions_all[0].keys())
    ffields = list(flowers_all[0].keys())
    country_i = pick(ifields, "Country", "country")
    country_f = pick(ffields, "Country", "country")
    site_i = pick(ifields, "Site_id", "site_id")
    site_f = pick(ffields, "Site_id", "site_id")
    day_i, month_i, year_i = pick(ifields, "Day"), pick(ifields, "Month"), pick(ifields, "Year")
    day_f, month_f, year_f = pick(ffields, "Day"), pick(ffields, "Month"), pick(ffields, "Year")
    poll_i = pick(ifields, "Pollinator_species", "Pollinator")
    interaction_i = pick(ifields, "Interaction", "Interactions")
    effort_i = pick(ifields, "Sampling_effort_minutes")
    area_i = pick(ifields, "Sampling_area_square_meters")
    method_i = pick(ifields, "Sampling_method")
    required = [country_i, country_f, site_i, site_f, day_i, month_i, year_i, day_f, month_f, year_f, poll_i]
    if any(value is None for value in required):
        raise RuntimeError(f"STEP source schema drift; interaction={ifields}; flower={ffields}")

    interactions = [row for row in interactions_all if clean(row.get(country_i)).upper() == "UK"]
    flowers = [row for row in flowers_all if clean(row.get(country_f)).upper() == "UK"]

    by_site: dict[str, dict] = {}
    for row in interactions:
        site = clean(row.get(site_i))
        day = date_key(row, day_i, month_i, year_i)
        partner = clean(row.get(poll_i))
        if not site:
            continue
        rec = by_site.setdefault(site, {
            "interaction_dates": set(), "flower_dates": set(), "partners": set(), "events": Counter(),
            "effort_minutes": set(), "areas_m2": set(), "methods": set(),
        })
        if day:
            rec["interaction_dates"].add(day)
        if partner:
            rec["partners"].add(partner)
            value = number(row.get(interaction_i)) if interaction_i else 1.0
            if day and value is not None and value >= 0:
                rec["events"][(day, partner)] += value
        if effort_i:
            x = number(row.get(effort_i))
            if x is not None:
                rec["effort_minutes"].add(x)
        if area_i:
            x = number(row.get(area_i))
            if x is not None:
                rec["areas_m2"].add(x)
        if method_i and clean(row.get(method_i)):
            rec["methods"].add(clean(row.get(method_i)))

    for row in flowers:
        site = clean(row.get(site_f))
        day = date_key(row, day_f, month_f, year_f)
        if not site:
            continue
        rec = by_site.setdefault(site, {
            "interaction_dates": set(), "flower_dates": set(), "partners": set(), "events": Counter(),
            "effort_minutes": set(), "areas_m2": set(), "methods": set(),
        })
        if day:
            rec["flower_dates"].add(day)

    systems = []
    for site in sorted(by_site):
        rec = by_site[site]
        idates = sorted(rec["interaction_dates"])
        fdates = sorted(rec["flower_dates"])
        full_dates = fdates if fdates else idates
        partners = sorted(rec["partners"])
        nonconstant = 0
        for partner in partners:
            series = [float(rec["events"].get((day, partner), 0.0)) for day in full_dates]
            if len(set(series)) > 1:
                nonconstant += 1
        dates_by_year: dict[str, int] = defaultdict(int)
        for day in full_dates:
            dates_by_year[day[:4]] += 1
        systems.append({
            "system_id": site,
            "interaction_dates": len(idates),
            "flower_count_dates": len(fdates),
            "interaction_dates_subset_of_flower_dates": bool(idates) and set(idates).issubset(set(fdates)),
            "full_schedule_dates": len(full_dates),
            "full_schedule_dates_by_year": dict(sorted(dates_by_year.items())),
            "partner_count": len(partners),
            "nonconstant_partner_series_on_full_schedule": nonconstant,
            "sampling_methods": sorted(rec["methods"]),
            "sampling_effort_minutes_values": sorted(rec["effort_minutes"]),
            "sampling_area_m2_values": sorted(rec["areas_m2"]),
            "published_round_contract_pass": len(full_dates) >= 8 and all(count >= 4 for count in dates_by_year.values()) and len(dates_by_year) >= 2,
            "six_bin_floor_pass": len(full_dates) >= 6,
            "three_series_floor_pass": nonconstant >= 3,
        })

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_roberts_england_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "repository": SOURCE_REPO,
            "tag": TAG,
            "study_id": "31_Roberts",
            "interaction_git_blob_sha": INTERACTION_BLOB_SHA,
            "flower_git_blob_sha": FLOWER_BLOB_SHA,
            "processing_script_git_blob_sha": PROCESSING_SCRIPT_BLOB_SHA,
            "interaction_sha256": hashlib.sha256(interaction_bytes).hexdigest(),
            "flower_sha256": hashlib.sha256(flower_bytes).hexdigest(),
            "interaction_encoding": interaction_encoding,
            "flower_encoding": flower_encoding,
            "source_defined_island_status": "included by EuPPollNet manuscript in its pre-existing island_studies vector",
            "source_metadata": {
                "country": "England",
                "sampling_years": [2012, 2013],
                "sampling_rounds": "4 per year",
                "sampling_method": "Transect",
                "sampling_area": "two transects per site of 150 x 1 m",
                "sampling_time": "15 minutes per transect",
                "site_effort_per_round_minutes": 30,
            },
        },
        "raw_rows": {"uk_interactions": len(interactions), "uk_flower_counts": len(flowers)},
        "systems": systems,
        "admission_candidates_before_coordinates": [
            row["system_id"] for row in systems
            if row["published_round_contract_pass"] and row["six_bin_floor_pass"] and row["three_series_floor_pass"]
            and row["interaction_dates_subset_of_flower_dates"]
        ],
        "coordinates_opened": False,
        "claim_boundary": (
            "This audit uses EuPPollNet's own pre-existing island-study classification and the source processing script's four-rounds-per-year design. "
            "Flower-count dates are used only to reconstruct the outcome-independent visit schedule when they cover interaction dates. No D1, phi, response, determinant or route value is computed. "
            "England is retained as a source-defined continental-island study under the frozen island_or_archipelago scope; it is not reclassified based on downstream coordinates."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "uk_interactions": len(interactions),
        "uk_flower_counts": len(flowers),
        "systems": len(systems),
        "admission_candidates": result["admission_candidates_before_coordinates"],
        "system_summaries": systems,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
