"""Model 3 two-proposition assertions: math support law vs archived data.

The 8-founder original 1,088-path campaign is replay-read only in the
separate exact-artifact scientific gate. These unit tests do NOT constitute
a second biological campaign or a new prospective inference family.
"""
from __future__ import annotations

from copy import deepcopy
import json

import numpy as np
import pytest

from scripts.audit_chapter2_two_propositions_20261016 import (
    RECEIPT, ROOT, source_gate,
)
from scripts.model3_island.population import inherit
from scripts.run_chapter2_assurance_generality import (
    DEFAULT_DESIGN, config, founders, load_design,
)


def _evidence():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_original_sources_and_distinct_inference_units_are_admitted():
    r = source_gate()
    assert r["historical_q1_first_crossing"] == 51
    assert r["historical_Q1_four_settings"] == 4
    assert r["source_bound_width_rows"] == 36
    assert r["original_standing_access_histories"] == 2304
    assert r["pre_fixation_exclusion"] == 703
    assert r["loss_selected_transitions"] == 1238
    assert r["favourably_weighted_but_realized_loss"] == 315
    assert "NOT_INDEPENDENT_BIOLOGICAL" in r["evidence_level"]


def test_tampered_source_readout_cannot_become_new_scientific_proof():
    d = _evidence()
    d["support_loss"]["excluded_before_fixation"] = 704
    with pytest.raises(ValueError, match="source|excluded|Historical|evidence"):
        source_gate(receipt=d)
    d = _evidence()
    d["allele_half_width_order_exploration"]["halfw"][1]["assurance_first"] = 945
    with pytest.raises(ValueError, match="h-width"):
        source_gate(receipt=d)


def test_mendelian_no_mutation_no_immigration_support_cannot_expand():
    """Pass through ORIGINAL offspring transmission with no mutation 3 loci."""
    from dataclasses import replace

    d = load_design(DEFAULT_DESIGN)
    pop = founders(d)
    # One explicitly heterozygous assurance background, centered at 0.5.
    h = .046875
    genes = pop.alleles.copy()
    genes[:, 2, 0] = .5 - h
    genes[:, 2, 1] = .5 + h
    pop = replace(pop, alleles=genes)
    cfg = config(d, "assurance_cost", 0., "evolving")
    assert cfg.mutation_rate == 0.
    start = [set(pop.alleles[:, k, :].ravel()) for k in range(3)]
    rng_seg=np.random.default_rng(20101601)
    rng_mut=np.random.default_rng(20101602)
    for year in range(1,11):
        previous = [set(pop.alleles[:,k,:].ravel()) for k in range(3)]
        mothers=np.arange(48,dtype=int)
        fathers=np.roll(mothers,1)
        pop=inherit(pop,mothers,fathers,cfg,segregation_rng=rng_seg,
                    mutation_rng=rng_mut,year=year,
                    mutation_traits=(False,False,False))
        for locus in range(3):
            updated = set(pop.alleles[:,locus,:].ravel())
            assert updated.issubset(previous[locus])
            assert updated.issubset(start[locus])
            assert min(start[locus]) <= float(pop.alleles[:,locus,:].mean()) <= max(start[locus])
        assert .5-h <= float(pop.alleles[:,2,:].mean()) <= .5+h


def test_accessibility_at_d025_is_not_interpreted_as_variance_only_causality():
    d=_evidence()["allele_half_width_order_exploration"]
    assert d["threshold"] == .025
    narrow,wide=d["halfw"]
    assert narrow["without_mutation_threshold_reachable"] is True
    assert wide["without_mutation_threshold_reachable"] is True
    assert narrow["all_start_D"] == pytest.approx(-437/3072)
    assert wide["all_start_D"] == pytest.approx(676/3072)
    assert d["experiment_allows_A_mutation"] is True
    assert d["n_starts_per_width"] == 3072
    assert d["original_unique_biological_paths"] == 6144


def test_new_founder_nonnecessity_is_not_same_as_four_way_attenuation():
    evidence=_evidence()
    f=evidence["fresh_founder_q1"]
    assert f["original_32_shard_case_count"] == 1088
    assert f["positive_mutation_main_paths_SHA256_admitted"] == 1024
    assert f["original_null_pairs_exact"] == 32
    for s in f["settings"]:
        assert s["fixed_far_minus_near_mean"] < 0
        assert s["fixed_far_minus_near_bootstrap95"][1] < 0
        assert s["fixed_far_change_from_actual_founder_mean"] < 0
        assert s["fixed_far_change_bootstrap95"][1] < 0
        assert s["negative_fixed_founder_means"] == 8
    direct = next(s for s in f["settings"] if s["setting"]=="assurance_cost")
    assert direct["original_D"]>0
    # The actual 8-founder D interval includes zero (separate registered test).
    assert evidence["fresh_founder_q1"]["global_support"].endswith("inconclusive")


def test_genetic_access_loss_is_not_double_counted_as_extra_history():
    s=_evidence()["support_loss"]
    assert s["cases"] == 2304
    assert s["first_exclusion_transitions"] + 1066 == 2304
    assert 315 + 923 == 1238
    assert s["excluded_before_fixation"] == 703
    assert s["among_703_preexisting_I_event"] == 1
    assert "same original" in s["inference_unit"]
    assert "not a prospective" in "315 / 1238 is outcome-conditioned on first-exclusion transitions from same 2304 histories, not a prospective allele-loss probability"


def test_density_finite_disagreement_remains_distinct_from_access_cohort():
    d = _evidence()["density_finite_realization"]
    assert d["realized_A_first"] == [3,2]
    assert d["realized_A_only"] == [15,7]
    assert d["total_original_ABM_histories"] == 320
    assert d["all_64_focal_ABM_occupied_at_update200"] is True
    assert "not proven to mediate" in d["inference_limit"]
