# Izu prediction-locked comparative programme (`paper/`)

This directory tests whether the response calibrated in *Campanula microdonta*
can be evaluated prospectively in independent Izu lineages. It is not currently
a completed multi-species meta-analysis.

## Current decision

The machine-generated evidence state is:

```text
focal_calibration_established_independent_holdout_blocked
```

The focal calibration has four retained channels:

| channel | retained shape | current evidence |
|---|---|---|
| floral size | continuous erosion | source locked |
| multilocus outcrossing | continuous erosion | source locked |
| autonomous reproductive capacity | second-transition step | source locked |
| guide / visible signal | second-transition decline | measured 300-DPI scan summary |

The independent positive specialist holdout remains absent. The current
cross-lineage evidence is one usable open-generalist negative-control lineage,
zero source-locked quantitative effect rows in the extraction table, and zero
ROI proposals released to the broad specialist holdout.

Generate the authoritative status report before interpreting older pilot output:

```bash
python scripts/report_current_evidence_state.py \
  --markdown-out artifacts/current_evidence_state.md \
  --json-out artifacts/current_evidence_state.json
```

The committed copy is [`../docs/CURRENT_EVIDENCE_STATE.md`](../docs/CURRENT_EVIDENCE_STATE.md).

## Reproduce the offline programme

```bash
pip install -e '.[dev]'
python scripts/report_current_evidence_state.py
python paper/run_all.py
python -m pytest
```

`paper/run_all.py` is a consolidated diagnostic runner. Its simulation and
rank-weighted pilot stages are planning/audit layers; they do not create
independent empirical lineages.

## Workstreams

| Workstream | Main files | Scientific role |
|---|---|---|
| Current claim/readiness state | `channel_id/current_evidence_state.py`, `scripts/report_current_evidence_state.py` | prevents pilot, discovery, and failed image routes from being reported as completed evidence |
| Focal calibration | `data/inoue_literature_island_traits.csv`, `data/predictive_meta/campanula_channel_shape_v1_1.csv`, `campanula_guide_scan_summary.csv` | fixes the observed Campanula channel shapes and the measured guide direction |
| Prospective prediction contract | `data/predictive_meta/two_breakpoint_prediction_contract.csv` | locks scenario directions before independent holdout data are scored |
| Source-native recovery | `data/predictive_meta/primary_source_extraction_queue.csv`, `primary_source_native_evidence.csv` | recovers direct tables and preserves exclusions/context without inventing effects |
| Quantitative effect gate | `paper/evidence_screening/quantitative_effects.csv`, `validate_quantitative_effects.py` | admits numeric effects only with source location, units, n, uncertainty, taxonomy, and geography |
| Generalist negative control | `generalist_negative_control_card_ledger.csv` | tests false visual thresholds where the specialist response is not predicted |
| Image-operator falsification | `roi_dual_control_result_20260710.csv` | blocks ROI operators that are insensitive or manufacture regional differences |
| Environment/history competitor | joint profile and source-level likelihood modules | remains a first-class alternative; not fully identified by the regime-only scorer |
| Detectability simulation | `comprehensive_sweep.py` and related design modules | estimates what future sampling must measure; not evidence that the field mechanism occurred |

## Current evidence-bearing results

1. The focal response is not one universal cline: morphology and outcrossing are
   retained as continuous erosion, while autonomous reproductive capacity has a
   sharp second-transition step.
2. The standardised flattened-corolla series records 28.39% guide coverage on
   Oshima and a 5.9325% equal-island mean across four no-Bombus islands, a
   -22.4575 percentage-point focal contrast.
3. The simple public-image route failed its negative/positive-control gates and
   remains closed rather than converting ineligible images to zero values.
4. *Ajania pacifica* supplies one flat three-regime generalist control; this is a
   calibration against false positives, not a generalist meta-analytic estimate.
5. The *Lilium* source is retained as an alternative Lepidoptera mechanism and
   excluded from the within-lineage Bombus holdout because variety and geography
   are confounded.

## Immediate evidence work

1. Recover the original population tables, locality mapping, n, and uncertainty
   for *Weigela coraeensis* and *Ligustrum ovalifolium*.
2. Keep the public-photo specialist route closed until an independent biological
   positive control validates the observation operator.
3. Add an explicit climate, island-area, isolation, and history likelihood before
   ranking `environment_only` against pollinator scenarios.
4. Start a cross-lineage synthesis only after independent lineages supply
   compatible source-native effects or validated ordinal holdout contrasts.

## Evidence boundary

Occurrence is availability, not a trait. A visitor name is not pollinator
effectiveness. Bagged capsule set is autonomous reproductive capacity, not
realised selfing. Simulation recovery is not historical reconstruction. A
calibration fit is not an independent replication. Older pilot documents remain
useful audit history, but the generated current evidence state supersedes them
when claims conflict.
