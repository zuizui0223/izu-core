"""Run a bounded, auditable Crossref discovery batch from the U1 query manifest.

The output is a *lead* table and an exact query log. A title match is never
converted into an effect, a functional-group assignment, or a retained source
without primary-source review. Zero result rows are kept deliberately.

Usage:
    python paper/run_u1_crossref_discovery.py \
        --manifest artifacts/u0_snapshot/u1_search_query_manifest.csv \
        --out-dir artifacts/u0_snapshot/crossref_batch_001 \
        --max-taxa 40 --max-queries 160
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.crossref.org/works"
USER_AGENT = "izu-core-u1-crossref/1.0 (systematic evidence screening)"
COMPARATIVE = re.compile(r"\b(island|insular|mainland|izu|geograph|population differentiation)\b|伊豆|島嶼|島|本土", re.I)
TRAIT = re.compile(r"\b(flower|floral|corolla|morpholog|pollinat|reproduct|mating|self.compat)\b|花|形態|送粉|訪花|繁殖|自家", re.I)

QUERY_FIELDS = (
    "query_id", "u0_accepted_key", "accepted_name", "queue_rank", "name_type", "search_name",
    "language", "source_lane", "query_purpose", "query_text", "query_url", "retrieved_at_utc",
    "records_returned", "retrieval_status", "error_detail",
)
LEAD_FIELDS = QUERY_FIELDS + (
    "result_rank", "title", "year", "doi", "container_title", "source_url", "crossref_score",
    "taxon_title_match", "comparative_title_match", "trait_title_match", "automated_triage",
)


def compact(text: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", text or "").casefold().split())


def query_url(text: str) -> str:
    return API + "?" + urlencode({
        "query.bibliographic": text, "rows": 6,
        "select": "title,DOI,published,container-title,URL,score",
    })


def request_items(url: str, attempts: int = 4) -> list[dict]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310 fixed HTTPS Crossref endpoint
                return json.load(response)["message"]["items"]
        except HTTPError as error:
            last_error = error
            if error.code not in (429, 500, 502, 503, 504) or attempt == attempts:
                raise
        except URLError as error:
            last_error = error
            if attempt == attempts:
                raise
        time.sleep(attempt)
    assert last_error is not None
    raise last_error


def published_year(item: dict) -> str:
    for key in ("published", "issued", "published-print", "published-online"):
        parts = item.get(key, {}).get("date-parts", [[]])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def title_flags(query: dict[str, str], title: str) -> tuple[str, str, str, str]:
    cleaned = compact(title)
    query_name = compact(query["search_name"])
    tokens = [token for token in query_name.split() if len(token) > 2]
    taxon_match = "yes" if tokens and all(token in cleaned for token in tokens) else "no"
    comparative_match = "yes" if COMPARATIVE.search(title or "") else "no"
    trait_match = "yes" if TRAIT.search(title or "") else "no"
    if taxon_match == "yes" and (comparative_match == "yes" or trait_match == "yes"):
        triage = "review_first"
    elif taxon_match == "yes":
        triage = "taxon_lead"
    elif comparative_match == "yes" and trait_match == "yes":
        triage = "context_only"
    else:
        triage = "noise_likely"
    return taxon_match, comparative_match, trait_match, triage


def priority(row: dict[str, str]) -> tuple[int, int, int, str]:
    purpose_order = {"taxon_baseline": 0, "island_comparison": 1, "izu_trait": 2}
    name_order = {"accepted_input": 0, "accepted_fallback": 0, "gbif_synonym": 1, "gbif_vernacular": 2}
    language_order = {"en": 0, "ja": 1}
    return (
        int(row["queue_rank"]), purpose_order.get(row["query_purpose"], 9),
        name_order.get(row["name_type"], 9) + language_order.get(row["language"], 9), row["query_id"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--max-taxa", type=int, default=40)
    parser.add_argument("--max-queries", type=int, default=160)
    parser.add_argument("--sleep-seconds", type=float, default=0.15)
    args = parser.parse_args()

    with args.manifest.open(encoding="utf-8", newline="") as handle:
        manifest = [row for row in csv.DictReader(handle) if row["source_lane"] == "Crossref"]
    taxon_keys = {row["u0_accepted_key"] for row in sorted(manifest, key=priority)[:0]}
    allowed_taxa = []
    for row in sorted(manifest, key=priority):
        key = row["u0_accepted_key"]
        if key not in taxon_keys and len(taxon_keys) >= args.max_taxa:
            continue
        taxon_keys.add(key)
        allowed_taxa.append(row)
    selected = sorted(allowed_taxa, key=priority)[: args.max_queries]

    query_log: list[dict[str, str]] = []
    leads: list[dict[str, str]] = []
    for query in selected:
        stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        url = query_url(query["query_text"])
        base = {field: query.get(field, "") for field in QUERY_FIELDS if field not in {"query_url", "retrieved_at_utc", "records_returned", "retrieval_status", "error_detail"}}
        base.update({"query_url": url, "retrieved_at_utc": stamp, "records_returned": "", "retrieval_status": "", "error_detail": ""})
        try:
            items = request_items(url)
            base["records_returned"] = str(len(items))
            base["retrieval_status"] = "retrieved"
            query_log.append(base.copy())
            for rank, item in enumerate(items, 1):
                title = " | ".join(item.get("title", []))
                taxon_match, comparative_match, trait_match, triage = title_flags(query, title)
                lead = base.copy()
                lead.update({
                    "result_rank": str(rank), "title": title, "year": published_year(item),
                    "doi": item.get("DOI", ""), "container_title": " | ".join(item.get("container-title", [])),
                    "source_url": item.get("URL", ""), "crossref_score": str(item.get("score", "")),
                    "taxon_title_match": taxon_match, "comparative_title_match": comparative_match,
                    "trait_title_match": trait_match, "automated_triage": triage,
                })
                leads.append(lead)
        except HTTPError as error:
            base.update({"retrieval_status": f"error:HTTPError:{error.code}", "error_detail": str(error.code)})
            query_log.append(base)
        except URLError as error:
            base.update({"retrieval_status": "error:URLError", "error_detail": str(error.reason)})
            query_log.append(base)
        time.sleep(args.sleep_seconds)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "u1_crossref_query_log.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUERY_FIELDS)
        writer.writeheader(); writer.writerows(query_log)
    with (args.out_dir / "u1_crossref_leads.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEAD_FIELDS)
        writer.writeheader(); writer.writerows(leads)
    summary = {
        "selected_taxa": len({row["u0_accepted_key"] for row in selected}),
        "queries_run": len(query_log),
        "queries_with_errors": sum(row["retrieval_status"].startswith("error:") for row in query_log),
        "lead_rows": len(leads),
        "review_first_leads": sum(row["automated_triage"] == "review_first" for row in leads),
        "boundary": "All rows are discovery leads. Primary-source checking remains mandatory before evidence extraction.",
    }
    (args.out_dir / "u1_crossref_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
