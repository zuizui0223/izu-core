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

## Joint-core rounding utility

Implemented the preregistered core-only HOSVD reduction with an analytical
truncation/rescaling L1 bound, separate from floating-point error. Seven tests
failed at missing module before implementation and now pass. No implicit
negative clipping and no trait-independence closure. Positive mass is restored
by scaling, but nonnegativity is not guaranteed; full trajectory validation
must quantify that error before adoption. Existing dense-roundtrip long run
has6/8 cases complete and passing,2 remain; its sources remain untouched.

## Integrated stagewise rounding probe started

Added an optional rounding hook at parent weighting, inherited births,
sequential channel summation and retention/survival. Test first failed on the
missing hook, then passed against the original full step with error and
negative-mass checks. Combined relevant suite69 passes.

Predeclared n5/40-period/eight-case admission is now running in session46733,
with per-stage receipts and every-period full-reference comparisons. Its
source archive/manifests are frozen; do not edit compressed solver modules
during this run. Existing13 and1000-period source manifests also reverified.
Long dense-roundtrip diagnostic has7/8 completed and passing, last case running.
The new integrated solver probe has no completed-case claim yet. Its outputs
are under outputs/model3_precision_feasibility/integrated_n5_40.

## Long dense-roundtrip gate completed and audited

Session57083 terminated successfully. All8 cases pass all1000-period thresholds.
Recomputed checkpoint L1 errors at200/400/1000, verified every NPZ/source hash
and expected condition identity, and retained all raw data in a34,058,669-byte
archive. Max path L1=1.0443221e-6; max mean-trait gap=8.1150344e-8; mass gap
5.6843419e-14. Compact audited result saved in data/results. This proves only
the declared one-history/n9 dense-update-roundtrip gate, not integrated solver
or high-resolution adequacy. Integrated session46733 confirmed live, first
case not yet reported;13-node session77498 at12/32 and still live. Do not
restart either valid run or alter their frozen sources.

## Performance diagnosis (no live source mutation)

Profile reproduced14s n5 first-step latency,99%+ in outcross contraction.
Fixed-rank paired benchmark isolated default einsum planning as the dominant
cause: default all-at-once82.701s, budget-aware binary path0.001288s, max output
difference1.7764e-14. Original integrated session46733 still live; do not edit
its solver sources. Next action: isolated corrected-source regression and
admission run, preserving original output/source identity and failed speed
evidence. Rank growth/high-grid feasibility remain separate unresolved gates.

## Isolated fast-path admission completed

Verified archive copy used to protect both live runs. Two planner-budget lines
changed only in candidate. Regression observed failing path then green;70
candidate-local tests pass. Eight identical40-period n5 cases pass in23.518s
total. Max path L1=1.3217425e-8, trait gap=1.7097166e-9, relative negative
mass=2.6360477e-11. Endpoint/source hashes and recomputed final errors agree.
Candidate patch plus provenance/metrics committed; full source/tests/raw bundle
retained with SHA256. Original frozen solver files have not been changed.
No claim of integrated1000-period or high-grid adequacy yet. Fast run session
19685 exited0; old admission46733 and13-node77498 remain live.

## Corrected solver long gate launched; higher-grid shape screen

Candidate runner extended under a separate fixed1000-period plan. Horizon
guard test observed red then green;71 local tests pass. Eight-case long run
session67923 started with unchanged biology/error thresholds. Its archived
manifest checked. Original live-run manifests also unchanged. Runner patch,
launch manifest and plan retained in tracked files; do not edit candidate
solver sources until its live run terminates.

Symbolic shape screen (no biological runs) shows schedule fixes alone cannot
handle assumed40-rank parents at33/65 nodes. Need bounded child-factor reduction
before core contraction, not unbounded allocation or a claim that65 is enough.

## Pre-contraction child-factor reduction bound

Added separate model3_child_factor_bound module outside all live source sets.
Plan fixed first, tests failed on missing module then passed. Nine focused
tests plus7 core-rounding tests pass. The analytical spectral bound is checked
against actual small-tensor errors and records retained ranks. This is not yet
an integrated solver modification or evidence of high-resolution efficiency.
Original13/slow-admission and candidate-long manifests all reverified. Latest
observed13 completion14/32; corrected integrated1000-period run3/8 complete and
passing, fourth running. No live run restarted or frozen source altered.

