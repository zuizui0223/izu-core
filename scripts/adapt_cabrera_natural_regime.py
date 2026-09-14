from __future__ import annotations

import argparse
import csv
import hashlib
import io
import math
import urllib.request
from collections import defaultdict
from pathlib import Path

SOURCE_STUDY_ID = "serra_marin_etal_2025_cabrera_pollination"
ARCHIPELAGO_ID = "balearic_islands"
SOURCE_URL = "https://digital.csic.es/bitstream/10261/420466/1/cabrera_22_23_habitat.csv"
SOURCE_SHA256 = "399ec11ae6ce18c8e9ebb050857ca7c1da4cb4a7858e24382750a92ae5e16a07"
PRIMARY_METHOD = "obs"
ADMITTED = {
    "Dune system 1",
    "Dune system 2",
    "Pine forest 2",
    "Rocky coastal 1",
    "Rocky coastal 2",
}
OUTPUT_FIELDS = [
    "source_study_id",
    "archipelago_id",
    "system_id",
    "time_bin",
    "partner_id",
    "value",
    "effort",
]


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def number(value: object) -> float | None:
    text = str(value or "").strip().replace(",", ".")
    if not text or text.lower() in {"na", "nan", "null", "none", "-"}:
        return None
    try:
        x = float(text)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def load_bytes(path: Path | None) -> bytes:
    if path is None:
        request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "text/csv,*/*;q=0.8"})
        with urllib.request.urlopen(request, timeout=90) as response:
            payload = response.read()
    else:
        payload = path.read_bytes()
    observed = hashlib.sha256(payload).hexdigest()
    if observed != SOURCE_SHA256:
        raise RuntimeError(f"Cabrera source checksum drift: {observed}")
    return payload


def decode(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError("Cabrera source cannot be decoded")


def adapt(payload: bytes) -> list[dict[str, object]]:
    rows = list(csv.DictReader(io.StringIO(decode(payload)), delimiter=";"))
    obs = [
        row for row in rows
        if clean(row.get("Method")) == PRIMARY_METHOD
        and clean(row.get("COMMUNITY")) in ADMITTED
    ]

    contexts: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in obs:
        community = clean(row.get("COMMUNITY"))
        visit = clean(row.get("visita"))
        if community and visit:
            contexts[(community, visit)].append(row)

    output: list[dict[str, object]] = []
    systems_seen = set()
    for (community, visit), subset in sorted(contexts.items()):
        census_durations: dict[str, set[float]] = defaultdict(set)
        values: dict[str, float] = defaultdict(float)
        partners = set()
        for row in subset:
            census = clean(row.get("censo"))
            duration = number(row.get("Delta_T_minutes"))
            if census:
                if duration is None or duration <= 0:
                    raise RuntimeError(f"{community}|{visit}|{census}: missing positive Delta_T_minutes")
                census_durations[census].add(duration)
            pollinator = clean(row.get("Pollinator"))
            n_ind = number(row.get("N ind"))
            if pollinator and n_ind is not None:
                if n_ind < 0:
                    raise RuntimeError(f"negative N ind in {community}|{visit}")
                partners.add(pollinator)
                if n_ind > 0:
                    values[pollinator] += n_ind

        inconsistent = {c: vals for c, vals in census_durations.items() if len(vals) != 1}
        if inconsistent:
            raise RuntimeError(f"inconsistent census durations in {community}|{visit}: {inconsistent}")
        effort = sum(next(iter(vals)) for vals in census_durations.values())
        if effort <= 0:
            raise RuntimeError(f"nonpositive context effort in {community}|{visit}")

        emitted = False
        for partner in sorted(partners):
            value = float(values.get(partner, 0.0))
            if value <= 0:
                continue
            output.append({
                "source_study_id": SOURCE_STUDY_ID,
                "archipelago_id": ARCHIPELAGO_ID,
                "system_id": community,
                "time_bin": visit,
                "partner_id": partner,
                "value": value,
                "effort": effort,
            })
            emitted = True
        if not emitted:
            raise RuntimeError(f"{community}|{visit}: sampled context has no positive pollinator interaction")
        systems_seen.add(community)

    if systems_seen != ADMITTED:
        raise RuntimeError(f"Cabrera admitted system drift: observed={sorted(systems_seen)} expected={sorted(ADMITTED)}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=None)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = adapt(load_bytes(args.source))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
