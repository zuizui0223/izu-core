from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_ireland_mullen_natural_regime_source_audit_20260915.json"
SOURCE_REPO = "JoseBSL/EuPPollNet"
TAG = "v1.3.0"
RAW_BLOB_SHA = "2aff02fbd6f11f006ea632d778d7632f5107c496"
PROCESSING_BLOB_SHA = "56fb9297b5d2c77ba2db7b61315ea41714dd9df4"
RAW_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/32_to_37_Russo/Interaction_data.csv"
PREFIX = "Sarah.Mullen_"
ROUND_RE = re.compile(r"^(?P<site>.+)_(?P<round>[1-6])_GS1$")


def get_bytes(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "text/csv,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def decode(payload: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return payload.decode(encoding, errors="strict"), encoding
        except UnicodeDecodeError:
            continue
    raise RuntimeError("Mullen source could not be decoded losslessly")


def clean(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def number(value: object) -> float | None:
    try:
        x = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def date_key(row: dict[str, str]) -> str:
    try:
        y = int(float(clean(row.get("Year"))))
        m = int(float(clean(row.get("Month"))))
        d = int(float(clean(row.get("Day"))))
    except ValueError:
        return ""
    return f"{y:04d}-{m:02d}-{d:02d}"


def main() -> None:
    payload = get_bytes(RAW_URL)
    text, encoding = decode(payload)
    rows = list(csv.DictReader(io.StringIO(text)))

    round_records: dict[tuple[str, int], dict] = {}
    source_rows = 0
    parse_failures: list[str] = []
    for row in rows:
        raw_id = clean(row.get("Site_id"))
        if not raw_id.startswith(PREFIX):
            continue
        source_rows += 1
        suffix = raw_id[len(PREFIX):]
        match = ROUND_RE.match(suffix)
        if match is None:
            parse_failures.append(raw_id)
            continue
        site = match.group("site")
        round_id = int(match.group("round"))
        key = (site, round_id)
        rec = round_records.setdefault(key, {
            "raw_ids": set(),
            "dates": set(),
            "effort_minutes": set(),
            "areas_m2": set(),
            "coordinates": set(),
            "partners": set(),
            "partner_counts": Counter(),
        })
        rec["raw_ids"].add(raw_id)
        day = date_key(row)
        if day:
            rec["dates"].add(day)
        effort = number(row.get("Sampling_effort_minutes"))
        area = number(row.get("Sampling_area_square_meters"))
        if effort is not None:
            rec["effort_minutes"].add(effort)
        if area is not None:
            rec["areas_m2"].add(area)
        lat = clean(row.get("WGS84/ETRS89"))
        lon = clean(row.get("WGS84/ETRS89_2"))
        if lat or lon:
            rec["coordinates"].add((lat, lon))
        partner = clean(row.get("Pollinator_species"))
        count = number(row.get("Interaction"))
        if partner:
            rec["partners"].add(partner)
            if count is not None and count >= 0:
                rec["partner_counts"][partner] += count

    sites = sorted({site for site, _ in round_records})
    systems = []
    admitted = []
    for site in sites:
        rounds = sorted(r for s, r in round_records if s == site)
        round_rows = [round_records[(site, r)] for r in rounds]
        partners = sorted(set().union(*(rec["partners"] for rec in round_rows))) if round_rows else []
        standardized: dict[str, list[float]] = {partner: [] for partner in partners}
        round_summaries = []
        round_structure_ok = True
        for r, rec in zip(rounds, round_rows):
            effort_values = sorted(rec["effort_minutes"])
            area_values = sorted(rec["areas_m2"])
            dates = sorted(rec["dates"])
            one_effort = len(effort_values) == 1 and effort_values[0] > 0
            one_area = len(area_values) == 1 and area_values[0] > 0
            one_date = len(dates) == 1
            round_structure_ok = round_structure_ok and one_effort and one_area and one_date
            effort = effort_values[0] if one_effort else None
            if effort is not None:
                for partner in partners:
                    standardized[partner].append(float(rec["partner_counts"].get(partner, 0.0)) / effort)
            round_summaries.append({
                "round": r,
                "date": dates[0] if one_date else None,
                "date_values": dates,
                "effort_minutes_values": effort_values,
                "sampling_area_m2_values": area_values,
                "partner_count": len(rec["partners"]),
                "positive_interaction_total": float(sum(rec["partner_counts"].values())),
            })

        nonconstant = sum(
            len(values) == len(rounds) and len({round(x, 15) for x in values}) > 1
            for values in standardized.values()
        )
        exact_rounds = rounds == [1, 2, 3, 4, 5, 6]
        unique_dates = {summary["date"] for summary in round_summaries if summary["date"]}
        distinct_dates = len(unique_dates)
        all_rounds_positive = all(summary["positive_interaction_total"] > 0 for summary in round_summaries)
        admission = bool(
            exact_rounds
            and round_structure_ok
            and distinct_dates == 6
            and nonconstant >= 3
            and all_rounds_positive
        )
        if admission:
            admitted.append(site)
        systems.append({
            "system_id": site,
            "source_native_round_ids": rounds,
            "exact_six_round_sequence": exact_rounds,
            "distinct_round_dates": distinct_dates,
            "round_structure_unique_date_effort_area": round_structure_ok,
            "partner_count": len(partners),
            "nonconstant_partner_series_after_effort_standardization": nonconstant,
            "all_six_rounds_have_positive_interactions": all_rounds_positive,
            "coordinate_variants": sorted({coord for rec in round_rows for coord in rec["coordinates"]}),
            "rounds": round_summaries,
            "decision": "ADMIT_STRUCTURE_BEFORE_COORDINATES" if admission else "FAIL_STRUCTURE",
        })

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_ireland_mullen_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "repository": SOURCE_REPO,
            "tag": TAG,
            "embedded_study": "35_Mullen / Sarah Mullen",
            "raw_git_blob_sha": RAW_BLOB_SHA,
            "processing_script_git_blob_sha": PROCESSING_BLOB_SHA,
            "raw_url": RAW_URL,
            "raw_sha256": hashlib.sha256(payload).hexdigest(),
            "encoding": encoding,
            "country": "Ireland",
            "sampling_method": "Transect",
            "processing_note": "The source-processing script explicitly preserves Sampling_effort_minutes for later effort calculation before dropping it from the harmonized EuPPollNet table.",
        },
        "source_rows_for_embedded_study": source_rows,
        "site_id_parse_failures": sorted(set(parse_failures)),
        "systems": systems,
        "admitted_system_ids_before_coordinates": admitted,
        "admitted_system_count_before_coordinates": len(admitted),
        "coordinates_opened": False,
        "decision": "ADMIT_SOURCE_STRUCTURE_BEFORE_COORDINATES" if admitted and len(admitted) == len(systems) else "PARTIAL_OR_FAILED_SOURCE_STRUCTURE",
        "claim_boundary": (
            "This audit uses only the pinned raw study rows and source-native Site_id round suffixes, dates, effort, area, partner identities and interaction counts. "
            "It does not compute Hill D1, synchrony phi, route thresholds, or any response variable. A stable farm is admitted only when rounds 1-6 are all explicitly represented, each round has one date and one positive effort value, and at least three effort-standardized partner series are nonconstant."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_rows": source_rows,
        "system_count": len(systems),
        "admitted_system_count": len(admitted),
        "admitted_system_ids": admitted,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
