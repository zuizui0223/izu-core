# Thesis positioning — Chapter 2

> Current-route note (2026-10-06): Chapter 2 is governed by
> `docs/CHAPTER2_PROCESS_MAINLINE_20261005.md`. Its primary process result is now
> independently confirmed: in the delayed-selfing/costly positive-mutation
> regime, assurance-first realized change repeated in 51/64 new visitor histories
> (95% bootstrap 0.6875–0.8906), while a preregistered fixed-assurance
> intervention retained negative investment change. The confirmed sequence is
> setting-specific and is not generalized to prior selfing. The older
> bridge-focused material below is retained as thesis provenance and supporting
> mechanism, not as the current paper-level headline.

Updated: 2026-09-27

## Role in the dissertation

`izu-core` is the **Chapter 2 / mechanistic explanation of non-uniform island-syndrome response** component of the dissertation.

The current dissertation sequence is:

- `zuizui0223/island` — **Chapter 1:** what recurs globally under island isolation, and which phenotype dimensions remain context dependent;
- `izu-core` — **Chapter 2:** why a recurrent broad constraint need not generate one detailed plant response, and how conditional interaction responses propagate through reproduction, demography and inherited floral change;
- `zuizui0223/shimahotarubukuro` — **Chapter 3:** what multivariate phenotype is actually realized in the focal Izu lineage.

The active cross-chapter bridge is fixed in [`docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md`](docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md). The 2026-09-18 bridge remains historical provenance.

## Chapter 1 handoff

Chapter 1 v13 now establishes a **recurrent but non-uniform floral island syndrome**.

Two partially separable phenotype modules form the recurrent functional core across all four predeclared geographic replication strata:

1. reproductive assurance;
2. floral accessibility/generalization.

Independent GloPL data also show increasing experimental pollen limitation with geographic isolation. In contrast, raw flower colour and colour–architecture coupling form a pollinator-facing display module whose detailed organization differs among ecological contexts.

The Chapter 1 handoff is therefore:

> **A common broad functional response recurs globally, but detailed pollinator-facing phenotype organization is not identical. Why can the same broad ecological constraint generate different response trajectories?**

## Chapter 1 unresolved-problem handoff

Chapter 1 leaves four problems that Chapter 2 must address without retroactive causal overreach:

1. **recurrent function versus non-recurrent phenotype** — assurance/accessibility recur, but detailed display does not;
2. **selfing is not the whole explanation** — some colour/architecture associations remain after selfing adjustment;
3. **stress versus compensation** — isolation is associated with stronger pollen limitation, yet some island-associated functional traits are associated with lower realized limitation;
4. **cross-sectional identifiability** — present regional states do not identify whether the route was selection, founding, immigration, buffering or demographic sorting.

Unified Model 3 now resolves the first three at a stronger level. Controlled state × visitor composition establishes branch capacity before demography; the prospective isolation bridge shows that realized visitor amount/richness strongly shifts the coarse mean response, while visitor-environment realization and finite plant demography separately modify the distribution of observed directional outcomes. Assurance can buffer or preserve populations without forcing one floral direction. Chapter 2 narrows the fourth by separating founding, immigration, chronology and finite realization, but the natural inherited longitudinal B layer remains unobserved.

Canonical resolution matrix: `docs/CHAPTER1_OPEN_PROBLEMS_TO_UNIFIED_MODEL3_20260927.md`.

## Canonical Chapter 2 question

> **Why can a recurrent island functional syndrome coexist with non-uniform floral trajectories, and under what reproductive and demographic conditions are those trajectories realized?**

The current answer is one **nested Model 3** examined at successive levels:

```text
A. fixed-state reproductive assay
visitor composition × starting floral state
        ↓
selection / reproductive-return branch

B. deterministic genotype-density propagation
   - conditional deterministic closure using the same reproduction/inheritance operator; not the stochastic mean of the finite ABM
same reproduction + Mendelian inheritance
without demographic sampling
        ↓
conditional deterministic inherited trajectory

C. finite-population ABM
same operator + finite demography
        ↓
persistence / extinction
+ standing-variation loss
+ realized inherited trajectory

D. context interventions
assurance + chronology + connectivity + recovery + life history
        ↓
conditional realization
```

The former Model 2 is not retained as a separate biological mechanism, active control gate or current Supporting Information component. Its exact-richness, synthetic-`k`, response-rule, S/C/I and community-mean results are historical legacy provenance under `legacy/model2/` because the previously unique richness and finite-visitor controls have now been evaluated prospectively inside Model 3.

The key biological interpretation is:

> **The same broad island pressure can recur at the level of function without forcing one floral endpoint: interaction geometry first creates conditional branches, and reproduction and demography determine which branches persist and how inherited floral investment changes.**

This is the mechanistic bridge from Chapter 1's recurrent functional core to its non-uniform detailed realization.

## Current Chapter 2 evidence

### Primary unified Model 3 result

The current mechanistic spine is the **fixed-state branch-capacity audit + 19,968-case island campaign + prospective 24,576-case isolation bridge**.

