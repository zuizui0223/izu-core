# Scientific core / founder campaign review

Snapshot: `91d884e8fc46def450c6091f617b0f96776aad75`, isolated checkout `work/repository_review_20261016`. Read-only audit; no frozen code, designs, results or scientific claims changed. All 21 `scripts/model3_island/*.py` source files were read, along with five campaign generation/readout files listed in `science_reviewed.json`. This is source review and small diagnostic testing, not a rerun of the scientific campaigns.

## Findings

### SC-01 — P2: fixed-assurance configuration is ignored by the investment-gradient helper

Location: `scripts/model3_island/selection.py:15-17` (and the subsequent use of `a` throughout the helper).

`investment_invasion_terms` takes A directly from the supplied genotype-derived resident vector even when `config.assurance_mode == 'fixed'`. The actual reproduction and density operators instead use `config.fixed_assurance`. Consequently changing the genetically stored, non-expressed A coordinate can change the inferred selection sign while leaving the native biological payoff exactly unchanged.

Reproducer: `science_repro.py`, using the existing assurance-cost configuration with fixed A=0.5 and resident matching=0.2/investment=0.5. Input resident A values 0.1, 0.5, 0.9 produce gradients `+0.588007190445476`, `-0.1522648262882323`, `-0.3313006173816718`; native maternal and paternal arrays are byte-identical across these cases. This is not the documented finite-versus-density self-exclusion distinction: it is a fixed-expression configuration being discarded.

Impact: a future fixed-A diagnostic or caller with neutral stored A variation can report the opposite investment-selection direction. No corruption of the original/fresh-founder trajectories was found: their fixed arms initialize and preserve A alleles at 0.5. The unified prehistory runner already works around this by replacing `means[2]` with `cfg.fixed_assurance` before calling the helper (`run_chapter2_unified_payoff_prehistories.py:79-81`). Existing gradient tests principally use evolving mode or A=0.5, so they do not expose it.

Suggested repair: in a versioned, non-frozen successor helper use the expressed A for fixed mode, or explicitly reject fixed-mode calls with a documented separate evaluator. Clarify that `syndrome_thresholds`' assurance gradient is an evolving-A counterfactual; do not silently call it the direction of an actually fixed trait. Add the fixed-mode invariance test above. Do not rewrite archived producer blobs or pretend existing numerical results changed.

### SC-02 — P2: extinct/non-evaluable cohorts cannot be written by the original summarizer

Location: `scripts/summarize_chapter2_assurance_generality.py:67-71`; failure occurs at line 277.

The empty bootstrap sample returns `[NaN, NaN]`. `setting_readout` correctly marks a cohort with no eligible endpoint contrasts as inadmissible and uses `None` for its means, but retains those NaNs in all interval fields. `main` then serializes with `allow_nan=False`, raising `ValueError: Out of range float values are not JSON compliant`. Thus a complete, integrity-verified but extinct cohort cannot produce the explicit negative/non-evaluable report required by the frozen design's `all_settings` rule.

Reproducer: `science_repro.py` patches only endpoint loading to return `(False, 0.5, NaN)` for all declared cases, then calls the unmodified full `setting_readout` and the same JSON serialization. No simulation, file falsification or external execution is involved. The result has `admissible=False`, `passes_frozen_rule=False` and serialization fails.

Impact: failure-reporting path, not the current saved all-occupied results. Suggested repair: successor summarizer represents unavailable intervals as JSON null (or explicit null endpoints) and preserves the inadmissibility reason; regression-test empty and partially eligible cohorts. Do not replace missing biological values with zero or relax eligibility.

## Other concerns, not promoted to confirmed scientific findings

- The fresh-founder shard runner supports valid per-case reuse, but its final immutable `atomic_json` refuses an already present completion marker on a fully completed shard rerun (`run_chapter2_q1_fresh_founders_20261016.py:229`, helper at 37-42). A wrapper could safely validate and return an identical completion marker. This is resumability ergonomics, not a numerical defect, and was not separately reproduced here.
- Fresh-founder `verify_complete` checks source manifests for mutual agreement and digest integrity, but does not independently pin the admitted source digest to an external approved revision. Original `verify_complete` does not inspect source manifests at all. Treat these as receipt-consistency checks, not independent biological source-identity proof; existing archive/revision audits may provide the missing admission step. No evidence of mixed or corrupted actual archives was found in this task.
- Fresh-founder equal-founder checks compare initial I means, not full `state_0` genomes. Producer tests do compare full initial genomes and the actual producer is paired correctly. Strengthening the independent readback would improve its claimed contract; this review did not establish a mispaired saved case.

