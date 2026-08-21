from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/results/thousand_island_lake_2022_source_audit.json"


def main() -> None:
    x = json.loads(RESULT.read_text())
    print("status", x.get("status"))
    print("source_admission", x.get("source_admission_succeeds"))
    print("source_bytes_ok", x.get("source_bytes_ok"))
    print("metadata_sha256", x.get("metadata_sha256"))
    print("file_count", x.get("file_count"))
    print("extracted_file_count", x.get("extracted_file_count"))
    print("signals", json.dumps(x.get("source_structure_signals"), sort_keys=True))
    for row in x.get("files", []):
        print(
            "ARCHIVE",
            row.get("key"),
            "bytes", row.get("bytes"),
            "md5", row.get("md5"),
            "sha256", row.get("sha256"),
            "md5_match", row.get("md5_match"),
        )
        for member in row.get("extracted_member_inventory", []):
            inv = member.get("inventory") or {}
            if inv.get("raw_pair_long_table_visible"):
                print(
                    "RAW_LONG_TABLE",
                    member.get("relative_path"),
                    "rows", inv.get("row_count"),
                    "headers", json.dumps(inv.get("candidate_headers"), ensure_ascii=False),
                    "roles", json.dumps(inv.get("field_role_candidates"), ensure_ascii=False, sort_keys=True),
                )
            elif inv.get("format") == "r_workspace" and (
                inv.get("list_element_matrix_like_count", 0) > 0
                or inv.get("matrix_or_dataframe_structure_line_count", 0) > 0
            ):
                print(
                    "R_WORKSPACE_STRUCTURE",
                    member.get("relative_path"),
                    "matrix_lines", inv.get("matrix_or_dataframe_structure_line_count"),
                    "matrix_elements", inv.get("list_element_matrix_like_count"),
                    "site_time_tokens", inv.get("site_time_name_token_line_count"),
                )


if __name__ == "__main__":
    main()
