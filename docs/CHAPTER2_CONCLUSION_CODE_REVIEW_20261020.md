# Chapter 2 conclusion and supporting-code review

Date: 2026-10-20. Reviewed head: `4f0dbafc1ee4d25e7fcb7821504f0f62f6f8d434`; editorial diff: `dd76ec6f0d2bf330375a69fdb76b06925ee4c32c...4f0dbafc`. Supporting scientific code already present on main was also inspected because the request concerns conclusions, not only the latest prose diff. No new simulation, biological replay, new significance test or equivalence decision was performed.

## Standards / implementation correctness

An independent code reviewer found **no new concrete result-changing defect in the inspected implementation**. Checked areas: confirm160 endpoint signs and crossed-source inference (`q3_joint_inference_20261019.py`, `q3_native_runner_20261019.py`); variation fixation/duration (`variation_clock_readback_20261019.py`); donor admission (`readaptation_sources_20261019.py`); baseline-pollen founder contrasts (`audit_chapter2_pollen_baseline_factorial_20261019.py`); both technical hitchhiking producers. No style-only finding is promoted to a scientific defect. This is not exhaustive certification of every script or historical raw archive.

The two hitchhiking producers have different I-reassignment random streams. The six-policy mutation-origin tracer's interaction is +0.054321; the ten-policy producer's corresponding I-neutral interaction is +0.058492. These are distinct source-conditional results, not interchangeable estimates or independent source replications.

## Specification / conclusion fidelity

An independent evidence reviewer found **one P2 interpretation error and one P3 navigation error**, corrected in this revision:

1. **P2 — favorable selection was incorrectly made necessary for realized recovery.** The completed manuscript's Methods said high-I recovery required BOTH favorable parental selection and sufficient allele support. Native stochastic parent sampling and Mendelian segregation (`scripts/model3_island/population.py`) can realize a trait increase against conditional selection. Retained upper support is necessary under the focal closed inheritance rule; favorable selection affects expected direction and response probability, but is not necessary for every finite realization. The active Methods now distinguish these statements. The historical mechanism synthesis is preserved with a dated interpretive erratum.
2. **P3 — dangling reference to excluded proposals.** The completed-only Methods referred to a two-clock proposal "below", although that extract excludes it. The reference now explicitly links the historical working draft.

No contradictory core numerical verdict was found in the crosschecks. Registered outcomes, Results, biological code and original protocols' outcome rules remain unchanged.

## All current conclusion families: disposition

The table covers the active Article's main conclusions and supplementary extensions. Supporting source documents remain authoritative for their exact cohort and inferential rank; absence of a new issue here is not fresh raw replication.

| Family / claim | Current verdict | Boundary retained / source checked |
|---|---|---|
| I decline does not require A evolution | Supported within tested model | Fixed expression A=.5 still permits selfing; Q1 original and fresh-founder reports. Does not reject a correlated selfing syndrome. |
| A evolution attenuates environmental I divergence | Original 4/4; independent-founder 3/4 | Direct-A-cost interaction inconclusive; no universal far-side retention. |
| Baseline pollen limitation changes additional A response | Exploratory positive interaction | 384 paths, 12 founders; genetic history and absolute delivery differ. Not an isolated instantaneous deficit or memory effect. |
| A always precedes I | Not supported generally | 51/64 versus30/64; threshold and mating setting matter. |
| Assigned expression order drives substantial survival change | Specific practical-equivalence result | Assigned phenotypes, not natural inherited sequence; original genetic-carrier Q2 remains both_inconclusive. |
| Initial genetic width changes order | Conditional exploratory effect | Support, variance and threshold geometry change jointly; not a pure variance mediator. |
| Visitor tempo changes event probability | Supported in specified experiment | Composition chronology, not a pure abundance manipulation; reference-clone matching does not match evolving exposure. |
| Finite outcomes differ from genotype density | Supported comparison | Density is not the exact stochastic expectation; no identified drift fraction. |
| Floral response is unstructured chance | Inconsistent with conditional repeatability | Eight-repeat reliability .621/.825 differs from single-trajectory ICC .170/.370; capacity changes more than drift. |
| A is inherently deterministic and I random | Not established | Matched endpoint A variability is often lower, but boundaries, fixed M, no mutation and survival conditioning limit generalization. |
| Genetic options can disappear before fixation | Supported structural observation | 703 LOW-I histories; retrospective1455 HIGH-I histories are the same2304 source cohort and a different target, not independent confirmation. |
| A changes high-I support loss at full survival | Registered model-conditional support | G=+8.328125pp;160×160 crossed axes; excludes differential extinction, not every demographic mediator. |
| A improves persistence under harsh resources | Registered model-conditional support | S=+92.707031pp policy×budget interaction; not proof that genetic erosion causes survival. |
| Joint alive-and-accessible effect reverses by budget | Descriptive post-outcome pattern | −8.328125/+35.566406pp; no third registered test or continuous ecological threshold. |
| A changes polymorphism duration | Post-outcome source readback | I duration−2.628 atB8/+12.684 atB4.5; harsh-budget duration mixes variation retention and longer survival. |
| Support restoration or renewal guarantees sustained change | Not supported | Conditional restoration, carrier distribution and mutation renewal have distinct partial/inconclusive results; no pooled rescue rate. |
| Late transfer demonstrates general recovery failure | Not supported | Some I targets already attained; only4/32 cohorts per arm polymorphic versus24/32 target-compatible; future replicates nested. |
| A-history improves adaptation in a new environment | Unresolved | Descriptive survival/return differences, inherited M/I/A differences and survivor conditioning; not unconditional A-mediated adaptation. |
| A-specific positive or negative hitchhiking | Unresolved; association-sensitive endpoint changes observed | A-mutation permission, not standing-A intervention; artificial reassignment and short reused sources; neither presence nor absence established. |
| Secondary-colonization occupancy equals migrant persistence/adaptation | Rejected as an endpoint equivalence | Verified pedigree distinguishes occupancy, selected markers and descendants; two founder×two visitor source axes; no identified adaptive A advantage. |
| Island syndrome is imported A plus locally evolved I | Not established | Technical sorting and within-survivor changes do not identify natural assembly; both traits can be filtered. |
| Private/public returns establish a tragedy of the commons | Not established | Some pollen externalities exist; sustained individual/group conflict driving extinction is unproven. |
| Natural irreversible selfing trap | Not established | Closed mutation-free target support is not permanent irreversibility in open natural populations. |