## Integrated long gate closed; snapshot compression limitation retained

Session67923 exited0. All8 n5/1000 integrated cases pass unchanged thresholds;
independently checked conditions, records, source/NPZ hashes and checkpoint
errors. Raw/source archive16,538,946 bytes retained. Max L1=2.3821655e-6,
mean-trait gap=2.7741491e-7; summed case runtime421.344s. This is solver accuracy,
not grid convergence or completion of ecological comparison.

Real n9 baseline200 child-factor probes also all8 pass their algebraic error
check, but two near cases retain full45x45x45 child directions. Retain this
failure to reduce ranks: no universal high-grid speed claim. Probe plan,
results, input hashes and exact source bundle retained. Live original13 and
slow admission sources remain unchanged.

## Nine-node admission running

Fixed n9/40 plan before outputs. New guard/founder tests observed red then
green;73 candidate-local tests pass. Founders remain identical five-node
genotypes/counts embedded at n9. Numerical tolerances unchanged; explicit
array budget16million values for one diagnostic worker, not a peak-RAM claim.
Session14030 runs the first n9 diagnostic; no case success claimed yet.

Measured another diagnostic-only bottleneck: full-array reconstruction omitted
einsum scheduling. Fixed-shape timing0.587s versus0.000824s, relative L1 difference
8.96e-16. A separate runner/output variant changes only that reconstruction
expression to optimize=True; solver sources unchanged. Session32212 runs it,
first case20/40 observed with L1=5.50e-10. Both source manifests verified; retain
both identities and do not confuse reconstruction speed with solver accuracy.
The new variant is scripts/audit_model3_rounded_integration_fast_reconstruct.py
inside the isolated candidate. Its diff is retained in tracked data/results.

## n9 diagnostic output-path failure and recovery

Session32212 terminated exit1 after first case40 periods, at NPZ output:
FileNotFoundError for a264-character Windows path. Directory existed, but no
case receipt was saved; do NOT count this as a completed passed case. Preserved
old source archive/manifest and terminal-error record. Added output-directory
helper and short-path regression (red then green);74 local tests pass. New
case path204 characters; actual NumPy write verified. Only the diagnostic
output path changed; solver/biology/tolerances unchanged.

Restart authorized by observed terminal failure, not a timeout. New session
6935, output candidate/gate_n9_40. First two40-period cases now saved and report
passed. Old original13/slow-admission/slow-reconstruction processes remain
separate live handles; their source files were not altered. Failure/recovery
provenance and short-path patch are retained in tracked data/results.


## Verified n9 integrated admission and long gate

All8 n9/40 cases pass;33 frozen source hashes, case JSON and NPZ hashes
verified. Reconstructed endpoint arrays agree with saved arrays. Maximum
path L1=3.34719484e-7, mean-trait gap=2.56282306e-8.
Receipt: data/results/model3_fastpath_n9_verified_20261004.json.
Archived complete outputs plus long-gate runner/tests.
Ruling: admit n9/1000 on same8 cases/history76001, unchanged numerical
tolerances and biology, single worker. This is solver error admission,
NOT grid convergence. Separate runner preserves all earlier source snapshots.
Admission guard test RED (undeclared horizon), then GREEN; candidate75tests
passed. Long run session58342, output fastpath_candidate/gate_n9_1000.
Original n13 run session77498 remains live,16/32 last verified.
Previous goal turn: progress (n9/40 completion evidence changed next action).


## 65-node single-channel resource measurement

Previous goal turn: progress, n9 long gate launched after verified admission.
Current n9 long session58342 live, firstcase100periods L1=5.47e-10.
Eight n9 period200 snapshots embedded exactly into65-node allele support;
apply65-node mutation and spectral child-factor reduction, without full
genotype tensor or child-core contraction. All8 measured within2million
values per raw factor. Largest raw factor1,450,020 values; reduced child
core at most91,125 values. This is evidence that initial high-grid child
factors are manageable, NOT full solver or long-time high-grid feasibility.
Rank<=45 partly reflects inherited nine-node support; later generations
can increase rank. No ecological or grid-convergence claim follows.
Next unresolved work includes weighted ecological integration, selfed
transitions and sustained rank/error control at high resolution.
Sources and outputs archived; receipt data/results/model3_highgrid_resource_20261004.json.


