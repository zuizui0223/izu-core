from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

RDATA_URL = "https://raw.githubusercontent.com/MaelDore/Pollination_networks/master/Data/Filtered_Datasets/aggreg.webs_full.RData"


def download(url: str, path: Path, timeout: int = 60) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "izu-core-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def candidate_columns(cols: list[str], patterns: tuple[str, ...]) -> list[str]:
    return [c for c in cols if any(re.search(p, c, re.I) for p in patterns)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", type=Path, default=Path("data/external/dore2021/aggreg.webs_full.RData"))
    p.add_argument("--out", type=Path, default=Path("data/results/dore2021_global_network_pool_audit.json"))
    args = p.parse_args()

    payload = {
        "source": "Dore et al. global pollination-network compilation",
        "article_doi": "10.1111/gcb.15474",
        "data_repo": "MaelDore/Pollination_networks",
        "rdata_url": RDATA_URL,
        "status": "source_audit",
        "claim_boundary": "This audit inspects source columns and geography before selecting any island systems. No ABM outputs are used."
    }
    try:
        import pyreadr  # type: ignore
        download(RDATA_URL, args.raw)
        objects = pyreadr.read_r(str(args.raw))
        summaries = {}
        for name, df in objects.items():
            cols = [str(c) for c in df.columns]
            geo_cols = candidate_columns(cols, (r"lat", r"lon", r"coord", r"country", r"location", r"site", r"region"))
            sample_cols = candidate_columns(cols, (r"sampl", r"effort", r"hour", r"duration", r"method", r"year", r"month"))
            id_cols = candidate_columns(cols, (r"study", r"network", r"web", r"site", r"location", r"id$"))
            preview_cols = []
            for c in geo_cols + id_cols + sample_cols:
                if c not in preview_cols:
                    preview_cols.append(c)
            preview_cols = preview_cols[:14]
            preview = []
            if preview_cols:
                for _, row in df[preview_cols].head(20).iterrows():
                    preview.append({c: (None if str(row[c]) == 'nan' else str(row[c])) for c in preview_cols})
            summaries[name] = {
                "rows": int(len(df)),
                "columns": cols,
                "geography_candidate_columns": geo_cols,
                "sampling_candidate_columns": sample_cols,
                "id_candidate_columns": id_cols,
                "preview": preview,
            }
        payload["objects"] = summaries
        payload["status"] = "read_success"
    except Exception as exc:
        payload["status"] = "read_failed"
        payload["error"] = repr(exc)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
