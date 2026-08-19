from __future__ import annotations

import csv
import io
import json
import math
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

URL = "https://www.web-of-life.es/get_network_info.php"
OUT = Path("data/results/weboflife_global_pollination_coverage.json")


def fetch_text(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def to_float(x: str):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def build_audit(text: str) -> dict:
    rows = list(csv.DictReader(io.StringIO(text)))
    poll = [r for r in rows if (r.get("network_name") or "").startswith("M_PL_")]
    weighted = [r for r in poll if str(r.get("is_weighted", "")).strip().lower() in {"1", "true", "yes"}]
    lats = [to_float(r.get("latitude", "")) for r in weighted]
    lons = [to_float(r.get("longitude", "")) for r in weighted]
    lats = [x for x in lats if x is not None]
    lons = [x for x in lons if x is not None]
    countries = Counter((r.get("country") or "unknown").strip() or "unknown" for r in weighted)
    refs = Counter((r.get("reference") or "unknown").strip() or "unknown" for r in weighted)
    locations = [
        {
            "network_name": r.get("network_name"),
            "location": r.get("location"),
            "country": r.get("country"),
            "latitude": to_float(r.get("latitude", "")),
            "longitude": to_float(r.get("longitude", "")),
            "reference": r.get("reference"),
        }
        for r in weighted
    ]
    return {
        "source": "Web of Life",
        "endpoint": URL,
        "status": "metadata_audit_not_traveset_membership_reconstruction",
        "all_network_metadata_rows": len(rows),
        "pollination_network_rows": len(poll),
        "weighted_pollination_network_rows": len(weighted),
        "weighted_latitude_range": [min(lats), max(lats)] if lats else None,
        "weighted_longitude_range": [min(lons), max(lons)] if lons else None,
        "countries": dict(countries.most_common()),
        "unique_references": len(refs),
        "locations": locations,
        "claim_boundary": "This audit describes the current Web of Life metadata pool. It does not identify the exact 18 oceanic-island networks used by Traveset et al. 2016 and must not be used to back-select a convenient replacement set."
    }


def main():
    try:
        text = fetch_text(URL)
        payload = build_audit(text)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        payload = {
            "source": "Web of Life",
            "endpoint": URL,
            "status": "blocked_source_retrieval",
            "error": repr(exc),
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
