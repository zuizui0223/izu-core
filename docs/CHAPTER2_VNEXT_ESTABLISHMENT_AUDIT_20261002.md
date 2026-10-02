# Chapter 2 vNext establishment audit — 2026-10-02

**Branch:** `research/ch2-vnext-establishment-20261002`  
**Parent main:** `941b6fcb594cb465af298f8f43756e5964ce26a8`  
**Purpose:** close the five establishment criteria before promoting the vNext syndrome framing.

## Five criteria

| criterion | current state |
|---|---|
| 1. one stable central claim | pending final re-audit after A–D |
| 2. headline numbers pass robustness tests | in execution: Route A surface + mutation-input calibration |
| 3. novelty checked against prior literature | closed |
| 4. preregistered successes and failures retained | closed |
| 5. remaining items can be written as limitations rather than open work | closed in principle for natural transfer; pending A/B outcome wording |

## A. Route A robustness — prospective falsification contract

Frozen design:

`data/design/chapter2_route_A_robustness_surface_20261002.json`

The original negative gradient occurred at one focal combination. The robustness
test therefore asks whether the negative selection route occupies a non-isolated
region rather than merely reproducing that cell.

The fixed-state surface crosses:

- visitor activity: 0.025–0.4;
- assurance: 0.25, 0.5, 0.75;
- investment cost: 0.25, 0.5, 0.75;
- inbreeding depression: 0.25, 0.5, 0.75.

Inherited propagation is separately tested in:

- annual life history;
- adult survival 0.75 with the same annual reproductive budget;
- adult survival 0.75 with annual ovule/pollen budgets scaled to 0.25 of the annual treatment.

**Drop rule:** Route A remains a headline model mechanism only if the negative
surface is non-isolated, remains contiguous across all three depression levels,
and the activity-0.05 inherited response remains negative in both annual and both
perennial sensitivity treatments. Otherwise it is moved to a model-conditional
possibility / Supporting Information result.

## B. Genetic-filter calibration — prospective ranking contract

Frozen design:

`data/design/chapter2_mutation_input_calibration_sensitivity_20261002.json`

Literal mutational heritability (V_M/V_E) cannot be calibrated because Model 3
has no environmental variance (V_E). We therefore use an empirically anchored
within-model ratio (V_M/V_{G,0}).

Houle, Morikawa & Lynch (1996) report that (V_G/V_M) averages on the order of
100 generations for morphological traits, motivating (V_M/V_{G,0}=0.01) per
generation as the central sensitivity rather than a natural parameter estimate.
The experiment also includes 0.001 and 0.03.

Reference:
Houle D, Morikawa B, Lynch M. 1996. Comparing mutational variabilities.
*Genetics* 143:1467–1483. DOI: 10.1093/genetics/143.3.1467.

A later meta-analysis found mutational-heritability estimates spanning roughly
(2.5\times10^{-5}) to (1.02\times10^{-2}), with plant estimates tending lower,
which reinforces the use of a broad sensitivity rather than a single calibrated
value.

Reference:
Mackay et al. 2022. Causes of variability in estimates of mutational variance
from mutation accumulation experiments. *Genetics* 221:iyac060.
DOI: 10.1093/genetics/iyac060.

The simulation follows the investment allelic additive-variance proxy through
800 years and reports both year 400 and year 800. The central comparison is:

- high standing variation, no mutation;
- low standing variation, (V_M/V_{G,0}=0.01).

**Drop rule:** if the low-standing central mutation input exceeds the high-standing
reference at year 400, remove the claim that standing variation dominates. Year
800 and the variance time series determine whether any retained ranking is only a
finite-horizon statement.

## C. Novelty framing — closed

The phrase **“syndromes are outcomes, not mechanisms” is not itself treated as a
novel claim.**

The relevant prior debate already establishes that syndrome categories are
descriptive hypotheses whose correspondence to actual flowers and pollinators
must be tested.

- Fenster et al. (2004) defend pollination syndromes as useful for understanding
  floral diversification through functional pollinator groups, while explicitly
  identifying unresolved questions about the selective factors behind shifts,
  independent versus combined trait selection, and historical effects.
  DOI: 10.1146/annurev.ecolsys.34.011802.132347.
- Ollerton et al. (2009) show that traditional discrete syndromes poorly capture
  many real floral phenotypes and frequently fail to predict the most common
  pollinator, and recommend directly linking flower/pollinator traits to visitation
  and pollen transfer. DOI: 10.1093/aob/mcp031.
- Rosas-Guerrero et al. (2014) subsequently show, using effective rather than merely
  frequent pollinators, substantial quantitative support for syndrome predictions,
  emphasizing that the syndrome debate is not a simple rejection of convergence.
  DOI: 10.1111/ele.12224.
- Dellinger (2020) synthesizes this debate and explicitly calls for analyses of the
  interplay among system-specific constraints, pollinator-mediated selection and
  adaptive trade-offs. DOI: 10.1111/nph.16793.

Therefore the vNext novelty is narrower:

> **the same explicit eco-evolutionary model is intervened on stage by stage to
> separate ecological return, reproductive substitution, functional rematching,
> genetic accessibility and finite realization, and to show where repeatability of
> a syndrome component can be lost.**

## D. Natural-island connection — scope decision closed

Quantitative transfer of Model 3 effect sizes to the source-audited island systems
is **out of scope for the vNext establishment claim**.

Reason:

- the current formal evidence audit has 0/25 complete same-unit A -> B -> C
  contracts;
- the natural systems are heterogeneous in response scale, exposure and
  independent unit;
- broad island pollination studies usually measure breeding systems, visitor
  composition, network structure or reproductive consequences, not inherited
  longitudinal trait change under the same measured transition;
- assigning real systems to synthetic Model 3 cells would therefore create a
  calibration claim that the data do not support.

Natural evidence retains two valid roles:

1. **layer-specific biological plausibility** — the required processes occur in
   real island systems;
2. **falsification/adversarial context** — natural systems include buffering,
   branching and counterdirectional responses rather than one universal pathway.

This is now a limitation, not an unfinished task:

> Quantitative natural transfer awaits same-population longitudinal data linking
> visitor transition, inherited response and demographic realization.

## E. Stability test

After A and B complete, re-read the vNext one-sentence claim without changing the
decision rules.

Current candidate:

> Island, selfing and pollination syndromes are emergent phenotypes produced by
> separable ecological, reproductive, genetic and demographic filters; a recurrent
> pollination problem can therefore generate recurrent functional insurance without
> one recurrent detailed floral phenotype.

Promotion criterion:

- if A fails, the one-sentence claim must remain valid after removing
  assurance-by-cost as a headline route;
- if B reverses, it must remain valid after removing any ranking of standing
  variation versus mutation;
- the sentence is considered stable only if neither failed sub-result requires
  rewriting the general stage-decomposition claim.