Historical S1–S33 and F1–F8 remain mapped in the [41-unit disposition](CHAPTER2_HISTORICAL_RESULTS_DISPOSITION_20261019.md). This review checked that map and its relation to the Article; it did **not** independently recompute all41 underlying raw archives. [Supplement](CHAPTER2_COMPLETED_EVIDENCE_SUPPLEMENT_20261019.md) now explicitly includes hitchhiking, secondary colonization and source-sorting extensions.

## Read-only arithmetic and hitchhiking interpretation

The [machine-readable receipt](audits/CHAPTER2_CONCLUSION_CODE_REVIEW_ARITHMETIC_20261020.json) records source identities and calculations. Registered G/S reproduce the compact source counts. Forty ten-policy panel records were read from [run39366397170, job118444292590](https://github.com/zuizui0223/izu-core/actions/runs/39366397170/job/118444292590); each includes4/4 occupied source cells. The focused source step succeeded, while its historical overall workflow was cancelled; the receipt does not reinterpret that workflow as fully green.

| Ten-policy producer, four-panel descriptive mean | I payoff neutral | M and I payoffs neutral |
|---|---:|---:|
| A mutation allowed minus prohibited, inherited I | +0.068930983 | +0.002403968 |
| Same difference with annual I reassignment | +0.010438515 | +0.049497030 |
| Difference between those policy differences | +0.058492469 | −0.047093063 |

These are trait units, not percentage points or new inferential estimates. Negative association-sensitive differences do not rule out hitchhiking: low-I backgrounds could also be associated with successful lineages. They likewise do not prove such a route, because the intervention does not isolate A-specific mediation and finite paths depend on sampling and pedigree. A small mean can reflect opposing conditional effects. There is no predeclared negligible-effect bound or source-level equivalence test here; "no effect" is not an admitted conclusion.

## Review outcome and limits

The principal paper conclusion survives this audit: under the specified model, assurance policy affects a defined floral genetic option and persistence differently; neither endpoint alone identifies subsequent adaptive success. The correction concerns a claimed necessary mechanism, not the registered G/S numbers. The paper should not claim a universal syndrome sequence, generic demographic independence, a quantified drift share, proved A-specific hitchhiking, or successful secondary adaptation.

Validation is limited to source arithmetic, code/spec inspection and existing non-biological evidence/figure/route tests. Raw audits and pedigree replays mentioned in source reports are earlier work, not newly repeated here. The full repository suite and all historical biological archives are outside this read-only review's fresh verification scope.

Verification outcome: selected completed-evidence numeric validator PASS;49 existing evidence, figure, editorial-route and three-state checks PASS; `git diff --check` clean. This is not a full-suite claim.
