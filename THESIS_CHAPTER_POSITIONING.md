# Thesis positioning — Chapter 2

Updated: 2026-09-18

## Role in the dissertation

`izu-core` is the **Chapter 2 / mechanistic explanation of non-uniform island-syndrome response** component of the dissertation.

The current dissertation sequence is:

- `zuizui0223/island` — **Chapter 1:** what recurs globally under island isolation, and which phenotype dimensions remain context dependent;
- `izu-core` — **Chapter 2:** why a recurrent broad constraint need not generate one detailed plant response, and when the relative importance of starting state, realized community and their interaction changes;
- `zuizui0223/shimahotarubukuro` — **Chapter 3:** what multivariate phenotype is actually realized in the focal Izu lineage.

The detailed cross-chapter bridge is fixed in [`docs/CHAPTER1_CHAPTER2_ISLAND_SYNDROME_BRIDGE_20260918.md`](docs/CHAPTER1_CHAPTER2_ISLAND_SYNDROME_BRIDGE_20260918.md).

## Chapter 1 handoff

Chapter 1 v13 now establishes a **recurrent but non-uniform floral island syndrome**.

Two partially separable phenotype modules form the recurrent functional core across all four predeclared geographic replication strata:

1. reproductive assurance;
2. floral accessibility/generalization.

Independent GloPL data also show increasing experimental pollen limitation with geographic isolation. In contrast, raw flower colour and colour–architecture coupling form a pollinator-facing display module whose detailed organization differs among ecological contexts.

The Chapter 1 handoff is therefore:

> **A common broad functional response recurs globally, but detailed pollinator-facing phenotype organization is not identical. Why can the same broad ecological constraint generate different response trajectories?**

## Canonical Chapter 2 question

> **Why need not a common island-like reorganization of pollinator interactions produce one detailed post-establishment plant response?**

The current answer is a **conditional response geometry**:

```text
broad pollinator-interaction reorganization
        ↓
coarse response regime
        ×
plant starting functional state
        ×
realized pollinator community
        ↓
response branch
```

The key biological interpretation is:

> **The same broad community change can help some plant starting states and harm others because response depends on which partners are actually realized and how they match the plant.**

This is the mechanistic bridge from Chapter 1's recurrent functional core to its non-uniform detailed realization.

## Frozen Q2 evidence

### 1. Mixed responses under the same broad island-like change

In the baseline matched design, **41/96** stochastic community histories contain both positive and negative plant responses across the starting-state grid.

Thus response direction is relational rather than an intrinsic property of one plant state.

### 2. Richness changes the mean but does not eliminate branching

Exact stepwise realized-richness matching makes the ensemble mean all-positive in **6/6** prespecified matching seeds, yet **51–65/96** realized community histories remain mixed-sign and state × community non-additivity remains **42.72–48.51%**.

Therefore realized richness matters for coarse regime placement, but richness alone is insufficient to explain branch heterogeneity.

### 3. Arrival/loss-rate differences are also insufficient

Equalizing the baseline partner-arrival and partner-loss rates between mainland-like and island-like regimes still leaves **70/96** mixed realizations and **65.61%** non-additivity.

Thus branch heterogeneity is not generated solely by a difference in turnover rate.

### 4. The dominant determinant changes across finite-community regimes

Under active plant adjustment, pooling independent community trajectories across `k={1,2,4,8,16}` changes the response decomposition:

- `k=1`: starting state 3.11%, community realization 74.27%, non-additivity 22.82%;
- `k=4`: starting state 24.70%, community realization 23.23%, non-additivity 50.82%;
- `k=16`: starting state 53.53%, community realization 14.05%, non-additivity 32.03%.

Starting state exceeds community realization in **4/6** prespecified seeds at `k=4` and **6/6** at `k=8` and `k=16`, while non-additivity is the largest component at `k=4`. The earlier 6/6-at-`k=4` statement came from the superseded offset-stream implementation.

**The numerical synthetic crossover is not transferred to nature.** The crossover near `k=4` is a model-specific coordinate, not a natural ecological threshold.

### 5. Branching is finite-community, not a deterministic mean-field property

Mixed branching persists at finite community size, including large pooled finite systems, but the deterministic mean-field kernel contrast is all-positive.

Branching is therefore finite-community in the asymptotic sense. Its persistence well beyond rare empty-community events means it is not merely a tiny-N extinction artefact.

### 6. Reproductive assurance buffers magnitude, not direction

Across **580** eligible baseline declines, increasing autonomous assurance through the declared envelope yields **0 sign rescues through 4×** assurance, while many declines become smaller in magnitude.

Reproductive assurance is therefore a downstream attenuator rather than a universal branch-flipping mechanism.

This connects directly to Chapter 1: assurance can recur globally as insurance without forcing all detailed pollinator-facing responses to converge.

