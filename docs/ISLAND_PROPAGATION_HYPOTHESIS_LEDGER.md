# Island propagation hypothesis ledger

Updated: 2026-08-22

## Current decision

The programme should no longer use a simple universal cascade as its central hypothesis:

```text
pollinator functional deterioration
    -> lower interaction quality
    -> lower reproduction
    -> one directional floral response
```

That universal reading is incompatible with the current real-data matrix.

The strongest remaining synthesis is instead:

```text
pollinator-functional change
        ↓
pre-existing functional position creates branch potential
        ↓
local support / partner effectiveness reallocate realised interaction quality
        ↓
plant-side propagation or buffering gate
        ↓
reproductive and floral response may decline, increase, remain buffered,
branch among lineages, or run counter to a simple directional prediction
```

This is a testable architecture, not a proven universal causal graph.

## What has been rejected

### U1. Universal same-direction island cascade — rejected

A universal rule requires every admissible case to follow the same sign. The programme already contains multiple counterexamples.

- **Izu:** corrected matching is lower across all eight shared targets, but pollen receipt is split 4 lower / 4 higher and tube morphology is 3 shorter / 4 longer / 1 equal.
- **Puerto Rico–Mona *Guaiacum*:** pollinator assemblage and visitation differ strongly, while the reported self/outcross breeding-system index is similar and autogamy is negligible.
- **Hawaiian lobelioids 2026:** signed bill–flower matching predicts pollen contact and nectar robbing, and experimental damage changes nectar replenishment, but fruit and seed performance remain high.
- **California Channel Islands *Nicotiana*:** greater island selfing capacity and longer corollas coexist with no detected current island decline in visitation or pollen transfer and no general island pollen limitation.
- **Dominica *Heliconia*:** the first frozen negative signed-position-to-selection prediction ran in the opposite direction.

These observations do **not** tell us the prevalence of each branch. They are sufficient to reject a universal one-way law.

### U2. Partner effectiveness alone generates the branching — rejected as sufficient

ABM v10 used matched upstream networks and switched partner-quality heterogeneity ON/OFF.

- 501/648 lineage reproductive contrasts changed in magnitude;
- 17 lineage contrasts changed sign;
- positive responses changed only 151 → 150;
- mixed-sign configurations remained 18 → 18.

Therefore partner effectiveness can change **which branch a lineage occupies**, but it does not create the aggregate branching breadth by itself.

Hawaii supplies the matching empirical warning: interaction quality/resource consequences can change without forcing the final reproductive sign.

### U3. Dependency heterogeneity is necessary for branching — rejected as necessary in the declared ABM

The v11 factorial test retains two-sided response branching even with local-support variation, dependency heterogeneity, adaptive assurance and partner effectiveness all OFF.

This does not make reproductive dependency irrelevant. It remains a plausible **propagation filter** and is the major empirical target of Issue #91. It means only that dependency heterogeneity is not the minimal branch generator in the declared model.

### U4. Initial signed position universally predicts downstream direction — rejected as universal

v12 identifies initial functional trait position as the minimal synthetic generator of within-environment branch signs. That is a mechanism-capability result.

The first frozen real-data projection in Dominica then failed its declared negative direction. Therefore initial position can remain a branch-potential variable, but it cannot be promoted to a universal direction law.

## What remains live

### S1. State-dependent propagation architecture — best current synthesis

The current synthesis is supported from several directions:

1. Izu supplies the clearest real pattern of common-ish upstream change with divergent downstream response.
2. v4 reproduces that qualitative structure without fitting the empirical 8/8 or 4/4 frequencies.
3. v10 shows that effectiveness reallocates branches rather than generating all branching.
4. v11 shows the four tested downstream heterogeneity terms are not individually necessary for branch generation.
5. v12 isolates initial functional position as a minimal synthetic branch generator, while Dominica prevents universalising its direction.
6. Hawaii independently connects a source-native signed position to interaction quality and then shows a separate reproductive-resilience boundary.
7. Guaiacum and Nicotiana supply additional cases where upstream/current interaction conditions do not map one-to-one onto final reproductive or trait response.

The missing proof is very specific: an independent transition that measures **signed functional position + direct effectiveness + controlled reproductive dependency + terminal reproductive outcome** at the same matched unit.

### S2. Reproductive buffering gate — empirically supported, identity unresolved

Hawaii, Nicotiana and Guaiacum all support the existence of a boundary at which upstream or interaction-quality change need not become reproductive collapse.

But these systems do not demonstrate one common buffering variable. Candidate processes include autonomous reproductive assurance, resource compensation, lineage functional position, colonisation/establishment filtering and other plant-side constraints. They must not be collapsed into one fitted `buffering` parameter before a source can distinguish them.

## Consequence for the research design

The next field/literature target is no longer “another island showing pollinator decline.” It is a **discriminating bridge** that tells us why propagation continues in one lineage and stops in another.

Priority measurement chain:

```text
source-native functional position
        -> direct visitor effectiveness / effective service
        -> controlled reproductive dependency or assurance
        -> terminal fruit / seed response
```

Issue #91 remains the direct Izu version of that test. External work should remain source-triggered and prioritize the same missing bridge rather than accumulate more disconnected island examples.

## Novelty boundary

The novelty is **not** that floral traits match pollinator traits, that island pollinator communities differ, or that reproductive assurance can evolve; those ideas already have direct precedents.

The stronger contribution now is the combined programme:

- identify a recurrent common-upstream / divergent-downstream pattern across island systems;
- preserve counterexamples rather than force one island syndrome;
- use held-out and prospectively frozen ABM tests to distinguish branch generation from branch reallocation;
- identify propagation/buffering boundaries where interaction change fails to become reproductive decline;
- let failed predictions (especially Dominica) constrain the mechanism rather than retuning them away.

## Claim boundary

This ledger rejects only the universal claims as stated. It does not estimate branch prevalence, identify a common buffering coefficient, establish historical pollinator-loss causation, or prove the current state-dependent propagation graph. The surviving architecture remains a falsifiable synthesis awaiting a matched empirical end-to-end bridge.