## Known limitations explicitly excluded as new bugs

Read `docs/REPOSITORY_NAVIGATION.md` and `docs/MODEL3_REPOSITORY_CODE_ECOLOGY_AUDIT_20261016.md`. Finite self-exclusion versus genotype density class mating, K/background coupling, exogenous visitors, two-episode exposure, one-founder conditionality of the old campaign, different study cohorts, and Q4 pre/post mutation contract are already documented. They were not reclassified as new code errors. The fresh 8x8 crossed bootstrap resamples both axes, and the four-cell contrast orientation is internally consistent.

## Validation / coverage

- Full text read of the 26 scientific modules in `science_reviewed.json`; additional caller excerpts and tests inspected but not counted as full reviews.
- `python science_repro.py`: both above diagnostic reproductions passed.
- Focused existing suite: `test_chapter2_q1_fresh_founders_20261016.py`, `test_model3_investment_invasion.py`, `test_model3_cross_layer_logic_audit_20261016.py`, `test_model3_mathematical_representation_audit_20261016.py`: **44 tests passed**.
- No P0/P1 new numerical-kernel defect found within this scope. This does not establish that every script or biological assumption in the repository is correct; no long scientific reruns or exhaustive all-input verification were performed.

## Expanded review: 60 additional source files

Coverage now totals **86 source files**. Exact membership is in `science_reviewed.json`. The additional tranche covers joint compressed ecology/inheritance, fourteen integration variants, streamed contractions/projections, local approximation bounds, exposure diagnostics, pollen assays and the saved-population assay runner. Near-identical variants were reviewed through a fully read base file plus complete unified diffs; unchanged text was compared mechanically. This is complete source-content inspection for those files, not 60 independent validated biological experiments.

### SC-03 — P2: bounded integrators reject valid zero-selfing populations

Representative location: `scripts/model3_batched_weight_integration.py:46-48`, duplicated in all fourteen `bounded_step` integration variants named in the reproducer. The function's selfing stage treats `exact_mass <= 0` as an arithmetic error. A zero selfing contribution is valid when all occupied genotypes have A=0, even though selfing weights on unoccupied grid nodes are positive. The earlier `not np.any(xy) or not np.any(a)` shortcut does not detect this support-dependent zero.

Reproducer appended to `science_repro.py`: a nonnegative rank-one state of 48 plants at X=I=0.5, A=0 on three `[0,0.5,1]` allele axes, evolving assurance, zero mutation, visitors present. Both native tensor density and the exact unrounded compressed operator return population mass **48.0** after outcross reproduction; every bounded integration variant instead raises `ArithmeticError('invalid weighted mass')` before outcross births are computed. The same support issue can occur for other legitimately zero reproductive channels. This is not an under-budget truncation stop and does not require numerical noise.

Impact: prospective low-rank integration/reproduction on admissible boundary-supported states is blocked. These are numerical prototype branches; this review does not establish impact on the frozen ABM or published readouts. Suggested repair for a successor implementation: distinguish a proven identically zero weighted measure from a negative/nonfinite or cancelling signed measure, return the exact zero channel in the former case, and retain the rejection for invalid signed states. Do not merely permit arbitrary zero signed mass. Add boundary-support regression tests against the uncompressed density operator. There is no need to weaken the local error tolerance or choose a more favorable ecological state.

## Logical dependencies, contradictions and circularity checks

