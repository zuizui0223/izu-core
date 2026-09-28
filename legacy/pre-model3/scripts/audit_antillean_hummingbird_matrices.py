from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from pathlib import Path

ZIP = Path("data/external/antillean_hummingbird/Data_and_code.zip")
OUT = Path("data/results/antillean_hummingbird_matrix_audit.json")


def island_hint(name: str) -> str | None:
    low = name.lower()
    rules = [
        (r"dominica|dom[_\-. ]|syndicate", "Dominica"),
        (r"grenada|gren[_\-. ]", "Grenada"),
        (r"jamaica|jam[_\-. ]", "Jamaica"),
        (r"puerto|rico|pr[_\-. ]", "Puerto Rico"),
        (r"cuba", "Cuba"),
    ]
    for pat, island in rules:
        if re.search(pat, low):
            return island
    return None


def tabular_shape(data: bytes, name: str) -> dict:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            text = data.decode("latin-1")
        except Exception:
            return {"parse_status": "non_text_or_unknown_encoding"}
    candidates = [",", "\t", ";"]
    best = None
    for delim in candidates:
        rows = list(csv.reader(io.StringIO(text), delimiter=delim))
        widths = [len(r) for r in rows if r]
        if widths and max(widths) > 1:
            score = (sum(w == max(set(widths), key=widths.count) for w in widths), max(widths))
            if best is None or score > best[0]:
                best = (score, delim, rows)
    if best is None:
        return {"parse_status": "text_not_delimited", "line_count": len(text.splitlines())}
    _, delim, rows = best
    widths = [len(r) for r in rows if r]
    return {
        "parse_status": "delimited_text",
        "delimiter": {",": "comma", "\t": "tab", ";": "semicolon"}[delim],
        "row_count": len(rows),
        "max_columns": max(widths),
        "first_row": rows[0][:12] if rows else [],
    }


def main() -> None:
    if not ZIP.exists():
        payload = {
            "analysis": "antillean_hummingbird_matrix_audit",
            "status": "raw_archive_not_recovered",
            "fourth_stratum_ready": False,
        }
    else:
        matrices = []
        with zipfile.ZipFile(ZIP) as zf:
            for name in zf.namelist():
                if "/webs/" not in name.lower() or name.endswith("/"):
                    continue
                data = zf.read(name)
                matrices.append({
                    "path": name,
                    "island_hint_from_filename": island_hint(name),
                    "bytes": len(data),
                    **tabular_shape(data, name),
                })
        hints = {}
        for m in matrices:
            h = m["island_hint_from_filename"]
            if h:
                hints[h] = hints.get(h, 0) + 1
        dom_gren = all(hints.get(x, 0) > 0 for x in ("Dominica", "Grenada"))
        payload = {
            "analysis": "antillean_hummingbird_matrix_audit",
            "status": "raw_matrices_audited",
            "n_matrix_files": len(matrices),
            "island_hints": hints,
            "dominica_and_grenada_filename_support": dom_gren,
            "sampling_effort_gate": "pending_network_specific_source_mapping",
            "fourth_stratum_ready": False,
            "decision": "raw_matrices_recovered_but_final_stratum_admission_requires_network_specific_sampling_and_geology_mapping" if matrices else "no_web_matrices_found",
            "claim_boundary": "Filename hints are only routing aids and cannot establish island identity. Final admission requires source documentation connecting each matrix to a named island/site and a sampling-effort proxy; ABM outcomes are not inspected here.",
            "matrices": matrices,
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
