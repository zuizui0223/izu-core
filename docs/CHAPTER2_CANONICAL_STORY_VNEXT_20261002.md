# Chapter 2 canonical story vNext — generative island-syndrome model

**Date:** 2026-10-03  
**Status:** established vNext scientific story; active Oikos submission remains unchanged  
**Manuscript:** docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md  
**Establishment audit:** docs/CHAPTER2_VNEXT_ESTABLISHMENT_AUDIT_20261002.md

## One-sentence claim

> **Island-like pollination constraints can generate a recurrent functional floral response without forcing a single detailed floral phenotype because functional matching, reproductive context, genetic accessibility, history and finite-population realization condition how that shared pressure is expressed.**

The scientific object is **generative syndrome structure**. The model is asked whether an island-like pollination problem can produce a recurrent functional response while retaining multiple detailed evolutionary outcomes. Repeatability is a diagnostic of that structure, not the primary question.

## Generative architecture

```text
island-like pollination constraint
    ↓
visitor amount + functional composition
    ↓
reproductive selection / assurance
    ↓
recurrent coarse functional regime
    ↓
genetic accessibility + history + finite demography
    ↓
non-unique detailed floral endpoint
```

No rule directly forces a plant toward an island syndrome, a selfing syndrome, a colour class or a corolla type.

## Established results

### 1. A coarse island-like response is generated

The natural near–far deterministic bridge retains a negative mean investment response across inbreeding depression 0.25, 0.50 and 0.75:

| depression | mean far−near effect |
|---|---:|
| 0.25 | **−0.3506** |
| 0.50 | **−0.4510** |
| 0.75 | **−0.4142** |

This is the recurrent coarse backbone.

### 2. Functional composition changes the detailed selective route

At identical visitor count, changing visitor functional composition redirects selection and inherited response away from the symmetric starting state. The exact ±2.377 fixed-gradient contrasts and zero at access 0.5 arise from the deliberately mirror-symmetric design and are not natural thresholds.

### 3. Reproductive assurance robustly affects persistence, not one compulsory floral endpoint

The stronger assurance-by-cost floral-reduction mechanism failed its preregistered robustness rule. Its sign boundary shifts strongly with inbreeding depression and its inherited response does not survive the declared annual/perennial envelope.

**Status:** reproductive assurance is retained as a robust persistence/insurance mechanism; assurance-by-cost floral reduction is SI-only and conditional.

### 4. Genetic accessibility changes which selected response can be realized

Reducing standing variation on one trait axis selectively suppresses response on that axis under the same ecological operator.

Under mutation input normalized to 1% of initial additive variance per generation, high-standing populations respond more over the tested 400–800-generation horizon, but the response ratio narrows from 2.56 to 1.49. No equilibrium hierarchy is claimed.

### 5. Detailed outcomes remain non-unique even when the coarse mean persists

At depression 0.75, the deterministic mean remains negative, but history-level direction is no longer uniform:

- 116/128 negative-only;
- 11/128 mixed across starting states;
- 1/128 positive-only.

Thus one recurrent mean regime does not imply one detailed trajectory.

### 6. Finite ecological and demographic realization adds another layer of diversity

The original 24,576-case bridge shows that:

- annual response-blind visitor-count matching reverses the mean isolation effect;
- pooling visitor histories changes descriptive directional heterogeneity;
- increasing plant capacity moves finite outcomes toward deterministic density;
- chronology, connectivity and reproductive assurance alter persistence and inherited endpoints.

These are distinct mechanisms, not estimates of natural branch prevalence.

## What is novel

The vNext does not claim that syndrome concepts are new or that ecological, genetic and demographic mechanisms have never been discussed separately.

The contribution is:

> **to demonstrate, within one explicit eco-evolutionary model, that an island-like pollination constraint can generate a recurrent functional syndrome-like response without generating one compulsory detailed floral phenotype.**

The repeatability analyses explain why the generated syndrome is hierarchical: recurrence can persist at the coarse functional level while detailed evolutionary realization remains contingent.

## Natural-data boundary

Natural island systems are used for biological plausibility and confrontation, not calibration. Model 3 is not quantitatively fitted to named islands, natural evolutionary rates or regional coefficient vectors. The formal source archive still contains 0/25 complete same-unit source-state → visitor transition → inherited response → demographic realization contracts.

This is a claim boundary, not an unfinished analysis.

## Trait-language firewall

- access = abstract functional matching, not literal tube length;
- investment = abstract pollinator-facing investment, not literal colour;
- assurance = reproductive route, not realized selfing rate.

Do not claim a universal colour-easy / morphology-hard genetic hierarchy.

## Retained negative results

Three negative/qualifying results remain scientifically important:

1. the mutation/pleiotropy sustained-crossing experiment failed;
2. Route A failed its robustness rule;
3. uniform deterministic near–far direction failed at depression 0.75 even though the mean direction remained negative.

These failures constrain the generative mechanism rather than defining the paper's main question.

## Quantitative Chapter 1 emulation provenance

A separate exploratory sequence attempted quantitative emulation of an external Chapter 1 coefficient vector and did not succeed. That work is **not part of the vNext scientific evidence, success criterion or submission spine** because the Chapter 2 paper is an independent generative-model study.

Repository provenance is retained at:

- docs/CHAPTER2_EMPIRICAL_EMULATION_NEGATIVE_AUDIT_20261003.md
- data/results/chapter2_empirical_emulation_negative_audit_20261003.json

Do not use those attempts as a reason to weaken or strengthen the vNext claim.

## Full clean computational reproduction

The frozen Model 3 analyses were regenerated from zero using only frozen designs, declared seeds and restored source snapshots:

- base Model 3 island campaign: **19,968 cases**;
- Chapter 2 prospective bridge: **24,576 cases**;
- total fresh cases: **44,544**.

The bridge reproduces the frozen scientific result surface with structural mismatch count 0 and maximum numeric difference 7.11 × 10^-15. The base campaign reproduces all common scientific fields with maximum numeric difference 1.11 × 10^-16 and no numeric difference above 10^-12; its raw schema differences are added audit metadata only.

Receipt:
`data/results/model3_full_clean_rerun_receipt_20261003.json`.

## vNext paper spine

1. Island-like pollination constraints pose a generative syndrome problem.
2. One explicit model generates a recurrent coarse response.
3. Functional rematching makes detailed selection state dependent.
4. Reproductive assurance preserves persistence without forcing one floral solution.
5. Genetic accessibility controls which selected changes are reachable.
6. History and finite demography make realized floral outcomes non-unique.
7. Natural island systems confront the mechanism qualitatively but are not fitted quantitatively.

## Submission state

Current Oikos package: **unchanged and locked**.

vNext: **scientifically established as a generative island-syndrome model, but not promoted to the active submission surface**.

Promotion remains a deliberate package reopening: manuscript + figures + SI + canonical lock + submission manifest must move together.
