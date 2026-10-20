"""Bounded source-disjoint technical pilot, with no scientific inference."""
from __future__ import annotations

from functools import lru_cache
import math
import numpy as np

from scripts.audit_two_origins_heldout_source_blocks_20261020 import (
    STATUS as SOURCE_BLOCK_STATUS, source_block_bootstrap,
)

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



def test_emit_scoped_source_disjoint_technical_scores():
    x = readout()
    for d in x["heldout_prediction_scores"]:
        z = d["result"]
        print("SOURCE-DISJOINT TECHNICAL SCREEN ONLY:",
              d["endpoint"], d["model"], f"n={z['n']}",
              f"Brier={z['brier']:.6f}",
              f"delta_vs_ecology={d['delta_brier_vs_ecology_only']:+.6f}",
              f"logloss={z['log_loss']:.6f}",
              f"source_groups={d['source_validation_groups']}")
    print("NO SCIENTIFIC CONFIRMATION; NO HELD-OUT ISLAND-CLASS CLAIM;"
          " 24 new train + 24 new heldout artificial genotypes."
          " Four factorial synthetic island environments, eight nested repeats.")



def test_emit_scope_limited_heldout_stage_origin_terms():
    """These six-year descriptive means are NOT separate genetic causal mediators."""
    d = readout()
    frames = d["stage_summary_by_split"]["heldout"]
    by_island = {}
    for frame in frames:
        by_island.setdefault(frame["island"], []).append(frame)
    assert len(by_island) == 4
    for island, contexts in sorted(by_island.items()):
        assert len(contexts) == 8
        fates = d["all_start_category_counts"]["heldout"][island]
        print("SOURCE-DISJOINT STAGE SCREEN TECHNICAL ONLY",island,
              "candidate",fates["total"],
              "six_fates",fates["fates"])
        for trait in ("A","I"):
            valid = [x[trait]["contributions"] for x in contexts
                     if x[trait]["contributions"] is not None]
            if valid:
                selection = [
                    z["arrival"]+z["establishment"]+z["persistence_filter"]
                    for z in valid
                ]
                within = [z["within_retained_lineage"] for z in valid]
                print("TECHNICAL TRAIT ORIGIN",island,trait,
                      f"nonempty_resets={len(valid)}",
                      f"mean_filter={float(np.mean(selection)):+.6f}",
                      f"mean_within={float(np.mean(within)):+.6f}",
                      f"mean_absolute_filter={float(np.mean(np.abs(selection))):.6f}",
                      f"mean_absolute_within={float(np.mean(np.abs(within))):.6f}")
            else:
                print("TECHNICAL TRAIT ORIGIN",island,trait,"all_eight_resets_empty=True")



def test_source_blocked_Brier_uncertainty_keeps_all_32_paths_together():
    """All 8 stochastic resets × 4 environments per genotype stay clustered."""
    d = readout()
    src = d["heldout_persistence_source_losses"]
    assert d["source_blocked_inference_exploratory_and_fixed_training_models"] is True
    assert len(src)==24 and len({z["source_id"] for z in src})==24
    assert len({z["source_seed"] for z in src})==24
    assert sum(z["paths"] for z in src)==768
    assert {z["paths"] for z in src}=={32}
    records = {x["model"]:x for x in d["heldout_prediction_scores"]
               if x["endpoint"]=="persistence_from_candidate"}
    assert set(records)==set(PREDICTORS)
    for model in PREDICTORS:
        clustered=float(np.mean([z["brier_by_model"][model] for z in src]))
        aggregate=records[model]["result"]["brier"]
        assert abs(clustered-aggregate)<1e-13

    q = source_block_bootstrap(src)
    assert q["status"]==SOURCE_BLOCK_STATUS
    assert q["heldout_source_groups"]==24
    assert q["bootstrap_draws"]==4000
    assert q["source_groups_per_stratum"]==4
    assert q["bootstrap_refits_models"] is False
    assert q["iid_path_or_island_interpretation"] is False
    assert q["inferential_rank"].startswith("postoutcome exploratory")
    expected={
        "A_vs_ecology":records["ecology_A"]["delta_brier_vs_ecology_only"],
        "I_vs_ecology":records["ecology_I"]["delta_brier_vs_ecology_only"],
        "A_I_vs_ecology":records["ecology_A_I"]["delta_brier_vs_ecology_only"],
        "A_minus_I":records["ecology_A"]["result"]["brier"] -
                    records["ecology_I"]["result"]["brier"],
    }
    for name,truth in expected.items():
        est=q["comparisons"][name]
        assert abs(est["observed_mean_difference"]-truth)<1e-13
        low,high=est["conditional_source_bootstrap_percentile_95"]
        assert low<=high and np.isfinite([low,high]).all()
        assert 0<=est["fraction_resamples_improving_score"]<=1
        print("SOURCE-BLOCKED EXPLORATORY BRIER",name,
              f"delta={est['observed_mean_difference']:+.8f}",
              f"conditional_95=[{low:+.8f},{high:+.8f}]",
              f"bootstrap_improve_fraction={est['fraction_resamples_improving_score']:.4f}",
              "groups=24 source genotypes, within-stratum resample, TRAIN predictions fixed")
    # Determinism of this purely source-level bootstrap audit is enforceable.
    assert source_block_bootstrap(src) == q


def test_source_blocked_uncertainty_invalid_source_duplication_fails_closed():
    import pytest
    src = readout()["heldout_persistence_source_losses"]
    duplicate=[*src[:-1],src[0]]
    with pytest.raises(ValueError,match="duplicated"):
        source_block_bootstrap(duplicate)
    with pytest.raises(ValueError,match="source groups"):
        source_block_bootstrap(src[:23])
    with pytest.raises(ValueError,match="bootstrap replicate"):
        source_block_bootstrap(src,n_boot=2)
