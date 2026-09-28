"""Declared finite-population floral inheritance model, separate from legacy models.

Access and investment are abstract functional traits, not colour categories.
Pollen matrices use donor rows and recipient columns throughout.
"""
from __future__ import annotations

import numpy as np

from scripts.model3_reproduction import reproductive_ledger


def pollen_transfer(traits, visitors, breadth, activity, budget, background):
    """Finite donor pollen, visitor-mediated mixing and explicit off-population loss."""
    traits = np.asarray(traits, dtype=float)
    visitors = np.asarray(visitors, dtype=float)
    if (traits.ndim != 2 or traits.shape[1] != 2
            or not np.isfinite(traits).all() or ((traits < 0) | (traits > 1)).any()
            or visitors.ndim != 1 or not np.isfinite(visitors).all()
            or ((visitors < 0) | (visitors > 1)).any()):
        raise ValueError('traits must be N x 2 and visitors a vector in [0,1]')
    values = np.array([breadth, activity, budget, background], dtype=float)
    if not np.isfinite(values).all() or breadth <= 0 or activity < 0 or budget < 0 or background <= 0:
        raise ValueError('invalid pollen-transfer parameters')
    n = len(traits)
    if len(visitors) == 0 or activity == 0 or n == 0:
        return np.zeros((n,n))
    affinity = (.1 + traits[:,1,None]) * np.exp(-((traits[:,0,None]-visitors)/breadth)**2)
    total_affinity = affinity.sum(axis=1, keepdims=True)
    channels = np.divide(affinity, total_affinity, out=np.zeros_like(affinity), where=total_affinity>0)
    removed = budget * (-np.expm1(-activity*affinity.mean(axis=1)))
    recipient_share = affinity / (affinity.sum(axis=0, keepdims=True) + background)
    transfer = (removed[:,None]*channels) @ recipient_share.T
    np.fill_diagonal(transfer, 0.)
    return transfer


def inherit(genotype, mothers, fathers, rng):
    """Unlinked diploid Mendelian gametes; no mutation or trait-target update."""
    genotype = np.asarray(genotype, dtype=float)
    mothers, fathers = np.asarray(mothers), np.asarray(fathers)
    if (genotype.ndim != 3 or genotype.shape[1:] != (2,2)
            or not np.isfinite(genotype).all() or ((genotype<0)|(genotype>1)).any()
            or mothers.ndim != 1 or mothers.shape != fathers.shape
            or mothers.dtype.kind not in 'iu' or fathers.dtype.kind not in 'iu'
            or (mothers<0).any() or (fathers<0).any()
            or (mothers>=len(genotype)).any() or (fathers>=len(genotype)).any()):
        raise ValueError('invalid genotypes or parental indices')
    count = len(mothers)
    maternal = rng.integers(0,2,size=(count,2))
    paternal = rng.integers(0,2,size=(count,2))
    loci = np.arange(2)[None,:]
    return np.stack([genotype[mothers[:,None],loci,maternal],
                     genotype[fathers[:,None],loci,paternal]],axis=-1)


def neutralize(pairs):
    """Remove parent identity selection but retain self/outcross offspring totals."""
    pairs = np.asarray(pairs, dtype=float)
    if (pairs.ndim != 2 or pairs.shape[0] != pairs.shape[1] or not len(pairs)
            or not np.isfinite(pairs).all() or (pairs<0).any()):
        raise ValueError('expected nonempty nonnegative finite parental matrix')
    n = len(pairs)
    outcross = pairs.copy()
    np.fill_diagonal(outcross,0.)
    result = np.full_like(pairs, outcross.sum()/(n*(n-1)) if n>1 else 0.)
    np.fill_diagonal(result, np.trace(pairs)/n)
    return result


def next_population(genotype, pairs, survival, capacity, rng):
    """Adult persistence plus finite viable recruitment; never rescue extinction.

    Density-independent establishment is implicit until capacity; excess viable
    recruits are thinned without regard to traits. Drawing parents only for the
    retained recruits is equivalent to uniform thinning of exchangeable recruits.
    """
    genotype = np.asarray(genotype, dtype=float)
    pairs = np.asarray(pairs, dtype=float)
    if (genotype.ndim != 3 or genotype.shape[1:] != (2,2)
            or not np.isfinite(genotype).all() or ((genotype<0)|(genotype>1)).any()
            or pairs.shape != (len(genotype),len(genotype))
            or not np.isfinite(pairs).all() or (pairs<0).any()
            or not np.isfinite(survival) or not 0 <= survival <= 1
            or not isinstance(capacity, (int,np.integer)) or capacity < len(genotype)):
        raise ValueError('invalid demographic state or parameters')
    survived = rng.random(len(genotype)) < survival
    adults = genotype[survived]
    total = pairs.sum()
    if not np.isfinite(total):
        raise ValueError('nonfinite reproductive total')
    potential = int(rng.poisson(total))
    established = min(capacity-len(adults), potential)
    if established:
        selected = rng.choice(pairs.size, size=established, p=pairs.ravel()/total)
        fathers, mothers = np.unravel_index(selected, pairs.shape)
        children = inherit(genotype, mothers, fathers, rng)
        result = np.concatenate([adults,children],axis=0)
    else:
        result = adults.copy()
    return result, dict(survivors=int(survived.sum()), potential_recruits=potential,
                        established=established)


