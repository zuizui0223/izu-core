# Reproducing the current Chapter 2 submission state

The active Chapter 2 paper uses **one nested Model 3**. Older response-geometry / synthetic-`k` analyses are historical legacy provenance under `legacy/model2/`; they are excluded from the current manuscript, Supporting Information and reviewer archive.

## Current unified manuscript review package

The active manuscript is `docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md` and its Supporting Information is `docs/CHAPTER2_UNIFIED_EL_SUPPORTING_INFORMATION_20261010.md`. Rebuild their reviewer package from stored evidence:

```bash
python -m pip install -e '.[dev]'
python -m scripts.figure_model3_return_components
python -m scripts.figure_model3_assurance_compression
python -m scripts.figure_model3_trait_pollen
python -m scripts.figure_model3_genetic_realization
python -m scripts.build_chapter2_unified_el_submission_bundle
pytest -q tests/test_chapter2_unified_one_paper_20261010.py tests/test_chapter2_unified_el_review_bundle_20261010.py tests/test_chapter2_sequence_tempo_result_receipt_20261011.py
```

`outputs/chapter2_unified_el_delivery/EL_ONE_PAPER_REVIEW.zip` contains the anonymous manuscript and Supporting Information, four main and three supplementary figures, and separately source-pinned evidence (including the observational S25 material). The merged 2026-10-14 PR #491 reviewer build contained **143 ZIP members / 142 manifest-listed payloads**; these counts are historical build facts, not fixed requirements for future versions. Use each generated `MANIFEST.json` and internal receipt to check current member hashes and counts. The builder checks PDF/SVG/JSON integrity, authenticates input receipts and reads back ZIP members. Given identical input bytes, ZIP output is deterministic. Figure regeneration reuses stored results; it launches no biological campaign. Visual inspection of the rendered figures remains part of release review.

The exact official tempo gzip and frozen design are included without changing their bytes. Only the table's identifying repository link is replaced in the anonymous copy; all numerical rows are retained. A derived anonymous audit summary retains all 128 independently checked setting/outcome comparisons and the exclusion of all 156 secondary fields per setting. The original audit, admission record and original tables remain unchanged in the repository. `EL_ONE_PAPER_REVIEW.receipt.json` is a **separate internal provenance record**, with build commit/tree, source-to-derived hashes and any tracked worktree changes; it is not inside the anonymous reviewer ZIP. Its build identity must not be confused with the tempo execution-source identity.

Keep inference units distinct: the primary evolutionary and registered demographic studies each use their own 64 independent visitor histories; the separately frozen tempo supplement uses 16 synthetic profiles with four nested repeats. The older 128-history bridge below remains supporting provenance. Neither repeated trajectories nor 410,624 tempo censuses enlarge these independent denominators. External raw-data deposition remains incomplete; see the [consolidated readiness record](docs/CHAPTER2_UNIFIED_DATA_DEPOSIT_READINESS_20261011.md).

## Recovered evolutionary raw archive (2026-10-11)

The [recovery receipt](data/submission/chapter2_evolution_archive_recovery_20261011.json) identifies a newly assembled historical archive containing all **50 original Actions ZIPs** from the independent confirmation and actual PR #411 generality campaigns. Its outer filename is `chapter2_public_archive_20261006.zip`, size **518,372,739 bytes**, SHA-256 **`0596de11afea2f9f0b5a781f6d0ddd1fa7ea772f048ec0ccfc06e9ecbbf60695`**. A separately retrieved private preserved copy matched that identity. Public external deposition remains pending.

After authenticating this exact outer ZIP against its receipt, extract it and check all original case receipts and stored arrays:

```bash
python -m zipfile -e chapter2_public_archive_20261006.zip outputs/chapter2_recovered_archive
python scripts/audit_chapter2_recovered_evolution_archives_20261011.py \
  --repo . \
  --artifact-dir outputs/chapter2_recovered_archive/raw-artifacts \
  --out outputs/chapter2_recovered_archive/original_case_audit.json
```

The output must be separate from the original archive inputs and tracked source files; unsafe destinations are rejected before writing. The checker requires NumPy and the original Git source objects: metadata reference `90c43f0f7b9c441bd4251d1139547e43e6d118d6`, confirmation execution `380de3240992db691e1434f8577256ced80d5ae8`, and generality execution `20e8e2d6ad25545b9cb4941305343b5f010a58f4`. For a shallow clone, fetch those exact commits before checking. The [recorded independent audit](data/submission/chapter2_evolution_original_case_audit_20261011.json) covers **4,096 + 8,448 = 12,544 NPZ/JSON pairs**, complete declared task sets, source snapshots, original member CRCs and NPZ receipt hashes. It preserves the distinction between original full result JSONs and their committed projections.

The existing archive workflow now keeps GitHub authorization on the initial API request and pins supporting materials to the historical packaging checkout `94c051850a43b89047e78e653edae25b043624ab`. That checkout preserves the historical manuscript association; it does not replace the current unified paper. Future builds may have different outer ZIP timestamps/checksums, so retain each actual bundle receipt and verify every original inner ZIP against the frozen source manifest.