## Bounded ecological weighting before expanded-core allocation

Previous goal turn: progress (65-node child-factor resource measurements).
Added isolated model3_weighted_factor_bound component; no frozen running
solver sources changed. It SVD-reduces raw weighted factors before forming
the output joint core. Bound uses implicit expanded-core Frobenius norm
sqrt(p)*norm(core), factor spectral norms, telescoping residuals and
sqrt(number of physical states). Preserves joint dependence; signed bases
allowed. No positivity or floating-roundoff guarantee.
Observed missing-module RED, then4 component tests GREEN including actual
nonzero truncation bounded against dense calculation; candidate79tests pass.
This is not yet integrated/admitted on ecological long trajectories.
Full raw weighted-factor allocation/SVD remains a possible65-node bottleneck;
next investigate weight-function reduction with an explicit error bound.
Long n9 run session58342 remains live: firstcase400periods L1=1.24581e-9.


## XY weight reduction and65-node ecological weighting admission

Previous goal turn: progress (bounded weighting module,79tests).
Added weight-function SVD truncation using sigma_next times a triangle-
inequality L1 bound from the absolute core/factors, including assurance.
Half absolute budget allocated to weight truncation; remaining budget to
factor truncation. Observed resource-guard RED then GREEN;80tests pass.
Old allocation test cap reduced100->50 because new weight compression
correctly makes the former100-value case feasible; input guard still tested.
All24 snapshot checks (8conditions x self/donor0/recipient0) at65nodes pass.
Maximum relative L1 upper bound including off-support output1.06201e-12.
Checks use coarse n9 period200 densities embedded exactly, NOT evolved
high-grid densities. This admits ecological weighting algebra/accuracy on
these inputs only. No high-grid trajectory or convergence claim.
Archived input hashes, sources and outputs in weight65_verified.zip.
Next: integrate bounded weighting and child factors in isolated solver,
validate against same-grid dense reference before high-grid trajectories.


## Bounded reproduction integration and first n9 long completion

Previous goal turn: progress,24 high-grid ecological weight checks.
Integrated isolated bounded_step with bounded weight/child factors, exact
selfing, rounded channel sums, capacity and survival. No live original
solver files changed. Local receipts do not imply a global propagated
error bound; same-grid full-state comparison is required.
Observed module-missing RED then8 repeated-step settings GREEN. Candidate
suite88tests passed; root focused13tests exit0. Supports evolving assurance,
no plant immigration, all3 mutable loci; fixed assurance is excluded.
Bounded n9/40 eight-case gate launched session77050; frozen sources at
fastpath_candidate/bounded_n9_40. Firstcase40periods passed L1=5.86135e-10.
Original corrected n9 long session58342 firstcase1000periods passed;
verified saved NPZ hash and1000 records. Remaining7 pending.
Original n13 refinement session77498 remains live18/32 last verified.


## Exact marginal reference for high-grid admission

Previous goal turn: progress, bounded integration/tests and trajectory gate.
Implemented exact next-locus marginals from full joint input after nonlinear
ecological weighting. Reproductive factorization permits exact single-locus
birth marginals without allocating the full child genotype tensor; this is
NOT propagation of independent marginal populations. Validated against full
joint density for8 settings including absent visitors and adult survival.
Missing-module RED then GREEN, candidate96tests pass.
Prepared response-blind first65-node complete-step gate, contingent on all8
bounded n9/40 cases passing with source hashes. Scope is resource/marginal
accuracy only; full joint error and long-time/grid convergence unresolved.


## First complete65-node reproductive step

