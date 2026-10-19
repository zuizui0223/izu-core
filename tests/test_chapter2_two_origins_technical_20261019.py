"""Source-compatible but technical-only island-assembly harness contracts."""
from __future__ import annotations

import math
from collections import defaultdict
from functools import lru_cache

import numpy as np
import pytest

from scripts.chapter2_two_origins_technical_20261019 import (
    HORIZON, POLICIES, REPEATS, Island, SourceLineage, attempt,
    score_binary, source_genotype, source_traits, stage_accounting,
    technical_fixture,
)


@lru_cache(maxsize=1)
def fixture():
    return technical_fixture()


def test_technical_fixture_is_bounded_and_not_scientific_evidence():
    d = fixture()
    assert d["status"] == "TECHNICAL_SMOKE_ONLY_NOT_SCIENTIFIC_EVIDENCE"
    assert d["registered_scientific_endpoints"] is False
    assert d["publication_claim_allowed"] is False
    assert d["competition"] is False
    assert d["immigration"] is False and d["mutation"] is False
    assert d["horizon"] == HORIZON == 6
    assert d["archipelago_resets"] == REPEATS == 2
    assert (d["lineages"], d["islands"]) == (6, 2)
    assert len(d["records"]) == 6 * 2 * REPEATS * len(POLICIES) == 96
    assert len(d["exact_stage_accounting"]) == 2 * REPEATS * len(POLICIES)
    assert all(r["technical_fixture_only"] is True for r in d["records"])


def test_arrival_and_native_establishment_are_common_across_later_policies():
    groups = defaultdict(list)
    for r in fixture()["records"]:
        groups[(r["island_id"], r["reset_id"], r["lineage_id"])].append(r)
    assert len(groups) == 24
    for values in groups.values():
        assert {r["policy"] for r in values} == set(POLICIES)
        assert len({r["arrived"] for r in values}) == 1
        assert len({r["established"] for r in values}) == 1
        assert len({tuple(sorted(r["source_traits"].items())) for r in values}) == 1
        for r in values:
            assert not r["persisted"] or r["established"]
            assert not r["established"] or r["arrived"]
            if r["persisted"]:
                assert r["final_expressed_traits"] is not None
                assert 0. <= r["final_expressed_traits"]["A"] <= 1.
                assert 0. <= r["final_expressed_traits"]["I"] <= 1.
                assert 1 <= r["terminal_abundance"] <= 12
            else:
                assert r["final_expressed_traits"] is None
                assert r["terminal_abundance"] == 0


def test_all_stage_arithmetic_exact_and_extinctions_not_zero_filled():
    for group in fixture()["exact_stage_accounting"]:
        for trait in ("A", "I"):
            d = group[trait]
            n = d["counts"]
            assert 0 <= n["persisted"] <= n["established"] <= n["arrived"] <= n["candidate"] == 6
            if n["persisted"] == 0:
                assert d["status"] == "EMPTY_STAGE_UNDEFINED_MEAN"
                assert d["contributions"] is None and d["total_change"] is None
                assert d["means"]["retained_final"] is None
            else:
                assert d["status"] == "DESCRIPTIVE_IDENTITY_NOT_CAUSAL"
                assert abs(math.fsum(d["contributions"].values()) -
                           d["total_change"]) < 1e-12
                assert abs(d["means"]["retained_final"] -
                           d["means"]["source"] -
                           d["total_change"]) < 1e-12


def test_expression_clamps_not_confused_with_fixed_genotypes_or_no_selfing():
    for r in fixture()["records"]:
        if not r["persisted"]:
            continue
        if r["policy"] in ("clamp_A", "clamp_A_I"):
            assert r["final_expressed_traits"]["A"] == r["source_traits"]["A"]
        if r["policy"] in ("clamp_I", "clamp_A_I"):
            assert r["final_expressed_traits"]["I"] == r["source_traits"]["I"]
        if r["policy"] == "clamp_A_I":
            assert r["final_expressed_traits"] == r["source_traits"]


