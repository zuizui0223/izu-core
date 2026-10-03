# Chapter 2 integrated Model 3 canonical story — 2026-10-03

**Status:** scientifically integrated candidate; locked active Oikos submission remains unchanged  
**Manuscript:** `docs/CHAPTER2_MANUSCRIPT_INTEGRATED_MODEL3_SYNDROME_20261003.md`

## Central question

> **Can one explicit eco-evolutionary Model 3 generate an island-syndrome-like functional response under island-like pollination constraints without forcing a single detailed floral phenotype?**

## Central claim

> **Yes within the declared synthetic model. Island-like pollination constraints generate a recurrent coarse functional regime, while functional matching, reproductive context, genetic accessibility, history and finite-population realization make the detailed inherited floral endpoint non-unique.**

## One model, not Model 3 plus another model

The completed paper has one biological engine.

### Frozen Model 3 backbone

1. **fixed-state reproductive selection** — plant state × visitor functional composition determines reproductive return before inheritance or demographic change;
2. **conditional deterministic genotype-density propagation** — the same reproduction and Mendelian operator is propagated without demographic sampling;
3. **finite-population ABM realization** — the same operator is exposed to recruitment, survival, extinction, ancestry change and loss of standing variation;
4. **context interventions** — assurance, chronology, connectivity, founding, recovery, life history and population scaling alter realization.

The frozen base campaign contains **19,968 cases**.

### Prospective extensions of the same Model 3

Later experiments did not introduce a second response rule. They intervened on the same Model 3 to test:

- functional replacement at fixed visitor count;
- assurance × investment-cost reduction;
- inbreeding-depression robustness;
- standing genetic variation;
- mutation input over 400–800 generations;
- the original 24,576-case near–far bridge under additional robustness controls.

These extensions either strengthen, qualify or falsify routes inside the same generative model.

## Integrated result

### 1. The model generates a coarse island-like response

The deterministic far-minus-near inherited-investment mean is negative across the tested inbreeding-depression envelope:

| depression | mean effect |
|---|---:|
| 0.25 | **−0.3506** |
| 0.50 | **−0.4510** |
| 0.75 | **−0.4142** |

This is the recurrent coarse response of the conditional deterministic closure over the frozen horizon; it is **not the stochastic mean** or an identified large-population limit of the finite ABM.

### 2. Visitor function determines how the coarse pressure is expressed

At fixed visitor number, changing functional composition redirects selection and inherited response. Starting floral state therefore matters even before demographic stochasticity.

The exact mirror-symmetric ±2.377 contrast is a designed operator control, not a natural threshold.

### 3. Reproductive assurance preserves persistence but does not force one floral syndrome

Assurance robustly determines whether populations persist through severe visitor loss.

The stronger proposed assurance-by-cost floral-reduction route failed its preregistered robustness rule and is retained only as a conditional sensitivity.

### 4. Genetic accessibility determines how much of a selected response can be realized

Reducing standing variation on one trait axis selectively suppresses response on that axis under an unchanged ecological operator.

With mutation input normalized to 1% of initial additive variance per generation, the high-standing / low-standing response ratio narrows from **2.56 at year 400** to **1.49 at year 800**. Standing variation therefore leads over the tested finite horizon, but no equilibrium hierarchy is claimed.

### 5. One coarse regime does not imply one detailed trajectory

The clean repeatability comparison comes from the occupied depression-0.50 finite bridge. Its aggregate far-minus-near mean is negative, while descriptive history-level realized signs are mixed in 12/128, 8/128 and 1/128 histories at deadbands 0, 0.01 and 0.05. All 3,072 near and 3,072 far finite cases remain occupied.

The later depression-0.75 deterministic sensitivity is not used as population-level evidence. At season 200, 98.18% of far history-by-start density trajectories are below one expected individual (median mass 0.000301), and one complete finite demographic replicate has 384/384 far populations extinct by that horizon. A prospectively frozen scan across depression 0.55–0.74 found no mixed or positive deterministic history among histories whose three starts and both near/far arms all retained terminal mass >=1. Its 116 negative-only / 11 mixed / 1 positive-only labels are therefore retained only as a mathematical closure sensitivity.

### 6. Finite ecological and demographic realization further modifies the endpoint

The 24,576-case bridge shows that:

- response-blind annual visitor-count matching reverses the mean near–far effect;
- pooling visitor histories changes directional heterogeneity;
- increasing plant capacity changes finite outcomes and numerically moves the mean toward the deterministic density closure, but that movement is descriptive rather than evidence of convergence to a stochastic expectation;
- chronology and connectivity leave different inherited endpoints;
- finite sign labels are descriptive and not natural branch-prevalence estimates.

## What is new

The novelty is not that pollination syndromes, reproductive assurance, genetic constraints or finite populations exist separately.

It is:

> **one explicit Model 3 generates a recurrent island-syndrome-like aggregate response and, within the same biological engine, separates that aggregate response from heterogeneous realized finite-population trajectories while identifying ecological, genetic and demographic filters.**

The old Model 3 paper supplied the backbone. The later prospective experiments complete and stress-test that backbone; they are not a second paper-level theory.

## Claim boundary

The integrated Model 3 does **not** claim:

- quantitative calibration to named islands;
- natural evolutionary rates or extinction probabilities;
- literal identification of the investment axis with colour, flower size or nectar guides;
- one universal selfing-syndrome route;
- equilibrium dominance of standing variation over mutation;
- stable natural branch prevalence from finite simulation labels;
- reproduction of any external Chapter 1 coefficient vector as a success criterion.

Natural island systems are used for biological plausibility and confrontation only.

## Reproducibility

Both frozen production campaigns were regenerated from zero:

- base Model 3: **19,968 cases**;
- prospective bridge: **24,576 cases**;
- total: **44,544 fresh simulations**.

Common scientific fields reproduce to floating-point roundoff, with no numeric difference above 10^-12.

Receipt:
`data/results/model3_full_clean_rerun_receipt_20261003.json`.

## Submission state

The existing Oikos package remains locked and unchanged.

The integrated manuscript is the **scientifically preferred successor** to both the old active Model 3 manuscript and the separate vNext manuscript. It is not yet the active submission surface because manuscript, figures, Supporting Information, canonical lock and submission manifest must be promoted together.
