# Direct dependency pilot status

## Current state

`implementation_ready_field_data_missing`

The direct effective-pollinator dependency gap is no longer a missing-method problem. The branch now contains a linked field protocol, schemas, validators, audit code, output guards, pilot-dispersion summaries, precision-driven replication planning, a separate final-estimand reliability gate, and a prospective `dependency × FDQ` design simulation.

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
ordinary focal pilot from multiple independent plants
    -> plant-level SVD and treatment dispersion
    -> empirical coverage + loss / damage / pending summaries
    -> lock biologically meaningful absolute CI half-width
    -> approximate independent-plant replication
    -> hierarchical/site/time design stress test
    -> confirmatory field lock

separate final-estimand calibration
    -> re-estimate the same 0-1 direct dependency estimand
       in independent, non-overlapping plant panels
       for repeated taxon x site x season target units
    -> estimate calibration-scope dependency reliability
    -> separate transportability review
    -> only then consider replacing synthetic dependency_reliability
       in a cross-lineage dependency x FDQ design
```

Flowers and SVD events within one plant are subsamples, not independent `n`.

A draft precision goal produces no sample-size recommendation. Only a goal explicitly marked `locked` is converted to an approximate independent-plant count.

### Reliability boundary

The ordinary Campanula pilot **does not identify** the reliability ratio of the final direct-dependency predictor. Repeated flowers, repeated visits, and between-plant dispersion within one unrepeated target panel mix biological variation with measurement variation. Blinded recounts of the same preserved SVD sample estimate pollen-count technical repeatability only.

The separate reliability gate therefore requires independent repeated estimates of the **final** dependency estimand for the same prespecified taxon × site × season target unit, built from non-overlapping plant panels and distinct frozen source bundles. The mathematical minimum for a variance-component calculation is three target units with at least two eligible repeat blocks each; this is not a confirmatory sample-size recommendation. Even when calibration-scope reliability becomes estimable, it is **not automatically injected** into the cross-lineage FDQ design simulation.

See:

- `data/design/effective_dependency_reliability_calibration.json`
- `templates/effective_dependency_reliability_repeat_template.csv`
- `scripts/audit_effective_dependency_reliability.py`

## Prospective dependency × FDQ result

The existing archive anchors 8 sites, 5 seasons, 9 proxy-eligible taxa and 105 plant × site × season rows, but supplies no direct dependency value and no high-dependency endpoint in the exact target populations.

Under explicitly synthetic interaction, dependency-support and reliability assumptions:

| design | moderate-effect detection |
|---|---:|
| current proxy-like structure | 0.065 |
| proxy + doubled seasons | 0.075 |
| proxy + four sites | 0.085 |
| direct measurement, narrow 9 taxa | 0.125 |
| direct + one high endpoint | 0.248 |
| direct full span, 10 taxa | 0.428 |
| direct narrow span, 16 taxa | 0.213 |
| direct full span, 16 taxa | 0.525 |

These are null-calibrated synthetic design operating characteristics, not empirical power. They imply that additional seasons/sites cannot substitute for directly measuring dependency and extending its support across multiple lineages. A single high endpoint is useful, but intermediate dependency values are also needed so one lineage does not determine the slope.

See:

- `docs/DEPENDENCY_FDQ_DESIGN_SIMULATION.md`
- `data/design/dependency_fdq_design_scenarios.json`
- `data/results/dependency_fdq_design_simulation.json`

## Pilot priority

1. *Campanula microdonta* is the focal anchor because it contains the strongest historical autonomous-reproduction breakpoint while matched contemporary effective dependency remains unmeasured.
2. Functional controls/comparators are not preassigned from floral form; they must be phenologically feasible and supported by direct interaction/reproductive evidence.
3. A high-dependency endpoint is admitted only after direct effective-pollinator evidence or an external prespecified calibration.
4. Confirmatory expansion should distribute directly measured taxa across low, intermediate and high dependency values, rather than adding many taxa inside one narrow survivor range.
5. Non-establishment, hybrid replacement and interaction rewiring remain response modes and potential causes of predictor truncation.

Pilot feasibility does not solve geographic identification: repeated plants at one Oshima site are still one bridge-state geographic unit.

## Files

- `docs/EFFECTIVE_POLLINATOR_DEPENDENCY_FIELD_PROTOCOL.md`
- `docs/DEPENDENCY_FDQ_DESIGN_SIMULATION.md`
- `data/design/effective_pollinator_dependency_field_readiness.json`
- `data/design/effective_dependency_pilot_field_priority.json`
- `data/design/effective_dependency_reliability_calibration.json`
- `data/design/dependency_fdq_design_scenarios.json`
- `data/results/dependency_fdq_design_simulation.json`
- `channel_id/effective_pollinator_dependency.py`
- `channel_id/effective_dependency_output.py`
- `channel_id/effective_dependency_precision.py`
- `channel_id/effective_dependency_reliability.py`
- `channel_id/dependency_fdq_design_simulation.py`
- `scripts/audit_effective_pollinator_dependency.py`
- `scripts/audit_effective_dependency_reliability.py`
- `scripts/plan_effective_dependency_pilot_precision.py`
- `scripts/run_dependency_fdq_design_simulation.py`
- `templates/field_dependency_plant_registry_template.csv`
- `templates/field_single_visit_pollen_deposition_template.csv`
- `templates/field_pollination_treatment_template.csv`
- `templates/effective_dependency_precision_goals_template.csv`
- `templates/effective_dependency_reliability_repeat_template.csv`

## Claim boundary

This implementation can support contemporary per-visit effectiveness, sampled rate-weighted service, and reproductive-dependence estimates once data exist. The ordinary pilot can replace variance/coverage/loss planning assumptions when the relevant data are admitted; it cannot by itself identify final dependency reliability. The design simulation ranks declared synthetic structures only. Neither identifies historical Bombus loss, historical selection, self-compatibility, realized selfing, empirical dependency × FDQ moderation, or a causal Oshima–Toshima boundary effect.
