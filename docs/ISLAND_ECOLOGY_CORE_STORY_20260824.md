# Island ecology core story

## Primary question

**Why does island-associated simplification or reorganization of pollinator function not produce one universal plant response?**

The primary paper is an island-ecology study. The ABM is used to ask whether a common decline/reorganization in pollinator functional opportunity can generate the diversity of response states seen across island plant–pollinator systems without fitting a different mechanism to every island.

## Core ecological claim

A common functional perturbation does **not** imply a common downstream response. In the frozen ABM, plant lineages can branch into opposite reproductive responses because they enter the same pollinator-environment shift from different pre-existing positions in functional trait space. Downstream interaction context then changes which branch a lineage occupies, while reproductive assurance mainly changes the magnitude of propagation.

The ecological synthesis is therefore:

```text
island-associated pollinator functional simplification / reorganization
        |
        v
lineage-specific starting functional state
        |
        +--> response branching: positive / negative / same-direction states
        |
        v
local interaction context / partner structure
        |
        +--> branch reallocation, occasional rescue, occasional worsening
        |
        v
reproductive filters such as autonomous assurance
        |
        +--> attenuation of decline magnitude more often than sign reversal
```

This supports a **state-dependent island-response view**, not a single universal post-establishment island syndrome.

## What the simulations establish

### 1. Pre-existing lineage state generates branching

In the original residual block, mixed-sign branching occurred in 0.4167 of matched runs and disappeared when initial trait-position heterogeneity was removed. The same boundary replicated in the independent seed block: full mixed-sign frequency = 0.4167; initial-trait-OFF = 0.0. Other tested residual single-factor removals retained branching.

Within the declared ABM, pre-existing lineage functional position is therefore the minimal identified generator of within-run response-sign branching.

### 2. Local network context decides where lineages go, not whether branching exists

Removing local support changed 105/288 paired lineage response signs, compared with 13/288 for partner effectiveness. Yet branching remained possible without these downstream modifiers.

An independent network-context block produced:

- sign rescue: 16/96;
- magnitude attenuation: 85/96;
- worsening: 11/96.

Network context is therefore not a universal protective buffer. It is a **context-dependent branch allocator with buffering capacity**.

### 3. Autonomous assurance mostly dampens propagation

Autonomous assurance attenuated 207/216 declines in the independent block but generated 0/216 sign rescues. A broadened envelope also produced 0/525 strong sign rescues.

Thus assurance is best interpreted as a **magnitude attenuator**, not a robust sign-reversing buffer.

## What the cross-island comparison adds

The external programme screened 54 geographic/system units and retained 13 strict island-system challenges:

- branching: 3;
- same-direction propagation: 6;
- buffering / alternative: 2;
- reproductive-axis decoupling: 1;
- retained falsification: 1.

All 11 generative challenges were covered or sign-compatible with state classes already present in the frozen ABM. This does **not** mean that one empirical mechanism explains all 11 systems. It means that the observed diversity of island responses is consistent with a common ecological architecture in which response depends on starting state and downstream context.

Guaiacum remains an axis-decoupling constraint rather than whole-reproduction buffering. Dominica Heliconia remains a failed frozen signed-position projection and is not retuned.

## Relation to the classic island syndrome idea

Broad island syndromes and lineage-level response branching are not mutually exclusive. Macroecological island patterns can reflect colonization/establishment filtering, differential persistence and repeated ecological responses accumulated across lineages. The present study addresses the **post-establishment response problem**: given a change in pollinator function, why do established lineages not all move in the same direction?

The answer supported by the frozen model is that the effect of island-associated biotic simplification is conditional on the lineage's existing functional state and the interaction context through which the perturbation propagates.

Therefore the paper should not claim that island syndromes are false. It should claim that **an aggregate island syndrome does not imply a universal within-lineage trajectory**.

## Role of state separability

State-separability analysis remains useful, but it is no longer the paper's primary novelty. Its role is a guard on ecological interpretation:

- mixed-sign branching is informative when present but not required whenever functional heterogeneity exists;
- same-direction response does not imply uniform starting states;
- attenuation alone cannot distinguish network buffering from reproductive assurance;
- qualitative external state compatibility cannot identify the real-world causal mechanism.

These points belong after the ecological results, mainly as an inference boundary and Supplementary methodological layer.

## Main-paper order

1. **Island ecological problem:** similar pollinator simplification can lead to different plant outcomes.
2. **Synthetic result:** a single frozen ABM generates branching, propagation and buffering states without island-specific retuning.
3. **Mechanistic decomposition:** initial functional position generates branching; local context reallocates it; assurance attenuates propagation.
4. **Cross-island challenge:** the same response-state diversity recurs across independent island systems.
5. **Ecological synthesis:** island responses are state-dependent and context-dependent rather than a universal post-establishment trajectory.
6. **Inference boundary:** state compatibility is not empirical causal identification; Guaiacum and Dominica remain protected constraints/failures.

## Working title

**One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification**

Alternative:

**Why do island plants diverge under pollinator simplification? Functional starting state predicts branching, while local context governs propagation**
