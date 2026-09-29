from __future__ import annotations

import json
import math
import re
import unicodedata
import urllib.request
from bisect import bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://gift.uni-goettingen.de/api/extended/index3.2.php"
DESIGN = ROOT / "data/design/abm_v5_menorca_nine_local_validation_v1.json"
REFERENCE = ROOT / "data/results/abm_v4_distance_ecdf_reference_runlock.json"
OUT = ROOT / "data/results/menorca2023_gift_opportunity_lock.json"


def get_json(url: str, timeout: int = 120):
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def norm(value: str | None) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = text.encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def number(value):
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def frozen_reference_distances() -> tuple[list[float], dict]:
    runlock = json.loads(REFERENCE.read_text())
    if runlock.get("source_pr") != 183:
        raise RuntimeError("distance-ECDF runlock is not the PR #183 frozen reference")
    if runlock.get("source_artifact_sha256") != "0de50c6cb3704a012a0653dffd3a8f7fea8ceac233b33a66d728a3732dd6b919":
        raise RuntimeError("distance-ECDF runlock artifact digest drifted")
    values = [float(value) for value in runlock["unique_distance_to_mainland_km"]]
    if values != sorted(set(values)):
        raise RuntimeError("frozen reference distances must be unique and sorted")
    if len(values) != int(runlock["frozen_unique_distance_count"]):
        raise RuntimeError("frozen reference distance count drifted")
    if len(values) < 2:
        raise RuntimeError("frozen v4 distance reference has fewer than two unique distances")
    return values, runlock


def frozen_ecdf_interpolate(distance: float, reference: list[float]) -> float:
    if distance <= reference[0]:
        return 0.0
    if distance >= reference[-1]:
        return 1.0
    hi = bisect_right(reference, distance)
    lo = hi - 1
    left, right = reference[lo], reference[hi]
    fraction = (distance - left) / (right - left)
    return (lo + fraction) / (len(reference) - 1)


def main() -> None:
    design = json.loads(DESIGN.read_text())
    expected_name = norm(design["held_out_system"]["island"])
    regions = get_json(API + "?query=regions")
    misc = get_json(API + "?query=geoentities_env_misc&envvar=longitude,latitude,area,dist")
    env = {str(row.get("entity_ID")): row for row in misc}

    exact = []
    for row in regions:
        if "Island" not in str(row.get("entity_class", "")):
            continue
        entity = str(row.get("geo_entity") or row.get("geo_entity_ref") or "")
        if norm(entity) != expected_name:
            continue
        joined = {**row, **env.get(str(row.get("entity_ID")), {})}
        distance = number(joined.get("dist"))
        exact.append({
            "entity_ID": row.get("entity_ID"),
            "geo_entity": entity,
            "entity_class": row.get("entity_class"),
            "latitude": number(joined.get("latitude")),
            "longitude": number(joined.get("longitude")),
            "area_km2": number(joined.get("area")),
            "distance_to_mainland_km": distance,
        })

    valid = [row for row in exact if row["distance_to_mainland_km"] is not None]
    if len(valid) != 1:
        payload = {
            "schema_version": "1.1",
            "analysis": "menorca2023_gift_opportunity_lock",
            "status": "blocked_no_unique_exact_menorca_gift_match",
            "exact_name_candidates": exact,
            "network_outcomes_used": False,
            "reference_source": str(REFERENCE),
            "claim_boundary": "No Menorca network metric or published turnover result was used. Validation is blocked until exactly one GIFT Island entity named Menorca with mainland distance is available.",
        }
    else:
        selected = valid[0]
        reference, runlock = frozen_reference_distances()
        isolation_index = frozen_ecdf_interpolate(
            float(selected["distance_to_mainland_km"]), reference
        )
        payload = {
            "schema_version": "1.1",
            "analysis": "menorca2023_gift_opportunity_lock",
            "status": "locked",
            "gift_version_for_heldout_menorca": "3.2",
            "selected": selected,
            "exact_name_candidate_count": len(exact),
            "reference_source": str(REFERENCE),
            "reference_source_pr": runlock["source_pr"],
            "reference_source_workflow_run": runlock["source_workflow_run"],
            "reference_source_artifact_id": runlock["source_artifact_id"],
            "reference_source_artifact_sha256": runlock["source_artifact_sha256"],
            "reference_unique_distance_count": len(reference),
            "reference_distance_min_km": reference[0],
            "reference_distance_max_km": reference[-1],
            "held_out_inserted_into_reference_ecdf": False,
            "distance_ecdf_interpolation_rule": design["island_opportunity_input"]["held_out_ecdf_extension"],
            "isolation_index": isolation_index,
            "network_outcomes_used": False,
            "claim_boundary": "Outcome-blind geography lock. The current GIFT Menorca distance is projected onto the exact PR #183 frozen v4 mainland-distance reference recovered from its source-locked artifact; the reference distribution is not recomputed or modified.",
        }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
