from __future__ import annotations

import json
import math
import re
import unicodedata
import urllib.request
from pathlib import Path

API = "https://gift.uni-goettingen.de/api/extended/index3.2.php"
DORE = Path("data/design/frozen_dore_candidate_network_locations.json")
IZU_POINTS = Path("configs/izu_island_proxy_points.json")
OUT = Path("data/results/frozen_candidate_gift_geography_match.json")

# Frozen before named-system ABM fit; aliases are geography/name disambiguators only.
REGION_ALIASES = {
    "RP4": ["Tenerife"],
    "RP17": ["Ile aux Aigrettes", "Ile aux Aigrettes Mauritius"],
    "RP18": ["Flores", "Flores Azores"],
    "RP36": ["Mauritius", "Mauritius Island"],
    "RP42": ["Mahe", "Mahe Island"],
    "RP47": ["Oahu", "O'ahu"],
    "RP100": ["El Hierro"],
    "RP101": ["La Gomera", "Gomera"],
    "RP102": ["Gran Canaria"],
    "RP103": ["Fuerteventura"],
    "RP154": ["Fernandina", "Fernandina Galapagos"],
    "RP155": ["Pinta", "Pinta Galapagos"],
    "RP156": ["Santiago Galapagos", "Santiago"],
    "RP157": ["Santa Cruz Galapagos", "Santa Cruz"],
    "RP158": ["San Cristobal", "San Cristobal Galapagos"],
    "RP160": ["Lanzarote"],
    "RP163": ["Hawaii Island", "Island of Hawaii", "Hawai'i", "Hawaii"],
    "RP164": ["Tenerife"],
    "RP197": ["Lanzarote"],
    "RP207": ["Terceira"],
    "RP208": ["Terceira"],
    "RP209": ["Terceira"],
    "RP210": ["Terceira"],
    "RP211": ["Terceira"],
    "RP222": ["Tenerife"],
    "RP225": ["Tenerife"],
}
IZU_ALIASES = {
    "Oshima": ["Izu Oshima", "Izu-Oshima", "O-shima", "Oshima"],
    "Niijima": ["Niijima", "Nii-jima"],
    "Kozushima": ["Kozushima", "Kozu-shima", "Kozu"],
    "Miyake": ["Miyakejima", "Miyake-jima", "Miyake"],
    "Hachijo": ["Hachijojima", "Hachijo-jima", "Hachijo"],
}
YONGXING_TARGET = {
    "kind": "coordinate_yongxing",
    "system": "Yongxing / Xisha",
    "target": "Yongxing Island",
    "aliases": ["Yongxing", "Yongxing Island", "Woody Island"],
    "latitude": 16 + 49/60,
    "longitude": 112 + 20/60,
    "coordinate_source": "Wang et al. 2025 Biotropica / Dryad study-site metadata",
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


def alias_score(aliases: list[str], entity: str) -> int:
    e = norm(entity)
    score = 0
    for alias in aliases:
        a = norm(alias)
        if not a:
            continue
        if e == a:
            score = max(score, 100)
        elif a in e or e in a:
            score = max(score, 40)
        else:
            atoks = {t for t in a.split() if len(t) >= 4}
            etoks = set(e.split())
            overlap = len(atoks & etoks)
            score = max(score, overlap * 5)
    return score


def numeric_or_none(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


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
        lat, lon = numeric_or_none(x.get("latitude")), numeric_or_none(x.get("longitude"))
        if lat is None or lon is None:
            continue
        x["latitude"], x["longitude"] = lat, lon
        islands.append(x)

    targets = []
    dore = json.loads(DORE.read_text())
    for r in dore["rows"]:
        aliases = REGION_ALIASES.get(r["region_pub"], [])
        targets.append({
            "kind": "dore_network_location",
            "system": r["system"],
            "target": r.get("location") or r.get("country_location") or r.get("region_pub"),
            "aliases": aliases,
            "latitude": float(r["latitude"]),
            "longitude": float(r["longitude"]),
            "source_reference": r.get("reference_id"),
            "region_pub": r.get("region_pub"),
        })

    izu = json.loads(IZU_POINTS.read_text())
    for p in izu["points"]:
        if p["island_id"] not in IZU_ALIASES:
            continue
        targets.append({
            "kind": "coordinate_izu",
            "system": "Izu archipelago",
            "target": p["island_id"],
            "aliases": IZU_ALIASES[p["island_id"]],
            "latitude": float(p["latitude"]),
            "longitude": float(p["longitude"]),
            "coordinate_source": "configs/izu_island_proxy_points.json",
        })
    targets.append(YONGXING_TARGET)

    matches = []
    for t in targets:
        ranked = []
        for x in islands:
            entity = str(x.get("geo_entity") or x.get("geo_entity_ref") or "")
            ns = alias_score(t.get("aliases", []), entity)
            distance = haversine_km(t["latitude"], t["longitude"], x["latitude"], x["longitude"])
            # Primary ordering is coordinate distance; aliases decide whether a close island can be locked.
            ranked.append((distance, -ns, x, ns))
        ranked.sort(key=lambda z: (z[0], z[1]))
        candidates = []
        for distance, _, x, ns in ranked[:12]:
            candidates.append({
                "entity_ID": x.get("entity_ID"),
                "geo_entity": x.get("geo_entity") or x.get("geo_entity_ref"),
                "entity_class": x.get("entity_class"),
                "alias_score": ns,
                "coordinate_distance_km": distance,
                "longitude": x.get("longitude"),
                "latitude": x.get("latitude"),
                "area_km2": numeric_or_none(x.get("area")),
                "distance_to_mainland_km": numeric_or_none(x.get("dist")),
                "max_elevation_m": numeric_or_none(x.get("max_mx30_grd") if "max_mx30_grd" in x else x.get("max")),
            })
        top = candidates[0] if candidates else None
        # Exact/substring alias + geographically plausible centroid is required.
        # Extremely close coordinate matches (<=10 km) may lock despite naming differences, useful for translated/local aliases.
        auto_lock = bool(top and ((top["alias_score"] >= 40 and top["coordinate_distance_km"] <= 80) or top["coordinate_distance_km"] <= 10))
        matches.append({**t, "auto_lock": auto_lock, "top_candidates": candidates})

    payload = {
        "analysis": "frozen_candidate_gift_geography_match",
        "gift_version": "3.2",
        "n_region_rows": len(regions),
        "n_island_entities_with_coordinates": len(islands),
        "n_targets": len(targets),
        "n_auto_locked": sum(x["auto_lock"] for x in matches),
        "matches": matches,
        "admission_rule": "Rank by geographic proximity. Auto-lock only when the nearest GIFT island is <=80 km and has exact/substring agreement with a preregistered explicit island alias (alias_score>=40), or is <=10 km from the source coordinate. Generic archipelago substring matches are not sufficient. No network outcome is used.",
        "next_gate": "Review non-locked cases only from names/coordinates; freeze one GIFT entity_ID per actual sampled island. Yongxing may remain source-native-only if GIFT has no corresponding island entity. Then run the preregistered distance-ECDF ABM prediction without replacing systems or selecting saturation post hoc.",
        "claim_boundary": "This is geography matching only. Ambiguous island-group/part matches are deliberately left unlocked. Source-native geography may be retained as a declared exception only when definitions are not silently treated as GIFT-equivalent.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
