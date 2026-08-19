from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

RAW = Path("data/external/dore2021_zenodo_v1/network interaction data.txt")
SOURCE_GATE = Path("data/results/dore2021_zenodo_v1_raw_interaction_source_gate.json")
FROZEN = Path("data/design/frozen_dore_candidate_network_locations.json")
OUT = Path("data/results/dore2021_zenodo_v1_raw_interaction_schema_audit.json")


def norm(x: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(x or "").lower())


def match_column(fieldnames: list[str], candidates: tuple[str, ...]) -> str | None:
    by_norm = {norm(x): x for x in fieldnames}
    for candidate in candidates:
        if norm(candidate) in by_norm:
            return by_norm[norm(candidate)]
    return None


def detect_dialect(path: Path) -> csv.Dialect:
    sample = path.read_text(encoding="utf-8-sig", errors="replace")[:100000]
    try:
        return csv.Sniffer().sniff(sample, delimiters="\t;,|")
    except csv.Error:
        return csv.excel_tab


def main() -> None:
    gate = json.loads(SOURCE_GATE.read_text()) if SOURCE_GATE.exists() else {}
    payload: dict[str, object] = {
        "schema_version": "1.0",
        "analysis": "dore2021_zenodo_v1_raw_interaction_schema_audit",
        "source_status": gate.get("status"),
        "source_sha256": gate.get("sha256"),
        "status": "blocked",
    }
    if gate.get("status") != "raw_interaction_bytes_recovered" or not RAW.exists():
        payload["decision"] = "raw_bytes_not_available_for_schema_audit"
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    dialect = detect_dialect(RAW)
    with RAW.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    roles = {
        "region_pub": match_column(fields, ("Region_pub", "region_pub", "regionpub", "region")),
        "plant": match_column(fields, ("Plant_sp", "plant_sp", "plant", "plant_species", "plantname")),
        "pollinator": match_column(fields, ("Pollinator_sp", "pollinator_sp", "pollinator", "insect_sp", "visitor_sp", "animal")),
        "interaction_weight": match_column(fields, ("Interaction", "interaction", "interaction_frequency", "frequency", "weight", "visits", "n_interactions")),
        "reference": match_column(fields, ("Ref_paper", "reference", "ref", "paper")),
        "location": match_column(fields, ("Location", "location", "site")),
    }

    frozen = json.loads(FROZEN.read_text())
    frozen_ids = sorted({str(r["region_pub"]) for r in frozen["rows"]})
    region_col = roles["region_pub"]
    raw_region_counts = Counter()
    if region_col:
        raw_region_counts.update(str(r.get(region_col, "")) for r in rows if r.get(region_col) not in (None, ""))
    matched = {rid: int(raw_region_counts.get(rid, 0)) for rid in frozen_ids}
    matched_nonzero = {k: v for k, v in matched.items() if v > 0}

    preview = []
    for row in rows[:5]:
        preview.append({k: row.get(k) for k in fields[:20]})

    required = [roles["region_pub"], roles["plant"], roles["pollinator"], roles["interaction_weight"]]
    payload.update(
        {
            "status": "schema_audited",
            "delimiter": getattr(dialect, "delimiter", None),
            "n_rows": len(rows),
            "n_columns": len(fields),
            "columns": fields,
            "resolved_roles": roles,
            "all_tier_b_roles_resolved": all(required),
            "frozen_region_pub_count": len(frozen_ids),
            "frozen_region_pub_with_raw_rows": len(matched_nonzero),
            "raw_rows_by_frozen_region_pub": matched,
            "frozen_region_pub_with_raw_rows_nonzero": matched_nonzero,
            "preview_first_rows_first_20_columns": preview,
            "decision": (
                "raw_schema_supports_frozen_tier_b_matrix_reconstruction"
                if all(required) and matched_nonzero
                else "schema_or_frozen_region_link_requires_resolution"
            ),
            "next_gate": "Only if Region_pub, plant, pollinator and interaction-weight roles are source-resolved, reconstruct weighted matrices for frozen rows and calculate source-compatible interaction diversity and plant niche overlap. Do not infer missing weights or treat absent raw rows as biological zero.",
            "claim_boundary": "Schema and row-link audit only. No Tier-B network metric is claimed until weighted matrices are reconstructed from the source interaction rows.",
        }
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
