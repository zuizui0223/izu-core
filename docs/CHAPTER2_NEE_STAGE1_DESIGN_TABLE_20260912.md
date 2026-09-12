# Chapter 2 NEE Registered Report Stage-1 design table — pre-data working surface

Version: v0.3 — 2026-09-13  
Status: **P1-P4, conditional P5/H5, R4, R5 and R1a focal/transport/block architecture are frozen; R1b exact site/time registry, R2/R3 and R6 remain open**

Parent contracts:

- `data/design/chapter2_nee_predata_promotion_lock_20260912.json`
- `data/design/chapter2_nee_effective_community_representation_lock_20260912.json`
- `data/design/chapter2_nee_h5_correlation_stratification_lock_20260912.json`
- `data/design/chapter2_nee_r5_transport_decision_20260912.json`
- `data/design/chapter2_nee_h5_prepilot_oc_freeze_20260912.json`
- `data/design/chapter2_nee_r1_scope_architecture_20260913.json`
- `data/design/izu_transition_linked_estimand_lock_20260909.json`
- `data/design/izu_effective_service_rank_crossover_lock_20260911.json`

This is the working hypothesis/design table for a possible Nature Ecology & Evolution Stage-1 Registered Report. The 32-block scale used below is an order-of-magnitude R1 screening floor derived from the frozen synthetic operating-characteristics screen. It is **not empirical power and not a final confirmatory sample size**.

## R1a architecture already frozen

| Item | Frozen state |
|---|---|
| focal natural system | *Campanula microdonta* |
| focal candidate geography | Oshima + Kozushima; **candidate geography only, not final named sites** |
| second prospective transport system | *Farfugium japonicum* |
| preferred transport geography | independent mainland coastal populations from the existing source universe: Hitachi / Hitachinaka / Tateyama, subject to R1b feasibility |
| P6 selection timing | before focal reproductive outcomes |
| P6 selection basis | source-defined pollen-target membership, high interaction breadth and broad source-site coverage; not future focal effect direction |
| H5 primary design lever | independent repeated exposure blocks |
| R1 triage floor | materially fewer than 32 plausibly independent blocks is not preferred for the NEE H5 lane unless R2/R3 later supply stronger empirical information |
| exact population/site/time registry | **OPEN — R1b** |

A same-archipelago *Farfugium* fallback is allowed only if it is biologically and sampling-wise independent enough to be a genuine prospective transport challenge rather than another focal block.

## Global unit and outcome-state rules

- strict linked unit: `block_id x plant_id`;
- independent precision unit: plant, nested in prespecified blocks;
- flowers, visits and SVD events are within-plant/block subsamples, not independent `n`;
- block boundaries and any dependence/synchronization strata are fixed from outcome-blind exposure information before reproductive outcomes are opened;
- confirmatory states are `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE`;
- failed measurement/support gates cannot become biological nulls;
- effect direction cannot redefine predictors, visitor groups, blocks, dependence strata, thresholds or endpoint families;
- generic-theory `rho=0.25` is a model-specific benchmark, **not** a natural cutoff.

## Mandatory hypothesis/design table

