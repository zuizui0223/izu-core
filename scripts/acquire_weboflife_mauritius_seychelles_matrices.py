from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.web-of-life.es/get_networks.php"
OUT = Path("data/results/weboflife_mauritius_seychelles_matrix_gate.json")
RAW = Path("data/external/weboflife_mauritius_seychelles")

SYSTEMS = {
    "Mauritius_Black_River_Gorges": [f"M_PL_060_{i:02d}" for i in range(1, 25)],
    "Seychelles_Mahe": [f"M_PL_061_{i:02d}" for i in range(1, 49)],
}


def fetch_json(network_id: str, timeout: int = 60):
    url = BASE + "?" + urllib.parse.urlencode({"network_name": network_id})
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        final_url = r.geturl()
        ctype = r.headers.get("Content-Type", "")
    parsed = json.loads(data.decode("utf-8"))
    if isinstance(parsed, dict):
        rows = parsed.get("data") or parsed.get("rows") or []
    else:
        rows = parsed
    if not isinstance(rows, list):
        raise ValueError(f"unexpected payload for {network_id}")
    normalized = []
    for row in rows:
        if str(row.get("network_name")) != network_id:
            continue
        normalized.append({
            "network_name": network_id,
            "species1": str(row.get("species1") or ""),
            "species2": str(row.get("species2") or ""),
            "connection_strength": float(row.get("connection_strength") or 0),
        })
    if not normalized:
        raise ValueError(f"no source rows returned for {network_id}")
    return url, final_url, ctype, data, normalized


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "Web of Life dedicated API",
        "endpoint": BASE,
        "purpose": "Recover source-native weighted plant-pollinator edge lists for two frozen island systems. The 24/48 rows are within-system temporal/subnetwork replicates and never count as 72 independent global island systems.",
        "guild_boundary": "For these Pollination networks, Web of Life examples show animal pollinators in species1 and plants in species2. This gate stores raw labels and does not infer pollinator effectiveness from visitation strength.",
        "systems": {},
    }
    for system, ids in SYSTEMS.items():
        entries = []
        for network_id in ids:
            try:
                url, final_url, ctype, raw, rows = fetch_json(network_id)
                path = RAW / f"{network_id}.json"
                path.write_bytes(raw)
                entries.append({
                    "network_id": network_id,
                    "status": "retrieved",
                    "url": url,
                    "final_url": final_url,
                    "content_type": ctype,
                    "bytes": len(raw),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "n_edges": len(rows),
                    "n_species1": len({r['species1'] for r in rows}),
                    "n_species2": len({r['species2'] for r in rows}),
                    "total_connection_strength": sum(r['connection_strength'] for r in rows),
                    "path": str(path),
                })
            except Exception as exc:
                entries.append({"network_id": network_id, "status": "failed", "error": repr(exc)})
        payload["systems"][system] = {
            "requested_networks": len(ids),
            "retrieved_networks": sum(x["status"] == "retrieved" for x in entries),
            "all_retrieved": all(x["status"] == "retrieved" for x in entries),
            "entries": entries,
        }
    payload["admission"] = {
        "all_requested_bytes_recovered": all(x["all_retrieved"] for x in payload["systems"].values()),
        "status": "ready_for_within_system_architecture_summary" if all(x["all_retrieved"] for x in payload["systems"].values()) else "partial_source_recovery",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
