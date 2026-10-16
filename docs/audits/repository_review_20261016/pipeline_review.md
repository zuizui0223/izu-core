# Pipeline integrity review

Snapshot: `91d884e8fc46def450c6091f617b0f96776aad75`. Read-only audit except the explicitly authorized finite-number fix in the Figure 3 verifier and its test. No data, designs, raw archives, scientific operators, or published receipts were changed. No research campaign or external publication was run.

## Coverage

`pipeline_reviewed.json` lists 49 assigned archive/verifier files: 20 complete source reads, 4 partial source reads, 25 automated AST scans only. All 49 parse successfully. Automated scans are NOT substantive code review. The 1,394-line active submission bundle was only partly reviewed; it must not be marked complete. README and REPRODUCE navigation were consulted to distinguish active from historical gates. No root AGENTS.md exists in this snapshot.

## Confirmed findings

### P2 — Reject nonfinite stored means before claiming original figure values match [fixed]

File: `scripts/verify_chapter2_figure3_onelocus_original_raw_20261015.py`, original lines 130–131 (fixed block 127–136).

The verifier compares stored means with `abs(reconstructed - stored) >= 1e-13`. A NaN operand makes that comparison false, accepting a corrupted mean while reporting `FIGURE3_BC_64_NATIVE_TRACES_RECHECKED`. Raw traces are finite and authenticated, but these two stored mean fields are not protected by their archive hash. Reproduced using the actual unchanged pinned 64-trace ZIP and temporary copies of both readouts: replacing all 16 variability means and the summary mean arrays with NaN still returned PASS.

Repair: explicitly require both stored scalar means to be finite before tolerance comparison. This preserves the exact numerical tolerance and all frozen science. Added six regression cases (NaN, +Inf, -Inf in each of the two readout surfaces), in addition to existing actual-original-archive positive and corruption tests.

Validation: `python -m pytest -q tests/test_chapter2_figure3_onelocus_original_raw_20261015.py --basetemp=../../outputs/repository_review_20261016/test_tmp_pipeline --disable-warnings` => 9 passed. The NaN mutation failed before repair and is rejected afterward. Positive verification reconstructs all 16 rows from original bytes, with no biological simulation.

Source-pin check: original verifier SHA256 `d4968c157ce7a56fc29c4ce5cbfddec4bcbf74662be76d87632d1ac1d8abd290`, Git blob `6f96b68da2fe14297ea35c123b42132be8212bd6`; repository-wide text searches found neither hash referenced. Path references exist only in its tests and source-audit documentation. No known receipt pin was invalidated; raw ZIP/source readout hashes remain unchanged. External untracked consumers are outside this search scope.

### P2 — Require declared result coverage before returning verified [fixed]

File: `scripts/verify_model3_persistent_readout.py`, lines 29–30 and 54–64.

Both result arrays are iterated without validating the expected key sets or even nonzero counts. A summary containing `temporal_order: []` and `endpoints: []`, with correctly recorded input digests, returns `status: verified`, `independent_crossing_checks: 0`, `endpoint_rows: 0`. Thus a truncated producer output can receive a verified verdict without checking any result. Although the stated scope delegates raw-case checks to the summarizer, completeness of the curve-derived result being verified still must be checked here.

Reproduced by copying the unchanged verifier to an isolated temporary root, creating an empty NPZ and empty result arrays plus matching SHA256 fields for plan/curve/source-manifest/analysis bytes, then running its normal CLI. Exit 0 and the zero-check verified JSON were observed. This is a parser/admission fixture, not a scientific rerun. Suggested repair: derive the exact setting × mutation × contrast × threshold/period inventory from the frozen plan; reject missing/duplicate/extra keys before checking rows. Do not alter the historical result or loosen frozen predicates.

## Not promoted to findings

- S29 numeric comparisons also use subtraction comparisons, but the production entry point authenticates exact pinned source Git blobs first; a mutated helper dictionary alone is not an executable production-path failure.
- Historical public-archive builder uses current root paths, but REPRODUCE explicitly pins its workflow packaging checkout. That documented historical constraint was not reported as a current-source provenance failure.
- External clock archive reader explicitly distinguishes provided mirror bytes from independent archival custody; two URLs alone are not claimed as proof.
- Several older scripts use asserts as gates. This is a hardening candidate under Python optimization, not independently elevated to a current defect without an actual supported optimized invocation.

## Remaining review

Substantive review remains for the 25 scan-only files and completion of four partial reads. The active submission bundle deserves function-level source/readout mutation tests and careful verification of deterministic archive/provenance handling. This report makes no claim of whole-repository completion.


## Follow-up authorized repair: persistent readout completeness

