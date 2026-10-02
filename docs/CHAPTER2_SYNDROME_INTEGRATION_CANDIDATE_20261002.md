# Chapter 2 vNext integration candidate — syndrome as an emergent outcome

**Date:** 2026-10-02  
**Status:** candidate integration only; current Oikos submission surface remains locked  
**Source PR:** #380

## Recommendation

Do not silently rewrite the currently closed submission package. The new experiments
materially strengthen the causal novelty, but integrating them into the submitted
story would require a coordinated manuscript, figure, Supporting Information and
machine-readable lock update.

The scientific vNext should change the centre of gravity from:

> visitor amount sets the coarse regime while ecological and demographic finiteness modify realization

to the broader causal statement:

> **Island, selfing and pollination syndromes are emergent outcomes of separable
> ecological, reproductive, genetic and demographic filters rather than mechanisms
> in themselves.**

The existing visitor-amount/history/demography result remains an important middle
layer, not the whole novelty.

## Chapter 1 -> Chapter 2 logic

### Chapter 1

Chapter 1 asks **what actually recurs in nature**.

Its handoff is:

- geographic isolation is associated with stronger pollen limitation;
- reproductive assurance and floral accessibility/generalization recur;
- detailed pollinator-facing display does not converge on one regional direction.

Therefore the empirical island syndrome is more repeatable at the level of
functional problem/insurance than at the level of detailed phenotype.

### Chapter 2 vNext

Chapter 2 asks **why that empirical pattern can be generated**.

The expanded causal architecture is:

```text
isolation
   ↓
visitor amount / functional composition
   ↓
pollen transfer and outcross opportunity
   ↓
┌──────────────────────────────────────────────┐
│ assurance substitutes for lost reproduction │
│ functional replacement changes matching     │
└──────────────────────────────────────────────┘
   ↓
selection on pollinator-facing traits
   ↓
available standing variation
   ↓
de novo mutation / genetic coupling
   ↓
finite recruitment / persistence
   ↓
realized syndrome components
```

This connects the macroecological regularity in Chapter 1 to an explicit
within-population generative mechanism in Chapter 2.

## What existing theory already explains

The novelty claim must explicitly concede the strong existing components.

- Porcher & Lande (2005) model pollen limitation, pollen discounting, selfing and
  inbreeding depression. They establish a mating-system route from pollen limitation
  to high selfing, not the full downstream realization of multiple pollinator-facing
  traits. DOI: 10.1111/j.1420-9101.2005.00905.x
- Sargent & Otto (2006) model how pollinator abundance and effectiveness alter the
  evolution of floral specialization. DOI: 10.1086/498433
- Dellinger (2020) reviews pollination syndromes as recurrent suites of floral
  traits associated with functional pollinator groups and their empirical limits.
  DOI: 10.1111/nph.16793
- Cui & Yuan (2026) review the genomic and molecular basis of pollination-syndrome
  transitions and emphasize coordinated multi-trait change, delayed selfing,
  standing variation and genetic architecture. DOI:
  10.1146/annurev-arplant-072125-082325
- Eriksson & Pontarp (2026) provide a trait-based plant-pollinator eco-evolutionary
  simulation focused on pollinator adaptation to changing plant abundance.
  DOI: 10.1002/ece3.73182
- Classical/general dynamic island-biogeography models focus on colonization,
  extinction, speciation, area, isolation and island ontogeny rather than the
  within-population pollination-to-floral-evolution chain.

The vNext novelty is therefore the **connection and decomposition of stages**, not
the invention of any individual component.

## New numerical evidence

### 1. Adaptive reduction requires more than relaxed positive selection

At low visitor activity (0.05), the unchanged Model 3 operator gives:

| assurance | investment cost | fixed total investment gradient | finite endpoint |
|---:|---:|---:|---|
| 0.0 | 0.5 | +0.602 | extinct |
| 0.5 | 0.0 | +0.611 | persists |
| 0.5 | 0.5 | **-0.393** | persists |
| 0.5 | 0.5, activity 0.4 | **+1.681** | persists |

Thus pollinator scarcity alone does not generate adaptive investment reduction.
The negative gradient appears when:

1. lost outcross service reduces the marginal return to pollinator-facing investment;
2. reproductive assurance keeps a reproductive route open;
3. positive investment cost remains.

This is a mechanistic distinction between **relaxed pollinator-mediated selection**
and **adaptive reduction of a costly attraction/display axis**.

### 2. Pollinator replacement is a different causal route

At identical visitor count, left4 versus right4 composition changes the fixed
investment gradient by:

- +2.377 at starting access 0.2;
- ~0 at starting access 0.5;
- -2.377 at starting access 0.8.

The corresponding deterministic inherited contrasts are +0.189, 0 and -0.189.

Therefore visitor scarcity and functional rematching are not interchangeable
versions of the same perturbation.

