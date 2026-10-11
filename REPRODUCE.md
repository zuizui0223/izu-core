# Reproducing the current Chapter 2 submission state

The active Chapter 2 paper uses **one nested Model 3**. Older response-geometry / synthetic-`k` analyses are historical legacy provenance under `legacy/model2/`; they are excluded from the current manuscript, Supporting Information and reviewer archive.

## Independent unit and denominator

The prospective isolation bridge contains **24,576 computational cases**, but those cases are **not independent replicates**. The uncertainty-bearing unit is **128 independent visitor-history seeds**. Eight demographic repeats are nested within each history/state/intervention combination and are averaged or retained for repeat-instability diagnostics; they **do not increase the independent history count**.

Mean intervals use **1,999 history-cluster bootstrap resamples**. Mixed-history counts are reported at deadbands `0`, `0.01`, and `0.05` and are descriptive realized labels, not estimates of a stable latent branch prevalence.

## Fast reviewer path

```bash
python -m pip install -e '.[dev]'

pytest -q \
  tests/test_chapter2_mechanistic_funnel.py \
  tests/test_chapter2_model3_submission.py \
  tests/test_chapter2_branch_identifiability_boundary.py \
  tests/test_chapter2_independent_unit_reporting.py \
  tests/test_chapter2_submission_closure_audit.py \
  tests/test_chapter2_unified_model3_figures.py \
  tests/test_repository_artifact_budget.py \
  tests/test_current_ci_surface.py \
  tests/test_model2_legacy_firewall.py \
  tests/test_workflow_trigger_policy.py
```

These checks verify the active Model 3 manuscript/manifest route, the frozen 24,576-case bridge receipt, the 128-history inference boundary, current figure regeneration, submission closure, workflow policy, repository-size guard, and the firewall that keeps Model 2 out of the current Supporting Information and reviewer archive.

For the complete test suite:

```bash
pytest -q
```

## Full production regeneration

The 24,576-case production campaign is intentionally **not** rerun on every pull request. The frozen production result and checksums are the routine verification surface. Full campaign regeneration remains available through the manual-only Model 3 production workflow:

```text
.github/workflows/model3_ch2_bridge_production.yml
```

The production workflow must remain `workflow_dispatch` only. Pull requests automatically run only:

```text
.github/workflows/ci.yml
.github/workflows/chapter2-scientific-gate.yml
```

`tests/test_workflow_trigger_policy.py` enforces that trigger boundary.

## Repository artifact boundary

Large enumerated campaign outputs are not design declarations. New large endpoint tables, case-receipt tables, and generated SVG diagnostics should be stored as workflow artifacts or in the permanent public archive and referenced by checksum/DOI from the repository. Existing large blobs are grandfathered only until the external archive is fixed; they may not grow.

The machine-readable policy is `data/design/repository_artifact_budget_20260928.json` and is enforced by `tests/test_repository_artifact_budget.py`.

History rewriting is deliberately **not** part of routine reproduction. Removing already-committed large blobs from the current tree does not remove them from clone history. A history rewrite is a separate destructive release operation that should occur only after the permanent archive, checksums, tags/releases, and collaborator migration plan are fixed.

## Complete functional-loss tempo result (2026-10-11)

The frozen 1,024-case / 16-profile abrupt-versus-gradual cohort is available as
an exact compressed [official readout](data/results/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json.gz),
with [results and all-setting figure](docs/CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FUNCTIONAL_LOSS_RESULTS_20261011.md),
[full tables](docs/CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FULL_TABLES_20261011.md), and
[admission/source/archive receipt](data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json).
The [raw archive ledger](docs/CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md)
records the private archive's digest. After obtaining the exact archive and
extracting it into `tempo-raw`, use an immutable source checkout at
`dba65f11a4ee7295ae32b623ea1103cc8a25c1b5` for the original source/design:

```bash
python scripts/audit_chapter2_sequence_tempo_results_20261011.py \
  --raw-root tempo-raw/cases \
  --official-readout tempo-raw/readout/chapter2_functional_loss_tempo_readout.json \
  --design /path/to/frozen-source/data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json \
  --source-root /path/to/frozen-source \
  --out tempo-recheck/independent_audit.json
```

This independently recomputes all 128 event/order/occupancy combinations and
registered descriptive profile intervals. All 156 secondary fields per setting
remain in the official readout but are outside that independent aggregate
calculator. This is endpoint recomputation from retained genomes, not a new
stochastic evolutionary replay or a validation in natural islands.

The unchanged table and figure generators are
`scripts/tabulate_chapter2_sequence_tempo_results_20261011.py` and
`scripts/plot_chapter2_sequence_tempo_results_20261011.py`. Both accept the
original uncompressed JSON via `--readout`; their output arguments are `--out`
and `--out-dir`, respectively. The original scientific interpretation review
is retained at [CHAPTER2_SEQUENCE_TEMPO_SCIENTIFIC_REVIEW_20261011.md](docs/CHAPTER2_SEQUENCE_TEMPO_SCIENTIFIC_REVIEW_20261011.md).