Added an independent inventory gate before row comparisons, based on the historical producer's declared grid: two settings, two mutation rates, three contrasts, three plan thresholds (36 rows), two endpoint times (8 rows), twelve curves of shape (64,1001,3), and the exact ordered 64 visitor-history seeds for each row. Missing, duplicate, foreign, or truncated coverage now raises ValueError. No research simulation ran.

Added tests against the unchanged committed summary plus layout fixtures: complete positive inventory; empty/missing/duplicate/foreign rows for both tables; missing/short curves; missing/duplicate/extra events; and the original complete CLI-path empty-readout reproducer with matching file digests. Combined focused run: **24 passed** (15 inventory tests + 9 Figure3 tests).

Unlike the Figure3 verifier, the historical persistent verifier SHA256 `d460bb6a738ebb34d48cbd6c6918c59ce67c3eeb73ba6f31380d6730929fd7bc` is listed in restoration/triangle preflight manifests under `FROZEN_SOURCE/` or `frozen_source/`. Those manifests authenticate archived historical source trees, not this revised current verifier. All frozen inventories and archived sources were preserved. A historical replay must continue using the exact archived source; do not replace its pinned copy with this hardened current verifier.


## Expansion: 60 further complete source reads

Read all 60 paths in `pipeline_next60.json`, including explicit rereads of two files whose first tool output was truncated. These are scripts in the current tree, including historical numerical engineering probes; this is not a claim that all 60 feed the current manuscript. Inventory now contains **80 complete reads, 4 partial reads, 12 automated-only scans (96 unique files)**. No campaigns or simulations were launched. The earlier Remaining review counts are superseded by this inventory. No additional production edits were made in this expansion.

### P2: duplicated clock rows satisfy an ALL320 verdict

`scripts/verify_existing_response_clocks_independent_20261013.py:12-16,30` checks only `len(records)==320`, then reads each record's self-selected task key, without requiring unique or exhaustive task identities. Repeating one valid record 320 times checks that same original row repeatedly and returns ALL320_RAW_CLOCKS_AND_SUMS_INDEPENDENTLY_MATCH, cases=320, checks=7040. This is a structural verifier coverage blind spot, not evidence that the committed readout or original archive is corrupt. The producer `audit_existing_response_timing_20261013.py` builds 320 distinct original cases and checks grouped replicate counts; its verifier must independently retain that coverage condition.

`repro_pipeline_coverage.py` reproduces the actual unchanged verify() control flow using one synthetic 200-update row repeated 320 times. **The original archive is absent locally, so the fixed SHA admission was explicitly mocked; this is not an original-archive replay or hash-bypass claim.** Once a genuine original archive is available the same test can repeat a genuine validated row without mocking. Repair should validate unique task keys against the original archive's declared case inventory, not merely increase arithmetic checks. Current source SHA256 50cc4d9a57315d8c5bfc2734517fdb89e1ddfc7fdea0b7789839c95f1ff1c165; Git blob b0a0808033cba0bfea470532dd22eae585e9f37d. No textual hash pins found.

### P2: empty kernel comparisons claim ALL48 with zero checks

`scripts/kernel_expression_accounting_20261013/verify_kernel_expression_independent.py:19,56-58` iterates readout comparisons without checking the declared 48-pair grid, then hardcodes pairs=48 in a successful receipt. Empty comparisons produce ALL48_TWO_REFERENCE_STATE_TIME_AND_SWITCH_REWARD_IDENTITIES_INDEPENDENTLY_MATCH, pairs=48, state_time_checks=0, switch_time_checks=0, max errors=0. The unchanged script is exercised by the same isolated synthetic reproducer. **Pinned original kernel NPZ and extracted readout are unavailable locally; its source-hash admission was mocked, explicitly, only to isolate downstream completeness logic.** No claim is made about invalidity of archived scientific outputs. A real original source does not cause the skipped loop to validate empty comparisons, so source authentication cannot substitute for inventory checks.

Repair should require the exact native/fixed-expression pair inventory, unique readout keys, contribution array dimensions, and derived nonzero expected counts before emitting success. Current source SHA256 9d73fa52fb37d8507006ef1d1f8531a91f7dd9846143199024a47f3dc925b341; Git blob 033966b896c5fa98d92a9138fd49ee745a53a846. Its current SHA is recorded in `data/results/kernel_expression_accounting_20261013/INDEPENDENT_REVIEW.json`; preserve that historical receipt and archived verifier if hardening the current script.

## Logic, circularity, and verification independence