The final prospective bridge resolves the two original Chapter 2 controls that had remained unique to Model 2:

- **natural isolation-driven assembly:** finite ABM mean far-minus-near inherited-investment effect `-0.1446`, conditional deterministic density closure `-0.4510`; mixed histories `12/128` versus `0/128` at epsilon 0; the magnitude gap is not a finite-population attenuation estimate;
- **annual response-blind richness matching:** means reverse to `+0.0333` and `+0.0338`; finite-ABM mixed histories rise to `68/128` at epsilon 0;
- **eight-history visitor pooling:** mixed histories fall to `0/128` in both finite ABM and deterministic density;
- **plant capacity 48 → 192:** finite-ABM mixed histories fall `12/128 → 1/128` at epsilon 0 and the mean numerically closes 41.5% of the trait-effect gap to deterministic density; this is descriptive and not evidence of convergence to a stochastic expectation;
- **S/C/I is not directional branching:** pooled finite ABM has `I=0.542` but `0/128` mixed histories.

The biological hierarchy is therefore:

> **visitor amount/richness sets the coarse mean regime; visitor composition/history and finite plant demography are separate axes that strongly modify realized outcomes.** Finite-ABM history labels are stochastic and numerically sensitive: repeat-specific classifications disagree within 97/128 natural histories and 128/128 richness-matched histories at epsilon 0, so they are not interpreted as stable latent lineage classes or prevalence estimates.

Legacy response-geometry analyses remain useful Supporting Information/provenance, but no longer carry an active scientific gate.

### Legacy reduced response-geometry robustness — Supporting Information only

#### 1. Mixed responses under the same broad island-like change

The historical offset-stream baseline contained **41/96** mixed-sign community histories, but that draw is provenance only. Under the collision-free six-seed correction, mixed-sign histories have median **45.5/96** with range **43–59/96**.

Thus response direction is relational rather than an intrinsic property of one plant state.

#### 2. Richness changes the mean but does not eliminate branching

Under the collision-free RNG correction, exact stepwise realized-richness matching makes the ensemble mean all-positive in **6/6** prespecified matching seeds, yet **55–64/96** realized community histories remain mixed-sign and state × community non-additivity remains **28.48–43.64%**.

Therefore realized richness matters for coarse regime placement, but richness alone is insufficient to explain branch heterogeneity.

#### 3. Arrival/loss-rate differences are also insufficient

Equalizing the baseline partner-arrival and partner-loss rates between mainland-like and island-like regimes still leaves **70/96** mixed realizations and **65.61%** non-additivity.

Thus branch heterogeneity is not generated solely by a difference in turnover rate.

#### 4. The dominant determinant changes across finite-community regimes

Under active plant adjustment, pooling independent community trajectories across `k={1,2,4,8,16}` changes the response decomposition:

- `k=1`: starting state 3.11%, community realization 74.27%, non-additivity 22.82%;
- `k=4`: starting state 24.70%, community realization 23.23%, non-additivity 50.82%;
- `k=16`: starting state 53.53%, community realization 14.05%, non-additivity 32.03%.

Starting state exceeds community realization in **4/6** prespecified seeds at `k=4` and **6/6** at `k=8` and `k=16`, while non-additivity is the largest component at `k=4`. The earlier 6/6-at-`k=4` statement came from the superseded offset-stream implementation.

**The numerical synthetic crossover is not transferred to nature.** The crossover near `k=4` is a model-specific coordinate, not a natural ecological threshold. In short, the legacy `k` crossover is **not a natural threshold**.

#### 5. Legacy community-mean limit removes response-geometry branching

In the legacy response-geometry reduction, mixed branching persists at finite community size, including large pooled finite systems, but averaging external community realization into the deterministic community-mean kernel yields an all-positive contrast. This is a different limit from the unified Model 3 genotype-density counterpart, which retains visitor composition/history while removing demographic sampling and therefore can retain branching.

### Unified Model 3: reproductive return, deterministic inheritance and finite realization

Across **580** eligible baseline declines, increasing autonomous assurance through the declared envelope yields **0 sign rescues through 4×** assurance, while many declines become smaller in magnitude.

At the reduced response layer, reproductive assurance is therefore an attenuator rather than a universal branch-flipping mechanism. In the full Model 3 trajectories, assurance can additionally determine whether a population persists long enough for an inherited endpoint to exist.

### 7. The unified Model 3 carries the same branch through deterministic and finite-population realization

The completed island campaign contains **19,968 audited cases** across 80 predeclared design cells plus six held-out rows. It adds explicit offspring accounting, delayed selfing, inbreeding depression, Mendelian inheritance, density regulation, adult survival, connectivity, disturbance timing and source-versus-resident immigration.

Four results now define the Chapter 2 handoff:

