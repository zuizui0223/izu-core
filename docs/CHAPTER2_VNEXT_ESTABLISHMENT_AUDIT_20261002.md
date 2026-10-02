# Chapter 2 vNext establishment audit — 2026-10-02

**Branch:** `research/ch2-vnext-establishment-20261002`  
**Parent main:** `941b6fcb594cb465af298f8f43756e5964ce26a8`  
**Purpose:** close the five establishment criteria before promoting the vNext syndrome framing.

## Final five-criterion assessment

| criterion | final state |
|---|---|
| 1. one stable central claim | **achieved** — claim survives removal of Route A and weakening of the standing-vs-mutation ranking |
| 2. headline numbers pass robustness tests | **achieved by pruning** — Route A fails and is demoted; genetic-accessibility claim survives with finite-horizon qualification |
| 3. novelty checked against prior literature | **achieved** — syndrome-as-outcome framing treated as prior context; novelty narrowed to stage decomposition/intervention |
| 4. preregistered successes and failures retained | **achieved** — Stage C failure and Route A robustness failure retained |
| 5. remaining items can be written as limitations rather than open work | **achieved** — quantitative natural transfer explicitly out of scope; mutation ranking explicitly finite-horizon |

## Stable central claim

> **A recurrent pollination problem can yield recurrent functional responses
> without a recurrent detailed floral phenotype because ecological selection,
> reproductive persistence, genetic accessibility and finite-population
> realization are separable stages.**

This sentence does not require:

- the assurance-by-cost route to be generally robust;
- standing variation to dominate mutation at equilibrium;
- quantitative transfer from synthetic cells to named islands.

That is why it remains stable after the prospective falsification tests below.

## A. Route A robustness — failed headline test

Frozen design:

`data/design/chapter2_route_A_robustness_surface_20261002.json`

Frozen result:

`data/results/chapter2_route_A_robustness_surface_20261002.json`

The fixed-state negative region was **not** an isolated single cell:

- low-activity-region negative fraction: **0.833**;
- depression 0.25: **1.000** negative;
- depression 0.50: **0.938**;
- depression 0.75: **0.563**.

However, the preregistered robustness rule failed.

At assurance 0.5 and investment cost 0.5, the estimated activity value where
the gradient changes sign shifted strongly with inbreeding depression:

- depression 0.25: activity ~**0.182**;
- depression 0.50: ~**0.096**;
- depression 0.75: ~**0.040**.

Thus the original activity 0.05 cell is negative at depression 0.25 and 0.50
but already positive at depression 0.75.

Inherited propagation also failed the declared life-history criterion. At
activity 0.05:

- annual, depression 0.25/0.50: negative;
- annual, depression 0.75: positive;
- perennial with the same annual reproductive budget: finite-ABM response was
  already positive at depression 0.50 and 0.75;
- perennial with approximately lifetime-matched annual budgets remained negative
  across all three depression levels, although occupancy was 0.75 at depression 0.75.

**Decision:** the assurance-by-cost route is **not a headline general mechanism**.
It is retained as a mathematically coherent, non-isolated but parameter- and
life-history-dependent mechanism in Supporting Information / sensitivity results.

This distinction matters: the negative gradient is a direct consequence of the
declared reproductive-return and investment-cost functions. The robustness
analysis establishes where that mechanism operates in the model; it does not turn
the mechanism into a new empirical law.

## B. Genetic-filter calibration — ranking survives, magnitude does not

Frozen design:

`data/design/chapter2_mutation_input_calibration_sensitivity_20261002.json`

Frozen result:

`data/results/chapter2_mutation_input_calibration_sensitivity_20261002.json`

Literal mutational heritability (V_M/V_E) is not calibrated because Model 3 has
no environmental variance (V_E). Instead mutation input was normalized to the
initial allelic additive-variance proxy.

The central sensitivity uses (V_M/V_{G,0}=0.01) per generation. This is anchored
to the order of magnitude implied by Houle, Morikawa & Lynch (1996), who report
(V_G/V_M) on the order of 100 generations for morphological traits.

References:

- Houle D, Morikawa B, Lynch M. 1996. *Comparing mutational variabilities*.
  Genetics 143:1467–1483. DOI: 10.1093/genetics/143.3.1467.
- Mackay et al. 2022. *Causes of variability in estimates of mutational variance
  from mutation accumulation experiments*. Genetics 221:iyac060.
  DOI: 10.1093/genetics/iyac060.

### Central-anchor result

