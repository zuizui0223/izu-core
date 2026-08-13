#!/usr/bin/env python3
"""Inventory every public bitstream in the locked Hetherington UofT ORIGINAL bundle.

The inventory distinguishes the full thesis, expanded abstract, and any non-PDF
attachments. It is a source-availability audit only and never treats absence of
an attachment as absence of a biological effect.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.acquire_hetherington_utoronto_dspace import BASE, get_json, object_candidates


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = ROOT / "artifacts/hetherington_2019/source_lock/source_lock.json"
DEFAULT_OUTPUT = ROOT / "artifacts/hetherington_2019/source_lock/bitstream_inventory.json"


def summarize(item: dict[str, Any]) -> dict[str, Any]:
    name = str(item.get("name") or "")
    lower = name.casefold()
    return {
        "uuid": item.get("uuid") or item.get("id"),
        "name": name,
        "sizeBytes": item.get("sizeBytes"),
        "sequenceId": item.get("sequenceId"),
        "description": item.get("description"),
        "mimeType": item.get("mimeType"),
        "is_pdf": lower.endswith(".pdf"),
        "is_full_thesis_pdf": lower.endswith("_msc_thesis.pdf") and "expandedabstract" not in lower,
        "is_expanded_abstract_pdf": "expandedabstract" in lower and lower.endswith(".pdf"),
        "looks_like_tabular_data_attachment": lower.endswith((".csv", ".tsv", ".xlsx", ".xls", ".rds", ".rdata", ".txt")),
    }


def build_inventory(lock: dict[str, Any], payload: dict[str, Any], api_url: str) -> dict[str, Any]:
    items = object_candidates(payload, kind="bitstream")
    summaries = sorted((summarize(item) for item in items), key=lambda row: (row["sequenceId"] is None, row["sequenceId"] or 0, row["name"]))
    full = [row for row in summaries if row["is_full_thesis_pdf"]]
    expanded = [row for row in summaries if row["is_expanded_abstract_pdf"]]
    tabular = [row for row in summaries if row["looks_like_tabular_data_attachment"]]
    return {
        "schema_version": "1.0",
        "status": "utoronto_original_bundle_bitstream_inventory_complete",
        "item_handle": lock.get("item_handle"),
        "item_uuid": lock.get("item_uuid"),
        "original_bundle_uuid": lock.get("original_bundle_uuid"),
        "api_url": api_url,
        "n_bitstreams": len(summaries),
        "bitstreams": summaries,
        "n_full_thesis_pdfs": len(full),
        "n_expanded_abstract_pdfs": len(expanded),
        "n_tabular_data_attachments": len(tabular),
        "tabular_data_attachments": tabular,
        "separate_numeric_136_pair_attachment_verified": False,
        "claim_boundary": (
            "This inventory reports public ORIGINAL-bundle attachments. A zero tabular-attachment count narrows the public repository route but does not prove that source-native numeric data never existed or are unavailable from every author/publisher route."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    lock = json.loads(args.lock.read_text(encoding="utf-8"))
    bundle_uuid = str(lock["original_bundle_uuid"])
    api_url = BASE + f"/core/bundles/{bundle_uuid}/bitstreams?size=100"
    payload = get_json(api_url, timeout=args.timeout)
    result = build_inventory(lock, payload, api_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
