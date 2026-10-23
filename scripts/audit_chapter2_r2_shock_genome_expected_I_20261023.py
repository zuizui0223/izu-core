"""Replay original authenticated census30 genomes and isolate immediate expected I sorting.

Inputs are 24 source-verified ORIGINAL census30 fingerprints, *not* new founder
genotypes. The first 30 native steps are re-executed deterministically with
frozen source RNG and compared to the authenticated original Actions ZIP hashes.
After census30 this audit calls ONLY the original deterministic reproduce()
operator at two visitor activities, with no advance(), offspring generation,
new population futures, significance tests, or natural-island inference.

Expected I shift is the ONE-GENERATION expected offspring mean relative to the
current parent population; this is conditional reproductive sorting, NOT a
multi-generation selection/drift decomposition or causal historical mediation.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from scripts.chapter2_pollen_baseline_factorial_20261019 import (
    admit, config, visitors, founders, streams, step, snap, fingerprint,
)
from scripts.model3_island.reproduction import reproduce

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "data/design/chapter2_r2_original_384_strict_AM_prefixes_20261023.csv"
# This is the exact immutable Git blob SHA of the roster derived from the
# original 2026-10-19 Actions ZIP (original ZIP SHA-256 listed below).
ROSTER_BLOB_SHA = "REPLACE_WITH_VERIFIED_GIT_BLOB_SHA"
SOURCE_COMMIT = "eb785dc6865ca1842ec9d6c7d511778c74e03478"
SOURCE_ZIP_SHA256 = "10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e"
ORIGINAL_PROTOCOL_SHA256 = "87af92484af9988181b4f3bed6760d39325de70cca8c0b4e1cec19c47b8c9849"
STATUS = "ORIGINAL_CENSUS30_GENOME_EXACT_REPLAY_STATIC_ONE_GENERATION_I_SORTING"


def load_roster() -> list[dict]:
    raw = ROSTER.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if blob != ROSTER_BLOB_SHA:
        raise AssertionError("original 24-source roster Git blob changed")
    text = raw.decode("utf-8")
    rd = csv.DictReader(text.splitlines())
    expected = [
        "initial_A", "baseline_code", "founder_seed", "demographic_repeat",
        "prefix_state_sha256", "control_terminal_sha256", "decline_terminal_sha256",
    ]
    if rd.fieldnames != expected:
        raise AssertionError("expected seven exact source-proof roster columns")
    out, keys = [], set()
    for record in rd:
        a, baseline = float(record["initial_A"]), record["baseline_code"]
        seed, rep = int(record["founder_seed"]), int(record["demographic_repeat"])
        key = (a, baseline, seed, rep)
        if (a not in (0.3, 0.5) or baseline not in ("S", "W")
                or not 810101 <= seed <= 810112 or rep not in (1,2,3,4)
                or key in keys
                or any(len(record[k]) != 64 or any(c not in "0123456789abcdef" for c in record[k])
                       for k in expected[-3:])):
            raise AssertionError("source roster row invalid")
        keys.add(key)
        out.append({
            "initial_A": a, "baseline_code": baseline,
            "baseline": ("strong_baseline_limitation" if baseline == "S"
                         else "weak_baseline_limitation"),
            "founder_seed": seed, "demographic_repeat": rep,
            "prefix_sha": record["prefix_state_sha256"],
            "control_sha": record["control_terminal_sha256"],
            "decline_sha": record["decline_terminal_sha256"],
        })
    if (len(out) != 24 or Counter(x["baseline_code"] for x in out) !=
            {"S": 22, "W": 2}
            or len({x["founder_seed"] for x in out}) != 11
            or Counter((x["initial_A"], x["baseline_code"]) for x in out) != {
                (0.3,"S"):16,(0.3,"W"):1,(0.5,"S"):6,(0.5,"W"):1
            }):
        raise AssertionError("authenticated original 24-source roster altered")
    return out


def expected_genetic_I(state, ledger) -> tuple[float,float,float]:
    """Native parentage/Mendelian expectation of mean I in recruited offspring.

    Father's donor rows and mother's recipient columns each transmit half the
    offspring's two I alleles. A viable autonomous-selfed offspring gets both
    homologs from the same maternal parent, with mean expected I equal to its
    parent's expressed I.
    This expectation conditions on positive resident recruits and excludes
    adult survival, immigrants and mutations (zero in original frozen source).
    """
    phenotype = state.alleles[:, 1, :].mean(axis=1)
    n = len(phenotype)
    ledger_outcross = np.asarray(ledger.outcross)
    viable_self = np.asarray(ledger.self_viable)
    if (n != 48 or ledger_outcross.shape != (n,n) or viable_self.shape != (n,)
            or not np.isfinite(ledger_outcross).all() or not np.isfinite(viable_self).all()
            or (ledger_outcross < 0).any() or (viable_self < 0).any()):
        raise AssertionError("unexpected source ledger: outcross/self-parentage invalid")
    total = float(ledger_outcross.sum() + viable_self.sum())
    if not np.isfinite(total) or total <= 0:
        raise AssertionError("nonpositive source parentage")
    genotype_weight = (0.5 * ledger_outcross.sum(axis=0)
                       + 0.5 * ledger_outcross.sum(axis=1) + viable_self)
    expected_offspring = float(np.dot(genotype_weight, phenotype) / total)
    # Independently compute the source parentage matrix over ordered parents.
    parentage = ledger_outcross.copy()
    idx = np.diag_indices(n)
    parentage[idx] += viable_self
    independent = float(
        (parentage * (phenotype[:, None] + phenotype[None, :]) * 0.5).sum()
        / parentage.sum()
    )
    if not np.isclose(independent, expected_offspring, atol=1e-13, rtol=0):
        raise AssertionError("independent ordered-parent transmission check failed")
    parent_mean = float(phenotype.mean())
    q = float(ledger_outcross.sum() / ledger.ovules.sum())
    if not (0 <= expected_offspring <= 1 and 0 <= q <= 1):
        raise AssertionError("invalid predicted native trait mean or pollen receipt")
    return expected_offspring - parent_mean, q, expected_offspring


def replay() -> dict:
    d = admit()  # fail-closed SHA: original full protocol and all native kernels
    if (d["status"] != "FROZEN_EXPLORATORY_MECHANISM_PILOT_NOT_INDEPENDENT_CONFIRMATION"
            or d["factorial"]["freeze_prefix_updates"] != 30
            or d["factorial"]["future_updates"] != 50
            or d["model"]["capacity"] != 48
            or d["model"]["adult_survival"] != 0
            or d["model"]["mutation_rate"] != 0
            or d["model"]["seed_immigration"] != 0
            or d["model"]["visitor_immigration"] != 0
            or d["model"]["assurance_mode"] != "evolving"):
        raise AssertionError("original native model source has changed")
    rows = load_roster()
    result = []
    for entry in rows:
        a, seed, rep = entry["initial_A"], entry["founder_seed"], entry["demographic_repeat"]
        baseline = entry["baseline"]
        source_state = founders(d,seed,a)
        rr = streams(seed,rep)
        vv = visitors(d,baseline)
        cc = config(d,baseline,0.4)
        for year in range(30):
            source_state, _ = step(source_state,vv,cc,rr,year)
        if fingerprint(source_state) != entry["prefix_sha"]:
            raise AssertionError(f"failed to exactly reconstruct ORIGINAL source genome at census30: {entry}")
        s=snap(source_state)
        supports=s["genetic_support"]
        if (s["n"] != 48 or len(supports["A"]["allele_values"]) != 1
                or len(supports["M"]["allele_values"]) != 1
                or len(supports["I"]["allele_values"]) <= 1
                or sum(supports["I"]["allele_counts"]) != 96):
            raise AssertionError("source census30 genetically invariant A/M condition failed")
        if (len(source_state.allele_origin) != 48 or
                np.any(source_state.mutation_flags)):
            raise AssertionError("original selected source ancestry/mutation differs")
        arms={}
        for arm,activity in (("control",0.4),("decline",0.04)):
            cfg=config(d,baseline,activity)
            ledger=reproduce(source_state,vv,cfg)
            selection,q,predicted = expected_genetic_I(source_state, ledger)
            arms[arm]={
                "expected_one_generation_I_shift": selection,
                "source_outcross_fraction_q": q,
                "expected_mean_I_child": predicted,
                "expected_parental_genome_return_total": float(
                    ledger.outcross.sum()+ledger.self_viable.sum()),
            }
        if not arms["decline"]["source_outcross_fraction_q"] < arms["control"]["source_outcross_fraction_q"]:
            raise AssertionError("original paired external pollen intervention not effective")
        result.append({
            "initial_A":a,"baseline":baseline,"founder_seed":seed,
            "demographic_repeat":rep,
            "original_source_prefix_sha":entry["prefix_sha"],
            "original_control_terminal_sha":entry["control_sha"],
            "original_decline_terminal_sha":entry["decline_sha"],
            "I_mean_at_shock":s["I"],
            "I_allele_values_at_shock":supports["I"]["allele_values"],
            "I_allele_counts_at_shock":supports["I"]["allele_counts"],
            "A_fixed_value":supports["A"]["allele_values"][0],
            "M_fixed_value":supports["M"]["allele_values"][0],
            "native_one_generation":arms,
            "decline_minus_control_expected_I_sorting": (
                arms["decline"]["expected_one_generation_I_shift"] -
                arms["control"]["expected_one_generation_I_shift"]),
        })
    summaries=[]
    for baseline in ("strong_baseline_limitation","weak_baseline_limitation"):
        subset=[x for x in result if x["baseline"]==baseline]
        ds=np.asarray([x["decline_minus_control_expected_I_sorting"] for x in subset])
        summaries.append({
            "baseline":baseline,"n_original_source_genomes":len(subset),
            "n_distinct_founders":len({x["founder_seed"] for x in subset}),
            "mean_static_expected_I_sorting_difference":float(ds.mean()),
            "n_static_expected_treatment_negative":int((ds<0).sum()),
            "n_static_expected_treatment_exact_zero":int((ds==0).sum()),
            "n_static_expected_treatment_positive":int((ds>0).sum()),
            "mean_original_q_control":float(np.mean([
                x["native_one_generation"]["control"]["source_outcross_fraction_q"] for x in subset])),
            "mean_original_q_decline":float(np.mean([
                x["native_one_generation"]["decline"]["source_outcross_fraction_q"] for x in subset])),
        })
    strong=next(x for x in summaries if x["baseline"]=="strong_baseline_limitation")
    if (strong["n_original_source_genomes"]!=22 or strong["n_distinct_founders"]!=11
            or abs(strong["mean_original_q_control"]-0.13920994216147997)>1e-12
            or abs(strong["mean_original_q_decline"]-0.01689527391924731)>1e-12):
        raise AssertionError("original 22-source pollen ledger readback changed")
    return {
        "status":STATUS,
        "original_run_id":39233450099,
        "original_zip_sha256":SOURCE_ZIP_SHA256,
        "original_source_commit":SOURCE_COMMIT,
        "original_protocol_sha256":ORIGINAL_PROTOCOL_SHA256,
        "reproduced_original_prefix_steps":24*30,
        "new_independent_population_future_steps":0,
        "new_experiments_or_statistical_tests":0,
        "original_source_genomes_exactly_recovered":24,
        "n_source_founders":11,
        "summaries":summaries,
        "rows":result,
        "selection_gradient_scope":"one-generation expected Mendelian offspring trait mean at source census30, fixed A/M and original heterogeneous I. Not a counterfactual causal selection-vs-drift decomposition of 50-generation realized endpoints.",
        "evidence_rank":"POST_OUTCOME_SOURCE_EXACT_STATIC_EXPECTATION_NOT_INDEPENDENT_CONFIRMATION",
    }


if __name__ == "__main__":
    print(json.dumps(replay(),ensure_ascii=False,indent=2,sort_keys=True))
