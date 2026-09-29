from __future__ import annotations

import json
import urllib.request
from pathlib import Path

API = "https://gift.uni-goettingen.de/api/extended/index3.2.php"
OUT = Path("data/results/gift_common_geography_fallback_audit.json")


def get_json(url: str, timeout: int = 60):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> None:
    payload = {
        "source": "GIFT stable API v3.2",
        "purpose": "Audit a public API fallback for common island geography after Dryad byte delivery is blocked; do not inspect any pollination-network outcome.",
        "api": API,
    }
    try:
        meta = get_json(API + "?query=env_misc")
        variables = []
        for row in meta:
            variable = str(row.get("variable", ""))
            desc = str(row.get("description", ""))
            dataset = str(row.get("dataset", ""))
            text = f"{variable} {desc} {dataset}".lower()
            if any(k in text for k in ("area", "dist", "isol", "elev", "longitude", "latitude", "mainland", "island", "geolog")):
                variables.append({
                    "dataset": row.get("dataset"),
                    "variable": row.get("variable"),
                    "description": row.get("description"),
                    "unit": row.get("unit"),
                    "num": row.get("num"),
                })
        payload["status"] = "metadata_recovered"
        payload["n_metadata_rows"] = len(meta)
        payload["candidate_geography_variables"] = variables
        names = {str(x.get("variable", "")).lower() for x in variables}
        payload["core_field_search"] = {
            "has_area_named_variable": any("area" in x for x in names),
            "has_distance_or_isolation_named_variable": any(("dist" in x or "isol" in x) for x in names),
            "has_elevation_named_variable": any("elev" in x for x in names),
            "has_longitude": "longitude" in names,
            "has_latitude": "latitude" in names,
        }
        payload["next_gate"] = "If the required variables are exposed, retrieve geoentities_env_misc and coordinate-match only the frozen candidate networks; otherwise retain Dryad/other source gate as blocked."
    except Exception as exc:
        payload["status"] = "metadata_query_failed"
        payload["error"] = repr(exc)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