| Question | Source-grounded finding | Claim boundary |
|---|---|---|
| Is trait direction prescribed? | `population.inherit` uses zero-centered normal mutations and reflection. Native `reproduce` assigns explicit I-dependent pollen returns, I resource costs, A selfing benefits, and setting-specific costs. It does not force I downward or A upward. | Trait directions are emergent **conditional on these imposed payoff functions**. Simulation cannot independently discover that floral investment has a resource cost; that is an assumption. |
| Are selfing costs counted twice? | Native reproduction applies ovule allocation once, then prior/delayed selfing and viability once. Recruitment uses donor-recipient outcross plus viable selfing; `.5` maternal/paternal weighting is a separate genome-contribution diagnostic, not reapplied to seed birth counts. The compressed selfing input is already viable births and its kernel only inherits/mutates. | No new double-counting defect found in reviewed paths. Seed production, parental genome equivalents, recruitment and persistence remain distinct quantities. |
| Are fixed/evolving comparisons initially paired? | Both old/new runners force both A alleles to0.5 and derive demographic streams from identical visitor/repeat seeds across treatment arms. Fixed mode blocks A mutation; evolving mode allows it. Original/fresh campaigns use different founder and visitor cohorts. | The contrast is allowing A variation/evolution, **not selfing present versus absent**. Common random streams are pairing; they do not turn treatment arms into independent replicates. SC-01 concerns a downstream analytic helper, not these initial states. |
| Is density agreement independent confirmation? | Exact compressed operators share native payoff and mutation kernels; their tests compare against density. They preserve joint genotype correlations and self-versus-outcross kernels. Fourteen copied integration variants mostly swap contraction/bounding helpers. | Agreement is implementation/algebra verification, **not fourteen biological replications**, and not proof of the finite ABM's expected trajectory. |
| Is a local numerical error receipt a trajectory guarantee? | Integration docstrings explicitly say local bounds are not global bounds. The code bounds compression/projection at successive stages but does not derive propagation through nonlinear ecology over all generations. Bounds exclude floating-point roundoff, and representations are not positivity preserving. | Do not interpret per-stage tolerance or successful short tests as long-horizon biological accuracy or positivity. Existing STOP/uncertainty for high-resolution long runs must remain. |
| Is pollen supplementation independent field evidence? | `model3_pollen_assay` computes an instantaneous model saturation ceiling at fixed ovule allocation. Prior selfed ovules remain unavailable; delayed selfing disappears with saturation. `run_model3_pollen_assay` applies this to saved states. The design labels it exploratory and excludes t1000 because no visitor1000 exists. | This is a counterfactual diagnostic of the same simulation, not another independent observational test, fitted natural PL effect, or causal mediation percentage. |
| Are chronology/selection and terminal differences identical estimands? | Sustained crossings use specified thresholds/windows and return censored labels; analytic selection is fixed-resident and local; endpoint contrasts integrate stochastic selection/inheritance over time. | Opposite signs at different levels are not arithmetic contradictions. An endpoint difference cannot alone prove its path-specific mechanism. No new source evidence was found that isolates the cause of old-versus-fresh-founder result differences. |

The review finds no same-time circular update in the native biological sequence. Feedback across generations is intentional. The main circular-evidence risk is narrative: reusing the same saved populations for local assays, compressed checks and outcome summaries must not be described as independent confirmation of a single historical causal chain.

## Expanded scientific source coverage

155 distinct files reviewed: 130 complete source reads and 25 full-base plus complete-diff reads, with exact per-file methods in science_reviewed.json. This includes all 69 remaining top-level run_/model3_ files assigned after the original 86. No campaign was executed. No additional confirmed correctness defect in these 69 files.

Factorial outcross controls preserve same-parent viable seed totals, not future demographic trajectories; their inclusion-exclusion is an algebraic decomposition of engineered operators, not independent biological causal evidence. Abrupt/gradual visitor experiments match cumulative pollen exposure on a fixed reference phenotype, not evolving-population exposure. Restoration edits create latent allelic variation and are artificial interventions. Shared-kernel exact replay establishes reproducibility, not independent biological validation. These boundaries are generally stated in the reviewed sources.

## Final lane coverage and authorized successor correction

194 files: 164 full source reads and 30 full-base plus complete-diff reviews (five native archival copies are text-identical). Exact paths/methods are in science_reviewed.json. Includes 19 additional chapter2 source/contrast files and 20 plan/comparison/proof/native/test files. Review does not establish that every possible input or scientific claim is correct.

### SC-04 — P2: initial gate validation skips the near visitor environment (fixed)

`scripts/chapter2_timed_self_viability_future.py:155-172`: the final per-K viability-gate checks were outside the visitor loop, using its last value `far`. A mocked `one_source` with an invalid near late-only t0 selfed yield of99 versus baseline1 was accepted and written. The same far defect was rejected. This is a validation coverage defect; the actual `gate_active` producer remained correct and no archived scientific result was shown to change.

Parent authorized the minimal correction in the review checkout after searching source-path pins in data/docs/scripts/tests/.github: no archived path pin found for this file. Indented the existing block into the visitor loop; no biological operation changed. New three-case regression verifies valid rows pass and corrupted near/far rows both fail before writing. Red: one failure (near), two pass. Green: all three pass. Combined regression + existing prospective + archive tests:97 pass using PYTHONUTF8=1 and dedicated workspace basetemp. Initial default-environment run hit the known shared-temp permissions issue; first broader run had one CP932 decoding error, resolved solely by UTF8 runtime setting.

