from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/results/giannutri2025_daily_network_reconstruction_source.json"
URL = "https://zenodo.org/api/records/14855496/files/Code%20for%20Resource%20use%20and%20overlap%20analysis.R/content"
EXPECTED_MD5 = "b1eae37f3cada984dcbe439c75806c39"
EXPECTED_SHA256 = "a8b6a0acaa7a5082264d93f5ab01067d6fc79ab1a202d8ff06fd3b76eed79a39"
SOURCE_RANGES = ((150, 350),)


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        if int(response.status) != 200:
            raise RuntimeError(f"unexpected source status {response.status}")
        return response.read()


def main() -> None:
    payload = fetch()
    md5 = hashlib.md5(payload).hexdigest()
    sha256 = hashlib.sha256(payload).hexdigest()
    if md5 != EXPECTED_MD5 or sha256 != EXPECTED_SHA256:
        raise RuntimeError("Giannutri source R checksum drifted")
    text = payload.decode("utf-8-sig")
    lines = text.splitlines()
    selected = []
    for start, end in SOURCE_RANGES:
        if len(lines) < end:
            raise RuntimeError(f"source R shorter than frozen inspection range: {len(lines)} < {end}")
        selected.append({
            "start_line": start,
            "end_line": end,
            "lines": [
                {"line": index, "text": lines[index - 1]}
                for index in range(start, end + 1)
            ],
        })
    result = {
        "schema_version": "1.0",
        "analysis": "giannutri2025_daily_network_reconstruction_source_inspection",
        "source_url": URL,
        "source_md5": md5,
        "source_sha256": sha256,
        "source_line_count": len(lines),
        "inspection_ranges": selected,
        "target_metrics_calculated": False,
        "network_metrics_imported": False,
        "purpose": "Freeze the exact source-code reconstruction logic before defining or calculating izu-core Giannutri v6 target estimands.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
