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

## Hypothesis recovery

### H1 — universal post-establishment response

**Prediction:** one common island-like pollinator perturbation should produce one common downstream response direction.

**Outcome:** rejected. Mixed-sign branching occurs in 0.4167 of matched runs in both the original and independently seeded blocks. A common perturbation therefore does not imply one lineage trajectory.

This rejection applies to post-establishment response. It does not reject aggregate island syndromes generated through colonization, establishment or persistence filtering.

### H2 — state-dependent branching

**Prediction:** pre-existing lineage functional position generates within-environment response branching.

**Outcome:** supported inside the declared ABM and independently replicated. Removing initial trait-position heterogeneity changes mixed-sign frequency from 0.4167 to 0 in both frozen blocks; other tested residual single-factor removals retain branching.

The identified coordinate is synthetic and relative. It is not automatically corolla length, flower area, colour, nectar guide or another named empirical trait.

### H3 — context-dependent branch allocation

**Prediction:** local interaction context changes which response branch a lineage occupies and can buffer some declines.

**Outcome:** supported, but not monotonically. Removing local support changes 105/288 paired lineage signs. In the independent network-context block, support produces 16/96 sign rescues and 85/96 magnitude rescues, but 11/96 worsenings.

Network context is therefore a **bidirectional branch allocator with buffering capacity**, not a universal protective buffer.

### H4 — autonomous-assurance buffering

**Prediction:** autonomous reproductive assurance reduces the downstream reproductive effect of service decline; a stronger version predicts sign reversal.

**Outcome:** partially supported and narrowed. Assurance attenuates 207/216 independent declines but produces 0/216 sign rescues, with 0/525 sign rescues in the broadened envelope.

The stable conclusion is **magnitude attenuation**, not robust sign-reversing rescue.

### H5 — cross-island recurrence of response architecture

**Prediction:** if the state-dependent architecture is ecologically relevant beyond the focal model, independent island systems should repeatedly occupy branching, same-direction propagation and buffering/alternative states without system-specific retuning.

**Outcome:** supported at the qualitative state level. The strict external set contains 13 systems: three branching, six same-direction propagation, two buffering/alternative, one reproductive-axis-decoupling constraint and one retained falsification. All 11 generative challenges are covered or sign-compatible with state classes already present before external inspection.

This supports recurrence of the **response architecture**, not one shared empirical mechanism across all systems.

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

The 13-system strict set is a **challenge set**, not a random prevalence sample. Its state counts must not be interpreted as estimates of how common each response class is globally.

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

These points belong after the ecological results, mainly as an inference boundary and Supplementary methodological layer. The current method-first Discussion heading `The inverse problem is the main methodological result` must not survive in the primary island-ecology manuscript.

## Unresolved but non-blocking future tests

Three unresolved branches are worth preserving as the direct next research programme, but none is required for submission of this paper.

1. **Real signed functional starting position:** identify a source-native plant trait and pollinator functional center, freeze the signed mapping before downstream outcomes, and test whether it predicts branch direction.
2. **Real network-context mechanism:** directly link local partner context to rate-weighted effective service and reproductive response in a matched transition.
3. **Complete external causal bridge:** recover one independent system linking pollinator functional change -> effective service -> dependency/assurance -> downstream response on compatible units.

Do not replace these missing empirical links with visitor identity, richness, body-size proxies or post-hoc trait labels.

## Main-paper order

1. **Island ecological problem / H1:** similar pollinator simplification can lead to different plant outcomes; reject a universal post-establishment trajectory.
2. **H2 branch generator:** initial functional position generates branch potential and replicates independently.
3. **H3/H4 propagation:** local context reallocates branches; assurance mainly attenuates magnitude.
4. **H5 cross-island challenge:** the same response-state diversity recurs across independent island systems.
5. **Ecological synthesis:** aggregate island syndromes can coexist with lineage-level state dependence and context dependence.
6. **Inference boundary and future tests:** state compatibility is not empirical causal identification; preserve Guaiacum, Dominica and the three unresolved empirical translation tests.

## Working title

**One perturbation, multiple island responses: state-dependent branching under pollinator functional simplification**

Alternative:

**Why do island plants diverge under pollinator simplification? Functional starting state shapes branching, while local context shapes propagation**
