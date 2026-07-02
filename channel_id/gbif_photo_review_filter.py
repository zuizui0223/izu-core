"""Source-provenance filter for GBIF guide-photo review bundles.

A GBIF record can republish media from iNaturalist. A clear iNaturalist URL or
reference is enough to prevent that GBIF row from being treated as an independent
candidate in a parallel GBIF review bundle. The converse is intentionally not
assumed: rows not flagged as iNaturalist are not proven independent.
"""

from __future__ import annotations

from collections import Counter
from typing import Sequence


INATURALIST_REPUBLICATION = "iNaturalist_republication"


def split_gbif_review_rows(rows: Sequence[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    """Split rows into retainable candidates and obvious cross-source duplicates."""
    retained: list[dict[str, str]] = []
    excluded: list[dict[str, str]] = []
    for row in rows:
        if str(row.get("origin_platform_hint", "")).strip() == INATURALIST_REPUBLICATION:
            excluded.append(dict(row))
        else:
            retained.append(dict(row))
    counts = Counter({
        "input_media_rows": len(rows),
        "excluded_obvious_iNaturalist_republication_rows": len(excluded),
        "retained_not_flagged_media_rows": len(retained),
        "input_unique_gbif_records": len({str(row.get("record_id", "")).strip() for row in rows if str(row.get("record_id", "")).strip()}),
        "excluded_unique_gbif_records": len({str(row.get("record_id", "")).strip() for row in excluded if str(row.get("record_id", "")).strip()}),
        "retained_unique_gbif_records": len({str(row.get("record_id", "")).strip() for row in retained if str(row.get("record_id", "")).strip()}),
    })
    return retained, excluded, dict(counts)
