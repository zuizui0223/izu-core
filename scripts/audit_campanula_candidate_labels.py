"""Audit declared Campanula public-photo discovery labels.

Search labels are not taxonomy decisions. This command writes source-record
candidate leads and summary counts, while keeping broader/historical labels out
of the focal blinded-trait workflow until manual taxon promotion.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from channel_id.campanula_candidate_label_audit import (
    build_audit_rows,
    load_label_registry,
    load_proxy_queue,
    load_snapshot_targets,
    validate_registry_against_snapshot,
    write_audit,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("data/campanula_candidate_label_registry.csv"))
    parser.add_argument("--snapshot-config", type=Path, default=Path("configs/izu_inaturalist_snapshot_targets.json"))
    parser.add_argument("--proxy-queue", type=Path, required=True)
    parser.add_argument("--output-records-csv", type=Path, required=True)
    parser.add_argument("--output-summary-csv", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()
    try:
        registry = load_label_registry(args.registry)
        validate_registry_against_snapshot(registry, load_snapshot_targets(args.snapshot_config))
        records, summary = build_audit_rows(registry, load_proxy_queue(args.proxy_queue))
        write_audit(args.output_records_csv, args.output_summary_csv, args.output_md, records, summary)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
