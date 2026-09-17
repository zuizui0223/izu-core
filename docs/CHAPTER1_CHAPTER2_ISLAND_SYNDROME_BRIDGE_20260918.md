# Chapter 1 → Chapter 2 bridge — recurrent core, non-uniform response

Updated: 2026-09-18

## Purpose

This document fixes the dissertation-level bridge after the September 2026 Chapter 1 v13 update. It does **not** change any frozen Chapter 1 or Chapter 2 result, simulation, parameterization, result lock, submission route, or claim ceiling.

The programme-level story is:

> **Chapter 1 establishes a recurrent global functional floral/reproductive island-syndrome core and an independent global pollination constraint, while pollinator-facing floral display is reorganized non-uniformly among contexts. Chapter 2 asks why a common broad constraint need not produce one detailed plant response.**

The four-step narrative is:

```text
1. recurrent global functional island-syndrome core
       ↓
2. independent evidence for increasing pollen limitation with isolation
       ↓
3. pollinator-facing display is reorganized differently among contexts
       ↓
4. Chapter 2: starting state × realized pollinator community can generate divergent branches
```

## Q1 — What recurs globally?

The latest `island` Chapter 1 v13 result separates a recurrent functional core from a context-dependent display layer.

### Recurrent functional core

Two partially separable phenotype modules recur in the classic-positive direction in all four predeclared geographic replication strata and in both evidence scopes:

1. **reproductive assurance** — self-compatibility, selfing and autonomous-selfing states that can reduce dependence on successful outcross pollen delivery;
2. **floral accessibility/generalization** — more open, generalized and radially accessible architectures that can reduce dependence on narrowly matched visitor access.

These are the frozen H1 core. Chapter 1 does not require every atomic trait to move identically.

### Independent pollination constraint

Independent GloPL data support a global increase in experimental pollen limitation with geographic isolation:

- 2,969 experiments;
- 1,248 sites;
- 919 publications;
- standardized distance coefficient `+0.07937`;
- SE `0.03773`;
- two-sided `p=0.0354`;
- one-sided positive `p=0.0177`.

The strongest post-hoc functional bridge is autonomous selfing, which is associated with lower current experimental pollen limitation (`beta=-0.4467`, two-sided `p=2.60e-08`). This is functional compatibility, not historical causal mediation.

## Q1b — What does not recur identically?

The third phenotype module is **pollinator-facing floral display**: raw flower-colour composition and colour–architecture coupling.

This layer contains real isolation-associated structure after measured reproductive assurance is conditioned out, but its detailed direction is context dependent.

- **Northern mid-latitude:** `red_pink` declines in both evidence scopes after `selfing_core` adjustment; no named colour-conditioned architecture survives FDR.
- **Northern high latitude:** the five-colour vector is not jointly supported, but `blue_purple × butterfly-associated form` and `blue_purple × intermediate/deep large-bee-associated tube` decline strongly.
- **Tropical:** direct evidence supports `yellow_orange × deep butterfly-associated tube` increasing with isolation.
- **Southern extratropical:** white increases strongly in direct evidence; yellow/orange architecture shows mixed restructuring in all-analysis but is not retained in direct-only after FDR.

The Chapter 1 conclusion is therefore:

> **same functional core, different pollinator-facing realization.**

It is not a claim that one realized pollinator guild replaces another everywhere.

---

# Q2 — Why need responses not be uniform?

Chapter 2 answers a narrower mechanistic question:

> **Why can the same broad island-like reorganization of pollinator interactions generate different plant responses?**

The answer is a conditional response geometry. A broad shift in pollinator community structure does not map one-to-one onto plant response because response depends on the relation between:

1. the plant's **starting functional position**;
2. the **pollinator community actually realized** after stochastic arrival, loss and replacement; and
3. their **trait-matching interaction**.

## Model logic

Plants and pollinators occupy a common standardized trait axis. Each pollinator has a trait position and interaction breadth. Plant–pollinator matching declines with trait mismatch. Community-level matching is converted into pollination service with a saturating response.

The response for each plant starting position is:

```text
island-like service − mainland-like service
```

The mainland-like regime has more initial pollinator types, higher arrival and lower loss; the island-like regime has fewer initial types, higher loss, more generalists and more replacement. These are synthetic response-geometry settings, not fitted estimates of a universal island community.

## Result 1 — the same island-like change can help and harm different plants

In the baseline matched design, **41/96** stochastic community histories contain mixed-sign responses: within one realized mainland→island community contrast, some plant starting positions gain service while others lose it.

Therefore the island effect is relational rather than intrinsic to one plant trait state.

## Result 2 — realized richness shifts the mean, but does not remove branching

Exact stepwise realized-richness matching removes the coarse richness difference between mainland-like and island-like communities.

- the ensemble mean becomes all-positive in **6/6** prespecified matching seeds;
- nevertheless **51–65/96** individual realized community histories remain mixed-sign;
- state × community non-additivity remains **42.72–48.51%**.

