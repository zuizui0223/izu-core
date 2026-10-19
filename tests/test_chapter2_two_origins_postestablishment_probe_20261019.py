"""Technical-only independently seeded post-establishment A/I expression probe."""
from __future__ import annotations
from functools import lru_cache
import math

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
    assert d["paired_policy_paths"]==3072
    assert d["independent_demographic_resets_per_source_island"]==8
    assert d["primary_inference_performed"] is False
    assert d["causal_mediation_identified"] is False
    assert d["no_reused_prior_exposed_train_or_heldout_genotypes"] is True
    original={(r["island"],r["reset"],r["source_id"]) for r in d["groups"]}
    assert len(original)==768
    for r in d["groups"]:
        assert set(r["arms"])=={"native","clamp_A","clamp_I","clamp_A_I"}
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
        for policy in ("native","clamp_A","clamp_I","clamp_A_I"):
            assert sum(v["survival"][policy]["persisted"]
                       for v in x["by_source_A"].values()) == \
                   b["survival"][policy]["persisted"]


def test_postestablishment_expression_clamps_retain_original_source_values():
    for r in readout()["groups"]:
        A,I=r["source_A"],r["source_I"]
        for name in ("clamp_A","clamp_I","clamp_A_I"):
            arm=r["arms"][name]
            if not arm["alive"]:
                continue
            if name in ("clamp_A","clamp_A_I"):
                assert arm["final_traits"]["A"]==A
            if name in ("clamp_I","clamp_A_I"):
                assert arm["final_traits"]["I"]==I


def test_emit_bounded_nonconfirmatory_fork_differences():
    d=readout()
    for island,record in sorted(d["summary"].items()):
        b=record["all_source_strata"]
        counts=" ".join(f"{p}={b['survival'][p]['persisted']}/{b['n_candidates']}"
                        for p in ("native","clamp_A","clamp_I","clamp_A_I"))
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
        for policy in ("clamp_A","clamp_I","clamp_A_I"):
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
