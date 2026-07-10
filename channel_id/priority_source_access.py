"""Access-route parsing for the predeclared priority source queue.

This module only classifies legal access routes.  It never promotes metadata,
abstracts, or a downloadable file into a trait observation.
"""
from __future__ import annotations

import json
from typing import Iterable


def _clean(value: object) -> str:
    return str(value or "").strip()


def flatten_locations(payload: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for location in payload.get("locations") or []:
        if not isinstance(location, dict):
            continue
        source = location.get("source") or {}
        if not isinstance(source, dict):
            source = {}
        pdf = _clean(location.get("pdf_url"))
        landing = _clean(location.get("landing_page_url"))
        key = (pdf, landing)
        if key in seen or (not pdf and not landing):
            continue
        seen.add(key)
        rows.append({
            "pdf_url": pdf,
            "landing_page_url": landing,
            "source_name": _clean(source.get("display_name")),
            "source_type": _clean(source.get("type")),
            "is_oa": "yes" if location.get("is_oa") else "no",
            "version": _clean(location.get("version")),
            "license": _clean(location.get("license")),
        })
    return rows


def summarize_openalex(payload: dict[str, object]) -> dict[str, str]:
    open_access = payload.get("open_access") or {}
    if not isinstance(open_access, dict):
        open_access = {}
    best = payload.get("best_oa_location") or {}
    if not isinstance(best, dict):
        best = {}
    source = best.get("source") or {}
    if not isinstance(source, dict):
        source = {}
    locations = flatten_locations(payload)
    oa_pdfs = [row for row in locations if row["is_oa"] == "yes" and row["pdf_url"]]
    oa_landings = [row for row in locations if row["is_oa"] == "yes" and row["landing_page_url"]]
    if oa_pdfs:
        next_action = "download_and_inspect_legal_OA_PDF"
        access_class = "oa_pdf"
    elif oa_landings:
        next_action = "inspect_OA_landing_or_repository"
        access_class = "oa_landing"
    else:
        next_action = "institutional_library_or_author_request"
        access_class = "library_or_author"
    return {
        "openalex_id": _clean(payload.get("id")),
        "title": _clean(payload.get("display_name")),
        "publication_year": _clean(payload.get("publication_year")),
        "is_oa": "yes" if open_access.get("is_oa") else "no",
        "oa_status": _clean(open_access.get("oa_status")),
        "best_oa_pdf_url": _clean(best.get("pdf_url")),
        "best_oa_landing_url": _clean(best.get("landing_page_url")),
        "best_oa_source": _clean(source.get("display_name")),
        "access_class": access_class,
        "next_action": next_action,
        "all_locations_json": json.dumps(locations, ensure_ascii=False, sort_keys=True),
        "location_count": str(len(locations)),
        "oa_pdf_location_count": str(len(oa_pdfs)),
        "oa_landing_location_count": str(len(oa_landings)),
    }


def select_oa_pdf_urls(rows: Iterable[dict[str, str]]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for row in rows:
        try:
            locations = json.loads(row.get("all_locations_json", "[]"))
        except json.JSONDecodeError:
            locations = []
        for location in locations:
            url = _clean(location.get("pdf_url")) if isinstance(location, dict) else ""
            is_oa = location.get("is_oa") == "yes" if isinstance(location, dict) else False
            if url and is_oa and url not in seen:
                seen.add(url); output.append(url)
    return output