def test_one_reset_repeatability_of_arrival_source_and_result():
    candidate = SourceLineage(71, .25, .65, 920711, 1.)
    island = Island("technical-reproducibility", 4.5, 0)
    x = attempt(candidate, island, 2)
    y = attempt(candidate, island, 2)
    assert x == y
    assert all(z["arrived"] for z in x)
    assert all(z["source_traits"] == source_traits(source_genotype(candidate)) for z in x)


def test_arrival_zero_is_not_imputed_as_extinction_after_establishment():
    candidate = SourceLineage(72, .75, .35, 920712, 0.)
    r = attempt(candidate, Island("technical-nonarrival", 4.5, 0), 2)
    assert len(r) == len(POLICIES)
    assert all(not z["arrived"] and not z["established"] and not z["persisted"] for z in r)
    assert all(z["final_expressed_traits"] is None for z in r)
    d = stage_accounting([r[0]], "A")
    assert d["status"] == "EMPTY_STAGE_UNDEFINED_MEAN"
    assert d["means"]["source"] is not None
    assert d["means"]["arrived"] is None and d["means"]["retained_final"] is None


def test_telescope_pure_synthetic_inventory_with_separate_filters():
    def row(id, source, arrived, established, persist, delta=0):
        return dict(lineage_id=id, island_id="synthetic", reset_id=0, policy="native",
                    source_traits=dict(A=source, I=source), arrived=arrived,
                    established=established, persisted=persist,
                    final_expressed_traits={"A": source + delta, "I": source + delta}
                    if persist else None)
    rows = [
        row(0, .1, False, False, False),
        row(1, .3, True, False, False),
        row(2, .5, True, True, False),
        row(3, .7, True, True, True, -.1),
    ]
    d = stage_accounting(rows, "I")
    assert d["status"] == "DESCRIPTIVE_IDENTITY_NOT_CAUSAL"
    assert d["counts"] == dict(candidate=4, arrived=3, established=2, persisted=1)
    assert abs(d["means"]["source"] - .4) < 1e-12
    assert abs(d["means"]["arrived"] - .5) < 1e-12
    assert abs(d["means"]["established"] - .6) < 1e-12
    assert abs(d["means"]["retained_source"] - .7) < 1e-12
    assert abs(d["means"]["retained_final"] - .6) < 1e-12
    assert abs(d["contributions"]["arrival"] - .1) < 1e-12
    assert abs(d["contributions"]["establishment"] - .1) < 1e-12
    assert abs(d["contributions"]["persistence_filter"] - .1) < 1e-12
    assert abs(d["contributions"]["within_retained_lineage"] + .1) < 1e-12
    assert abs(d["total_change"] - .2) < 1e-12


def test_invalid_contracts_fail_closed():
    with pytest.raises(ValueError):
        SourceLineage(1, 1.5, .5, 5, .5)
    with pytest.raises(ValueError):
        SourceLineage(1, .5, .5, 5, .5, propagules=9)
    with pytest.raises(ValueError):
        Island("x", 100., 0)
    with pytest.raises(ValueError):
        Island("x", 4.5, 3)
    with pytest.raises(ValueError):
        attempt(SourceLineage(3, .5, .5, 10, .5), Island("x", 4.5, 0),
                0, policies=["unknown"])
    with pytest.raises(ValueError):
        stage_accounting([], "A")
    with pytest.raises(ValueError):
        stage_accounting([dict(lineage_id=1)], "not-a-trait")


def test_proper_scores_available_only_with_predicted_outcomes():
    d = score_binary([0, 1], [.2, .8])
    assert d["n"] == 2 and abs(d["brier"] - .04) < 1e-12
    assert abs(d["log_loss"] + math.log(.8)) < 1e-12
    assert score_binary([0, 1], [0, 1])["brier"] == 0
    with pytest.raises(ValueError):
        score_binary([0, 1], [.2, 1.5])
    with pytest.raises(ValueError):
        score_binary([1, 1], [.2])
    with pytest.raises(ValueError):
        score_binary([], [])


def test_no_claim_of_native_SC_or_identified_colonization_in_module_docstring():
    import scripts.chapter2_two_origins_technical_20261019 as mod
    assert "TECHNICAL-ONLY" in mod.__doc__
    assert "NONINTERACTING" in mod.__doc__
    assert "not a claim about a mapped causal flower-size locus or SC" in mod._expressed_state.__doc__
