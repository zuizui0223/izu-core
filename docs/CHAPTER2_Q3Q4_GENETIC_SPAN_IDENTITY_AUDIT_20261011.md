# Q3→Q4: hidden allelic variance changes 80-update consequences at fixed founder phenotype

**Date:** 2026-10-11. **Evidence:** deterministic, post-discovery sensitivity in *one* synthetic Model 3 family, not an independently preregistered experiment, measured island response, or an evolved reproductive-assurance-to-extinction causal test.

## Immediate scientific decision

An earlier stand-alone follow-up incorrectly suggested that moderate hidden genetic variation could improve 80-update occupancy at K8/budget6. That numerical result was **INVALID**: it identified the alternate inherited allele by checking whether its numeric value was exactly `0.50`. Changing the source allele values to `0.30/0.40` or `0.25/0.45` consequently and incorrectly treated every inherited allele as the "low" class. This PR corrects the inference by using **genotype-class identity**, not the floating-point value of the allele, to compute Mendelian gamete probabilities.

**Corrected descriptive result:** in the source K8/B48 fixed-visitor synthetic model, all four original mating systems at resource budgets 6 and 8 have a more negative native-genomic-expression-minus-fixed-expression P80 contrast as the founder allele separation increases from zero through ±0.05, ±0.10 and ±0.15. At budget 4.5 both expression policies are very close to the extinction floor and contrasts are tiny (absolute probability difference under 2×10⁻⁹). These conditions were chosen after exploratory outcomes and are **not** a general biological law.

## Source biology and genetic initial condition

- Eight founding parents are **all heterozygotes**, with *the same expressed floral investment value 0.35* in every tested arm. Founder matching and assurance are fixed at 0.20 and 0.35, respectively.
- Change only the founding investment homolog values `(0.35−w, 0.35+w)`, where `w = 0, 0.05, 0.10, 0.15`. Thus the founders' displayed trait and their first-year fecundity are identical for every `w`, while inherited segregation variance scales with `w²`.
- The reproductive operator is the **unchanged** `scripts/chapter2_kb_reproduction.py::reproduce_kb` with fixed pollen-background B48 and the original four mating-system settings. Visitor availability and composition are the original *static* four artificial visitor functions.
- Demography: original zero-survival, zero-immigration, zero-mutation eight-place capped Poisson offspring recruitment; parental transmissions follow the unchanged original donor-row/mother-column outcross + viable-selfing weights. Every inherited genotype-count state is integrated by an exact 165-state Markov chain for 80 reproductive updates.
- The comparator fixes **reproductive expression** of investment at 0.35 while still allowing original biparental inheritance and neutral genetic sorting; it does **not** freeze diploid alleles or change the spontaneous mutation-order biology of #411.
- The four original ovule budgets/settings are not newly calibrated to island field populations. The 4×3×4 = **48 synthetic source evaluations** are related interventions within one model family, not 48 independent replicates.

## Corrected exact model results: probability difference at update 80

All entries are `P(occupied80 | native genotype-dependent expression) − P(occupied80 | fixed expressed investment=0.35)`, shown in **absolute probability units**.

| Mating setting | Budget | w=0 | w=0.05 | w=0.10 | w=0.15 |
|---|---:|---:|---:|---:|---:|
| Delayed selfing | 6 | 0 | −0.00047303 | −0.00184325 | −0.00397082 |
| Prior selfing | 6 | 0 | −0.00014394 | −0.00056294 | −0.00122373 |
| Pollen discount | 6 | 0 | −0.00001858 | −0.00008349 | −0.00022277 |
| Assurance cost | 6 | 0 | −0.00006494 | −0.00025063 | −0.00053182 |
| Delayed selfing | 8 | 0 | −0.00094554 | −0.00381381 | −0.00870067 |
| Prior selfing | 8 | 0 | −0.00119754 | −0.00483600 | −0.01105272 |
| Pollen discount | 8 | 0 | −0.00130945 | −0.00528505 | −0.01206629 |
| Assurance cost | 8 | 0 | −0.00181276 | −0.00728374 | −0.01650848 |

For budget 4.5, all four mating rules and all four genetic widths are retained in the executable 48-cell readout. The finite 80-update endpoint is near the extinction floor in both policies; differences can be tiny positive values on the order 10⁻¹¹–10⁻⁹ and are **not** a survival benefit that warrants a headline.

**Original K8/budget6 delayed selfing check:** w=0.15 reproduces the prior native P80 0.02627183 vs fixed P80 0.03024265 (Δ=−0.00397082), whereas w=0.05 has Δ=−0.00047303. The source-first reproduction and first-generation inherited-genotype lottery stay matched between native/fixed at the common heterozygous founder phenotype.

## Why this is useful (and what it does not show)

The **same average starting phenotype** can conceal very different segregating inheritance. In a small population, the magnitude of segregating variation can alter both short-lived genetic sorting and later source reproduction under the density cap. This clarifies a mechanistic assumption behind the Q3→Q4 result: the previously reported negative occupancy change at founder alleles 0.20/0.50 is **not a universal effect of allowing genetic inheritance**; its magnitude depends on how much investment genetic variation is present, on resource budget and mating system.

The corrected model does **not** establish natural selective evolution, an externally calibrated variance threshold, evolutionary suicide, or the demographic mediation of #411's evolving assurance. It does not make #418's prior assigned-order practical equivalence false. The difference between a post-discovery mathematical parameter sensitivity and a new independently confirmed evolutionary prediction remains strict.

## Source and verification contract

- `scripts/audit_chapter2_q3q4_genetic_span_20261011.py`: source-native original `reproduce_kb` with 165-state exact genotype/census Markov and 48 complete source-grid cells. Uses **genotype classes 0/1/2** for Mendelian transmission; never compares alleles to a hardcoded high value.
- `tests/test_chapter2_q3q4_genetic_span_20261011.py`: ensures all common expressed founder phenotypes produce identical initial reproduction and child-genotype lottery **[0.25,0.50,0.25]**, regardless of actual allele values; checks founder homozygotes, 165-state mass conservation, eight previously frozen b6/b8 reference contrasts and all 48 cells.
- Source upstream: merged #464 (original genomic-factorial source ledger), merged #462 (one-generation inherited moments), and Draft #465 (time dependence across original mating systems); verified independent existing source receipts #411 and #442 remain unchanged.
- **No new stochastic histories or field observations** were created. All numerical checks are conditional on the unchanged original source operator; this does not publish or retitle the active manuscript.