- **Independent arithmetic on shared raw inputs is legitimate, narrower than independent biology.** `verify_model3_replenishment_raw_curves.py:57-67` rebuilds per-time live-repeat reductions directly from raw cases; it explicitly states no independent simulator reimplementation. `verify_model3_replenishment_readout.py:20-25` implements a sustained-window loop rather than importing the producer's convolution. Its event/interval agreement validates readout arithmetic, not ecological premises or historical causation. Shared bootstrap seed is necessary to reproduce the declared bootstrap, not circular evidence of an effect.
- **Parameter-selection cross check is partially independent.** `verify_model3_parameter_selection.py:9,37-50` uses finite differences of `_log_fitness_batch`; the producer uses analytic `syndrome_thresholds` for the stored cross derivatives, so it is a distinct derivative path. However, `audit_model3_parameter_selection.py:11` imports the same fitness helper for its earlier gradient cross-check, and both share visitor/config assumptions. This supports numerical derivative consistency, not an independent fitness-model implementation. Its scope already limits trajectory/calibration claims, so no bug is inferred from sharing.
- **Hashes are provenance/integrity conditions, not mathematical validation.** In the trait-pollen verifier, `scripts/verify_model3_trait_pollen_intervention.py:16-21` compares manifest, source ZIP, and working source; this checks consistency among supplied artifacts, not an external trust anchor. Its subsequent explicit raw 6912-key inventory and independent contrasts provide additional verification. The distinction should remain in any review summary; no evidence here supports calling an internally consistent manifest an independent scientific replication.
- **Coverage is a prerequisite for an independent claim.** The two new findings above have genuinely separate numerical formulas, yet their ALL320/ALL48 claims are not entailed when coverage is duplicated/empty. No number of repeated same-case checks supplies independent case coverage.
- **Further hardening candidate, not separately reproduced:** trait-pollen verifier checks 12 summary cells and seven contrasts per cell but does not require unique complete summary keys (`:30-33`); replenishment readout similarly checks row lengths without exact unique row grids (`:42-45`). Those are related completeness risks; this expansion does not claim archived results are affected or count these as independently reproduced findings.


## Clock inventory repair and continuing review

Authorized current clock verifier fix now requires the exact unique 320 evolving-case keys from the authenticated original ZIP before checking arithmetic; rejects duplicate ZIP members. Frozen payloads unchanged. Six entrypoint tests exercise positive full inventory and duplicate/missing/foreign/extra/empty readouts with explicitly mocked original-source hash only. Combined pipeline-focused suite: **30 passed**. Kernel historical verifier is still unchanged pending archive-source scope.

A further 16 complete reads from pipeline_remaining_read_order.json indices 0 through 15 are now recorded (including one newly added current Q4 contract; inventory is current tree, not exclusively original HEAD). The variance/Price and resource-envelope scripts limit their mathematical claims appropriately; sharing the density ledger for Price conservation is an identity check, not an independent biological mechanism proof. Mutational-priority replay imports the original analyze() function and tests historical-decision preservation; it must not be described as independently reimplemented analysis. No new campaign run or new confirmed finding in these 16 reads.


## Further expansion: 32 files in remaining read order completed

Indices 0–31 inclusive in pipeline_remaining_read_order.json now fully read. Current complete reads total112, partial4, scan-only10. Current-tree coverage includes the newly added Q4 admission contract and is not restricted to initial HEAD.

### P2: finite-history tensor loader ignores per-shard axis identities

`scripts/audit_chapter2_finite_history_signal.py:31-42` adopts starts and demographic_seeds from the first shard, and verifies subsequent array shapes only. Equal-length reordered axes in later shards silently enter the first shard's labels. Reproduced with 16 synthetic exported JSONs, eight unique histories per shard (128 total), three starts and eight repeats: shard0 starts [.2,.5,.8], other starts [.8,.5,.2], each tensor filled by its own labelled starting value. `_load` succeeds and reports start .2 while returning .8 at index [0,8,0]. No hash admission mocked; no research campaign executed; this does not claim committed exports are malformed. The misalignment can change the start-by-history variance component and split-repeat comparisons. The standard bridge aggregator already checks starts/demographic_seeds/arms equality at `summarize_model3_ch2_bridge_shards.py:178`; this diagnostic loader needs equivalent checks and exact tensor-key coverage before merging. No fix yet.


## Additional logical review and authorized repairs

- Finite-history signal loader: equal shapes did not guarantee equal start/demographic/arm axis labels. Reversed starts in 15 of 16 synthetic shards were silently aggregated under first-shard labels. The current loader now requires identical ordered axes, unique/nonempty labels, exact arm/model tensors. `tests/test_finite_history_signal_axes.py`: 6 checks including correct far-minus-near orientation. No original result changed; no current source-pin hit for original SHA a2f130a2098dfc1e216c9184ad030e8f1b28e6ea895596496862213a782e9161.

