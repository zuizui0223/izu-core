# Constraint-mediated pollination ABM v10: effective service × dependency

## Scientific purpose

v10 asks a narrower question than a new all-purpose island model:

> After the fixed-visit-budget correction and the v9 local plant/pollinator/pair-support hierarchy are in place, can partner-specific effectiveness change which downstream reproductive branch a lineage occupies, while upstream interaction opportunity is held fixed?

This is the missing integration between the network-architecture programme (v4–v9) and the lineage dependency/assurance programme (v2–v4).

## Why partner effectiveness can be retested after the v3 failure

v3 already tested broad partner-level service quality and failed: it produced fewer positive lineage responses than v2 and remained strongly decline-biased. That result is preserved as `partner_service_quality_heterogeneity_alone_is_insufficient`.

The v3 model, however, still used the old many-partner accumulation rule. v4 subsequently showed that pollinator richness must not automatically become more visitation opportunity and replaced that rule with a fixed visit budget. v5–v9 then separated island-scale opportunity from local plant availability, local pollinator availability, pair support and within-support weights.

Therefore v10 does **not** tune or erase v3. It performs a new interaction test:

```text
v9 opportunity/support hierarchy
        ↓
existing pair opportunity weights
        ×
partner-specific effectiveness
        ↓
effective pollen-service proxy
        ×
lineage pollinator dependency
        +
reproductive assurance
        ↓
reproductive response branch
```

## Frozen mechanism

### Upstream

Unchanged v9:

1. v4 continuous island-scale opportunity;
2. local plant/resource availability;
3. local pollinator availability;
4. pair support;
5. v5 within-support weight realization.

### Partner effectiveness

The quality layer multiplies **existing positive pair weights only**. It cannot create a plant, pollinator or pair.

The full probe is the already-used v3 broad range:

```text
quality = 1 + U(-0.8, 0.8)
```

so quality lies in `[0.2, 1.8]`. The distribution does not depend on geography, island identity, native/introduced labels, or empirical outcome.

`quality_strength = 0` is an exact ablation: all multipliers equal 1.

### Fixed visit budget

For a plant row, v9 weights are treated as the existing opportunity/service budget. Partner quality changes its composition-weighted service score, which then passes through one saturating transform. Pollinator richness is never added as an extra visit-frequency term.

### Plant response filter

Lineage templates reuse the v4 ranges for:

- `pollinator_dependency`;
- `assurance_ceiling`;
- `assurance_responsiveness`.

Assurance follows the v4 update rule: it increases only when reproduction is below 0.5 and is capped by the lineage-specific ceiling.

## Matched ablation

For every synthetic geography/network/context, v10 evaluates:

- quality OFF;
- quality ON.

The local plant/pollinator/pair realization and within-support opportunity weights are identical between these two evaluations. Consequently, any changed reproductive contrast or sign flip is downstream of the effectiveness layer rather than a changed network.

The implementation asserts this invariant directly.

## What is tested

The synthetic run reports:

1. the fraction of lineage contrasts with lower oceanic interaction opportunity;
2. positive/negative reproductive responses with quality OFF;
3. positive/negative reproductive responses with quality ON;
4. mixed-sign configurations;
5. matched lineage response-sign flips caused by the quality layer;
6. whether quality expands the positive-response tail or instead only changes branch identity/magnitude.

No Izu frequency is a target. In particular, the known 8/8 matching decline and 4/4 pollen split are not loaded by the model.

## Decision classes

- `v10_partner_effectiveness_interacts_with_v9_to_broaden_downstream_branching`
- `v10_partner_effectiveness_changes_branch_identity_without_broadening_positive_tail`
- `v10_quality_layer_changes_magnitude_but_not_response_branch_identity`
- `v10_invalid_quality_layer_changes_upstream_opportunity`

The first three are scientific outcomes. Only the last is an implementation-invalid state.

A scientific failure is not converted into a CI failure.

## Interpretation boundary

v10 is a mechanistic sufficiency/interaction test, not empirical causal identification. Network opportunity weights are not SVD or direct reproductive dependency. The known Izu outcome pattern may be used later as retrodictive context but cannot become a calibration target after it has already informed model development.

The next real confirmation must use a new independent island system with compatible, source-locked effective-service and reproductive outcomes frozen before inspection.
