"""Bounded source-disjoint technical pilot, with no scientific inference."""
from __future__ import annotations

from functools import lru_cache
import math
import numpy as np

from scripts.chapter2_two_origins_disjoint_source_pilot_20261019 import (
    TECHNICAL_ONLY, PROTOCOL, DEMOGRAPHIC_RESETS, source_registry,
    island_registry, technical_screen, PREDICTORS,
)


@lru_cache(maxsize=1)
def readout():
    return technical_screen()


def test_source_ids_and_seeds_are_disjoint_across_train_validation_and_old_fixture():
    train = source_registry("train")
    hold = source_registry("heldout")
    assert len(train) == len(hold) == 24
    assert not ({z.lineage_id for z in train} & {z.lineage_id for z in hold})
    assert not ({z.source_seed for z in train} & {z.source_seed for z in hold})
    assert min(z.source_seed for z in train + hold) > 73005
    for split in (train, hold):
        strata = {}
        for z in split:
            k = (z.a_hint, z.i_hint)
            strata[k] = strata.get(k,0) + 1
        assert len(strata) == 6
        assert set(strata.values()) == {4}
        assert all(z.arrival_probability == .8 and z.propagules == 2 for z in split)


def test_island_budget_and_visitor_factors_crossed_not_confounded():
    x = island_registry()
    assert len(x) == 4
    assert {(z.ovule_budget,z.visitors) for z in x} == {
        (4.5,0), (4.5,4), (8.,0), (8.,4)
    }
    assert len({z.island_id for z in x}) == 4


def test_pilot_is_completed_as_technical_only_and_not_1536_independent_islands():
    d = readout()
    assert d["status"] == TECHNICAL_ONLY
    assert d["protocol"] == PROTOCOL
    assert d["official_scientific_confirmation"] is False
    assert d["statistical_significance_tested"] is False
    assert d["no_original_six_source_genotypes_reused"]
    assert d["no_interacting_species_or_empirical_self_compatibility"]
    assert d["technical_source_lineages_each_split"] == 24
    assert d["technical_islands"] == 4
    assert d["demographic_resets_per_source_island"] == DEMOGRAPHIC_RESETS == 8
    assert d["source_records_each_split"] == 768
    assert d["source_records_total"] == 1536


def test_all_candidate_fates_and_trait_means_are_conserved_across_resets():
    d = readout()
    keys = ("not_arrived","arrived_not_established",
            "established_then_extinct", "survivor_I_above_source_by_0p05",
            "survivor_I_below_source_by_0p05","survivor_I_within_0p05")
    for split in ("train", "heldout"):
        blocks = d["all_start_category_counts"][split]
        assert len(blocks) == 4
        for block in blocks.values():
            assert block["total"] == 24 * DEMOGRAPHIC_RESETS
            assert set(block["fates"]) == set(keys)
            assert sum(block["fates"].values()) == block["total"]
        stage = d["stage_summary_by_split"][split]
        assert len(stage) == 4 * DEMOGRAPHIC_RESETS
        for frame in stage:
            a, i = frame["A"], frame["I"]
            assert a["counts"] == i["counts"]
            count = a["counts"]
            assert 0 <= count["persisted"] <= count["established"] <= \
                count["arrived"] <= count["candidate"] == 24
            for z in (a,i):
                if z["contributions"] is None:
                    assert z["total_change"] is None
                    assert z["status"] == "EMPTY_STAGE_UNDEFINED_MEAN"
                else:
                    assert abs(math.fsum(z["contributions"].values()) -
                               z["total_change"]) < 1e-12


def test_validation_scores_are_finite_nonparametric_crosssource_and_no_leakage_flags():
    d = readout()
    records = d["heldout_prediction_scores"]
    assert len(records) == 3 * (len(PREDICTORS) + 1) - 1
    for endpoint in ("establishment_from_candidate",
                     "establishment_given_arrival",
                     "persistence_from_candidate"):
        subset = [x for x in records if x["endpoint"] == endpoint]
        expected = len(PREDICTORS) + (endpoint != "persistence_from_candidate")
        assert len(subset) == expected
        ecology = next(x for x in subset if x["model"] == "ecology_only")
        for r in subset:
            z = r["result"]
            assert 0 < z["n"] <= 768
            assert r["source_validation_groups"] == 24
            assert math.isfinite(z["brier"]) and 0 <= z["brier"] <= 1
            assert math.isfinite(z["log_loss"]) and z["log_loss"] >= 0
            assert 0 <= z["calibration_mean"] <= 1
            assert 0 <= z["event_rate"] <= 1
            assert abs(r["delta_brier_vs_ecology_only"] -
                       (z["brier"] - ecology["result"]["brier"])) < 1e-13
            if r["model"] == "native_full_genotype_probability_oracle":
                assert r["fitted_only_on_new_train_source_groups"] is False
            else:
                assert r["fitted_only_on_new_train_source_groups"] is True
        assert next(x for x in subset if x["model"]=="ecology_only")[
            "delta_brier_vs_ecology_only"] == 0.


def test_arrival_is_excluded_from_conditional_establishment_but_included_elsewhere():
    d = readout()
    n_candidate = {x["result"]["n"] for x in d["heldout_prediction_scores"]
                   if x["endpoint"]=="establishment_from_candidate"}
    n_arrived = {x["result"]["n"] for x in d["heldout_prediction_scores"]
                 if x["endpoint"]=="establishment_given_arrival"}
    assert n_candidate == {768}
    assert len(n_arrived)==1
    assert 0 < next(iter(n_arrived)) < 768
