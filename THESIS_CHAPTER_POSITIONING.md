# Thesis positioning — Chapter 2

## Role in the dissertation

This repository is the **Chapter 2 / mechanistic-identification** component of the dissertation.

The shared dissertation-level question is:

> **How does geographic isolation alter plant reproduction through changes in ecological interactions, and why do those changes produce different floral outcomes across islands and lineages?**

The three empirical levels are now:

- [`zuizui0223/island`](https://github.com/zuizui0223/island) — **Chapter 1:** asks **when and where** isolation-associated floral/reproductive filtering is detectable and where multivariate response vectors differ.
- `izu-core` — **Chapter 2:** asks **how** post-establishment interaction change can generate different response architectures and supplies a model-conditional **proximal why**. It does not assign the Chapter 1 regions to particular model regimes.
- [`zuizui0223/shimahotarubukuro`](https://github.com/zuizui0223/shimahotarubukuro) — **Chapter 3:** measures **what phenotype axes actually diverge** within one focal lineage.

## Chapter 1 handoff now entering Chapter 2

The canonical Chapter 1 when/where run (`32837335384`) establishes that:

1. isolation-associated floral/reproductive filtering is confirmatorily detectable in **northern mid-latitude** island floras;
2. it is also confirmatorily detectable in **tropical** island floras;
3. both signals persist within **native non-endemic** assemblages, so neither is confined to endemic-lineage turnover;
4. the northern-midlatitude and tropical isolation-response vectors differ confirmatorily at the multivariate level;
5. northern high-latitude and southern-extratropical contexts remain data-limited at the confirmatory tier.

Chapter 1 therefore ends with:

> **Why does isolation generate detectable filtering in both northern mid-latitude and tropical island floras, yet produce significantly different multivariate response vectors in those contexts?**

That is the Chapter 2 question.

## Chapter 2 causal framework

The mechanistic framework remains:

\[
W(z)=F(z)E(z),
\]

where:

- `F(z)` is local reproductive contribution under a focal trait or interaction state;
- `E(z)` is establishment / reachability conditional on viable reproduction;
- `W(z)` is the observed island pattern.

Chapter 1 mainly detects differences in `W`. The current Chapter 2 simulation diagnoses post-establishment ecological processes inside `F`. Alternative establishment/history processes inside `E` remain ultimate explanations outside its direct test.

The bridge is therefore a capability and conditional-response argument: Chapter 1 establishes that a broad geographic/source-pool gradient is expressed through different regional multivariate vectors, while Chapter 2 shows how one broad interaction perturbation can produce different response signs. It does **not** empirically identify which Chapter 2 regime generated the northern-midlatitude or tropical Chapter 1 vector.

## Candidate mechanisms to distinguish

Chapter 2 should not assume one preferred pollinator story. Candidate explanations include:

- Bombus taxonomic identity or dependency;
- large/long-tongued pollinator function;
- pollinator functional diversity;
- plant–pollinator trait matching;
- effective pollination service;
- visitor effectiveness / legitimate contact;
- reproductive dependency and assurance;
- functional replacement by alternative guilds;
- interaction-network state;
- geography, establishment and lineage history.

Pollinator occurrence, floral phenotype, visitor identity or island order alone are insufficient to identify mechanism.

## Current mechanistic evidence

The current Izu evidence retains the following useful chain:

```text
pollinator functional diversity
-> trait matching                     [comparatively robust]
-> pollen receipt                     [directional, network-state uncertain]
-> morphology / reproductive response [branching / lineage dependent]
```

This is now interpreted against a stronger Chapter 1 boundary result: the same broad exposure, geographic isolation, is associated with **different multivariate floral/reproductive response vectors** in northern-midlatitude and tropical floras.

Chapter 2 therefore needs to explain **response allocation**, not merely whether isolation matters.

## HOW, proximal WHY and ultimate WHY

- **HOW:** pollinator turnover and matching alter service; local availability / interaction filtering changes the realized response branch; autonomous assurance changes downstream magnitude without rescuing sign in the declared envelope.
- **Proximal WHY:** the response surface changes with the balance of partner loss and arrival and other matching dimensions, realized community state is the largest source of cell-level variation, and starting position combines non-additively with community realization.
- **Ultimate WHY:** why a region acquired its biota, lineage starting states or local interaction architecture remains an assembly, colonization, persistence and evolutionary-history question not tested by the current simulation.

The frozen conditional-WHY diagnostics sharpen this division. In the baseline `21 × 96` response matrix, starting-position, community-realization and non-additive remainder account for `2.18%`, `80.17%` and `17.64%` of total sum of squares, respectively. Starting position organizes the mean U-shaped boundary, but realized community state dominates cell-level variation. Across the fixed joint surface, partner loss and partner arrival have the largest sign-stable additive associations with the negative fraction of the starting-position grid. Local filtering is bidirectional but asymmetric: positive baseline branches cross to non-positive more readily than negative branches cross to non-negative at every non-zero declared strength.

These are synthetic design diagnostics. They do not estimate natural frequencies, causal field effects or calibrated ecological thresholds.

## Response-branching expectation

> **A shared geographic perturbation need not generate one biological response if functional starting state, interaction context, reproductive buffering, alternative partners and lineage history differ.**

Possible response modes include:

1. continuous within-lineage trait or mating-system change;
2. threshold reproductive assurance;
3. interaction rewiring;
4. hybrid / lineage replacement;
5. alternative-guild specialization;
6. little downstream response despite upstream interaction change;
7. occupancy / persistence filtering rather than within-lineage evolution.

These are not pooled into one island-adaptation score.

## Falsification logic

A convincing mechanism should show that:

- the proposed functional/dependency state changes at the relevant boundary;
- matched nondependent or alternative systems do not reproduce the same result merely because they share geography;
- climate, area, history and observation structure do not explain the pattern equally well;
- visitor identity is separated from effective pollen transfer;
- effective service is separated from reproductive dependency;
- occupancy/lineage replacement is not mislabeled as within-lineage adaptation;
- null and counterdirectional results do not trigger post-hoc mechanism rescue.

## Relationship to the frozen `izu-core` publication mainline

The current `izu-core` publication mainline remains scientifically frozen. This thesis-positioning document does **not** reopen that manuscript or require new data for its submission.

For the dissertation, the Chapter 1 when/where result supplies a broader motivation for the mechanistic architecture already developed here. Any future direct field comparison of northern/tropical or Bombus/functional-service alternatives should be treated as a thesis empirical extension, not as a prerequisite for the frozen publication.

## Relationship to Chapter 3

Chapter 3 provides a directly measured within-lineage phenotype across five Izu islands. It does not identify the causal pollinator mechanism.

The dissertation sequence is therefore:

```text
Chapter 1
WHEN / WHERE is filtering detectable?
WHERE do response vectors differ?
        ↓
Chapter 2
WHY do those contexts generate different response architectures?
        ↓
Chapter 3
WHAT floral phenotype axes actually diverge within one lineage?
```

## Claim boundary

Chapter 2 should not imply that:

- Chapter 1 has identified Bombus loss or another pollinator as the cause of the northern/tropical difference;
- pollinator occurrence equals effectiveness;
- floral form identifies effective-pollinator dependency;
- one functional decline must yield one floral response direction;
- occupancy / lineage replacement equals within-lineage floral evolution; or
- Chapter 3 phenotypic divergence identifies the historical mechanism;
- the northern-midlatitude and tropical Chapter 1 vectors have been assigned to particular Chapter 2 parameter regimes; or
- the Chapter 2 model explains why those regional biotas, starting states or interaction architectures formed.

The Chapter 2 contribution is: **to show how declared post-establishment interaction states can produce different response architectures under a common broad perturbation, while leaving the origins of the Chapter 1 regional patterns unresolved.**
