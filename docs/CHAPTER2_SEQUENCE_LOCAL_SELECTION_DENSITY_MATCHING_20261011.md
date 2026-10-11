# Chapter 2 — Why the observed sequence may arise: selection thresholds depend jointly on census and functional matching

**2026-10-11, post-discovery fixed-source diagnostic.** This is a new **model-internal ecological counterfactual**, not a preregistered cohort, actual selection-gradient history, independent island experiment or demonstration of naturally evolved temporal order.

## Scientific question

The proposed order-centered paper says reproductive assurance A may become advantageous before lower floral investment I. The critical falsifier is whether investment **is always initially selected to increase** before pollinator functional mismatch accumulates, while assurance is already selected to increase. The model's density and visitor effects must be separated.

At one **fixed plant genome** with matching=0.20, investment=0.35 and assurance=0.35, hold four visitor functional types, pollen background B48, ovule budget6 and original reproductive source operator unchanged. Cross:

- Plant current census **N=8,24,48**, but always **capacity K=48** and pollen background B48; this varies current density, not demographic carrying capacity.
- Visitor functional optimum profiles from the historical `matched4` to `shifted4` four-type assemblages, interpolation fractions **0, .25, .50, .75, 1**; all have four types and equal widths/effectiveness.
- A 2×2 factorial of **autonomous selfing timing** (delayed/prior) and **direct assurance allocation cost** (0/0.5). This explicitly disentangles the two factors that differed simultaneously in the historical 51/64 versus 38/64 comparison.
- Two symmetric derivative steps **0.005 and 0.0025** and a finite-sign deadband of ±0.02, preserving uncertain numerical signs. No ecological parameter is selected after an independently exposed viability result to claim prospective confirmation.

Use the original full focal genetic return

```text
W_i = 0.5 maternal viable outcross_i
    + 0.5 paternal viable outcross_i
    + viable selfed offspring_i

beta_trait = d log(W_i)/d(expressed focal trait_i)
```

**Perturb only the first plant's diploid trait-mean**, not the whole population, and evaluate `reproduce_kb` with both maternal and paternal pollen contributions. These are the local source invasion-style *finite one-focal* derivatives at each resident reference N. They are not true rare-mutant infinite-population gradients, not observed allele-frequency changes and not time-inferred switching events.

## Key post-discovery source-operator diagnostic (independent formula check, original source CI pending)

At delayed selfing with zero direct assurance cost, local floral-investment log return derivatives are:

| Visitor functional mismatch fraction | N8 beta_I | N24 beta_I | N48 beta_I |
|---:|---:|---:|---:|
| 0 | **−0.0632** | **+0.3129** | **+0.5840** |
| 0.25 | −0.1488 | +0.1483 | +0.3923 |
| 0.50 | −0.3225 | −0.2656 | −0.1933 |
| 0.75 | −0.3495 | −0.3484 | −0.3467 |
| 1 | −0.3500 | −0.3500 | −0.3500 |

The local assurance log return derivative beta_A is **positive at every tested N and every mismatch fraction** (it remains positive even when a direct assurance cost0.5 is introduced in this source fixture).

This yields an important **conditional mechanism diagnosis**:

- In **larger** resident populations (N24/48), the source return favors investment at good functional matching, but shifts to opposing investment between 25% and 50% functional optimum replacement. In this restricted fixed-genotype environment, there is therefore an ecological **investment fitness-sign switch**.
- In **small N8** populations, *investment is already selected against at the matched baseline*, even before functional mismatch increases. A proposed universal rule that "assurance must be selected first because attraction initially remains beneficial" is **refuted within the source Model3**. A chronological A-first genetic response at N8 can arise from initial standing variation, different trait supply/response speed or threshold conventions even without a later investment-selection sign switch.
- The original source cost/timing factorial checks all four combinations at identical plant genotypes and visitor distributions. Comparing the historically observed delayed/costly sequence to prior/costless sequence by itself cannot identify the effect of selfing timing.

**This is not a test that the recorded A-first 51/64 histories were explained by density.** It supplies *conditional source fitness reasons* that density and functional matching need to be included in the next experiment. These numeric values are not independently sampled observed population estimates.

## Implications for the proposed order-centered manuscript

The attractive title "What evolves first need not be what caused or benefited later evolution" is an interpretable hypothesis, **not yet a validated blanket causal theorem**. We currently have:

