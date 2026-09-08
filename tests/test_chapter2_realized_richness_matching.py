import json

from scripts.audit_chapter2_realized_richness_matching import (
    DESIGN,
    match_trajectories,
    verify_design,
)


def test_realized_richness_design_is_frozen_and_source_locked():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    assert design["status"] == "fixed_before_execution"
    assert design["baseline"]["matched_community_realizations"] == 96
    assert design["baseline"]["steps"] == 120
    assert design["matching_policy"]["target_richness"] == (
        "min(realized_mainland_richness, realized_island_richness)"
    )
    assert design["matching_policy"]["response_information_used_for_matching"] is False
    assert len(design["matching_rng"]["seeds"]) == 6
    verify_design(design)


def test_stepwise_matching_forces_exact_richness_without_adding_members():
    design = json.loads(DESIGN.read_text(encoding="utf-8"))
    mainland = (("m1", "m2", "m3"), ("m1",), (), ("m1", "m2"))
    island = (("i1",), ("i1", "i2"), ("i1",), ("i1", "i2"))
    matched_mainland, matched_island, audit = match_trajectories(
        mainland,
        island,
        matching_seed=design["matching_rng"]["primary_seed"],
        replicate_index=0,
        design=design,
    )
    assert [len(row) for row in matched_mainland] == [1, 1, 0, 2]
    assert [len(row) for row in matched_island] == [1, 1, 0, 2]
    assert audit["unequal_after_matching"] == 0
    assert set(member for row in matched_mainland for member in row) <= {"m1", "m2", "m3"}
    assert set(member for row in matched_island for member in row) <= {"i1", "i2"}