- Prospective intermediate grid5 summary (`scripts/summarize_model3_ch2_bridge_prospective.py`, original lines 94-116): self-comparing input.json did not establish design identity, and counting folders did not establish complete cells. A 32-case synthetic complete grid replacing near/start.8/history1 by a duplicate .2/history1 returned `prospective_bridge_summary_complete`, 32 checked, occupancy .75. Missing output had become apparent biological extinction. Current code checks unique exact Cartesian design cells, canonical producer IDs, case/receipt manifest hashes. Six regression tests cover complete, duplicate, missing, foreign, wrong manifest and genuine recorded extinction; recorded extinction policy unchanged. Original SHA c1c54c064aba7cb4d8c9a9c520b9339fdf502faefc82832553b045ef536adfd0 / Git blob 26e534f190182379a4927456caa3c443d59e7db6 had no current-source pin hits; q3_triangle_hold's frozen_source pin has different SHA and remains untouched. This is a structural admission defect of intermediate grid5, NOT evidence the final 24576-case campaign or archived scientific results are invalid.

- Deferred metadata mismatch (`scripts/audit_model3_reduced_pde_selection.py:149-151,174`): numerical velocity uses Cov(i,w)/mean(w), while returned equation says (w-mean_w)p. Correct normalized expression is dp/dt=(w/mean_w-1)p + D*d2p/di2 (D=0 in tested frozen operator). Tiny no-trajectory evidence for access .2/left4: normalized 0.0027652711235113406; multiplying fitness by 7 gives 0.002765271123511339. Unnormalized covariance instead changes 0.010016649321961404 to 0.07011654525372983. Historical closeout receipt pins source SHA 5be1014a77354c32a47ff1ddbfff9bf9d84e6d6d1698fc354bff0cd2d1d9d74b; parent directed preserving code and historical JSON relationship pending separate versioned correction. Correct normalized equation already appears in trajectory audit and closeout documentation. This is equation-label inconsistency, no changed numeric science.

Latest focused suite: 42 passed (five verifier/loader regression modules). No campaigns run.

Independence notes: kernel channel v2/v3 independently reconstruct with scipy/moment laws, enforce 48 rows/192 unique slots and finite scalars; not the old empty kernel-expression gap. Source cluster aggregation correctly keeps signed-vector-before-TV and conditional-TV separate. Exact clonal demographic null integrates source reproduction plus independent Poisson census law; it explicitly disclaims closing the evolving genotype process. Source replay parity and self-consistent hash receipts alone are not independent evidence of ecology or mechanism.


Additional P2 pending repair: summarize_chapter2_long_horizon_stationarity.py lines 45-48 derive histories/starts from observed rows, and summarize never checks frozen full domain. Using actual frozen chapter2_long_horizon_stationarity_20261003.json, synthetic files containing just 1 history x 1 start x 6 checkpoints and 2 mutation trajectories returned complete_prospective_long_horizon_stationarity with both stationarity claims true. Actual contract specifies all128 parent histories x3starts and full mutation factorial. No hashes mocked; no originals modified. Historical frozen_source receipt pin differs from current SHA 01a87b6e0065af9451e79989bfde81be2e4f04b3f0f487918cc8dd2099c727d0. Report only pending parent direction.

### Long-horizon inventory repair completed
The prior pending finding is repaired in summarize_chapter2_long_horizon_stationarity.py. Admission now requires the frozen parent-history x start x checkpoint product and the mutation regime x capacity x founder seed x demographic seed x visitor-history product, including checkpoint completeness, uniqueness, and declared mutation parameters. Six malformed fixtures fail closed; one complete fixture succeeds. Combined six repaired pipeline entrypoint suites: 49 tests passed. Frozen scientific payloads and historical source pins were not rewritten.

### Final eleven audits fully read
Initial-clock transfer uses train-only scaling and explicitly calls repeated-seed context transfer non-independent. Commons pilot and conflict replay retain the originally exposed 16 histories; the exact 384-path hash is reproduction evidence, not new confirmation. Genome accounting and matched-operator decomposition close signed identities, explicitly not unique causal allocations. Izu parentage is structural linkage and explicitly does not authenticate field claims from self-declared hashes. Joint G-beta is tested against a distinct exact density transition and declares its approximation. Stochastic scaling is a finite-K necessary-condition screen plus a bounded no-visitor algebraic counterexample, not a universal diffusion proof. No new confirmed production-result error arose from these eleven source reads. Coverage is source inspection, not running every research campaign.
