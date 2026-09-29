from __future__ import annotations

import csv
import io
import json
import math
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/chapter2_mauritius_temporal_natural_regime_source_audit_20260914.json"

NETWORK_IDS = [f"M_PL_060_{i:02d}" for i in range(1, 25)]
WOL_INFO = "https://www.web-of-life.es/get_network_info.php?network_name=M_PL_060"
WOL_NETWORK = "https://www.web-of-life.es/get_networks.php?network_name={network_id}"
ARTICLE_DOI = "10.1111/j.1461-0248.2009.01437.x"
SUPPLEMENT_FILE = "ELE_1437_sm_AppendixS6.xls"
WILEY_CANDIDATES = [
    "https://onlinelibrary.wiley.com/action/downloadSupplement?doi="
    + urllib.parse.quote(ARTICLE_DOI, safe="")
    + "&file="
    + urllib.parse.quote(SUPPLEMENT_FILE, safe=""),
    "https://onlinelibrary.wiley.com/doi/suppl/"
    + ARTICLE_DOI
    + "/supinfo/"
    + SUPPLEMENT_FILE,
]


def get_bytes(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-natural-regime-source-audit/1.0",
            "Accept": "*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def safe_number(value: object) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {
        "schema_version": "1.0",
        "analysis": "chapter2_mauritius_temporal_natural_regime_source_audit",
        "status": "source_structure_only_coordinates_not_opened",
        "source": {
            "article_doi": ARTICLE_DOI,
            "reference": "Kaiser-Bunbury et al. 2010 Ecology Letters 13:442-452",
            "archipelago": "Mauritius / Mascarene Islands",
            "published_design": "two sites with 12 consecutive 2-week temporal snapshots per site",
            "expected_network_rows": 24,
        },
        "coordinates_opened": False,
    }

    # Web of Life metadata: source/reference/weight semantics only.
    metadata_state: dict[str, object] = {"status": "not_recovered"}
    try:
        text = get_bytes(WOL_INFO).decode("utf-8-sig", errors="replace")
        rows = list(csv.DictReader(io.StringIO(text)))
        rows = [row for row in rows if row.get("network_name") in NETWORK_IDS]
        metadata_state = {
            "status": "recovered",
            "row_count": len(rows),
            "network_ids": sorted(row.get("network_name") for row in rows if row.get("network_name")),
            "locations": sorted({row.get("location", "") for row in rows}),
            "countries": sorted({row.get("country", "") for row in rows}),
            "references": sorted({row.get("reference", "") for row in rows}),
            "is_weighted_values": sorted({row.get("is_weighted", "") for row in rows}),
            "cell_values_descriptions": sorted({row.get("cell_values_description", "") for row in rows}),
            "abundance_descriptions": sorted({row.get("abundance_description", "") for row in rows}),
        }
    except Exception as exc:
        metadata_state = {"status": "failed", "error": repr(exc)}
    result["web_of_life_metadata"] = metadata_state

    # Recover interaction rows without computing any natural-regime coordinate.
    network_audits = []
    union_resource: set[str] = set()
    union_partner: set[str] = set()
    all_strengths: list[float] = []
    for network_id in NETWORK_IDS:
        audit: dict[str, object] = {"network_id": network_id, "status": "not_recovered"}
        try:
            payload = json.loads(get_bytes(WOL_NETWORK.format(network_id=network_id)))
            if isinstance(payload, dict):
                # Some deployments wrap rows in a top-level key.
                for key in ("data", "rows", "network"):
                    if isinstance(payload.get(key), list):
                        payload = payload[key]
                        break
            if not isinstance(payload, list):
                raise RuntimeError(f"unexpected Web of Life payload type: {type(payload)!r}")
            strengths = []
            resources: set[str] = set()
            partners: set[str] = set()
            for row in payload:
                if not isinstance(row, dict):
                    continue
                s1 = str(row.get("species1") or "").strip()
                s2 = str(row.get("species2") or "").strip()
                value = safe_number(row.get("connection_strength"))
                if s1:
                    resources.add(s1)
                if s2:
                    partners.add(s2)
                if value is not None:
                    strengths.append(value)
            union_resource.update(resources)
            union_partner.update(partners)
            all_strengths.extend(strengths)
            audit.update({
                "status": "recovered",
                "interaction_rows": len(payload),
                "resource_labels": len(resources),
                "partner_labels": len(partners),
                "numeric_strength_rows": len(strengths),
                "positive_strength_rows": sum(value > 0 for value in strengths),
                "strength_min": min(strengths) if strengths else None,
                "strength_max": max(strengths) if strengths else None,
            })
        except Exception as exc:
            audit.update({"status": "failed", "error": repr(exc)})
        network_audits.append(audit)

    recovered_count = sum(row["status"] == "recovered" for row in network_audits)
    result["web_of_life_interactions"] = {
        "expected_network_count": len(NETWORK_IDS),
        "recovered_network_count": recovered_count,
        "network_audits": network_audits,
        "union_resource_labels": len(union_resource),
        "union_partner_labels": len(union_partner),
        "numeric_strength_rows_total": len(all_strengths),
        "all_numeric_strengths_nonnegative": bool(all_strengths) and all(value >= 0 for value in all_strengths),
        "claim_boundary": "Only source structure, labels and weight availability are inspected; D1, phi, rho_eq and route effects are not computed.",
    }

    # Try to recover the peer-reviewed Appendix S6 that carries the temporal-network mapping.
    supplement_state: dict[str, object] = {
        "filename": SUPPLEMENT_FILE,
        "status": "not_recovered",
        "attempts": [],
    }
    for url in WILEY_CANDIDATES:
        try:
            blob = get_bytes(url, timeout=120)
            attempt = {"url": url, "bytes": len(blob), "prefix_hex": blob[:8].hex()}
            # Legacy XLS is an OLE compound file.
            if not blob.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
                attempt["status"] = "not_legacy_xls_payload"
                supplement_state["attempts"].append(attempt)
                continue
            import xlrd

            book = xlrd.open_workbook(file_contents=blob, on_demand=True)
            sheets = []
            for sheet in book.sheets():
                sample = []
                for r in range(min(sheet.nrows, 8)):
                    sample.append([sheet.cell_value(r, c) for c in range(min(sheet.ncols, 12))])
                sheets.append({
                    "name": sheet.name,
                    "nrows": sheet.nrows,
                    "ncols": sheet.ncols,
                    "first_rows": sample,
                })
            supplement_state.update({
                "status": "recovered_valid_legacy_xls",
                "transport_url": url,
                "bytes": len(blob),
                "sheet_count": len(sheets),
                "sheets": sheets,
            })
            attempt["status"] = "recovered_valid_legacy_xls"
            supplement_state["attempts"].append(attempt)
            break
        except Exception as exc:
            supplement_state["attempts"].append({"url": url, "status": "failed", "error": repr(exc)})
    result["published_appendix_s6"] = supplement_state

    metadata_complete = metadata_state.get("status") == "recovered" and metadata_state.get("row_count") == 24
    interactions_complete = recovered_count == 24 and bool(all_strengths)
    appendix_recovered = supplement_state.get("status") == "recovered_valid_legacy_xls"

    result["gate_checks"] = {
        "public_machine_readable_interaction_rows": interactions_complete,
        "twenty_four_weighted_network_rows": metadata_complete and interactions_complete,
        "published_two_site_by_twelve_bin_design": True,
        "stable_partner_labels_across_snapshots_reconstructible": interactions_complete,
        "source_native_site_and_chronological_snapshot_mapping_recovered": appendix_recovered,
        "sampling_effort_or_source_normalized_weight_semantics_recovered": bool(
            metadata_complete
            and any(
                str(value).strip()
                for value in metadata_state.get("cell_values_descriptions", [])
            )
        ),
        "coordinates_opened": False,
    }

    if metadata_complete and interactions_complete and appendix_recovered:
        decision = "SOURCE_BYTES_PASS_NEXT_FREEZE_SITE_TIME_WEIGHT_MAPPING"
    elif metadata_complete and interactions_complete:
        decision = "WOL_TEMPORAL_MATRICES_RECOVERED_MAPPING_OR_EFFORT_SEMANTICS_STILL_REQUIRED"
    else:
        decision = "FAIL_OR_TRANSPORT_BLOCKED_REQUIRES_SOURCE_DIAGNOSIS"
    result["decision"] = decision
    result["biological_negative"] = False
    result["next_gate"] = (
        "Before any D1/phi calculation, verify a source-native mapping of the 24 Web of Life matrices to the two Mauritius sites and their 12 chronological two-week bins, and verify that quantitative weights are comparable across bins by source normalization or explicit effort. No ordering may be inferred from observed network values."
    )
    result["claim_boundary"] = (
        "The 24 Web of Life network IDs were selected only because the frozen outcome-blind metadata pool assigns them to the Kaiser-Bunbury 2010 Mauritius source. This audit does not treat 24 networks as 24 independent systems, does not compute breadth or synchrony, and does not infer missing site/time labels from ecological values."
    )

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
