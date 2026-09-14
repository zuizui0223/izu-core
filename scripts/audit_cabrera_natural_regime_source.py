from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_cabrera_natural_regime_source_audit_20260914.json"
CSV_URL = "https://digital.csic.es/bitstream/10261/420466/1/cabrera_22_23_habitat.csv"
CSV_SHA256 = "399ec11ae6ce18c8e9ebb050857ca7c1da4cb4a7858e24382750a92ae5e16a07"
USER_AGENT = "izu-core-source-audit/1.0"
PRIMARY_METHOD = "obs"
MIN_BINS = 6
MIN_SERIES = 3


def fetch() -> bytes:
    req = urllib.request.Request(CSV_URL, headers={"User-Agent": USER_AGENT, "Accept": "text/csv,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=90) as response:
        payload = response.read()
    observed = hashlib.sha256(payload).hexdigest()
    if observed != CSV_SHA256:
        raise RuntimeError(f"Cabrera source checksum drift: {observed}")
    return payload


def decode(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError("Cabrera source cannot be decoded")


def number(value: object) -> float | None:
    text = str(value or "").strip().replace(",", ".")
    if not text or text.lower() in {"na", "nan", "null", "none", "-"}:
        return None
    try:
        x = float(text)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def main() -> None:
    payload = fetch()
    rows = list(csv.DictReader(io.StringIO(decode(payload)), delimiter=";"))
    obs = [row for row in rows if clean(row.get("Method")) == PRIMARY_METHOD]

    contexts: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in obs:
        community = clean(row.get("COMMUNITY"))
        visit = clean(row.get("visita"))
        if community and visit:
            contexts[(community, visit)].append(row)

    community_visits: dict[str, list[str]] = defaultdict(list)
    context_effort: dict[str, dict[str, object]] = {}
    context_partner_totals: dict[tuple[str, str, str], float] = defaultdict(float)
    effort_consistent = True

    for (community, visit), subset in sorted(contexts.items()):
        community_visits[community].append(visit)
        census_durations: dict[str, set[float]] = defaultdict(set)
        for row in subset:
            census = clean(row.get("censo"))
            duration = number(row.get("Delta_T_minutes"))
            if census and duration is not None and duration > 0:
                census_durations[census].add(duration)
            pollinator = clean(row.get("Pollinator"))
            n_ind = number(row.get("N ind"))
            if pollinator and n_ind is not None and n_ind > 0:
                context_partner_totals[(community, visit, pollinator)] += n_ind

        inconsistent_censuses = {
            census: sorted(values)
            for census, values in census_durations.items()
            if len(values) != 1
        }
        missing_census_duration = sorted({
            clean(row.get("censo"))
            for row in subset
            if clean(row.get("censo")) and not (
                number(row.get("Delta_T_minutes")) is not None
                and number(row.get("Delta_T_minutes")) > 0
            )
        })
        effort = sum(next(iter(values)) for values in census_durations.values() if len(values) == 1)
        reconstructible = bool(census_durations) and not inconsistent_censuses and not missing_census_duration and effort > 0
        effort_consistent = effort_consistent and reconstructible
        context_effort[f"{community}|{visit}"] = {
            "unique_census_count_with_duration": len(census_durations),
            "effort_minutes": effort if reconstructible else None,
            "inconsistent_census_durations": inconsistent_censuses,
            "censuses_missing_positive_duration": missing_census_duration,
            "effort_reconstructible": reconstructible,
        }

    community_summary = {}
    admitted = []
    for community, visits in sorted(community_visits.items()):
        ordered_visits = sorted(set(visits), key=lambda x: int(x) if x.isdigit() else x)
        partners = sorted({
            partner
            for (c, _visit, partner), value in context_partner_totals.items()
            if c == community and value > 0
        })
        series = {partner: [] for partner in partners}
        all_effort = True
        for visit in ordered_visits:
            effort = context_effort[f"{community}|{visit}"]["effort_minutes"]
            if effort is None or effort <= 0:
                all_effort = False
                continue
            for partner in partners:
                series[partner].append(context_partner_totals.get((community, visit, partner), 0.0) / float(effort))
        nonconstant = [
            partner for partner, values in series.items()
            if len(values) == len(ordered_visits) and len({round(v, 15) for v in values}) > 1
        ]
        passes = len(ordered_visits) >= MIN_BINS and all_effort and len(nonconstant) >= MIN_SERIES
        if passes:
            admitted.append(community)
        community_summary[community] = {
            "time_bins": len(ordered_visits),
            "visits": ordered_visits,
            "all_context_effort_reconstructible": all_effort,
            "positive_partner_count": len(partners),
            "nonconstant_effort_standardized_partner_series": len(nonconstant),
            "passes_frozen_structure_gate": passes,
        }

    result = {
        "schema_version": "1.0",
        "analysis": "chapter2_cabrera_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source_sha256": CSV_SHA256,
        "primary_method": PRIMARY_METHOD,
        "source_rows": len(rows),
        "primary_method_rows": len(obs),
        "community_x_visit_contexts": len(contexts),
        "effort_definition_frozen_before_coordinates": "Within each source-observed obs COMMUNITY x visita, count each source-native censo once and sum its unique positive Delta_T_minutes. Repeated interaction rows within a censo do not multiply effort.",
        "all_contexts_effort_reconstructible": effort_consistent,
        "context_effort": context_effort,
        "communities": community_summary,
        "admitted_communities_before_coordinates": admitted,
        "admitted_system_count": len(admitted),
        "excluded_communities": sorted(set(community_summary) - set(admitted)),
        "gate_checks": {
            "minimum_time_bins": MIN_BINS,
            "minimum_nonconstant_partner_series": MIN_SERIES,
            "coordinates_opened": False,
        },
        "decision": "ADMIT_ELIGIBLE_COMMUNITIES_BEFORE_COORDINATES" if admitted else "FAIL_SOURCE_STRUCTURE_GATE",
        "claim_boundary": "This audit uses only source structure, durations, identities, and whether effort-standardized partner series vary. It does not compute D1, phi, rho_eq, route thresholds, or prior v8 target metrics."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
