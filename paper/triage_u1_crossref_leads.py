"""Collapse U1 Crossref discovery leads into a source-level review queue.

Raw Crossref rows are intentionally retained separately because one work can be
retrieved by several names and queries. This script groups duplicate DOI/title
leads, preserves their query provenance, and assigns a *review priority* only.
It never asserts that a work contains a compatible trait effect. Obvious title
scopes that cannot inform floral/reproductive geographic response are excluded
at triage, with the raw lead retained for audit.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


FIELDS = (
    "review_rank", "review_priority", "recommended_synthesis_role", "u0_accepted_key", "accepted_name",
    "queue_rank", "title", "year", "doi", "container_title", "source_url", "crossref_score",
    "matched_query_ids", "matched_query_texts", "matched_search_names", "languages", "title_flags",
    "required_primary_checks", "review_status", "notes",
)
TITLE_SCOPE_EXCLUSION = re.compile(
    r"\b(?:correction to|erratum|ectomycorrhiz\w*|mycorrhiz\w*|seedling regeneration|vegetation recovery|"
    r"landslide|planting|forest composition|phylogenetic relationships|chloroplast genome|genome sequencing|"
    r"flower constituents|components of the flower|cultivar|re-blooming|floral transformation)\b",
    re.I,
)


def clean(value: str) -> str:
    return " ".join((value or "").casefold().split())


def group_key(row: dict[str, str]) -> str:
    doi = clean(row.get("doi", ""))
    if doi:
        return f"doi:{doi}"
    return "title:" + clean(row.get("title", "")) + "|year:" + clean(row.get("year", ""))


def title_scope_reason(rows: list[dict[str, str]]) -> str:
    matches = []
    for row in rows:
        match = TITLE_SCOPE_EXCLUSION.search(row.get("title", ""))
        if match:
            matches.append(match.group(0))
    return "; ".join(sorted(set(matches)))


def priority(rows: list[dict[str, str]]) -> tuple[int, str, str]:
    excluded_scope = title_scope_reason(rows)
    if excluded_scope:
        return 8, "exclude_title_scope", "exclude"
    review_first = any(row.get("automated_triage") == "review_first" for row in rows)
    taxon = any(row.get("taxon_title_match") == "yes" for row in rows)
    comparative = any(row.get("comparative_title_match") == "yes" for row in rows)
    trait = any(row.get("trait_title_match") == "yes" for row in rows)
    if review_first and comparative:
        return 0, "direct_geographic_candidate", "primary_geographic_candidate"
    if review_first and trait:
        return 1, "trait_or_function_candidate", "pending_scope_check"
    if taxon and trait:
        return 2, "taxon_trait_candidate", "functional_or_trait_context"
    if taxon:
        return 3, "taxon_context_candidate", "comparative_context"
    return 9, "noise_or_context", "exclude_unless_manual_reason"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leads", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    with args.leads.open(encoding="utf-8", newline="") as handle:
        raw = list(csv.DictReader(handle))
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in raw:
        if not row.get("title"):
            continue
        grouped[group_key(row)].append(row)

    queue: list[dict[str, str]] = []
    for rows in grouped.values():
        rows.sort(key=lambda row: (int(row.get("queue_rank") or 999999), int(row.get("result_rank") or 999999)))
        first = rows[0]
        priority_code, review_priority, role = priority(rows)
        query_ids = sorted({row.get("query_id", "") for row in rows if row.get("query_id")})
        query_texts = sorted({row.get("query_text", "") for row in rows if row.get("query_text")})
        search_names = sorted({row.get("search_name", "") for row in rows if row.get("search_name")})
        languages = sorted({row.get("language", "") for row in rows if row.get("language")})
        flags = sorted({f"taxon={row.get('taxon_title_match', '')};comparative={row.get('comparative_title_match', '')};trait={row.get('trait_title_match', '')};triage={row.get('automated_triage', '')}" for row in rows})
        scope = title_scope_reason(rows)
        note = f"Grouped from {len(rows)} raw Crossref lead rows; title-only priority is not evidence."
        if scope:
            note += f" Excluded automatically by title scope: {scope}."
        queue.append({
            "review_rank": "", "review_priority": review_priority, "recommended_synthesis_role": role,
            "u0_accepted_key": first.get("u0_accepted_key", ""), "accepted_name": first.get("accepted_name", ""),
            "queue_rank": first.get("queue_rank", ""), "title": first.get("title", ""), "year": first.get("year", ""),
            "doi": first.get("doi", ""), "container_title": first.get("container_title", ""),
            "source_url": first.get("source_url", ""), "crossref_score": first.get("crossref_score", ""),
            "matched_query_ids": "|".join(query_ids), "matched_query_texts": " | ".join(query_texts),
            "matched_search_names": "|".join(search_names), "languages": "|".join(languages),
            "title_flags": " | ".join(flags),
            "required_primary_checks": "Taxonomic concept; locality/population units; wild/cultivated status; page/table/figure; trait definition; n; variance; source independence.",
            "review_status": "not_reviewed", "notes": note,
            "_priority_code": str(priority_code),
        })
    queue.sort(key=lambda row: (int(row["_priority_code"]), int(row["queue_rank"] or 999999), row["title"].casefold()))
    for index, row in enumerate(queue, 1):
        row["review_rank"] = str(index)
        row.pop("_priority_code", None)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(queue)
    summary = {
        "raw_lead_rows": len(raw), "deduplicated_source_candidates": len(queue),
        "direct_geographic_candidates": sum(row["review_priority"] == "direct_geographic_candidate" for row in queue),
        "trait_or_function_candidates": sum(row["review_priority"] == "trait_or_function_candidate" for row in queue),
        "excluded_title_scope": sum(row["review_priority"] == "exclude_title_scope" for row in queue),
        "boundary": "Candidate categories are generated from metadata/title signals and require primary-source verification.",
    }
    args.out.with_suffix(".summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
