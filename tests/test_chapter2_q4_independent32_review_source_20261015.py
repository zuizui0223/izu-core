"""Q4A 32-history archival packet: original immutable source, no new simulation."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

import scripts.build_chapter2_unified_el_submission_bundle as builder

ROOT=Path(__file__).resolve().parents[1]
PINNED={
  "EVIDENCE/Q4_32_DESIGN.json": (
    "data/design/chapter2_island_demographic_independent32_20261008.json",
    "5f6c11aac76b93e1a67cbff1c971213fb08c7768"),
  "EVIDENCE/Q4_32_RESULT.json": (
    "data/results/chapter2_island_demographic_independent32_20261008.json",
    "5c46c3c3a1a0f02c9526b265590fc6a6de54005c"),
  "EVIDENCE/Q4_32_REPLAY_RECEIPT.json": (
    "data/results/chapter2_island_demographic_independent32_replay_receipt_20261013.json",
    "14a78981cd63dd2bf34799d3d76dc3adc417ca58"),
  "EVIDENCE/Q4_32_ORIGINAL_RUNNER.py": (
    "scripts/run_chapter2_island_demographic_independent32.py",
    "b5f9d42d8423092c1524a2ed33993ca4f7f0d725"),
}


def test_original_q4a_readout_sources_are_exact_and_safe():
    from scripts.verify_chapter2_q2_s29_source_bridge_20261015 import git_blob
    members,derivations=builder.q4_independent32_materials()
    assert set(members)==set(derivations)==set(PINNED)
    for destination,(path,git_sha) in PINNED.items():
        raw=(ROOT/path).read_bytes()
        assert git_blob(raw)==git_sha
        assert members[destination]==raw
        assert derivations[destination]["original_sha256"]==hashlib.sha256(raw).hexdigest()
        assert derivations[destination]["derived_sha256"]==derivations[destination]["original_sha256"]
        builder.validate_member(destination,raw)
    design=json.loads(members["EVIDENCE/Q4_32_DESIGN.json"])
    results=json.loads(members["EVIDENCE/Q4_32_RESULT.json"])
    replay=json.loads(members["EVIDENCE/Q4_32_REPLAY_RECEIPT.json"])
    assert design["independent_visitor_histories"]["count"]==32
    assert design["prehistories"]==400 and design["post_updates"]==80
    assert design["pre_mutation_rate"]==design["post_mutation_rate"]==.01
    assert results["post_switch_trajectories"]==4096
    assert results["predeclared_pooled_primary"]["mean"]==0.1083984375
    assert results["predeclared_pooled_primary"]["bootstrap95"]==[0.0654296875,0.1513671875]
    assert replay["validation"]["all_eight_biological_projection_hashes_exact"]
    assert replay["validation"]["pooled_primary_exact"]
    assert replay["validation"]["post_trajectories"]==4096


def test_blinded_S33_source_paths_are_resolved_in_builder():
    source=(ROOT/"docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md").read_text(encoding="utf-8")
    source=source.split("## S33. Independent 32-history",1)[1]
    assert "no natural island" in source.lower() or "no natural island survival rates" in source.lower()
    for path,_ in PINNED.values():
        assert (ROOT/path).is_file()
    build_source=(ROOT/"scripts/build_chapter2_unified_el_submission_bundle.py").read_text()
    assert "q4_independent32_materials()" in build_source
    assert "EVIDENCE/Q4_32_RESULT.json" in build_source
    assert "si_text=si_text.replace(old,new)" in build_source