Bounded n9/40 all8 passed, source/NPZ hashes and endpoint reconstruction
verified; maximum pathL1=3.34720e-7. Archived complete gate.
First65-node full reproductive step completed all8 parameter combinations
in approximately0.86-1.08seconds each, ranks10/15/10. Exact same-input locus
marginal comparison maximum relativeL1=1.98297e-13; sources/NPZs verified.
Near/far initial visitor histories are identical, so these are not8 unique
isolation responses. This is numerical first-step admission, not biology.
Full joint positivity/error and sustained rank growth remain unverified.
Next gate: bounded multistep65-node resource measurement and tolerance
convergence, before production or ecological conclusions.


## 2026-10-05:65-node rank growth blocks second step

Previous goal turn: progress, first65-step verified. Ten-step resource probe
launched session29425, frozen sources in fastpath_candidate/ten65. First
assurance_cost_near_jump case fails at period2 by predeclared memory guard:
28,902,780 child-core values >16million. First step remains valid.
Independent diagnostic on saved first-step state reproduces failure in
bounded_outcross contraction, child ranks844/761/45; parent cores29/38/10
and34/42/10. This is output-core growth, not just poor contraction scheduling.
Other cases still live; do not classify unfinished cases as failures.
No memory/tolerance relaxation. Next numerical route is blockwise child-core
projection with directly evaluated residual bounds; plan recorded separately.
No65-node long-run or grid-convergence claim.


## Streamed projection component and actual-input measurement

Previous goal turn: progress,65-node second-step failure reproduced.
Added separate project_columns component. Gram identifies candidate bases;
acceptance uses direct blockwise residual, never spectral-tail subtraction.
Per-array allocation cap enforced; input callbacks must be deterministic.
Missing-module RED then four tests GREEN, candidate100tests pass.
Captured real failed child operands844x761x45 with hashes. Blocks width1/4/16
use binary contraction paths, measured0.016/0.015/0.063seconds respectively.
Source/input archive stream_input_verified.zip.
Actual-input projection started session99502, direct Frobenius1e-14 target,
width4 (180columns),16million allocation cap. Not yet accepted into solver.
Nine-node long session58342 now2/8complete/pass; far_jump500periods live.
65-node ten-step session29425 still live after firstcase resource failure;
no restart and unfinished cases not classified as numerical failures.


## Direct sketch alternative after Gram precision failure

Previous goal turn: progress, block implementation and actual probe started.
Gram actual probe session99502 terminated failed: direct residual3.78305e-9
at rank467 vs1e-14 target,109.406seconds. Failure preserved.
Separate direct Gaussian sketch+QR component uses fixed numerical seed997
and full block residual for admission, same allocation/tolerance.
Ill-conditioned control: Gram fails8.18990e-10; direct succeeds8.23584e-16
at rank8. This supports the numerical-conditioning diagnosis, not any
biological conclusion. Missing module RED then candidate103tests passed.
Actual captured-input direct probe started session84365; no solver adoption
until verified. Old frozen modules unchanged.
Nine-node long session58342 now3/8complete/pass; n13 session77498 remains live.


Actual direct projection session84365 completed: rank128, residual
4.90098661e-16 vs1e-14,73.047seconds. Output4,383,360 values instead of
28,902,780. Independently recomputed saved-array block residual matches;
NPZ hash verified and source/input/output archive retained. This is one
child-core projection, not yet integrated whole-step or trajectory success.
Next integration must split the declared local L1 budget between child
factor truncation and streamed core projection, converting Frobenius by
sqrt(physical genotype count) with orthonormal bases. Preserve old failures.


## Streamed outcross integrated under shared local budget

Previous goal turn: progress, direct projection of failed actual core verified.
Added separate streamed_child/integration modules, old running sources remain
unchanged. Half local channel L1 budget for child factors; remaining budget
for streamed projection after sqrt(physical genotype count) conversion.
Fallback when output exceeds cap or global contraction has >2-operand step.
Missing-module RED then forced-stream and repeated-step tests GREEN; candidate
113tests passed. No numerical/biological tolerance relaxation.
Previously failed65-node second near/jump step launched as separate diagnostic
session13293, frozen sources/output stream_second65. First child channel
completed78.75s within16million cap; remaining channels/full-step checks live.
This does not yet prove second-step completion, joint positivity or long-path
convergence. New local bounds are not summed into a global trajectory claim.
Original n13 refinement20/32 last verified; n9 long3/8complete with far_heat
700periods live and current L1 below gate.