### SC-05 — P3: clean-rerun comparator silently equates NaN with finite results (deferred)

`scripts/compare_model3_bridge_clean_rerun.py:28-32`: numeric branch computes `abs(x-y)` and appends only if `d>0`. For x=NaN,y=1, comparison returns max difference0, zero numeric differences, zero structural mismatches. JSON decoder permits NaN; final CLI output does reject it through canonical serialization (`design.py:26`, `allow_nan=False`), but `_maxdiff` itself reports no discrepancy and should reject nonfinite inputs explicitly. Reproduced directly with a one-value dictionary in science_repro_extra.py; no campaign executed.

This path is pinned as archived source in `data/designs/restoration_futures_preflight_20261014.json`, `data/designs/q3_triangle_preflight_20261014.json`, and the Q3 hold record. Left untouched. Successor comparator should reject nonfinite inputs (including NaN and infinities) before comparison, with regression tests. Current finite comparison result is unaffected.

Scientific logic checked in extra chapter tranche: true independent inference unit remains visitor history; post-outcome channels retain exploratory labels; initial engineered gate parity is a manipulation check, not new evidence; cumulative recruits are duration-dependent and not identified mediators; prospective expression-order assignment is distinct from post-treatment inherited crossing order. These distinctions are explicit in the reviewed code. No additional evidence of direction hard-coding or reproductive-cost double counting was found.

## Final additional access / onset / allele-loss audit

Coverage now200files:170full source reads and30complete-diff reviews. Added6scripts listed in science_reviewed.json. No further confirmed defect. Existing access/loss unit tests:24passed; no raw campaign or full archive re-analysis executed.

Directional-access logic: integer bound10*N*min_scaled >5*initial_scaled_sum-4*N is exactly equivalent to minimum remaining I allele >initial diploid mean minus0.05. Under the explicitly verified no-I-mutation/no-immigration law, all future inherited means exceed this bound; exclusion is sufficient for impossibility, while absence of exclusion is not proof of attainability. Homolog ancestry checks pair value and origin in the same homolog. The scalar verifier uses Fraction arithmetic and set-based support inheritance independently of the vector producer.

Expected-response onsets: sum of sex-channel Price responses is an on-path expected inherited change, not a direct fitness gradient. The code distinguishes its first positive update or20-update streak from the original0.05 biological threshold and does not rename the source categories. It reuses saved kernel outputs and therefore cannot independently validate that kernel or establish causal chronology.

Last-loss decomposition: parents are weighted by viable selfed seeds plus half each parental outcross contribution. For a heterozygote selfing, two independent gametes give zero-needed-allele probability1/4, not1/2. Conditional on the realized retained offspring count n, the iid recruitment/segregation law gives q0**n. Sampling/transmission residual=-expected frequency is an accounting identity after selecting an observed complete-loss transition; it is not a discovered independent drift force, prospective hazard or p-value. This claim boundary is explicit. The verifier independently enumerates gametes but shares the archived reproductive kernel, so its independence is computational verification only. No circular biological inference was found inside these labeled claims.

RECIPE_SOURCE is frozen provenance code. Its design() requires a sibling natural_campaign_design.json and is not invoked by the loss audit, which rebuilds inputs from authenticated archived metadata. It must not be mistaken for a standalone runnable current campaign entry point.

## K32 scientific diagnostics tranche (19 additional full reads)

Coverage now 219 sources: 189 full source reads and 30 full-base plus complete-diff reviews. Exact paths are recorded in science_reviewed.json. Three additional test modules were read to choose bounded checks; they are not counted as source-script coverage. Fifteen focused tests passed (four historical simulation cases deselected). No scientific campaign executed.

### SC-06 — P2: legitimate insufficient-survivor results crash three CLI summaries

- scripts/audit_model3_k32_fixed_frequency_heterozygosity.py:344-345 indexes cell_by_source_parent_year although run_fixed_frequency returns only an insufficient-survivor status at lines 174-176.
- scripts/audit_model3_k32_heterozygosity_reproductive_channels.py:313 indexes source_parent_years although run_channels has a NOT_ENOUGH_SURVIVORS return.
- scripts/audit_model3_k32_self_transmission_curvature.py:312 indexes source_parent_years although run_self_curvature returns INSUFFICIENT_SOURCE_YEAR8_PARENT_SURVIVORS at line 218.

