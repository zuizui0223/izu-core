# Q3 triangle execution package review

Fresh whole-package review of staged source/workflow against `CHAPTER2_Q3_TRIANGLE_EXECUTION_DESIGN_20261014.md` and its implementation plan. Reviewer: independent `q3_triangle_whole_review` agent. Review was read-only; no native calls or actual PCG/permutation draws. Base is PR #515 `914b5040ff1dd75378277c643bad87c0d9132a62`; PR #516 previously published partial implementation `ee976a9ff574ae943a2d0c9583de2ea8d8145830`. The current source includes the implementation and fix pass below.

## Findings and dispositions

No Critical finding; three Important findings; no separate Minor finding.

1. **Partial trajectories were only held in RAM until an arm completed.** Fixed with an exclusive per-arm journal containing each census, all five individual fields, parents, year, assignment and provenance. Each checksummed record is flushed and fsynced before the next transition. The journal is deleted only after an immutable final NPZ is durably written and hashed. An interrupted final journal record can be ignored while recovering preceding intact records. Two active journals are each capped at8MiB within the existing128MiB metadata allowance; total pre-execution metadata plus later receipt reserve is capped accordingly. The interruption test first failed because no journal existed; after the fix it recovers both the original census and the completed synthetic transition with parents.
2. **Archive endpoints reused the replay calculator.** Fixed with a separately implemented archive algorithm: it constructs each original-prefix/future census by its year and searches all length20 windows, independently of the replay calculator's streak logic. A regression test deliberately corrupts the replay calculator and verifies the archive answer, intervention-crossing window,19-versus20 boundary and event retained after extinction. The test first failed on the missing independent implementation and now passes.
3. **Timers started after setup/download rather than at job start.** Fixed by reading the current job's authoritative `started_at` through the GitHub Jobs API before checkout/setup/download. Both runners convert this epoch into a monotonic deadline, include a30-second cushion, and reserve3 minutes for final upload; shard work additionally reserves2 minutes for packaging. Setup/download/upload steps have explicit timeouts. Insufficient remaining time prevents native work, including fixture calls. Pure tests first failed for the missing deadline calculation; they now prove that5 minutes of setup reduce a15-minute job to390 seconds of remaining processing budget after reserves, and that an expired fixture budget spends zero calls.

The reviewer confirmed80 synthetic/pure tests at review time. The complete fix-pass suite is84 passing tests under Python3.10. No second review was substituted for the failure-first regression tests. The full GitHub CI for the final published head is still required.

## Evidence and limits

- Actual frozen-input admission verified315 registered original/source/campaign members,11,613,772 bytes including its receipt, zero extracted bytecode and zero native updates.
- The independent review found the remaining approval/hash, fixed-inventory, reservation, extinction and statistical comparison logic conservative. Existing CLI artifact extraction and workflow upload path roots matched the expected transport layout.
- Four synthetic fixture updates are scheduled only in the approved campaign's shard0, with a durable reservation; scientific production plus replay remains6,687,360 updates. Scheduled total is6,687,364, within the frozen6,687,392 ceiling.
- The durable journals add unbenchmarked I/O. The preflight's60–100 runner-minute estimate is not a measured guarantee; the300-minute hard job budget remains unchanged.
- No actual frozen-native triangle execution, Linux/Python3.11.14 performance,1.6GB transfer under timeout, or activated release cycle was tested. These are deliberately deferred to the concretely approved campaign, not asserted by mocks or green CI. Technical failures preserve available records and remain HOLDs; infrastructure loss or interrupted upload cannot be represented as a successful scientific result.
- Original primary and earlier confirmation-margin uncertainty remain unchanged. No activation file exists and this review is not permission to run biology.

Relevant platform references used by the reviewer: [GitHub whole-job timeout](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idtimeout-minutes), [gh run download](https://cli.github.com/manual/gh_run_download), [upload-artifact](https://github.com/actions/upload-artifact).
