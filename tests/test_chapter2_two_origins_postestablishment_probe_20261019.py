"""Technical-only independently seeded post-establishment A/I expression probe."""
from __future__ import annotations
from functools import lru_cache
import math
import numpy as np

from scripts.chapter2_two_origins_technical_20261019 import (
    SourceLineage, source_genotype, _center_A_expression_preserve_genotypic_spread
)

from scripts.chapter2_two_origins_postestablishment_probe_20261019 import (
    STATUS, new_source_registry, technical_policy_probe
)

@lru_cache(maxsize=1)
def readout():
    return technical_policy_probe()


def test_third_source_namespace_is_disjoint_from_prior_six_train_and_holdout():
    a=new_source_registry()
    assert len(a)==24
    assert {z.lineage_id for z in a}==set(range(30000,30024))
    assert {z.source_seed for z in a}==set(range(21030000,21030024))
    assert not ({z.source_seed for z in a} &
                (set(range(73000,73006)) | set(range(21010000,21010024)) |
                 set(range(21020000,21020024))))
    assert {z.a_hint for z in a}=={.2,.5,.8}
    assert {z.i_hint for z in a}=={.3,.7}


def test_all_candidate_and_policy_forks_share_establishment():
    d=readout()
    assert d["status"]==STATUS
    assert d["new_source_genotype_count"]==24
    assert d["candidate_assignments"]==768
    assert d["paired_policy_paths"]==3840
    assert set(d["technical_policy_roster"])=={"native","clamp_A","clamp_I","clamp_A_I","center_A_mean"}
    assert d["independent_demographic_resets_per_source_island"]==8
    assert d["primary_inference_performed"] is False
    assert d["causal_mediation_identified"] is False
    assert d["no_reused_prior_exposed_train_or_heldout_genotypes"] is True
    original={(r["island"],r["reset"],r["source_id"]) for r in d["groups"]}
    assert len(original)==768
    for r in d["groups"]:
        assert set(r["arms"])=={"native","clamp_A","clamp_I","clamp_A_I","center_A_mean"}
        assert not r["established"] or r["arrived"]
        for name,v in r["arms"].items():
            assert not v["alive"] or r["established"]
            if v["alive"]:
                assert 1 <= v["terminal_abundance"] <= 12
                assert v["final_traits"] is not None
                assert all(0<=x<=1 for x in v["final_traits"].values())
            else:
                assert v["terminal_abundance"]==0
                assert v["final_traits"] is None


def test_policy_counts_strata_and_paired_differences_conserve_denominators():
    d=readout()
    assert len(d["summary"])==4
    for island,x in d["summary"].items():
        b=x["all_source_strata"]
        assert b["n_candidates"]==192
        assert 0<=b["n_established"]<=b["n_arrived"]<=192
        assert len(x["by_source_A"])==3
        for key,v in x["by_source_A"].items():
            assert v["n_candidates"]==64
            assert 0<=v["n_established"]<=v["n_arrived"]<=64
        for q in [b,*x["by_source_A"].values()]:
            n=q["n_candidates"]
            for policy,counts in q["survival"].items():
                assert counts["all_candidates"]==n
                assert 0<=counts["persisted"]<=q["n_established"]
            for name,paired in q["paired"].items():
                assert sum(paired[k] for k in
                           ("both","native_only","policy_only","neither"))==n
                assert abs(paired["native_minus_clamped_pp"] -
                           100*(paired["native_only"]-paired["policy_only"])/n)<1e-12
                assert q["survival"]["native"]["persisted"] - \
                       q["survival"][name]["persisted"] == \
                       paired["native_only"]-paired["policy_only"]
        assert sum(v["n_candidates"] for v in x["by_source_A"].values()) == 192
        for policy in ("native","clamp_A","clamp_I","clamp_A_I","center_A_mean"):
            assert sum(v["survival"][policy]["persisted"]
                       for v in x["by_source_A"].values()) == \
                   b["survival"][policy]["persisted"]


def test_postestablishment_expression_clamps_retain_original_source_values():
    for r in readout()["groups"]:
        A,I=r["source_A"],r["source_I"]
        for name in ("clamp_A","clamp_I","clamp_A_I","center_A_mean"):
            arm=r["arms"][name]
            if not arm["alive"]:
                continue
            if name in ("clamp_A","clamp_A_I","center_A_mean"):
                assert arm["final_traits"]["A"]==A
            if name in ("clamp_I","clamp_A_I"):
                assert arm["final_traits"]["I"]==I



def test_center_A_mean_preserves_allele_and_individual_deviations():
    source=SourceLineage(987,.2,.7,929191,1.0)
    state=source_genotype(source)
    original=state.alleles[:,2,:].copy()
    target=.5
    centered=_center_A_expression_preserve_genotypic_spread(state,target)
    seen=centered.alleles[:,2,:]
    assert abs(float(seen.mean())-target)<1e-14
    assert np.allclose(seen-seen.mean(),original-original.mean(),atol=1e-14,rtol=0)
    assert np.array_equal(state.alleles[:,2,:],original)
    assert np.array_equal(centered.allele_origin,state.allele_origin)
    assert np.array_equal(centered.alleles[:,:2,:],state.alleles[:,:2,:])
    with np.testing.assert_raises(ValueError):
        _center_A_expression_preserve_genotypic_spread(state,.9999)