def simulate(*, seed, years=80, activity=1., island_community=False,
             selfing=0., survival=0., start=.3, control='selected', capacity=48):
    """Run reproductive years (not generations for perennials).

    Community RNG is independent of plant response and shared across controls,
    starts, activity and life history for the same seed/community scenario.
    This supports controlled within-seed contrasts; seeds are the replicates.
    """
    if (not isinstance(seed,(int,np.integer)) or seed < 0
            or not isinstance(years,(int,np.integer)) or years < 1
            or control not in ('selected','neutral','fixed')
            or not isinstance(island_community,(bool,np.bool_))
            or not np.isfinite([activity,selfing,survival,start]).all()
            or activity < 0 or not 0 <= selfing <= 1 or not 0 <= survival < 1
            or not .1 <= start <= .9 or not isinstance(capacity,(int,np.integer))
            or capacity < 2):
        raise ValueError('invalid simulation settings')
    founder_rng = np.random.default_rng(np.random.SeedSequence([seed,1]))
    visitor_rng = np.random.default_rng(np.random.SeedSequence([seed,2,int(island_community)]))
    # Separate from all visitor draws. Common demographic seed is variance
    # reduction only: different population sizes consume different draws.
    demo_rng = np.random.default_rng(np.random.SeedSequence([seed,3]))
    genotype = np.array([start,.5])[None,:,None] + founder_rng.uniform(-.1,.1,(capacity,2,2))
    founder_mean = genotype.mean(axis=(0,2))
    if control == 'fixed':
        genotype[:] = founder_mean[None,:,None]
    initial_genotype = genotype.copy()
    visitors = visitor_rng.uniform(0,1,4 if island_community else 9)
    arrival, loss = (.1,.15) if island_community else (.3,.05)
    population = np.zeros(years+1,dtype=int)
    trait_mean = np.full((years+1,2),np.nan)
    trait_variance = np.full((years+1,2),np.nan)
    allele_count = np.zeros((years+1,2),dtype=int)
    visitor_count = np.zeros(years,dtype=int)
    expected_outcross = np.zeros(years)
    expected_selfed = np.zeros(years)
    established = np.zeros(years,dtype=int)
    survivors = np.zeros(years,dtype=int)
    potential_recruits = np.zeros(years,dtype=int)
    extinction_year = None

    def record(year):
        population[year] = len(genotype)
        if len(genotype):
            traits = genotype.mean(axis=2)
            trait_mean[year] = traits.mean(axis=0)
            trait_variance[year] = traits.var(axis=0)
            allele_count[year] = [len(np.unique(genotype[:,locus])) for locus in range(2)]

    record(0)
    for year in range(years):
        # Record the community that actually supplies this year's pollen.
        visitor_count[year] = len(visitors)
        if len(genotype):
            traits = genotype.mean(axis=2)
            n = len(genotype)
            pairs = np.zeros((n,n))
            for _episode in range(2):
                transfer = pollen_transfer(traits, visitors, .2, activity,
                                           20*(1-survival)/2, capacity)
                ledger = reproductive_ledger(
                    transfer, 8*(1-survival)*np.exp(-.5*traits[:,1]**2)/2,
                    np.ones(n),np.full(n,selfing),np.full(n,.5))
                pairs += ledger['outcross_by_donor_recipient']
                pairs[np.diag_indices(n)] += ledger['selfed_viable']
                expected_outcross[year] += ledger['female_outcross'].sum()
                expected_selfed[year] += ledger['selfed_viable'].sum()
            if control == 'neutral':
                pairs = neutralize(pairs)
            genotype, info = next_population(genotype,pairs,survival,capacity,demo_rng)
            survivors[year] = info['survivors']
            established[year] = info['established']
            potential_recruits[year] = info['potential_recruits']
            if control == 'fixed':
                genotype[:] = founder_mean[None,:,None]
            if not len(genotype):
                extinction_year = year+1
        record(year+1)
        # Community keeps running even after plant extinction, without feedback.
        visitors = visitors[visitor_rng.random(len(visitors)) >= loss]
        if visitor_rng.random() < arrival:
            visitors = np.append(visitors,visitor_rng.uniform())
    return dict(population=population,trait_mean=trait_mean,trait_variance=trait_variance,
                allele_count=allele_count,
                visitor_count=visitor_count,expected_outcross=expected_outcross,
                expected_selfed=expected_selfed,established=established,
                survivors=survivors,potential_recruits=potential_recruits,
                extinction_year=extinction_year,initial_genotype=initial_genotype,
                final_genotype=genotype.copy())