## HOW, proximal WHY and ultimate WHY

| Level | Question | Current Chapter 2 answer | Claim ceiling |
|---|---|---|---|
| **HOW** | Through what response architecture does pollinator reorganization propagate? | Starting functional state and realized pollinator community jointly determine response branch through trait matching; richness and turnover influence the realized regime but do not uniquely determine branch direction. | Directly represented and audited within the declared synthetic model. |
| **Proximal WHY** | Why can the same broad perturbation yield different responses? | Because response is conditional on starting state × realized community, with strong non-additivity; the relative importance of state, community and interaction changes across finite-community regimes. | Mechanistic existence argument within the frozen synthetic design. The numerical synthetic crossover is not transferred to nature. |
| **Ultimate WHY** | Why did an island acquire its biota, starting states or interaction architecture? | Not tested. | Assembly, colonization, persistence, historical partner loss and evolutionary history remain upstream explanations. |

## Relationship to Chapter 1

The dissertation-level interpretation is:

```text
Chapter 1
WHAT RECURS?
    isolation
      → stronger pollen limitation
      → recurrent functional core
           reproductive assurance ↑
           accessibility/generalization ↑
      + context-dependent display/coupling
                ↓
Chapter 2
WHY NEED RESPONSES NOT BE IDENTICAL?
    starting state × realized partner community
      → positive / negative response branches
      → regime-dependent determinant ordering
```

The strongest cross-chapter statement is:

> **Same broad pressure, recurrent functional core, different detailed trajectories.**

Chapter 2 supplies a mechanistic explanation for how such non-uniformity is possible. It does not identify the historical cause of any specific Chapter 1 regional display pattern.

## What the current paper does not require

The paper does **not** require a same-block field chain of

```text
visitor exposure → single-visit deposition/effective service
→ dependency treatment → mature seed
```

to be scientifically complete.

The E3/E4 Izu field design remains a useful, preregisterable **future falsification/validation protocol**, but it is not:

- part of the present paper's main inferential spine;
- part of the Chapter 2 claim ceiling;
- a required empirical gate for manuscript completion; or
- a prerequisite for the Chapter 2 → Chapter 3 handoff.

The field programme remains **parallel/future validation**, not a completion requirement.

## Relationship to world evidence

World/literature evidence is used to:

1. establish biological plausibility;
2. identify the empirical measurement ceiling; and
3. prevent synthetic results from being narrated as already demonstrated natural causal chains.

The formal source audit remains outcome-rich but process-poor: **21/25** entries contain comparable plant responses, **2/25** directly measure partner arrival/replacement, and **0/25** provide a full outcome-independent transition-linked contract.

This is an identifiability limitation, not a remaining fieldwork obligation.

## Relationship to Izu

Izu remains valuable as a high-continuity future validation system and as the geographic setting of the focal lineage used in Chapter 3.

For the current Chapter 2 paper, Izu is not required to validate the synthetic mechanism. Present-day Izu associations do not identify historical *Bombus* loss or an Oshima–Toshima causal boundary.

## Relationship to Chapter 3

The Chapter 2 → Chapter 3 handoff is a change in inferential scale:

```text
Chapter 2
conditional response mechanism
    → branch heterogeneity
    → regime-dependent determinant ordering
        ↓
Chapter 3
realized multivariate phenotype in the focal lineage
```

Chapter 3 phenotype values are not used to tune, rescue or validate Chapter 2.

## Claim boundary

Chapter 2 must not imply that:

- Chapter 1 identified *Bombus* loss or another named pollinator as the cause of regional differences;
- Chapter 1 regional display patterns have been assigned to specific Chapter 2 parameter regimes;
- the Chapter 2 model proves why a particular Chapter 1 region shows a particular colour/architecture pattern;
- one universal pollinator mechanism has been identified;
- starting state alone determines response;
- realized community is universally dominant;
- synthetic branch frequencies estimate natural prevalence;
- the crossover near `k=4` is a natural threshold;
- raw visitor richness or effective-service diversity is literally synthetic `k`;
- reproductive assurance is sufficient to reverse every upstream service disadvantage;
- historical *Bombus* loss, evolutionary selection or causal mediation has been identified;
- the prospective Izu same-block chain is required for Chapter 2 completion; or
- Chapter 3 phenotype divergence proves the Chapter 2 mechanism.

## Dissertation sequence

```text
Chapter 1
WHAT recurs globally?
    recurrent functional core
    + context-dependent pollinator-facing display
        ↓
Chapter 2
WHY need responses not be uniform?
    starting state × realized community
    → conditional branches
    → regime-dependent determinant ordering
        ↓
Chapter 3
WHAT multivariate phenotype is realized in the focal lineage?
```

The Izu same-block E3/E4 programme remains explicitly parallel/future validation.
