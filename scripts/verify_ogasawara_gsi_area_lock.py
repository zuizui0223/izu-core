from __future__ import annotations

import hashlib
import io
import json
import re
import ssl
import urllib.request
from pathlib import Path

from pypdf import PdfReader

DESIGN = Path("data/design/ogasawara_gift_capacity_targets_v1.json")
OUT = Path("data/results/ogasawara_gsi_area_source_lock.json")

READINGS = {
    "A_Chichijima": "ちちじま",
    "B_Hahajima": "ははじま",
    "C_Anijima": "あにじま",
    "D_Ototojima": "おとうとじま",
}


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def gsi_ssl_context() -> ssl.SSLContext:
    """Permit the official GSI endpoint's legacy server renegotiation for this fetch only."""
    context = ssl.create_default_context()
    legacy_option = getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)
    context.options |= legacy_option
    return context


def main() -> None:
    design = json.loads(DESIGN.read_text())
    source = design["primary_area_source"]
    req = urllib.request.Request(
        source["url"],
        headers={"User-Agent": "izu-core-source-audit/1.0", "Accept": "application/pdf"},
    )
    with urllib.request.urlopen(req, timeout=120, context=gsi_ssl_context()) as response:
        payload = response.read()
    if not payload.startswith(b"%PDF"):
        raise RuntimeError("GSI area source did not return a PDF")

    reader = PdfReader(io.BytesIO(payload))
    target_page_index = None
    target_text = None
    for index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if all(name in text for name in ("父島", "母島", "兄島", "弟島")):
            target_page_index = index
            target_text = text
            break
    if target_page_index is None or target_text is None:
        raise RuntimeError("Could not identify GSI Tokyo island-area page containing all four Ogasawara targets")

    normalized = compact(target_text)
    checks = []
    for target in design["targets"]:
        island = target["source_island"]
        japanese = target["japanese_name"]
        reading = READINGS[island]
        area_text = f"{float(target['gsi_area_km2']):.2f}"
        pattern = re.compile(
            rf"{re.escape(japanese)}\s+{re.escape(reading)}\s+{re.escape(area_text)}(?:\s|$)"
        )
        matched = bool(pattern.search(normalized))
        checks.append({
            "source_island": island,
            "japanese_name": japanese,
            "reading": reading,
            "expected_area_km2": float(target["gsi_area_km2"]),
            "matched_in_source_pdf": matched,
        })
    verified = all(row["matched_in_source_pdf"] for row in checks)
    if not verified:
        raise RuntimeError(f"GSI area verification failed: {checks}")

    out = {
        "schema_version": "1.0",
        "status": "verified_authoritative_gsi_area_source",
        "source": source,
        "transport_note": "The official GSI host required TLS legacy-server-connect on the GitHub runner. The relaxed option is scoped only to this official source fetch; certificate verification remains enabled.",
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "pdf_page_index_zero_based": target_page_index,
        "pdf_page_number_one_based": target_page_index + 1,
        "checks": checks,
        "all_four_areas_verified": verified,
        "claim_boundary": "This verifies island identity and area only. It does not inspect or use pollination-network outcomes and does not validate the capacity hypothesis.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