## Stable full-joint comparison prepared

Previous goal turn: progress, streamed second-step integration launched.
Added separate joint_distance using common QR bases and direct difference
cores. Exact-arithmetic L1 upper bound; roundoff not bounded. No independent
locus closure. Missing-module RED then GREEN. Candidate116tests passed;
four focused distance tests subsequently pass, including equal marginals
but different joint structure. No high-grid trajectory claim from tests.
Second-step session13293 live, three child channels completed; fourth live.
Next after completion: verify source/NPZ hashes and compare full state under
a stricter declared numerical tolerance, preserving16million allocation cap
and all biological parameters. Precision must include joint-state agreement.


Second65-step session13293 completed/pass:334.078seconds, final core98/79/39.
Marginal relativeL1=4.41603e-13, mean-trait gap2.17604e-14. Independently
reconstructed saved marginals and verified all frozen sources/NPZ hash.
Archived stream_second65_verified.zip. This overcomes the demonstrated
second-step output-allocation failure, but five-and-a-half minutes per
step is not yet a feasible long campaign. Full joint tolerance convergence
and later rank/resource growth remain unresolved; no biological claim.


## Rank-start optimization and stricter joint-state admission

Previous goal turn: progress, complete second65 step verified.
Separate rank-hint component skips known failed trial ranks while retaining
fixed seed997, residual acceptance, allocation cap and adaptive escalation.
Missing-module RED, rank-hint tests GREEN; new fast integration tests RED
then GREEN, candidate130tests passed.
Actual captured contraction:73.047s->20.000s; q/core NPZ SHA256 identical,
not merely matching means. This single-case timing is not full-solver speed.
Prepared strict second-step gate: same saved first65 state/environment,
local1e-10 vs prior1e-8,16million cap. Full joint QR-distance normalized
L1 upper<=1e-5 plus existing exact marginal checks. No retuning on failure.
Launched session48191, sources/output fastpath_candidate/strict_second65.
This checks one step only, not accumulated high-grid trajectory convergence.
Original n9 long session58342 now5/8complete/pass; sixth near_heat_fv live.


## Strict tolerance resource failure and multiaxis route

Previous goal turn: progress, rank-start acceleration and strict gate launched.
Strict session48191 ended failed97.547s: rank74 storage ceiling, residual
7.82824e-13 >3.35389e-15. No full state produced; joint tolerance convergence
remains unverified. Failed sources/output and captured strict child archived.
Captured child shape1399x2145x100: single projected unfolding limits rank.
New basis-only projection avoids storing that unfolding; sequential different
mode projections commute and summed direct residuals bound joint residual.
Missing modules RED, candidate133tests GREEN. Test fixture corrected from
1000 to500 cap because original test could fit after one mode; no science
threshold changed. Separate actual-input multiaxis probe uses same strict
Frobenius3.3538949820031467e-15 and16million cap.
Initial diagnostic driver exited1 before computation: archive-loop variable
shadowed NPZ path with plan path. Fixed explicit input_path, retained failed
source archive, separate output multi_probe_run2; session84375 now live.
No allow_pickle workaround and no numerical failure counted for that IO bug.


## Seven long coarse-grid cases verified while multiaxis probe runs

Previous goal turn: progress, strict failure preserved and multiaxis probe
started. Verified34 frozen source hashes and all7 completed n9/1000 case
NPZ hashes. Recomputed200/400/1000 checkpoint L1 and reconstructed final
compressed arrays. All7 pass; max trait error9.35104e-8, max pathL1
9.00491e-7. Last far_heat case remains live session58342.
Progress receipt model3_n9_long_progress_20261005.json is explicitly7/8,
not full completion. Multiaxis actual session84375 confirmed live; process
23924 observed CPU86.58s and145MB working set. No restart or premature
convergence claim; awaiting declared component result.


## Multiaxis actual probe stops at final contraction scheduling

