"""Independent *synthetic* 48-adult t0 source-pool feasibility: NO biological futures.

Sixteen fresh source genotype *inputs* are created from explicitly artificial
discrete M/I adult phenotype support (not original historical or field genomes).
The original Model3 types/reproduction operators are source-pinned. Source
draws and interventions are technical randomisations, NOT registered cohorts.
"""
from __future__ import annotations

from hashlib import sha256
import json
import numpy as np

from scripts.model3_island import types, reproduction
from scripts.audit_chapter2_native_founder_source_20261014 import (
    native_gate, ordered_ids, LEDGER_FIELDS,
)
from scripts.audit_chapter2_original_founder_compatibility_20261014 import (
    original_fixture, original_context, ledger_parity, CONTEXTS,
)
from scripts.audit_chapter2_founder_F1_conditional_moments_20261014 import (
    conditional_f1_moments,
)

SOURCE_SALT = "izu-core-independent-model3-source-fixture-V0-NO-BIOLOGY-20261014"
DRAW_SALT = "izu-core-independent-founder-draw-V0-NO-BIOLOGY-20261014"
POOL_COUNT = 16
OVERLAPS = (0, 3, 6, 12)
FOUNDER_SIZES = (2, 8, 24, 48)
SOURCE_M = (7/16, 8/16, 9/16)
SOURCE_I = (6/16, 7/16, 8/16, 9/16, 10/16)
ALLELE_HALF_WIDTH = 1/16
SYNTH_ORIGIN_NS = 4_000_000_000_000


def _unbiased_bucket(pool: int, individual: int, locus: int, modulus: int) -> int:
    """Deterministic SHA source draw, rejection of any modulo bias."""
    top = 2**64
    limit = top - top % modulus
    for counter in range(16):
        raw = sha256(
            f"{SOURCE_SALT}:{pool}:{individual}:{locus}:{counter}".encode()
        ).digest()
        value = int.from_bytes(raw[:8], "big")
        if value < limit:
            return value % modulus
    raise ValueError("SHA uniform-bucket generation failed")


def source_state(pool: int) -> types.PlantState:
    """Fresh independent synthetic genotype INPUT, not a new trajectory."""
    native_gate()
    if type(pool) is not int or not 0 <= pool < POOL_COUNT:
        raise ValueError("Unregistered synthetic source pool index")
    ids = np.arange(48, dtype=np.int64)
    mean = np.full((48, 3), .5, dtype=np.float64)
    for ind in range(48):
        mean[ind,0] = SOURCE_M[_unbiased_bucket(pool, ind, 0, len(SOURCE_M))]
        mean[ind,1] = SOURCE_I[_unbiased_bucket(pool, ind, 1, len(SOURCE_I))]
    a = np.repeat(mean[:, :, None], 2, axis=2)
    origins = (SYNTH_ORIGIN_NS + pool*100_000 +
               ids[:,None,None]*10 +
               np.arange(3)[None,:,None]*2 +
               np.arange(2)[None,None,:])
    return types.PlantState(
        alleles=a, allele_origin=origins,
        mutation_flags=np.zeros((48,3,2), dtype=bool),
        ids=ids, birth_years=np.zeros(48,dtype=np.int64),
    )


def assign_hidden_heterozygotes(
    source: types.PlantState, pool: int, overlap: int
) -> tuple[types.PlantState, frozenset[int], frozenset[int]]:
    if (type(overlap) is not int or overlap not in OVERLAPS or
            type(pool) is not int or not 0 <= pool < POOL_COUNT
            or not np.array_equal(source.ids,np.arange(48))):
        raise ValueError("Unregistered source or co-carriage treatment")
    base = source_state(pool)
    if not np.array_equal(source.alleles, base.alleles):
        raise ValueError("Not the source-authenticated synthetic F0 pool")
    ranked = ordered_ids(
        source.ids, pool, SOURCE_SALT + "::carrier-assignment"
    )
    A = ranked[:12]
    I = np.concatenate((ranked[:overlap], ranked[12:24-overlap]))
    if len(np.unique(I)) != 12 or len(np.intersect1d(A,I)) != overlap:
        raise AssertionError("Synthetic carrier overlap changed")
    alleles = source.alleles.copy()
    origin = source.allele_origin.copy()
    for locus, carriers in ((1,I),(2,A)):
        centers = source.alleles[:,locus,:].mean(axis=1)
        alleles[carriers,locus,0] = centers[carriers] - ALLELE_HALF_WIDTH
        alleles[carriers,locus,1] = centers[carriers] + ALLELE_HALF_WIDTH
        origin[:,locus,:] += 1_000_000_000
    edited = types.PlantState(
        alleles=alleles, allele_origin=origin,
        mutation_flags=source.mutation_flags,
        ids=source.ids,birth_years=source.birth_years,
    )
    if (not np.array_equal(edited.alleles.mean(axis=2),
                           source.alleles.mean(axis=2))
            or not np.array_equal(edited.alleles[:,0],source.alleles[:,0])
            or not np.array_equal(edited.allele_origin[:,0],source.allele_origin[:,0])):
        raise ValueError("Synthetic source genotype change affects adult return state")
    return edited, frozenset(map(int,A)), frozenset(map(int,I))


