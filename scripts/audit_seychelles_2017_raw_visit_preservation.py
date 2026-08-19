from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/external/seychelles_temporal_compilation/OIK-07303_database.csv"
FALLBACK = ROOT / "data/results/seychelles_2017_temporal_compilation_fallback_audit.json"
OUT = ROOT / "data/results/seychelles_2017_raw_visit_preservation.json"
STUDY = "Kaiser-Bunbury2017"
EXPECTED_SITES = {"Ber", "Cas", "Cop", "Res", "Ros", "Sal", "Tea", "Tro"}


def main() -> None:
    fallback = json.loads(FALLBACK.read_text())
    if fallback.get("decision") != "target_study_identified_in_verified_compilation_next_resolve_interaction_rows":
        raise RuntimeError("verified fallback target-study gate is not open")

    with DB.open("r", encoding="latin-1", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [row for row in reader if row.get("study") == STUDY]
    if not rows:
        raise RuntimeError("target study has no interaction rows")

    sites = {row["sSite"] for row in rows}
    grains = {row["sgrainID"] for row in rows}
    site_grains = {(row["sSite"], row["sgrainID"]) for row in rows}
    largest = {row["largestgrain"] for row in rows}
    pairs = {(row["lower"], row["higher"]) for row in rows}
    freq = [float(row["freq"]) for row in rows]
    grain_types = {row["sgrain"] for row in rows}

    preservation = {
        "eight_sites": sites == EXPECTED_SITES,
        "eight_month_grain_ids": len(grains) == 8,
        "sixty_four_site_month_networks": len(site_grains) == 64 and all(sum(site == s for site, _ in site_grains) == 8 for s in sites),
        "reported_total_visits": len(rows) == 12235 and abs(sum(freq) - 12235.0) < 1e-9,
        "one_row_per_visit": all(value == 1.0 for value in freq),
        "reported_unique_links": len(pairs) == 581,
        "month_grain": grain_types == {"month"},
        "eight_largest_site_units": len(largest) == 8,
    }
    raw_count_ready = all(preservation.values())
    payload = {
        "schema_version": "1.0",
        "analysis": "seychelles_kaiser_bunbury2017_raw_visit_preservation",
        "verified_compilation_files": fallback["files"],
        "target_study": STUDY,
        "target_doi": fallback["target_doi"],
        "row_encoding": "latin-1",
        "n_rows": len(rows),
        "freq_sum": sum(freq),
        "freq_unique_values": sorted(set(freq)),
        "n_sites": len(sites),
        "sites": sorted(sites),
        "n_month_grain_ids": len(grains),
        "month_grain_ids": sorted(grains, key=lambda x: int(x)),
        "n_site_month_networks": len(site_grains),
        "n_unique_species_pairs": len(pairs),
        "n_plants": len({row["lower"] for row in rows}),
        "n_pollinators": len({row["higher"] for row in rows}),
        "preservation_tests": preservation,
        "secondary_raw_count_admission": raw_count_ready,
        "primary_standardized_visitfreq_admission": False,
        "decision": "raw_no_visits_secondary_layer_preserved_primary_visitfreq_still_unrecovered" if raw_count_ready else "raw_count_preservation_incomplete",
        "date_warning": "Compilation cdate values are not used as the original study calendar. Original IWDB states months 1-8 correspond to September 2012-April 2013; only source grain IDs/site identities and visit events are used here.",
        "next_gate": "Use the preserved raw no.visits layer only as the prespecified secondary Seychelles sensitivity. Continue source recovery for the original standardized 64 networks_visitfreq workbook before opening the preregistered primary four-system Tier-B LOSO.",
        "claim_boundary": "This verified compilation preserves one raw visit per row and the source-reported 8 sites x 8 monthly networks, 12,235 visits and 581 unique links. It does not contain or reconstruct the original standardized visitfreq weights, so it cannot substitute for the preregistered Seychelles primary weight family."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
