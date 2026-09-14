from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_petanidou_aegean_natural_regime_source_audit_20260915.json"
SOURCE_REPO = "JoseBSL/EuPPollNet"
TAG = "v1.3.0"
INTERACTION_BLOB_SHA = "a068f2ffa63505a20d5bfed3abec3dab540bc622"
FLOWER_BLOB_SHA = "8b564cdd7d2f706469fb4a746a96bae016172353"
PROCESSING_SCRIPT_BLOB_SHA = "f3cc40599892705996979beb27f0b12e4e3d9d98"
INTERACTION_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/51_Petanidou/Interaction_data.csv"
FLOWER_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/51_Petanidou/Flower_count.csv"


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
    raise RuntimeError("Petanidou source could not be decoded losslessly")


def clean(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def date_key(row: dict[str, str]) -> str:
    day = clean(row.get("Day"))
    month = clean(row.get("Month"))
    year = clean(row.get("Year"))
    if not all((day, month, year)):
        return ""
    try:
        return f"{int(float(year)):04d}-{int(float(month)):02d}-{int(float(day)):02d}"
    except ValueError:
        return ""


def number(value: object) -> float | None:
    try:
        x = float(str(value or "").strip())
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def main() -> None:
    interaction_bytes = get_bytes(INTERACTION_URL)
    flower_bytes = get_bytes(FLOWER_URL)
    interaction_text, interaction_encoding = decode(interaction_bytes)
    flower_text, flower_encoding = decode(flower_bytes)
    interactions = list(csv.DictReader(io.StringIO(interaction_text)))
    flowers = list(csv.DictReader(io.StringIO(flower_text)))

    by_site: dict[str, dict] = {}
    for row in interactions:
        site = clean(row.get("Site_id"))
        if not site:
            continue
        rec = by_site.setdefault(site, {
            "localities": set(),
            "coordinates": set(),
            "interaction_dates": set(),
            "flower_dates": set(),
            "methods": set(),
            "effort_minutes": set(),
            "areas_m2": set(),
            "partners": set(),
            "events": Counter(),
        })
        locality = clean(row.get("Locality"))
        lat, lon = clean(row.get("Latitude")), clean(row.get("Longitude"))
        if locality:
            rec["localities"].add(locality)
        if lat and lon:
            rec["coordinates"].add((lat, lon))
        date = date_key(row)
        if date:
            rec["interaction_dates"].add(date)
        method = clean(row.get("Sampling_method"))
        if method:
            rec["methods"].add(method)
        effort = number(row.get("Sampling_effort_minutes"))
        area = number(row.get("Sampling_area_square_meters"))
        if effort is not None:
            rec["effort_minutes"].add(effort)
        if area is not None:
            rec["areas_m2"].add(area)
        partner = clean(row.get("Pollinator_species"))
        count = number(row.get("Interaction"))
        if partner:
            rec["partners"].add(partner)
            if date and count is not None and count >= 0:
                rec["events"][(date, partner)] += count

    for row in flowers:
        site = clean(row.get("Site_id"))
        if not site:
            continue
        rec = by_site.setdefault(site, {
            "localities": set(), "coordinates": set(), "interaction_dates": set(), "flower_dates": set(),
            "methods": set(), "effort_minutes": set(), "areas_m2": set(), "partners": set(), "events": Counter(),
        })
        date = date_key(row)
        if date:
            rec["flower_dates"].add(date)

    systems = []
    for site in sorted(by_site):
        rec = by_site[site]
        interaction_dates = sorted(rec["interaction_dates"])
        flower_dates = sorted(rec["flower_dates"])
        field_dates = flower_dates if flower_dates else interaction_dates
        partners = sorted(rec["partners"])
        nonconstant_interaction_dates = 0
        nonconstant_field_dates = 0
        for partner in partners:
            x = [float(rec["events"].get((day, partner), 0.0)) for day in interaction_dates]
            if len(set(x)) > 1:
                nonconstant_interaction_dates += 1
            y = [float(rec["events"].get((day, partner), 0.0)) for day in field_dates]
            if len(set(y)) > 1:
                nonconstant_field_dates += 1
        interaction_subset_flower = bool(interaction_dates) and set(interaction_dates).issubset(set(flower_dates))
        flower_only = sorted(set(flower_dates) - set(interaction_dates))
        systems.append({
            "system_id": site,
            "localities": sorted(rec["localities"]),
            "coordinates": [list(value) for value in sorted(rec["coordinates"])],
            "interaction_dates": len(interaction_dates),
            "flower_count_dates": len(flower_dates),
            "field_date_rule_candidate": "flower_count_dates_if_source_protocol_confirms_same_visit_schedule_else_unresolved",
            "interaction_dates_subset_of_flower_dates": interaction_subset_flower,
            "flower_only_dates": len(flower_only),
            "flower_only_dates_preview": flower_only[:12],
            "date_min": min(field_dates) if field_dates else None,
            "date_max": max(field_dates) if field_dates else None,
            "sampling_methods": sorted(rec["methods"]),
            "sampling_effort_minutes_values": sorted(rec["effort_minutes"]),
            "sampling_area_m2_values": sorted(rec["areas_m2"]),
            "partner_count": len(partners),
            "nonconstant_partner_series_on_interaction_dates": nonconstant_interaction_dates,
            "nonconstant_partner_series_on_field_dates": nonconstant_field_dates,
            "six_bin_floor_pass_on_interaction_dates": len(interaction_dates) >= 6,
            "six_bin_floor_pass_on_flower_dates": len(flower_dates) >= 6,
            "three_series_floor_pass_on_interaction_dates": nonconstant_interaction_dates >= 3,
            "three_series_floor_pass_on_field_dates": nonconstant_field_dates >= 3,
            "effort_constant_in_interaction_rows": rec["effort_minutes"] == {120.0},
            "area_constant_in_interaction_rows": rec["areas_m2"] == {4000.0},
        })

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_petanidou_aegean_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "repository": SOURCE_REPO,
            "tag": TAG,
            "dataset_id": "51_Petanidou",
            "interaction_git_blob_sha": INTERACTION_BLOB_SHA,
            "flower_git_blob_sha": FLOWER_BLOB_SHA,
            "processing_script_git_blob_sha": PROCESSING_SCRIPT_BLOB_SHA,
            "interaction_url": INTERACTION_URL,
            "flower_url": FLOWER_URL,
            "interaction_sha256": hashlib.sha256(interaction_bytes).hexdigest(),
            "flower_sha256": hashlib.sha256(flower_bytes).hexdigest(),
            "interaction_encoding": interaction_encoding,
            "flower_encoding": flower_encoding,
            "source_metadata_description": "9 different sites within 7 islands in the Aegean",
            "raw_interaction_effort_columns": ["Sampling_effort_minutes", "Sampling_area_square_meters"],
        },
        "source_rows": {"interactions": len(interactions), "flower_counts": len(flowers)},
        "systems": systems,
        "structural_pass_using_positive_interaction_dates_only": [
            row["system_id"] for row in systems
            if row["six_bin_floor_pass_on_interaction_dates"] and row["three_series_floor_pass_on_interaction_dates"]
            and row["effort_constant_in_interaction_rows"] and row["area_constant_in_interaction_rows"]
        ],
        "structural_pass_if_flower_dates_are_confirmed_as_same_interaction_visit_schedule": [
            row["system_id"] for row in systems
            if row["six_bin_floor_pass_on_flower_dates"] and row["three_series_floor_pass_on_field_dates"]
            and row["effort_constant_in_interaction_rows"] and row["area_constant_in_interaction_rows"]
        ],
        "coordinates_opened": False,
        "decision": "REQUIRE_SOURCE_PROTOCOL_CONFIRMATION_FOR_ZERO_INTERACTION_FIELD_DATES_BEFORE_FREEZE",
        "claim_boundary": (
            "This audit opens source structure only. It never selects dates because of D1, phi, response or route values. "
            "Positive-interaction dates are reported but are not automatically accepted as the sampling frame because that would condition time-bin inclusion on observing an interaction. "
            "Flower-count dates are evaluated only as a candidate outcome-independent visit schedule; they are not promoted to interaction-zero bins until the source protocol confirms that floral counts and interaction random walks share the same field visits."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "systems": len(systems),
        "positive_date_pass": result["structural_pass_using_positive_interaction_dates_only"],
        "flower_date_candidate_pass": result["structural_pass_if_flower_dates_are_confirmed_as_same_interaction_visit_schedule"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
