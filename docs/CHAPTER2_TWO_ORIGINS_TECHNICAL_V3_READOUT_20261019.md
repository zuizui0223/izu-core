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

## Tests and biological limitations

The associated v3 [implementation](../scripts/chapter2_two_origins_technical_20261019.py), [technical tests](../tests/test_chapter2_two_origins_technical_20261019.py) and [source control and audit design](CHAPTER2_TWO_ORIGINS_ENGINEERING_GATE_20261019.md) were exercised through the successful Actions technical gate. Full fixture allocates **6 lineages × 2 technical islands × 2 arrival/demographic resets × 5 early establishment modes × 4 post-establishment expression policies = 480 path records**, with only 24 distinct source×island×reset candidate events; this table summarizes 12 source×island probability functions rather than 480 independent island taxa. The initial-probability table uses no outcome-selected survivor restriction. Subsequent demographic and genotype results do not identify a natural island-assembly mechanism.

This fixture omits interspecific competition, separate species-level seed dispersal heterogeneity, immigrant origins, source-population empirical alleles, functional self-compatibility, flower-colour traits, replicated held-out lineage/island prediction and any natural colonization history. Therefore neither “A is imported and selected” nor “I is created on islands” is confirmed by this output. The next independent scientific design must be prospective, with new source genotypes/islands, actual candidate→arrival→establishment→persistence denominators, source-level held-out proper scores, and controls for founder, ecology and phylogeny.
