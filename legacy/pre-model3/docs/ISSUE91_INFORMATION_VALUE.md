# Issue #91 field effort: gate first, information value second

## Current state

The repository status remains `implementation_ready_field_data_missing`. Therefore the current priority is **not** an information-theoretic choice among optional measurements. The mandatory linked pilot channels have not yet been collected.

Current collection order remains:

1. stable plant/flower IDs plus observation-effort denominator;
2. no-visit SVD controls;
3. controlled SVD on at least two independent plants for one relevant visitor group;
4. open, bagged-autonomous, and supplemental-outcross terminal outcomes on at least two independent plants each;
5. terminal fruit/seed linkage and explicit loss/damage/pending states;
6. parentage only as an optional downstream layer.

This order is inherited from `data/design/effective_dependency_pilot_field_priority.json` and is not changed by the causal-identifiability port.

## Two-stage rule

`channel_id/issue91_information_value.py` enforces:

```text
missing mandatory gate
    > any optional/marginal replication

all mandatory gates satisfied
    -> rank marginal options by expected causal resolvability gain / declared cost
```

The second stage uses the RACH-style `expected_observation_value` function added in PR #215. Candidate outcome probabilities must be declared before using the ranking and are planning assumptions, not empirical probabilities.

## Why this matters

Without the gate-first rule, a high-scoring optional observation could incorrectly outrank a missing no-visit SVD control or a missing core reproductive treatment. That would create a numerically attractive but scientifically unusable pilot.

The information-value layer is therefore a **marginal effort allocator**, not a replacement for the field protocol.

## Current actionable ranking

Because no real linked field bundle is committed, the present ranking is deterministic from gate status:

```text
Tier 1: complete missing linked pilot channels and dispersion-estimability minima
Tier 2: only after Tier 1 passes, compare extra independent plants / extra calibration / optional parentage by declared information gain and cost
```

At present, adding repeated flowers within an already represented plant must not outrank adding a new independent plant needed to make SVD or treatment dispersion estimable.

## Claim boundary

This ranking does not estimate empirical power, natural-cause probabilities, historical Bombus loss, or a causal Oshima-Toshima boundary. It only orders field effort under the declared Issue #91 design and causal grammar.
