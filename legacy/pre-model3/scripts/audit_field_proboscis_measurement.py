#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from channel_id.proboscis_measurement import (
    SOURCE_TARGET_N,
    read_proboscis_measurements,
    summarize_proboscis_measurements,
)

SUMMARY_COLUMNS = (
    "visitor_taxon_id",
    "source_taxon_name",
    "island_id",
    "site_id",
    "measurement_n",
    "mean_proboscis_length_mm",
    "sd_proboscis_length_mm",
    "measurement_methods",
    "all_available_at_site",
    "source_target_n",
    "admission_state",
    "trait_lookup_ready",
)
LOOKUP_COLUMNS = (
    "visitor_taxon_id",
    "source_taxon_name",
    "site_id",
    "proboscis_length_mm",
    "measurement_n",
    "measurement_source",
    "source_locator",
    "trait_status",
    "source_bundle_sha256",
    "notes",
)


def _write_csv(path: Path, columns: tuple[str, ...], rows: tuple[dict, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit prospective Issue #91 proboscis measurements")
    parser.add_argument("--measurements", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--target-n", type=int, default=SOURCE_TARGET_N)
    args = parser.parse_args()

    rows = read_proboscis_measurements(args.measurements)
    summaries, lookup = summarize_proboscis_measurements(rows, target_n=args.target_n)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(args.output_dir / "proboscis_taxon_site_summary.csv", SUMMARY_COLUMNS, summaries)
    _write_csv(args.output_dir / "field_pollinator_trait_lookup_measured_new.csv", LOOKUP_COLUMNS, lookup)

    report = {
        "schema_version": "1.0",
        "analysis": "field_proboscis_measurement_admission",
        "source_matched_target_n": args.target_n,
        "measurement_rows": len(rows),
        "taxon_site_groups": len(summaries),
        "trait_lookup_ready_groups": len(lookup),
        "blocked_groups": len(summaries) - len(lookup),
        "rule": (
            "measured_new requires digital-caliper mm measurements and either target_n independent specimens "
            "or explicit confirmation that all available specimens were measured when fewer existed"
        ),
        "claim_boundary": (
            "A source-matched prospective trait mean enables Rao-Q FDQ calculation for the sampled site; it does "
            "not reconstruct historical Table S2, identify pollinator effectiveness, or replace SVD/reproductive treatments."
        ),
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
