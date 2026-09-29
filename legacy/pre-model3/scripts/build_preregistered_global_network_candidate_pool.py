from __future__ import annotations

import argparse
import csv
import io
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

URL = "https://www.web-of-life.es/get_network_info.php"


def norm(x: str) -> str:
    return re.sub(r"\s+", " ", (x or "").strip()).casefold()


def fetch_text(url: str, timeout: int = 45) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def truthy(x: str) -> bool:
    return str(x or "").strip().casefold() in {"1", "true", "yes"}


def build_pool(text: str) -> dict:
    rows = list(csv.DictReader(io.StringIO(text)))
    weighted = [
        r for r in rows
        if (r.get("network_name") or "").startswith("M_PL_") and truthy(r.get("is_weighted", ""))
    ]
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in weighted:
        key = (norm(r.get("location", "")), norm(r.get("reference", "")))
        groups[key].append(r)

    programs = []
    for _, xs in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        first = xs[0]
        ids = sorted(r.get("network_name") for r in xs if r.get("network_name"))
        programs.append({
            "candidate_program_id": ids[0] if len(ids) == 1 else f"{ids[0]}__plus_{len(ids)-1}",
            "network_ids": ids,
            "n_network_rows": len(xs),
            "location": first.get("location"),
            "country": first.get("country"),
            "latitude": first.get("latitude"),
            "longitude": first.get("longitude"),
            "reference": first.get("reference"),
            "island_status": "unreviewed",
            "geological_origin": "unreviewed",
            "sampling_effort_status": "unreviewed",
            "admission_state": "pending_source_review"
        })

    return {
        "source": "Web of Life weighted pollination metadata",
        "raw_weighted_rows": len(weighted),
        "deduplicated_location_reference_programs": len(programs),
        "candidate_programs": programs,
        "claim_boundary": "This is an outcome-blind candidate pool. Island status, geological origin and sampling effort are intentionally unreviewed. No ABM output is consulted during admission."
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/results/preregistered_global_network_candidate_pool.json"))
    args = p.parse_args()
    payload = build_pool(fetch_text(URL))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
