# Direct dependency pilot status

## Current state

`implementation_ready_field_data_missing`

The direct effective-pollinator dependency gap is no longer a missing-method problem. The branch now contains a linked field protocol, schemas, validators, audit code, output guards, pilot-dispersion summaries, and precision-driven replication planning.

What is **not** yet present is empirical pilot data from the same tagged Izu populations.

## Implemented chain

```text
registered plant / flower
    -> usable observation effort
    -> visitor bout + contact
    -> single-visit pollen deposition (SVD)
    -> rate-weighted effective pollen service
    -> open / bagged-autonomous / supplemental-outcross treatment
    -> fruit / mature seed / optional parentage
```

The official output masks background-adjusted SVD, effective pollen delivery and service share if the visitor group lacks a no-visit SVD control.

## Pilot-to-confirmatory transition

No universal sample size is locked.

```text
pilot data from multiple independent plants
    -> plant-level SVD and treatment dispersion
    -> lock biologically meaningful absolute CI half-width
    -> approximate independent-plant replication
    -> hierarchical/site/time design stress test
    -> confirmatory field lock
```

Flowers and SVD events within one plant are subsamples, not independent `n`.

A draft precision goal produces no sample-size recommendation. Only a goal explicitly marked `locked` is converted to an approximate independent-plant count.

## Pilot priority

1. *Campanula microdonta* is the focal anchor because it contains the strongest historical autonomous-reproduction breakpoint while matched contemporary effective dependency remains unmeasured.
2. Functional controls/comparators are not preassigned from floral form; they must be phenologically feasible and supported by direct interaction/reproductive evidence.
3. A high-dependency endpoint is admitted only after direct effective-pollinator evidence or an external prespecified calibration.

Pilot feasibility does not solve geographic identification: repeated plants at one Oshima site are still one bridge-state geographic unit.

## Files

- `docs/EFFECTIVE_POLLINATOR_DEPENDENCY_FIELD_PROTOCOL.md`
- `data/design/effective_pollinator_dependency_field_readiness.json`
- `data/design/effective_dependency_pilot_field_priority.json`
- `channel_id/effective_pollinator_dependency.py`
- `channel_id/effective_dependency_output.py`
- `channel_id/effective_dependency_precision.py`
- `scripts/audit_effective_pollinator_dependency.py`
- `scripts/plan_effective_dependency_pilot_precision.py`
- `templates/field_dependency_plant_registry_template.csv`
- `templates/field_single_visit_pollen_deposition_template.csv`
- `templates/field_pollination_treatment_template.csv`
- `templates/effective_dependency_precision_goals_template.csv`

## Claim boundary

This implementation can support contemporary per-visit effectiveness, sampled rate-weighted service, and reproductive-dependence estimates once data exist. It does not itself identify historical Bombus loss, historical selection, self-compatibility, realized selfing, or a causal Oshima–Toshima boundary effect.
