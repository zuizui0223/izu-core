"""Collect and triage Crossref discovery leads for Izu evidence screening.

Returned records are discovery leads, never evidence observations. The script
records source-query provenance and a transparent title-only triage flag; each
candidate must still be checked against the original source before use.
"""
from __future__ import annotations

import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HERE = Path(__file__).parent
DOCKET = HERE / "evidence_screening"
DOCKETS = (
    "docket_specialists.csv", "docket_generalists.csv",
    "docket_large_flower.csv", "docket_other_systems.csv",
)
MAX_ATTEMPTS = 3
FIELDS = (
    "species", "screening_id", "query", "query_url", "retrieved_at_utc", "rank",
    "title", "year", "doi", "container_title", "url", "crossref_score",
    "species_title_match", "comparative_title_match", "automated_triage", "retrieval_status",
)
COMPARATIVE = re.compile(r"island|insular|mainland|izu|floral differentiation|geograph", flags=re.I)


def compact(text: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", text or "").lower().split())


def query_url(text: str) -> str:
    params = {
        "query.bibliographic": text, "rows": 8,
        "select": "title,DOI,published,container-title,URL,score",
    }
    return "https://api.crossref.org/works?" + urlencode(params)


def query_crossref(url: str) -> list[dict]:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        request = Request(url, headers={"User-Agent": "izu-meta-analysis/1.1 (evidence screening)"})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310: fixed HTTPS API
                return json.load(response)["message"]["items"]
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == MAX_ATTEMPTS:
                raise
            time.sleep(attempt)
        except URLError:
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(attempt)
    raise RuntimeError("unreachable retry state")


def year(item: dict) -> str:
    parts = item.get("published", {}).get("date-parts", [[]])
    return str(parts[0][0]) if parts and parts[0] else ""


def title_flags(species: str, title: str) -> tuple[str, str, str]:
    species_tokens = [token for token in compact(species).split() if len(token) > 2]
    cleaned = compact(title)
    species_match = bool(species_tokens) and all(token in cleaned for token in species_tokens)
    comparative_match = bool(COMPARATIVE.search(cleaned))
    if species_match and comparative_match:
        return "yes", "yes", "review_first"
    if species_match:
        return "yes", "no", "taxon_lead"
    if comparative_match:
        return "no", "yes", "context_only"
    return "no", "no", "noise_likely"


def main() -> None:
    candidates: list[dict[str, str]] = []
    for filename in DOCKETS:
        with (DOCKET / filename).open(encoding="utf-8", newline="") as handle:
            candidates.extend(csv.DictReader(handle))
    output: list[dict[str, object]] = []
    for candidate in candidates:
        species = candidate["scientific_name"]
        query = f"{species} Izu Islands floral morphology pollination"
        url = query_url(query)
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        try:
            items = query_crossref(url)
            for rank, item in enumerate(items, 1):
                title = " | ".join(item.get("title", []))
                species_match, comparative_match, triage = title_flags(species, title)
                output.append({
                    "species": species, "screening_id": candidate["screening_id"],
                    "query": query, "query_url": url, "retrieved_at_utc": timestamp,
                    "rank": rank, "title": title, "year": year(item),
                    "doi": item.get("DOI", ""), "container_title": " | ".join(item.get("container-title", [])),
                    "url": item.get("URL", ""), "crossref_score": item.get("score", ""),
                    "species_title_match": species_match, "comparative_title_match": comparative_match,
                    "automated_triage": triage, "retrieval_status": "retrieved",
                })
        except HTTPError as error:
            output.append({"species": species, "screening_id": candidate["screening_id"], "query": query, "query_url": url, "retrieved_at_utc": timestamp, "rank": "", "title": "", "year": "", "doi": "", "container_title": "", "url": "", "crossref_score": "", "species_title_match": "", "comparative_title_match": "", "automated_triage": "", "retrieval_status": f"error:HTTPError:{error.code}"})
        except URLError as error:
            output.append({"species": species, "screening_id": candidate["screening_id"], "query": query, "query_url": url, "retrieved_at_utc": timestamp, "rank": "", "title": "", "year": "", "doi": "", "container_title": "", "url": "", "crossref_score": "", "species_title_match": "", "comparative_title_match": "", "automated_triage": "", "retrieval_status": f"error:URLError:{error.reason}"})
        time.sleep(0.4)
    path = DOCKET / "crossref_batch_001_leads.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(output)
    print(f"wrote {len(output)} Crossref lead rows to {path}")


if __name__ == "__main__":
    main()
