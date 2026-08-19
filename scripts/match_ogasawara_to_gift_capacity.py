from __future__ import annotations

import json
import math
import re
import unicodedata
import urllib.request
from pathlib import Path

API = "https://gift.uni-goettingen.de/api/extended/index3.2.php"
TARGETS = Path("data/design/ogasawara_gift_capacity_targets_v1.json")
OUT = Path("data/results/ogasawara_gift_capacity_match.json")


def get_json(url: str, timeout: int = 120):
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def norm(value: str | None) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = text.encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def finite_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def finite_positive(value):
    number = finite_number(value)
    return number if number is not None and number > 0 else None


def alias_score(entity: str, aliases: list[str]) -> int:
    entity_norm = norm(entity)
    best = 0
    for alias in aliases:
        alias_norm = norm(alias)
        if not alias_norm:
            continue
        if entity_norm == alias_norm:
            best = max(best, 100)
        elif alias_norm in entity_norm or entity_norm in alias_norm:
            best = max(best, 40)
    return best


def inside_frozen_bbox(candidate: dict, target: dict) -> bool:
    gate = target.get("gsi_map_sheet_gate")
    if not gate:
        return True
    lat = finite_number(candidate.get("latitude"))
    lon = finite_number(candidate.get("longitude"))
    if lat is None or lon is None:
        return False
    return (
        float(gate["latitude_min"]) <= lat <= float(gate["latitude_max"])
        and float(gate["longitude_min"]) <= lon <= float(gate["longitude_max"])
    )


def audit_candidate(island: dict, target: dict) -> dict | None:
    score = alias_score(island["geo_entity"], target["aliases"])
    if score <= 0:
        return None
    gsi_area = float(target["gsi_area_km2"])
    relative_error = abs(float(island["area_km2"]) - gsi_area) / gsi_area
    area_ok = relative_error <= float(target["gift_area_relative_tolerance"])
    bbox_ok = inside_frozen_bbox(island, target)
    return {
        **island,
        "alias_score": score,
        "gsi_area_km2": gsi_area,
        "area_relative_error_vs_gsi": relative_error,
        "area_plausible": area_ok,
        "frozen_bbox_plausible": bbox_ok,
        "audit_valid": bool(area_ok and bbox_ok),
    }


def main() -> None:
    design = json.loads(TARGETS.read_text())
    regions = get_json(API + "?query=regions")
    misc = get_json(API + "?query=geoentities_env_misc&envvar=longitude,latitude,area,dist")
    env = {str(row.get("entity_ID")): row for row in misc}

    islands = []
    for row in regions:
        if "Island" not in str(row.get("entity_class", "")):
            continue
        entity_id = str(row.get("entity_ID"))
        joined = {**row, **env.get(entity_id, {})}
        area = finite_positive(joined.get("area"))
        if area is None:
            continue
        islands.append(
            {
                "entity_ID": row.get("entity_ID"),
                "geo_entity": str(row.get("geo_entity") or row.get("geo_entity_ref") or ""),
                "entity_class": row.get("entity_class"),
                "area_km2": area,
                "distance_to_mainland_km": finite_number(joined.get("dist")),
                "latitude": finite_number(joined.get("latitude")),
                "longitude": finite_number(joined.get("longitude")),
            }
        )

    matches = []
    for target in design["targets"]:
        candidates = []
        for island in islands:
            audited = audit_candidate(island, target)
            if audited is not None:
                candidates.append(audited)
        candidates.sort(
            key=lambda row: (
                not row["audit_valid"],
                -row["alias_score"],
                row["area_relative_error_vs_gsi"],
                str(row["geo_entity"]),
            )
        )
        valid = [row for row in candidates if row["audit_valid"]]
        best_score = max((row["alias_score"] for row in valid), default=0)
        best = [row for row in valid if row["alias_score"] == best_score]
        locked = len(best) == 1 and best_score in (100, 40)
        selected = best[0] if locked else None
        matches.append(
            {
                **target,
                "gift_audit_locked": locked,
                "gift_audit_reason": (
                    "unique_geographically_plausible_exact_alias" if locked and best_score == 100
                    else "unique_geographically_plausible_alias_substring" if locked
                    else "no_unique_geographically_plausible_gift_entity"
                ),
                "gift_selected": selected,
                "gift_candidates": candidates[:12],
            }
        )

    payload = {
        "schema_version": "1.1",
        "analysis": "ogasawara_gift_capacity_cross_source_audit",
        "gift_version": "3.2",
        "primary_area_source": design["primary_area_source"],
        "target_count": len(matches),
        "gift_locked_count": sum(row["gift_audit_locked"] for row in matches),
        "all_gift_audits_locked": all(row["gift_audit_locked"] for row in matches),
        "matches": matches,
        "audit_rule": design["gift_audit_rule"],
        "claim_boundary": design["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "all_gift_audits_locked": payload["all_gift_audits_locked"],
        "gift_locked_count": payload["gift_locked_count"],
        "matches": [
            {
                "source_island": row["source_island"],
                "gift_audit_locked": row["gift_audit_locked"],
                "gift_selected": row["gift_selected"],
                "top_candidate": row["gift_candidates"][0] if row["gift_candidates"] else None,
            }
            for row in matches
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
