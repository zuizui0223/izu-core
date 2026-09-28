from __future__ import annotations

import csv
import hashlib
import io
import json
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/giannutri2025_daily_reconstruction_structure.json"
URL = "https://zenodo.org/api/records/14855496/files/transect_data_for_overlap_analysis.txt/content"
EXPECTED_SHA256 = "d28233d4a95e7dfe0f8048f917b424eabaffa97c9d37bb270b17d947a07f33ca"
FOCAL = {"Anthophora_dispar", "Bombus_terrestris", "Apis_mellifera"}
CHECK_SPECIES = ("Anthophora_dispar", "Bombus_terrestris")
MONTHS = {"February", "March", "April"}
CONDITIONS = {"open", "closed"}
POOL_FIRST = "20240225"
POOL_SECOND = "20240228"
POOL_DAY = "56"


def fetch_rows() -> list[dict[str, str]]:
    request = urllib.request.Request(URL, headers={"User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    sha = hashlib.sha256(payload).hexdigest()
    if sha != EXPECTED_SHA256:
        raise RuntimeError(f"Giannutri flower-visit source checksum drifted: {sha}")
    text = payload.decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


def source_prefilter(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        dict(row)
        for row in rows
        if row["Month"] in MONTHS
        and row["hives.condition"] in CONDITIONS
        and row["species"] in FOCAL
    ]


def transect_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    per_date: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        per_date[row["Date"]].add(row["transetto"])
    return {date: len(values) for date, values in per_date.items()}


def pool_rows(rows: list[dict[str, str]], remove_low_transect_dates: set[str]) -> list[dict[str, str]]:
    pooled = []
    for row in rows:
        if row["Date"] in (POOL_FIRST, POOL_SECOND):
            copy = dict(row)
            copy["Date"] = POOL_FIRST
            copy["day"] = POOL_DAY
            pooled.append(copy)
    removal = set(remove_low_transect_dates) | {POOL_FIRST}
    remaining = [row for row in rows if row["Date"] not in removal]
    return remaining + pooled


def minimum_observation_filter(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    totals: dict[tuple[str, str], float] = defaultdict(float)
    dates = sorted({row["Date"] for row in rows})
    for row in rows:
        if row["plant"] == "volo":
            continue
        if row["species"] in CHECK_SPECIES:
            totals[(row["Date"], row["species"])] += float(row["total"])
    removed = [
        date
        for date in dates
        if any(totals.get((date, species), 0.0) < 10.0 for species in CHECK_SPECIES)
    ]
    removed_set = set(removed)
    return [row for row in rows if row["Date"] not in removed_set], removed


def summarize_variant(prefiltered: list[dict[str, str]], low_dates: set[str]) -> dict:
    after_pool = pool_rows(prefiltered, low_dates)
    after_minimum, low_observation_dates = minimum_observation_filter(after_pool)
    final_dates = sorted({row["Date"] for row in after_minimum})
    conditions_by_date: dict[str, list[str]] = {}
    for date in final_dates:
        conditions_by_date[date] = sorted({
            row["hives.condition"] for row in after_minimum if row["Date"] == date
        })
    return {
        "low_transect_dates_removed_before_pool": sorted(low_dates),
        "low_observation_dates_removed_after_pool": sorted(low_observation_dates),
        "final_daily_network_count": len(final_dates),
        "final_dates": final_dates,
        "conditions_by_date": conditions_by_date,
        "dates_with_nonunique_hive_condition": [
            date for date, values in conditions_by_date.items() if len(values) != 1
        ],
    }


def main() -> None:
    rows = fetch_rows()
    prefiltered = source_prefilter(rows)
    counts = transect_counts(prefiltered)
    intended_low = {date for date, count in counts.items() if count <= 2}

    # R source line 181 creates column 'number', while line 198 reads tab$numero.
    # Literal $.data.frame lookup finds no 'numero' column, so the <=2 component
    # contributes no dates; only the explicitly appended 20240225 is removed before pooling.
    literal = summarize_variant(prefiltered, set())
    intended = summarize_variant(prefiltered, intended_low)

    result = {
        "schema_version": "1.0",
        "analysis": "giannutri2025_daily_reconstruction_structure_audit",
        "source_sha256": EXPECTED_SHA256,
        "raw_row_count": len(rows),
        "prefiltered_row_count": len(prefiltered),
        "source_column_mismatch": {
            "declared_column_line_181": "number",
            "lookup_line_198": "numero",
            "interpretation": "literal R source and comment-intended <=2-transect filtering are audited separately before any network target is calculated"
        },
        "published_expected_daily_network_count": 29,
        "literal_source_semantics": literal,
        "comment_intended_number_semantics": intended,
        "literal_matches_published_count": literal["final_daily_network_count"] == 29,
        "intended_matches_published_count": intended["final_daily_network_count"] == 29,
        "target_metrics_calculated": False,
        "network_matrices_built": False,
        "claim_boundary": "This audit resolves source-native day selection only. It does not compute pollinator support, interaction Shannon, plant niche overlap, or any v6 fit."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