1. An archived historical 51/64 assurance-first crossing in one delayed/costly condition, but strong founder-relative versus additional-isolation ordering differences (paired source PR #472).
2. Four-setting independent evidence that assurance evolution is **not necessary** for reduced investment and modulates the near–far phenotype gap (#411).
3. Independently preregistered practical equivalence (±.05) of an **assigned transient expression-order × environment interaction** (#418); that is NOT a test of naturally occurring mutation sequence.
4. A source-only ecological gradient threshold that changes with BOTH density and functional matching (this audit), while next-generation genetic return covariance/finite Mendelian realization has separate source-level evidence (#462/#470).
5. The 80-update persistence contrasts in #461–#471 are synthetic population-model counterfactuals; none automatically proves fitness effects of actual evolved historical order.

## Next decisive test

**A: genuine retrospective sign-onset vs allele-onset diagnostic.** The frozen annual t0–1000 `trace` matrices hold census and three trait means/variances but **not each adult's full diploid genotype at every year**; original `*.npz` checkpoints contain diploid genomes only at t0,200,400,1000. Exact original within-history focal full-W gradient switch times would require source-identical RNG replay with instrumentation, comparing to original trajectory receipts. Do not calculate true selection-switch time by imputing all adult genotypes from aggregate means.

**B: targeted independent temporal manipulation.** At identical diploid founders and ecological conditions, vary **abrupt versus gradual visitor functional mismatch**, ideally with explicit cumulative pollen-supply comparators and controlled current census, then test selection-sign onset and actual inherited order separately. This would be a **new** experiment, with its frozen design and independent visitor histories, not a post-outcome extension of the current 64 histories.

**C: independently factorial mating-system biology.** Hold timing and direct cost separately fixed instead of comparing two historical packages confounded in timing/cost. We have now implemented a fixed-source 2×2 assay, not yet an independent longitudinal evolution test.

## Reproducibility

- `scripts/audit_chapter2_order_selection_mismatch_census_20261011.py`: original `reproduce_kb` and full F/P/S, complete 60-source 3×2×2×5 grid, two derivative widths and results by factorial.
- `tests/test_chapter2_order_selection_mismatch_census_20261011.py`: finite-source conservation, independent numeric anchors, density-dependent investment sign and cost/timing factorial, negative and positive source controls.
- Original #452 functional matching profiles, main-based #468–#469 long-run source contrasts, main historical #411 evolution, #418 assigned order and archived #472 paired order estimands.
- No core biology modification, independent natural history, natural pollinator losses, or manuscript-headline change.

**Evidence rank remains post-discovery mathematical mechanism.** The claim that different dates of selection-onset explain actual spontaneous A/I precedence is NOT admitted until the genuine selection-gradient history test is performed and validated.


## Follow-up: individuals need not share the same density response

The original N8/N24/N48 grid above used **clones**, so every focal individual had the same floral phenotype and therefore the same derivative. This hides real within-population heterogeneity in the original Model3 reproduction operator. Population census `N` is a group property, but local genetic returns `W_i` are **individual-specific**.

The follow-up extends the same original `reproduce_kb` calculation to eight **distinct diploid homozygous floral phenotypes**, preserving equal type frequencies across N=8,24,48 by repeating each type respectively 1,3,6 times. Pollinator function count=4, source pollen background B48 and **capacity K48 remain constant**. Only current census and a disclosed flower genotype fixture vary:

- `clonal`: all individuals matching=.20, investment=.35, assurance=.35.
- `investment_heterogeneity`: matching=.20 and assurance=.35 in everyone; investment spans .20–.50 among 8 types.
- `matching_heterogeneity`: investment=.35 and assurance=.35; matching spans .05–.55.
- `matching_and_investment_heterogeneity`: both investment and matching vary over the original indicated intervals.

There are **192 post-discovery source combinations** = 4 genotype compositions × (delayed/prior selfing × direct assurance cost0/.5) × 4 visitor optimum mismatch states (0/.25/.5/1) × 3 current censuses. The 192 cells are **not independent natural ecological observations**.

### Source-mathematics diagnostic: delayed selfing, zero direct assurance cost

At 50% mismatched functional visitor optima, the *eight genotype types* have the following signs for the **focal, full male+female+self log fitness investment derivative β_I**:

| Flower genotype fixture | Current N | Types with β_I positive | Types with β_I negative | Individual β_I range |
|---|---:|---:|---:|---|
| Clonal | 24 | 0/8 | 8/8 | all −0.2656 |
| Matching heterogeneity | 8 | 0/8 | 8/8 | −0.3456 to −0.1711 |
| Matching heterogeneity | **24** | **4/8** | **4/8** | **−0.3379 to +0.1569** |
| Matching heterogeneity | **48** | **5/8** | **3/8** | **−0.3285 to +0.4407** |
| Matching + investment heterogeneity | 24 | 3/8 | 4/8 (1 near-zero) | −0.1944 to +0.1144 |

**Crucially, N=24 does NOT uniquely determine the local investment-selection sign.** Under the same N, visitor assemblage, population census and assurance phenotype, different floral matching genotypes can face selection in *opposite directions*. One must not replace `β_i` with a single monomorphic resident gradient and assume all adult plants select alike.

At N=8 with matching held identical at .20, varying **investment alone** already yields 2/8 types with β_I positive, 5/8 negative and 1/8 near-zero under the original matched four visitors, while the monomorphic N8 reference is uniformly negative. Thus individual trait variation also matters when floral visitor matching itself is fixed.

These values are from an independent direct-array implementation of the original source equations and are retained as **original-code CI regression targets**, not field fitness measurements or independently confirmed ecological tests.

### Scientific meaning for the order-centered hypothesis

An apparent temporal order A-before-I may depend on which genotypes already exist in the founder population, what fraction experiences positive/negative focal selection, how the **complete full paternal-inclusive W_i** covaries with inherited trait alleles, and how drift/segregation changes genotype frequencies through time. Small N is not synonymous with uniformly negative selection in a **heterogeneous** source community.

The direct test linking Q1 to Q3 is the expected inherited trait covariance (source PR #470), followed by actual time-resolved diploid histories. The historical 51/64 A-first crossing cannot be explained solely by the *clonal* β sign at N8/24/48. The field analogue needs individual plant floral traits and parentage/fitness data, not only island-wide species richness or mean census size.

Implementation: `scripts/audit_chapter2_order_individual_density_heterogeneity_20261011.py`, regression tests `tests/test_chapter2_order_individual_density_heterogeneity_20261011.py`.