1. **History matters even under a common final environment.** Early visitor loss produced mean investment change `-0.1603`, late loss `+0.0322`, and uninterrupted histories `+0.2115` over the declared horizon.
2. **Assurance controls whether an evolutionary endpoint exists.** Under the scheduled long visitor absence, fixed zero assurance yielded `0/256` terminal survivors, whereas fixed/evolving assurance treatments retained `256/256` in the corresponding declared cells.
3. **Branch capacity does not require demographic stochasticity, but isolation-driven realization can.** Controlled fixed compositions retain positive and negative responses in deterministic genotype density, whereas the stored near-versus-far isolation effect is mixed in finite ABM histories but 0/128 mixed in deterministic density in both cohorts.
4. **Current environment does not uniquely identify trajectory.** Transported S/C/I ordering can remain similar while marginal trait predictions degrade sharply across disturbance regimes; source-state, history and demographic context remain necessary.

These are model-conditional results and not calibrated natural-island rates. Several magnitude comparisons remain numerically resolution-sensitive, so Chapter 2 uses Model 3 primarily for directional and mechanistic contrasts rather than universal quantitative forecasts.

Together the nested levels of Model 3 explain how assurance can recur globally as insurance while detailed pollinator-facing and inherited floral responses remain contingent. The prospective bridge closes the old richness and finite-community controls: visitor amount shifts the mean regime, while visitor-environment and plant-demographic manipulations strongly modify descriptive heterogeneity without identifying a stable latent branch prevalence. Legacy Model 2 is now robustness/provenance only.

## HOW, proximal WHY and ultimate WHY

| Level | Question | Current Chapter 2 answer | Claim ceiling |
|---|---|---|---|
| **HOW — ecological selection** | Where does non-uniformity first arise? | Within Model 3's fixed-state reproductive operator, starting floral state × visitor composition changes the sign of the reproductive-selection gradient even before inheritance or demographic updating. | Directly represented in the unified reduction audit. |
| **HOW — deterministic evolution** | Does branching require demographic noise? | Not universally. Controlled compositions branch without demographic sampling, but the stored isolation-driven deterministic contrast is one-directional while finite ABM histories can be mixed. | Deterministic discrete-genotype closure; regime-specific answer; not a diffusion PDE. |
| **HOW — finite realization** | What changes in finite populations? | Finite demography, extinction, standing-variation loss, ancestry and stochastic recruitment can shift magnitude and sometimes direction relative to the conditional deterministic closure. | The closure is a comparator, not the stochastic mean of the ABM; quantitative natural calibration is absent. |
| **Proximal WHY** | Why can the same broad perturbation yield different responses? | Because functional matching already makes selection state-dependent, while assurance, life history, connectivity and disturbance history condition which deterministic or finite-population trajectory is realized. | One nested synthetic mechanism, not two independent models. Numerical thresholds and rates are not transferred to nature. |
| **Ultimate WHY** | Why did an island acquire its biota, starting states or interaction architecture? | Not identified. | Deep-time assembly, colonization history and the historical causes of any named natural-island transition remain outside the claim ceiling. |

## Chapter 1 unresolved problems now carried explicitly into Chapter 2

The active cross-chapter bridge is `docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md`, with a problem-by-problem ledger in `docs/CHAPTER1_OPEN_PROBLEMS_TO_UNIFIED_MODEL3_20260927.md`.

The key shift is that Chapter 2 no longer merely demonstrates that heterogeneous responses are possible. It now identifies the stage at which Chapter 1's non-uniformity can arise:

- **before demography:** starting floral state × visitor composition reverses reproductive-selection direction;
- **under controlled deterministic inheritance:** branch capacity can remain when demographic sampling is removed;
- **under isolation-driven assembly:** annual visitor amount/richness strongly shifts the mean deterministic regime;
- **during finite realization:** visitor histories and finite plant demography separately modify observed heterogeneity, while assurance, chronology, connectivity and life history change which trajectories persist; exact branch prevalence remains unresolved.

This addresses the central Chapter 1 tension — recurrent assurance/accessibility but non-uniform detailed display — without assigning any Chapter 1 region to a Model 3 parameter cell.

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
    Unified Model 3:
      fixed-state matching/selection
        → positive / negative branches
      isolation-driven deterministic response
        → coarse directional backbone set partly by visitor amount
      finite visitor histories + finite plant demography
        → branch realization / suppression
      assurance + history
        → persistence / extinction
        → inherited floral-investment trajectories
```

The strongest cross-chapter statement is:

> **Same broad pressure, recurrent functional core, different detailed trajectories because coarse ecological pressure and finite ecological/demographic realization operate at different levels.**

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
Unified Model 3
    → fixed-state selection branching
    → deterministic branch capacity, regime-dependent under isolation
    → finite-population/history-dependent realization
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
    one nested Model 3
      → starting state × visitor composition changes selection
      → visitor amount/richness shifts the coarse deterministic regime
      → finite visitor + finite plant sampling shape branch realization
      → demography/history modifies persistence
        ↓
Chapter 3
WHAT multivariate phenotype is realized in the focal lineage?
```

The Izu same-block E3/E4 programme remains explicitly parallel/future validation.
