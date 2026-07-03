"""Collect Crossref literature leads for the Izu evidence-screening dockets.

This creates discovery leads, not evidence observations. Each returned record must
be read and checked against the source before it can enter the meta-analysis.
"""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
DOCKET = HERE / "evidence_screening"
DOCKETS = (
    "docket_specialists.csv",
    "docket_generalists.csv",
    "docket_large_flower.csv",
    "docket_other_systems.csv",
)
FIELDS = ("species", "screening_id", "query", "rank", "title", "year", "doi", "container_title", "url", "crossref_score", "retrieval_status")


def query_crossref(text: str) -> list[dict]:
    params = {"query.bibliographic": text, "rows": 8, "select": "title,author,DOI,published,container-title,URL,score"}
    request = Request("https://api.crossref.org/works?" + urlencode(params), headers={"User-Agent": "izu-meta-analysis/1.0 (evidence screening)"})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed HTTPS source
        return json.load(response)["message"]["items"]


def year(item: dict) -> str:
    parts = item.get("published", {}).get("date-parts", [[]])
    return str(parts[0][0]) if parts and parts[0] else ""


def main() -> None:
    candidates: list[dict[str, str]] = []
    for filename in DOCKETS:
        with (DOCKET / filename).open(encoding="utf-8", newline="") as handle:
            candidates.extend(csv.DictReader(handle))
    output: list[dict[str, object]] = []
    for candidate in candidates:
        species = candidate["scientific_name"]
        text = f"{species} Izu Islands floral morphology pollination"
        try:
            items = query_crossref(text)
            for rank, item in enumerate(items, 1):
                output.append({
                    "species": species, "screening_id": candidate["screening_id"], "query": text,
                    "rank": rank, "title": " | ".join(item.get("title", [])), "year": year(item),
                    "doi": item.get("DOI", ""), "container_title": " | ".join(item.get("container-title", [])),
                    "url": item.get("URL", ""), "crossref_score": item.get("score", ""), "retrieval_status": "retrieved",
                })
        except Exception as error:
            output.append({"species": species, "screening_id": candidate["screening_id"], "query": text, "rank": "", "title": "", "year": "", "doi": "", "container_title": "", "url": "", "crossref_score": "", "retrieval_status": f"error:{type(error).__name__}"})
        time.sleep(0.2)
    path = DOCKET / "crossref_batch_001_leads.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(output)
    print(f"wrote {len(output)} Crossref lead rows to {path}")


if __name__ == "__main__":
    main()