Previous goal turn: progress,7 long n9 cases verified. Session84375 now
terminal failed344.687s: no bounded binary final contraction path. Frozen
sources verified and failure archive preserved. Failure arises after mode
projection at final core assembly; no completed projected core saved, so
do not claim strict joint tolerance convergence. Next route: tile final
output contraction with independently checked bounded paths, without
raising memory cap or changing biological/numerical tolerances.
N9 last case session58342 confirmed live at700periods, currentL1=3.30411e-7.

## 2026-10-05: tiled final assembly and n9 long admission closure

Previous goal turn reread existing resolution evidence without advancing a gate.
This turn repaired the next available numerical obstacle without changing biology.
The original multiaxis projection failure is retained. A separate variant uses
recursive output tiles, rejecting nonbinary contraction paths and any retained
intermediate above the same 16,000,000-value ceiling. This ceiling is per array,
not a guarantee on total process memory. Tiling introduces no new truncation.
Two direct-contraction tests and the multiaxis direct-reference test passed.
The captured strict input is now running with unchanged Frobenius tolerance
3.3538949820031467e-15 in candidate multi_tiled_probe; no result claimed yet.

The integrated n9/1000 gate finished all eight declared cases. Source archive and
34 current source hashes matched; all eight NPZ hashes and stored checkpoint
L1 values (200,400,1000) were independently checked. Final Tucker reconstruction
matches each stored final joint array. Every period satisfies the declared
L1, mass, trait, negativity, and occupancy criteria. Worst recorded normalized
joint L1 is 1.0660185138013266e-6 and maximum trait difference is
9.747215330702108e-8. Receipt: model3_n9_long_verified_20261005.json.
This verifies the compressed solver against the SAME nine-node model, not
continuum/grid convergence, positivity as a theorem, or ecological ABM-density
interpretation. Resolution admission and full Model3 goal remain open.

## 2026-10-05: actual tiled projection passes; full-step gate launched

The captured strict child contraction passed without relaxing tolerance or
allocation cap: shape128x128x100, two assembly tiles, largest assembly
intermediate2,252,800values, residual upper7.775451753295329e-16 against
3.3538949820031467e-15. Wall time197.953s. Six source hashes/archive entries
and both input/output hashes checked; basis orthogonality and four independent
projected-core entries checked. Floating-point roundoff remains excluded from
the projection bound. Receipt: model3_multi_tiled_verified_20261005.json.
This repairs the previously preserved final-contraction failure.

A separate tiled reproduction integration was introduced after a missing-module
RED test. Ten tests cover direct-density agreement across reproduction settings,
mutation operators and adult survival, plus forced projection against exact
outcrossing. They passed. The same previously declared n65 second-step tolerance
gate is running in tiled_strict_second65, local relativeL1=1e-10; it compares
marginals to an exact one-step reference and the full joint distribution against
the existing1e-8 result. The earlier strict failure and baseline remain intact.
No longer trajectory or high-grid ecological interpretation is yet admitted.

## Next gate prepared, not launched

The repaired ten-period resource driver retains all8 settings, history76001,
founders, local1e-8 tolerance and per-array16million cap from the frozen
highgrid-tenstep plan. It now refuses launch unless tiled_strict_second65
completes with its full-joint<=1e-5 and marginal/trait thresholds, source hashes,
and final-state hash matching. Output is separate tiled_ten65; existing ten65
failure/running process preserved. This gate is local numerical/resource
admission, not full-path accuracy or ecological inference. Driver snapshot:
data/results/model3_tiled_ten65_runner_20261005.py.txt.

## 2026-10-05: strict integrated step fails after first successful child

The tiled strict second-step process exited normally with a FAILED receipt:
first child projection/assembly completed207.0s, then core rounding raised
'rank-reduction bound exceeds tolerance'; total209.953s. No final state or
full-joint comparison was produced. The next ten-period gate remains closed.
All captured source hashes/archive entries matched; failure archive and receipt
are retained in model3_tiled_strict_failure_20261005.json.

A diagnostic capture reuses the successful projected child only after exact
array equality against its captured parent cores/transforms, matching tolerance
and output hash. It replays rounding to save the failing state; it is not a new
simulation success or a relaxation. Diagnose truncation versus mass-rescaling
bound before any repair. The original strict sources remain unchanged.

