# Chapter 2 canonical story vNext — syndrome as an emergent outcome

**Date:** 2026-10-02  
**Status:** vNext candidate; active Oikos submission remains unchanged  
**Manuscript:** `docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md`

## One-sentence claim

> **Island, selfing and pollination syndromes are emergent phenotypes produced by separable ecological, reproductive, genetic and demographic filters; a recurrent pollination problem can therefore generate recurrent functional insurance without one recurrent detailed floral phenotype.**

## Dissertation handoff

### Chapter 1 — what recurs?

Chapter 1 resolves the empirical syndrome:

```text
isolation
  -> stronger pollen limitation
  -> recurrent reproductive assurance / accessibility
  -> but detailed pollinator-facing phenotype is less repeatable
```

The unresolved question is not whether island plants change. It is why functional
repeatability is stronger than phenotypic repeatability.

### Chapter 2 — why can that happen?

```text
pollinator loss / replacement
        ↓
visitor amount + functional composition
        ↓
pollen transfer / outcross opportunity
        ↓
reproductive assurance + cost / functional rematching
        ↓
selection on pollinator-facing traits
        ↓
standing genetic variation
        ↓
new mutation / genetic coupling
        ↓
finite recruitment + extinction + history + connectivity
        ↓
realized syndrome components
```

Each arrow can preserve, redirect, attenuate or terminate the response.

## Five causal statements

### 1. Functional matching creates branch capacity before demography

The existing fixed-state assay shows that the same visitor composition can favour
opposite investment directions depending on starting access state. Under left4,
the investment gradient is +1.5048 at access 0.20 and -0.8720 at 0.80; right4
reverses those signs.

**Meaning:** non-uniformity can enter at the ecological selection layer.

### 2. Pollinator scarcity does not automatically imply adaptive floral reduction

Under visitor activity 0.05:

- no assurance + cost 0.5 -> gradient +0.602; finite population does not persist;
- assurance 0.5 + no investment cost -> gradient +0.611;
- assurance 0.5 + cost 0.5 -> gradient -0.393;
- assurance 0.5 + cost 0.5 with activity restored to 0.4 -> gradient +1.681.

**Meaning:** relaxed positive selection and directional adaptive reduction are
different. In this model, low pollinator service produces lower investment only
when reproductive assurance preserves an alternative reproductive route and a
continuing investment cost remains.

### 3. Pollinator replacement is a distinct route from pollinator scarcity

At the same visitor count, left4 versus right4 changes the fixed selection
contrast by +2.377 at starting access 0.2 and -2.377 at 0.8, with deterministic
inherited contrasts of +0.189 and -0.189.

**Meaning:** changing who pollinates can redirect the floral optimum even when
visitor number is unchanged.

### 4. Shared selection does not imply shared evolution

When one trait's founder standing SD is reduced from 0.15 to 0.03 while the
ecological operator remains unchanged:

- access response is reduced by 0.1136 deterministically / 0.0961 in finite ABM;
- investment response is reduced by 0.1054 / 0.0830.

**Meaning:** genetic accessibility is a separate filter downstream of ecological
selection.

### 5. Over the tested finite horizon, standing variation dominates new mutation

The first prospectively frozen mutation/pleiotropy timing experiment failed and
remains a negative result. A later prospective decision-tree diagnostic then
separated investment standing variation, de novo mutation supply and plant
capacity:

- restore standing variation: +0.14777 absolute investment response;
- increase de novo mutation supply: +0.01389;
- capacity 48 -> 192 adds +0.00102 to mutation rescue.

**Meaning:** in this synthetic 400-year setting, pre-existing variation is the
dominant identified genetic bottleneck. New mutation contributes, but much less;
finite establishment is a smaller modifier.

## The original Model 3 bridge still matters

The vNext does not discard the 24,576-case isolation bridge.

It now occupies the **realization layer**:

- natural near/far isolation gives a negative coarse mean response;
- annual visitor-count matching reverses that mean;
- visitor-history pooling removes descriptive mixed labels;
- increasing plant capacity moves the finite result toward deterministic density;
- chronology, connectivity and assurance further alter persistence and endpoints.

The old conclusion “visitor amount sets the coarse regime while finite histories
and plant demography modify realization” therefore remains true, but it is no
longer the whole Chapter 2 story.

## What is new relative to existing theory

Do not claim that Chapter 2 invented selfing models, pollinator matching models,
pollination syndromes or island biogeography.

Existing work separately covers:

- pollen limitation / pollen discounting / selfing evolution;
- pollinator abundance and floral specialization;
- pollination-syndrome association and its limits;
- genetic architecture of syndrome transitions;
- immigration / extinction / speciation in island biogeography.

The vNext contribution is the **stage-by-stage causal integration and knockout**:

```text
ecological return
≠ reproductive substitution
≠ functional rematching
≠ genetic accessibility
≠ demographic realization
```

A syndrome is the phenotype that emerges after these filters, not one of the filters.

## Trait-language firewall

The current abstract trait axes must remain abstract.

- access is an architecture-like functional matching coordinate, not literal tube length;
- investment is a pollinator-facing signal/display investment coordinate, not literal colour;
- assurance is a reproductive route, not synonymous with realized selfing rate.

Do not claim “colour is easy and morphology is hard.”

The defensible prediction is:

> different trait modules can differ in standing variation, mutational target size,
> effect-size distribution and developmental/pleiotropic coupling, so the same
> ecological selection need not move them synchronously.

Literal colour/shape mechanisms require external trait-specific genetic evidence.

## Negative result firewall

The mutation/pleiotropy timing experiment is part of the science.

It failed because the investment axis was almost entirely censored at the
predeclared sustained 0.05 threshold over 400 years. Threshold and horizon were
not changed after inspection.

Do not rewrite this as a successful pleiotropy result.

## Natural-data boundary

The source-audited natural systems show several pieces of the architecture:

- Izu: common upstream matching decline + divergent downstream pollen/tube response;
- Ogasawara / Xisha: stronger access/effectiveness -> reproduction links;
- Hawaii / Puerto Rico-Mona: buffering;
- Dominica: counterdirectional falsifier;
- Surtsey / Tiritiri Matangi / partner-loss systems: historical realization.

The major missing natural layer remains longitudinal inherited response under a
measured visitor transition on the same population units.

## vNext paper spine

1. Syndrome labels are outcomes, not mechanisms.
2. Functional matching creates conditional selection.
3. Assurance + cost creates an adaptive-reduction route under low service.
4. Functional replacement creates a distinct rematching route.
5. Standing variation filters which selected trait response is reachable.
6. New mutation partly rescues depleted accessibility but is secondary in the
   tested horizon; the first pleiotropy timing prediction failed.
7. Visitor history, plant finiteness, chronology and connectivity filter realized
   inherited outcomes.
8. Natural islands contain these layers but do not yet close the full transition.

## Submission state

Current Oikos package: **unchanged and locked**.

vNext: **scientifically drafted and source-backed, but not promoted to the active
submission surface**.

Promotion requires a deliberate package reopening: manuscript + figures + SI +
canonical lock + submission manifest must all move together.
