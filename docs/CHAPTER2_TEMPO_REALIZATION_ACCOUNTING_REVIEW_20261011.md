# Review record: archived tempo realization accounting

**2026-10-11.** These are independent assistant-agent implementation and scientific reviews, plus independent numerical recomputation. They are not external peer review, new biological observations, or an independent experimental cohort.

## Native accounting implementation

**Verdict: APPROVE, no critical or important blockers.** Reviewed commit `303c7f6a41a8f8273e8595b6d2863e85e1113e4a` against the bounded task specification, original native reproduction/recruitment source and existing integrity helper. The reviewer did not implement the code or rerun biological histories.

The review verified full maternal/paternal/self genetic weight, the independently indexed donor/mother pair expectation, actual retained parent IDs, exact child-ID coverage, genotype means, 100/300/400-update sums, endpoint indexing, four-repeat then sixteen-profile aggregation, and propagation of undefined empty-population means. It found the cohort admission, source rehashing, stable ordering and JSON serialization consistent with the specified scope.

The reviewer independently checked the Poisson kernel against SciPy at very small intensities, values around 48, the observed minimum-intensity region, and intensities 80–800. Maximum absolute differences were 4.72e-15 for the probability below capacity, 4.62e-14 for expected shortfall, and 2.42e-13 for expected next census. A synthetic sequence with 173 available transitions retained the correct unavailable late/full windows through four-repeat aggregation. No full test suite or new history was run by this reviewer.

The review preserved two limits: archived parents/final alleles do not identify separate mutation and homolog-draw effects, and receipt/source consistency checks do not replace the original archive-preservation record.

## Independent archive calculation

The independent checker was written and executed before its author read the native-accounting implementation. Its source bytes are preserved in [the independent audit script](../scripts/audit_chapter2_tempo_realization_independent_20261011.py), SHA256 `86dc521c9e1944a7fc0279fcb4b441aedf537b6c251b14e200a0fcbdd8ffa019`.

It verified all 1,024 case hashes and original receipts, all 16 manifests, 410,624 diploid censuses, 409,600 updates, and 819,200 trait-update accountings. It independently reconstructed adult, retained-parent and child means using archived IDs/alleles. Expected-response fields were declared archive inputs; the checker did not replay native reproductive expectations. No case or update was filtered, and no new biology, bootstrap or hypothesis test was generated.

The complete independent JSON is preserved under deterministic gzip in [the independent result](../data/results/chapter2_tempo_realization_independent_audit_20261011.json.gz). Its original JSON SHA256 is `18ece42b333427c1ee93e0b9620ec45075eb1ca7925c4450cd3733a448fed6ba`.

The separate native replay subsequently verified every saved expected I/A response and every used delivered/outcross/viable-self quantity against the unchanged native source, with zero discrepancy for those fields. The [cross-calculation receipt](../data/results/chapter2_tempo_realization_comparison_20261011.json) reports exact agreement for 34,368 case/profile/arm/paired-profile/paired-setting component values, with 1,024 matching raw/receipt hash pairs. This does not claim independent recomputation of every original secondary readout field.

## Scientific report

**Verdict: APPROVE, no substantive numerical or interpretation blockers.** The independent numerical analyst reviewed [the scientific report](CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_20261011.md) against its independently completed calculation and the completed native result. The reviewed substantive draft SHA256 was `b14f86b5cc706be016571ee32d17ea9043b613d940f2fb6392e07cdbaed23c07`.

All 112 displayed genetic numerical entries matched the independent result to six-decimal rounding (maximum discrepancy below 5e-7). The reviewer verified all sign-count statements, the founder-relative distinction, phase windows, original event versus terminal-state descriptors, conditional source-path interpretation, demographic inventory, S0 algebra and limits. The report retains all eight settings and does not promote the decomposition to causal mediation, a survival-equivalence finding or a new prospective confirmation.

Two recommended precision edits were accepted: the population table explicitly labels the uncapped seed intensity, and A-only explicitly requires an assurance event as well as the absent investment-decrease event. A displayed numerical-error bound was also rounded to 1.42e-13. These edits alter no underlying quantity or scientific conclusion. The final report byte identity is recorded in the [artifact receipt](../data/results/chapter2_tempo_realization_receipt_20261011.json).

## Integration scope

The original frozen design, native source, 1,024 raw case/receipt pairs, primary readout, original endpoint audit, original figure, October10 machine-readable snapshot and active manuscript remain unchanged. The new current evidence addendum updates availability and scope separately. The complete annual accounting is a saved standalone file; its explicitly identified Git projection retains all case/window/profile/arm support and omits only annual census/update arrays.

Focused implementation tests, artifact identities and preserved-source checks are recorded in the artifact receipt. Required repository CI checks are evaluated on the final pull-request head before integration; their live results are GitHub checks, rather than future results asserted in this pre-integration record.
