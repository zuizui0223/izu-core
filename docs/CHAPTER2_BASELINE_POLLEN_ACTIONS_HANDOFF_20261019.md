# Frozen baseline pollen pilot: execution handoff

## Scope

Use the existing 384-trajectory exploratory design without changing seeds,
parameters, allocation, endpoints, or hypothesis direction. Source branches:

- `analysis/ch2-baseline-pollen-factorial-20261019` at `d2dbbc776dacb8d39b8cc73c8d5219dcc2cb8a41` (protocol).
- `analysis/ch2-baseline-pollen-limit-2x2-20261019` at `167d48441d58873369e54709be3d3f9f8b63a19e` (producer, independent endpoint reader, tests).

## Duplicate execution check

On 2026-10-19 the two branches contained the protocol/implementation but no
384-trajectory result files. Neither branch had a matching PR or Actions run
in the queried branch histories. No corresponding release was found in the
latest 15 releases. These checks do not establish that an off-GitHub run never
occurred. The Actions artifact inventory request failed and is not counted as
a completed search.

The user identified the other task as
[遐皮ｩｶ險育判縺ｮ荳譛ｬ蛹望(https://chatgpt.com/c/6ad38e91-6aac-83ec-a905-8018388e2b86).
Its status was `systemError`; both the thread reader (rate limited) and browser
(conversation could not be loaded) failed to expose its execution/results.
Therefore the duplicate-run check is **unresolved**, and this PR does not
launch the scientific pilot. Read the existing task or recover its saved
results first. An existing completed run should be audited, not repeated.

## Ready execution path

After resolving the duplicate-run check, add `run-baseline-pollen-384` to this
same-repository execution PR once. The workflow only responds to that label
on `execution/baseline-pollen-actions-20261019`; ordinary pushes do not launch
it. A global concurrency group prevents simultaneous workflow jobs. It does
not prevent a later deliberate repeat; inspect prior runs before relabeling.

The workflow checks frozen source hashes and tests, runs the two 192-path
shards, requires the full 384 allocation, then runs the independent endpoint
reader and founder-cluster bootstrap. It retains source SHA, environment,
protocol, raw endpoints, summary, audit and checksums for 90 days; partial
files are also uploaded on failure. Successful completion requires `audit.json`
and the audit PASS status, not merely the presence of an artifact. Execution
is capped at 45 minutes on one Ubuntu runner. No automatic retry is configured.

## Interpretation

The target is the difference in decline-minus-control A responses between
weak and strong baseline limitation, separately for initial A = 0.3 and 0.5.
The independent units are 12 founders, not 384 trajectories. Intervals are
exploratory founder-bootstrap intervals, not a registered confirmatory test.
Report all-start survival and survivor-conditioned trait denominators.
A small terminal contrast can reflect fixation or shared allele bounds and
must not automatically be interpreted as weak selection. The baseline
manipulation changes pollen effectiveness; activity decline is the separate
intervention. Calibration values are not observed evolutionary responses.

## Prelaunch review corrections

The inherited producer omitted protocol-specified genetic support and
reproduction readouts. It now retains allele values/counts and genotype-mean
variance for M/I/A at initial, fork, and terminal censuses, plus expected
outcross/raw-self/viable-self production and realized selfed/outcrossed
recruits for all updates. The audit checks these records against saved
means, q and occupancy. An observation-only native-transition equality test
checks that recording does not change the population update. The frozen
protocol and five pinned native operator files are unchanged.

Empty-prefix aggregates now return null with an explicit denominator rather
than invalid JSON NaN. Prefix extinction time now records its actual first
census. Founder-level surviving-pair counts and the equal-founder-weight,
baseline-specific survivor-conditioned interaction estimand are exposed.
Seven focused tests pass locally, including synthetic extinction and
record-corruption checks. These are technical checks, not the 384-path pilot.
