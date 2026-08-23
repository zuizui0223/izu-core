from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/design/nicotiana_source_artifact_recovery_gate.json"
DEFAULT_OUTPUT = ROOT / "data/results/nicotiana_source_artifact_recovery.json"
MAX_BYTES = 30 * 1024 * 1024


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def classify_payload(payload: bytes, content_type: str | None) -> str:
    if payload.startswith(b"%PDF-"):
        return "recovered_pdf"
    if content_type and "application/pdf" in content_type.lower():
        return "claimed_pdf_but_missing_pdf_magic"
    return "recovered_non_pdf"


def fetch_source(source: dict[str, object], *, timeout: int = 30) -> dict[str, object]:
    url = str(source["retrieval_url"])
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "izu-core-source-audit/1.0 (+https://github.com/zuizui0223/izu-core)",
            "Accept": "application/pdf,text/html;q=0.8,*/*;q=0.5",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read(MAX_BYTES + 1)
            if len(payload) > MAX_BYTES:
                return {
                    "source_id": source["source_id"],
                    "requested_url": url,
                    "final_url": response.geturl(),
                    "http_status": getattr(response, "status", None),
                    "state": "blocked_payload_exceeds_limit",
                    "bytes": len(payload),
                    "sha256": None,
                }
            content_type = response.headers.get("Content-Type")
            state = classify_payload(payload, content_type)
            return {
                "source_id": source["source_id"],
                "requested_url": url,
                "final_url": response.geturl(),
                "http_status": getattr(response, "status", None),
                "content_type": content_type,
                "state": state,
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "pdf_magic": payload.startswith(b"%PDF-"),
            }
    except urllib.error.HTTPError as error:
        return {
            "source_id": source["source_id"],
            "requested_url": url,
            "final_url": error.geturl(),
            "http_status": error.code,
            "state": "blocked_http_status",
            "bytes": 0,
            "sha256": None,
        }
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return {
            "source_id": source["source_id"],
            "requested_url": url,
            "final_url": None,
            "http_status": None,
            "state": "blocked_transport_error",
            "error_type": type(error).__name__,
            "bytes": 0,
            "sha256": None,
        }


def build(*, timeout: int = 30) -> dict[str, object]:
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    sources = gate["sources"]
    results = [fetch_source(source, timeout=timeout) for source in sources]
    by_id = {str(row["source_id"]): row for row in results}
    recovered = [row["source_id"] for row in results if row["state"] == "recovered_pdf"]
    if len(recovered) == len(results):
        decision = "both_primary_pdf_artifacts_recovered_checksum_lock_ready"
    elif by_id["schueller_2004_self_pollination"]["state"] == "recovered_pdf":
        decision = "2004_source_recovered_2007_effectiveness_source_still_blocked"
    else:
        decision = "source_artifact_recovery_incomplete_keep_nicotiana_mapping_unadmitted"
    return {
        "analysis": "nicotiana_source_artifact_recovery",
        "checked_sources": len(results),
        "recovered_pdf_sources": recovered,
        "results": results,
        "decision": decision,
        "formal_effectiveness_values_admitted": False,
        "network_context_mapping_ready": False,
        "claim_boundary": (
            "This transport audit only checks whether the declared stable primary-source routes return PDF bytes and records their hashes. "
            "It does not verify scientific table contents by itself and cannot promote indexed numeric values unless source identity is separately checked."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    result = build(timeout=args.timeout)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"decision": result["decision"], "results": result["results"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
