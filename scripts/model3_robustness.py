"""Separately parameterized robustness model; frozen campaign remains untouched.

Forward-ported from model3_evolution.simulate at commit28d56f8. Default-settings
exact replay is required by tests. New reproductive parameters act BEFORE parent
sampling and inheritance; limitation indices are recorded before density thinning.
No scientific robustness campaign has been admitted by this module alone.
"""
from __future__ import annotations
import numpy as np
from scripts.model3_evolution import pollen_transfer, neutralize, next_population
from scripts.model3_reproduction import reproductive_ledger


def simulate_scenario(*, seed, years=80, activity=1., island_community=False,
             selfing=0., survival=0., start=.3, control='selected', capacity=48, depression=.5, pollen_scale=1.,
                      investment_cost=.5, ovule_effort='lifetime',
                      pollen_effort='lifetime', background_ratio=1.):
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
    if (not np.isfinite([depression,pollen_scale,investment_cost,background_ratio]).all()
            or not 0<=depression<=1 or pollen_scale<=0 or investment_cost<0 or background_ratio<=0
            or ovule_effort not in ('lifetime','annual') or pollen_effort not in ('lifetime','annual')):
        raise ValueError('invalid robustness parameters')
    ovule_multiplier=(1-survival) if ovule_effort=='lifetime' else 1.
    pollen_multiplier=(1-survival) if pollen_effort=='lifetime' else 1.
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
    ovule_supply = np.zeros(years)
    selfed_raw = np.zeros(years)
    inbreeding_loss = np.zeros(years)
    pollen_limitation = np.full(years,np.nan)
    viable_limitation = np.full(years,np.nan)
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
                                           20*pollen_multiplier/2, capacity*background_ratio)
                ledger = reproductive_ledger(
                    transfer, 8*ovule_multiplier*np.exp(-investment_cost*traits[:,1]**2)/2,
                    np.full(n,pollen_scale),np.full(n,selfing),np.full(n,depression))
                pairs += ledger['outcross_by_donor_recipient']
                pairs[np.diag_indices(n)] += ledger['selfed_viable']
                expected_outcross[year] += ledger['female_outcross'].sum()
                expected_selfed[year] += ledger['selfed_viable'].sum()
                ovule_supply[year] += (8*ovule_multiplier*np.exp(-investment_cost*traits[:,1]**2)/2).sum()
                selfed_raw[year] += ledger['selfed_raw'].sum()
                inbreeding_loss[year] += (ledger['selfed_raw']-ledger['selfed_viable']).sum()
            if ovule_supply[year]>0:
                pollen_limitation[year]=1-expected_outcross[year]/ovule_supply[year]
                viable_limitation[year]=1-(expected_outcross[year]+expected_selfed[year])/ovule_supply[year]
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
                final_genotype=genotype.copy(),ovule_supply=ovule_supply,selfed_raw=selfed_raw,
                inbreeding_loss=inbreeding_loss,pollen_limitation_before_selfing=pollen_limitation,
                viable_seed_limitation=viable_limitation)