The checker launches no biological simulation, selection replay, endpoint calculation or bootstrap. These archives store a 1,001-row trace and genomes at t0/t200/t400/t1000, not annual diploid genomes. They do not close the [original discovery-cohort replay gap](docs/CHAPTER2_SOURCE_REPLAY_COHORT_IDENTITY_20261011.md), or replace the separate demographic and tempo archive requirements.


## Fixed-B48 source-only integrity check (2026-10-14)

The original `chapter2-k48-future-shard-18.zip` remained accessible in GitHub Actions at artifact ID **11600619779** (workflow run **37896872795**). For an *authorized, locally obtained read-only source copy*, independently check the exact artifact SHA-256, ZIP CRC and 32 JSON/sidecar pairs:

```bash
python -m scripts.verify_chapter2_k48_shard18_source_20261014 \
  /path/to/chapter2-k48-future-shard-18.zip \
  --receipt outputs/source_verification/k48_shard18_source_readback.json
pytest -q tests/test_verify_chapter2_k48_shard18_source_20261014.py
```

The [2026-10-14 source readback](data/submission/chapter2_k48_shard18_fresh_actions_readback_20261014.json) independently matched the complete original 118,143-byte ZIP and all 32 JSON SHA-256 sidecars. **This is not a new external private backup or an authorized DOI deposit:** the external service's prior safety check was not bypassed, and the fixed-B48 private external backup remains **130/131** (all four cohorts **520/521**). See [the deposit handoff](docs/CHAPTER2_PRIVATE_EXTERNAL_BACKUP_DEPOSIT_HANDOFF_20261013.md) and [open Issue #436](https://github.com/zuizui0223/izu-core/issues/436). This check does not recompute 1,792 biological future conditions or upgrade the study's inference.

## Historical isolation bridge: independent unit and denominator

The prospective isolation bridge contains **24,576 computational cases**, but those cases are **not independent replicates**. The uncertainty-bearing unit is **128 independent visitor-history seeds**. Eight demographic repeats are nested within each history/state/intervention combination and are averaged or retained for repeat-instability diagnostics; they **do not increase the independent history count**.

Mean intervals use **1,999 history-cluster bootstrap resamples**. Mixed-history counts are reported at deadbands `0`, `0.01`, and `0.05` and are descriptive realized labels, not estimates of a stable latent branch prevalence.

## Historical bridge verification path

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

These checks preserve the historical Model 3 bridge manuscript/manifest route, the frozen 24,576-case receipt, the 128-history inference boundary, bridge figure regeneration, workflow policy, repository-size guard, and the Model 2 firewall. Use the unified package commands above for the active manuscript.

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

## Existing tempo cohort: realized inheritance and recruitment accounting (2026-10-11)

The [new report](docs/CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_20261011.md) and
[complete tables](docs/CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_TABLES_20261011.md)
account for every original case without generating biological histories.
Use this checkout for the new auditors; their preflight rehashes all 30 original
receipted native source files against the unchanged execution identity. With
the original archive extracted into `tempo-raw`, run:

```bash
python -m scripts.audit_chapter2_tempo_realization_accounting_20261011 \
  --raw-root tempo-raw \
  --output-json tempo-recheck/native_realization_accounting.json \
  --workers 8

python scripts/audit_chapter2_tempo_realization_independent_20261011.py \
  --raw-root tempo-raw/cases \
  --design data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json \
  --out tempo-recheck/independent_genetic_accounting.json \
  --workers 8

python -m scripts.tabulate_chapter2_tempo_realization_accounting_20261011 \
  --accounting tempo-recheck/native_realization_accounting.json \
  --independent tempo-recheck/independent_genetic_accounting.json \
  --summary-gzip tempo-recheck/realization_summary.json.gz \
  --comparison-json tempo-recheck/realization_comparison.json \
  --tables-md tempo-recheck/realization_tables.md
```

The first calculation uses deterministic native reproduction on archived
genotypes and verifies saved expectations and reproductive totals. The second
independently maps archived parent and child IDs, treating saved expectations
as declared inputs. It records fresh runtime/timestamp metadata, so a repeated
independent audit has different receipt bytes while its compared numerical
fields remain reproducible. The final command compares all case, profile, arm,
paired-profile and paired-setting component summaries before producing outputs.

The compact Git result retains every case/window/profile/arm value and omits
only each case's annual `censuses` and `updates` arrays. Those remain in the
separately saved `izu_core_tempo_realization_full_20261011.json.gz`, identified
by SHA256 in the [artifact receipt](data/results/chapter2_tempo_realization_receipt_20261011.json).
Its 85,737,428 decompressed bytes equal the native JSON output from the recorded
runtime; gzip uses an empty stored filename and `mtime=0`. Neither the compact
projection nor the full result replaces the original raw-genome archive.

The new accounting rank is retrospective and descriptive. It adds no intervals,
p-values, mutation-order intervention, survival-equivalence claim, or evolutionary
mediation estimate. The earlier independent endpoint audit's stated exclusions
remain historical; this separate audit verifies the specific expectation,
trait-mean, parentage and recruitment quantities it uses, rather than declaring
all 156 original secondary fields per setting independently recomputed.