Mean absolute investment response:

| treatment | year 400 | year 800 |
|---|---:|---:|
| high standing variation, no mutation | **0.1968** | **0.2015** |
| low standing variation, (V_M/V_{G,0}=0.01) | **0.0769** | **0.1354** |

The ranking therefore does **not** reverse at either horizon.

However, the gap narrows strongly:

- high/low ratio at year 400: **2.56**;
- high/low ratio at year 800: **1.49**.

Most mutation-input cells were not near a variance plateau between years 600 and
800. The additive-variance trajectories were strongly nonstationary.

The older mutation setting (mu=10^{-3}, sigma_m=0.04) corresponds to only
about (V_M/V_{G,0}=0.00194) in the low-standing N=48 treatment — roughly one
fifth of the new central 0.01 anchor. Therefore the earlier statement that de
novo mutation rescue was only ~9.4% of the standing-variation effect is
**design-dependent and is retired as a general effect size**.

**Decision:** retain only:

> **Standing variation leads the response over the tested 400–800 generation
> horizons under the central mutation-input sensitivity, but mutation progressively
> narrows the gap and no equilibrium hierarchy is established.**

Do not write that standing variation universally dominates new mutation.

## C. Novelty framing — closed

The phrase **“syndromes are outcomes, not mechanisms” is prior conceptual context,
not the novelty claim.**

Relevant literature:

- Fenster et al. (2004) defend pollination syndromes as useful functional-group
  hypotheses while explicitly identifying unresolved questions about selective
  factors, combined trait evolution and history.
  DOI: 10.1146/annurev.ecolsys.34.011802.132347.
- Ollerton et al. (2009) show poor correspondence of many real flowers with
  traditional discrete syndrome clusters and recommend direct analysis of
  flower/pollinator traits, visitation and pollen transfer.
  DOI: 10.1093/aob/mcp031.
- Rosas-Guerrero et al. (2014) recover strong quantitative support when effective
  pollinators are used, showing that the debate is not a simple rejection of
  pollinator-mediated convergence.
  DOI: 10.1111/ele.12224.
- Dellinger (2020) calls explicitly for analysis of system-specific evolutionary
  constraints, pollinator-mediated selection and adaptive trade-offs.
  DOI: 10.1111/nph.16793.

**Novelty retained:**

> **The same explicit eco-evolutionary model is intervened on stage by stage to
> separate ecological selection, reproductive persistence, functional rematching,
> genetic accessibility and finite realization, and to identify where repeatability
> of a syndrome component is lost.**

The paper must not present syndrome criticism itself as new.

## D. Natural-island connection — scope decision closed

Quantitative transfer of Model 3 effect sizes to the source-audited island systems
is **out of scope** for the vNext establishment claim.

Reasons:

- current formal audit: **0/25** complete same-unit A -> B -> C contracts;
- natural systems differ in response scale, exposure and independent unit;
- island pollination datasets commonly provide breeding system, visitor
  composition, network structure or reproductive consequences, but not inherited
  longitudinal trait change under the same measured transition;
- fitting those systems to synthetic Model 3 cells would imply calibration that
  the evidence does not support.

Natural evidence has two retained roles:

1. layer-specific biological plausibility;
2. falsification/adversarial context.

This is a **limitation**, not an unfinished analysis:

> Quantitative natural transfer requires future same-population longitudinal data
> linking visitor transition, inherited response and demographic realization.

## E. Stability re-audit — passed

The stronger pre-robustness story changed in two places:

1. assurance-by-cost adaptive reduction was demoted from a headline route;
2. the specific standing-variation >> mutation effect-size ratio was retired.

The central claim did **not** need to change:

> **A recurrent pollination problem can yield recurrent functional responses
> without a recurrent detailed floral phenotype because ecological selection,
> reproductive persistence, genetic accessibility and finite-population
> realization are separable stages.**

Therefore the vNext passes the stability criterion.

## Final promotion boundary

The vNext can now be promoted scientifically only with these restrictions:

- Route A appears as a conditional sensitivity / failed robustness result, not a
  general causal pillar;
- same-count left/right symmetry is described as an operator demonstration, not
  a discovered natural threshold;
- standing variation is described as leading over the tested finite horizon, not
  as universally or asymptotically dominant;
- “syndromes are outcomes” is cited as conceptual context;
- natural islands remain layer-specific confrontation, not quantitative
  calibration/validation.

Within those boundaries, all five establishment criteria are closed.
