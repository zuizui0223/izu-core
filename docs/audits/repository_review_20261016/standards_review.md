# Standards / maintainability review

Snapshot: 91d884e8 (review checkout). Source review plus narrowly authorized maintenance fixes.

## Coverage and limitations

All 593 Python files under scripts were parsed with AST. There are 604 tracked scripts-tree files including 11 protocol/manifest documents; no src directory. This is static inventory coverage, not a claim that 593 implementations have had individual semantic review. Exact full and partial source-read lists, per-file line counts and duplicate groups are in standards_reviewed.json. Other reviewers cover biological core and verifier internals. No long simulation or scientific regeneration was run.

Static indicators: 9 files mutate sys.path; 16 reference CWD; 123 contain assertions. Exact AST comparison of functions spanning at least 8 lines found 58 duplicate groups, 159 occurrences in 78 files. Nested functions overlap parent functions, so these counts must not be summed into a lines-saved estimate.

## Concrete finding: input admission checks disappear under optimization (P2)

scripts/figure_model3_assurance_compression.py:53-55 and 65 use assert for required completed/admitted cohort status and expected settings. scripts/figure_model3_return_components.py:20 and scripts/figure_model3_trait_pollen.py:33 have the same pattern. These are entrypoints in the current REPRODUCE route. Under python -O or PYTHONOPTIMIZE the program can render incompletely admitted inputs if their schema remains sufficient. The builder may independently protect its own final bundle; that does not make the standalone render command fail closed.

Reproduced without changing inputs or rendering: extracted the actual first three main() assertion AST nodes and compiled normally vs optimize=1 against statuses NOT_CONFIRMED/incomplete/incomplete. Normal rejects with AssertionError; optimized accepts. This proves the admission bypass, not that current committed inputs are invalid.

Safe fix: explicit conditional ValueError in active renderers, with a subprocess optimized-mode regression using temporary fixture inputs. Keep all source datasets, values and claim language unchanged. Avoid mechanical replacement throughout frozen source snapshots.

## Concrete maintainability issue: current figure has import-time write side effects (P2 candidate)

scripts/figure_model3_genetic_realization.py:13 onward creates its output directory, reads three sources, plots and overwrites artifacts at module import. All other reviewed current main figures expose main() with an execution guard. Importing this module for reuse, introspection or test collection changes outputs and global matplotlib rcParams. It also has no way to request help without generating the figures. This is source-demonstrated; the module was deliberately not imported in the read-only review.

Safe fix: wrap this existing body in main(), use a __main__ guard, and close the figure; no numerical rewriting. Test importing with temporary OUT instrumentation causes no file writes, and script invocation still exports identical plotted CSV values/provenance scope. Byte-identical PDFs may require timestamp normalization, so do not promise that automatically.

## Packaging gap (P3; does not invalidate documented dev-install route)

pyproject.toml:12 declares dependencies=[] while installed model3_island/types.py:5 unconditionally imports NumPy. Default installation in a clean interpreter therefore does not provision a core runtime dependency. All dependencies, including NumPy and figure libraries, are only in dev. The documented editable .[dev] route and CI install dev, so they conceal this gap but remain valid. Safe next step: define core NumPy requirement and optional plotting/submission extras, retain dev as superset. Verify in clean venv, without relying on host-site packages. Do not claim this package currently supports standalone data reproduction from a wheel: data/results/design/docs are checkout-resident and explicit package list only includes scripts and scripts.model3_island.

## Refactor opportunities, NOT immediate defects or deletion approval

