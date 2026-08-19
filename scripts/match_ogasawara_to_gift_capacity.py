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


def finite_positive(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


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
                "distance_to_mainland_km": joined.get("dist"),
                "latitude": joined.get("latitude"),
                "longitude": joined.get("longitude"),
            }
        )

    matches = []
    for target in design["targets"]:
        aliases = target["aliases"]
        candidates = []
        for island in islands:
            score = alias_score(island["geo_entity"], aliases)
            if score > 0:
                candidates.append({**island, "alias_score": score})
        candidates.sort(key=lambda row: (-row["alias_score"], str(row["geo_entity"])))
        best_score = candidates[0]["alias_score"] if candidates else 0
        best = [row for row in candidates if row["alias_score"] == best_score]
        locked = len(best) == 1 and best_score in (100, 40)
        selected = best[0] if locked else None
        matches.append(
            {
                **target,
                "locked": locked,
                "lock_reason": (
                    "unique_exact_normalized_alias" if locked and best_score == 100
                    else "unique_alias_substring" if locked
                    else "unresolved_or_ambiguous"
                ),
                "selected": selected,
                "candidates": candidates[:12],
            }
        )

    payload = {
        "schema_version": "1.0",
        "analysis": "ogasawara_gift_capacity_geography_match",
        "gift_version": "3.2",
        "target_count": len(matches),
        "locked_count": sum(row["locked"] for row in matches),
        "all_locked": all(row["locked"] for row in matches),
        "matches": matches,
        "lock_rule": design["lock_rule"],
        "claim_boundary": design["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "all_locked": payload["all_locked"],
        "locked_count": payload["locked_count"],
        "matches": [
            {
                "source_island": row["source_island"],
                "locked": row["locked"],
                "selected": row["selected"],
            }
            for row in matches
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
