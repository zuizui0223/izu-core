"""Build an auditable English/Japanese query manifest for every U1 taxon.

A query manifest is not a source search result. It records the exact searches
that must be attempted in each lane before a taxon can be marked screened. The
manifest draws from the U1 accepted-name/synonym/vernacular registry and keeps
source lanes separate; a zero-hit query is evidence of search coverage, not of
biological absence.

Usage:
    python paper/build_u1_search_query_manifest.py \
        --u1 artifacts/u0_snapshot/u1_screening_queue.csv \
        --names artifacts/u0_snapshot/u1_taxon_name_registry.csv \
        --out artifacts/u0_snapshot/u1_search_query_manifest.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

MAX_SCIENTIFIC_NAMES = 3
MAX_JAPANESE_NAMES = 2


FIELDS = (
    "query_id", "u0_accepted_key", "accepted_name", "queue_rank", "name_type", "search_name",
    "language", "source_lane", "query_purpose", "query_text", "required_output", "query_status",
)


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def clean(value: str) -> str:
    return " ".join((value or "").split())


def deduplicate(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, str, str]] = set()
    out = []
    for row in rows:
        key = (row["u0_accepted_key"], row["source_lane"], row["query_purpose"], row["query_text"], row["language"])
        if key not in seen:
            seen.add(key)
            out.append(row)
    return out


def add_query(rows: list[dict[str, str]], *, key: str, accepted: str, rank: str, name_type: str, name: str, language: str, lane: str, purpose: str, query: str) -> None:
    rows.append({
        "query_id": "", "u0_accepted_key": key, "accepted_name": accepted, "queue_rank": rank,
        "name_type": name_type, "search_name": name, "language": language, "source_lane": lane,
        "query_purpose": purpose, "query_text": query, "required_output": "Record hit count and retain/exclude each candidate source with identifier and reason.",
        "query_status": "not_run",
    })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--u1", required=True, type=Path)
    parser.add_argument("--names", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    queue = load(args.u1)
    raw_names = load(args.names)
    names_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in raw_names:
        if row.get("review_status") == "error" or not clean(row.get("search_name", "")):
            continue
        names_by_key[row["u0_accepted_key"]].append(row)

    planned: list[dict[str, str]] = []
    for taxon in queue:
        key = taxon["u0_accepted_key"]
        accepted = taxon["accepted_name"]
        rank = taxon["queue_rank"]
        names = names_by_key.get(key, [])
        scientific = [row for row in names if row["name_type"] in {"accepted_input", "gbif_synonym"}]
        japanese = [row for row in names if row["name_type"] == "gbif_vernacular" and row.get("language", "").lower() in {"ja", "jpn", "jp"}]
        if not scientific:
            scientific = [{"name_type": "accepted_fallback", "search_name": accepted, "language": ""}]

        seen_scientific: set[str] = set()
        for row in scientific:
            name = clean(row["search_name"])
            if not name or name.casefold() in seen_scientific:
                continue
            seen_scientific.add(name.casefold())
            if len(seen_scientific) > MAX_SCIENTIFIC_NAMES:
                break
            for lane in ("Crossref", "OpenAlex", "CiNii_Research", "J_STAGE", "IRDB"):
                add_query(planned, key=key, accepted=accepted, rank=rank, name_type=row["name_type"], name=name, language="en", lane=lane, purpose="taxon_baseline", query=name)
            for lane in ("Crossref", "OpenAlex", "CiNii_Research", "J_STAGE", "IRDB"):
                add_query(planned, key=key, accepted=accepted, rank=rank, name_type=row["name_type"], name=name, language="en", lane=lane, purpose="island_comparison", query=f"{name} island mainland floral pollination")

        seen_japanese: set[str] = set()
        for row in japanese:
            name = clean(row["search_name"])
            if not name or name in seen_japanese:
                continue
            seen_japanese.add(name)
            if len(seen_japanese) > MAX_JAPANESE_NAMES:
                break
            for lane in ("Crossref", "CiNii_Research", "J_STAGE", "IRDB"):
                add_query(planned, key=key, accepted=accepted, rank=rank, name_type=row["name_type"], name=name, language="ja", lane=lane, purpose="izu_trait", query=f"{name} 伊豆 花 形態 送粉")
                add_query(planned, key=key, accepted=accepted, rank=rank, name_type=row["name_type"], name=name, language="ja", lane=lane, purpose="island_comparison", query=f"{name} 島 本土 比較")

    planned = deduplicate(planned)
    planned.sort(key=lambda row: (int(row["queue_rank"]), row["source_lane"], row["query_purpose"], row["query_text"]))
    for index, row in enumerate(planned, 1):
        row["query_id"] = f"u1q-{index:06d}"

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(planned)
    summary = {
        "u1_taxa": len(queue), "planned_queries": len(planned),
        "taxa_with_japanese_vernacular_leads": len({row["u0_accepted_key"] for row in planned if row["language"] == "ja"}),
        "queries_by_lane": {lane: sum(row["source_lane"] == lane for row in planned) for lane in sorted({row["source_lane"] for row in planned})},
        "boundary": "The manifest records intended searches. It does not certify a lane as searched until a run log is produced.",
    }
    args.out.with_suffix(".summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
