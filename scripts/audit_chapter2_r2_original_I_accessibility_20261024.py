"""R2 standing I alleles at shock versus ORIGINAL fixed-I endpoints.

External archive only: SHA-256 authenticated 384-path Actions source ZIP,
producer 39233450099/artifact 12178257738. No new population simulations,
mutations, fitness retuning, inferential tests, or ecological generalization.

In 22 source pairs under strong previous pollen limitation, A and M were
monomorphic and I remained polymorphic before the imposed visitor decline.
The result is retrospective SOURCE-EXACT association, NOT a registered
low-allele-frequency threshold or identified drift-versus-selection mechanism.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import zipfile

from scripts.audit_chapter2_r2_shock_frozen_AM_I_sorting_20261023 import (
    audit as original_strict_audit, classify_strict
)
from scripts.audit_chapter2_r2_original_384_pair_convergence_20261023 import (
    ZIP_SHA, SOURCE_SHA, PROTOCOL_SHA
)

STATUS="PASS_ORIGINAL_R2_STANDING_I_ALLELES_EXPLORATORY_NOT_FREQUENCY_THRESHOLD"
STRONG="strong_baseline_limitation"
ORIGINAL_ACTIONS_RUN=39233450099


def analyze_original_zip(path: Path) -> dict:
    original=original_strict_audit(path)  # full 384 archive checksum/manifest and pair keys
    if (original["status"]!="EXPLORATORY_STRICT_FIXED_A_M_SORTING_IN_ORIGINAL_384_NO_NEW_BIOLOGY"
            or original["source_zip_sha256"]!=ZIP_SHA or original["source_sha"]!=SOURCE_SHA
            or original["source_protocol_sha256"]!=PROTOCOL_SHA
            or original["totals"]["strong_pairs"]!=22
            or original["totals"]["strong_distinct_founders"]!=11):
        raise AssertionError("not the exact original, admitted R2 shock-source cohort")
    pairs=defaultdict(dict)
    with zipfile.ZipFile(path) as z:
        for shard in ("strong.json","weak.json"):
            for row in json.loads(z.read(shard))["rows"]:
                k=(row["start_A"],row["baseline"],row["founder_seed"],row["demography_repeat"])
                if row["arm"] in pairs[k]:
                    raise AssertionError("duplicate original source-future arm")
                pairs[k][row["arm"]]=row
    if len(pairs)!=192:
        raise AssertionError("original cohort must have exactly 192 complete source pairs")
    rows=[]
    for key in sorted(pairs):
        arm=pairs[key]
        if set(arm)!={"control","decline"}:
            raise AssertionError("original matched source arms incomplete")
        c,d=arm["control"],arm["decline"]
        eligible=classify_strict(c,d)
        if eligible is None or key[1]!=STRONG:
            continue
        pre=c["t_prefix"]["genetic_support"]["I"]
        vals=pre["allele_values"]
        counts=pre["allele_counts"]
        if (len(vals)<2 or len(vals)!=len(counts) or vals!=sorted(vals)
                or sum(counts)!=96 or any(k<=0 for k in counts)):
            raise AssertionError("original diploid I accessibility at shock invalid")
        endc=c["t_end"]["genetic_support"]["I"]["allele_values"]
        endd=d["t_end"]["genetic_support"]["I"]["allele_values"]
        if len(endd)!=1:
            raise AssertionError("original strong-history decline arm must finish I-fixed")
        lowest=vals[0]
        fixed=endd[0]
        if fixed not in vals:
            raise AssertionError("no-mutation source produced an unobserved I allele")
        if any(a not in vals for a in endc):
            raise AssertionError("source maintained arm acquired unobserved I allele")
        min_count=int(counts[0])
        n_origin=len(vals)
        contrast=d["t_end"]["I"]-c["t_end"]["I"]
        rows.append({
            "initial_A":key[0],
            "original_founder_seed":key[2],
            "nested_demographic_repeat":key[3],
            "original_prefix_state_sha256":c["prefix_state_hash"],
            "I_allele_values_at_shock":vals,
            "I_allele_counts_at_shock":counts,
            "original_number_I_allele_values_at_shock":n_origin,
            "lowest_I_allele_value_present_at_shock":lowest,
            "lowest_I_allele_count_out_of_96":min_count,
            "lowest_I_allele_fraction":min_count/96,
            "decline_terminal_fixed_I_value":fixed,
            "decline_fixed_to_lowest_accessible_I_value":fixed==lowest,
            "control_terminal_I_allele_values":endc,
            "control_terminal_mean_I":c["t_end"]["I"],
            "decline_terminal_mean_I":d["t_end"]["I"],
            "decline_minus_control_terminal_I":contrast,
            "terminal_I_treatment_contrast_exact_zero":contrast==0,
        })
    return _finalize(rows)


def _finalize(rows: list[dict]) -> dict:
    if len(rows)!=22 or len({x["original_founder_seed"] for x in rows})!=11:
        raise AssertionError("not the exact 22 selected original source pairs")
    successes=[x for x in rows if x["decline_fixed_to_lowest_accessible_I_value"]]
    exceptions=[x for x in rows if not x["decline_fixed_to_lowest_accessible_I_value"]]
    if len(successes)!=20 or len(exceptions)!=2:
        raise AssertionError("original fixed-I accessibility result changed")
    exceptional_keys={(x["initial_A"],x["original_founder_seed"],x["nested_demographic_repeat"],
                       x["lowest_I_allele_count_out_of_96"],x["decline_terminal_fixed_I_value"])
                      for x in exceptions}
    if exceptional_keys != {
        (0.3,810102,4,6,0.75),
        (0.5,810110,3,4,0.5),
    }:
        raise AssertionError("two original high-I fixed exceptions changed")
    if any(not x["terminal_I_treatment_contrast_exact_zero"] for x in exceptions):
        raise AssertionError("original source exception does not have zero I treatment contrast")
    least_success=min(x["lowest_I_allele_count_out_of_96"] for x in successes)
    most_exception=max(x["lowest_I_allele_count_out_of_96"] for x in exceptions)
    if least_success!=16 or most_exception!=6:
        raise AssertionError("source low-allele input accessibility range changed")
    fixed_dest=Counter(str(x["decline_terminal_fixed_I_value"]) for x in rows)
    if fixed_dest!={"0.25":9,"0.5":12,"0.75":1}:
        raise AssertionError("source original decline I fixed-value distribution changed")
    by_initial_A=[]
    for a in (0.3,0.5):
        subset=[x for x in rows if x["initial_A"]==a]
        by_initial_A.append({
            "initial_A":a,
            "n_source_cells":len(subset),
            "n_decline_fixed_to_lowest_accessible_I":sum(
                x["decline_fixed_to_lowest_accessible_I_value"] for x in subset),
            "n_fixed_above_lowest_accessible_I":sum(
                not x["decline_fixed_to_lowest_accessible_I_value"] for x in subset),
        })
    if [(x["n_source_cells"],x["n_decline_fixed_to_lowest_accessible_I"]) for x in by_initial_A] != [(16,15),(6,5)]:
        raise AssertionError("original source A-stratified I fixation changed")
    return {
        "status":STATUS,
        "original_actions_run_id":ORIGINAL_ACTIONS_RUN,
        "original_zip_sha256":ZIP_SHA,
        "original_source_commit":SOURCE_SHA,
        "original_protocol_sha256":PROTOCOL_SHA,
        "n_original_paths":384,
        "n_original_paired_futures":192,
        "n_strict_AM_fixed_I_polymorphic_strong_history_source_cells":22,
        "n_distinct_founder_seeds":11,
        "n_decline_fixed_to_lowest_I_allele_present_at_shock":20,
        "n_decline_fixed_to_other_higher_I_allele":2,
        "min_lowest_allele_count_among_lower_fixations":least_success,
        "max_lowest_allele_count_among_higher_fixations":most_exception,
        "n_allele_copies_at_shock_per_cell":96,
        "decline_fixed_I_value_counts":dict(sorted(fixed_dest.items())),
        "by_initial_A":by_initial_A,
        "exceptions":exceptions,
        "rows":rows,
        "claim_rank":"RETROSPECTIVE_ORIGINAL_22_CELLS_NOT_INDEPENDENT_CONFIRMATION",
        "new_biological_population_updates":0,
        "new_statistical_tests":0,
        "not_identified":[
            "Any prospective or universal allele-frequency fixation threshold",
            "Causal distinction of selection from neutral drift or stochastic reproductive sampling",
            "Natural-population selection effect, independent 22 founder replications",
            "Proof that rare alleles are always lost or abundant low-I alleles always fix",
        ],
    }


def replay_original_native() -> dict:
    """Independent readback using only original seeds and original source kernels.

    Genotype fingerprints at census30 and BOTH t80 endpoints must exactly
    match the immutable 24-state original source ZIP-derived manifest already
    verified in PRs #633/#634. This reexecutes the SAME source trajectories,
    never samples a new founder or a new independently planned future.
    """
    from scripts.audit_chapter2_r2_shock_genome_expected_I_20261023 import load_roster
    from scripts.chapter2_pollen_baseline_factorial_20261019 import (
        admit, founders, visitors, config, streams, step, clone, fingerprint, snap,
    )
    original=admit()
    if (original["status"] != "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
            or original["model"]["mutation_rate"] != 0
            or original["model"]["seed_immigration"] != 0
            or original["factorial"]["freeze_prefix_updates"] != 30
            or original["factorial"]["future_updates"] != 50):
        raise AssertionError("native original source changed since archiving")
    original_cells=[c for c in load_roster() if c["baseline"]==STRONG]
    if len(original_cells)!=22:
        raise AssertionError("original strong-history 22-state source roster missing")
    rows=[]
    for cell in original_cells:
        seed,repeat,a=cell["founder_seed"],cell["demographic_repeat"],cell["initial_A"]
        baseline=cell["baseline"]
        v=visitors(original,baseline)
        cfg=config(original,baseline,0.4)
        st=founders(original,seed,a)
        rng=streams(seed,repeat)
        for year in range(30):
            st,_=step(st,v,cfg,rng,year)
        if fingerprint(st)!=cell["prefix_sha"]:
            raise AssertionError("original full diploid shock-time genotype fingerprint changed")
        initial=snap(st)
        pre=initial["genetic_support"]["I"]
        vals,counts=pre["allele_values"],pre["allele_counts"]
        if (initial["n"] != 48 or len(vals)<2 or len(vals)!=len(counts)
                or sum(counts)!=96 or vals!=sorted(vals)
                or len(initial["genetic_support"]["A"]["allele_values"])!=1
                or len(initial["genetic_support"]["M"]["allele_values"])!=1):
            raise AssertionError("source initial A/M-fixed, I-segregating genetic state changed")
        saved=clone(rng)
        terminals={}
        for arm,activity in (("control",0.4),("decline",0.04)):
            st2=st
            rr=clone(saved)
            cc=config(original,baseline,activity)
            for year in range(30,80):
                st2,_=step(st2,v,cc,rr,year)
            end_sha=cell["control_sha"] if arm=="control" else cell["decline_sha"]
            if fingerprint(st2)!=end_sha:
                raise AssertionError("original archived terminal complete-genome SHA256 mismatch")
            terminals[arm]=snap(st2)
        c=terminals["control"]
        d=terminals["decline"]
        cval=c["genetic_support"]["I"]["allele_values"]
        dval=d["genetic_support"]["I"]["allele_values"]
        if len(dval)!=1:
            raise AssertionError("decline treatment I must be monomorphic in original selected cells")
        fixed=dval[0]
        contrast=d["I"]-c["I"]
        rows.append({
            "initial_A":a,
            "original_founder_seed":seed,
            "nested_demographic_repeat":repeat,
            "original_prefix_state_sha256":cell["prefix_sha"],
            "I_allele_values_at_shock":vals,
            "I_allele_counts_at_shock":counts,
            "original_number_I_allele_values_at_shock":len(vals),
            "lowest_I_allele_value_present_at_shock":vals[0],
            "lowest_I_allele_count_out_of_96":int(counts[0]),
            "lowest_I_allele_fraction":int(counts[0])/96,
            "decline_terminal_fixed_I_value":fixed,
            "decline_fixed_to_lowest_accessible_I_value":fixed==vals[0],
            "control_terminal_I_allele_values":cval,
            "control_terminal_mean_I":c["I"],
            "decline_terminal_mean_I":d["I"],
            "decline_minus_control_terminal_I":contrast,
            "terminal_I_treatment_contrast_exact_zero":contrast==0,
        })
    return _finalize(rows)



if __name__=="__main__":
    p=argparse.ArgumentParser()
    source=p.add_mutually_exclusive_group(required=True)
    source.add_argument("--zip",type=Path,
                   help="Original external SHA256-verified 384-path Actions ZIP; NOT bundled")
    source.add_argument("--native",action="store_true",
                   help="Replay the SAME original t30/t80 genomes, verifying saved ZIP SHA fingerprints")
    args=p.parse_args()
    out=replay_original_native() if args.native else analyze_original_zip(args.zip)
    print(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2))
