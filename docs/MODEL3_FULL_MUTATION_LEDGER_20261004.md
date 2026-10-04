# Full mutation campaign execution ledger

Plan: `docs/superpowers/plans/2026-10-04-model3-full-mutation.md`.
Execution counts and shared-founder refinement: its `-execution.md` addendum.

## Completed implementation checks

- Sparse/tensor inheritance preserves the full joint genotype distribution.
  Twelve operator comparisons against the original dense implementation passed
  at absolute tolerance 1e-10 across both selfing timings, mutation on/off,
  and the three mutation operators. This is an algebraic implementation check,
  not evidence that diffusion approximates jump mutation.
- Campaign tests check the common visitor continuation after period 200,
  absence of plant immigration, declared case counts, retention of stage 1
  within stage 2, corruption rejection, and summary direction/allele columns.
- The initial 1,024 core cases completed. The declared precision gate passed
  in only 2 of 8 setting/rate/endpoint groups; each group requires both focal
  traits. Therefore the fixed 64-history, 8-repeat maximum was launched.
- The 128 projected-founder ABM controls completed. These four histories
  support a matched numerical comparison, not population-level precision.

## Final execution evidence

- All 4,096 core cases completed; all prespecified precision groups passed
  at the fixed maximum. No further seeds or parameter changes were used.
- All 144 density cases completed. Positive-mutation refinement failed in
  all 16 jump conditions and 8 of 16 heat conditions. Zero-mutation cases
  all passed. Quantitative positive-mutation bridge claims remain withheld.
- Matched ABM/density/heat contrasts are retained with explicit limitations.
- Final verifier accepted all 4,368 cases and 25 source files, including
  declared task identities, hashes, population traces and saved checkpoints.
- Full interpretation is in `MODEL3_FULL_MUTATION_RESULTS_20261004.md`.
  Raw archive and compact summary are prepared separately; see that report.

## Provenance ruling

Source fingerprints and a source archive were captured before execution.
Runtime package versions were recorded during execution, not before launch,
in `runtime_observed.json`; do not describe them as a pre-execution snapshot.
The documented commands explicitly limited BLAS/OpenMP threads to one.
The summarizer is outside the simulation snapshot and has been extended to
report allele retention, change from founders, last-100-period change, and
matched benchmark contrasts. Archive its final version with the results.

## Interpretation boundaries

The three traits evolve jointly. Capacity is 48 in this campaign, so it adds
no capacity-scaling evidence. Time is in uncalibrated reproductive periods.
Survivor-conditioned trait differences are distinct from persistence.
Finite-horizon memory is distinct from alternative stable endpoints.
Terminal mean grid agreement is not full-distribution convergence.
The continuous-genotype integral formulation and mutation PDE component
remain representations of the deterministic branch of Model 3.

Evolution Letters is a target for communicating a substantive evolutionary
prediction, not an acceptance rule for results. No settings, seeds or
precision thresholds are changed to obtain a stronger story.

## Independent implementation review

Read-only review found no evident engine defect. Two postprocessing findings
were repaired: summary readers now check declared task identity as well as
archive hashes, and grid summaries retain both 5-to-7 and 7-to-9 differences.
A mislabeled-but-hash-valid receipt regression failed before the repair and
passed afterward. The final signed three-way comparison is also tested.

The frozen runner does not verify an existing source ZIP on resume. Its
25 archived members were therefore verified externally against the source
manifest, including exact member names. The final campaign verifier repeats
that check. Do not edit the active simulation source merely to fix a future
resume safeguard; retain the original snapshot for this campaign.

Conditioning: arm means describe each arm's occupied replicates. Paired
effects describe jointly occupied replicates averaged within history and
then equally across histories. They are not generally the difference of
the marginal arm means when survival differs. All are descriptive.
# Additional precision preparation

Subsequent steering: user requested estimating necessary grid resolution before
additional full computation. The17 campaign is pending and will not start
automatically. The cheap analytical operator screen was planned, tested and
run separately; it motivates investigating feasible numerical representation
before more full-grid campaigns. See MODEL3_RESOLUTION_SCREEN_20261004.md.

The user requested additional precision during the live 13-node continuation.
The fixed 17-node plan and separate runner are prepared, preserving all 32
conditions and all biological rules. The 13-node source snapshot was rechecked
and remains unchanged. The 17-node campaign has NOT started: it requires the
complete verified predecessor and a reviewed single-worker resource probe.
Seventeen nodes are a refinement stage, not an assumed final resolution.

