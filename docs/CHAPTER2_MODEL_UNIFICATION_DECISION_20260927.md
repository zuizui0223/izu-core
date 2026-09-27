# Chapter 2 model unification decision — 2026-09-27

## Decision

**Model 2 is no longer required as a separate biological mechanism for the Chapter 2 core branching question, but it is not yet redundant for every original Chapter 2 control.**

Chapter 2 should use one nested eco-evolutionary Model 3 with three analytical levels:

1. **fixed-state reproductive assay** — demographic updating and inheritance off;
2. **deterministic genotype-density propagation** — the same reproduction/inheritance operator without demographic sampling;
3. **finite-population ABM** — the same operator with finite individuals, demographic sampling, extinction, ancestry and standing-variation loss.

The former Model 2 is retained as control evidence and Supporting Information for exact realized-richness matching, finite-visitor-community pooling and response-rule sensitivity until those two original controls are reproduced prospectively inside Model 3. It must not be narrated as a second biological mechanism.

## Why the decision changed

The old separation was developmental rather than biological. Model 2 was built first to show that starting state × realized community can generate response branching. Model 3 later implemented explicit pollen transfer, reproduction, selfing, offspring viability, Mendelian inheritance, density regulation, survival, connectivity and demographic history.

The remaining concern was whether Model 2 still had two unique scientific roles:

- show that branching exists **before** demographic stochasticity;
- show that **community composition**, not functional-type count alone, can create divergent responses.

The prospective Model 3 unified reduction audit was frozen before execution to test exactly those roles.

## Prospective unified reduction audit

Design: `data/design/model3_unified_reduction_audit_20260927.json`

Frozen result: `data/results/model3_unified_reduction_audit_frozen_20260927.json`

Workflow run: `36294376577` — success.

Five starting access states were crossed with fixed visitor communities. The assay compared a broad 8-type reference, three 4-type compositions, and an 8-entry duplicate of the left 4-type composition under fixed total activity.

### 1. Branching occurs before demography

The fixed-state Model 3 reproductive assay produced both positive and negative investment gradients across starting access states in **all three 4-type communities**.

| starting access | left4 gradient | right4 gradient |
|---:|---:|---:|
| 0.20 | +1.5048 | -0.8720 |
| 0.80 | -0.8720 | +1.5048 |

Therefore the core branch is already present in the Model 3 ecological/reproductive operator. It does not require drift, extinction or demographic sampling.

### 2. Fixed richness does not remove composition dependence

`left4`, `right4` and `center4` all contain four visitor functional types, yet response changes strongly with which four types are present.

Maximum fixed-state left-versus-right composition difference in the declared audit: **2.3768** in the reproductive-gradient scale.

Thus the composition result previously supplied by Model 2 can be generated directly inside Model 3.

### 3. Functional-type count alone is not the explanation in the fixed-budget control

Duplicating every `left4` type to make `leftdup8` changed the operator by only:

`1.7763568394002505e-15`

maximum absolute error across the fixed-state, density and ABM controls.

This is machine-precision equality under the declared fixed-total-activity operator. It is an operator control, not a claim that field species richness never matters.

### 4. Branching survives removal of demographic sampling

The deterministic genotype-density counterpart showed mixed positive and negative inherited investment changes across starting states in **left4, right4 and center4**.

Maximum deterministic composition effect: **0.1891** investment units.

Therefore finite demographic stochasticity is not necessary for non-uniform response.

### 5. The finite ABM retains the same simple-design branching

The finite ABM also showed mixed signs in all three fixed-richness contexts. In this deliberately simple reduction audit, deterministic-density and mean-ABM response signs agreed in **100%** of evaluable cells.

This does not imply that finite demography is unimportant. In the full 19,968-case island campaign, ABM–density sign disagreement is nonzero in nearly every trajectory family and is large in chronology, life-history, assurance and recovery conditions. The reduction audit identifies the upstream branch; the full campaign shows how finite demography can subsequently alter realized trajectories.

Across the frozen full-campaign summary, mean ABM–density sign-disagreement fractions by family are:

| family | mean sign disagreement | maximum |
|---|---:|---:|
| scaling | 0.053 | 0.195 |
| connectivity | 0.258 | 0.340 |
| transport | 0.274 | 0.445 |
| initialization | 0.293 | 0.293 |
| chronology | 0.453 | 0.945 |
| assurance | 0.468 | 1.000 |
| life history | 0.487 | 0.996 |
| recovery | 0.499 | 1.000 |

These fractions are descriptive cell-level diagnostics from the frozen synthetic campaign, not natural frequencies. They show that the deterministic distribution is a genuine mechanistic comparator rather than a trivial smoothing of the ABM.

## Correction from the original-Chapter-2 answer audit