def subset(state: types.PlantState, pool: int, n: int) -> types.PlantState:
    if (type(n) is not int or n not in FOUNDER_SIZES
            or not np.array_equal(state.ids,np.arange(48))):
        raise ValueError("Invalid nonreplacement technical founder draw")
    indices = np.sort(ordered_ids(state.ids, pool, DRAW_SALT)[:n])
    fields = ("alleles", "allele_origin", "mutation_flags", "ids", "birth_years")
    return types.PlantState(**{name:getattr(state,name)[indices] for name in fields})


def input_only_qa() -> dict:
    fixtures = original_fixture()
    contexts = {j:original_context(fixtures, "main", j) for j in CONTEXTS}
    rows = []
    source_hashes=[]
    for p in range(POOL_COUNT):
        base=source_state(p)
        source_hashes.append(sha256(base.alleles.tobytes()).hexdigest())
        if np.any(base.mutation_flags) or len(base.ids)!=48:
            raise AssertionError("Synthetic source construction state incorrect")
        selected_by_n={}
        for m in OVERLAPS:
            altered,A,I=assign_hidden_heterozygotes(base,p,m)
            for n in FOUNDER_SIZES:
                old=subset(base,p,n)
                eng=subset(altered,p,n)
                sample=set(map(int,old.ids))
                if n in selected_by_n and selected_by_n[n]!=sample:
                    raise AssertionError("Carrier-overlap intervention changed sampled founders")
                selected_by_n[n]=sample
                a_car=len(A&sample)
                i_car=len(I&sample)
                for j, (cfg,vis) in contexts.items():
                    ledger_parity(old,eng,cfg,vis)
                    led=reproduction.reproduce(eng,vis,cfg)
                    moments=conditional_f1_moments(eng,led)
                    if not moments["eligible"]:
                        raise ValueError("No resident offspring conditional sampling law")
                    rows.append({
                        "synthetic_source_pool":p, "overlap":m,"sample_n":n,
                        "context":j, "A_carriers":a_car,"I_carriers":i_car,
                        "expected_single_offspring_A_variance":moments[
                            "first_offspring_variance_M_I_A"][2],
                        "expected_single_offspring_I_variance":moments[
                            "first_offspring_variance_M_I_A"][1],
                    })
    if (len(rows)!=POOL_COUNT*len(OVERLAPS)*len(FOUNDER_SIZES)*len(CONTEXTS)
            or len(set(source_hashes))!=POOL_COUNT):
        raise AssertionError("Independent technical source fixture domain incomplete")
    return {
        "status":"SYNTHETIC_INDEPENDENT_SOURCE_INPUT_ONLY_NOT_APPROVED",
        "source_support_M":SOURCE_M,
        "source_support_I":SOURCE_I,
        "source_sampling_mode":"Independent SHA-derived uniform categorical draws per pool/adult/trait",
        "n_source_genotype_inputs":POOL_COUNT,
        "source_phenotype_ancestor_type":"Artificial discrete t0, no historical/field source claims",
        "independent_islands_or_mainland_populations_observed":0,
        "n_technical_initial_conditions":len(rows),
        "native_t0_return_parity_checks":len(rows),
        "n_realized_births_or_biological_future_updates":0,
        "n_20_census_response_order_events":0,
        "source_allele_array_sha256":source_hashes,
        "rows":rows,
        "scope_limits":[
            "Input-only synthetic source pools, no biological histories simulated",
            "M/I trait choices are arbitrary source-support examples, not empirical frequencies",
            "A initial expressed phenotype is .5 in every source adult",
            "Only hidden homologs differ across overlap arms; expected t0 return parity is checked",
            "These are not 16 independently field-observed island systems",
            "Cannot infer selection/drift mediation or sustained order or fitness from moments",
            "Future evolution requires independent reviewed registration and separate approval",
        ],
    }


if __name__=="__main__":
    print(json.dumps(input_only_qa(),indent=2,sort_keys=True))