| Hypothesis | Confirmatory prediction | Primary predictor / contrast | Outcome | Unit / hierarchy | Outcome-neutral gate | Frozen analysis family | Interpretation |
|---|---|---|---|---|---|---|---|
| **H1 / P1 — composition beyond amount** | Effective-community composition retains information beyond coarse amount/breadth controls. | Background-controlled effective-service composition vector versus the same model without composition, retaining effort, total effective service and declared breadth terms. | Mature reproductive endpoint; dependency may be linked secondary. | Plants within blocks. | Q0-Q5 as applicable; R4 composition available. | Frozen hierarchical response model plus prespecified inferential/out-of-block comparison. | `SUPPORTED` if declared composition contribution passes; adequate null/adverse = `FALSIFIED_OR_ADVERSE`; failed support/measurement = `NOT_EVALUABLE`. |
| **H2 / P2 — plant state × realized community** **PRIMARY** | Pre-outcome plant functional state interacts non-additively with realized effective-community composition for same-plant response. | Pre-outcome state × full declared effective-service composition. | Same-plant mature reproductive response. | `block_id x plant_id`. | Q0, Q2, Q4-Q6 pass; state measured before outcome. | Frozen hierarchical relational contrast; no post-hoc state threshold or community simplification. | `SUPPORTED`, `FALSIFIED_OR_ADVERSE`, or `NOT_EVALUABLE` under the frozen criterion. |
| **H3 / P3 — functional bridge** | Visitor identity/composition maps to an independent effectiveness intermediate before reproductive outcome. | Visitor group/taxon identity + visit exposure. | Background-controlled single-visit conspecific pollen deposition; rate-weighted effective service only after gate passes. | SVD within plants/blocks. | Confirmed first visit, no-visit controls, pollen QC, adequate SVD support. | Frozen background-controlled effectiveness model; no seed-informed regrouping. | Failed SVD control/reliability = `NOT_EVALUABLE`, not zero effectiveness. |
| **H4 / P4 — reproductive dependency consequence** | Treatment contrasts identify whether pollination service can alter mature reproduction. | Open natural pollination, bagged autonomous, supplemental outcross; optional single-visit-then-bagged only if frozen before execution. | Mature fruit/seed endpoint. | Treatment flowers within plants within blocks. | Q0, Q3-Q5; terminal treatment linkage. | Frozen hierarchical treatment-contrast model. | Adequate declared contrast supports/adversely tests H4; treatment/endpoint gate failure = `NOT_EVALUABLE`. |
| **H5a / P5 — lower shared dependence** | Aggregation across prospectively comparable lower-dependence opportunities decreases community-realization contribution and increases plant-state contribution; state-over-community reversal is tested only in a pre-admitted crossover-capable domain. | Outcome-blind shared-dependence/synchronization × aggregation. | Relative state, community and non-additive contributions. | Plants nested in repeated independent blocks. | Dependence coordinate frozen before outcomes; repeated-block support and Q5/Q6 pass. | Prespecified dependence-by-aggregation interaction and/or contribution decomposition; no breakpoint search. | Both directional redistribution components required; adequately measured opposite/absent pattern = `FALSIFIED_OR_ADVERSE`; inadequate support = `NOT_EVALUABLE`. |
| **H5b / P5 — higher shared dependence countercondition** | Shared/synchronous stochasticity retains a community-realization floor, weakening or preventing state-over-community reversal as aggregation increases. | Same frozen dependence coordinate and aggregation rule as H5a. | Same decomposition as H5a. | Same repeated-block hierarchy. | High-dependence admission frozen before outcomes; Q5/Q6 pass. | Same H5 family, no outcome-selected cutoff. | Persistent community dominance/no reversal under admitted high dependence supports the countercondition; clear reversal under adequate admitted high dependence is adverse; inadequate support = `NOT_EVALUABLE`. |
| **H6 / P6 — prospective transport** **REQUIRED FOR NEE ROUTE** | The frozen H2 mapping and outcome-state logic are challenged prospectively in *Farfugium japonicum* without retuning; the same H5 coordinates are carried where estimable. | Same plant-state × effective-community mapping; same dependence/aggregation definitions when supported. | Prespecified comparable reproductive endpoint. | Independent *Farfugium* natural context. | Context/site/time units admitted outcome-blind under R1b; no focal-outcome-driven remapping. | Apply frozen mapping without changing predictor direction, endpoint family or aggregation rule. | P6 cannot rescue adverse H1-H5. Existing secondary metadata do not count as P6. |

## Cross-hypothesis quality gates

| Gate | Requirement | Failure state |
|---|---|---|
| **Q0 scope** | named focal and transport population/site/time registry passes outcome-blind feasibility and block-independence rules | NEE confirmatory execution does not open |
| **Q1 effort** | usable monitored flower-hours and zero-visit windows retained | affected exposure analyses `NOT_EVALUABLE` |
| **Q2 effectiveness** | sufficient background-controlled SVD coverage for R4 composition | H1/H2/H5 composition-dependent claims `NOT_EVALUABLE` |
| **Q3 dependency** | core treatments assigned and retained under frozen hierarchy | H4/dependent downstream claims `NOT_EVALUABLE` |
| **Q4 endpoint** | terminal mature-fruit/seed linkage sufficient | endpoint-dependent claims `NOT_EVALUABLE` |
| **Q5 replication** | independent plants and repeated blocks satisfy pilot-frozen R3 precision for H2 and conditional H5 | confirmatory effect decision withheld |
| **Q6 prediction** | H2/H5 estimands identifiable without post-hoc simplification/outcome-selected strata | H2/H5 `NOT_EVALUABLE` |
| **Q7 breadth** | second prospective independent context feasible under same mapping | NEE route closes; retain EL/Ecology route rather than weakening H5 |

## H5 pre-pilot scale screen

Frozen benchmark rows:

| low-dependence benchmark | recruited design scale | crossover separation |
|---:|---:|---:|
| 16 blocks × 16 plants | 256 | 0.5425 |
| 32 blocks × 16 plants | 512 | 0.8350 |
| 48 blocks × 16 plants | 768 | 0.9000 |

Near-boundary shared dependence remained difficult even at 1536 recruited plants, whereas high dependence increasingly separated the predicted no-crossover side. The actionable result is therefore **block structure + dependence regime**, not a universal plant count. Final R3 must be rebuilt from empirical pilot dispersion, support and attrition.

## R1b — exact registry still open

R1 is not fully closed until the following are filled prospectively:

1. actual named *Campanula* population/site units rather than island labels alone;
2. actual named *Farfugium* transport population/site units;
3. exact predeclared time windows and block-construction rule;
4. eligible flowering-plant counts and independence basis;
5. SVD background-control feasibility and all three reproductive treatments at each admitted context;
6. feasibility of the outcome-blind dependence coordinate before reproductive outcomes;
7. access/permit/phenology exclusion reasons independent of effect direction.

Oshima + Kozushima are therefore not automatically admitted merely because they are logistically convenient or already represented in prior work.

## Retreat line

If R3 later shows confirmatory H5 infeasible, **do not weaken H5**. H1-H4 remain confirmatory and H5 becomes descriptive/exploratory for the single-system EL/Ecology study; full confirmatory H5 plus prospective transport is retained for an expanded NEE design. If P6 is infeasible but focal H5 is strong, route the frozen single-system design to EL/Ecology rather than back-promoting old metadata.
