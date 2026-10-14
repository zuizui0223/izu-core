"""Original-genome-preserving m0/m6 A/I co-carriage F1 law, no biological futures.

The ONLY experimental edit is symmetric hidden A heterozygosity (±1/16) on
six original confirmation founders in a single identical adult-phenotype
stratum. I homologs, every original M allele, adult expressed M/I/A, native
reproductive return laws, t0 N=K=48 and all original Model3 operators stay
unchanged. This does not imply natural source genotype generation or actual
offspring births. No history, mutation, or population advancement is called.
"""
from __future__ import annotations

from dataclasses import replace
import argparse
import json
from pathlib import Path
import numpy as np

from scripts.model3_island import reproduction, types
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, source_state, original_context, CONTEXTS, ledger_parity,
)
from scripts.audit_chapter2_full_F1_joint_distribution_20261014 import (
    one_offspring_joint_distribution, total_variation,
)
from scripts.audit_chapter2_original_t0_carriage_swap_bound_20261015 import (
    report as source_limit_report, load_original,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/audits/chapter2_Q2_original_confirmation_m0_m6_F1_20261015.json"
A_HALFWIDTH = 1 / 16
N_A_CARRIERS = 6
ARTIFICIAL_A_ORIGIN_BASE = 9_000_000_000_000
CLASSES = ("m0", "m6")


def source_carriers(base: types.PlantState) -> dict[str, tuple[int, ...]]:
    """Exact original-I groups, no regrouping original or engineered I genomes."""
    if len(base.ids) != 48 or not np.array_equal(base.ids, np.arange(48)):
        raise ValueError("Expected original 48 confirmation adult IDs")
    ph = base.alleles.mean(axis=2)
    original_I = base.alleles[:, 1, :]
    selected = np.flatnonzero(
        (ph[:, 0] == 0.5625) & (ph[:, 1] == 0.5) & (ph[:, 2] == 0.5))
    homo = selected[original_I[selected, 0] == original_I[selected, 1]]
    hetero = selected[original_I[selected, 0] != original_I[selected, 1]]
    if (len(selected) != 24 or len(homo) != 6 or len(hetero) != 18
            or not np.array_equal(homo, [5,13,21,29,37,45])):
        raise ValueError("Original-source phenotype/I-carrier composition drift")
    # The first six I heterozygotes are a deterministic technical control,
    # not natural founder sampling or a new independent genetic source.
    return {"m0": tuple(int(x) for x in homo),
            "m6": tuple(int(x) for x in hetero[:N_A_CARRIERS])}


def assign_A_only(base: types.PlantState, carriers: tuple[int, ...]) -> types.PlantState:
    if (len(carriers) != N_A_CARRIERS or len(set(carriers)) != N_A_CARRIERS
            or min(carriers) < 0 or max(carriers) >= 48):
        raise ValueError("Unexpected 6-carrier source-locked A intervention")
    a = base.alleles.copy()
    # CRITICAL: the authenticated original t0 has 48/48 already A-heterozygous.
    # Both arms therefore artificially reset ALL A homologs to 0.5/0.5,
    # then assign exactly six A heterozygotes within the matched phenotype
    # stratum. Original I and M copies are never edited.
    if (not np.array_equal(a[:,2,0],np.full(48,.5-A_HALFWIDTH))
            or not np.array_equal(a[:,2,1],np.full(48,.5+A_HALFWIDTH))):
        raise ValueError("Authentic original A full-carrier source is not unchanged")
    a[:,2,:] = .5
    a[list(carriers),2,0] = .5 - A_HALFWIDTH
    a[list(carriers),2,1] = .5 + A_HALFWIDTH
    origins = base.allele_origin.copy()
    ix = np.arange(48, dtype=np.int64)
    # Reconstruct the entire manipulated A-locus origin as a synthetic
    # allele provenance namespace; original I/M provenance remains exact.
    origins[:,2,0] = ARTIFICIAL_A_ORIGIN_BASE + ix * 2
    origins[:,2,1] = ARTIFICIAL_A_ORIGIN_BASE + ix * 2 + 1
    edited = replace(base, alleles=a, allele_origin=origins)
    if (not np.array_equal(edited.alleles.mean(axis=2),base.alleles.mean(axis=2))
            or not np.array_equal(edited.alleles[:,:2,:],base.alleles[:,:2,:])
            or not np.array_equal(edited.allele_origin[:,:2,:],base.allele_origin[:,:2,:])
            or not np.array_equal(edited.mutation_flags,base.mutation_flags)
            or not np.array_equal(edited.ids,base.ids)
            or not np.array_equal(edited.birth_years,base.birth_years)):
        raise ValueError("Original I/M state, adult phenotype or provenance changed")
    return edited


def _tail_probability(joint: np.ndarray, adult_A: float, adult_I: float) -> float:
    v = np.arange(33, dtype=float)/32
    flagA = v >= adult_A + .05
    flagI = v <= adult_I - .05
    return float(joint[np.ix_(flagA,flagI)].sum())


def audit() -> dict:
    old = load_original()
    constraint = source_limit_report(old)["blocks"]["confirmation"]
    if constraint["exact_matched_A_carrier_swap_capacity_with_I_original"] != 6:
        raise ValueError("Historical source matching feasibility changed")
    fixture = original_fixture()
    base = source_state(fixture, "confirmation")
    carriers = source_carriers(base)
    edited = {name: assign_A_only(base, ids) for name,ids in carriers.items()}
    if len(set(carriers["m0"]) & set(carriers["m6"])) != 0:
        raise ValueError("A source interventions no longer have m0/m6 overlap")
    # verify actual number of A/I co-carriers instead of trusting arm label
    for name,st in edited.items():
        Ihet = st.alleles[:,1,0] != st.alleles[:,1,1]
        Ahet = st.alleles[:,2,0] != st.alleles[:,2,1]
        expected = 0 if name=="m0" else 6
        if int(np.count_nonzero(Ahet & Ihet)) != expected:
            raise ValueError("Actual source t0 co-carriage mismatch")
        if int(np.count_nonzero(Ahet)) != N_A_CARRIERS:
            raise ValueError("Changed original A-carrier count")
    original = np.mean(base.alleles, axis=(0,2))
    rows=[]
    for context in CONTEXTS:
        cfg,vis=original_context(fixture,"confirmation",context)
        ledgers={}
        joints={}
        for name in CLASSES:
            ledger_parity(base,edited[name],cfg,vis)
            ledgers[name]=reproduction.reproduce(edited[name],vis,cfg)
            joints[name]=one_offspring_joint_distribution(edited[name],ledgers[name])
        for key in ("outcross","self_raw","self_viable","ovules","exported",
                    "delivered","lost","maternal","paternal"):
            if not np.array_equal(getattr(ledgers["m0"],key),getattr(ledgers["m6"],key)):
                raise ValueError("Original native t0 reproductive lottery changed")
        p,q=joints["m0"],joints["m6"]
        dA=float(np.max(np.abs(p.sum(axis=1)-q.sum(axis=1))))
        dI=float(np.max(np.abs(p.sum(axis=0)-q.sum(axis=0))))
        if max(dA,dI)>1e-12:
            raise ValueError("A/I entire first-offspring marginal distributions differ")
        tv=total_variation(p,q)
        rows.append({
            "context":int(context),
            "N_initial":48,
            "m0_A_heterozygote_original_IDs":list(carriers["m0"]),
            "m6_A_heterozygote_original_IDs":list(carriers["m6"]),
            "original_I_homologs_identical_in_both_arms":True,
            "original_adult_M_I_A_identical_in_both_arms":True,
            "original_native_reproductive_return_matrices_identical":True,
            "entire_F1_A_marginal_max_bin_error":dA,
            "entire_F1_I_marginal_max_bin_error":dI,
            "F1_joint_A_I_total_variation":tv,
            "P_one_child_Aup_Itdown_relative_to_original_founder_mean": {
                name:_tail_probability(joint, float(original[2]), float(original[1]))
                for name,joint in joints.items()},
        })
    if len(rows) != 3:
        raise AssertionError("Missing original visitor context")
    return {
        "schema": "chapter2_original_confirmation_m0_m6_static_F1_joint_review_v1",
        "status": "ORIGINAL_I_UNMODIFIED_F1_ANALYTICAL_ONLY_NOT_EVOLUTION",
        "original_t0_fixture_git_blob": "4b529cce12bc44e06d43a22b10c325a52bbd967b",
        "original_biology_commit": "328548612e93469fcc8663f24548530a57399b9a",
        "source_founder_background": "confirmation",
        "independent_source_genome_realizations": 1,
        "N_initial":48,
        "new_biological_born_offspring":0,
        "new_Model3_future_updates":0,
        "new_sustained_6class_response_histories":0,
        "original_I_allele_copies_preserved":True,
        "original_A_heterozygote_adults":48,
        "six_A_heterozygous_carriers_per_arm":6,
        "original_A_heterozygosity_reset_in_each_arm":42,
        "arm_m0_vs_m6_I_A_co_carrier_counts":[0,6],
        "contexts":rows,
        "limits":[
            "This is a conditional one-child F1 distribution integrated from native t0 parent returns; no actual birth or evolutionary history.",
            "All 48 original adults were A-heterozygous at baseline; in EACH arm 42 are artificially made A-homozygous while the other six retain the original symmetric A halfwidth. Original I homologs and all adult expressed traits are unchanged.",
            "This is an I-preserving artificial A-locus reconstruction conditioned on one original source, NOT the untouched historical complete genotype.",
            "The two arms derive from ONE original founder source; none of the three pollinator contexts are independent genomic source replicates.",
            "Full single-offspring trait margins and static parental return parity do not guarantee equal long-run genetic variances, joint offspring distributions, sustained evolutionary order or population survival.",
            "The A-up/I-down child event is a single-offspring founder-relative diagnostic, not a sustained population-average response or proof of beneficial genotypes.",
            "The original main genomic source cannot support any such strictly matched I-fixed carrier reassignment; confirmation permits only six.",
            "Different from the A halfwidth pilot and the synthetic m0/m12 quartet experiment; does not authorize the new Q2 200-update Model3 study.",
        ]
    }


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true")
    cli.add_argument("--write", action="store_true")
    args=cli.parse_args()
    if args.check and args.write:
        cli.error("Select either --check or --write")
    result=json.dumps(audit(),indent=2,ensure_ascii=False,allow_nan=False)+"\n"
    if args.check:
        if json.loads(OUTPUT.read_text(encoding="utf-8")) != json.loads(result):
            raise SystemExit("FAIL: saved source-only F1 report differs from original native replay")
        print("PASS: source-locked native m0/m6 original-I F1 and joint-law checks")
    elif args.write:
        if OUTPUT.exists():
            raise FileExistsError("Never overwrite original-source genetic constraint result")
        OUTPUT.parent.mkdir(parents=True,exist_ok=True)
        OUTPUT.write_text(result,encoding="utf-8",newline="\n")
        print("WROTE: native t0 F1 conditional distribution audit")
    else:
        print(result,end="")


if __name__ == "__main__":
    main()
