from __future__ import annotations

import csv
import hashlib
import json
import urllib.request
import zipfile
from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

EXPECTED_SHA256 = "887f8ca24585c216ed11c561ca3dcdcc0882aa0aa8e7c99d064a3c9d2370ae8a"
ARCHIVE_URLS = [
    "https://ipt.gbif.pt/ipt/archive.do?r=pollinators_terceira&v=1.2",
    "https://ipt.gbif.pt/ipt/archive.do?r=pollinators_terceira",
]
OUT = Path("data/results/chapter2_terceira_natural_regime_source_audit_20260914.json")


def request_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "application/zip,application/octet-stream,*/*;q=0.8"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read()


def acquire_exact_archive() -> tuple[bytes, str, list[dict[str, object]]]:
    attempts: list[dict[str, object]] = []
    for url in ARCHIVE_URLS:
        try:
            payload = request_bytes(url)
            sha = hashlib.sha256(payload).hexdigest()
            attempts.append({"url": url, "bytes": len(payload), "sha256": sha})
            if sha == EXPECTED_SHA256:
                return payload, url, attempts
        except Exception as exc:
            attempts.append({"url": url, "error": repr(exc)})
    raise RuntimeError(f"exact Terceira v1.2 archive not recovered: {attempts}")


def read_table(archive: zipfile.ZipFile, basename: str) -> list[dict[str, str]]:
    names = [name for name in archive.namelist() if Path(name).name.casefold() == basename.casefold()]
    if len(names) != 1:
        raise RuntimeError(f"expected one {basename}, found {names}")
    with archive.open(names[0]) as raw:
        wrapper = TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        return list(csv.DictReader(wrapper, delimiter="\t"))


def clean(value: object) -> str:
    return str(value or "").strip()


def occurrence_event_key(row: dict[str, str]) -> str:
    for key in ("eventID", "coreid", "id"):
        value = clean(row.get(key))
        if value:
            return value
    return ""


def main() -> None:
    payload, successful_url, attempts = acquire_exact_archive()
    archive_path = Path("data/external/terceira_pollinators_v1_2.zip")
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path.write_bytes(payload)

    with zipfile.ZipFile(archive_path) as archive:
        events = read_table(archive, "event.txt")
        occurrences = read_table(archive, "occurrence.txt")
        members = sorted(archive.namelist())

    event_lookup: dict[str, dict[str, str]] = {}
    for event in events:
        for key in ("id", "eventID"):
            value = clean(event.get(key))
            if value:
                event_lookup[value] = event

    site_dates: dict[str, set[str]] = defaultdict(set)
    site_partners: dict[str, set[str]] = defaultdict(set)
    site_protocols: dict[str, set[str]] = defaultdict(set)
    site_efforts: dict[str, set[tuple[str, str]]] = defaultdict(set)
    linked_rows = 0
    unresolved_event_links = 0
    positive_quantity_rows = 0

    for row in occurrences:
        association = clean(row.get("associatedTaxa"))
        if "pollinator observed on" not in association.casefold():
            continue
        linked_rows += 1
        key = occurrence_event_key(row)
        event = event_lookup.get(key)
        if event is None:
            unresolved_event_links += 1
            continue
        protocol = clean(event.get("samplingProtocol"))
        if "transect" not in protocol.casefold():
            continue
        location = clean(event.get("locationID"))
        date = clean(event.get("eventDate"))
        if not location or not date:
            continue
        partner = clean(row.get("scientificName"))
        quantity_raw = clean(row.get("organismQuantity"))
        try:
            quantity = float(quantity_raw) if quantity_raw else 0.0
        except ValueError:
            quantity = 0.0
        if quantity > 0:
            positive_quantity_rows += 1
        site_dates[location].add(date)
        if partner:
            site_partners[location].add(partner)
        site_protocols[location].add(protocol)
        site_efforts[location].add((clean(event.get("sampleSizeValue")), clean(event.get("sampleSizeUnit"))))

    sites = []
    for location in sorted(site_dates):
        dates = sorted(site_dates[location])
        partners = sorted(site_partners[location])
        sites.append(
            {
                "locationID": location,
                "aligned_event_dates": len(dates),
                "event_dates": dates,
                "partner_series": len(partners),
                "sampling_protocols": sorted(site_protocols[location]),
                "sample_effort_values": [list(value) for value in sorted(site_efforts[location])],
                "passes_six_bin_floor": len(dates) >= 6,
                "passes_three_partner_floor": len(partners) >= 3,
            }
        )

    admitted = [row for row in sites if row["passes_six_bin_floor"] and row["passes_three_partner_floor"]]
    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_terceira_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "dataset": "Unveiling Azorean Pollinators: A Critical Step for Biodiversity and Conservation",
            "gbif_uuid": "db765f95-20f4-49ef-8fe4-b57228200a2e",
            "version": "1.2",
            "archive_bytes": len(payload),
            "archive_sha256": hashlib.sha256(payload).hexdigest(),
            "successful_url": successful_url,
            "transport_attempts": attempts,
            "archive_members": members,
        },
        "raw_structure": {
            "event_rows": len(events),
            "occurrence_rows": len(occurrences),
            "interaction_linked_occurrence_rows": linked_rows,
            "unresolved_event_links": unresolved_event_links,
            "positive_quantity_interaction_rows": positive_quantity_rows,
            "sites_with_linked_transect_interactions": len(sites),
            "sites_passing_frozen_structure_floor": len(admitted),
        },
        "sites": sites,
        "decision": (
            "ADMIT_STRUCTURALLY_ELIGIBLE_SITES_BEFORE_COORDINATES"
            if admitted else "FAIL_NO_SITE_REACHES_FROZEN_TEMPORAL_FLOOR"
        ),
        "claim_boundary": "This audit uses only source-native archive structure, dates, protocol, effort fields, partner identities and quantities. It does not compute D1, phi, rho_eq or any route statistic.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"decision": result["decision"], "raw_structure": result["raw_structure"], "sites": sites}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
