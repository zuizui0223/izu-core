# Ch2 completion audit: five ecological questions

**Final disposition:** `CHAPTER2_PROCESS_FINAL_AUDIT_20261005.md` supersedes the
intermediate checkpoints below. The full suite completed with 933 passing tests;
the current manuscript, SI, four main figures and preserved-Q1 poster have been
assembled and checked. Earlier statements below about pending package work and
running tests document the audit sequence, not additional unfinished tasks. The
high-resolution branch remains explicitly closed unresolved. Git delivery is
recorded separately after commit and remote verification.

Updated 2026-10-05 after completion and independent verification of the 13-rate replenishment extension and processes-v6 poster. This replaces the earlier dated runtime checkpoint in this file. The goal remains active pending the final whole-manuscript/source audit; scientific completion is not inferred from a passing subset of checks.

## Confirmatory amendment — 2026-10-06

A separate prospectively frozen new-history experiment now closes the main
sequence/necessity evidence gate. The primary delayed-selfing/costly
positive-mutation cell confirmed assurance-first realized order (51/64; 95%
history-bootstrap 0.6875–0.8906), while the fixed-assurance replication confirmed
negative investment change without assurance evolution. The result is
setting-specific and must not be generalized to prior selfing, where the
positive-mutation primary-threshold sequence was 30/64 assurance-first.

Design and compact result:
`data/design/chapter2_1005_confirmatory_replication_20261006.json`;
`data/results/chapter2_1005_confirmatory_replication_20261006.json`.

## Ecological evidence and remaining requirements

| Goal requirement | Evidence and current disposition | Remaining scope |
|---|---|---|
| 1. Selection conditions and isolation | Analytical joint thresholds, independently checked at 900 cells; 13-rate/64-history fixed-state diagnostic, all 45 residents and three snapshots; completed finite ABM at all 13 rates | No calibrated natural distance threshold; selection and evolutionary timing are distinct readouts |
| 2. Reciprocal effects | Original 144,060-state diagnostic plus 500-parameter/112,500-case independent tradeoff grid; all four sign regimes and 25 cross-effect exceptions preserved and checked | Dynamic feedback and mediation are not established by cross derivatives; full sequence sensitivity remains open |
| 3. Realized order and extent | Sustained-isolation ABM and completed 13-rate extension, 64 histories x eight repeats; 9,984 extension events and 156 endpoint rows independently checked; fixed/evolving-capacity intervention and separate zero-mutation density bridge | Distinct cohorts are labelled. No admitted full high-resolution positive-mutation ABM/density timing comparison. Do not claim universal onset order or pure-drift attribution |
| 4. Genetic variation and diffusion | Restricted one-locus mutation diagnostic, zero-mutation fixed-support comparison, analytical mutation-kernel limits | One heat-versus-jump tolerance failure retained. Full three-locus positive-mutation comparison closed unresolved under explicit stop decision |
| 5. Reproductive consequences | 12,288 supplementation assays and 6,912 trait manipulations; raw/viable deficits and viable offspring reported separately | Fixed depression does not model purging/genetic load; same-state interventions do not prove field mediation |
| Q1 independence | Manuscript H1-H4 mapping, no regional/colour calibration | Keep this boundary and all Q1 content when updating the final poster |
| Reproducibility and uncertainty | Frozen designs, archived arrays, source hashes, repeat/survival-aware summaries, independent checks | Final packaged source/figure manifest and delivery verification still required |
| Manuscript | Abstract, five questions, methods, parameter dependence and conclusion integrated; Figures 1 and 2 now generated from stored results | Complete editorial/source audit and remaining figure/package integration; no submission-ready claim yet |
| Poster | Processes v6 PPTX/PDF/PNG built and rendered in PowerPoint; Q1 upper 144 shapes and 18 images identical to v2 | 105,946 numeric coordinates verified; seven other charts unchanged. Q2 render reviewed: rate insets, mutation repeats and temporal-reference distinction added. Source package verified with 18 inputs including Q1 original and v2 reference; whole-manuscript review remains. |

## Canonical evidence routes

- Selection: MODEL3_PDE_CLOSEOUT_20261004.md; MODEL3_ISOLATION_SELECTION_GRADIENT_20261005.md.
- Reciprocal and parameter sensitivity: MODEL3_RECIPROCAL_SELECTION_20261005.md; MODEL3_PARAMETER_SELECTION_RESULTS_20261005.md; MODEL3_ASSUMPTION_SENSITIVITY_SCOPE_20261005.md.
- Evolution: MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md; MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md; MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md.
- Reproduction: MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md; MODEL3_TRAIT_POLLEN_RESULTS_20261005.md.
- Numerical closure: MODEL3_LONG_COMPARISON_DECISION_20261005.md; MODEL3_MUTATION_MEMORY_20261004.md.
- Latest poster receipt: data/results/model3_poster_processes_v6_delivery_20261005.json.

