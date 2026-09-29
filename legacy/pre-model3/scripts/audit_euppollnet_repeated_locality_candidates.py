from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import math
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_euppollnet_repeated_locality_screen_20260914.json"
TAG = "v1.3.0"
SOURCE_REPO = "JoseBSL/EuPPollNet"
SOURCE_BLOB_SHA = "6e639d4af81feee76eefa6804622f8b901c39feb"
SOURCE_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/3_Final_data/Interaction_data.csv.gz"
METADATA_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/3_Final_data/Metadata.csv"


def get_bytes(url: str, timeout: int = 180) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def decode_text(payload: bytes) -> tuple[str, str]:
    """Decode pinned source bytes losslessly; never replace undecodable bytes."""
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return payload.decode(encoding, errors="strict"), encoding
        except UnicodeDecodeError:
            continue
    raise RuntimeError("EuPPollNet source could not be decoded losslessly")


def clean(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def pick(fieldnames: list[str], *candidates: str) -> str | None:
    lower = {name.casefold(): name for name in fieldnames}
    for candidate in candidates:
        if candidate.casefold() in lower:
            return lower[candidate.casefold()]
    return None


def number(value: object) -> float | None:
    try:
        x = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def main() -> None:
    payload = get_bytes(SOURCE_URL)
    source_sha256 = hashlib.sha256(payload).hexdigest()
    decompressed = gzip.decompress(payload)
    text, interaction_encoding = decode_text(decompressed)
    reader = csv.DictReader(io.StringIO(text))
    fields = list(reader.fieldnames or [])

    study_col = pick(fields, "Study_id")
    network_col = pick(fields, "Network_id")
    country_col = pick(fields, "Country")
    locality_col = pick(fields, "Locality")
    lat_col = pick(fields, "Latitude")
    lon_col = pick(fields, "Longitude")
    date_col = pick(fields, "Date")
    interaction_col = pick(fields, "Number_interactions", "Interactions", "Number_of_interactions")
    poll_col = pick(fields, "Pollinator_accepted_name", "Pollinator_name", "Pollinator")
    method_col = pick(fields, "Sampling_method")
    flower_available_col = pick(fields, "Floral_count_data", "Flower_count_data", "Flower_counts_available")

    required = {
        "study": study_col,
        "country": country_col,
        "locality": locality_col,
        "latitude": lat_col,
        "longitude": lon_col,
        "date": date_col,
        "pollinator": poll_col,
    }
    missing = [role for role, col in required.items() if col is None]
    if missing:
        raise RuntimeError(f"EuPPollNet schema drift; missing roles={missing}; fields={fields}")

    metadata_payload = get_bytes(METADATA_URL)
    metadata_text, metadata_encoding = decode_text(metadata_payload)
    metadata_rows = list(csv.DictReader(io.StringIO(metadata_text)))
    metadata_by_study = {clean(row.get("Study_id")): row for row in metadata_rows if clean(row.get("Study_id"))}

    groups: dict[tuple[str, str, str, str, str], dict] = {}
    total_rows = 0
    for row in reader:
        total_rows += 1
        study = clean(row.get(study_col))
        country = clean(row.get(country_col))
        locality = clean(row.get(locality_col))
        lat = clean(row.get(lat_col))
        lon = clean(row.get(lon_col))
        day = clean(row.get(date_col))[:10]
        pollinator = clean(row.get(poll_col))
        if not all((study, day, pollinator)):
            continue
        # The exact source-native location identity is the full study/country/locality/lat/lon tuple.
        key = (study, country, locality, lat, lon)
        record = groups.setdefault(key, {
            "dates": set(),
            "partners": set(),
            "events": Counter(),
            "network_ids": set(),
            "sampling_methods": set(),
            "flower_flags": set(),
            "interaction_values": [],
        })
        record["dates"].add(day)
        record["partners"].add(pollinator)
        record["events"][(day, pollinator)] += 1
        if network_col and clean(row.get(network_col)):
            record["network_ids"].add(clean(row.get(network_col)))
        if method_col and clean(row.get(method_col)):
            record["sampling_methods"].add(clean(row.get(method_col)))
        if flower_available_col and clean(row.get(flower_available_col)):
            record["flower_flags"].add(clean(row.get(flower_available_col)))
        if interaction_col:
            x = number(row.get(interaction_col))
            if x is not None:
                record["interaction_values"].append(x)

    candidates = []
    for key, record in groups.items():
        dates = sorted(record["dates"])
        if len(dates) < 6:
            continue
        partners = sorted(record["partners"])
        nonconstant = 0
        for partner in partners:
            series = [record["events"].get((day, partner), 0) for day in dates]
            if len(set(series)) > 1:
                nonconstant += 1
        if nonconstant < 3:
            continue
        study, country, locality, lat, lon = key
        meta = metadata_by_study.get(study, {})
        values = record["interaction_values"]
        candidates.append({
            "study_id": study,
            "country": country,
            "locality": locality,
            "latitude": lat,
            "longitude": lon,
            "distinct_dates": len(dates),
            "date_min": dates[0],
            "date_max": dates[-1],
            "partner_count": len(partners),
            "nonconstant_partner_series": nonconstant,
            "network_id_count": len(record["network_ids"]),
            "network_ids_preview": sorted(record["network_ids"])[:20],
            "sampling_methods_in_rows": sorted(record["sampling_methods"]),
            "flower_count_flags_in_rows": sorted(record["flower_flags"]),
            "interaction_value_column": interaction_col,
            "numeric_interaction_values_present": bool(values),
            "nonbinary_interaction_values_present": any(x not in {0.0, 1.0} for x in values),
            "study_metadata": {
                "doi": clean(meta.get("DOI")),
                "year": clean(meta.get("Year")),
                "sampling_method": clean(meta.get("Sampling_method")),
                "min_date": clean(meta.get("Min_date")),
                "max_date": clean(meta.get("Max_date")),
                "sampling_days": clean(meta.get("Sampling_days")),
                "sampling_period": clean(meta.get("Sampling_period")),
                "total_interactions": clean(meta.get("Total_interactions")),
            },
            "island_status": "unreviewed_after_result_blind_structure_screen",
            "effort_status": "unreviewed_after_result_blind_structure_screen",
        })

    candidates.sort(key=lambda row: (row["study_id"], row["country"], row["locality"], row["latitude"], row["longitude"]))
    result = {
        "schema_version": "1.1",
        "analysis": "chapter2_euppollnet_repeated_locality_screen",
        "status": "result_blind_source_structure_screen_coordinates_not_opened",
        "source": {
            "repository": SOURCE_REPO,
            "tag": TAG,
            "interaction_git_blob_sha": SOURCE_BLOB_SHA,
            "interaction_url": SOURCE_URL,
            "interaction_gzip_bytes": len(payload),
            "interaction_gzip_sha256": source_sha256,
            "interaction_decoded_bytes": len(decompressed),
            "interaction_text_encoding": interaction_encoding,
            "metadata_url": METADATA_URL,
            "metadata_sha256": hashlib.sha256(metadata_payload).hexdigest(),
            "metadata_text_encoding": metadata_encoding,
        },
        "schema_fields": fields,
        "resolved_roles": {
            "study": study_col,
            "network": network_col,
            "country": country_col,
            "locality": locality_col,
            "latitude": lat_col,
            "longitude": lon_col,
            "date": date_col,
            "interaction_value": interaction_col,
            "pollinator": poll_col,
            "sampling_method": method_col,
            "flower_count_available": flower_available_col,
        },
        "total_interaction_rows": total_rows,
        "exact_locality_groups": len(groups),
        "screen_rule": {
            "stable_system": "exact Study_id x Country x Locality x Latitude x Longitude tuple",
            "minimum_distinct_dates": 6,
            "minimum_nonconstant_partner_series": 3,
            "island_filter_applied": False,
            "effort_filter_applied": False,
            "coordinates_or_response_values_calculated": False,
        },
        "candidate_count": len(candidates),
        "candidate_studies": sorted({row["study_id"] for row in candidates}),
        "candidates": candidates,
        "claim_boundary": "The screen is performed across the complete pinned EuPPollNet v1.3.0 interaction table before island or effort review. It uses only source identifiers, exact locality/coordinates, dates and partner identities to enforce the frozen >=6-bin and >=3-nonconstant-series requirements. No D1, phi, response, determinant or journal-route value is computed or used. Source text is decoded losslessly using a deterministic encoding fallback; undecodable bytes are never replaced."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "interaction_text_encoding": interaction_encoding,
        "total_interaction_rows": total_rows,
        "exact_locality_groups": len(groups),
        "candidate_count": len(candidates),
        "candidate_studies": result["candidate_studies"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
