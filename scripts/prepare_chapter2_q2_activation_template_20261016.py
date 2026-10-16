"""Prepare a complete, source-bound Q2 activation *template*, never an approval.

This procedure runs no Model 3 biology. It records the current source+design
fingerprints so the researcher can review a transparent 384-case proposal.
Output is deliberately NOT the manually dispatched approved activation file.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.chapter2_q2_i_support_order_20261016 import (
    DEFAULT_DESIGN, ROOT, PIN_PATH, load_protocol, sha, source_manifest,
)
from scripts.run_chapter2_q2_i_support_production_20261016 import SOURCE_PATH, admission


def approval_template(design_path: Path = DEFAULT_DESIGN) -> dict:
    design_path = Path(design_path)
    d = load_protocol(design_path)
    files = source_manifest(design_path)
    files[str(SOURCE_PATH.relative_to(ROOT))] = sha(SOURCE_PATH.read_bytes())
    digest = sha(json.dumps(files, sort_keys=True).encode("utf-8"))
    return {
        "schema": "chapter2_q2_i_support_activation_proposal_v1",
        "status": "PENDING_AUTHOR_REVIEW_NOT_APPROVED",
        "owner_explicit_approval": False,
        "approval_is_new_not_reused": False,
        "study": "ch2_q2_I_support_order_20261016",
        "declared_full_cases": len(d["policies"]) * d["founders"]["count"] *
                                d["visitors"]["count"] * len(d["visitors"]["arms"]),
        "model_baseline_sha": d["source_baseline_commit"],
        "source_pin_receipt_sha256": sha(PIN_PATH.read_bytes()),
        "design_sha256": sha(design_path.read_bytes()),
        "source_manifest_sha256": digest,
        "original_model_source_files_pinned": 25,
        "scope": "384 new 200-update finite-diploid trajectories; 8 founders x 8 visitor histories x 2 environments x 3 I policies",
        "owner_signoff": None,
        "authorization_history": [],
        "not_an_activation": "Never execute without separate owner-approved activated record; this proposal must be reviewed and dated first.",
        "no_biological_runs": True,
    }


def write_pending_template(out: Path, design_path: Path = DEFAULT_DESIGN) -> dict:
    out = Path(out)
    if out.exists():
        raise FileExistsError("Refuse approval-template overwrite")
    proposal = approval_template(design_path)
    if proposal["declared_full_cases"] != 384:
        raise ValueError("Incorrect frozen design task count")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(proposal, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                   encoding="utf-8")
    # Fail-closed negative admission: a template must never authorize production.
    try:
        admission(out, design_path)
    except ValueError as exc:
        if "HOLD" not in str(exc):
            raise
    else:
        raise AssertionError("SECURITY: pending template unexpectedly authorized biology")
    return proposal


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=DEFAULT_DESIGN)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    p = write_pending_template(args.out, args.design)
    print(json.dumps({"status": p["status"], "cases": p["declared_full_cases"],
                      "approval": p["owner_explicit_approval"],
                      "source_pins": p["original_model_source_files_pinned"]}))


if __name__ == "__main__":
    main()