def test_emit_bounded_nonconfirmatory_fork_differences():
    d=readout()
    for island,record in sorted(d["summary"].items()):
        b=record["all_source_strata"]
        counts=" ".join(f"{p}={b['survival'][p]['persisted']}/{b['n_candidates']}"
                        for p in ("native","clamp_A","clamp_I","clamp_A_I","center_A_mean"))
        print("TECHNICAL DISJOINT SOURCE POSTESTABLISHMENT ONLY",island,
              f"arrived={b['n_arrived']}/{b['n_candidates']}",
              f"established={b['n_established']}/{b['n_candidates']}",
              counts,
              "native_minus_A_fixed_pp=",
              round(b["paired"]["clamp_A"]["native_minus_clamped_pp"],4),
              "native_minus_I_fixed_pp=",
              round(b["paired"]["clamp_I"]["native_minus_clamped_pp"],4))
        for stratum,z in sorted(record["by_source_A"].items()):
            print("TECHNICAL SOURCE_A_STRATUM",island,stratum,
                  "native",z["survival"]["native"]["persisted"],
                  "A_fixed",z["survival"]["clamp_A"]["persisted"],
                  "I_fixed",z["survival"]["clamp_I"]["persisted"],
                  "original_sources=8,nested_trials=64")
    print("THIS IS NOT A REGISTERED, INDEPENDENT ISLAND, NATURAL SC OR CAUSAL MEDIATION STUDY")



def test_emit_paired_discordances_and_successor_trait_differences():
    """Audit terminal policy pairs; shared initial source does not imply identical fates."""
    d=readout()
    for island,z in sorted(d["summary"].items()):
        q=z["all_source_strata"]
        print("TECHNICAL POSTESTABLISHMENT PAIR AUDIT", island,
              f"n={q['n_candidates']}", f"arrived={q['n_arrived']}",
              f"established={q['n_established']}",
              "native_survival",q["survival"]["native"]["persisted"])
        for policy in ("clamp_A","clamp_I","clamp_A_I","center_A_mean"):
            p=q["paired"][policy]
            assert p["both"]+p["native_only"]+p["policy_only"]+p["neither"] == 192
            pair=[g for g in d["groups"] if g["island"]==island and
                  g["arms"]["native"]["alive"] and g["arms"][policy]["alive"]]
            assert len(pair)==p["both"]
            signed_deltaA=[g["arms"]["native"]["final_traits"]["A"] -
                           g["arms"][policy]["final_traits"]["A"] for g in pair]
            signed_deltaI=[g["arms"]["native"]["final_traits"]["I"] -
                           g["arms"][policy]["final_traits"]["I"] for g in pair]
            meanA=sum(signed_deltaA)/len(pair) if pair else None
            meanI=sum(signed_deltaI)/len(pair) if pair else None
            print("TECHNICAL PAIRED POLICY",island,policy,
                  f"both={p['both']}",f"native_only={p['native_only']}",
                  f"fixed_only={p['policy_only']}",f"neither={p['neither']}",
                  f"net_pp={p['native_minus_clamped_pp']:+.6f}",
                  f"survivors_pair_delta_A={meanA!r}",
                  f"survivors_pair_delta_I={meanI!r}")
    print("TECHNICAL ONLY: paired same-source comparison with expression clamp;"
          " this cannot isolate genetic evolution or its mediation.")


def test_source_locked_centered_A_fates_and_flat_comparison():
    """Protect the exposed original 2026-10-19 technical cohort, NOT new inference.

    Source: scientific-gate job 118156720195 at bd262063fb0b...
    Matching 2x2 marginal counts cannot establish exact individual overlap.
    """
    d = readout()
    frozen = {
        "pilot_budget_4p5_visitors_0": (50, 49, 1, 1, 141),
        "pilot_budget_4p5_visitors_4": (67, 67, 0, 0, 125),
        "pilot_budget_8p0_visitors_0": (91, 90, 1, 1, 100),
        "pilot_budget_8p0_visitors_4": (118, 118, 0, 0, 74),
    }
    for island,(n_alive,both,native_only,center_only,neither) in frozen.items():
        s=d["summary"][island]["all_source_strata"]
        assert s["n_candidates"]==192
        assert s["survival"]["native"]["persisted"]==n_alive
        for policy in ("clamp_A","center_A_mean"):
            assert s["survival"][policy]["persisted"]==n_alive
            q=s["paired"][policy]
            assert (q["both"],q["native_only"],q["policy_only"],q["neither"]) == (
                both,native_only,center_only,neither)
        x=[z for z in d["groups"] if z["island"]==island]
        assert len(x)==192
        flat_only = sum(z["arms"]["clamp_A"]["alive"] and
                        not z["arms"]["center_A_mean"]["alive"] for z in x)
        centered_only = sum(z["arms"]["center_A_mean"]["alive"] and
                            not z["arms"]["clamp_A"]["alive"] for z in x)
        overlap = sum(z["arms"]["clamp_A"]["alive"] and
                      z["arms"]["center_A_mean"]["alive"] for z in x)
        assert flat_only==centered_only
        assert flat_only+overlap==n_alive
        print("SOURCE-LOCKED TECHNICAL FLAT-vs-CENTERED",island,
              "flat_only",flat_only,"centered_only",centered_only,
              "both",overlap,"neither",192-flat_only-centered_only-overlap)
    assert sum(q["survival"]["native"]["persisted"]
               for q in (s["all_source_strata"] for s in d["summary"].values())) == 326
