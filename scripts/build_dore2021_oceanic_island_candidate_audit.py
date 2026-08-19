from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def classify(row: pd.Series) -> tuple[str | None, str | None]:
    text = f"{row.get('Location', '')} {row.get('Country_location', '')}".lower()
    rules = [
        (r"canary|tenerife|lanzarote|el hierro|la gomera|gran canaria|fuerteventura", "North Atlantic / Macaronesia", "Canary Islands"),
        (r"azores|flores island|terceira", "North Atlantic / Macaronesia", "Azores"),
        (r"mauritius|mauritian|aigrettes", "western Indian Ocean", "Mauritius"),
        (r"seychell|mahe", "western Indian Ocean", "Seychelles"),
        (r"galapagos|fernandina|pinta island|santiago island|santa cruz island|san cristobal", "eastern / central Pacific", "Galapagos"),
        (r"hawai|o'ahu|oahu", "eastern / central Pacific", "Hawaii"),
    ]
    for pat, stratum, system in rules:
        if re.search(pat, text):
            return stratum, system
    return None, None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", type=Path, default=Path("data/external/dore2021/aggreg.webs_full.csv"))
    p.add_argument("--out", type=Path, default=Path("data/results/dore2021_oceanic_island_candidate_audit.json"))
    args = p.parse_args()

    df = pd.read_csv(args.csv)
    oi = df[df["Land_type"].astype(str).eq("OI")].copy()
    rows = []
    for _, r in oi.iterrows():
        stratum, system = classify(r)
        rows.append({
            "region_pub": None if pd.isna(r.get("Region_pub")) else str(r.get("Region_pub")),
            "location": None if pd.isna(r.get("Location")) else str(r.get("Location")),
            "country_location": None if pd.isna(r.get("Country_location")) else str(r.get("Country_location")),
            "latitude": None if pd.isna(r.get("Latitude_dec")) else float(r.get("Latitude_dec")),
            "longitude": None if pd.isna(r.get("Longitude_dec")) else float(r.get("Longitude_dec")),
            "reference_id": None if pd.isna(r.get("Ref_paper")) else str(r.get("Ref_paper")),
            "sampling_time": None if pd.isna(r.get("Sampling_time")) else float(r.get("Sampling_time")),
            "sampling_effort": None if pd.isna(r.get("Sampling_effort")) else float(r.get("Sampling_effort")),
            "source_land_type": "OI",
            "programme_stratum": stratum,
            "candidate_system": system,
            "admission_state": "candidate_pending_source_matrix_and_geology_gate" if system else "not_admitted_by_preregistered_strata",
        })

    systems: dict[str, dict] = {}
    for x in rows:
        if not x["candidate_system"]:
            continue
        key = x["candidate_system"]
        systems.setdefault(key, {
            "stratum": x["programme_stratum"],
            "source_rows": 0,
            "references": set(),
            "locations": set(),
            "all_rows_have_sampling_effort": True,
        })
        s = systems[key]
        s["source_rows"] += 1
        if x["reference_id"]: s["references"].add(x["reference_id"])
        if x["location"]: s["locations"].add(x["location"])
        if x["sampling_effort"] is None: s["all_rows_have_sampling_effort"] = False

    system_rows = []
    for name, s in sorted(systems.items()):
        system_rows.append({
            "system": name,
            "stratum": s["stratum"],
            "source_rows": s["source_rows"],
            "references": sorted(s["references"]),
            "locations": sorted(s["locations"]),
            "all_rows_have_sampling_effort": s["all_rows_have_sampling_effort"],
            "selection_used_abm_outcome": False,
        })

    counts: dict[str, int] = {}
    for s in system_rows:
        counts[s["stratum"]] = counts.get(s["stratum"], 0) + 1

    payload = {
        "analysis": "dore2021_outcome_blind_oceanic_island_candidate_audit",
        "source_rows_total": int(len(df)),
        "source_labeled_OI_rows": int(len(oi)),
        "candidate_systems": system_rows,
        "candidate_system_count_by_stratum": counts,
        "strata_with_at_least_two_candidate_systems": sorted(k for k, v in counts.items() if v >= 2),
        "release_condition_met_from_dore_alone": sum(v >= 2 for v in counts.values()) >= 4,
        "decision": "dore_pool_supplies_three_two-system_strata_but_not_balanced_global_release" if sum(v >= 2 for v in counts.values()) == 3 else "see_counts",
        "next_gap": "A fourth geographically distinct stratum with two source-locked quantitative oceanic-island systems is required before geographically balanced release.",
        "claim_boundary": "Candidate extraction uses only source Land_type, geography, identifiers and sampling metadata. No network outcome or ABM fit is used. Source Land_type=OI is not by itself geological verification; final admission still requires the preregistered geology and matrix gates.",
        "rows": rows,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
