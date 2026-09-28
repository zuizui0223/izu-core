from __future__ import annotations

import csv
import io
import json
import urllib.request
from pathlib import Path

OUT = Path("data/results/chapter2_mahe2014_natural_regime_source_audit_20260914.json")
WOL_META = "https://www.web-of-life.es/get_network_info.php"
WOL_MATRIX = "https://www.web-of-life.es/get_networks.php?network_name={network_id}"
FIGSHARE_COLLECTION = "https://api.figshare.com/v2/collections/3307269/articles"
NETWORK_PREFIX = "M_PL_061_"
ARTICLE_DOI = "10.1890/14-0024.1"


def get_bytes(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def get_json(url: str) -> object:
    return json.loads(get_bytes(url).decode("utf-8"))


def main() -> None:
    state: dict[str, object] = {
        "schema_version": "1.1",
        "analysis": "chapter2_mahe2014_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "article_doi": ARTICLE_DOI,
        "coordinates_opened": False,
    }

    text = get_bytes(WOL_META).decode("utf-8", errors="replace")
    rows = list(csv.DictReader(io.StringIO(text)))
    wol = [row for row in rows if (row.get("network_name") or "").startswith(NETWORK_PREFIX)]
    network_ids = sorted(row.get("network_name") for row in wol if row.get("network_name"))
    state["web_of_life"] = {
        "network_count": len(wol),
        "network_ids": network_ids,
        "locations": sorted({row.get("location") for row in wol if row.get("location")}),
        "countries": sorted({row.get("country") for row in wol if row.get("country")}),
        "references": sorted({row.get("reference") for row in wol if row.get("reference")}),
        "weighted_flags": sorted({row.get("is_weighted") for row in wol}),
    }

    # Inspect only the serialization/schema of the first matrix. No diversity,
    # synchrony, determinant or route metric is calculated here.
    if network_ids:
        raw = get_bytes(WOL_MATRIX.format(network_id=network_ids[0])).decode("utf-8-sig", errors="replace")
        state["wol_matrix_format_probe"] = {
            "network_id": network_ids[0],
            "first_lines": raw.splitlines()[:8],
            "bytes": len(raw.encode("utf-8")),
        }

    figshare_attempts = []
    articles: list[dict] = []
    try:
        collection = get_json(FIGSHARE_COLLECTION)
        if isinstance(collection, list):
            for entry in collection:
                if not isinstance(entry, dict):
                    continue
                article_id = entry.get("id")
                if article_id is None:
                    continue
                url = f"https://api.figshare.com/v2/articles/{article_id}"
                try:
                    meta = get_json(url)
                    if isinstance(meta, dict):
                        articles.append({
                            "id": article_id,
                            "title": meta.get("title"),
                            "doi": meta.get("doi"),
                            "description": meta.get("description"),
                            "files": [
                                {
                                    "id": f.get("id"),
                                    "name": f.get("name"),
                                    "size": f.get("size"),
                                    "download_url": (f.get("download_url") or f.get("download_url_private")),
                                }
                                for f in (meta.get("files") or []) if isinstance(f, dict)
                            ],
                        })
                    figshare_attempts.append({"url": url, "status": "ok"})
                except Exception as exc:
                    figshare_attempts.append({"url": url, "status": "failed", "error": repr(exc)})
        state["figshare_collection_status"] = "ok"
    except Exception as exc:
        state["figshare_collection_status"] = "failed"
        state["figshare_collection_error"] = repr(exc)
    state["figshare_articles"] = articles
    state["figshare_attempts"] = figshare_attempts

    state["published_design_contract"] = {
        "sites": 6,
        "months": 8,
        "expected_site_month_networks": 48,
        "study_window": "September 2007 through April 2008",
        "interaction_weight": "mean visitation frequency per flower per observation time",
        "observation_effort_note": "each woody flowering plant species approximately 3 h per site and month; total observation time varied among networks but the published interaction weight is effort-standardized",
        "published_fingerprint_fields": ["plant_species", "pollinator_taxa", "links", "total_interaction_frequency"],
    }

    file_names = [str(f.get("name") or "") for a in articles for f in a.get("files", [])]
    explicit_candidate = any(
        any(token in name.casefold() for token in ("data", "network", "interaction", "matrix", "table"))
        and not name.casefold().endswith(".pdf")
        for name in file_names
    )
    state["decision"] = (
        "SOURCE_FILE_CANDIDATE_PRESENT_NEXT_VERIFY_SITE_MONTH_MAPPING"
        if explicit_candidate
        else "WOL_48_MATRICES_PRESENT_BUT_SOURCE_NATIVE_SITE_MONTH_MAPPING_REQUIRES_FROZEN_FINGERPRINT_LINKAGE"
    )
    state["claim_boundary"] = (
        "This audit opens only source metadata, file inventories and one matrix serialization probe. The 48 Web of Life matrices are not assigned to sites or months from D1, phi, diversity, synchrony or route effects. Any next mapping must be frozen in advance and use only the four Appendix-B identity fingerprints: plant count, pollinator count, positive-link count and total interaction frequency."
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(state, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