Interpretation:

> **richness helps determine the coarse mean regime, but which partners remain and how they match the plant determine individual response branches.**

It is therefore too strong to say that richness is irrelevant; the control shows that richness is insufficient to explain branch heterogeneity.

## Result 3 — arrival/loss-rate differences are also insufficient

Equalizing the baseline partner-arrival and partner-loss rates between mainland-like and island-like regimes still leaves:

- **70/96** mixed realizations;
- **65.61%** state × community non-additivity.

Thus branch heterogeneity is not generated solely by a difference in turnover rate.

## Result 4 — the dominant determinant changes with finite-community regime

With active plant adjustment and independent community trajectories pooled across `k={1,2,4,8,16}`, the normalized response decomposition changes:

| `k` | starting state `S` | community realization `C` | non-additivity `I` | dominant component |
| ---: | ---: | ---: | ---: | --- |
| 1 | 0.0255 | 0.7298 | 0.2471 | community |
| 2 | 0.1033 | 0.4803 | 0.4171 | community |
| 4 | 0.2733 | 0.2352 | 0.4947 | interaction |
| 8 | 0.4252 | 0.1826 | 0.4007 | starting state |
| 16 | 0.5584 | 0.1272 | 0.3199 | starting state |

Starting state exceeds community realization from `k=4` onward in **6/6** prespecified seeds, while the interaction component is largest at `k=4`.

The biological reading is:

> **small stochastic communities are strongly contingent on which partners remain; intermediate regimes emphasize plant × community interaction; larger pooled regimes reduce community-realization variance and expose the plant's starting functional position.**

The numerical crossover near `k=4` is model-specific and is not a natural threshold.

## Result 5 — branching is a finite-community phenomenon, but not merely a tiny-N artefact

A finite-community limit analysis shows:

- community stochasticity declines as independent community copies are pooled;
- mixed responses persist at finite `k`, including `k=16`;
- the deterministic mean-field kernel contrast is all-positive.

Thus branching disappears only in the deterministic mean-field limit. It is finite-community in the asymptotic sense, but its persistence well beyond rare empty-community events means it is not merely a tiny-community extinction artefact.

## Result 6 — reproductive assurance buffers magnitude, not direction

The downstream assurance audit contains **580** eligible baseline declines. Increasing autonomous assurance through the declared envelope produces:

- many magnitude improvements;
- **0/580 sign rescues** through `4×` assurance.

Therefore reproductive assurance is a downstream buffer in this model: it can reduce the cost of poor pollination service, but it does not erase the upstream state × community geometry or convert every losing branch into a winning branch.

This connects naturally to Chapter 1: reproductive assurance can be globally recurrent as insurance while detailed pollinator-facing responses remain contingent.

---

# Integrated dissertation interpretation

The strongest cross-chapter statement is:

> **Island isolation is associated globally with a recurrent functional shift toward reproductive assurance and floral accessibility, but this common functional syndrome does not require identical detailed floral responses. Chapter 2 provides a mechanistic existence argument: under the same broad pollinator-community reorganization, response direction can branch because plants begin at different functional positions and encounter different realized partner compositions.**

A concise version is:

> **Same pressure, recurrent functional core, different detailed trajectories.**

Or, in Chapter language:

> **Chapter 1 asks what recurs; Chapter 2 asks why recurrence need not imply uniform response.**

## What Chapter 2 does and does not explain

Chapter 2 supports the mechanistic possibility that Chapter 1-like non-uniformity can emerge from conditional plant × community response geometry.

It does **not** show that:

- the northern-high-latitude, northern-midlatitude, tropical or southern-extratropical Chapter 1 display patterns were caused by specific Chapter 2 parameter regimes;
- one named pollinator group caused any regional Chapter 1 response;
- synthetic branch frequencies estimate natural prevalence;
- `k≈4` is a natural ecological threshold;
- the model proves historical pollinator loss, selection or causal mediation;
- reproductive assurance is sufficient to reverse an upstream service disadvantage.

The link is therefore a programme-level explanation of **how non-uniform response is possible under a recurrent broad constraint**, not a cross-repository causal validation of the observed regional patterns.

## Presentation spine

For a thesis talk or poster, the recommended four-step order is:

1. **Global recurrent functional core** — reproductive assurance and accessibility/generalization recur across all four geographic strata.
2. **Independent pressure** — experimental pollen limitation increases with isolation globally.
3. **Non-uniform realization** — pollinator-facing colour/architecture is reorganized differently among contexts.
4. **Mechanistic explanation** — starting functional position × realized pollinator community generates branch heterogeneity; richness and turnover alone are insufficient, determinant importance changes across finite-community regimes, and assurance buffers magnitude without erasing direction.

This is the current Chapter 1 → Chapter 2 dissertation bridge.