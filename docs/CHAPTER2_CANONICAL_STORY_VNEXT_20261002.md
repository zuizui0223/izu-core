# Chapter 2 canonical story vNext — where syndrome repeatability is retained and lost

**Date:** 2026-10-02
**Status:** established vNext scientific story; active Oikos submission remains unchanged
**Manuscript:** docs/CHAPTER2_MANUSCRIPT_VNEXT_SYNDROME_20261002.md
**Establishment audit:** docs/CHAPTER2_VNEXT_ESTABLISHMENT_AUDIT_20261002.md

## One-sentence claim

> **A recurrent pollination problem can yield recurrent functional responses without
> a recurrent detailed floral phenotype because repeatability can persist in the
> coarse mean response while being redirected or lost by state-dependent selection,
> reproductive context, genetic accessibility and finite-population realization.**

This is deliberately stronger than saying that Model 3 contains separable modules.
The scientific object is **repeatability across stages**: where a repeated
direction survives, where it becomes conditional, and where it disappears.

## Chapter 1 → Chapter 2

### Chapter 1 — what recurs in nature?

isolation
→ stronger pollen limitation
→ recurrent reproductive assurance / accessibility
→ detailed pollinator-facing phenotype is less repeatable

Chapter 1 establishes the empirical asymmetry between functional repeatability and
detailed phenotypic repeatability.

### Chapter 2 — where is repeatability lost?

pollinator loss / replacement
→ visitor amount + functional composition
→ ecological selection
→ reproductive context / persistence
→ standing variation + new mutation
→ finite history / recruitment / extinction / connectivity
→ realized phenotype

The same perturbation is carried through these stages. The question is not whether
the stages can be named separately, but whether a repeated response direction
survives each transition.

## Established results

### 1. Functional matching can break repeatability at the selection stage

Controlled visitor compositions can favour opposite investment directions
depending on starting access state. Non-uniformity therefore need not wait for
demographic stochasticity.

### 2. Functional replacement redirects response at fixed visitor amount

At identical visitor count, left4 versus right4 changes selection and inherited
response away from the symmetric starting state.

The exact ±2.377 fixed-gradient contrasts and zero at access 0.5 arise from the
mirror-symmetric design. They establish operator dependence, not natural thresholds.

### 3. Assurance-by-cost reduction is conditional, not a headline route

The negative assurance-by-cost region is non-isolated, but its activity threshold
moves strongly with inbreeding depression and its inherited sign does not survive
the declared annual/perennial robustness envelope.

**Status:** retain as a model-conditional SI mechanism, not a general explanation
of selfing-syndrome floral reduction.

### 4. The coarse deterministic isolation direction survives depression sensitivity

The natural near–far deterministic bridge was prospectively rerun at inbreeding
depression 0.25, 0.50 and 0.75.

| depression | mean far−near effect | start 0.3 | start 0.5 | start 0.7 |
|---|---:|---:|---:|---:|
| 0.25 | **−0.3506** | −0.3789 | −0.3841 | −0.2887 |
| 0.50 | **−0.4510** | −0.4523 | −0.4710 | −0.4297 |
| 0.75 | **−0.4142** | −0.4248 | −0.4487 | −0.3692 |

Thus the **coarse mean backbone remains negative** across the tested depression
envelope.

### 5. History-level deterministic repeatability does not survive high depression

The stronger claim of uniform direction across all 128 visitor histories fails at
depression 0.75:

- depression 0.25: 128 negative-only / 0 mixed / 0 positive-only;
- depression 0.50: 128 / 0 / 0;
- depression 0.75: **116 / 11 / 1**.

The single positive-only history is seed 74019; 11 additional histories contain
both negative and positive effects across the three starting investment states.

**Meaning:** reproductive context can erase history-level repeatability even while
the overall deterministic mean retains the same direction. This occurs before
finite demographic stochasticity.

### 6. Genetic accessibility filters a shared selective response

Reducing standing variation on one trait axis selectively suppresses response on
that axis while the ecological operator is unchanged.

Under mutation input normalized to 1% of initial additive variance per generation,
high-standing populations still respond more at years 400 and 800, but the gap
narrows from a response ratio of 2.56 to 1.49 and most mutation cells are not near
variance plateau.

**Status:** standing variation leads over the tested finite horizon; no equilibrium
or universal standing-variation > mutation hierarchy is claimed.

### 7. Finite realization further erodes repeatability

The original 24,576-case bridge remains the realization layer:

- annual visitor-count matching reverses the mean isolation effect;
- visitor-history pooling changes descriptive branching;
- increasing plant capacity moves finite outcomes toward deterministic density;
- chronology, connectivity and reproductive assurance alter persistence and
  inherited endpoints.

The finite ABM therefore adds another filter after deterministic ecological and
genetic differences have already appeared.

## What the vNext adds beyond prior syndrome debate

The vNext does **not** claim that syndrome criticism is new.

Prior work already debates:

- functional pollinator groups and differential selection (Fenster et al. 2004);
- mismatch between many traditional syndrome categories and observed pollinators
  (Ollerton et al. 2009);
- strong syndrome prediction when effective pollinators are used
  (Rosas-Guerrero et al. 2014);
- system-specific constraints, pollinator-mediated selection and trade-offs
  (Dellinger 2020).

The new target is:

> **use preregistered interventions in one explicit eco-evolutionary model to
> locate where repeatability of a syndrome component is retained, redirected,
> attenuated or lost.**

The contribution is the **pattern of transmission across stages**, not the mere
existence of the stages.

## Natural-data boundary

Natural systems provide:

1. layer-specific biological plausibility;
2. adversarial / falsification context.

They are not quantitatively calibrated to Model 3 cells. The formal archive still
contains 0/25 complete same-unit A → B → C contracts. Quantitative transfer
therefore requires future longitudinal data linking visitor transition, inherited
response and demographic realization in the same populations.

This is a limitation, not an unfinished vNext analysis.

## Trait-language firewall

- access = abstract functional matching, not literal tube length;
- investment = abstract pollinator-facing investment, not literal colour;
- assurance = reproductive route, not realized selfing rate.

Do not claim “colour is easy and morphology is hard.”

The testable biological prediction is that trait modules can differ in standing
variation, mutational target size, effect-size distribution and developmental /
pleiotropic coupling, so the same ecological selection need not move them
synchronously.

## Negative-result and qualification firewall

Retain all three:

1. mutation/pleiotropy sustained-crossing experiment failed;
2. Route A failed its robustness rule;
3. uniform deterministic near–far direction failed at depression 0.75 even though
   the mean direction remained negative.

Do not retune any of these into positive results.

## vNext paper spine

1. Prior syndrome debate motivates a transmission problem: where is repeatability
   lost?
2. Functional matching can create state-dependent selection.
3. Functional replacement can redirect response at fixed visitor amount.
4. Reproductive assurance robustly affects persistence; assurance-by-cost adaptive
   reduction is conditional.
5. Natural near–far isolation retains a negative **mean** deterministic response
   across depression 0.25–0.75.
6. High inbreeding depression breaks deterministic history-level uniformity before
   demographic stochasticity.
7. Genetic accessibility filters how much selected response is reachable through
   finite time.
8. Visitor history, plant finiteness, chronology and connectivity further filter
   realized inherited outcomes.
9. Natural islands confront these layers qualitatively but are not quantitatively
   fitted to synthetic cells.

## Submission state

Current Oikos package: **unchanged and locked**.

vNext: **scientifically established including the final depression-propagation
check, but not promoted to the active submission surface**.

Promotion remains a deliberate package reopening: manuscript + figures + SI +
canonical lock + submission manifest must move together.
