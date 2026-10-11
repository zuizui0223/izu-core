# Chapter 2: functional-trait mismatch with four pollinator types held constant

**2026-10-11 — exploratory exact synthetic Model 3 operator, not external ecological confirmation.** This extends the Q3→Q4 four-question framework (**threshold → order → realization → consequence**) using the previously documented functional-visitor *replacement* in Draft #452, not simple pollinator absence.

## The missing ecological contrast

Pollinator absence and functional mismatch are DIFFERENT interventions. A plant population can retain four pollinator functional types yet have diminished reproductive compatibility if pollinator optimal floral traits no longer match the resident flowers.

The original `reproduce_kb` affinity model has the functional kernel

```text
affinity(i,v) = (0.1 + expressed_investment_i)
                * exp(-((plant_matching_i - visitor_optimum_v) / breadth_v)^2).
```

This test keeps the **plant's matching trait exactly 0.20**, the visitor functional-type **count at four**, breadth **0.18**, effectiveness **1**, pollen background **B48**, census capacity **K8**, founder genome (eight heterozygotes at investment 0.20/0.50, all initially expressing 0.35), zero mutation and plant immigration, and the original reproduction/allocation model.

Historical source visitor profiles from #452:

| Replacement fraction λ | Four visitor optimum trait values | Mean Gaussian matching kernel (dimensionless) |
|---:|---|---:|
| 0 | 0.15 / 0.35 / 0.55 / 0.75 | **0.361996** |
| 0.25 | 0.275 / 0.45 / 0.625 / 0.80 | 0.247431 |
| 0.50 | 0.40 / 0.55 / 0.70 / 0.85 | 0.078553 |
| 0.75 | 0.525 / 0.65 / 0.775 / 0.90 | 0.010089 |
| 1 | 0.65 / 0.75 / 0.85 / 0.95 | **0.000505** |

The proxy `mean Gaussian matching` is calculated from the *trait-overlap kernel alone* at the original plant matching state 0.20. It is NOT empirical visitation, species overlap, delivered pollen, an externally fitted specialization index or a natural field effect size. The source `reproduce_kb` ledger separately calculates delivered pollen, maternal outcross seeds, viable selfing and paternal parentage for each source state.

All five profiles preserve four visitors; the λ=1 *shifted4* arm is **not** zero visitors.

## Model-internal result: absolute persistence falls, relative expression effect changes sign

The experiment propagates the complete original 165-state diploid-genotype/census Markov transition for 80 reproductive updates, with native inherited-investment expression versus **fixed expression** of investment 0.35 (real alleles still segregate). These are mutually matched at the founding generation.

At resource budget **6**, delayed selfing:

| λ | Mean kernel | P80 native genetic expression | P80 fixed expression | Native − fixed |
|---:|---:|---:|---:|---:|
| 0 | 0.361996 | 0.0262718 | 0.0302426 | **−0.0039708** |
| 0.25 | 0.247431 | 0.01360 | 0.01337 | +0.0002317 |
| 0.50 | 0.078553 | 0.00586 | 0.00259 | +0.0032690 |
| 0.75 | 0.010089 | 0.00529 | 0.00203 | +0.0032572 |
| 1 | 0.000505 | 0.00528 | 0.00203 | **+0.0032565** |

**Ecological distinction:** both arms' *absolute* P80 declines strongly as the visitors' functional optima shift away from the flower state. Only the **relative effect** of allowing genotype-dependent investment expression changes sign. **This is not evidence that mismatch benefits island population survival.**

At budget **8**, the same delayed-selfing native–fixed contrast remains negative from matching λ0 (**−0.0087007**) to shifted λ1 (**−0.0125689**). Hence the apparent expression-benefit reversal at budget6 is **resource-dependent**, not a general law of replacement.

The exploratory 5×4×2 = **40 complete synthetic cells** include all four original mating-system settings and resource budgets6/8. In the budget8 assurance-cost rule, the native–fixed contrast changes from −0.0165085 at λ0 to **+0.0122838** at λ1, illustrating a different interaction. These 40 cells are NOT 40 independent visitors, populations, islands or ecological histories.

## Link to Q1 and the earlier #452 visitor-swap audit

In unmerged #452, same-census/same-genome comparisons with functional visitor replacement reclassified the focal investment β−/group viable seed Γ+ conflict for **176/505** repeated path-year records even when both assemblies had *exactly four* visitor types. Thus replacing functional composition was already tested for **instantaneous source reproductive incentives**, but had NOT established 80-update inherited-genotype or population persistence consequences. The present exact restricted Markov calculation adds the latter to a distinct fixed synthetic source setting; it does NOT retrospectively upgrade the 505 correlated years to independent ecological confirmation.

The earlier #452 **matched total delivered pollen** falsifier is also critical: large collective seed differences between shifted visitor compositions largely vanished after matching the quantity of delivered pollen. Genetically mixed paternal shares and F/P/S incentives could still differ. Accordingly **do not claim the mismatch creates an additional collective seed benefit beyond total pollen arrival**, nor that relative occupancy reversal is caused uniquely by partner routing. Functional matching changes original pollen *quantity* and *recipient/donor structure*, and their separate longitudinal mediation has not been identified here.

## Scientific ranking and next falsifiers

- **Q1 threshold:** functional matching changes local pollen delivery and genetic payoff; fixed richness alone does not fix the investment selection gradient.
- **Q2 order:** no mutation order or forced sequence is manipulated; previous assigned-order practical equivalence remains.
- **Q3 realization:** genetic variation can sort via original parentage with fixed-visitor functional composition, but first-generation founders have the same expressed phenotype.
- **Q4 consequence:** absolute survival effects and *incremental expression treatment* effects must be reported separately, at every budget and mating rule. A positive native−fixed effect at low overlap does not mean the low-overlap condition improves survival relative to the matched reference.

**Next decisive falsifier:** independently justified real or externally parameterized plant/visitor trait distributions, and a prospective contrast distinguishing equal-total-pollen delivery from donor/recipient composition, linked to viable seeds, actual inherited alleles and unconditional population outcome. An activity-scaled source counterfactual alone is not a replacement for ecological measurement.

## Source implementation and boundaries

- Original source Model 3: `scripts/chapter2_kb_reproduction.py::reproduce_kb`.
- Code: `scripts/audit_chapter2_q3q4_functional_mismatch_20261011.py`.
- Regression: `tests/test_chapter2_q3q4_functional_mismatch_20261011.py` checks unchanged richness4, fixed visitor breadth and efficacy, declining compatibility, real source pollen/seed ledger, 165-state stochasticity, and the b6 versus b8 sign counterexample.
- Historic source: unmerged [#452](https://github.com/zuizui0223/izu-core/pull/452) for matched4/shifted4 profiles and within-source visitor replacement.
- Current source: merged [#464](https://github.com/zuizui0223/izu-core/pull/464) for original genome/census factorial and the independent original clonal null #461.
- No new random histories, measured ecological taxa, independent archipelago comparisons, field-calibrated traits, revised frozen #411/#442 estimand, model biology changes or publication claim.