## Stopped numerical extension

The 1,000-update high-grid job was stopped by the user after verified update 7, with update 8 unfinished. `data/results/model3_long_run_user_stop_20261005.json` records the terminal decision. A current Windows process query found no Python command matching highgrid, checked_streamed or fastpath_candidate at this audit; no computation was restarted. Historical live-PID statements in earlier revisions are not current status.

The alternative evaluation found no validated cheap replacement for the full positive-mutation long comparison. Coarse-grid terminal gates failed in 31/32 cases; a restricted one-locus heat approximation failed its declared tolerance in one condition. These are retained numerical limits, not biological falsification and not a reason to loosen tolerances. The user explicitly permits closing this branch as unresolved; this does not complete the manuscript/poster deliverables.

## Immediate completion work

1. Finish source-linked figure assembly and editorial review; retain all conditions and exploratory labels.
2. Update Q2 in the poster without changing Q1, distinguishing selection, sequence and necessity; show the uncertainty and parameter dependence at appropriate scale.
3. Verify the delivered artifact against results and inspect its rendered layout.
4. Audit every requirement again before marking the goal complete. Parameter sensitivity of actual sequence remains unestablished and must be explicitly bounded, not silently generalized from fixed-state assays.

## Current versus historical delivery audit

The older Oikos renderer, RTF and submission bundle had remained attached to the
changing active manuscript, despite their historical title, figures and claim
guards. They now reproduce an exact manuscript snapshot from commit
4b7d7bc7c0d6cd9b87e38150c55dfa99fd9b0556. Every render verifies the snapshot SHA-256;
a changed-byte test confirms rejection. This preserves the historical results
without presenting their closed submission gate as closure of the current paper.

The current route is `scripts/render_chapter2_process_manuscript.py` and
`scripts/build_chapter2_process_review.py`. Its review ZIP contains the current
manuscript, four main PDFs, companion condition/threshold PDFs, plotted tables,
supporting explanations and working Python sources. All members are read back
and hash-checked. It is not a complete raw-data deposit or journal submission;
the 13-rate raw archive remains separately identified. The software's full test
run is still in progress at this checkpoint. The 21 focused current/historical
delivery tests pass. Figure verification independently rechecked 2,340 local
selection means and 468 gradient endpoint estimates against source arrays and
summaries. Figure 3 now labels the actual replenishment rates rather than
geographic categories; its twelve component means were rechecked against raw
assays and its rendered labels inspected.

The review package additionally includes the numerical inputs required by all
four main figure scripts, at their original repository-relative paths. In a
fresh extraction, all four scripts exited successfully without accessing the
working repository. Regenerated selection tables, temporal events and genetic
realization tables were byte-identical; all 512,512 sequence coordinates also
matched. `outputs/chapter2_process_delivery/isolated_redraw.json` identifies the
exact tested ZIP and extraction. This verifies figure reproduction; primary
raw campaigns and the stopped numerical branch retain their separate status.

The parameter-sensitivity scope document has been updated to include the
completed intermediate-rate evolutionary trajectories. Remaining untested
joint biological-parameter sensitivity is not confused with this now-completed
replenishment-rate comparison.

## Continuous replenishment extension

The 11 intermediate-rate finite-ABM conditions completed as a separate, declared extension of the existing two endpoints. The design retains capacity 48, the biological rules and the blocked histories/repeats. It adds 11,264 cases and reuses 2,048 endpoint cases. `MODEL3_REPLENISHMENT_EVOLUTION_20261005.md` identifies the design, exact endpoint replay and readout. Raw reconstruction of all 13,312 cases and 9,993,984 trait coordinates, plus independent readout of 9,984 events and 156 endpoint rows, passed with zero numeric discrepancy. Results are integrated in the manuscript and v6 poster. The complete local archive (763,914,318 bytes) was read back and hash-verified; data/results/model3_replenishment_archive_20261005.json records its identity. It is not a public deposit. The stopped high-resolution deterministic/PDE branch remains stopped.

The manuscript now distinguishes finite-plant parental-contribution slopes from resident-fixed rare-mutant log-fitness gradients, uses uncalibrated reproductive updates for chronology, and removes an unsupported inference of evolution toward broader floral accessibility. The composition assay source is `scripts/audit_model3_unified_reduction.py` calling `scripts/model3_island/assays.py::investment_assay`; these editorial changes do not alter frozen calculations.

Main Figure 2 now assembles temporal crossings and capacity-intervention trajectories as separate panels/cohorts. All 128 event points and 512,512 trajectory coordinates exactly match the stored source arrays; the PDF was rendered with Poppler and visually reviewed. Verification: `data/results/model3_sequence_necessity_figure_verified_20261005.json`. Threshold sensitivity and evolving-capacity trajectories remain in their companion figures.