TDD: initial five tests failed at missing-module collection, then passed.
Independent review identified missing provenance checks in summary and unsafe
recreation of a predecessor manifest. Three regression tests reproduced those
failures; fixes now require existing provenance and verify own archive and
predecessor identity. Eleven combined 13/17-stage tests pass. No full campaign
or ecological conclusions are inferred from these infrastructure tests.

## Joint compression propagation diagnostic

Ruling: first test dense-update/recompression, not a new biological approximation.
It isolates accumulated truncation error but offers no scalable implementation;
failure would reject the representation before a large solver investment.
Forty-period/nine-node/eight-condition design was saved before execution.
TDD: missing-module failure observed, implementation added, six tests passed.
All eight admission cases completed and passed; worst path L1=3.3495e-7,
mean-trait gap=2.8312e-8. Full metrics and hashes retained. Long-horizon and
direct compressed-operator gates remain open. Original13 run verified live at
8/32; no frozen source touched and no17+ full campaign started.

## Thousand-period compression propagation gate (running)

The same eight cases now run for1000 periods under the separately saved
2026-10-04-model3-compression-long plan. The40-period source archive was saved
and hash-checked before extending the diagnostic runner. Per-step tolerance
and trajectory admission thresholds are unchanged. Checkpoints at200/400/1000
retain both distributions; final case receipts hash their NPZ files. The long
run has its own source archive and output directory propagation1000.

TDD: an undeclared-horizon test failed before adding horizon admission and
passed afterward;19 compression/inheritance tests pass. The running session is
57083 (one worker/one BLAS thread). This is an error-propagation experiment,
not the high-resolution production campaign and not a compressed time solver.
No long-horizon pass is claimed until all eight result receipts are inspected.

## Exact selfing transform for future compressed solver

Implemented the predeclared local selfed-birth operator outside the frozen
model3_island package. It retains the joint core and transforms its factors;
no independent-trait assumption or altered mutation law. Initial tests failed
at missing-module collection; seven new tests then pass against the original
full-joint inheritance operator. Combined compression/inheritance suite26 passes.
Still not a complete solver: outcrossing, ecology weighting and rank control
remain. Long-run probe sources reverified unchanged during its execution.

## Exact outcross component and remaining rank-growth gate

Implemented one visitor channel's outcross inheritance directly on Tucker
factors/cores, outside all frozen model sources. Six tests initially failed
on missing module and now pass against the original full operator, including
correlated inputs, unequal grids, signed bases and allocation-budget rejection.
Combined relevant suite32 passes. No biological law changed. Exact outcross
algebra multiplies parental ranks; high-rank output is explicitly refused.
Nonlinear ecological weighting, channel summation and rank/error management
remain required before any complete high-resolution solver can be claimed.

## Outcross exact QR contraction

Added an optional no-truncation QR contraction path. Observed tests fail on
missing orthogonalize arguments, then pass after implementation;38 relevant
tests pass. The contraction path and raw/final array sizes are checked before
large core allocation. A4096-to27 core-size test validates exact re-expression,
not biological independence or approximation. Full high-resolution feasibility
is still open. Three long-probe result receipts and NPZ hashes checked; all
three pass, five remain. Sessions57083 and77498 verified live this turn.

## Ecological weights preserving joint associations

Implemented the separately planned exact phenotype grouping and joint marginal
calculation, retaining frozen pollen delivery, costs, reproductive timing and
inbreeding depression. Eight tests first failed at missing module, then pass
against the dense reference ledger. Combined suite46 passes. Components still
need integration and full trajectory/resource validation. Long compression
probe now4/8 complete and passing; original13 run10/32 complete, both live.
No frozen production source edited or17+ full-grid campaign launched.

## Integrated exact compressed-basis step

Implemented the weighted joint density and QR channel sum, then wired ecology,
selfing, outcrossing, mutation, survival and capacity retention. No singular
values discarded. Initial integration tests failed at missing module;15 new
tests now pass, including four12-step far-history comparisons with adult
survival. Combined61 tests pass. The adapter explicitly restricts to the
campaign's evolving assurance/no-immigration scope. Full-grid ranks remain a
scalability obstacle; no high-resolution success claim. Both live source
manifests remain intact. The separate1000-period truncation probe has5/8
completed cases passing,3 remain; it is not this newly integrated solver.
