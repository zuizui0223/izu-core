# Q3→Q4 exact native-ledger factorial: genetic sorting versus seed-output feedback

**2026-10-11 — exploratory, deterministic source-operator experiment. Not a preregistered, independently sampled or field-validated study. Not a causal estimate of natural evolutionary suicide.**

## Current scientific decision

The original source Model 3 allows two *mathematically distinct* descendants of a changing heritable investment phenotype: (1) changed net viable maternal seed output, which sets the next Poisson recruitment intensity `mu`, and (2) changed paternal/maternal parentage probabilities `q`, which determine the inherited genotype mix. Can a genetic-parentage shift by itself affect population survival? **Not when viable seed intensity is held independent of genotype under fixed expression.** It can still bias genetic fixation. This is the missing link between Q3 **realization** and Q4 **consequence** after merged #459–#463.

## Native source and finite Markov structure

The script imports **unchanged** `scripts/chapter2_kb_reproduction.py::reproduce_kb` and original Model 3 configurations from `scripts/audit_chapter2_exact_clonal_demographic_null.py` rather than manually reimplementing the pollen kernel.

- Eight initially heterozygous adults: investment alleles `0.20/0.50`, expressed mean `0.35`; matching `0.20` and assurance `0.35` fixed, mutation zero.
- Three possible investment genotypes: `0.20/0.20`, `0.20/0.50`, `0.50/0.50`. Exactly `C(8+3,3)=165` nonnegative finite genotype-count states including extinction.
- `K=8`, fixed pollen background `B=48`, four synthetic static visitor types; original ovule budgets `4.5, 6, 8`, already explored in the #452 pilot.
- Original source genotype-specific seed intensity `mu_native` and parentage-derived Mendelian child probabilities `q_native`; `mu_fixed` and `q_fixed` computed from the same source genomic adults after **reproduction-only** flower investment expression is forced to `0.35`. Their actual diploid parental alleles remain unchanged for transmission.
- Conditional on census `N=n`: `R=min(Poisson(mu),8)`; children from a multinomial distribution `Multinomial(R,q)`. The original `outcross[fathers,mothers]` and diagonal viable-selfing parental weights are respected.

The artificial 2×2 operator forms `(mu_native,q_native)`, `(mu_fixed,q_fixed)`, `(mu_native,q_fixed)` and `(mu_fixed,q_native)`. **The mixed operators are experimental surgery on the source ledger**, not naturally feasible mating systems. Their numerical differences are not mediation proportions.

## Eighty-generation result, original six source settings

The last two source columns isolate the effects under the specified held channel, **not independent population histories**.

| Resource budget | Both native P80 | Both fixed P80 | Only native `mu` P80 | Only native parentage `q` P80 |
|---:|---:|---:|---:|---:|
| 4.5 | 0.000000004700 | 0.000000003940 | 0.000000004382 | 0.000000003940 |
| **6** | **0.02627183** | **0.03024265** | **0.02588795** | **0.03024265** |
| 8 | 0.89404723 | 0.90274790 | 0.89392533 | 0.90274790 |

At budget 6, use `both fixed` as the source-operator reference:

- Complete native-minus-fixed occupancy = **−0.00397082** probability (**−0.3971 percentage points**).
- Change **only viable maternal seed intensity**, while parentage is fixed: **−0.00435470** (**−0.4355 pp**).
- Change **only parental genetic transmission probabilities**, while seed intensity is fixed: **approximately 0**, by a **structural identity** of the clonal expressed seed kernel.
- Remaining **operator interaction** = **+0.00038388** (**+0.0384 pp**), the algebraic difference from the 2×2 factorial. It is not a genetic-causal mediation fraction or a biological compensation parameter.

At budget 8, the full effect is −0.00870067 and the seed-intensity-only effect −0.00882257, with a positive interaction +0.00012191. At budget 4.5, the full effect is tiny and positive (≈+7.6×10⁻¹⁰), close to an extinction floor. None is an independent confirmatory trial.

## Important Q3 finding: genetic sorting without altered occupancy

At budget 6 and generation 80, among populations **still occupied**, probabilities of having fixed the *low investment* allele `0.20` are:

- Full native phenotype + parentage: **62.60%** of occupied source-model population probability mass.
- Entirely fixed expression, neutral parentage: **approximately 50%** (exactly equal low/high fixation probabilities; a minute fraction of occupied populations remains genetically segregating).
- **Native parentage only** with fixed viable seed intensity: **55.13%**, yet the population P80 remains exactly unchanged from the fully fixed case (≈3.0243%).

The final case is the decisive conceptual control: the source parentage operation can bias genotype fixation while **demographic occupancy is unaltered**. The original fixed-expression kernel is **lumpable by census N**: if `mu(N)` depends only on the number of adults, its `N→N'` transition probabilities do not depend on the genetic composition or the genotype lottery. The exact Markov calculation verifies this over all 80 generations. **Genetic evolution/segregation cannot change survival in this restricted case until genetic differences affect a reproductive or demographic quantity such as `mu`.**

Interpret the low-fixation fractions as *survivor-conditioned* distributions. They combine within-population parental contribution, drift and differential survival of genotype compositions. They are **not** a direct estimate of selection coefficients, unconditional allele-frequency evolution or a genetic survival-mediation effect.

## Inferential boundary and next experiment

The research spine is **閾値 → 順序 → 実現 → 帰結**:

- **Q1 閾値:** Individual full genetic return, positive pollen externality and collective viable seed are different estimands. This factorial is at a selected, fixed ecological fixture, not a calibrated island threshold.
- **Q2 順序:** Mutation or expression order is not randomized or observed here. #418's near/far assigned-order pooled result remains practically equivalent; this cannot overturn it.
- **Q3 実現:** Mendelian segregation + parentage bias can change fixation distributions; observed post-survival genotype means and fixation fractions are conditional on survival, not an independent adaptive response.
- **Q4 帰結:** In this restricted operator, changed mean viable seed intensity `mu` is required for genetically sorted adult compositions to alter demography. A finite-Poisson crowding cap and subsequent census histories mediate that effect through the modeled transition law.

**Next admissible high-value test:** independently justified same-genome population histories including dynamic visitors and standing trait variation, with advance-fixed mating-system and demographic source conditions, requiring independent source–mechanism–recruitment–occupancy measurements and null cases. Do not use these exposed budget4.5/6/8 contrasts to select a favourable confirmatory treatment after observation.

## Reproduction and source provenance

- `scripts/audit_chapter2_q3q4_exact_genotype_factorial_20261011.py`: native-ledger 165×165 matrix with two independently controlled biological readout channels; output JSON contains each setting's first/late occupancy and genotype-class fixation.
- `tests/test_chapter2_q3q4_exact_genotype_factorial_20261011.py`: original `N=8` ledger source `mu=8.994424151`, first-generation identity, original no-genetic-change #461 reference, 165-state mass conservation, identical-`N` `mu` lumpability, original 80-step results, fixation and evidence-rank tests.
- Source references: merged [#461](https://github.com/zuizui0223/izu-core/pull/461) (exact clonal demographic null), merged [#462](https://github.com/zuizui0223/izu-core/pull/462) (Q3 exact finite Mendelian moments), merged [#463](https://github.com/zuizui0223/izu-core/pull/463) (time sign reversal).
- Prior independent model campaign [#411](https://github.com/zuizui0223/izu-core/pull/411) and capacity campaign [#442](https://github.com/zuizui0223/izu-core/pull/442) retain their frozen status. The active one-paper manuscript and earlier Draft #452 remain untouched.