1. Add a machine-readable command index linking the current reproduction entrypoints to tests, workflows and source-receipt boundaries. Current navigation already provides strong prose rules; operational metadata can make 604 files navigable without moving them. Reference counts are not enough to authorize deletion because original SHA references remain authoritative.
2. Preserve duplicate frozen execution copies. Examples: scripts/prepare_chapter2_clock_pilot_archive_20261013.py vs clock_approved_execution_20261014/producer.py, and model3_island/population.py vs directional_access_20261013/POPULATION_SOURCE.py / low_allele_loss_20261014/native/population.py. A shared helper would retroactively couple independent frozen experiments.
3. The eight identical bounded_step definitions in model3_{batched_weight,binary_reader,checked_weight,complete,exact_gamete,gamete,rounded_gamete,streamed_weight}_integration.py are candidates for a future common implementation only after import/receipt/workflow/source-hash consumers are mapped and mathematical regression is available. Do not consolidate just because AST bodies match: module globals can differ.
4. A shared new figure-export helper could unify font/output/provenance plumbing for future active figures. Keep cohort-specific status, independent unit and contrast logic in each renderer. Do not create one global mutable settings registry to simplify historical scripts.

## Explicitly rejected false positives

- resume_frozen_atom_20261011.py hardcodes a Windows BASE and run_model3_highgrid_long_continuation.py uses WinDLL plus a fixed producer PID. These are explicitly infrastructure-only historical continuation tools, not generic current portable runners. Their platform scope should be indexed, not silently generalized.
- Existing three genetic-realization JSONs successfully decode with cp932; lack of explicit encoding is a future fragility, not a reproduced current failure.
- No claim of unused scripts is made. Workflow references exist for the resume tool; tests dynamically load it. Bulk cleanup is unsafe.

## Recommended first change set

Limit an initial maintenance PR to explicit active-renderer guards plus import-safe figure entrypoint and clean-install metadata verification. Preserve frozen numerical modules and receipts. Follow with command registry and targeted golden-value regressions. The remaining static inventory is a queue for further semantic review, not a completed scientific validation.

## Broad pass update / destructive archive overlap fixed

Whole-source reading extended to 33 renderer/builder/plot scripts listed in JSON (metadata cover letter literal truncated in output; executable code fully read). Found build_chapter2_public_archive.py deleting a guessed staging directory even when it was the authenticated artifact directory. Reproduced using two real ZIP fixtures and valid digests while intercepting rmtree, so originals were never deleted. Fixed only current builder with resolved output/source overlap rejection, existing-output protection, exclusive ZIP/receipt creation, and owned unique temporary staging. 12 relevant tests passed. Historical workflow checks out 94c05185 and will still use its original builder; frozen recovery receipt unchanged. No research payload semantics changed.

## Follow-up full-source pass

69 additional full-source reads recorded individually in standards_reviewed.json, including all17 audit_n..z files. The latter preserve frozen hashes and explicit retrospective/conditional limits; many early precision probes execute on import and intentionally retain failed gates. No scientific reruns or automatic historical refactors.

Corrected unified EL bundle receipt-only stale figure role text: actual SI assigns original-mutation ten-context comparison to Figure3 and earlier finite realization to SupplementaryS3, while receipt said the reverse old route. Existing archive regression reproduced failure then passed after one-string fix; source manuscript and evidence bytes unchanged.

## Final extended source coverage and fixes

Completed all 44 exact pipeline handoff audit_chapter2 files, plus the six parent miscellaneous files; each full-source path is recorded separately under chapter_handoff_full_source_read and parent_misc_full_source_read. This is additional to the 69 broad-pass files and initial review lists; union paths before counting overlap. The source review covers logic, contrast orientation, conditional denominators and explicit historical/admission scope, not merely AST inventory.

Signed-quadrant --check previously zipped saved/current context lists without checking their lengths and used a comparison permitting NaN. A synthetic truncated-context record produced PASS. Replaced this with a recursive complete-key/list-length/type and finite numeric comparator retaining the existing absolute tolerance. Four synthetic tests passed (valid record, truncated contexts, NaN, metadata mismatch); no native calculations or saved scientific records changed.

Active figure changes: explicit admission ValueError guards in three active renderers and an import-safe main() in the separately named figure_model3_genetic_realization_safe.py successor. The original genetic renderer was restored byte-for-byte after full-suite verification exposed its SOURCE_BLOBS pin; the frozen original still has import side effects and is deferred. Fourteen tests passed. Genetic realization CSV, provenance JSON and PNG compared byte-identically against original git source in a temporary output path (2770, 521 and 284496 bytes respectively).

