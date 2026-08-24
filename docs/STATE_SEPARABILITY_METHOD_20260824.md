# Frozen state-separability analysis for agent-based ecological models

## Purpose

This document extracts the reusable methodological component from the island plant–pollinator test case.

The problem is simple but often hidden:

> **A model being able to generate an observed state is not the same as the observed state identifying the mechanism that generated it.**

A flexible ABM may produce the same macroscopic state under several mechanism settings. Conversely, a mechanism may be necessary for a state but the state may appear only in a subset of stochastic runs. Frozen state-separability analysis treats the model's own interventions as a diagnostic experiment.

## Inputs

The method requires:

1. a frozen simulation model `M`;
2. a state classifier `C` defined before the external challenge being evaluated;
3. at least one declared mechanism intervention with a **present** and **absent/alternative** condition;
4. matched or otherwise comparable stochastic runs under those conditions;
5. optionally, an external challenge set that is not used to tune the model.

The state classifier may be binary, categorical, or derived from a continuous response. The current island example uses binary events such as `mixed_sign_branching` and `strong_sign_rescue`.

## Step 1 — Freeze the forward state vocabulary

Before inspecting held-out external outcomes, define the states the model already generates and the zero/directional boundaries used to distinguish them.

Examples from the island test case:

- mixed-sign branching;
- same-direction response;
- strong sign rescue;
- magnitude attenuation;
- worsening.

Do not add a new state label after seeing an external case unless that case is first recorded as a state-space miss.

## Step 2 — Define intervention contrasts

For each candidate mechanism, define the intervention that represents mechanism presence and the intervention that represents absence or a declared alternative.

Examples:

| observable state | mechanism-present intervention | absent/alternative intervention |
|---|---|---|
| mixed-sign branching | initial trait heterogeneity ON | initial trait heterogeneity OFF |
| same-direction response as evidence of uniformity | trait uniformity | trait heterogeneity ON |
| strong sign rescue | network context/support ON | tested autonomous-assurance route |
| magnitude attenuation | assurance route ON | network-context route |

These comparisons are conditional on the declared model family. They do not imply that the absent/alternative intervention exhausts all mechanisms in nature.

## Step 3 — Estimate forward and inverse frequencies

For an observable state `S` and mechanism contrast `M=1` versus `M=0`, estimate:

\[
\mathrm{sensitivity} = P(S=1\mid M=1)
\]

and

\[
\mathrm{FPR} = P(S=1\mid M=0).
\]

Then:

\[
\mathrm{specificity}=1-\mathrm{FPR}
\]

and

\[
\mathrm{FNR}=1-\mathrm{sensitivity}.
\]

The reusable implementation is `channel_id/state_separability.py`.

When event counts are retained, use `StateDiagnostic`. When only already-frozen aggregate frequencies exist, use `diagnostic_from_frequencies`.

## Step 4 — Interpret diagnostic asymmetry

Four qualitatively different outcomes are possible.

### High sensitivity, high specificity

The state is both commonly expressed when the mechanism is present and uncommon when it is absent. It is a strong synthetic diagnostic within the tested mechanism family.

### Low sensitivity, high specificity

The state is informative when observed, but failure to observe it does not exclude the mechanism.

The island example's mixed-sign branching and strong network sign rescue occupy this class.

### High sensitivity, low specificity

The state is commonly produced by the candidate mechanism but also by alternatives. It is a weak inverse diagnostic despite strong forward coverage.

Magnitude attenuation in the island example is close to this situation.

### Low sensitivity, low specificity

The state does little to distinguish the tested mechanisms.

## Step 5 — Replicate the strongest intervention boundary independently

If one intervention supplies the central causal claim, freeze an independent stochastic block before running it:

- seed or seed-generation rule;
- parameter envelope;
- replicate count;
- state classifier;
- decision rule;
- stop rule.

Accept the first scientific result from that block. Do not search additional seeds until the preferred state frequency appears.

The island test case independently replicated the collapse of within-run branching after initial trait heterogeneity was removed.

## Step 6 — Challenge the frozen state space externally

External systems can then be used as held-out qualitative or quantitative challenges. They must not retroactively choose the intervention, classifier or model parameters used in the primary state-separability analysis.

Keep three outcomes distinct:

1. **state covered** — the frozen model already generates the state;
2. **mechanism identified** — stronger evidence links the real system to a model mechanism;
3. **state-space miss / prediction failure** — the frozen state or signed prediction does not cover the held-out case.

The first does not imply the second.

## Step 7 — Protect failures

A useful ABM validation framework needs explicit failure rules. Examples:

- a state still occurs after removal of the claimed necessary mechanism;
- a proposed universal buffer worsens any matched decline;
- a strong-buffer route fails to reproduce sign rescue in an independent block;
- an external signed prediction is counterdirectional;
- a future external state lies outside every frozen state class.

Record these before model extension. Otherwise model flexibility can absorb almost any external observation.

## Minimal reusable API example

```python
from channel_id.state_separability import StateDiagnostic

mixed_sign = StateDiagnostic(
    state="mixed_sign_branching",
    mechanism_present="initial_trait_heterogeneity_on",
    mechanism_absent_or_alternative="initial_trait_heterogeneity_off",
    present_state_events=5,
    present_total=12,
    absent_state_events=0,
    absent_total=12,
)

print(mixed_sign.sensitivity)         # 0.4167
print(mixed_sign.specificity)         # 1.0
print(mixed_sign.false_negative_rate) # 0.5833
```

The numerical values are test-case specific. The reusable object is the intervention-to-diagnostic transformation.

## Relationship to pattern-oriented modelling

Pattern-oriented modelling (POM) already provides a framework for using multiple empirical patterns to constrain bottom-up models and reduce equifinality. Frozen state-separability analysis is intended as a narrower extension, not a replacement for POM.

Its additional question is:

> **Given a model intervention and an observable state, how informative is that state about the intervention-defined mechanism?**

Thus the workflow connects:

```text
forward state generation
    ↓
mechanism intervention / ablation
    ↓
state diagnostic sensitivity + specificity
    ↓
independent robustness
    ↓
held-out external challenge
    ↓
protected falsification / state-space miss
```

## Claim boundary

The resulting sensitivity and specificity are **conditional synthetic frequencies**. They describe observability and separability inside the declared simulation family. They are not population-level diagnostic accuracies for natural ecosystems unless a separate empirical transport argument is supplied.

That boundary is part of the method rather than a limitation to be removed after fitting.
