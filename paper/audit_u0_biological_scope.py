"""Audit biological scope of a rebuilt U0 table before floral evidence screening.

GBIF occurrence search filters can still yield taxonomic mismatches through
accepted-name reconciliation or upstream record issues. This step rechecks each
accepted GBIF key and makes a separate floral-screening universe:

- exclude non-Plantae taxa;
- exclude known non-flowering plant classes (ferns, lycophytes, bryophytes,
  gymnosperms);
- retain flowering-plant candidates for U1 literature screening.

This is a screening-scope filter, not an assertion that every retained taxon is
entomophilous. Ambiguous plant classifications are retained with an explicit
`needs_taxonomic_review` flag rather than silently dropped.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = "https://api.gbif.org/v1/species/"
USER_AGENT = "izu-core-biological-scope-audit/1.0"
NONFLOWERING_CLASSES = {
    "Anthocerotopsida", "Bryopsida", "Cycadopsida", "Equisetopsida", "Ginkgoopsida",
    "Gnetopsida", "Jungermanniopsida", "Liliopsida?", "Lycopodiopsida", "Marchantiopsida",
    "Pinopsida", "Polypodiopsida", "Psilotopsida", "Sphagnopsida",
}
# Liliopsida must not be excluded: the sentinel above is deliberately non-matching.


def request_json(key: str, attempts: int = 4) -> tuple[dict, int]:
    url = API + key
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=45) as response:  # nosec B310 fixed HTTPS GBIF endpoint
                return json.load(response), int(response.status)
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


def classify(record: dict) -> tuple[str, str]:
    kingdom = str(record.get("kingdom") or "")
    phylum = str(record.get("phylum") or "")
    class_name = str(record.get("class") or "")
    if kingdom != "Plantae":
        return "exclude_nonplant", f"accepted kingdom={kingdom or 'missing'}"
    if class_name in NONFLOWERING_CLASSES:
        return "exclude_nonflowering_plant", f"class={class_name}"
    if phylum and phylum != "Tracheophyta":
        return "exclude_nonvascular_or_unresolved", f"phylum={phylum}"
    if not phylum or not class_name:
        return "retain_needs_taxonomic_review", f"missing phylum/class: phylum={phylum or 'missing'} class={class_name or 'missing'}"
    return "retain_flowering_candidate", f"kingdom={kingdom}; phylum={phylum}; class={class_name}"


def fetch_one(key: str) -> tuple[str, dict, int]:
    record, status = request_json(key)
    return key, record, status


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--u0", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 12:
        raise ValueError("--workers must be between 1 and 12")

    with args.u0.open(encoding="utf-8", newline="") as handle:
        u0 = list(csv.DictReader(handle))
    keys = sorted({row["accepted_key"] for row in u0})
    records: dict[str, tuple[dict, int]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch_one, key): key for key in keys}
        for future in as_completed(futures):
            key = futures[future]
            try:
                result_key, record, status = future.result()
            except Exception as error:
                raise RuntimeError(f"GBIF scope audit failed for accepted_key={key}") from error
            records[result_key] = (record, status)

    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    audit_rows: list[dict[str, str]] = []
    retained_rows: list[dict[str, str]] = []
    excluded_rows: list[dict[str, str]] = []
    for row in u0:
        record, status = records[row["accepted_key"]]
        decision, reason = classify(record)
        audit = {
            **row,
            "gbif_scope_checked_at_utc": stamp,
            "gbif_scope_http_status": str(status),
            "gbif_kingdom": str(record.get("kingdom") or ""),
            "gbif_phylum": str(record.get("phylum") or ""),
            "gbif_class": str(record.get("class") or ""),
            "biological_scope_decision": decision,
            "biological_scope_reason": reason,
        }
        audit_rows.append(audit)
        if decision.startswith("retain_"):
            retained_rows.append(audit)
        else:
            excluded_rows.append(audit)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    fields = list(audit_rows[0]) if audit_rows else []
    for filename, rows in (
        ("u0_biological_scope_audit.csv", audit_rows),
        ("u0_flowering_candidate_universe.csv", retained_rows),
        ("u0_biological_scope_exclusions.csv", excluded_rows),
    ):
        with (args.out_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader(); writer.writerows(rows)
    summary = {
        "u0_input_taxa": len(u0),
        "retained_flowering_candidates": sum(row["biological_scope_decision"] == "retain_flowering_candidate" for row in audit_rows),
        "retained_needs_taxonomic_review": sum(row["biological_scope_decision"] == "retain_needs_taxonomic_review" for row in audit_rows),
        "excluded_nonplant": sum(row["biological_scope_decision"] == "exclude_nonplant" for row in audit_rows),
        "excluded_nonflowering_plant": sum(row["biological_scope_decision"] == "exclude_nonflowering_plant" for row in audit_rows),
        "excluded_nonvascular_or_unresolved": sum(row["biological_scope_decision"] == "exclude_nonvascular_or_unresolved" for row in audit_rows),
        "boundary": "Retained taxa are floral-screening candidates, not asserted entomophilous taxa.",
    }
    (args.out_dir / "u0_biological_scope.summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
