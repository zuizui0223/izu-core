# Thesis positioning — Chapter 2

Updated: 2026-09-27

## Role in the dissertation

`izu-core` is the **Chapter 2 / mechanistic explanation of non-uniform island-syndrome response** component of the dissertation.

The current dissertation sequence is:

- `zuizui0223/island` — **Chapter 1:** what recurs globally under island isolation, and which phenotype dimensions remain context dependent;
- `izu-core` — **Chapter 2:** why a recurrent broad constraint need not generate one detailed plant response, and how conditional interaction responses propagate through reproduction, demography and inherited floral change;
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

> **Why can a recurrent island functional syndrome coexist with non-uniform floral trajectories, and under what reproductive and demographic conditions are those trajectories realized?**

The current answer has **two linked mechanistic layers**:

```text
Model 2 — conditional interaction response
broad pollinator-interaction reorganization
        ↓
coarse response regime
        ×
plant starting functional state
        ×
realized pollinator community
        ↓
response branch

Model 3 — demographic/evolutionary realization
response branch + pollen delivery
        ×
reproductive assurance / inbreeding depression
        ×
life history / connectivity / demographic history
        ↓
persistence + inherited floral-investment trajectory
```

The key biological interpretation is:

> **The same broad island pressure can recur at the level of function without forcing one floral endpoint: interaction geometry first creates conditional branches, and reproduction and demography determine which branches persist and how inherited floral investment changes.**

This is the mechanistic bridge from Chapter 1's recurrent functional core to its non-uniform detailed realization.

## Frozen Q2 evidence

### 1. Mixed responses under the same broad island-like change

The historical offset-stream baseline contained **41/96** mixed-sign community histories, but that draw is provenance only. Under the collision-free six-seed correction, mixed-sign histories have median **45.5/96** with range **43–59/96**.

Thus response direction is relational rather than an intrinsic property of one plant state.

### 2. Richness changes the mean but does not eliminate branching

Under the collision-free RNG correction, exact stepwise realized-richness matching makes the ensemble mean all-positive in **6/6** prespecified matching seeds, yet **55–64/96** realized community histories remain mixed-sign and state × community non-additivity remains **28.48–43.64%**.

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

### 6. Reproductive assurance buffers magnitude, not direction in Model 2

Across **580** eligible baseline declines, increasing autonomous assurance through the declared envelope yields **0 sign rescues through 4×** assurance, while many declines become smaller in magnitude.

Reproductive assurance is therefore a downstream attenuator rather than a universal branch-flipping mechanism in the response-geometry layer.

### 7. Model 3 carries the argument through reproduction, demography and inheritance

The completed island campaign contains **19,968 audited cases** across 80 predeclared design cells plus six held-out rows. It adds explicit offspring accounting, delayed selfing, inbreeding depression, Mendelian inheritance, density regulation, adult survival, connectivity, disturbance timing and source-versus-resident immigration.

Three results are the Chapter 2 handoff rather than a separate project:

1. **History matters even under a common final environment.** Early visitor loss produced mean investment change `-0.1603`, late loss `+0.0322`, and uninterrupted histories `+0.2115` over the declared horizon.
2. **Assurance controls whether an evolutionary endpoint exists.** Under the scheduled long visitor absence, fixed zero assurance yielded `0/256` terminal survivors, whereas fixed/evolving assurance treatments retained `256/256` in the corresponding declared cells.
3. **Current environment does not uniquely identify trajectory.** Transported S/C/I ordering can remain similar while marginal trait predictions degrade sharply across disturbance regimes; source-state, history and demographic context remain necessary.

These are model-conditional results and not calibrated natural-island rates. Several magnitude comparisons remain numerically resolution-sensitive, so Chapter 2 uses Model 3 primarily for directional and mechanistic contrasts rather than universal quantitative forecasts.

Together Models 2 and 3 explain how assurance can recur globally as insurance while detailed pollinator-facing and inherited floral responses remain contingent.

## HOW, proximal WHY and ultimate WHY

| Level | Question | Current Chapter 2 answer | Claim ceiling |
|---|---|---|---|
| **HOW — interaction layer** | Through what response architecture does pollinator reorganization propagate? | Starting functional state and realized pollinator community jointly determine response branch through trait matching; richness and turnover influence the realized regime but do not uniquely determine branch direction. | Directly represented and audited in Model 2. |
| **HOW — realization layer** | How can a conditional branch become an inherited island trajectory? | Model 3 propagates pollen delivery through selfing/outcrossing, viability, inheritance, density regulation, survival, connectivity and history to persistence and floral-investment change. | Directly represented within the declared Model 3 scenarios; quantitative natural calibration is absent. |
| **Proximal WHY** | Why can the same broad perturbation yield different responses? | Because response is conditional on starting state × realized community, and because reproductive assurance, life history, connectivity and disturbance history change whether and how those responses persist. | Mechanistic existence argument across the two linked synthetic layers. Numerical thresholds and rates are not transferred to nature. |
| **Ultimate WHY** | Why did an island acquire its biota, starting states or interaction architecture? | Not identified. | Deep-time assembly, colonization history and the historical causes of any named natural-island transition remain outside the claim ceiling. |

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
    Model 2: starting state × realized partner community
      → positive / negative response branches
      → regime-dependent determinant ordering
    Model 3: branch × reproduction × demography × history
      → persistence / extinction
      → inherited floral-investment trajectories
```

The strongest cross-chapter statement is:

> **Same broad pressure, recurrent functional core, different detailed trajectories because ecological branching and demographic/evolutionary realization are both conditional.**

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
Model 2: conditional response mechanism
    → branch heterogeneity
    → regime-dependent determinant ordering
Model 3: reproductive/demographic realization
    → persistence + inherited floral-investment trajectories
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
- Model 3 establishes a universal evolutionary direction, a calibrated island timescale, or natural extinction probability;
- Model 3's investment coordinate is already identified with a specific flower colour, size or nectar-guide trait in nature;
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
    Model 2: starting state × realized community
      → conditional functional branches
    Model 3: reproduction × demography × history
      → persistence and inherited floral trajectories
        ↓
Chapter 3
WHAT multivariate phenotype is realized in the focal lineage?
```

The Izu same-block E3/E4 programme remains explicitly parallel/future validation.
