"""Crosswalk a rebuilt U0 universe to the existing 156-species pilot cohort.

A mismatch is a diagnostic, not an error: the legacy pilot may use a different
spatial profile, taxonomic interpretation or entomophily filter. The output
makes those differences reviewable before U0 is used as a new denominator.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
PILOT = HERE / "izu_entomophilous_candidates.csv"


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalise(value: str) -> str:
    return " ".join((value or "").casefold().split())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--u0", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    u0_rows = load(args.u0)
    pilot_rows = load(PILOT)
    by_u0_key = {row["accepted_key"]: row for row in u0_rows}
    by_raw_key: dict[str, dict[str, str]] = {}
    by_u0_name = {normalise(row["accepted_name"]): row for row in u0_rows}
    for row in u0_rows:
        for raw in filter(None, row.get("raw_species_keys_merged", "").split("|")):
            by_raw_key[raw] = row

    output: list[dict[str, str]] = []
    matched_u0_keys: set[str] = set()
    for pilot in pilot_rows:
        pilot_key = pilot["speciesKey"]
        pilot_name = pilot["name"]
        u0 = by_u0_key.get(pilot_key) or by_raw_key.get(pilot_key)
        status = ""
        if u0:
            status = "pilot_in_u0_key_crosswalk"
        else:
            u0 = by_u0_name.get(normalise(pilot_name))
            status = "pilot_in_u0_name_only" if u0 else "pilot_not_in_u0_profile"
        if u0:
            matched_u0_keys.add(u0["accepted_key"])
        output.append({
            "record_type": "pilot", "crosswalk_status": status,
            "pilot_speciesKey": pilot_key, "pilot_name": pilot_name,
            "pilot_family": pilot.get("family", ""), "pilot_n_islands": pilot.get("n_islands", ""),
            "u0_accepted_key": u0.get("accepted_key", "") if u0 else "",
            "u0_accepted_name": u0.get("accepted_name", "") if u0 else "",
            "u0_n_islands": u0.get("n_islands", "") if u0 else "",
            "u0_total_occ": u0.get("total_occ", "") if u0 else "",
            "review_note": "Review spatial profile/taxonomy before treating a mismatch as a biological absence." if not u0 else "",
        })
    for row in u0_rows:
        if row["accepted_key"] in matched_u0_keys:
            continue
        output.append({
            "record_type": "u0_only", "crosswalk_status": "u0_not_in_156_entomophilous_pilot",
            "pilot_speciesKey": "", "pilot_name": "", "pilot_family": "", "pilot_n_islands": "",
            "u0_accepted_key": row["accepted_key"], "u0_accepted_name": row["accepted_name"],
            "u0_n_islands": row["n_islands"], "u0_total_occ": row["total_occ"],
            "review_note": "Candidate for U1 search; absence from the 156 pilot does not determine pollination or trait relevance.",
        })

    fields = list(output[0]) if output else []
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(output)
    summary = {
        "legacy_pilot_taxa": len(pilot_rows),
        "u0_taxa": len(u0_rows),
        "pilot_matched_to_u0": sum(row["record_type"] == "pilot" and row["crosswalk_status"] != "pilot_not_in_u0_profile" for row in output),
        "pilot_not_in_u0_profile": sum(row["crosswalk_status"] == "pilot_not_in_u0_profile" for row in output),
        "u0_not_in_156_pilot": sum(row["record_type"] == "u0_only" for row in output),
    }
    args.out.with_suffix(".summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
