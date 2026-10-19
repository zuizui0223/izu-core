# Two-origin technical v3 — source-matched conditional establishment probabilities

**2026-10-19; TECHNICAL FIXTURE ONLY, NOT SCIENTIFIC OR CONFIRMATORY EVIDENCE.** These 12 source×synthetic-island probabilities were read directly from the successful [GitHub Actions technical gate](https://github.com/zuizui0223/izu-core/actions/runs/39269659188) (job `118118291104`, source code at commit `1ef4379d1f2ba53d658c84a9c08490c6ea987024`). Values shown are rounded to four decimal probability units as printed by the original job. The six source genotypes and arrival RNG namespace were retained from technical v2; new v3 early filters are **not independent source/genotype replications**. No new publication outcome or confidence interval.

## Measured technical construction

- Six artificial candidate source genotypes (two starting individuals each), with three A-hints (.25/.5/.75) and two I-hints (.35/.65), each having its own independent random allele draw around the hint.
- One native reproduction update defines initial establishment; adult carryover=0, mutation=0, immigration=0, island carrying capacity=12. Resource/visitor cases are `no_visitors_harsh` (B4.5; no visitors) and `visitors_milder` (B8; 4 visitors).
- Source/arrival/genetic founding states are matched across early expression interventions. Actual arrival is a **separate 0.8 Bernoulli draw** per lineage/island/reset; reported values are conditional on a candidate *having arrived*.
- Initial establishment is Poisson with expected viable recruit count `lambda` calculated by the unchanged Model3 maternal/paternal/self ledger, hence **p(establish | arrived, source, island, filter) = 1-exp(-lambda)**. This holds for all candidates, including ones that did not actually arrive.
- Early filter modes: **native** (actual source A/I/M), **neutral_A** (set only expressed A=.5), **neutral_I** (only I=.5), **neutral_A_I** (both A and I=.5), and **trait_neutral** (A/I/M all=.5). In all modes the offspring inherit **the original source genotype**, not the expression-clamped values.

## Direct source-bound numerical readout

| Technical island | Source ID | A0 | I0 | P native | P neutral_A | P neutral_I | P neutral_A_I | P all-neutral |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| no_visitors_harsh | 0 | 0.226 | 0.350 | 60.61% | 84.54% | 58.31% | 82.66% | 82.66% |
| no_visitors_harsh | 1 | 0.263 | 0.648 | 60.35% | 79.99% | 63.47% | 82.66% | 82.66% |
| no_visitors_harsh | 2 | 0.512 | 0.349 | 85.01% | 84.54% | 83.17% | 82.66% | 82.66% |
| no_visitors_harsh | 3 | 0.497 | 0.667 | 79.43% | 79.59% | 82.48% | 82.66% | 82.66% |
| no_visitors_harsh | 4 | 0.784 | 0.306 | 91.55% | 84.96% | 89.83% | 82.66% | 82.66% |
| no_visitors_harsh | 5 | 0.741 | 0.626 | 87.53% | 80.45% | 89.31% | 82.66% | 82.66% |
| visitors_milder | 0 | 0.226 | 0.350 | 87.89% | 97.45% | 89.76% | 97.45% | 97.45% |
| visitors_milder | 1 | 0.263 | 0.648 | 92.33% | 97.24% | 91.57% | 97.41% | 97.45% |
| visitors_milder | 2 | 0.512 | 0.349 | 97.54% | 97.41% | 97.51% | 97.40% | 97.45% |
| visitors_milder | 3 | 0.497 | 0.667 | 97.19% | 97.23% | 97.39% | 97.43% | 97.45% |
| visitors_milder | 4 | 0.784 | 0.306 | 98.98% | 97.43% | 98.82% | 97.44% | 97.45% |
| visitors_milder | 5 | 0.741 | 0.626 | 98.52% | 97.29% | 98.73% | 97.43% | 97.45% |

**Interpretation within this exact engineering fixture only:**
- Under zero visitors and B4.5, source lineages with A0 ≈ .23–.26 have establishment probabilities **60.35–60.61%**, while sources with A0 ≈ .74–.78 have **87.53–91.55%**; other inherited traits differ among these same source draws and so unadjusted across-lineage contrasts are not pure A effects.
- The **paired A-only expression intervention** changes the initial p at fixed founding genotype and original I/M. For source 0 with no visitors, native p=.6061 versus neutral_A p=.8454, difference **−23.93 percentage points** (rounded); for source 4 native p=.9155 versus neutral_A p=.8496, difference **+6.59 points**. These are **policy contrasts** against a fixed reference expression .5, not the causal effect of species-level self-compatibility.
- The **paired I-only expression intervention** likewise changes native establishment in both directions depending on source state, without changing A/M or the inherited genotype. The table is the correct data for checking whether its effect is smaller/larger than the A clamp in a particular source; it does **not** establish a general trait-ranking from 6 exposed genotypes.
- After fixing all M/I/A expressions, conditional p is identical among all six founders at each synthetic island (**82.66%** at no-visitors B4.5, **97.45%** with visitors B8), an expected negative-control property of this deliberately standardized reproduction kernel.
- Because actual arrival chance is .8 independent of source, the *candidate-to-establishment* probability in this fixture is `0.8 × p(establish|arrived)` for each source and mode. Even if p is high, individual lineage establishment remains stochastic. **A trait-state gradient in establishment probability is not near-certain lineage fate prediction**.

## Descriptive source → establishment → persistence → within-lineage accounting (technical only)

The completed [second v3 technical job](https://github.com/zuizui0223/izu-core/actions/runs/39271024143) (job `118123058991`, code SHA `a395df76d2496fe75ccc43a1f8358e0d07cb09b6`) independently prints **20 technical group summaries**: two artificial islands × two resets × five early filters, all under the *same later native A/I phenotype policy*. Four unmanipulated-early-filter examples are shown below; each includes the **same six original source genotypes** before the stochastic arrival event.

| Technical island | Reset | Candidates | Arrived | Established | Present at T | A: arrival+establishment+persistence filtering | A: within survivors' changes | I: filtering | I: within survivors' changes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| no_visitors_harsh | 0 | 6 | 4 | 4 | 2 | +0.1151 | +0.0537 | +0.1555 | -0.0191 |
| no_visitors_harsh | 1 | 6 | 5 | 4 | 1 | +0.2799 | -0.0218 | -0.1851 | +0.0205 |
| visitors_milder | 0 | 6 | 6 | 6 | 6 | +0.0000 | +0.0064 | +0.0000 | -0.0006 |
| visitors_milder | 1 | 6 | 3 | 3 | 1 | +0.2369 | -0.0041 | +0.1349 | +0.0046 |

These values are **species-weighted changes in model trait units**, computed by the exact conditional telescoping identity in `stage_accounting`. A positive filtering contribution means the **surviving pool's original source trait mean** exceeds that of the complete six-candidate source pool. It is **not** a causal main effect of selection, and it does not mean the lineage's allele was already fixed on a real mainland. The within-survivor term includes changes during the one initial establishment update as well as later finite inheritance; it is not synonymous with deterministic adaptive evolution.

**What the two technical stochastic resets expose:** in the no-visitor artificial island, the original A-filtering contribution is positive in both resets (+0.1151, +0.2799) while I-filtering changes sign (+0.1555 vs −0.1851), but two resets of the SAME six genotypes cannot establish which trait is intrinsically more stochastic or which function explains global island floras. In the visitor-present artificial island, one reset retained all six sources (both filtering terms exactly zero), whereas the second retained one of the three arrivals and had nonzero positive filtering contributions for both traits. **Arrival and finite lineage survival remain integral sources of variability.** Other early A/I-expression modes cause distinct cohort fates; all source/census denominators are preserved in the original technical gate logs.

**Provenance/limits:** This table is not a new independent biological confirmation, is not prospectively registered, has no uncertainty interval, and is neither six independent natural species nor multiple realized island communities. No interspecific competition, natural-colonization event, calibrated source self-compatibility score or measured floral phenotype enters the fixture. **These numbers cannot validate the proposed "A imported; I evolved" origin split**; they show that the code correctly records the stage-specific quantities that a *new independently designed study* would need.

## Analytical sanity check of the native no-visitor founding kernel (NOT a discovery of a new island law)

At the single founding reproductive update with **no visitors**, delayed autonomous selfing, zero adult carryover, zero immigration and no mutation, the native [Model3 reproduction ledger](../scripts/model3_island/reproduction.py) yields no outcross births. For source adults \(j=1,\dots,n\) with expressed autonomous assurance \(A_j\) and floral investment \(I_j\), the **exact conditional expected number of viable selfed recruits** is

\[
\Lambda=B(1-\delta)\sum_{j=1}^n A_j\exp(-c_I I_j^2-c_A A_j^2),
\qquad P(\text{establish}\mid\text{arrived})=1-\exp(-\Lambda).
\]

For the narrower homogeneous-source illustration, \(\Lambda=nB(1-\delta)A\exp(-c_I I^2-c_A A^2)\). With the **technical** cost settings \(c_I=c_A=0.5\), its log sensitivities are

\[
\frac{\partial\log\Lambda}{\partial A}=\frac{1}{A}-A\geq0\quad(0<A\leq1),\qquad
\frac{\partial\log\Lambda}{\partial I}=-I\leq0\quad(I\geq0).
\]

Thus at fixed source floral investment, increasing expressed A increases expected viable offspring in this no-visitor founding model. But **I ALSO contributes to the founding filter through allocation cost**, before any post-establishment evolution. The proposed absolute statement “only A is selected, I only evolves” is therefore false even in this basic Model3 regime. With visitors, I additionally affects maternal and paternal pollen transfer, so its founding effect can change with ecological context. Different assurance costs, mating timing, adult survival, propagule counts or source genetic distributions can change the formulas and results; the generality must be independently tested. A positive derivative of a conditional establishment *probability* does NOT make the discrete fate of an individual lineage certain. The separate arrival lottery and stochastic Poisson recruitment still apply.

## Tests and biological limitations

The associated v3 [implementation](../scripts/chapter2_two_origins_technical_20261019.py), [technical tests](../tests/test_chapter2_two_origins_technical_20261019.py) and [source control and audit design](CHAPTER2_TWO_ORIGINS_ENGINEERING_GATE_20261019.md) were exercised through the successful Actions technical gate. Full fixture allocates **6 lineages × 2 technical islands × 2 arrival/demographic resets × 5 early establishment modes × 4 post-establishment expression policies = 480 path records**, with only 24 distinct source×island×reset candidate events; this table summarizes 12 source×island probability functions rather than 480 independent island taxa. The initial-probability table uses no outcome-selected survivor restriction. Subsequent demographic and genotype results do not identify a natural island-assembly mechanism.

This fixture omits interspecific competition, separate species-level seed dispersal heterogeneity, immigrant origins, source-population empirical alleles, functional self-compatibility, flower-colour traits, replicated held-out lineage/island prediction and any natural colonization history. Therefore neither “A is imported and selected” nor “I is created on islands” is confirmed by this output. The next independent scientific design must be prospective, with new source genotypes/islands, actual candidate→arrival→establishment→persistence denominators, source-level held-out proper scores, and controls for founder, ecology and phylogeny.