Diagnosis on the saved failing rounding input: mass5.318706430903526,
postprojection5.3187064309034655, scale-1=1.1324274851176597e-14.
Truncation bound4.958504001741601e-11, rescaling bound1.1044499766571795e-9,
allowed5.318706430903526e-10. The rescaling uses sqrt(N)||core||F=97529.42.
The equally valid separable triangle bound sum|core| prod(sum|factor|) is
16.764520348068903 on this input. Taking the minimum of these two rigorous
exact-arithmetic L1 upper bounds would preserve tolerance and rescaling while
avoiding this overly loose bound. This is a proposed numerical repair, not yet
implemented or admitted. Roundoff remains excluded; full-step/tolerance gates
must still be rerun and pass. Diagnostic term receipts retained separately.

## 2026-10-05: sharper exact-arithmetic norm bound implemented

Separate sharp_rounding retains HOSVD ranks, mass correction and tolerance.
For orthonormal factors it uses min(sqrt(N)||core||F,
sum|core_abc| ||factor0_a||1 ||factor1_b||1 ||factor2_c||1).
Both bound the represented tensor L1 norm in exact arithmetic, including signed
factors; no positivity assumption or clipping is introduced. New tests cover
signed joint states, localized distributions, ordinary rounding and mass.

On the saved failed input the bound drops from1.154035e-9 to4.977489e-11,
below5.318706e-10. Direct common-basis joint comparison gives Frobenius
1.151842e-14, a conservative L1 upper1.144284e-9; this floating-point comparison
is not certified by the analytical truncation bound. No claim that roundoff
vanishes. The full-step gate still requires independently compared full-joint
error<=1e-5, unchanged. A separate sharp integration/driver is prepared for
that gate, preserving all prior failures and source snapshots.

## 2026-10-05: strict step hits a new allocation ceiling

Sharp strict gate completed three child channels then failed:
'explicit array size16438212 exceeds budget16000000', total612.422s.
The norm-bound repair passed its prior failure point. This new failure is
resource admission, not measured biological or precision failure. No terminal
state/full-joint comparison; ten-step launch remains forbidden. Sources and
archive verified; model3_sharp_strict_failure_20261005.json preserves outcome.
A diagnostic replay saves every completed child plus failing rounding/sum
input and traceback, so subsequent numerical repairs can reuse captured inputs
without repeating expensive child projections. Same parameters/tolerances/cap.

## 2026-10-05: sum allocation failure identified and captured

Diagnostic replay completed and traceback identifies compressed_step.summed:
QR common-basis core allocation exceeds16million before summing. It is not
child projection or final rounding. Two failed_sum input NPZs and all3 completed
child states are retained, with verified source fingerprints. The next repair
can be tested directly on these saved sums without repeating the600s ancestry
calculation. Sum input shapes/hashes and traceback are in
model3_sum_failure_diagnosis_20261005.json. Need project shared factor spaces
before full common-core allocation, with a declared joint error bound; do not
simply increase cap, discard correlation, or relax tolerance.

## 2026-10-05: bounded shared-factor sum passes captured resource case

Implemented a separate bounded_sum after RED tests. Each concatenated factor
space is SVD-projected BEFORE the joint core is allocated. Per-axis spectral
residual is multiplied by sum(||core_s||F product(other factor spectral norms))
and sqrt(number of physical states). The sum of these three bounds follows
from telescoping orthogonal projections and bounds joint L1 in exact arithmetic.
Signed factors/correlations are retained; no independent-marginal closure.
Three small direct-reference/invalid-input tests pass.

On the exact saved failing inputs, the core becomes333x301x154 (15,436,422
values), below16million, in6.265s. Projection L1 bound7.874181685223706e-10
against allowed6.619543380939491e-9. Mass before66.19543380939491 and
after66.19543380939523. This is component admission only, not a full strict
step or trajectory. Sources/input/output hashes in the actual-run receipt.
Next: integrate fallback with a shared per-stage projection+rounding error
budget, then revalidate full-step comparison. Previous failures remain intact.
