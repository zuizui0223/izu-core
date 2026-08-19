from __future__ import annotations

import csv
import json
import math
import re
import unicodedata
import urllib.request
from bisect import bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://gift.uni-goettingen.de/api/extended/index3.2.php"
DESIGN = ROOT / "data/design/abm_v5_aride_seasonal_validation_v1.json"
REFERENCE = ROOT / "data/results/frozen_candidate_gift_geography_match.json"
TARGETS = ROOT / "data/results/frozen_dore_network_targets.csv"
OUT = ROOT / "data/results/aride2026_gift_opportunity_lock.json"


def get_json(url: str, timeout: int = 120):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def norm(value: str | None) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = text.encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def num(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0088 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def alias_score(entity: str) -> int:
    e = norm(entity)
    aliases = [norm("Aride"), norm("Aride Island")]
    score = 0
    for alias in aliases:
        if e == alias:
            score = max(score, 100)
        elif alias in e or e in alias:
            score = max(score, 40)
    return score


def frozen_reference_distances() -> list[float]:
    geography = json.loads(REFERENCE.read_text())
    with TARGETS.open(newline="", encoding="utf-8") as handle:
        target_ids = {row["region_pub"] for row in csv.DictReader(handle)}
    values = []
    used = set()
    for match in geography["matches"]:
        region = match.get("region_pub")
        if match.get("kind") != "dore_network_location" or region not in target_ids:
            continue
        if not match.get("auto_lock"):
            continue
        candidates = match.get("top_candidates") or []
        if not candidates:
            continue
        distance = num(candidates[0].get("distance_to_mainland_km"))
        if distance is None:
            continue
        values.append(distance)
        used.add(region)
    if len(used) < 20:
        raise RuntimeError(f"unexpectedly small frozen v4 reference geography: {len(used)} rows")
    unique = sorted(set(values))
    if len(unique) < 2:
        raise RuntimeError("frozen v4 distance reference has fewer than two unique distances")
    return unique


def frozen_ecdf_interpolate(distance: float, reference: list[float]) -> float:
    if distance <= reference[0]:
        return 0.0
    if distance >= reference[-1]:
        return 1.0
    hi = bisect_right(reference, distance)
    lo = hi - 1
    x0, x1 = reference[lo], reference[hi]
    fraction = (distance - x0) / (x1 - x0)
    return (lo + fraction) / (len(reference) - 1)


def main() -> None:
    design = json.loads(DESIGN.read_text())
    coords = design["held_out_system"]["coordinates"]
    target_lat = float(coords["latitude"])
    target_lon = float(coords["longitude"])
    regions = get_json(API + "?query=regions")
    misc = get_json(API + "?query=geoentities_env_misc&envvar=longitude,latitude,area,dist")
    env = {str(row.get("entity_ID")): row for row in misc}
    candidates = []
    for row in regions:
        if "Island" not in str(row.get("entity_class", "")):
            continue
        joined = {**row, **env.get(str(row.get("entity_ID")), {})}
        lat, lon = num(joined.get("latitude")), num(joined.get("longitude"))
        if lat is None or lon is None:
            continue
        entity = str(row.get("geo_entity") or row.get("geo_entity_ref") or "")
        score = alias_score(entity)
        if score <= 0:
            continue
        candidates.append({
            "entity_ID": row.get("entity_ID"),
            "geo_entity": entity,
            "entity_class": row.get("entity_class"),
            "alias_score": score,
            "coordinate_distance_km": haversine_km(target_lat, target_lon, lat, lon),
            "latitude": lat,
            "longitude": lon,
            "area_km2": num(joined.get("area")),
            "distance_to_mainland_km": num(joined.get("dist")),
        })
    candidates.sort(key=lambda row: (-row["alias_score"], row["coordinate_distance_km"]))
    valid = [
        row for row in candidates
        if row["alias_score"] >= 40
        and row["coordinate_distance_km"] <= 20
        and row["distance_to_mainland_km"] is not None
    ]
    locked = len(valid) == 1
    selected = valid[0] if locked else None
    if selected is None:
        payload = {
            "schema_version": "1.0",
            "analysis": "aride2026_gift_opportunity_lock",
            "status": "blocked_no_unique_aride_gift_match",
            "target_coordinates": coords,
            "candidates": candidates[:20],
            "claim_boundary": "No network metric or ABM fit was used. Biological validation is blocked until Aride GIFT distance is uniquely resolved from geography only.",
        }
    else:
        reference = frozen_reference_distances()
        z = frozen_ecdf_interpolate(float(selected["distance_to_mainland_km"]), reference)
        payload = {
            "schema_version": "1.0",
            "analysis": "aride2026_gift_opportunity_lock",
            "status": "locked",
            "gift_version": "3.2",
            "target_coordinates": coords,
            "selected": selected,
            "candidate_count": len(candidates),
            "reference_unique_distance_count": len(reference),
            "reference_distance_min_km": reference[0],
            "reference_distance_max_km": reference[-1],
            "held_out_inserted_into_reference_ecdf": False,
            "distance_ecdf_interpolation_rule": design["island_opportunity_input"]["held_out_ecdf_extension"],
            "isolation_index": z,
            "claim_boundary": "This is outcome-blind geography mapping. The held-out Aride distance is projected onto the frozen v4 opportunity axis without changing the frozen reference ECDF.",
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