The scripts save the legitimate non-evaluable JSON and then raise KeyError while printing their final summaries. This converts a declared scientific stop into a failed command, confusing orchestration/retry handling. Existing adequate-survivor numerical results are unaffected. Bounded reproducer science_repro_k32_status.py mocks only the expensive runner return and calls each real CLI main; all three reproduce the exact missing-key exception after the status JSON is written. Recommend status-aware concise summaries; no biological changes or reruns needed. Sources were left untouched pending frozen-source review.

Scientific logic and circularity checks:

- Pathwise q-p plus realized-minus-q is an exact accounting identity, not independent evidence identifying drift versus selection. The source explicitly limits martingale claims to current-state/positive-offspring conditioning; late-survivor conditioning can change the residual mean.
- Neutral census control preserves mean allele frequency conditional on its imposed census but deliberately replaces mating payoffs. Mean-matched ceiling comparison uses source outcomes to fit its comparator, so it cannot independently confirm a source biological mechanism. The code labels this. Demographic holdout fits coefficients only on its training half; visitor-history dependence and imposed source census remain explicit.
- Offspring variance mu(1-mu)-H/4 and self transmission dosage curvature are algebraic identities. Under zero assurance cost the self-seed count is linear in A; the allele transmission numerator includes A times dosage, making its curvature a transmission-weighting effect, not a newly discovered nonlinear assurance cost. The reviewed code and tests preserve this distinction.
- Shapley export/routing/maternal allocations are baseline-relative exact factorizations, not separable causal effects. Father/mother marginal identities verify the same Mendelian kernel; unchanged marginals constrain immediate allele means but not multilocus offspring composition or subsequent dynamics.
- Heterozygosity edits preserve parental copies and census but may change fertility, intensity and genotype associations. Eligibility differs between up/down edits; same-sham pairing and separate denominators are explicit. Founder resets can reintroduce lost alleles and are correctly labeled artificial.
- State/visitor crossing uses common late-survivor paths and off-diagonal one-step assays. The two-factor symmetrized allocation sums to total change, with interaction separately recorded; it is not an autonomous historical causal intervention.
- Eight-history predictor standardization, ridge fitting and baseline estimation exclude the held-out history. Early covariates are confined to years 1-2; retrospective descriptors do not enter the forecast. The same eight histories used at two budgets are explicitly not sixteen ecological replicates.

No additional confirmed direction-hard-coding, cost double counting or unlabelled circular biological proof was identified in these 19 sources. This does not independently validate empirical biology or numerical campaign outputs.

### SC-06 correction and peer review follow-up

Authorized minimal correction applied in the review clone only. Each of the three CLI mains now recognizes its explicit insufficient-survivor status after saving the JSON, prints status plus budget, and returns normally. Exactly three added lines per script; successful-output logic and all scientific runners remain unchanged. New tests/test_k32_insufficient_cli_status_review.py supplies bounded runner results to each real main: 3 failures before correction, 3 passes after. No campaign executed.

Frozen-source check: HEAD remained 91d884e8fc46def450c6091f617b0f96776aad75. Exact current SHA256 and git blob searches across data/docs/scripts/tests/.github found no pins for these files (path mentions only documented CLI commands):

- fixed_frequency_heterozygosity: SHA256 9023c18a18407a32fd5e06c7dacddc60f11bfa1f21b2bc5f41ec755b61d5871a; blob ace3f668732ad6f6b8dead5594f6a471c63c6024.
- heterozygosity_reproductive_channels: SHA256 456303537cb3b60f5eb99d2b36f8a13947aa04b9ddbcead466f771c263fe0e7e; blob 44f8d11ec68c9ed25e5512a6422a2a397a9d2286.
- self_transmission_curvature: SHA256 2bd1da720589a6557f0b987653ed558ff8303d2142ec3e4609524dd25bb94f68; blob 0e1cf4a9d614158bfdfd63f44088b9d05583ab6e.

Peer-reviewed docs/REPOSITORY_REVIEW_LOGIC_20261016.md in full. No scientific overclaim requiring correction found. In particular it correctly separates the poster Q1/Q2 from repository question numbering, fixed assurance from absent assurance, relative far-side investment retention from an absolute increase, finite/deterministic structural differences from pure drift, and computational/source identity checks from independent biological evidence. Its old/new founder discussion does not select conclusions by preferred outcome or claim the source audit identified a unique cause. Document left unchanged.
