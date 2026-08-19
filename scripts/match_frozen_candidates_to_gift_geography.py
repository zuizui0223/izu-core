from __future__ import annotations

import json
import math
import re
import unicodedata
import urllib.request
from pathlib import Path

API = "https://gift.uni-goettingen.de/api/extended/index3.2.php"
DORE = Path("data/design/frozen_dore_candidate_network_locations.json")
OUT = Path("data/results/frozen_candidate_gift_geography_match.json")

IZU_TARGETS = [
    {"system": "Izu archipelago", "target": "Oshima", "aliases": ["Izu Oshima", "Oshima Island", "Oshima"]},
    {"system": "Izu archipelago", "target": "Niijima", "aliases": ["Niijima", "Nii-jima"]},
    {"system": "Izu archipelago", "target": "Kozushima", "aliases": ["Kozushima", "Kozu-shima", "Kozu"]},
    {"system": "Izu archipelago", "target": "Miyakejima", "aliases": ["Miyakejima", "Miyake-jima", "Miyake"]},
    {"system": "Izu archipelago", "target": "Hachijojima", "aliases": ["Hachijojima", "Hachijo-jima", "Hachijo"]},
]
YONGXING_TARGET = {
    "system": "Yongxing / Xisha",
    "target": "Yongxing",
    "aliases": ["Yongxing", "Woody Island", "Yongxing Island", "Xisha"],
}


def get_json(url: str, timeout: int = 120):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(x: str | None) -> str:
    s = unicodedata.normalize("NFKD", str(x or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def haversine_km(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 6371.0088 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def score_name(target_text: str, entity: str) -> int:
    t, e = norm(target_text), norm(entity)
    score = 0
    for tok in set(t.split()):
        if len(tok) >= 4 and tok in e:
            score += 2
    if t and t in e:
        score += 10
    return score


def main() -> None:
    regions = get_json(API + "?query=regions")
    misc = get_json(API + "?query=geoentities_env_misc&envvar=longitude,latitude,area,dist")
    elev = get_json(API + "?query=geoentities_env_raster&layername=mx30_grd&sumstat=max")

    reg = {str(r.get("entity_ID")): r for r in regions}
    env = {}
    for r in misc:
        env[str(r.get("entity_ID"))] = dict(r)
    for r in elev:
        env.setdefault(str(r.get("entity_ID")), {}).update(r)

    islands = []
    for eid, r in reg.items():
        klass = str(r.get("entity_class", ""))
        if "Island" not in klass:
            continue
        x = {**r, **env.get(eid, {})}
        try:
            lat = float(x.get("latitude")); lon = float(x.get("longitude"))
        except (TypeError, ValueError):
            continue
        x["latitude"] = lat; x["longitude"] = lon
        islands.append(x)

    dore = json.loads(DORE.read_text())
    targets = []
    for r in dore["rows"]:
        targets.append({
            "kind": "dore_network_location",
            "system": r["system"],
            "target": r.get("location") or r.get("country_location") or r.get("region_pub"),
            "latitude": float(r["latitude"]),
            "longitude": float(r["longitude"]),
            "source_reference": r.get("reference_id"),
            "region_pub": r.get("region_pub"),
        })
    targets.extend({"kind": "name_only_izu", **x} for x in IZU_TARGETS)
    targets.append({"kind": "name_only_yongxing", **YONGXING_TARGET})

    matches = []
    for t in targets:
        ranked = []
        for x in islands:
            entity = str(x.get("geo_entity") or x.get("geo_entity_ref") or "")
            ns = max(score_name(a, entity) for a in t.get("aliases", [t["target"]]))
            distance = None
            if "latitude" in t:
                distance = haversine_km(t["latitude"], t["longitude"], x["latitude"], x["longitude"])
            combined = ns * 1000 - (distance if distance is not None else 500)
            ranked.append((combined, ns, distance, x))
        ranked.sort(key=lambda z: z[0], reverse=True)
        candidates = []
        for _, ns, distance, x in ranked[:8]:
            candidates.append({
                "entity_ID": x.get("entity_ID"),
                "geo_entity": x.get("geo_entity") or x.get("geo_entity_ref"),
                "entity_class": x.get("entity_class"),
                "name_score": ns,
                "coordinate_distance_km": distance,
                "longitude": x.get("longitude"),
                "latitude": x.get("latitude"),
                "area_km2": x.get("area"),
                "distance_to_mainland_km": x.get("dist"),
                "max_elevation_m": x.get("max_mx30_grd") if "max_mx30_grd" in x else x.get("max"),
            })
        top = candidates[0] if candidates else None
        auto_lock = bool(top and top["name_score"] >= 2 and (top["coordinate_distance_km"] is None or top["coordinate_distance_km"] <= 120))
        matches.append({**t, "auto_lock": auto_lock, "top_candidates": candidates})

    payload = {
        "analysis": "frozen_candidate_gift_geography_match",
        "gift_version": "3.2",
        "n_region_rows": len(regions),
        "n_island_entities_with_coordinates": len(islands),
        "n_targets": len(targets),
        "n_auto_locked": sum(x["auto_lock"] for x in matches),
        "matches": matches,
        "admission_rule": "Only auto-lock strong name matches with <=120 km coordinate discrepancy; all other cases remain manual/name-source gated. No network outcome is used.",
        "next_gate": "Review non-locked name/coordinate cases, freeze one entity_ID per actual island, then convert dist/area/max elevation to ABM input without using network response metrics.",
        "claim_boundary": "This is geography matching only. A GIFT polygon may be an island group/part rather than the exact sampled island; ambiguous matches are deliberately not admitted automatically.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
