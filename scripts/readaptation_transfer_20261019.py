"""Seed-derived entry cohorts and the five bounded local destinations.

No production runner: callers must separately admit donor source and contract.
"""
from dataclasses import replace
import hashlib

import numpy as np

from scripts.model3_island.population import inherit
from scripts.model3_island.reproduction import reproduce
from scripts.model3_island.types import VisitorState
from scripts.readaptation_contract_20261019 import canonical, validate, DESIGN


STATE_FIELDS=('alleles','allele_origin','mutation_flags','ids','birth_years')


def cohort_digest(state):
    digest=hashlib.sha256()
    for name in STATE_FIELDS:
        value=np.ascontiguousarray(getattr(state,name))
        digest.update(canonical([name,value.shape,value.dtype.str]))
        digest.update(value.tobytes())
    return digest.hexdigest()


def make_cohort(donor, donor_config, donor_visitors, streams, cohort_key):
    """Native donor reproduction, capped viable seed sampling, fresh entry clock.

    Matrix rows are fathers and columns mothers. Source production is sampled
    before the cap. The cap is standardized transfer, not local recruitment.
    All transferred viable seeds establish at entry by the proposed design.
    """
    if donor_config.mutation_rate!=0:
        raise ValueError('entry experiment requires unchanged inherited alleles')
    if donor_config.capacity!=DESIGN['capacity']:
        raise ValueError('unexpected donor capacity')
    ledger=reproduce(donor,donor_visitors,donor_config)
    weights=ledger.outcross.copy()
    n=len(donor.ids)
    weights[np.diag_indices(n)]+=ledger.self_viable
    total=float(weights.sum())
    if not np.isfinite(total) or total<0 or (weights<0).any():
        raise ValueError('invalid parental contribution weights')
    potential=int(streams['recruitment'].poisson(total))
    count=min(potential,DESIGN['propagule_cap'])
    probabilities=weights/total if total else np.zeros_like(weights)
    if count:
        choices=streams['parents'].choice(n*n,size=count,p=probabilities.ravel())
        fathers,mothers=np.unravel_index(choices,weights.shape)
    else:
        fathers=mothers=np.empty(0,dtype=np.int64)
    children=inherit(donor,mothers,fathers,donor_config,
                     segregation_rng=streams['segregation'],
                     mutation_rng=streams['mutation'],year=1)
    # Population identity is (cohort_key, local ID). Preserve source parent IDs
    # and allele origins in the receipt, rather than mislabeling donor age as
    # the recipient's age. Future births start at the native year-1 ID offset.
    cohort=replace(children,ids=np.arange(count,dtype=np.int64),
                   birth_years=np.zeros(count,dtype=np.int64))
    receipt=dict(allocated=True,cohort_key=list(cohort_key),
                 donor_sha256=cohort_digest(donor),
                 donor_assurance_mode=donor_config.assurance_mode,
                 donor_fixed_assurance=donor_config.fixed_assurance,
                 expected_viable_production=total,source_production=potential,
                 transferred=count,propagule_cap=DESIGN['propagule_cap'],
                 parent_probability_matrix=probabilities.tolist(),
                 father_source_ids=donor.ids[fathers].tolist(),
                 mother_source_ids=donor.ids[mothers].tolist(),
                 cohort_sha256=cohort_digest(cohort))
    return cohort,receipt


def destination_states(contract):
    validate(contract)
    result={'none':VisitorState(np.empty(0,dtype=np.int64),np.empty(0),np.empty(0),np.empty(0))}
    for ai,_ in enumerate(contract['activity']):
        for mi,optima in enumerate(contract['optima']):
            n=len(optima)
            result[f'a{ai}_m{mi}']=VisitorState(
                ids=np.arange(n,dtype=np.int64),optima=np.asarray(optima,dtype=float),
                breadths=np.full(n,contract['breadth']),
                effectiveness=np.full(n,contract['effectiveness'],dtype=float))
    return result


def destination_activity(key,contract):
    validate(contract)
    activities={'none':0.}
    for ai,activity in enumerate(contract['activity']):
        for mi,_ in enumerate(contract['optima']):
            activities[f'a{ai}_m{mi}']=float(activity)
    if key not in activities:
        raise ValueError('unknown destination')
    return activities[key]
