"""Retrieve GBIF synonym and vernacular-name leads for systematic taxon searches.

The output is a search expansion registry, not a taxonomic decision. Every name
is retained with source API, retrieval time and acceptance status for review.
"""
from __future__ import annotations

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
DOCKET = HERE / "evidence_screening"
INPUTS = ("docket_specialists.csv", "docket_generalists.csv", "docket_large_flower.csv", "docket_other_systems.csv")
OUT = DOCKET / "gbif_taxon_search_registry.csv"
FIELDS = ("screening_id", "species_key", "accepted_name", "name_type", "name", "language", "source_api", "retrieved_at_utc", "review_status", "notes")


def get(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "izu-meta-analysis-taxon-registry/1.0"})
    with urlopen(request, timeout=45) as response:  # nosec B310 fixed HTTPS API
        return json.load(response)


def main() -> None:
    taxa = []
    for filename in INPUTS:
        with (DOCKET / filename).open(encoding="utf-8", newline="") as handle:
            taxa.extend(csv.DictReader(handle))
    rows = []
    for taxon in taxa:
        key = taxon["species_key"]
        stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        rows.append({"screening_id": taxon["screening_id"], "species_key": key, "accepted_name": taxon["scientific_name"], "name_type": "accepted_input", "name": taxon["scientific_name"], "language": "", "source_api": "candidate_docket", "retrieved_at_utc": stamp, "review_status": "input", "notes": "Candidate name; verify GBIF status before literature use."})
        try:
            synonyms = get(f"https://api.gbif.org/v1/species/{key}/synonyms").get("results", [])
            for item in synonyms:
                name = str(item.get("scientificName") or item.get("canonicalName") or "").strip()
                if name:
                    rows.append({"screening_id": taxon["screening_id"], "species_key": key, "accepted_name": taxon["scientific_name"], "name_type": "gbif_synonym", "name": name, "language": "", "source_api": f"https://api.gbif.org/v1/species/{key}/synonyms", "retrieved_at_utc": stamp, "review_status": "unreviewed", "notes": str(item.get("taxonomicStatus") or "")})
            names = get(f"https://api.gbif.org/v1/species/{key}/vernacularNames").get("results", [])
            for item in names:
                name = str(item.get("vernacularName") or "").strip()
                if name:
                    rows.append({"screening_id": taxon["screening_id"], "species_key": key, "accepted_name": taxon["scientific_name"], "name_type": "gbif_vernacular", "name": name, "language": str(item.get("language") or ""), "source_api": f"https://api.gbif.org/v1/species/{key}/vernacularNames", "retrieved_at_utc": stamp, "review_status": "unreviewed", "notes": "Search lead only; confirm Japanese taxonomic concept."})
        except Exception as error:
            rows.append({"screening_id": taxon["screening_id"], "species_key": key, "accepted_name": taxon["scientific_name"], "name_type": "retrieval_error", "name": "", "language": "", "source_api": "GBIF API", "retrieved_at_utc": stamp, "review_status": "error", "notes": type(error).__name__})
        time.sleep(0.3)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(rows)
    print(f"wrote {len(rows)} taxon-name rows to {OUT}")


if __name__ == "__main__":
    main()