### 3. Selection and evolutionary accessibility are separable

Reducing standing genetic variation in one trait axis while leaving the ecological
operator unchanged suppresses the response specifically on that axis.

Average lost response when standing SD is reduced from 0.15 to 0.03:

| constrained axis | deterministic | finite ABM |
|---|---:|---:|
| access-like | 0.1136 | 0.0961 |
| investment-like | 0.1054 | 0.0830 |

This provides a direct mechanism for incomplete or asynchronous syndrome
realization without requiring different ecological selection.

### 4. Standing variation dominates de novo mutation in the current finite horizon

The first preregistered mutation/pleiotropy timing experiment failed because the
investment axis almost never crossed the fixed 0.05 sustained-response threshold
by year 400. That failure is retained.

A new prospective diagnostic then separated standing investment variation, de
novo mutation supply and population capacity:

| genetic filter | increase in absolute investment response |
|---|---:|
| restore standing variation | **+0.14777** |
| increase de novo investment mutation supply | **+0.01389** |
| extra mutation rescue from capacity 48 -> 192 | **+0.00102** |

The mutation rescue is ~9.4% of the standing-variation effect. The capacity
modulation is ~7.3% of the mutation-rescue effect.

Within this synthetic horizon, the strongest identified genetic bottleneck is
therefore variation already present when ecological selection begins.

## What this changes conceptually

The old question:

> Why does the same island pressure produce different floral trajectories?

becomes more precise:

> **At which stage does a recurrent ecological problem cease to imply a recurrent
> phenotypic solution?**

The current numerical answer is:

1. **ecological return:** visitor amount and composition determine the selective problem;
2. **reproductive substitution:** assurance changes persistence and the value of
   pollinator-facing investment;
3. **genetic accessibility:** standing variation determines how much of the favoured
   response is immediately reachable;
4. **new mutation:** can partly expand that reachable space, but was secondary in
   the tested finite horizon;
5. **finite realization/history:** recruitment, extinction, chronology and
   connectivity determine which accessible trajectories persist.

Thus a “syndrome” can recur at one layer and fail to recur at the next.

## Trait interpretation

Do not write “colour is easy, morphology is hard” as a result.

The defensible formulation is:

> **Different visible trait modules may have different evolutionary accessibility
> because they differ in standing variation, mutational target size, effect-size
> distributions and developmental/pleiotropic coupling.**

There is empirical motivation for that decomposition, but no universal ranking:

- a major anthocyanin QTL between *Mimulus lewisii* and *M. cardinalis* maps to
  the R3 MYB regulator ROI1 (Yuan et al. 2013,
  DOI: 10.1534/genetics.112.146852);
- corolla-tube formation in *Mimulus* depends on coordinated tasiRNA-ARF/auxin
  developmental growth, while large-effect loss-of-function mutations can still
  disrupt fusion (Ding et al. 2020, DOI: 10.1105/tpc.18.00471).

These examples motivate trait-specific accessibility; they do not identify the
molecular basis of the abstract Model 3 axes.

## Recommended manuscript architecture if the package is deliberately reopened

### Introduction

Replace a generic “context dependence” gap with:

> syndrome labels summarize recurrent outcomes but do not identify which ecological,
> reproductive, genetic or demographic stage generated them.

### Methods

Add three nested intervention blocks after the existing fixed-state assay:

1. assurance x investment-cost causal knockout;
2. same-count functional-rematching contrast;
3. standing-variation and mutation-rescue genetic-filter experiments.

Keep the failed mutation/pleiotropy threshold experiment in Supporting Information
as a prospectively retained negative result.

### Results

Recommended order:

1. functional matching creates state-dependent selection;
2. **assurance + cost can reverse the sign of selection under low service;**
3. **functional replacement produces a distinct rematching route;**
4. isolation/visitor amount sets the coarse regime;
5. **standing variation filters which trait response is reachable;**
6. finite visitor history and finite plant demography filter realization;
7. chronology/assurance/connectivity alter persistence;
8. real-island layer confrontation.

### Discussion

Open with:

> **Syndromes are outcomes, not mechanisms.**

Then distinguish:

- reproductive assurance;
- relaxed versus negative selection on attraction;
- pollinator rematching;
- genetic accessibility;
- demographic realization.

### Figures

Do not add many new panels to the current four figures. A vNext package should
probably make one new causal-decomposition figure and move detailed genetic-filter
diagnostics to SI.

## Integration decision

**Scientific value: high.** The new results directly answer the user's intended
Chapter 2 role: convert descriptive syndrome language into an explicit numerical
causal hierarchy.

**Submission disruption: also high.** The current Oikos package is machine-locked as
scientifically closed, so integration should be treated as a deliberate vNext
reopening rather than a silent patch.

Until that deliberate reopening, PR #380 should remain a source-complete,
tested extension beside the current submission surface.