A subsequent audit of all 3,072 stored Model 3 transport cases asked a stricter question: does the **actual isolation-driven near-versus-far visitor assembly contrast** show the same deterministic branching?

The answer is not yet yes.

For the paired far-minus-near inherited-investment effect:

- production finite ABM: mixed in `22/128` histories at epsilon 0;
- held-out finite ABM: mixed in `30/128`;
- production deterministic density: mixed in `0/128`;
- held-out deterministic density: mixed in `0/128`.

The two finite demographic repeats also disagreed in their zero-threshold branch classification in `41/128` production and `48/128` held-out histories.

This means the fixed-composition unification audit and the isolation-driven transport audit answer different questions:

```text
fixed visitor composition
    -> Model 3 can generate deterministic state-dependent branching

isolation-driven dynamic visitor assembly
    -> deterministic density is one-directional in the stored transport contrast
    -> finite ABM can show mixed realized outcomes
```

Therefore **demographic stochasticity is not a necessary condition for branching in the Model 3 operator, but it may be decisive for realized branching under some island-assembly regimes**.

Two original Chapter 2 questions remain open inside Model 3:

1. whether response branching persists after **response-blind annual realized-richness matching** of near and isolated visitor histories;
2. whether the relevant finite-community effect is specifically **finite visitor-community sampling**, independently of finite plant-population sampling.

A frozen prospective bridge design now targets these questions with matched, pooled and large-capacity arms. Until that campaign is complete, the legacy Model 2 exact-richness and synthetic-`k` results remain useful controls rather than disposable history.

## What the unified model now answers

| Chapter 2 question | Model 3 level | Current answer |
|---|---|---|
| Can one pollinator context favour opposite floral responses? | fixed-state assay | Yes; starting access state changes the sign of the reproductive gradient. |
| Is richness/count alone sufficient? | fixed-state count/composition controls | Type count alone is insufficient under the fixed-total-activity operator, but dynamic response-blind realized-richness matching inside Model 3 remains prospectively unresolved. |
| Does branching require demographic stochasticity? | fixed-composition deterministic density + isolation transport audit | Not universally: controlled compositions branch deterministically, but the stored isolation-driven density contrast is one-directional while finite ABM histories can be mixed. |
| Does finite population structure matter after branching exists? | ABM vs density | Yes; full-campaign sign disagreement and magnitude bias can be large. |
| Does current environment uniquely determine phenotype? | chronology | No; early vs late visitor loss yields different endpoints under a common final environment. |
| Why can reproductive assurance recur without one floral phenotype? | assay + assurance trajectories | Assurance changes reproductive trade-offs and can determine persistence, without imposing one floral direction. |
| Can isolation be represented by one scalar distance? | connectivity | No; seed and pollinator connectivity act through different biological routes. |
| Does recovery imply reversal to the original phenotype? | recovery | No in the declared horizons; visitor return, mutation and source immigration have different effects. |
| Is one island syndrome phenotype required? | all levels | No. A recurrent functional pressure can coexist with conditional inherited trajectories. |

## What remains useful from legacy Model 2

The following are retained, but **not as a second mechanistic model**:

- exact stepwise realized-richness matching;
- synthetic `k` community-pooling sensitivity;
- alternative heuristic response operators;
- historical S/C/I decomposition and provenance.

These answer controls that are partly historical and partly still scientifically active. They are not needed as a separate biological mechanism, but exact dynamic richness matching and finite visitor-community averaging remain the only evidence for two original Chapter 2 questions until the prospective Model 3 bridge campaign closes those gates.

## New Chapter 2 architecture

```text
Chapter 1
recurrent functional island syndrome
+ non-uniform detailed phenotype
        |
        v
Chapter 2 — one unified Model 3

A. fixed-state ecological/reproductive assay
   visitor composition × starting floral state
        -> reproductive selection branch

B. deterministic genotype distribution
   selection + inheritance
        -> expected evolutionary trajectory
   demographic sampling removed

C. finite-population ABM
   selection + inheritance + finite demography
        -> persistence/extinction
        -> standing-variation loss
        -> realized inherited trajectory

D. historical/context interventions
   assurance + chronology + connectivity + recovery + life history
        -> conditional realization
```

The core interpretation is:

> **A recurrent island functional syndrome does not require phenotypic convergence because non-uniformity already arises from functional matching before demographic stochasticity, persists under deterministic inheritance, and is further modified by finite demography and ecological history.**

## Claim ceiling

The deterministic counterpart is a **discrete genotype-density / integrodifference-style reproductive operator**, not a demonstrated continuous diffusion PDE. A true continuous-trait PDE would require an additional justified mutation/small-step limit.

None of the synthetic time, distance, extinction frequency, investment magnitude or type-count controls are calibrated natural-island estimates.