Fixed original_evolved_pollen_service.source_audit passing the dictionary returned by original_shards to state_from_archive. A bounded real ZIP/NPZ checkpoint fixture reproduced AttributeError on its first read; callsites now select the fixed/evolving shard before calling the unchanged reader. All four near/far x fixed/evolving branches are tested, including receipt and allele-trace checks. The new fixture and existing source-evidence suite pass: 7 tests. Exact filename/digest search found no current auditor source pin (original SHA256 acd23f4eccc600a2d57febb2d5232e553aad1e18bf210d9469e3796df1249153); the frozen reproduction operator, archives and historical scientific results remain unchanged. No model campaign was run.

A lower-priority output-preservation candidate remains sequence_tempo_results main(): write_text to a guessed <out>.tmp can overwrite a pre-existing temporary file, although the final output itself is checked first. No speculative broad output rewrite was made.

Peer review: read the complete current patches and regression tests for shard axis/domain inventory, persistent readout/clock uniqueness, three prehistory dry-run key fixes, timed-gate visitor loop indentation and Figure3 finite stored means. No additional blocker found in those changes. Tests are bounded fixture/admission tests; independent historical implementations and frozen scientific operators remain distinct.


## Final handoff and frozen-surface finding

Completed ten additional top-level summarize/verify files, listed in final_handoff_full_source_read. Nested directional-access and low-allele-loss verifiers remain the science reviewer lane; not counted here. Total standards-lane unique full-source Python coverage: 137.

Confirmed defects in pinned summarize_chapter2_finite_history_signal_validation.py: _load_discovery accepts reversed starting-population/demographic-seed axes and overlapping history assignments, then overwrites earlier cells. A bounded 16-file fixture reproduced all three admissions with finite arrays. Separately, a synthetic failed ordering through main() produces failure=true while interpretation.main still states that new seeds reproduced the ordering. Evidence: finite_validation_pinned_reproduction.json. These are admission/narrative defects; the existing historical receipt records strong_success=true, so this does not demonstrate its scientific result is false.

Deferred source editing: committed_reproduction_surface.summarizer_git_blob_sha in the historical receipt is dece866839c557db7c097e2944ed538e2b99fa1a and tests/test_chapter2_el_repeatability_claim_ceiling.py:286 binds the current source to it. Correct through a separately versioned reproduction surface or explicitly reconciled archival policy, never by silently changing the receipt. No campaign or scientific history was run for reproduction: only synthetic tensors and existing readout logic.

Completed the final 13 chapter audits in last13_full_source_read (150 unique Python sources total in this lane). Reviewed complete source text, including design gates, F/P/S orientation, inherited-state support, snapshot versus future inference, paired history units and CLI output admission. No new simulations. A further candidate is Q2_original_F1_focal_return --check: selected numeric comparisons use abs(saved-current)>TOL, which can admit NaN, and summary claims are not fully compared; bounded reproduction confirmed false PASS after replacing one saved parental_genome_W by NaN and mocking audit() to the unchanged baseline (no native calculations). Current source SHA256 1236044fa3d5a03c2fac924d2c65cd0deea2b256cf110d74a1e8d0ab9efca0bc and blob 8a054df288fd2f65fb3fbf5509ccfe2dad25c81e had no source-pin matches. Authorized minimal fix now compares the complete finite record with the existing tolerance. Tests first reproduced false PASS for NaN and altered summary, then passed for those cases plus valid finite and truncated records. No historical result changed.

Final focused verification: 22 tests passed together (4 F1 integrity, 14 active renderer/successor, 4 original Figure3 source-to-DOI). Final report and long-horizon inventory changes peer-reviewed without an additional blocker. Original genetic renderer restored exactly; source-to-DOI pin remains unchanged.
