from __future__ import annotations

import argparse
import csv
import hashlib
import io
import urllib.request
from collections import defaultdict
from pathlib import Path

SOURCE_STUDY_ID = "euppollnet_31_roberts_england_step"
ARCHIPELAGO_ID = "great_britain"
TAG = "v1.3.0"
SOURCE_REPO = "JoseBSL/EuPPollNet"
INTERACTION_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/29_30_31_STEP/Interaction_data.csv"
FLOWER_URL = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{TAG}/Data/1_Raw_data/29_30_31_STEP/Flower_count.csv"
INTERACTION_SHA256 = "19af30ad6a0e2f9e8a1d129dfed9073592f331446251c6a1df6f91b39c7df099"
FLOWER_SHA256 = "f23f3996229da48a279728a0fd8432a380d35c31e9f484f6e86cd49855adb9c3"
ADMITTED = {"Carlisle", "Livingstone_far", "Livingstone_house"}
EFFORT_MINUTES = 30.0
OUTPUT_FIELDS = [
    "source_study_id", "archipelago_id", "system_id", "time_bin", "partner_id", "value", "effort"
]


def clean(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def load_bytes(url: str, expected_sha256: str, path: Path | None = None) -> bytes:
    if path is None:
        req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=180) as response:
            payload = response.read()
    else:
        payload = path.read_bytes()
    observed = hashlib.sha256(payload).hexdigest()
    if observed != expected_sha256:
        raise RuntimeError(f"source checksum drift for {url}: {observed}")
    return payload


def decode(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return payload.decode(encoding, errors="strict")
        except UnicodeDecodeError:
            continue
    raise RuntimeError("source cannot be decoded losslessly")


def date_key(row: dict[str, str]) -> str:
    try:
        y = int(float(clean(row.get("Year"))))
        m = int(float(clean(row.get("Month"))))
        d = int(float(clean(row.get("Day"))))
    except ValueError:
        return ""
    return f"{y:04d}-{m:02d}-{d:02d}"


def number(value: object) -> float | None:
    try:
        return float(clean(value))
    except ValueError:
        return None


def adapt(interaction_payload: bytes, flower_payload: bytes) -> list[dict[str, object]]:
    interactions = list(csv.DictReader(io.StringIO(decode(interaction_payload))))
    flowers = list(csv.DictReader(io.StringIO(decode(flower_payload))))

    schedule: dict[str, set[str]] = defaultdict(set)
    for row in flowers:
        if clean(row.get("country")).upper() != "UK":
            continue
        site = clean(row.get("Site_id"))
        day = date_key(row)
        if site in ADMITTED and day:
            schedule[site].add(day)

    events: dict[tuple[str, str, str], float] = defaultdict(float)
    partners_by_site: dict[str, set[str]] = defaultdict(set)
    effort_values: dict[str, set[float]] = defaultdict(set)
    area_values: dict[str, set[float]] = defaultdict(set)
    for row in interactions:
        if clean(row.get("Country")).upper() != "UK":
            continue
        site = clean(row.get("Site_id"))
        if site not in ADMITTED:
            continue
        plant = clean(row.get("Plant_species"))
        partner = clean(row.get("Pollinator_species"))
        if plant in {"[Unknown] [Unknown]", "[Nothing] [Nothing]"} or partner == "[Unknown] [Unknown]":
            continue
        day = date_key(row)
        if not day or not partner:
            continue
        if day not in schedule.get(site, set()):
            raise RuntimeError(f"{site}: interaction date {day} is outside frozen flower-count schedule")
        value = number(row.get("Interaction"))
        if value is None or value < 0:
            raise RuntimeError(f"{site}|{day}|{partner}: invalid Interaction")
        events[(site, day, partner)] += value
        partners_by_site[site].add(partner)
        effort = number(row.get("Sampling_effort_minutes"))
        area = number(row.get("Sampling_area_square_meters"))
        if effort is not None:
            effort_values[site].add(effort)
        if area is not None:
            area_values[site].add(area)

    output: list[dict[str, object]] = []
    for site in sorted(ADMITTED):
        dates = sorted(schedule.get(site, set()))
        if len(dates) != 8:
            raise RuntimeError(f"{site}: expected exactly 8 frozen source-native rounds, got {len(dates)}")
        counts_by_year = defaultdict(int)
        for day in dates:
            counts_by_year[day[:4]] += 1
        if dict(sorted(counts_by_year.items())) != {"2012": 4, "2013": 4}:
            raise RuntimeError(f"{site}: frozen 4+4 annual schedule drift: {dict(counts_by_year)}")
        if effort_values.get(site) != {EFFORT_MINUTES}:
            raise RuntimeError(f"{site}: sampling effort drift {effort_values.get(site)}")
        if area_values.get(site) != {300.0}:
            raise RuntimeError(f"{site}: sampling area drift {area_values.get(site)}")
        partners = sorted(partners_by_site.get(site, set()))
        if len(partners) < 3:
            raise RuntimeError(f"{site}: fewer than 3 identified partners")
        anchor = partners[0]
        for day in dates:
            emitted = False
            for partner in partners:
                value = float(events.get((site, day, partner), 0.0))
                if value <= 0:
                    continue
                output.append({
                    "source_study_id": SOURCE_STUDY_ID,
                    "archipelago_id": ARCHIPELAGO_ID,
                    "system_id": site,
                    "time_bin": day,
                    "partner_id": partner,
                    "value": value,
                    "effort": EFFORT_MINUTES,
                })
                emitted = True
            if not emitted:
                output.append({
                    "source_study_id": SOURCE_STUDY_ID,
                    "archipelago_id": ARCHIPELAGO_ID,
                    "system_id": site,
                    "time_bin": day,
                    "partner_id": anchor,
                    "value": 0.0,
                    "effort": EFFORT_MINUTES,
                })
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interactions", type=Path, default=None)
    parser.add_argument("--flowers", type=Path, default=None)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    interaction_payload = load_bytes(INTERACTION_URL, INTERACTION_SHA256, args.interactions)
    flower_payload = load_bytes(FLOWER_URL, FLOWER_SHA256, args.flowers)
    rows = adapt(interaction_payload, flower_payload)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
