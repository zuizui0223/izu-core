# Izu prediction-locked regime-transition programme (`paper/`)

This directory tests whether independent Izu plant lineages show repeatable
response shapes at predeclared pollinator-regime boundaries. It is not currently
a completed multi-species meta-analysis.

## Current decision

```text
focal_three_channel_calibration_established_independent_holdout_blocked
```

The adopted *Campanula microdonta* calibration contains three source-locked
channels only:

| channel | retained shape | current evidence |
|---|---|---|
| floral size | continuous erosion | source locked |
| multilocus outcrossing | continuous erosion | source locked |
| autonomous reproductive capacity | second-transition step | source locked |

Nectar-guide and visible-signal analyses are excluded from the current evidence
state. They contribute no adopted direction, breakpoint, or effect estimate.

The independent positive specialist holdout remains absent. Current cross-lineage
evidence comprises one usable open-generalist negative-control lineage, zero
source-locked quantitative effect rows in the extraction table, and zero ROI
operators released to the broad specialist photo holdout.

Generate the authoritative status report before interpreting older pilot output:

```bash
python scripts/report_current_evidence_state.py \
  --markdown-out artifacts/current_evidence_state.md \
  --json-out artifacts/current_evidence_state.json
python paper/validate_regime_transition_registry.py
```

See [`../docs/CURRENT_EVIDENCE_STATE.md`](../docs/CURRENT_EVIDENCE_STATE.md) and
[`../docs/REGIME_TRANSITION_COMPARATIVE_DESIGN.md`](../docs/REGIME_TRANSITION_COMPARATIVE_DESIGN.md).

## Competing response shapes

Each eligible lineage-response unit may compare:

```text
none
cline
first_step
second_step
two_step
environment_history
```

The goal is not to force all traits into the same island syndrome. A lineage may
show a smooth morphological cline, a discrete mating-system transition, a binary
state change, ecological filtering in occupancy, or no ordered response.

## Response domains

| domain | examples | model family |
|---|---|---|
| quantitative trait | size, outcrossing, bagged set | continuous/count/proportion |
| binary or ordinal state | SI/SC, autonomous capacity, accessibility | Bernoulli/ordinal/multistate |
| effective interaction | guild breadth, legitimate-contact link | count/binary/network with effort |
| occupancy | species present/absent by island | detection-aware occupancy |

These domains share a response-shape vocabulary but not an effect-size scale.
They must not be pooled as though presence/absence were a noisy flower-size value.

## Generalist falsification

Open-generalist lineages are negative controls for a **shared specialist-specific
breakpoint**, not a claim that all generalist traits must equal zero. The intended
moderator test is a dependency-class by boundary interaction, with environment,
history, observation effort, lineage, and phylogeny handled explicitly.

## Workstreams

| Workstream | Main files | Scientific role |
|---|---|---|
| Current claim/readiness state | `channel_id/current_evidence_state.py`, `scripts/report_current_evidence_state.py` | excludes unfinished analyses and prevents pilot output becoming evidence |
| Regime-transition registry | `data/predictive_meta/regime_transition_registry.csv`, `validate_regime_transition_registry.py` | fixes response domain, observation unit, dependency class, regime coverage, and allowed models |
| Focal calibration | `data/inoue_literature_island_traits.csv`, `campanula_channel_shape_v1.csv` | supplies three calibration channels; never an independent holdout replicate |
| Prospective prediction contract | `data/predictive_meta/two_breakpoint_prediction_contract.csv` | locks scenario directions before independent data are scored |
| Source-native recovery | `primary_source_extraction_queue.csv`, `primary_source_native_evidence.csv` | recovers direct tables and preserves exclusions/context without inventing effects |
| Quantitative effect gate | `paper/evidence_screening/quantitative_effects.csv`, `validate_quantitative_effects.py` | admits numeric effects only with source location, units, n, uncertainty, taxonomy, and geography |
| Generalist negative control | `generalist_negative_control_card_ledger.csv` | tests whether the observation process manufactures a shared breakpoint |
| Image-operator falsification | `roi_dual_control_result_20260710.csv` | blocks operators that are insensitive or create regional differences |
| Environment/history competitor | joint profile and source-level likelihood modules | remains a first-class alternative to regime steps |
| Detectability simulation | `comprehensive_sweep.py` and related modules | plans sampling; does not establish a field mechanism |

## Presence/absence boundary

Occurrence can support a separate ecological-filtering question: do mainland
specialist-like plants cross the second regime boundary less often than open
generalists after area, isolation, climate, history, and observation effort are
controlled? It cannot show that an extant island population evolved a floral or
mating-system trait.

## Immediate evidence work

1. Recover original population tables, n, uncertainty, and locality mapping for
   *Weigela coraeensis* and *Ligustrum ovalifolium*.
2. Expand the registry with source-native SI/SC, autonomous-reproduction,
   flower-size, accessibility, effective-guild, and occupancy channels.
3. Implement the explicit climate, area, isolation, and history competitor.
4. Keep the public-photo specialist route closed until an independent biological
   positive control validates the observation operator.
5. Start hierarchical synthesis only after independent lineages supply compatible
   native-scale observations.
6. Keep every nectar-guide result outside current evidence until a final dataset
   and analysis are explicitly declared.

## Evidence boundary

Occurrence is availability or occupancy evidence, not a floral trait. Visitor
identity is not pollinator effectiveness. Bagged capsule set is autonomous
reproductive capacity, not realised selfing. SC is not synonymous with autonomous
selfing. Simulation recovery is not historical reconstruction. Calibration is not
independent replication.
